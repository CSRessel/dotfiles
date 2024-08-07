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
  - fd (cargo install fd-find)
  - ripgrep (cargo install rigrep)
  - bat (rust-bat)
  - fzf
  - delta (git-delta)
  - dust (cargo install du-dust)

## Getting Started

Install binary, for example:

> [One-line binary install](https://www.chezmoi.io/install/#one-line-binary-install)

Then configure for local files and templating:

```
mkdir -p ~/.config/chezmoi/
touch ~/.config/chezmoi/chezmoi.toml
echo "[data]"                           >> ~/.config/chezmoi/chezmoi.toml
echo "  email = \"<EMAIL>@gmail.com\"" >> ~/.config/chezmoi/chezmoi.toml

chezmoi cd
git remote add origin https://github.com/CSRessel/dotfiles.git
git pull origin master
exit

chezmoi status
chezmoi diff
```

## Configuration Philosophy

1. Maximize consistency everywhere
2. Minimize future cost to revise
3. Never do something thrice, automate it after twice

### Philosophy in Practice

- For aliases, use a prefix of the command when possible.
    - If you're ever in an unsupported environment, muscle memory is still consistent with the default tooling (*Consistency*), and if you ever revise your aliases or resolve a collision then you can still retain any existing muscle memory (*Revision Cost*).
- TODO...
    - keyboards,
    - vi bindings everywhere,
    - ephemeral environments,
    - treat yearly setups like infra provisioning,
    - SSOT where possible for binaries/shortcuts/scripts/aliases/etc),

