# Modules

The shared base is Zsh, Bash, Git, tmux, and useful aliases on Linux and macOS.
Original command names stay intact except `rm`, which uses recoverable trash.
The base also installs `add_iso_prefixes.sh` and `open_github.sh` in `~/.local/bin`.
Standalone app configs are also always managed: Ghostty (`~/.config/ghostty`),
Kitty (`~/.config/kitty`), LunarVim (`~/.config/lvim`), VS Code (`~/.config/Code`),
marimo (`~/.config/marimo`), Tridactyl (`~/.config/tridactyl`), NetHack (`~/.nethackrc`)
and Nix (`~/.config/nix`). Applying them does not install the applications.
System settings, toolchain installation, dictation and AI-tool integrations remain opt-in.

Warp, Alacritty, k9s and Poetry configs have been retired. Apply removes only their
previously managed config files, preserving other application files and installed
packages. The old configs remain available in Git history.

Tmux loads Catppuccin when installed. The contribution graph builds when Cargo
is available and displays in interactive Zsh login shells when its binary exists.

## Catalog

| Module | Opinion / purpose | Platform |
| --- | --- | --- |
| [builtin-keyboard](mod_builtin-keyboard.md) | Native remapping of the matching Framework internal keyboard; external keyboards untouched | Linux |
| [fonts](mod_fonts.md) | IBM Plex Sans, Noto fallback, FiraCode Nerd Font Mono | Linux with apt |
| [desktop-apps](packages.md#desktop-defaults) | Firefox, VLC, Zed and Ghostty defaults when installed | Linux |
| [cosmic](mod_cosmic.md) | Native RON settings: compact dark desktop, panel, vertical workspaces | Linux / COSMIC |
| [boot-theme](mod_boot-theme.md) | Coffee splash, lock-cat disk prompt; key login artwork staged only | Pop!OS 24.04 |
| [codex](mod_codex.md) | Shared settings merged with machine-local state | Linux / macOS |
| `claude`, `gemini`, `opencode` | Optional AI-tool configs | App-dependent |
| [dev-tools](dev-tools.md) | Pinned mise tools, automatic installation and shell integration | Linux / macOS |
| `memory-protection` | Per-machine tmux scope memory limits and user-manager OOM policy | Linux / systemd |
| `mac-shortcuts` | Keyboard shortcut automation | macOS |
| [dictation](mod_dictation.md) | On-device streaming speech to clipboard; optional desktop shortcut | Linux / systemd |

Platform labels describe intended scope, not cross-platform validation.

## Composition and ownership

`data.modules` in `~/.config/chezmoi/chezmoi.toml` selects modules; none are enabled
by default. [The catalog](../.chezmoidata.json) maps names to managed paths;
[ignore rules](../.chezmoiignore) enforce selection and platform boundaries.
Remove old standalone-app and retired-app names from `data.modules` when updating;
those entries no longer control any paths.

Chezmoi uses an explicit `0022` umask: ordinary files are `0644`, executable files
and directories `0755`; `private_` attributes remove group/other access.

- `fonts` needs `cosmic` for COSMIC font preferences; Fontconfig settings stand alone.
- `cosmic` requires ImageMagick for hostname-colored wallpaper generation; install it manually before applying.
- `memory-protection` requires `data.tmuxMemory.high`, `.max`, and `.swap`; it limits matching tmux scopes, not their creation, and sets `DefaultOOMPolicy=continue` for the user manager.
- Most modules configure existing tools. `fonts` installs dependencies; `builtin-keyboard` and `boot-theme` install system configuration through sudo.
- Disabling a module stops management. It does not remove applied files, packages, or system changes.

Selection: `chezmoi edit-config`. Review: `chezmoi diff`. Apply: `chezmoi apply`.

`memory-protection` replaces `tmux-memory` and `user-oom-policy`. Replace either
old name in `data.modules` with `memory-protection`; both policies are now managed
together. Existing `[data.tmuxMemory]` values and deployed file paths stay the same.
If only `user-oom-policy` was selected, also set the three per-machine memory limits
before applying. Machines with neither selected remain opt-out.

When enabling it through `chezmoi edit-config`, add the limits too; editing the
module list does not run the `chezmoi init` prompts. For example:

```toml
[data.tmuxMemory]
high = "24G"
max = "32G"
swap = "8G"
```

These are the setup's suggested values; choose limits appropriate to the machine.
Missing limits cause `chezmoi status`, `diff` and `apply` to fail until configured.
