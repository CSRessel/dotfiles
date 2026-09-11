# Fonts

IBM Plex Sans for interface text, Noto for broad character coverage, and FiraCode
Nerd Font Mono for code and terminal symbols.

| Default | Primary | Fallback |
| --- | --- | --- |
| Interface / sans-serif | IBM Plex Sans | Noto Sans |
| Monospace | FiraCode Nerd Font Mono | Noto Sans Mono |

Explicit app font settings take precedence. Fontconfig controls fallback in apps
that use it; COSMIC selects a primary family and leaves fallback to its renderer.
Noto CJK and emoji fonts provide additional coverage.

## Mechanism and ownership

- [Installer](../run_once_before_install_fonts.sh.tmpl): Linux with apt; installs missing system font packages through sudo and checksum-pinned FiraCode into `~/.local/share/fonts/`. Runs once per script version; failures retry. Versions and checksums live in the script.
- [Fontconfig](../dot_config/fontconfig/conf.d/60-dotfiles-fonts.conf): generic defaults under `~/.config/fontconfig/conf.d/`.
- COSMIC [interface](../dot_config/cosmic/com.system76.CosmicTk/v1/interface_font) and [monospace](../dot_config/cosmic/com.system76.CosmicTk/v1/monospace_font) preferences: native RON under `~/.config/cosmic/`; require both `fonts` and `de-cosmic` modules.

Fontconfig settings work independently of COSMIC. Disabling the module leaves
installed fonts and applied preferences in place.
