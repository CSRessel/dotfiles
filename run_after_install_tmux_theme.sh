#!/bin/sh
set -eu

theme_dir="$HOME/.config/tmux/plugins/catppuccin/tmux"
if [ ! -e "$theme_dir" ]; then
    mkdir -p "$(dirname "$theme_dir")"
    git clone --depth 1 --branch v2.3.0 \
        https://github.com/catppuccin/tmux.git "$theme_dir"
fi
