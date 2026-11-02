#!/usr/bin/env bash
# ==============================================================================
# run_once_after_20-setup-fish.sh
# Configures Fisher, git plugin, terminal features and default shell
# ==============================================================================
set -euo pipefail

if command -v fish >/dev/null 2>&1; then
  echo "==> [chezmoi] Setting up Fisher and Git plugin in Fish..."
  mkdir -p "$HOME/.config/fish/functions"
  if ! fish -c "type -q fisher" 2>/dev/null; then
    curl -sSfL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish -o "$HOME/.config/fish/functions/fisher.fish"
  fi
  fish -c "fisher update" </dev/null || true
  fish -c "set -Ua fish_features no-keyboard-protocols" || true

  # Set Fish as default login shell if needed
  if [[ "$SHELL" != *"fish"* ]]; then
    echo "==> Changing default shell to Fish..."
    chsh -s "$(which fish)" 2>/dev/null || true
  fi
fi

echo "==> [chezmoi] Fish setup complete!"
