# Boot theme

Enable `boot-theme` with `chezmoi edit-config`, review `chezmoi diff`, then apply
when ready. This module is limited to Pop!OS 24.04; nothing installs on macOS.

```sh
chezmoi diff
chezmoi apply
```

Apply stages `~/.config/boot-theme`, then runs its `install.sh` with ordinary sudo
prompts for system changes. It saves the previous theme, installs a separate
`/usr/share/plymouth/themes/clifford-cat` theme, selects it through
`update-alternatives`, and rebuilds all installed initramfs images. Pop's existing
post-update hooks refresh the EFI copy. Verify at the next reboot; no live desktop
or greeter restart is performed.

- Coffee cat: boot splash (also shutdown/reboot).
- Lock cat: beside the native disk-password field. The native `two-step` renderer
  retains entry, caps-lock/keymap indicators, messages and authentication behavior.
- Key cat: staged as `~/.config/boot-theme/login-background.png` only. COSMIC's
  wallpaper-loading issue remains unresolved, so no login override is installed.

Artwork uses the renderer's 320 × 224 transparent Plymouth exports. The module
includes PNGs directly from the repository assets; rendering tools are not needed
on the target machine. Existing Pop password-entry assets are copied at install.
Missing OS/tool/theme prerequisites skip installation with a message. Unchanged
installs do not prompt or rebuild; changes and interrupted installs retry on apply.
The module does not install packages or alter disk encryption itself.

## Rollback

```sh
~/.config/boot-theme/install.sh rollback
chezmoi edit-config  # remove boot-theme from modules
```

Rollback selects the saved previous theme and rebuilds initramfs. It leaves inert
theme files and rollback metadata on disk. Removing the module alone does not undo
system changes. If the graphical theme fails, use Plymouth's Escape text view.

Implementation reference: Pop's [two-step renderer](https://github.com/pop-os/plymouth/blob/master/src/plugins/splash/two-step/plugin.c)
shows the header outside dialogs and the lock image inside them. The native layout
places the lock image beside the entry, rather than above it.
