# Fonts

Enable `fonts` with `chezmoi edit-config`, then `chezmoi diff` and `chezmoi apply`.
Keep `cosmic` enabled too for the COSMIC-specific font settings.

On Pop!OS/Ubuntu the before-script installs IBM Plex and Noto core/CJK/emoji
packages via apt (sudo only when packages are missing). It downloads Nerd Fonts
3.5.1 FiraCode into your user font directory with a pinned SHA-256 checksum.
Font preferences are written after installation succeeds. Repeated applies reuse
the installed fonts. This module currently targets Linux with apt; macOS support
is deferred.

- COSMIC interface: IBM Plex Sans, normal weight.
- Generic sans-serif: IBM Plex Sans, then Noto Sans.
- COSMIC/generic monospace: FiraCode Nerd Font Mono.

Noto's script-specific families and emoji fonts remain available to the font
renderer for missing characters. COSMIC's RON setting accepts a single primary
family; Fontconfig fallback ordering applies to apps that use Fontconfig, and
other renderers may choose their own fallback fonts.

Restart existing apps or log out/in if they retain the old font list. Check:

```sh
fc-match sans-serif
fc-match monospace
fc-match -s 'IBM Plex Sans' | head
```

Editors/terminals with an explicit font setting override the generic default;
choose `FiraCode Nerd Font Mono` there when configuring their optional modules.
Disabling `fonts` stops management but does not uninstall fonts or remove applied
preferences.
