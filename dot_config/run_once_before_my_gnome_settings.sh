#!/usr/bin/env bash
set -euo pipefail

dconf load /org/gnome/ < ~/.config/my-gnome-settings.conf
dconf load /org/gnome/ < ~/.config/my-gnome-keybindings.conf
