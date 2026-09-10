# dotfiles

Personal configs. Linux and MacOS support.

Generally biased for Pop!OS 24.04 / COSMIC (for code-as-config: settings, keybinds, and extras).

## Quickstart

Install prerequisites on Pop!OS (macOS already includes Zsh; install Apple Command Line Tools with `xcode-select --install` if Git is missing):

```sh
sudo apt update && sudo apt install -y ca-certificates curl git zsh imagemagick
```

Install chezmoi, clone, and inspect:

```sh
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- -b "$HOME/.local/bin" init https://github.com/CSRessel/dotfiles.git && "$HOME/.local/bin/chezmoi" status
```

Enter Git email and select optional modules when prompted; none are enabled by default.
The checkout is `~/.local/share/chezmoi`, local configuration is `~/.config/chezmoi/chezmoi.toml`.

## Overview

The shared base is Zsh, Bash fallback, Git, tmux, explicit tool shortcuts and aliases. A series of composable modules support the other configs. The optional `dev-tools` module provides a global mise configuration and shared shell integration.

For initial checkout, compose desired modules with `chezmoi init` and then review the diff.
Change later selections with `chezmoi edit-config`

## Docs

- [Module settings overview](docs/modules.md)
- [Expected packages and defaults](docs/packages.md)
- [Development tools and environments](docs/dev-tools.md)


## Philosophy

1. Maximize consistency everywhere
2. Minimize future cost to revise

### Rules

- For aliases, use a prefix of the command when possible.
    - If you're ever in an unsupported environment, muscle memory is still consistent with the default tooling (*Consistency*)
    - If you ever revise your aliases or resolve a collision then you can still retain any existing muscle memory (*Revision Cost*)
- Satisfy all tooling with only terminal + browser, if possible.
    - Fewer applications means fewer configs to update (*Revision Cost*) and less config drift (*Consistency*)
    - Proprietary tools will phase in and out of use, meaning configs break over time
- Write everything twice, automate on thrice
    - If it's not automated, it's not likely to stay up-to-date (*Consistency*)
    - And if it's manual to make updates across environments, it's honerous to change (*Revision Cost*)
    - (However, automation used less than yearly is the worst of all worlds)
