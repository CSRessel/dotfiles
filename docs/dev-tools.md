# Development tools and environments

Enable `dev-tools` in chezmoi's `data.modules`, install
[mise](https://mise.jdx.dev/installing-mise.html), then run `ch diff` and `ch apply`.
There are no separate language setup commands.

## Ownership and updates

| Owner | Responsibility |
| --- | --- |
| chezmoi | Global mise and user Nix configs, shell integration, mise tool installation on apply |
| mise | Exact versions of rustup, sccache, uv, Node, Bun, kubectl, gh, btop and mold |
| Native Nix installation | Nix itself, the shared store, daemon and upgrades |
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
independent. Native compilers and headers still come from apt or flakes.
Mise installs mold on Linux; projects choose whether to use it as their linker.

Kubectl and gh are shared CLI defaults; btop and mold are Linux-only with the
selected release packages. Override kubectl in a project's `mise.toml` to match
its cluster: the client must stay within one minor version of the server
([compatibility guidance](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)).

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

Independently launched editors need their own PATH setup; use the project flake
or `mise exec -- COMMAND` for explicit execution environments as appropriate.

Interactive shells generate completions from installed mise, gh, kubectl, uv/uvx,
rustup/Cargo and Bun; Bash also loads npm completions. A fresh shell picks up tool upgrades.
Cargo and Bun global application paths remain available. sccache is enabled
unless a wrapper is already set or setup occurs inside Nix; an explicitly empty
`RUSTC_WRAPPER` disables it. Linux task sockets follow `CODEX_THREAD_ID`.

## Nix and project flakes

Install upstream Nix separately using the [native installation link](packages.md#native-installs);
use the recommended multi-user installation on Pop!OS. The installer owns the
store, daemon and system shell initialization. Update Nix through its native
installation; mise and chezmoi do not install or upgrade it.

Enable `nix` in chezmoi's `data.modules`, then review and apply. This deploys
`~/.config/nix/nix.conf`, enabling `nix-command`, `flakes` and `keep-outputs`.
Installing Nix alone does not enable this module. Open a fresh shell afterward.

Projects retain their existing `flake.nix`, `flake.lock` and `.envrc`. Use
`nix develop`, or direnv for directory-based activation. Bash and Zsh load direnv's
hook when installed; no mise prompt hook is registered. Nix-provided tools should
precede mise shims inside a flake environment; verify selection when entering and
leaving a project. Upstream mise does not support mixed direnv/mise integration.

[nix-direnv](https://github.com/nix-community/nix-direnv) is an optional follow-up
for cached flake environments; this repository does not configure it.

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
