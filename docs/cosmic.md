# COSMIC desktop

A compact dark desktop: panel without dock, vertical workspaces, and natural
touchpad scrolling. Native RON files under `~/.config/cosmic/`; no sudo.

| Component (`com.system76.*`) | Preferences |
| --- | --- |
| CosmicBackground | Bundled phytoplankton wallpaper across displays |
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

The wallpaper references Pop!OS's bundled
`/usr/share/backgrounds/cosmic/phytoplankton_bloom_nasa_oli2_20240121.jpg`.
Wallpaper-picker history is excluded. [Fonts](fonts.md) owns font selection;
[builtin-keyboard](builtin-keyboard.md) owns hardware key remapping.
