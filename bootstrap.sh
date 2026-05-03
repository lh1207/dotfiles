#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME"

# Dirs that live in the repo but are NOT stow packages
NON_PACKAGES=(wallpapers)

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

is_excluded() {
  local name="$1"
  for excluded in "${NON_PACKAGES[@]}"; do
    [[ "$name" == "$excluded" ]] && return 0
  done
  return 1
}

echo "Stowing packages from $DOTFILES_DIR -> $TARGET"

for dir in "$DOTFILES_DIR"/*/; do
  package="$(basename "$dir")"
  if is_excluded "$package"; then
    echo "  skip  $package"
    continue
  fi
  echo "  stow  $package"
  stow --dir="$DOTFILES_DIR" --target="$TARGET" --restow "$package"
done

echo "Done."
