# COSMIC desktop

The Linux-only `cosmic` module records the Desktop GUI changes from September 8,
2026 as native files under `~/.config/cosmic/`. Enable it in `data.modules`, then
review with `chezmoi diff` and apply with `chezmoi apply`. No sudo is needed for
these settings; other enabled modules may use sudo.

| Component namespace (com.system76.*) | Recorded preferences |
| --- | --- |
| CosmicBackground | Bundled phytoplankton wallpaper, shared across displays |
| CosmicTheme.Mode | Dark mode |
| CosmicTheme.Dark/Light and their Builder namespaces | Changed theme values, tighter corners, spacing, 4-pixel active hint |
| CosmicTk | Compact interface/header; minimize and maximize controls |
| CosmicPanel, CosmicPanel.Panel/Dock | Panel enabled, dock disabled; edited panel and saved dock geometry |
| CosmicComp | Edge snapping threshold, autotile behavior, global vertical workspaces with wraparound |
| CosmicComp input_default/input_touchpad | Default pointer speed −0.10288643756187243; touchpad natural two-finger scrolling, tap-to-click and tap-drag |
| CosmicAppletTime | Week starts Saturday; 12-hour clock |
| CosmicIdle | No automatic suspend on AC; 30 minutes on battery |

Both changed theme-builder inputs and the changed generated theme values are
recorded, preserving what the GUI wrote without assuming a theme rebuild on apply.
Unchanged settings continue to use the machine's existing values or COSMIC defaults.
This is a preference overlay, not a complete frozen desktop image.

Pointer preferences are shared defaults, not tied to a device ID. COSMIC saved
the sensitivity under `input_default`; no separate touchpad speed override is
present. Natural scrolling is explicitly enabled for the touchpad only.

The wallpaper requires Pop!OS's bundled file:
`/usr/share/backgrounds/cosmic/phytoplankton_bloom_nasa_oli2_20240121.jpg`.
Other distributions must supply that image or choose a different background.
Wallpaper-picker UI history is excluded. Keyboard remapping remains in
`builtin-keyboard`; font selection and installation belong to a later module.

For the next capture, snapshot `~/.config/cosmic/`, change a batch in the GUI, and
compare files. Add the intended changed files with `chezmoi add <path>`, review the
Git diff, and update this summary. Capture GUI edits before applying chezmoi again,
or the managed files may overwrite those edits.
