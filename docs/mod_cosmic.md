# COSMIC desktop

A compact dark desktop: panel without dock, vertical workspaces, and natural
touchpad scrolling. Native RON files under `~/.config/cosmic/`; applying the
module requires no sudo after installing ImageMagick.

| Component (`com.system76.*`) | Preferences |
| --- | --- |
| CosmicBackground | Hostname-colored phytoplankton wallpaper across displays |
| CosmicTheme.Mode | Dark mode |
| CosmicTheme.Dark/Light and Builder namespaces | Tight corners, spacing, 4-pixel active hint |
| CosmicTk | Compact interface/header; minimize and maximize controls |
| CosmicPanel, CosmicPanel.Panel/Dock | Panel enabled, dock disabled; panel and dock geometry |
| CosmicComp | Edge snapping and tiling preferences; global vertical workspaces with wraparound |
| CosmicComp input_default/input_touchpad | Reduced pointer speed; natural two-finger scrolling, tap-to-click and tap-drag |
| CosmicAppletTime | Saturday week start; 12-hour clock |
| CosmicIdle | No automatic suspend on AC; 30 minutes on battery |

## Ownership and boundaries

[Managed files](../dot_config/cosmic/) overlay existing preferences; untracked
settings retain their local values or COSMIC defaults. Theme-builder inputs and
generated theme values are both tracked, avoiding a required rebuild on apply.
GUI edits to managed files can be overwritten by the next apply.

Pointer settings are shared defaults, not device-specific. Natural scrolling is
set only for the touchpad; sensitivity comes from `input_default`.

Wallpaper-picker history is excluded. [Fonts](mod_fonts.md) owns font selection;
[builtin-keyboard](mod_builtin-keyboard.md) owns hardware key remapping.

[Desktop app defaults](packages.md#desktop-defaults) use XDG associations through
the independent `desktop-apps` module.

## Hostname-colored wallpaper

Install ImageMagick manually on Pop!OS with `sudo apt install imagemagick`.
The generator accepts ImageMagick 7's `magick` or ImageMagick 6's `convert`.
It runs only on Linux with the `cosmic` module enabled.

The [before script](../run_before_cosmic_wallpaper.sh.tmpl) renders the
[vendored original](assets/cosmic/README.md) before chezmoi updates the
[background setting](../dot_config/cosmic/com.system76.CosmicBackground/v1/all.tmpl):

```text
vendored JPEG + hostname → cached color variant → COSMIC background setting
```

The first six hexadecimal digits of the hostname's SHA-256, modulo 200,
select ImageMagick's hue percentage (100 leaves hue unchanged; 200 is a full
turn). Brightness and saturation are both 125%, with JPEG quality 95. The same
hostname selects the same hue; different hostnames can collide, so colors are
not guaranteed unique.

The [shared path template](../.chezmoitemplates/cosmic-wallpaper-path) hashes the
hostname, source image SHA-256, and recipe version `v1` into a filename under
`~/.config/cosmic/wallpapers/`. Generated JPEGs are local cache files, not managed
source files. Existing nonempty output skips rendering; deleting it regenerates
it on the next apply. A hostname or source-image change selects a new output;
bump the recipe version when changing rendering parameters. Older outputs remain.

Rendering writes to a temporary file and atomically renames it on success.
Missing renderer or rendering errors stop a full apply before the background
setting is updated. A cached image needs no renderer until regeneration is required.

Ordinary `chezmoi diff` previews the changes; a full `chezmoi apply` is recommended
because it runs the generator before updating settings. To review and apply only
the wallpaper, run the generator separately and update the setting only on success:

```sh
chezmoi diff --parent-dirs "$HOME/cosmic_wallpaper.sh" "$HOME/.config/cosmic/com.system76.CosmicBackground/v1/all"
chezmoi apply "$HOME/cosmic_wallpaper.sh" && chezmoi apply --parent-dirs "$HOME/.config/cosmic/com.system76.CosmicBackground/v1/all"
```

The script target is chezmoi's name for the apply hook; it is not installed as a
shell script in the home directory. Applying the setting alone skips generation.
Chezmoi 2.60.1 does not preserve before-script ordering when both targets are
passed to one apply command, so use the sequential command above.
