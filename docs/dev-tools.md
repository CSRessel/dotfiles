# Development tools and environments

Enable `dev-tools` in chezmoi's `data.modules`, install
[mise](https://mise.jdx.dev/installing-mise.html), then run `ch diff` and `ch apply`.
There are no separate language setup commands.

## Ownership and updates

| Owner | Responsibility |
| --- | --- |
| chezmoi | Global mise config, shell integration, installation on apply |
| mise | Exact versions of rustup, sccache, uv, Node and Bun |
| rustup | Rust compilers, components, targets and project toolchain selection |
| uv | Python interpreters, environments, dependencies and Python applications |
| Projects | Existing flakes, language manifests and lockfiles |

Edit pins in `dot_config/mise/config.toml`, review, and apply. The apply hook
runs `mise install` every time; existing exact versions are reused and missing
tools are installed. Successful checks are silent; failures print their diagnostics.
It does not upgrade mise itself, run `mise upgrade`, or
remove older installations. Update mise through its original installation method.
The hook isolates configuration discovery from the invoking project.

The config's `[vars]` also pins the bootstrap Rust and Python versions. Rust
installs with rustfmt, Clippy and rust-src. An existing Rust default is preserved;
the pinned compiler becomes the default only if none exists. Set your preferred
default explicitly with `rustup default VERSION`. Python installs a versioned
executable without replacing system `python3`. Project toolchain selections remain
independent. Native compilers/linkers and headers still come from apt or flakes.

Rustup's native Cargo proxies are refreshed when the mise-managed installer
changes. Self-updates are disabled so mise owns the rustup version. After setup,
the githubgraph script builds the contribution graph if its executable is missing
or its tracked source changes (with one follow-up run after initial creation).

## Shells and projects

Chezmoi templates inline the shared PATH and completion setup into Bash and Zsh;
there is no deployed `~/.config/dev-tools` helper set. Apply removes only the five
retired helper files. Disabling the module stops management and automatic setup; it does not uninstall tools.

Mise shims select tools by directory. Global defaults are overridden by project
`mise.toml` files; existing `.nvmrc` and `.node-version` files are supported.
Use `mise config` and `mise ls --current` to inspect selection. Review configuration
before trusting it. Keep personal project overrides in ignored `mise.local.toml`.

Direnv retains control of flake activation; no mise prompt hook is installed.
Nix-provided tools should precede the shims. Verify paths entering/leaving your
actual flakes. Upstream does not support mixed direnv/mise integration.
Independently launched editors need their own PATH setup; use the project flake
or `mise exec -- COMMAND` for explicit execution environments as appropriate.

Interactive shells generate completions from installed mise, uv/uvx, rustup/Cargo
and Bun; Bash also loads npm completions. A fresh shell picks up tool upgrades.
Cargo and Bun global application paths remain available. sccache is enabled
unless a wrapper is already set or setup occurs inside Nix; an explicitly empty
`RUSTC_WRAPPER` disables it. Linux task sockets follow `CODEX_THREAD_ID`.

## Daily commands

- Rust: `cargo build`, `cargo test`; projects own `rust-toolchain.toml` and `Cargo.lock`.
- Python: `uv run`, `uv sync --locked`; projects own `.python-version`, `pyproject.toml`, `uv.lock`.
- Scripts: `uv init --script`, `uv add --script`, optionally `uv lock --script`.
- Python applications: `uv tool install PACKAGE` or `uvx PACKAGE`.
- JavaScript: keep project scripts, package manager and lockfile; Node includes npm/npx,
  Bun includes bunx. TypeScript and linters belong in project dev dependencies.
- `watchpytest [directory]`: runs `uv run pytest` using `entr` and `fd`/`fdfind`.
  Install entr and add pytest to the project's development dependencies.

Other global applications are explicit additions. The migration inventory found
no extra Cargo, uv or Bun applications; npm had only its bundled npm/Corepack.
Legacy Poetry, editors, marimo and k9s remain separate optional modules.

References: [mise selection](https://mise.jdx.dev/faq.html),
[chezmoi scripts](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/),
[shims](https://mise.jdx.dev/dev-tools/shims.html),
[direnv limitations](https://mise.jdx.dev/direnv.html).

`ch st` hides script entries so it reports file changes. `ch diff` still shows
scripts scheduled for apply, including the every-apply tool check.
