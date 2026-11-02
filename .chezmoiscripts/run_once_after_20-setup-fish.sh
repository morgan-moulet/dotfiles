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
    chsh -s "$(which fish)" 2>/dev/null || true
  fi
fi

echo "==> [chezmoi] Fish setup complete!"
