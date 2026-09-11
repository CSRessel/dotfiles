# Checks and contributing

GitHub Actions runs on pull requests and pushes to `master`; both workflows can
also be started manually. The README badges show the actual default-branch runs
once these workflows have been pushed.

| Check | Coverage |
| --- | --- |
| Python tests | Chezmoi module boundaries, Linux/macOS rendering, config merges, shell setup, wallpaper generation and mocked dictation |
| Ruff | Python lint, import order and formatting, including the extensionless MIME-apps modifier |
| Shell syntax | Rendered apply hooks for both operating systems and literal shell scripts; none are executed by this check |
| actionlint | Workflow syntax, expressions and embedded shell via ShellCheck |
| Rust | Contribution graph formatting, Clippy warnings and locked-dependency tests/build |
| Gitleaks | Past year of Git history plus current files of any age, with findings redacted; also runs weekly |
| Pre-commit | Staged secrets, private URLs/configuration and sensitive credential filenames |
| Dependabot | Weekly update PRs for Actions, Python tooling and Rust dependencies |

Tests run on Ubuntu in temporary home directories. macOS coverage is template
rendering and mocks, not a native Mac integration test. Tests do not install system
settings, open the microphone or download a dictation model. CI has read-only
repository permissions, does not apply dotfiles to the runner's home and does not
commit formatting fixes. Third-party actions are pinned to commit SHAs; standalone
CI binaries are pinned by version and SHA-256 in [tools.json](../.github/tools.json).
Update those binary pins manually with checksums from their upstream releases.

## Run locally

Install Python 3.11+, chezmoi, Bash, Zsh and ImageMagick. For the exact pinned Linux
x86_64 CI binaries:

```sh
python3 .github/install-tools.py --directory /tmp/dotfiles-ci-bin chezmoi actionlint gitleaks
export PATH="/tmp/dotfiles-ci-bin:$PATH"
```

Use the pinned Python tooling through uv (or install `requirements-dev.txt` into
a virtual environment):

```sh
uvx --with-requirements requirements-dev.txt ruff check .
uvx --with-requirements requirements-dev.txt ruff format --check .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
actionlint
python3 .github/scan-secrets.py recent
python3 .github/scan-secrets.py files
```

Install ShellCheck for actionlint's embedded-shell checks. The `git` scan covers
the past year of commits; the `dir` scan covers current files regardless of age,
including edits that have not been committed. Neither
requires sending file contents to a scanning service. Review findings before
committing; never hide real credentials with an allowlist. The shared wrapper prints
only filenames, line numbers and rule names, suppresses scanner snippets and
deletes temporary redacted reports. CI uploads no scan reports. Older deleted content is outside the rolling history
window; expanding the window or rewriting history is a separate maintenance task.

## Pre-commit protection

The hook configuration is committed, but each clone needs a one-time installation:

```sh
uvx --with-requirements requirements-dev.txt pre-commit install --install-hooks
uvx --with-requirements requirements-dev.txt pre-commit run
```

The hook builds a commit-pinned Gitleaks version in pre-commit's isolated Go
environment; it does not require a global Gitleaks installation. Its first setup
needs network access. Commits scan staged additions, including renamed files,
without rescanning old history. A clean working copy cannot hide staged secrets.

[.gitleaks.toml](../.gitleaks.toml) extends the standard credential detectors with
private/link-local network URLs, internal hostnames and endpoint settings, account-specific AWS sign-in
URLs, credentials embedded in connection URLs, sensitive query parameters and
literal secret settings. The wrapper also blocks credential-shaped filenames,
such as `.env`, private keys, `.aws/credentials`, `auth.json` and their chezmoi
source equivalents. Example/template filenames still receive content scanning.

These are review guards, not a guarantee: a private service on an ordinary public
domain or a novel secret format may need a custom rule. Add organization-specific
patterns to `.gitleaks.toml`; review false positives explicitly rather than
disabling categories or adding real credentials to an allowlist. Inline
`gitleaks:allow` comments are not honored. Public loopback URLs and ordinary
dotfiles preferences are not automatically considered secrets.

The same content rules run in CI. Scanner tests use synthetic fixtures to check
blocking, staged-versus-unstaged handling and output privacy. Run them with
`gitleaks` on `PATH`; CI installs it automatically. Update the hook's commit pin
alongside the Gitleaks binary pin in `.github/tools.json`.

Use `ruff format .` to apply Python formatting. `.editorconfig` supplies basic
whitespace defaults for other source files; Go-template, RON and app-specific
formats are not sent through a generic formatter.

```sh
cargo +1.98.1 fmt --manifest-path git-contribution-graph/Cargo.toml -- --check
cargo +1.98.1 clippy --manifest-path git-contribution-graph/Cargo.toml --locked --all-targets -- -D warnings
cargo +1.98.1 test --manifest-path git-contribution-graph/Cargo.toml --locked
```

CI configuration, tests and documentation are excluded from chezmoi management.
Review changes with `git diff`; use `chezmoi diff` separately for any resulting
home-file changes. Resolve local conflicts before applying. Branch protection and
required checks must be configured in GitHub repository settings if desired;
adding these workflows alone does not enforce merging rules.
