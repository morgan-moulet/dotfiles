# AI Instructions & Directives — Chezmoi Dotfiles (`dotfiles`)

> 🔀 **PR Lifecycle**: Never push directly to `origin/main`. Every modification MUST go through a feature branch pushed to `origin` (`git@github.com:morgan-moulet/dotfiles.git`) and a Pull Request against `main`.
> 🔒 **Secrets Hygiene**: Never commit private SSH keys, API tokens, or `.chezmoistate.boltdb`.
> 💬 **Transparent Reasoning**: Output 1–2 line progress updates before and after tool calls (`transparent-step-reasoning`).

---

## 1. Repository Purpose & Scope

Manages host user configuration files (`dot_gitconfig`, `dot_tmux.conf`, `dot_vimrc`, `private_dot_config/`, `private_dot_ssh/`) via **Chezmoi**.

---

## 2. Shared Engineering Skills (`.agents/skills.json` & `skills-lock.json`)

Managed declaratively from [`https://github.com/morgan-moulet/ai-skills`](https://github.com/morgan-moulet/ai-skills) via `npx skills` (external files ignored in Git via `.gitignore`):
- `agent-git-workflow`
- `conventional-commits`
- `missing-tool-management`
- `pr-code-review`
- `transparent-step-reasoning`

### Authorized Commit Scopes (`conventional-commits`)

| Scope | Target |
| :--- | :--- |
| `ssh` | SSH client configuration (`private_dot_ssh/`) |
| `git` | Git configuration (`dot_gitconfig`) |
| `shell` | Fish, Starship, environment.d (`private_dot_config/`) |
| `tmux` | Tmux configuration (`dot_tmux.conf`, `TMUX.md`) |
| `vim` | Vim configuration (`dot_vimrc`) |
| `agents` | `AGENTS.md`, `.agents/skills.json`, `skills-lock.json` |
| `ci` | GitHub Actions workflows (`.github/workflows/`) |
| `docs` | `README.md` and documentation |
