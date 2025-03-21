#!/bin/bash
set -euxo pipefail
if type "cargo"; then
  echo "cargo already installed! installing tools..."
  cargo install tealdeer
  tldr --update
  cargo install bat
  cargo install ripgrep
  cargo install du-dust
  cargo install fd-find
else
  echo "rustup.rs to install cargo"
fi
