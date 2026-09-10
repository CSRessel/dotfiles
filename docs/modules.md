# Modules

The shared base is Zsh, Bash, Git, tmux, and useful aliases on Linux and macOS.
Original command names stay intact except `rm`, which uses recoverable trash.
Toolchains and desktop preferences, including Ghostty, are opt-in.

Tmux loads Catppuccin when installed. The contribution graph builds when Cargo
is available and displays in interactive Zsh login shells when its binary exists.

## Catalog

| Module | Opinion / purpose | Platform |
| --- | --- | --- |
| [builtin-keyboard](mod_builtin-keyboard.md) | Native remapping of the matching Framework internal keyboard; external keyboards untouched | Linux |
| [fonts](mod_fonts.md) | IBM Plex Sans, Noto fallback, FiraCode Nerd Font Mono | Linux with apt |
| [desktop-apps](packages.md#desktop-defaults) | Firefox, VLC and Zed defaults when installed | Linux |
| [cosmic](mod_cosmic.md) | Native RON settings: compact dark desktop, panel, vertical workspaces | Linux / COSMIC |
| [boot-theme](mod_boot-theme.md) | Coffee splash, lock-cat disk prompt; key login artwork staged only | Pop!OS 24.04 |
| `alacritty`, `kitty`, `ghostty` | Terminal preferences | Linux / macOS |
| `warp` | Terminal preferences | macOS |
| `lunarvim`, `vscode` | Editor preferences | App-dependent |
| [codex](mod_codex.md) | Shared settings merged with machine-local state | Linux / macOS |
| `claude`, `gemini`, `opencode` | Optional AI-tool configs | App-dependent |
| `k9s`, `marimo`, `tridactyl`, `nethack` | Application preferences | App-dependent |
| [dev-tools](dev-tools.md) | Pinned mise tools, automatic installation and shell integration | Linux / macOS |
| [nix](dev-tools.md#nix-and-project-flakes) | User Nix config with flakes enabled; install Nix separately | Linux / macOS |
| `poetry` | Legacy Poetry preferences; no toolchain installation | Tool-dependent |
| `tmux-memory` | Per-machine memory limits for matching tmux scopes | Linux / systemd |
| `user-oom-policy` | User services continue after an OOM kill | Linux / systemd |
| `mac-shortcuts` | Keyboard shortcut automation | macOS |
| `local-scripts` | Personal command scripts | Script-dependent |

Platform labels describe intended scope, not cross-platform validation.

## Composition and ownership

`data.modules` in `~/.config/chezmoi/chezmoi.toml` selects modules; none are enabled
by default. [The catalog](../.chezmoidata.json) maps names to managed paths;
[ignore rules](../.chezmoiignore) enforce selection and platform boundaries.

Chezmoi uses an explicit `0022` umask: ordinary files are `0644`, executable files
and directories `0755`; `private_` attributes remove group/other access.

- `fonts` needs `cosmic` for COSMIC font preferences; Fontconfig settings stand alone.
- `cosmic` requires ImageMagick for hostname-colored wallpaper generation; install it manually before applying.
- `tmux-memory` requires `data.tmuxMemory.high`, `.max`, and `.swap`; it limits existing scopes, not their creation.
- Most modules configure existing tools. `fonts` installs dependencies; `builtin-keyboard` and `boot-theme` install system configuration through sudo.
- Disabling a module stops management. It does not remove applied files, packages, or system changes.

Selection: `chezmoi edit-config`. Review: `chezmoi diff`. Apply: `chezmoi apply`.
