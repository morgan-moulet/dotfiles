# 🛠️ Dotfiles — Morgan's Workstations & Homelab

> Clean, minimalist terminal and shell configurations managed across Linux and macOS using [**Chezmoi**](https://www.chezmoi.io/).

---

## 📦 What's Included

* **Shell:** [Fish Shell](https://fishshell.com/) with autosuggestions and fast syntax highlighting.
* **Prompt:** [Starship](https://starship.rs/) prompt:
  * Two-line layout with Nerd Font icons on desktop terminals.
  * Automatic fallback to a clean text-only layout on mobile or basic terminals.
* **Modern CLI Tools:**
  * **`eza`** for colorized, git-aware directory listings (`ls`, `ll`, `lt`).
  * **`bat`** for syntax-highlighted file viewing (`cat`).
  * **`fd`** for fast and intuitive file searching (`find`).
  * **`ripgrep`** (`rg`) for rapid recursive text search (`grep`).
  * **`duf`** & **`dust`** for modern disk usage visualization (`df`, `du`).
  * **`btop`** for interactive system resource monitoring (`top`).
* **Navigation & History:**
  * **`zoxide`** (`z <folder>`) for directory jumping based on frequency and recency.
  * **`fzf`** fuzzy finding integration for command history (`Ctrl+R`) and file selection (`Ctrl+T`, `Alt+C`).
* **Git Productivity:**
  * Dynamic expanding abbreviations via [`jhillyerd/plugin-git`](https://github.com/jhillyerd/plugin-git) (`gst`, `gco`, `gaa`, `gcm`, `gwip`, etc.).

---

## 🚀 Installation & Setup

### Step 1: Install Base Packages

Choose your system's package manager:

#### 🔴 Rocky Linux / RHEL / Fedora (`dnf`)
```bash
sudo dnf install -y epel-release
sudo dnf install -y fish git curl fzf ripgrep btop util-linux-user bat
```

#### 🟣 Debian / Ubuntu (`apt`)
```bash
sudo apt update
sudo apt install -y fish git curl fzf ripgrep btop batcat fdfind
# Standardize binary aliases if needed
[[ -x /usr/bin/batcat && ! -e "$HOME/.local/bin/bat" ]] && ln -sf /usr/bin/batcat "$HOME/.local/bin/bat" || true
[[ -x /usr/bin/fdfind && ! -e "$HOME/.local/bin/fd" ]] && ln -sf /usr/bin/fdfind "$HOME/.local/bin/fd" || true
```

#### 🔵 Arch Linux / Manjaro (`pacman`)
```bash
sudo pacman -S --needed fish git curl fzf ripgrep btop eza bat fd zoxide starship
```

#### 🍏 macOS (`brew`)
```bash
brew install fish git curl fzf ripgrep btop eza bat fd zoxide starship
```

#### 🟢 openSUSE (`zypper`)
```bash
sudo zypper install -y fish git curl fzf ripgrep btop bat zoxide
```

---

### Step 2: Install Modern CLI Tools (if not in package manager)

```bash
mkdir -p ~/.local/bin

# Starship Prompt
curl -sS https://starship.rs/install.sh | sh -s -- -y -b ~/.local/bin

# Zoxide (smarter cd)
curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh

# Eza (modern ls)
curl -sL https://github.com/eza-community/eza/releases/download/v0.23.5/eza_x86_64-unknown-linux-musl.tar.gz | tar -xz -C ~/.local/bin/ ./eza
chmod +x ~/.local/bin/eza
```

---

### Step 3: Apply Configurations with Chezmoi

Apply dotfiles directly from GitHub:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply morgan-moulet
```
*(Or via SSH: `sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply git@github.com:morgan-moulet/dotfiles.git`)*

---

### Step 4: Setup Fisher & Git Plugin (inside Fish)

Launch Fish and install the Git plugin:

```bash
fish -c "curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher && fisher install jhillyerd/plugin-git"
```

To set Fish as your default shell:
```bash
chsh -s "$(which fish)"
```

---

## 🔄 Daily Usage Commands

* **Check differences between machine and repo:**
  ```bash
  chezmoi diff
  ```
* **Apply latest changes from the repo:**
  ```bash
  chezmoi apply
  ```
* **Pull latest changes from GitHub and apply:**
  ```bash
  chezmoi update
  ```
* **Edit a managed configuration:**
  ```bash
  chezmoi edit ~/.config/fish/config.fish
  ```
* **Add a new configuration file to track:**
  ```bash
  chezmoi add ~/.gitconfig
  ```
