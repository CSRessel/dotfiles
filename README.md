# dotfiles

Personal configs. Linux and MacOS support.

Generally biased for Pop!OS 24.04 / COSMIC (for code-as-config: settings, keybinds, and extras).

## Quickstart

Install prerequisites on Pop!OS (macOS already includes Zsh; install Apple Command Line Tools with `xcode-select --install` if Git is missing):

```sh
sudo apt update && sudo apt install -y ca-certificates curl git zsh
```

Install chezmoi, clone, and inspect:

```sh
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- -b "$HOME/.local/bin" init https://github.com/CSRessel/dotfiles.git && "$HOME/.local/bin/chezmoi" status
```

Enter Git email and select optional modules when prompted; none are enabled by default.
The checkout is `~/.local/share/chezmoi`, local configuration is `~/.config/chezmoi/chezmoi.toml`.

## Overview

The shared base is Zsh, Bash fallback, Git, tmux, explicit tool shortcuts and aliases. A series of composable modules support the other configs.

It does not currently handle language runtimes or development toolchains.
(Extras: catppuccin loads if installed. The contribution graph builds on apply when Cargo exists and displays in Zsh login shells.)

For initial checkout, compose desired modules with `chezmoi init` and then review the diff.
Change later selections with `chezmoi edit-config`; [module settings](docs/modules.md)
include per-machine Linux memory limits and the shortcut names.
To make Zsh login shell after installing it: `chsh -s "$(command -v zsh)"`, then log out and back in.

```sh
~/.local/bin/chezmoi diff
```

## Built-in keyboard

Add `"builtin-keyboard"` to your modules with `chezmoi edit-config`, then `chezmoi diff`.
Follow the [install/rollback runbook](docs/builtin-keyboard.md): Right Alt → Escape,
Caps Lock → Control, Left Control → volume down, Escape → Caps Lock,
Right Shift → Right Alt; Left Alt and Super stay normal.
Run `chezmoi apply`; once per script/rule version, it installs and activates the native udev hwdb rule via sudo
only when the required tools and matching internal keyboard are present.
It targets this Framework model's internal keyboard, leaving external keyboards alone.
## COSMIC desktop

Add `"cosmic"` to your modules with `chezmoi edit-config`, then `chezmoi diff` and
`chezmoi apply`. Native RON files capture wallpaper, compact appearance, panel/dock,
window/workspace preferences, pointer sensitivity, touchpad natural scrolling,
clock, and suspend settings. See the
[captured settings](docs/cosmic.md). Fonts will be a separate module.

## Fonts

Enable `fonts` alongside `cosmic`, then `chezmoi diff` and `chezmoi apply`.
Installs IBM Plex Sans with Noto fallback and FiraCode Nerd Font Mono, then sets
desktop and generic font defaults. [Details](docs/fonts.md).

## Boot appearance

Enable `boot-theme`, then `chezmoi diff` and `chezmoi apply` when ready. Installs
coffee for boot splash and lock for disk encryption via sudo, then rebuilds initramfs.
[Install/rollback](docs/boot-theme.md). Key artwork for COSMIC login is staged only;
login wallpaper support remains unresolved.

[Cat assets](docs/assets/boot-cat/): `cat.txt`, `render.py`, and four emoji variants
(coffee/key/laptop/lock), each white on black, transparent white (640 × 448), and
left-offset on black (1920 × 1200), plus 320 × 224 Plymouth exports for coffee/lock. Based on [my website](https://clifford.ressel.fyi/)
(CC BY-SA 4.0); fixed character spacing with FiraCode Nerd Font and Unicode fallback.

To regenerate with the fonts module and `python3-gi-cairo`, `python3-cairo`, and
`gir1.2-pango-1.0` installed:

```sh
python3 docs/assets/boot-cat/render.py
```

TODO: Development environment management and optional apps.

[Chezmoi installation](https://www.chezmoi.io/install/) · [Configuration internals](docs/codex.md)

### Philosophy

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
