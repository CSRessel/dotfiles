# Noridoc: Nori Green theme snapshots

Path: @/docs/assets/nori-green

### Overview

- Backups of Nori Green mappings for different applications. They share a core
  palette, but each maps colors to its application's own UI and syntax roles.
- Sessions sources were captured at commit
  `5696cebae0e987a6183e2cf51b0a78d0fc82a749`; these are snapshots, not a live sync.

### How it fits into the larger codebase

- [Chezmoi's ignore rules](../../../.chezmoiignore) exclude `docs/` from deployment.
  These backups are not installed automatically and add no project dependencies.
- The deployed Zed theme remains
  [dot_config/zed/themes/nori-green.json](../../../dot_config/zed/themes/nori-green.json),
  selected by the [shared Zed settings](../../../.chezmoitemplates/zed-settings.json).

### Core Implementation

| Backup | Source and intended use |
| --- | --- |
| [VS Code extension](vscode/extension/package.json) | Text contents unpacked from sessions `broker/server/bootstrap/assets/nori-green.vsix`, including extension metadata, for backup or rebuilding the package. |
| [xterm palette](xterm/nori-xterm.json) | Exact copy of sessions `broker/server/bootstrap/nori-xterm.json`; terminal color mapping. |
| [CodeMirror theme](codemirror/noriTheme.ts) | Exact copy of sessions `broker/ui/src/codemirror/noriTheme.ts`; editor styling and syntax highlighting. |
| [Web palette](web/palette.css) | The first `:root` block from sessions `broker/ui/src/style.css`; shared color and font tokens, not the full stylesheet. |
| [Local VS Code theme](vscode-local/nori-green-color-theme.json) | Preserved from this Mac's `~/.config/zed/themes/nori-green-color-theme.json`. It is a different VS Code-format version, despite its former Zed directory. |

### Things to Know

- The unpacked extension retains its original publisher metadata and
  [MIT license](vscode/extension/LICENSE.txt). Its text tree is not an installable
  VSIX archive until repackaged.
- CodeMirror's source imports CodeMirror and Lezer packages from its original
  application. They are not installed or executed by this dotfiles repository.
- The local VS Code-format variant is kept separately from both the packaged
  extension theme and the deployed Zed-format theme.

Created and maintained by Nori.
