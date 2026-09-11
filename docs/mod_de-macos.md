# macOS desktop settings

Enable `de-macos` in `data.modules` on macOS. The chezmoi platform identifier is
`darwin`; the module uses the familiar desktop name, macOS.
The [module catalog](../.chezmoidata.json) and [ignore rules](../.chezmoiignore)
gate its shortcut setup and AeroSpace config on both module selection and platform.

[The setup script](../run_once_mac_keyboard_shortcuts.sh.tmpl) manages the existing
macOS shortcut preferences:

- Control-based menu shortcuts for tabs, windows and page reload.
- Control+Shift copy, cut and paste in iTerm2.
- Control-based word navigation, selection and deletion in Cocoa text fields,
  using `~/Library/KeyBindings/DefaultKeyBinding.dict`.

This is app and desktop shortcut configuration. Physical modifier positions belong
to [keyboard-remapping](mod_keyboard-remapping.md), whose macOS implementation is TODO.

The script runs once per rendered version when selected on macOS. It adds missing
menu entries and preserves existing ones. For an existing text-binding file, its
legacy merge checks for `moveWordLeft` before adding the word-navigation block.
Disabling the module stops future setup; it does not undo applied preferences.

The tracked [AeroSpace config](../dot_aerospace.toml) deploys to `~/.aerospace.toml`.
It carries the existing laptop settings: tiled workspaces, Alt-based focus and
window controls, and service-mode layout controls. AeroSpace is installed and
started separately; `start-at-login` remains disabled. Unlike the shortcut script,
this file is fully managed rather than merged. Disabling the module leaves the
deployed file in place.

Zed settings and Nori Green belong to the [shared base](modules.md), so they are
managed independently of `de-macos` on Linux and macOS.

`de-macos` replaces the old `mac-shortcuts` entry. Previously the script ran on
macOS regardless of module selection; it now requires this module. The shortcut
values and setup implementation are unchanged.
