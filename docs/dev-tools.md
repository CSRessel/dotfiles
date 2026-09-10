# Development tools and environments

Enable `dev-tools` in chezmoi's `data.modules`. This module manages
`~/.config/mise/config.toml` and `~/.config/dev-tools/`; it does not download
software during `chezmoi apply`. Existing project Nix flakes remain authoritative.

## Ownership

| Layer | Responsibility |
| --- | --- |
| chezmoi | Personal tool declarations, shell setup, bootstrap instructions |
| mise | Install and select global tools, with directory overrides |
| rustup | Rust toolchains, components and targets |
| uv | Python interpreters, environments, dependencies and Python applications |
| Project | Flakes, language manifests and version/lock files |

The target replaces master's asdf, nvm, standalone Bun startup, and pyenv setup.
It retains Cargo tools, optional sccache, and direnv/Nix. Poetry remains an
independent legacy module for projects that still need its configuration.


## Setup and updates

1. Install mise using its [upstream installation instructions](https://mise.jdx.dev/installing-mise.html).
   Use `~/.local/bin` for a standalone install, or the operating system's package
   manager. Install direnv separately if your flakes use it.
2. Enable `dev-tools`, review `chezmoi diff`, and run `chezmoi apply`.
3. Open a fresh shell. From your home directory, run `mise install` to install
   the global declarations (running it in a project also loads that project's config).
4. Follow the language initialization instructions below as they are introduced.

Edit `dot_config/mise/config.toml` in the chezmoi source to change shared defaults,
then apply. `mise use --global` edits the destination instead; use `chezmoi re-add
~/.config/mise/config.toml` if you intentionally make changes that way.
Rolling defaults update explicitly with `mise upgrade` from home. Update mise
itself through its installation method. Exact pins are an alternative when the
same version on every machine matters; installed versions are local state.

## Global and project scope

User defaults live in `~/.config/mise/config.toml`. A directory's `mise.toml`
overrides matching tools in parent directories and the global configuration;
unmentioned tools remain inherited. Git is not required and its root does not
stop inheritance. Commit project declarations; ignore `mise.local.toml` for
personal overrides. Keep language dependencies in their native lockfiles.

Use `mise config` and `mise ls --current` to inspect the effective configuration.
Use `mise exec -- command` or `mise run task` in CI and scripts that need mise's
full environment. Review project configuration before trusting it.

## Shells, editors, and Nix

Zsh and Bash source the same small environment file when the module is enabled.
It adds mise's shims once, without a mise prompt hook. Shims select tools for the
current directory at invocation time. direnv keeps its shell hook for flakes.
This avoids competing prompt hooks; upstream does not support mixed direnv/mise
integration. We do not generate `use mise` or change project `.envrc` files.

Nix-provided executables should precede the shims while a flake is active.
Starting a nested shell preserves existing entries; when `IN_NIX_SHELL` is set,
new fallback paths are appended. Confirm actual project behavior with
`command -v node cargo python`, enter/leave the flake, and check again.
Shims do not export all mise environment settings into the parent shell.

An editor launched independently needs its own PATH setup. For a noninteractive
job needing these personal paths, explicitly source
`~/.config/dev-tools/env.sh`. For a Nix project, run commands inside its existing
Nix environment instead of wrapping them in `mise exec`, which selects mise tools.

## Migration checks

Before retiring old installations, inventory `cargo install --list`,
`uv tool list`, `npm ls -g --depth=0` under each old Node version, and
`bun pm ls -g`. Global applications are not enumerated in master's shell config
and do not automatically migrate between managers. Check shell startup files
outside chezmoi for old installer additions. Do not delete old tool directories
until representative projects and their editors work.

Disabling the module stops management and removes its integration from rendered
shell files; it does not uninstall tools or delete previously applied files.

References: [configuration](https://mise.jdx.dev/configuration.html),
[shims](https://mise.jdx.dev/dev-tools/shims.html),
[direnv limitations](https://mise.jdx.dev/direnv.html).

## Rust

Run `~/.config/dev-tools/setup-rust` after applying. It installs rustup and sccache
through mise, refreshes native Cargo/rustc proxies without editing shell files,
preserves existing toolchains/defaults, and selects stable only if no default
exists. It adds rustfmt, Clippy and rust-src to that default toolchain.
Rerun after upgrading the mise rustup package to refresh the native proxy copy.
Rustup self-updates are disabled so mise owns the installer version.

There is deliberately no `rust` entry in mise and no global `RUSTUP_TOOLCHAIN`.
Rustup continues to honor `rust-toolchain.toml`; Cargo owns `Cargo.lock` and
`cargo install` applications. Update compilers with `rustup update`, separately
from updating the installer. Native linkers and headers still come from your
OS or project flake (for example, a C compiler/linker is required for normal
Cargo builds). Mise does not install a complete native build environment.

The shared environment enables sccache when available, unless `RUSTC_WRAPPER`
is already set (including an empty value). A Nix shell can supply its own policy;
the helper does not newly enable caching when `IN_NIX_SHELL` is set. A wrapper
inherited before entering Nix remains inherited unless the flake overrides it.
Use `RUSTC_WRAPPER= cargo build` to disable it for a command. On Linux, task-specific
sccache sockets follow `CODEX_THREAD_ID`, retaining master's behavior.

Check `rustup show active-toolchain`, `cargo --version`, and `sccache --show-stats`.
The githubgraph build explicitly sources the shared environment when this module
is enabled, so it can find Cargo without an interactive shell. If it was skipped
before Rust installation, build
`git-contribution-graph` manually with `cargo build --release --locked` and copy
its executable to `~/.local/bin/githubgraph`.
