#!/bin/bash

BACKUP_DIR="$HOME/.installed_packages"
LOG_FILE="$BACKUP_DIR/cron.log"

if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "$(date): Created backup directory $BACKUP_DIR" >> "$LOG_FILE"
fi

APT_PKG_NAMES_USER="$BACKUP_DIR/apt_packages_names_user.txt"
APT_PKG_NAMES_ALL="$BACKUP_DIR/apt_packages_names_all.txt"
APT_PKG_INFO="$BACKUP_DIR/apt_packages_info.txt"
FLATPAK_PKG_NAMES="$BACKUP_DIR/flatpak_packages_names.txt"
SNAP_PKG_NAMES="$BACKUP_DIR/snap_packages_names.txt"

if command -v dpkg &> /dev/null; then
    dpkg --get-selections | awk '{print $1}' > "$APT_PKG_NAMES_ALL"
    dpkg -l > "$APT_PKG_INFO"
else
    echo "dpkg command not found, skipping Ubuntu package list." >> "$LOG_FILE"
fi

if command -v apt-mark &> /dev/null; then
    apt-mark showmanual > "$APT_PKG_NAMES_USER"
else
    echo "apt-mark command not found, skipping Ubuntu user package list." >> "$LOG_FILE"
fi

if command -v snap &> /dev/null; then
    snap list | awk 'NR>1 {print $1}' > "$SNAP_PKG_NAMES"
else
    echo "snap command not found, skipping snap package list." >> "$LOG_FILE"
fi

if command -v flatpak &> /dev/null; then
    flatpak list --columns=name > "$FLATPAK_PKG_NAMES"
else
    echo "flatpak command not found, skipping flatpak package list." >> "$LOG_FILE"
fi
