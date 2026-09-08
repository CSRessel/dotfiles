#!/bin/sh
# Pop!OS 24.04: keep the packaged theme untouched; select our own alternative.
set -eu
action=${1:-install}
case "$action" in install|rollback) ;; *) echo 'Usage: install.sh [install|rollback]' >&2; exit 2 ;; esac
skip() { printf 'boot-theme: %s; skipping.\n' "$*"; exit 0; }
[ -r /etc/os-release ] || skip 'OS identity unavailable'
. /etc/os-release
[ "$ID:${VERSION_ID:-}" = pop:24.04 ] || skip 'requires Pop!OS 24.04'
for tool in plymouth update-alternatives update-initramfs sha256sum install cmp; do
    command -v "$tool" >/dev/null 2>&1 || skip "$tool unavailable"
done
if [ "$(id -u)" -ne 0 ]; then
    command -v sudo >/dev/null 2>&1 || skip 'sudo unavailable'
fi
as_root() { if [ "$(id -u)" -eq 0 ]; then "$@"; else sudo "$@"; fi; }
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
target=/usr/share/plymouth/themes/clifford-cat
theme=$target/clifford-cat.plymouth
state=/var/lib/dotfiles-boot-theme
base=/usr/share/plymouth/themes/pop-basic
current=$(readlink -f /etc/alternatives/default.plymouth)

if [ "$action" = rollback ]; then
    [ -f "$state/previous-theme" ] || { echo 'boot-theme: no saved previous theme' >&2; exit 1; }
    previous=$(cat "$state/previous-theme")
    [ -f "$previous" ] || { echo 'boot-theme: previous theme is missing' >&2; exit 1; }
    as_root update-alternatives --set default.plymouth "$previous"
    as_root update-alternatives --remove default.plymouth "$theme"
    as_root update-initramfs -u -k all
    as_root rm -f "$state/applied.sha256"
    echo 'boot-theme: previous theme restored; disable the module before the next apply.'
    exit 0
fi

[ -f "$(plymouth --get-splash-plugin-path)/two-step.so" ] || skip 'two-step plugin unavailable'
# Use the installed Pop entry UI rather than maintaining our own password code.
native_assets='entry.png bullet.png capslock.png cursor.png endcap.png return.png progress_bar.png'
for file in $native_assets; do
    [ -f "$base/$file" ] || skip "Pop asset $file unavailable"
done
for file in clifford-cat.plymouth header-image.png lock.png; do
    [ -f "$source_dir/plymouth/$file" ] || { echo "boot-theme: missing staged $file" >&2; exit 1; }
done
[ -f "$current" ] || { echo 'boot-theme: cannot identify current theme' >&2; exit 1; }

fingerprint=$( {
    sha256sum "$source_dir/install.sh" "$source_dir/plymouth/"*
    for file in $native_assets; do sha256sum "$base/$file"; done
} | sha256sum | cut -d ' ' -f 1)
unchanged=true
for file in clifford-cat.plymouth header-image.png lock.png; do
    cmp -s "$source_dir/plymouth/$file" "$target/$file" || unchanged=false
done
for file in $native_assets; do cmp -s "$base/$file" "$target/$file" || unchanged=false; done
if [ "$unchanged" = true ] && [ "$current" = "$theme" ] &&
   [ -f "$state/applied.sha256" ] && [ "$(cat "$state/applied.sha256")" = "$fingerprint" ]; then
    echo 'boot-theme: already installed.'
    exit 0
fi

as_root install -d -m755 "$state" "$target"
if [ ! -f "$state/previous-theme" ]; then
    [ "$current" != "$theme" ] || { echo 'boot-theme: original theme unknown; cannot save rollback' >&2; exit 1; }
    printf '%s\n' "$current" | as_root tee "$state/previous-theme" >/dev/null
fi
# Invalidate before any mutation so interrupted installs retry on the next apply.
as_root rm -f "$state/applied.sha256"
for file in clifford-cat.plymouth header-image.png lock.png; do
    as_root install -m644 "$source_dir/plymouth/$file" "$target/$file"
done
for file in $native_assets; do as_root install -m644 "$base/$file" "$target/$file"; done
as_root update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth "$theme" 100
as_root update-alternatives --set default.plymouth "$theme"
# Pop's post-update hooks also refresh the EFI copy through kernelstub.
as_root update-initramfs -u -k all
printf '%s\n' "$fingerprint" | as_root tee "$state/applied.sha256" >/dev/null
echo 'boot-theme: installed and initramfs rebuilt; verify on the next reboot.'
