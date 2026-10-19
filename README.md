# dotfiles

> Dotfiles for environments with stow installed. Designed for simple & easy deployment.

## Overview

This repository contains my personal dotfiles, organized and maintained for seamless management and deployment across different systems using [GNU Stow](https://www.gnu.org/software/stow/). The collection is designed to be straightforward and compatible with any Unix-like environment where Stow is available.

## Structure

Each package directory contains configuration for a program (for example, Zsh or tmux). GNU Stow creates symlinks in the corresponding locations in your home directory.

## Getting Started

### Prerequisites

- A Unix-like operating system (Linux, macOS, WSL, etc.)
- [GNU Stow](https://www.gnu.org/software/stow/) installed

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/lh1207/dotfiles.git ~/dotfiles
   cd ~/dotfiles
   ```

2. **Stow your desired configurations:**
   For example, to stow your Zsh and tmux configurations:
   ```sh
   stow --no-folding zsh
   stow --no-folding tmux
   ```
   This will symlink the configuration files into your `$HOME` directory.

### Updating

Pull the latest changes and re-run the `stow` commands as needed:
```sh
cd ~/dotfiles
git pull
stow --no-folding <directory>
```

## Directory List

- Agent instructions: `codex/`, `claude/`, `cursor/`, `gemini/`, `qwen/`, `roo/`
- Shell and terminal: `zsh/`, `p10k/`, `tmux/`
- Tools and desktop: `local/`, `gh/`, `karabiner/`, `fonts/`
- `wallpapers/` contains assets and is not a Stow package.

## Shared agent instructions

The only shared workflow source is `codex/.codex/INSTRUCTIONS.md`, exposed as
`~/.codex/INSTRUCTIONS.md`. Read [AGENT-SETUP.md](AGENT-SETUP.md) for native
entry points, model guidance, installation, backups, and verification limits.

For an existing home, prefer the narrowly scoped instruction installer:

```sh
python3 agent-links.py          # preview
python3 agent-links.py --apply  # backs up replaced entries; installs links only
python3 agent-links.py --check
```

It does not install settings, hooks, tools, or credentials. Cursor needs a separate
global User Rule in its native UI; home `.cursor/rules` links are only templates.
Native Windows and WSL caveats are documented in AGENT-SETUP.md. Keep this checkout in
place; installed links refer to it. Review existing files before installing other
packages. After raw Stow on Linux, run the instruction installer to create Claude's
uppercase native entry point. `bootstrap.sh` installs an explicit package list into the real home and
may invoke Homebrew for Stow; it is not a verification or cloud setup command.

Run `bash cloud-verify.sh` for static checks and disposable instruction-link tests.
Do not source personal configuration during verification. See
[CODEX-CLOUD.md](CODEX-CLOUD.md) for the cloud pilot and platform limits.

## Customization

Feel free to fork this repository and modify the dotfiles to suit your own workflow.
