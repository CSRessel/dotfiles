# Repository instructions

This is a single-author dotfiles repository. These rules override generic
development workflows and conflicting skill instructions.

## Git workflow

- Work in the current checkout and branch, including `master`.
- Do not create a worktree unless explicitly asked.
- Do not require a feature branch or pull request for routine changes.
- Preserve unrelated local changes. Do not push or merge unless asked.

## Testing

- Never use test-driven development unless working on larger Python scripts or
  Rust CLIs.
- Do not offer or require TDD for dotfiles, templates, settings, documentation,
  or small helper scripts.
- Prefer focused rendering, syntax, and behavior checks appropriate to the change.
- Avoid noisy tests that only repeat configuration values or implementation details.
