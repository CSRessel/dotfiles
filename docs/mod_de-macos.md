# macOS desktop settings

Enable `de-macos` in `data.modules` on macOS. The chezmoi platform identifier is
`darwin`; the module uses the familiar desktop name, macOS.

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

`de-macos` replaces the old `mac-shortcuts` entry. Previously the script ran on
macOS regardless of module selection; it now requires this module. The shortcut
values and setup implementation are otherwise unchanged and have not been tested
on macOS during this Linux-side cleanup.
