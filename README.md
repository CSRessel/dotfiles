# dotfiles

[twpayne/chezmoi](https://github.com/twpayne/chezmoi)

[Quick Start](https://www.chezmoi.io/quick-start/)

## Getting Started

> **Note**: This relies on my personal computer having the username `clifford`, and my work machine having the username of `resselc`.

```
touch ~/.config/chezmoi/chezmoi.toml
echo "[data]"                             >> ~/.config/chezmoi/chezmoi.toml
echo "  email = \"CSRessel@gmail.com\"" >> ~/.config/chezmoi/chezmoi.toml

chezmoi cd
git remote add origin https://github.com/CSRessel/dotfiles.git
git pull origin master
exit

chezmoi status
chezmoi diff
```

