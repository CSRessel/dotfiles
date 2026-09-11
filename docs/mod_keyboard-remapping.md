# Keyboard remapping

Enable `keyboard-remapping` in `data.modules` to manage physical-key mappings.
Desktop and app hotkeys belong to their OS or application settings:
[de-cosmic](mod_de-cosmic.md) keeps COSMIC shortcuts, and
[de-macos](mod_de-macos.md) keeps macOS menu and text-navigation shortcuts.

## Linux

Native Linux remapping for the Framework Laptop 13 Pro (Intel Core Ultra Series 3)
internal AT keyboard. USB and Bluetooth keyboards retain their firmware mappings.
No remapping daemon or global desktop key swap.

| Physical key | Result |
| --- | --- |
| Right Alt | Escape |
| Caps Lock | Left Control |
| Left Control | Volume down |
| Escape | Caps Lock |
| Right Shift | Right Alt |

Left Alt, Super and Left Shift stay unchanged. Kernel mappings apply in text
consoles, login and desktop sessions. The desktop layout determines Right Alt's
meaning; with `lv3:ralt_switch`, remapped Right Shift acts as AltGr.

## Mechanism and ownership

- [Rule](../dot_config/keyboard-remapping/linux/90-builtin-keyboard.hwdb): scan-code mappings and hardware match; staged under `~/.config/keyboard-remapping/linux/`.
- [Installer](../run_once_after_keyboard_remapping_linux.sh.tmpl): verifies model, keyboard connection, driver and tools; installs `/etc/udev/hwdb.d/90-builtin-keyboard.hwdb` through sudo, rebuilds hwdb and activates only that keyboard.
- Runs once per script/rule version. Failures retry; successful skips are remembered. Activation verifies that udev imported every mapping.

The rule matches udev's sanitized model name; the installer checks the raw sysfs
identity. Other laptops require their own verified match and scan codes.

Removal requires disabling the module, deleting its system rule, rebuilding hwdb
and rebooting to restore the driver's original mappings.

## macOS: TODO

Choose and verify an implementation that remaps only the built-in keyboard,
preserving external keyboards' firmware mappings. Decide the physical modifier
layout on Mac hardware before implementing it. Selecting `keyboard-remapping`
on macOS currently deploys no files and runs no remapping commands.

## Migration

Replace `builtin-keyboard` in `data.modules` with `keyboard-remapping`. Apply moves
the staged Linux rule to `~/.config/keyboard-remapping/linux/`; the installed
`/etc/udev/hwdb.d/90-builtin-keyboard.hwdb` path and mappings stay the same.
Replace the old `mac-shortcuts` entry with `de-macos` to opt into macOS shortcut
settings. That module is independent of physical-key remapping.
