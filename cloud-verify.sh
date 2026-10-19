#!/usr/bin/env bash
# Static checks only: never source configs or stow into the real home.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
for tool in bash sh zsh python3 git stow; do
  command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }
done
check_syntax() {
  local shell="$1" file="$2"
  # Syntax diagnostics can include config contents; report the path only.
  if ! "$shell" -n "$file" >/dev/null 2>&1; then
    echo "FAIL syntax: $file (inspect locally without sharing values)" >&2
    exit 1
  fi
  echo "PASS syntax: $file"
}
check_syntax bash cloud-verify.sh
check_syntax bash bootstrap.sh
check_syntax bash claude/.claude/save-at-session-end.sh
check_syntax bash claude/.claude/statusline-command.sh
check_syntax sh local/bin/qwen-exec
check_syntax zsh zsh/.zshrc
check_syntax zsh p10k/.p10k.zsh
python3 - <<'PYJSON'
import json
import ast
import pathlib
import subprocess
paths = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "*.json"]).decode().split("\0")
for name in filter(None, paths):
    try:
        json.loads(pathlib.Path(name).read_text())
    except (ValueError, OSError):
        raise SystemExit(f"FAIL JSON: {name} (contents omitted)")
    print(f"PASS JSON: {name}")
ast.parse(pathlib.Path("agent-links.py").read_text())
ast.parse(pathlib.Path("test_agent_links.py").read_text())
print("PASS Python syntax: installer and regression tests")
PYJSON
python3 test_agent_links.py
target="$(mktemp -d)"
trap 'rm -rf -- "$target"' EXIT
# Explicit packages avoid treating documentation/automation as dotfiles.
stow --dir="$PWD" --target="$target" --simulate   claude codex cursor fonts gemini gh karabiner local p10k qwen roo tmux zsh
echo "PASS Stow simulation against an empty temporary target"
# Confirm native filenames and package symlinks on an actual disposable target.
# Configuration is linked but never sourced or executed.
stow --dir="$PWD" --target="$target" --no-folding claude codex cursor gemini qwen roo
# Exercise installer normalization and idempotence, never against the real home.
python3 agent-links.py --target "$target" --apply
python3 agent-links.py --target "$target" --check
python3 agent-links.py --target "$target" --apply
echo "Static checks passed; platform behavior and live integrations remain untested."
