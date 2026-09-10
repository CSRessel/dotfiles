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
4. Follow the language initialization instructions below.

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

## Python

Run `~/.config/dev-tools/setup-python` after applying. It installs uv through
mise and Python 3.14 through uv. Pass a version, for example
`~/.config/dev-tools/setup-python 3.13`, for another interpreter. The default
bootstrap installs a versioned `python3.14` executable in uv's normal bin location
(`~/.local/bin` by default); it does not replace `python` or system `python3`.
Use `uv run --python 3.14 script.py` when the interpreter matters.

Projects own `.python-version`, `pyproject.toml`, and `uv.lock`:

```sh
uv python pin 3.14
uv sync --locked
uv run python your_script.py
```

For standalone scripts, `uv init --script script.py` and
`uv add --script script.py requests` record inline dependencies.
Use `uv lock --script script.py` when a script needs a dependency lockfile.
Use `uv tool install PACKAGE` for persistent applications and `uvx PACKAGE`
for occasional use. Existing tools can be inspected with `uv tool list`.
There is no mise Python declaration, pyenv initialization, or automatic virtualenv
activation; uv owns `.venv` and `uv run` supplies the correct project context.

Upgrade the uv executable with `mise upgrade uv` from home, and Python with
uv's Python management commands. Do not use `uv self update` for a mise install.
The old Poetry config remains optional; projects requiring Poetry must install
it explicitly, for example with `uv tool install poetry`.

Reference: [uv Python installation](https://docs.astral.sh/uv/guides/install-python/),
[uv scripts](https://docs.astral.sh/uv/guides/scripts/).

## JavaScript and TypeScript

Run `~/.config/dev-tools/setup-javascript` after applying. Mise installs Node's
current LTS release (with npm/npx) and Bun (with bunx). Update with
`mise upgrade node bun` from home; use mise rather than `bun upgrade`.
The rolling `lts` default may cross a Node major release when LTS changes.

Existing `.nvmrc` and `.node-version` files are supported through mise's Node
idiomatic-file setting. Run `mise install` in an existing project to install its
requested version; shims select it on invocation. A conflicting Node declaration
in `mise.toml` takes precedence. Do not initialize nvm or asdf alongside this setup.
Use `mise use node@VERSION` or `mise use bun@VERSION` for new project declarations.

TypeScript, linters and build tools belong in `package.json` dev dependencies.
Keep the project's selected package manager, scripts, and lockfile; this does not
convert npm/pnpm/Yarn projects to Bun. Install a project's required pnpm or Yarn
explicitly; Node/npm/Bun do not guarantee those commands are available.

The shared PATH retains Bun's global application directory (`~/.bun/bin`, or
`$BUN_INSTALL/bin`) behind mise shims on fresh setup. npm globals from nvm are tied
to the old Node installation; inventory and reinstall desired applications under
the new Node, or declare standalone CLIs in mise. Bun global applications remain
in their existing location. Do not assume an old `~/.bun/_bun` completion script
matches the new runtime; regenerate completions with the installed Bun if desired.

Check `command -v node npm bun`, their version output, and a representative
project's existing test command. Check again inside a flake to verify its runtimes
win, and after leaving it to verify personal defaults return.

Reference: [mise Node](https://mise.jdx.dev/lang/node.html),
[mise Bun](https://mise.jdx.dev/lang/bun.html).

## Shell conveniences

Interactive Bash and Zsh load completions generated by installed mise, uv/uvx,
rustup/Cargo and Bun; Bash also loads npm completions. This does not enable
mise's PATH activation hook or run completion installers that edit shell files.
A fresh shell picks up tool upgrades.

`watchpytest [directory]` uses `entr` and `fd`/`fdfind` to run `uv run pytest`
from the current project. Add pytest to that project's development dependencies.
The helper is available when uv, entr and a file finder are installed.

The githubgraph apply script retries when its executable is missing. Its changed
presence marker also causes one follow-up build on the next apply after creation.
