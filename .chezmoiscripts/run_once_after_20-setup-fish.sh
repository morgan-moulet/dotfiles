#!/usr/bin/env bash
# ==============================================================================
# run_once_after_20-setup-fish.sh
# Configures Fisher, git plugin, terminal features and default shell
# ==============================================================================
set -euo pipefail

if command -v fish >/dev/null 2>&1; then
  echo "==> [chezmoi] Setting up Fisher and Git plugin in Fish..."
  fish -c "curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher && fisher install jhillyerd/plugin-git" || true
  fish -c "set -Ua fish_features no-keyboard-protocols" || true

  # Set Fish as default login shell if needed
  if [[ "$SHELL" != *"fish"* ]]; then
    echo "==> Changing default shell to Fish..."
    if command -v sudo >/dev/null 2>&1; then
      sudo chsh -s "$(which fish)" "$USER" || chsh -s "$(which fish)" || true
    else
      chsh -s "$(which fish)" || true
    fi
  fi
fi

echo "==> [chezmoi] Fish setup complete!"
