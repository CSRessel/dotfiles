# Codex

Codex preferences are always managed as part of the shared base; no module
selection is needed. Machine and runtime state remain local.
The [modifier](../dot_codex/modify_private_config.toml) merges owned settings into
`~/.codex/config.toml` rather than replacing the file.

| Shared ownership | Preserved local values |
| --- | --- |
| Model, personality and reasoning preferences | Project trust entries |
| Approval policy and selected permission settings | Unrelated permission profiles |
| Selected features, plugins, TUI and desktop preferences | Marketplace metadata and runtime state |
| Explicit platform-specific paths | All other configuration paths |

Exact settings live in the modifier. Preserving a value does not create it on a
fresh machine.

Shared defaults select `gpt-6-astra`, `pragmatic` personality and the `never`
approval policy. The remote GitHub plugin is explicitly disabled.

## Platform policy

- Linux: workspace permissions extended with network access and writes to `~/.cache/sccache`.
- macOS: `workspace-write` sandbox mode; platform-specific desktop and Computer Use preferences. The Linux default permission profile is removed.

The [Zsh config](../dot_zshrc.tmpl) uses sccache when installed and gives Linux
Codex threads separate server sockets.

Invalid TOML stops the merge without changing the destination. Serialization
preserves values, not comments or formatting; project entries appear last.
