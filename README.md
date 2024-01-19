# dotfiles

[twpayne/chezmoi](https://github.com/twpayne/chezmoi)

[Quick Start](https://www.chezmoi.io/quick-start/)

## Pre-Install Dependencies

Tools that will be configured by chezmoi below:

- git
- neovim
  - LunarVim
- zsh
  - oh-my-zsh
  - zsh-kubectl-prompt
- tmux
- direnv
- input-remapper
- Tridactyl

Tools needed for my aliases and vim to work:

- lang and toolchains
  - rustup
  - node (through nvm)
  - python3 (through the system)
- command line replacements
  - fd (fd-find)
  - ripgrep
  - bat
  - fzf
  - delta (git-delta)
  - dust (cargo install du-dust)

## Getting Started

> **Note**: This relies on my personal computer having the username `clifford`, and my work machine having the username of `clifford.ressel`.

Install binary, for example:

> [One-line binary install](https://www.chezmoi.io/install/#one-line-binary-install)

Then configure for local files and templating:

```
mkdir -p ~/.config/chezmoi/
touch ~/.config/chezmoi/chezmoi.toml
echo "[data]"                           >> ~/.config/chezmoi/chezmoi.toml
echo "  email = \"CSRessel@gmail.com\"" >> ~/.config/chezmoi/chezmoi.toml

chezmoi cd
git remote add origin https://github.com/CSRessel/dotfiles.git
git pull origin master
exit

chezmoi status
chezmoi diff
```
