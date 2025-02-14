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
  - uv
  - node (through nvm)
- command line replacements
  - fzf
  - ~~delta (git-delta)~~
  - cargo
    - tldr
    - bat
    - fd-find
    - ripgrep
    - du-dust
    - (TODO review repo, pick a commit hash) zenith (cargo install --git https://github.com/bvaisvil/zenith.git)

Other tools, useful but not blocking install:

- gh
- jq
- yq
- direnv
- kubectl

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

## Philosophy

1. Maximize consistency everywhere
2. Minimize future cost to revise

### Philosophy in Practice

- For aliases, use a prefix of the command when possible.
    - If you're ever in an unsupported environment, muscle memory is still consistent with the default tooling (*Consistency*)
    - If you ever revise your aliases or resolve a collision then you can still retain any existing muscle memory (*Revision Cost*)
- Satisfy all (or every possible) tooling need with solely a terminal + a browser.
    - Fewer applications means fewer configs to update with changes (*Revision Cost*) and less config drift (*Consistency*)
    - If any of them phase in and out of use, configs break or are out-of-date
- Never do thrice, automate after twice
    - If it's not automated, it's not likely to stay up-to-date (*Consistency*)
    - And if it's manual to update and sync across environments, it's honerous to change (*Revision Cost*)
    - However, automation used less than yearly is often the worst of all worlds (if the automation itself breaks, you did twice the work and got no use out of it!)

- TODO...
    - keyboards,
    - vi bindings everywhere,
    - ephemeral environments,
    - remote development,
    - treat yearly setups like infra provisioning,
    - SSOT where possible for binaries/shortcuts/scripts/aliases/etc,

