# dotfiles

> Dotfiles for environments with stow installed. Designed for simple & easy deployment.

## Overview

This repository contains my personal dotfiles, organized and maintained for seamless management and deployment across different systems using [GNU Stow](https://www.gnu.org/software/stow/). The collection is designed to be straightforward and compatible with any Unix-like environment where Stow is available.

## Structure

Each directory within the repository corresponds to a set of configuration files for a specific program (e.g., bash, vim, git). GNU Stow is used to create symlinks from these directories into the appropriate places in your home directory.

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
   For example, to stow your bash and vim configurations:
   ```sh
   stow bash
   stow vim
   ```
   This will symlink the configuration files into your `$HOME` directory.

### Updating

Pull the latest changes and re-run the `stow` commands as needed:
```sh
cd ~/dotfiles
git pull
stow <directory>
```

## Directory List

<!-- Example; will be replaced with actual directories -->
- bash/
- vim/
- git/
- ...

## Customization

Feel free to fork this repository and modify the dotfiles to suit your own workflow.
