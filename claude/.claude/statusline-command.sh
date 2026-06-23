#!/bin/bash
# Claude Code status line - Powerlevel10k style
# Format: ~/path  on  branch ✚

input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')

# Abbreviate home directory to ~
dir="${cwd/#$HOME/~}"

# Git info (skip optional locks to avoid contention)
git_segment=""
if git -C "$cwd" --no-optional-locks rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  branch=$(git -C "$cwd" --no-optional-locks symbolic-ref --short HEAD 2>/dev/null)
  if [ -z "$branch" ]; then
    branch=$(git -C "$cwd" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
  fi

  dirty=""
  if [ -n "$(git -C "$cwd" --no-optional-locks status --porcelain 2>/dev/null)" ]; then
    dirty=" ✚"
  fi

  if [ -n "$branch" ]; then
    git_segment="  on  ${branch}${dirty}"
  fi
fi

# Dimmed colors: directory in dim cyan, "on" label dim, branch in dim yellow
printf "\033[2;36m%s\033[0m\033[2m%s\033[0m" "$dir" "$git_segment"
