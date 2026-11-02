# 🛠️ Dotfiles

> Centralized terminal and shell configuration managed across Linux workstations and servers (Debian, Ubuntu, Rocky Linux / RHEL) using [**Chezmoi**](https://www.chezmoi.io/).

---

## 📦 Features & Included Utilities

* **Shell:** [Fish Shell](https://fishshell.com/) with autosuggestions and fast completion.
* **Prompt:** [Starship](https://starship.rs/) cross-shell prompt:
  * Two-line layout with Nerd Font icons on desktop terminals.
  * Automatic fallback to a clean text-only layout on mobile or basic terminals.
* **Modern CLI Replacements:**
  * **`eza`** for colorized, git-aware directory listings (`ls`, `ll`, `lt`).
  * **`bat`** for syntax-highlighted file viewing (`cat`).
  * **`fd`** for fast and intuitive file searching.
  * **`ripgrep`** (`rg`) for rapid recursive text search.
  * **`duf`** & **`dust`** for modern disk usage visualization.
  * **`btop`** for interactive system resource monitoring.
* **Navigation & History:**
  * **`zoxide`** (`z <folder>`) for directory jumping based on frequency and recency.
  * **`fzf`** fuzzy finding integration for command history (`Ctrl+R`) and file selection (`Ctrl+T`, `Alt+C`).
* **Git Productivity:**
  * Package manager [Fisher](https://github.com/jorgebucaran/fisher) with [`jhillyerd/plugin-git`](https://github.com/jhillyerd/plugin-git) for dynamic expanding abbreviations (`gst`, `gco`, `gaa`, `gcm`, `gwip`, etc.).
* **Multi-Distribution Automation:**
  * Automated package installation for **Rocky Linux / RHEL / Fedora** (`dnf`).
  * Automated package installation for **Debian / Ubuntu** (`apt`).

---

## 🚀 Quick Start (One-Liner Installation)

On any fresh machine, run:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply morgan-moulet
```

### Hardened / Enterprise Systems (Rocky Linux, RHEL with `noexec` `/tmp`)
If your workstation or server mounts `/tmp` with `noexec` (causing `fork/exec: permission denied`), run the installer with a custom local temporary directory:

```bash
mkdir -p ~/.local/tmp && TMPDIR=$HOME/.local/tmp sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply git@github.com:morgan-moulet/dotfiles.git
```

This single command will:
1. Download and initialize Chezmoi.
2. Automatically detect the distribution (Rocky / RHEL / Fedora / Debian / Ubuntu).
3. Install missing system packages (`fish`, `git`, `curl`, `fzf`, `ripgrep`, `btop`) and modern CLI tools (`starship`, `zoxide`, `eza`).
4. Apply Fish and Starship configurations.
5. Set up Fisher with `jhillyerd/plugin-git` and configure Fish as the default shell.

---

## 🔄 Daily Usage Commands

* **Check diff between host and repository:**
  ```bash
  chezmoi diff
  ```
* **Apply configuration changes:**
  ```bash
  chezmoi apply
  ```
* **Edit a managed file:**
  ```bash
  chezmoi edit ~/.config/fish/config.fish
  ```
* **Add a new configuration file:**
  ```bash
  chezmoi add ~/.gitconfig
  ```
