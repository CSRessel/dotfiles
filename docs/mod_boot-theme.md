# Boot theme

White cat artwork on black, using Pop!OS 24.04's native Plymouth `two-step` renderer.

| Screen | Artwork |
| --- | --- |
| Boot, shutdown, reboot | Coffee cat |
| Disk unlock | Lock cat beside the native password field |
| COSMIC login | Key wallpaper staged only; no login override installed |

The renderer retains native password handling, keyboard indicators and messages.
Encryption configuration is unchanged.

## Mechanism and ownership

- [Artwork](assets/boot-cat/): text source, Python renderer and PNG variants. Plymouth uses 320 × 224 transparent exports; target machines need no rendering tools.
- [Module files](../dot_config/boot-theme/): staged under `~/.config/boot-theme/`, including the login wallpaper.
- [Installer](../dot_config/boot-theme/executable_install.sh): copies the theme and installed Pop entry assets to `/usr/share/plymouth/themes/clifford-cat`, selects it through `update-alternatives`, and rebuilds initramfs through sudo. Pop's hooks refresh the EFI copy.
- `/var/lib/dotfiles-boot-theme/`: saved previous theme and successful-install fingerprint.

The after-script runs once per installer, theme or artwork version. Failed runs
retry; successful prerequisite skips are remembered. The installer itself avoids
rebuilding unchanged files. Disabling the module does not undo system changes.

Rollback: `~/.config/boot-theme/install.sh rollback` restores the saved theme and
rebuilds initramfs; disable the module to prevent reinstallation. Inert theme files
and rollback metadata remain on disk.

## Activate

Enable `boot-theme` in your chezmoi modules, then run `chezmoi apply`.
To install files staged without scripts, run `~/.config/boot-theme/install.sh install`
in a terminal; sudo authenticates the system install and initramfs rebuild.
The initial Framework firmware logo may still appear before Plymouth takes over.
