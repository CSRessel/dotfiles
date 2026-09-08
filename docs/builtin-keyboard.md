# Built-in keyboard remapping

The Linux-only `builtin-keyboard` module stages a udev hwdb file under
`~/.config/builtin-keyboard/`. A chezmoi after-script installs and activates it
through sudo only when the hwdb tools, matching model, and internal AT keyboard
are present. It runs once per script/rule version. Missing prerequisites skip
with a message; a successful skip is also remembered by chezmoi.
It matches the internal AT keyboard on the Framework Laptop 13 Pro (Intel Core
Ultra Series 3), using its DMI model. USB and Bluetooth keyboards do not match.
Other laptop models need their own verified match and scan codes.

| Physical key | Scan code | Result |
| --- | --- | --- |
| Right Alt | `b8` | Escape |
| Caps Lock | `3a` | Left Control |
| Left Control | `1d` | Volume down |
| Escape | `01` | Caps Lock |
| Right Shift | `36` | Right Alt |

Left Alt, Super and Left Shift are unchanged. These kernel keycode mappings apply
at the login screen and text consoles as well as in COSMIC. Right Alt's meaning
follows the desktop layout: the current `lv3:ralt_switch` option makes the remapped
Right Shift act as AltGr. COSMIC handles the volume-down key using its existing shortcut.
No additional daemon, global XKB remap, or desktop layout change is needed.

## Install

Add `"builtin-keyboard"` to your existing `data.modules` list with
`chezmoi edit-config` (replace `"cosmic"` if previously selected). Then:

```sh
chezmoi diff
chezmoi apply
```

Enter your sudo password if prompted. The first apply rebuilds the hwdb and triggers
only the internal keyboard. Unchanged successful scripts disappear from subsequent
diffs; script/rule changes run again. Failed runs retry on the next apply.
The script checks that udev imported every mapping before reporting success.
The hwdb match uses udev's sanitized DMI model (parentheses become underscores),
while the installation guard checks the raw model in sysfs.

Verify all five mappings with `sudo evtest /dev/input/by-path/platform-i8042-serio-0-event-kbd`,
then test in COSMIC and on an external keyboard. Use physical Caps Lock+C to stop
evtest after remapping. The rule persists across reboots. If the session does not
recognize a newly available key, reboot and retest.

The abandoned global COSMIC/XKB files were never applied in this setup. If you
applied them independently, restore your previous COSMIC `xkb_config` before
installing this rule to avoid remapping twice.

To retry a skipped version or reapply after another tool changed the mapping:

```sh
chezmoi execute-template --file "$(chezmoi source-path)/run_once_after_builtin_keyboard.sh.tmpl" | sh
```

## Rollback

Remove `"builtin-keyboard"` from `data.modules` with `chezmoi edit-config` first,
so the next apply does not reinstall it. Then:

```sh
sudo rm -- /etc/udev/hwdb.d/90-builtin-keyboard.hwdb
sudo systemd-hwdb update
sudo reboot
```

A reboot restores the driver's original scan-code map; removing the hwdb entry
and triggering udev alone does not undo mappings already loaded into the kernel.
Remove `"builtin-keyboard"` from your modules if you also want to stop managing the
staged file. Disabling the module alone does not uninstall the system rule.

Reference: [systemd keyboard hwdb documentation](https://github.com/systemd/systemd/blob/main/hwdb.d/60-keyboard.hwdb).
