# Built-in keyboard

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

- [Rule](../dot_config/builtin-keyboard/90-builtin-keyboard.hwdb): scan-code mappings and hardware match; staged under `~/.config/builtin-keyboard/`.
- [Installer](../run_once_after_builtin_keyboard.sh.tmpl): verifies model, keyboard connection, driver and tools; installs `/etc/udev/hwdb.d/90-builtin-keyboard.hwdb` through sudo, rebuilds hwdb and activates only that keyboard.
- Runs once per script/rule version. Failures retry; successful skips are remembered. Activation verifies that udev imported every mapping.

The rule matches udev's sanitized model name; the installer checks the raw sysfs
identity. Other laptops require their own verified match and scan codes.

Removal requires disabling the module, deleting its system rule, rebuilding hwdb
and rebooting to restore the driver's original mappings.
