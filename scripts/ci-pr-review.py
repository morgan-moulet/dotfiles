#!/usr/bin/env python3
"""
Homelab Two-Stage Zero-Noise PR Audit & Code Review Engine for GitHub Actions.
Combines:
  - Stage 1: Deterministic Gate (Docker Compose config, :latest tag check, secret check,
             and Alibaba Open Code Review `ocr delegate preview` + `ocr delegate rule`)
  - Stage 2: Context-Aware AI Code Review via Google Gemini REST API (zero pip dependencies)
             with resilient model cascade (Gemini 4 / Gemini 3.8 -> 3.5) against AGENTS.md.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(os.environ.get("GITHUB_WORKSPACE", str(Path.cwd()))).resolve()
REPORT_PATH = Path("/tmp/pr-ci-report.md")

GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-4-argon",
    "gemini-4-hydrogen",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]


def run_cmd(cmd: List[str], cwd: Path = REPO_ROOT, timeout: int = 120) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as exc:
        return 1, "", str(exc)


def run_gitleaks_diff(diff_text: str) -> Tuple[bool, str, str]:
    """
    Scan only added lines in the PR diff using zricethezav/gitleaks:v8.21.2 via stdin
    (avoids host path mapping issues in Rootless Docker).
    Returns (passed, status_badge, details_output).
    """
    added_lines = "\n".join(
        line[1:] for line in diff_text.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )
    if not added_lines.strip():
        return True, "✅ Passed (no added lines)", ""

    try:
        proc = subprocess.run(
            ["docker", "run", "--rm", "-i", "zricethezav/gitleaks:v8.21.2", "stdin", "--no-banner", "--redact", "-v"],
            input=added_lines,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        combined = "\n".join(filter(None, [proc.stdout.strip(), proc.stderr.strip()])).strip()
        if proc.returncode == 0:
            return True, "✅ Passed (`gitleaks` 0 leaks)", ""
        if proc.returncode == 1 and "leaks found:" in combined:
            return False, "❌ Secrets detected (`gitleaks`)!", combined
        return True, "⚠️ Skipped (docker/gitleaks unavailable)", combined
    except Exception as exc:
        return True, f"⚠️ Skipped (`{str(exc)[:50]}`)", ""


def check_compose() -> Tuple[str, bool, str]:
    has_compose = (REPO_ROOT / "docker-compose.yml").exists() or (REPO_ROOT / "compose.yml").exists()
    if not has_compose:
        return "⚪ N/A (no Compose file)", True, ""
    env_file = REPO_ROOT / ".env"
    demo_file = REPO_ROOT / ".env.demo"
    if not demo_file.exists():
        demo_file = REPO_ROOT / ".env.example"
    created_temp_env = False
    try:
        if not env_file.exists() and demo_file.exists():
            shutil.copyfile(demo_file, env_file)
            created_temp_env = True
        rc, out, err = run_cmd(["docker", "compose", "config", "-q"])
        combined = "\n".join(filter(None, [out, err])).strip()
        lines = [
            line for line in combined.splitlines()
            if "exists but was not created by compose" not in line
            and "Set `external: true` to use an existing network" not in line
        ]
        cleaned = "\n".join(lines).strip()
        if rc == 0:
            status = "✅ Valid (with warnings)" if cleaned else "✅ Valid (`exit 0`)"
            return status, True, cleaned
        return "❌ Failed", False, cleaned
    finally:
        if created_temp_env and env_file.exists():
            try:
                env_file.unlink()
            except OSError:
                pass


def run_alibaba_ocr(base_ref: str) -> Tuple[str, str, str]:
    """
    Execute Alibaba Open Code Review (`ocr delegate preview` and `ocr delegate rule`)
    using `--from <base_ref> --to HEAD --format json`.
    Returns (status_badge, markdown_summary, rules_context_for_llm).
    """
    ocr_bin = shutil.which("ocr")
    if ocr_bin:
        base_cmd = [ocr_bin]
    else:
        base_cmd = ["npx", "--yes", "@alibaba-group/open-code-review"]

    preview_cmd = base_cmd + [
        "delegate",
        "preview",
        "--from",
        base_ref,
        "--to",
        "HEAD",
        "--format",
        "json",
    ]
    rc, out, err = run_cmd(preview_cmd, timeout=90)
    if rc != 0 or not out:
        err_msg = (err or out or "unknown error").splitlines()[0] if (err or out) else "unknown error"
        return f"⚠️ Error (`{err_msg[:80]}`)", "", ""

    try:
        json_start = out.find("{")
        if json_start == -1:
            return "⚠️ Non-JSON output", "", ""
        data = json.loads(out[json_start:])
    except Exception as exc:
        return f"⚠️ Parse error (`{exc}`)", "", ""

    review_files = data.get("reviewable_files") or data.get("review_files") or []
    excluded_files = data.get("excluded_files") or []
    total_ins = data.get("total_insertions", 0)
    total_del = data.get("total_deletions", 0)

    summary_lines = [
        f"- **Alibaba OCR (`ocr delegate preview`)**: **{len(review_files)}** reviewable file(s), **{len(excluded_files)}** excluded file(s) (`+{total_ins} / -{total_del}` lines)"
    ]
    file_paths: List[str] = []
    for item in review_files[:20]:
        if isinstance(item, dict):
            p = item.get("path") or item.get("file") or ""
            status = item.get("status", "modified")
            ins = item.get("insertions", item.get("added", 0))
            dels = item.get("deletions", item.get("deleted", 0))
            if p:
                file_paths.append(p)
                summary_lines.append(f"  - `{p}` ({status}: `+{ins} / -{dels}`)")
        elif isinstance(item, str):
            file_paths.append(item)
            summary_lines.append(f"  - `{item}`")

    rules_context = ""
    if file_paths:
        rule_cmd = base_cmd + [
            "delegate",
            "rule",
            "--from",
            base_ref,
            "--to",
            "HEAD",
            "--format",
            "json",
        ] + file_paths[:15]
        r_rc, r_out, _ = run_cmd(rule_cmd, timeout=60)
        if r_rc == 0 and r_out:
            rules_context = r_out[:4000]

    return f"✅ Passed ({len(review_files)} reviewable, {len(excluded_files)} excluded)", "\n".join(summary_lines), rules_context


def run_gemini_review(
    api_key: str,
    base_ref: str,
    diff_text: str,
    changed_files: str,
    ocr_summary: str,
    ocr_rules: str,
    deterministic_issues: List[str],
) -> Tuple[str, str]:
    """
    Call Google Gemini REST API directly (zero third-party pip dependencies) with
    resilient model cascade and the Two-Stage Zero-Noise Conventional Comments prompt.
    """
    agents_md = ""
    agents_path = REPO_ROOT / "AGENTS.md"
    if agents_path.exists():
        agents_md = agents_path.read_text(encoding="utf-8", errors="replace")[:6000]

    rule_04 = ""
    rule_04_path = REPO_ROOT / ".agents" / "rules" / "04-git-and-pr-lifecycle.md"
    if rule_04_path.exists():
        rule_04 = rule_04_path.read_text(encoding="utf-8", errors="replace")[:4000]

    pr_num = os.environ.get("PR_NUMBER", "")
    pr_title = os.environ.get("PR_TITLE", "")
    pr_author = os.environ.get("PR_AUTHOR", "maintainer")

    prompt = f"""You are the Autonomous Code Review Engine for the 'jenko' & 'uruk' Docker Homelab.
You are auditing Pull Request #{pr_num} ('{pr_title}') by @{pr_author} (comparing {base_ref}...HEAD).

### REPOSITORY CONTRACT (AGENTS.md):
{agents_md}

### PR REVIEW & CONVENTIONAL COMMENTS STANDARD (Rule 04):
{rule_04}

### STAGE 1 — DETERMINISTIC & ALIBABA OCR GATE RESULTS:
- Deterministic Issues: {deterministic_issues if deterministic_issues else 'None (All passed)'}
- Changed Files:
{changed_files}
- Alibaba OCR Summary:
{ocr_summary}
- Alibaba OCR Resolved Rules:
{ocr_rules or 'Standard infrastructure & bash defensive rules apply.'}

### GIT DIFF TO AUDIT:
```diff
{diff_text[:18000]}
```

### INSTRUCTIONS (TWO-STAGE ZERO-NOISE STANDARD):
1. Do NOT output bureaucratic multi-row tables with `N/A` rows for unrelated domains.
2. Evaluate only what applies to the modified files across 3 engineering lenses:
   - **Correctness & Runtime Safety**: Logic bugs, shell quoting, `set -euo pipefail`, Docker Compose syntax, or service regressions.
   - **Security & Isolation Boundaries**: Leaked secrets/keys, unpinned `:latest` tags, automated `sudo`, or unintended port exposure.
   - **Project Contract (`AGENTS.md` & Docs)**: Adherence to repository standards and documentation synchronization.
3. Write the review explanations in **French** (while keeping Conventional Comments labels `issue (blocking):`, `suggestion (non-blocking):`, `nit:`, `praise:` in English).
4. Format your response strictly as follows:

- **Verdict**: `✅ APPROVE` (or `🚨 REQUEST_CHANGES` if blocking issues exist)

#### 💬 Findings (Conventional Comments)
- **[`path/to/file:L10`](path/to/file)** **issue (blocking):** <explanation if any>
- **[`path/to/file:L25`](path/to/file)** **suggestion (non-blocking):** <concrete improvement if any>
- **[`path/to/file:L5`](path/to/file)** **praise:** <1 concise highlight of good engineering>
*(If there are zero blocking issues or suggestions, write `Aucun problème bloquant ni régression identifié.` and 1 brief `praise:` bullet.)*
"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    errors: List[str] = []
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                candidates = resp_data.get("candidates") or []
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts") or []
                    text = "".join(p.get("text", "") for p in parts).strip()
                    if text:
                        return f"✅ `gemini:{model}`", text
        except urllib.error.HTTPError as http_err:
            errors.append(f"{model}: HTTP {http_err.code}")
        except Exception as exc:
            errors.append(f"{model}: {str(exc)[:60]}")

    return "⚠️ Gemini unavailable", f"⚠️ Échec de l'appel Gemini après cascade : `{'; '.join(errors)}`"


def main() -> int:
    base_branch = os.environ.get("GITHUB_BASE_REF", "main")
    base_ref = f"origin/{base_branch}"

    exit_code = 0
    deterministic_issues: List[str] = []

    # 1. Docker Compose Validation
    compose_status, compose_ok, compose_output = check_compose()
    if not compose_ok:
        exit_code = 1
        deterministic_issues.append(f"Docker Compose syntax error: {compose_output}")

    # 2. Git diff & Changed files
    _, changed_files, _ = run_cmd(["git", "diff", "--name-status", f"{base_ref}...HEAD"])
    _, changed_names, _ = run_cmd(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    file_list = [f for f in changed_names.splitlines() if f.strip()]
    file_count = len(file_list)

    _, diff_text, _ = run_cmd(["git", "diff", f"{base_ref}...HEAD"])

    # 3. Unpinned :latest tag check in Compose files
    _, compose_diff, _ = run_cmd(["git", "diff", f"{base_ref}...HEAD", "--", "*compose*.yml"])
    latest_hits = [
        line for line in compose_diff.splitlines()
        if line.startswith("+") and not line.startswith("+++") and re.search(r"image:\s*\S+:latest\b", line)
    ]
    if latest_hits:
        latest_status = f"⚠️ {len(latest_hits)} unpinned `:latest` tag(s)"
        deterministic_issues.append(f"Unpinned :latest tag(s): {latest_hits}")
    else:
        latest_status = "✅ All image tags pinned"

    # 4. Secret & private key file check
    secret_files = [
        f for f in file_list
        if re.search(r"(^|/)\.env($|\.(?!demo|example))|\.(key|pem)$|id_ed25519$|id_rsa$", f)
    ]
    if secret_files:
        secret_status = f"❌ Sensitive file(s): `{', '.join(secret_files)}`"
        exit_code = 1
        deterministic_issues.append(f"Committed secret/key files: {secret_files}")
    else:
        secret_status = "✅ No `.env` or private key files"

    # 4b. Gitleaks secret scan on added diff lines
    gitleaks_ok, gitleaks_status, gitleaks_out = run_gitleaks_diff(diff_text)
    if not gitleaks_ok:
        exit_code = 1
        deterministic_issues.append(f"Gitleaks detected secret(s) in PR diff: {gitleaks_out[:400]}")

    # 5. Stage 1: Alibaba Open Code Review (ocr delegate)
    ocr_status, ocr_summary, ocr_rules = run_alibaba_ocr(base_ref)

    # 6. Stage 2: Gemini AI Review (if GEMINI_API_KEY is provided)
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    ai_model_badge = "⚪ Disabled (no `GEMINI_API_KEY`)"
    ai_review_md = ""
    if gemini_key:
        ai_model_badge, ai_review_md = run_gemini_review(
            api_key=gemini_key,
            base_ref=base_ref,
            diff_text=diff_text,
            changed_files=changed_files,
            ocr_summary=ocr_summary,
            ocr_rules=ocr_rules,
            deterministic_issues=deterministic_issues,
        )

    # 7. Build unified Zero-Noise Markdown report
    _, node_ver, _ = run_cmd(["node", "-v"])
    report_lines = [
        f"### 🤖 Homelab CI & Code Review (`jenko-runner` · Node `{node_ver or 'N/A'}`)",
        "",
        "| Gate | Status |",
        "| :--- | :--- |",
        f"| **1. Docker Compose Syntax** (`docker compose config -q`) | {compose_status} |",
        f"| **2. Image Tag Pinning** (Rule 02) | {latest_status} |",
        f"| **3. Secrets & Key Hygiene** | {secret_status} |",
        f"| **4. Gitleaks Diff Scan** (`v8.21.2`) | {gitleaks_status} |",
        f"| **5. Alibaba OCR Gate** (`ocr delegate`) | {ocr_status} |",
        f"| **6. Gemini AI Code Review** | {ai_model_badge} |",
        f"| **7. Modified Scope** | **{file_count}** file(s) |",
        "",
    ]

    if ocr_summary:
        report_lines.extend([
            "<details><summary>🔍 Stage 1 — Alibaba OCR File Grouping (<code>ocr delegate preview</code>)</summary>",
            "",
            ocr_summary,
            "",
            "</details>",
            "",
        ])

    if ai_review_md:
        report_lines.extend([
            "---",
            f"### 🧠 Stage 2 — Context-Aware AI Code Review ({ai_model_badge})",
            "",
            ai_review_md,
            "",
        ])

    if compose_output:
        title = "❌ Docker Compose Error Output" if not compose_ok else "⚠️ Docker Compose Warnings"
        report_lines.extend([
            f"<details><summary>{title}</summary>",
            "",
            "```text",
            compose_output,
            "```",
            "</details>",
            "",
        ])

    if gitleaks_out and not gitleaks_ok:
        report_lines.extend([
            "<details open><summary>🚨 Gitleaks Secret Scan Findings (Redacted)</summary>",
            "",
            "```text",
            gitleaks_out,
            "```",
            "</details>",
            "",
        ])

    if latest_hits:
        report_lines.extend([
            "<details><summary>⚠️ Unpinned <code>:latest</code> lines</summary>",
            "",
            "```diff",
            "\n".join(latest_hits),
            "```",
            "</details>",
            "",
        ])

    report_lines.extend([
        f"<details><summary>📁 Changed Files ({file_count})</summary>",
        "",
        "```text",
        changed_files or "(none)",
        "```",
        "</details>",
    ])

    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"CI report written to {REPORT_PATH}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
