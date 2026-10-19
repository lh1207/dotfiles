#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME"

# Explicit packages: new documentation/tool directories must never be installed.
PACKAGES=(claude codex cursor fonts gemini gh karabiner local p10k qwen roo tmux zsh)

# Check the instruction installer dependency before modifying the home.
command -v python3 >/dev/null || { echo "Error: Python 3 is required." >&2; exit 1; }

# Ensure stow is available
if ! command -v stow &>/dev/null; then
  if command -v brew &>/dev/null; then
    echo "Installing stow via Homebrew..."
    brew install stow
  else
    echo "Error: stow not found and Homebrew is not available. Install stow manually." >&2
    exit 1
  fi
fi

echo "Stowing packages from $DOTFILES_DIR -> $TARGET"

for package in "${PACKAGES[@]}"; do
  echo "  stow  $package"
  # Real parent directories keep agent runtime state outside this checkout.
  stow --dir="$DOTFILES_DIR" --target="$TARGET" --no-folding --restow "$package"
done

python3 "$DOTFILES_DIR/agent-links.py" --target "$TARGET" --apply
python3 "$DOTFILES_DIR/agent-links.py" --target "$TARGET" --check

echo "Done. Configure Cursor User Rules separately; see AGENT-SETUP.md."
