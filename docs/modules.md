# Per-machine modules

The base manages shell, Git, and tmux files on Linux and macOS. All app configs are
opt-in via `data.modules` in `~/.config/chezmoi/chezmoi.toml`. Initialization prompts
once; use `chezmoi edit-config` to change the selection, then `chezmoi diff`.
Turning a module off stops managing its files; it does not delete files already applied.
Modules configure existing tools; they do not install them.

```toml
[data]
email = "you@example.com"
modules = ["ghostty", "tmux-memory"]

[data.tmuxMemory]
high = "24G"
max = "32G"
swap = "8G"
```

Choose limits appropriate to the machine; the example is not a default allocation.
`tmux-memory` is Linux-only and requires all three limits. It affects only existing
`tmux-spawn-*.scope` units; it does not create scopes. The separate `user-oom-policy`
module sets `DefaultOOMPolicy=continue` across user services. Neither is enabled by default.
After applying changed systemd files, run `systemctl --user daemon-reload` and start
new scopes to use the settings. Verify the actual scope limits before relying on them.

Available modules are listed in [the catalog](../.chezmoidata.json):

- Terminals: `alacritty`, `ghostty`, `kitty`, `warp` (macOS).
- Editors: `lunarvim`, `vscode`.
- AI tools: `claude`, `codex`, `gemini`, `opencode`.
- Other apps: `k9s`, `marimo`, `tridactyl`, `nethack`.
- Deferred toolchains: `nix`, `poetry`.
- Keyboard: `builtin-keyboard` (Linux; [hardware-specific remapping](builtin-keyboard.md), installs via sudo on matching hardware).
- System/personal extras: `tmux-memory`, `user-oom-policy`, `mac-shortcuts`, `local-scripts`.

Legacy app configs, especially Claude/Gemini's Nori hooks and macOS keyboard automation,
still need their own review. Leave them unselected until their chapter.

## Shell shortcuts

Original command names remain intact, except the deliberately retained `rm` → `safe_rm`.
Shortcuts appear only when their dependencies exist at shell startup.

| Shortcut | Command |
| --- | --- |
| `lv` | `lvim` |
| `bcat` | `bat` or `batcat` |
| `fdf` | `fdfind` |
| `kc`, `kx` | `kubectl`, `kubectx` |
| `mkc` | `minikube kubectl --` |
| `pd`, `pdc` | `podman`, `podman-compose` |
| `tx` | `tmux -L clifford-human-only` |
| `cpi`, `dfh`, `k9` | `cp -i`, `df -h`, `k9s --logoless` |
| `nclaude`, `ncodex`, `nnori`, `npi` | Existing Nori wrappers |

`safe_rm` uses `gio trash` or `trash-put` on Linux and `/usr/bin/trash` (or an installed
`trash` command) on macOS. Missing backends fail without deleting. It accepts `-r`, `-R`,
`-f` and `--`; other flags fail explicitly. Use `rm --really-delete ...` or
`command rm ...` for permanent deletion. No hand-built trash metadata is used.

The base does not initialize language runtimes or toolchain managers. Those belong in a
later development-environment layer. Oh My Zsh is used when already installed, with its
aliases disabled; Bash remains the fallback and reads the same shared aliases.
