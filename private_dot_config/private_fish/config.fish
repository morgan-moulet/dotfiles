# ~/.config/fish/config.fish — Modern, Fast & Homelab-Ready Fish Configuration

# -----------------------------------------------------------------------------
# 1. Environment & Paths
# -----------------------------------------------------------------------------
# Dynamically determine user runtime directory and rootless Docker socket
set -l current_uid (id -u)
if not set -q XDG_RUNTIME_DIR; and test -d "/run/user/$current_uid"
    set -gx XDG_RUNTIME_DIR "/run/user/$current_uid"
end

if test -S "/run/user/$current_uid/docker.sock"
    set -gx DOCKER_HOST "unix:///run/user/$current_uid/docker.sock"
end
set -gx VOLTA_HOME "$HOME/.volta"

# Prepend user local binaries to PATH
fish_add_path -m "$HOME/.local/bin" "$HOME/bin" "$VOLTA_HOME/bin"

# Disable default greeting
set -g fish_greeting ""

# Fix for mobile SSH / older terminals (e.g. JuiceSSH): disable kitty keyboard protocol probes
set -g fish_features no-keyboard-protocols

# -----------------------------------------------------------------------------
# 2. Interactive Shell Integrations
# -----------------------------------------------------------------------------
if status is-interactive
    # Auto-detect terminal font/type: use plain prompt on mobile/linux consoles, Nerd Fonts otherwise
    if test "$TERM" = "linux" -o "$TERM" = "dumb" -o "$TERM" = "vt100"
        set -gx STARSHIP_CONFIG "$HOME/.config/starship-plain.toml"
    else
        set -gx STARSHIP_CONFIG "$HOME/.config/starship.toml"
    end

    # Starship prompt
    if type -q starship
        starship init fish | source
    end

    # Zoxide (smarter cd command: 'z <dir>')
    if type -q zoxide
        zoxide init fish | source
    end

    # FZF key bindings (Ctrl+R history, Ctrl+T files, Alt+C cd)
    if type -q fzf
        if fzf --fish >/dev/null 2>&1
            fzf --fish | source
        else if functions -q fzf_key_bindings
            fzf_key_bindings
        end
    end
end

# -----------------------------------------------------------------------------
# 3. Modern CLI Tools (eza, bat, fd, rg, etc.)
# -----------------------------------------------------------------------------
if type -q eza
    # If on a plain terminal (TERM=linux), avoid glyphs in eza
    if test "$TERM" = "linux" -o "$TERM" = "dumb"
        alias ls="eza --group-directories-first"
        alias ll="eza -la --group-directories-first --git"
        alias lt="eza --tree --level=2"
    else
        alias ls="eza --icons=auto --group-directories-first"
        alias ll="eza -la --icons=auto --group-directories-first --git"
        alias lt="eza --tree --level=2 --icons=auto"
    end
    alias la="eza -a --group-directories-first"
else
    alias ll="ls -lah"
end

if type -q bat
    alias cat="bat -p --paging=never"
    alias bcat="bat"
end

if type -q fdfind
    alias fd="fdfind"
end

if type -q rg
    alias grep="rg"
end

if type -q duf
    alias df="duf"
end

if type -q dust
    alias du="dust"
end

if type -q btop
    alias top="btop"
end

# -----------------------------------------------------------------------------
# 4. Homelab & Docker Compose Shortcuts
# -----------------------------------------------------------------------------
alias d="docker"
alias dps="docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
alias dco="docker compose"
alias dcl="docker compose logs -f --tail=50"
alias dcps="docker compose ps"
alias dcup="docker compose up -d"
alias dcdown="docker compose down"
alias dcrestart="docker compose restart"
alias dcpull="docker compose pull"

# -----------------------------------------------------------------------------
# 5. Git Shortcuts (Compléments à jhillyerd/plugin-git)
# -----------------------------------------------------------------------------
# Le plugin gère déjà ga, gaa, gc, gco, gb, gd, gl (pull), gp (push), gp!, etc.
alias gs="git status -sb"
alias ggraph="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# -----------------------------------------------------------------------------
# 6. System & Utility Helpers
# -----------------------------------------------------------------------------
alias ports="ss -tulnp"
alias myip="curl -s ifconfig.me && echo"
alias reload="source ~/.config/fish/config.fish"

# Manual prompt switchers if needed
alias prompt-plain="set -gx STARSHIP_CONFIG ~/.config/starship-plain.toml"
alias prompt-nerd="set -gx STARSHIP_CONFIG ~/.config/starship.toml"

# -----------------------------------------------------------------------------
# 7. Tmux Multiplexer Shortcuts
# -----------------------------------------------------------------------------
if type -q tmux
    alias ta="tmux attach -t"
    alias tn="tmux new -s"
    alias tl="tmux ls"
    alias tk="tmux kill-session -t"
end
