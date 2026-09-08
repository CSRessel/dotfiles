# Codex configuration

Codex CLI and Desktop both write runtime and user-specific state to
`~/.codex/config.toml`. Chezmoi therefore manages this file with a
[modify source](../dot_codex/modify_private_config.toml) instead of replacing the
whole file. The native chezmoi template parses the existing destination from
standard input with `fromToml`, updates or removes the stable paths owned by
these dotfiles with `setValueAtPath` and `deleteValueAtPath`, then serializes the
complete configuration with `toToml`. The round trip preserves configuration
values, not the original TOML formatting or comments.

These shared top-level values are always enforced:

| Setting | Value |
| --- | --- |
| `personality` | `pragmatic` |
| `model` | `gpt-5.6-sol` |
| `model_reasoning_effort` | `medium` |
| `approvals_reviewer` | `auto_review` |
| `approval_policy` | `on-request` |
| `service_tier` | `default` |

Managed paths are always enforced rather than seeded. They include selected
feature flags, plugin enablement flags, TUI settings, and platform-specific
desktop preferences. Everything outside those explicit paths remains local,
including trusted projects, unrelated permission profiles, unknown future
keys, marketplace metadata, and node or browser runtime state. The modifier
does not seed that runtime state merely because it preserves it. The preserved
`projects` subtree is deliberately serialized as the final section so
app-written trust entries stay visually separate from chezmoi-owned settings.

Platform policy comes from the operating system and `HOME`. Linux removes the
global `sandbox_mode` and enforces the `sccache-workspace` permission profile,
which extends workspace access with writes to `~/.cache/sccache` and network
access. macOS removes that Linux-only default and profile, enforces
`sandbox_mode = "workspace-write"`, and manages the Computer Use notification,
plugin/MCP settings, and related desktop preferences. Other permission profiles
survive on both platforms.

The modifier is implemented entirely with chezmoi template functions. If the
input is invalid TOML, `fromToml` stops the apply before serialization, chezmoi
returns a non-zero status, and the destination is left unchanged.
`CHEZMOI_CODEX_CONFIG_OS` is a platform override intended for tests and
previews, including the [merge tests](../tests/test_codex_config_merge.py).

The [Zsh configuration](../dot_zshrc.tmpl) sets `RUSTC_WRAPPER` when
`~/.cargo/bin/sccache` exists. On Linux, Codex sessions with `CODEX_THREAD_ID`
also set `SCCACHE_SERVER_UDS=/tmp/sccache-${CODEX_THREAD_ID}.sock`, isolating
sccache servers for concurrent Codex threads.

Preview the scoped merge before applying it:

```sh
chezmoi diff ~/.codex/config.toml
chezmoi apply ~/.codex/config.toml
```

Run all repository tests with:

```sh
python3 -m unittest discover -v tests
```

The [`tests/`](../tests) directory is source-only and excluded by
[`.chezmoiignore`](../.chezmoiignore), so chezmoi does not deploy it into the
destination home directory.

