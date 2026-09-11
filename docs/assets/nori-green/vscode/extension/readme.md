# Nori Green — VS Code / code-server Theme

High contrast, accessible dark color theme with bright green accents. Inspired by [oxocarbon](https://github.com/nyoom-engineering/oxocarbon) and the [Nori](https://noriagentic.com) brand identity.

## Features

- **WCAG 2.1 accessible** — all foreground colors pass at least AA (4.5:1) against the editor background
- **Bright green hero accent** (#6fdc8c) — used for cursor, active line numbers, search matches, and primary highlights
- **Pastel companion palette** — soft coral, lavender, periwinkle, gold, and teal for syntax differentiation
- **Deep carbon base** (#161616) — easy on the eyes for long sessions
- **Full terminal ANSI colors** — integrated terminal matches the editor theme exactly
- **Semantic highlighting** — enhanced token coloring for TypeScript, Python, Rust, Go, and more

## Installation

### code-server (manual)

Copy the `nori-green` folder into your extensions directory:

```bash
cp -r nori-green ~/.local/share/code-server/extensions/nori-green
```

Then reload code-server and select the theme:
1. Open the command palette: `Ctrl+Shift+P`
2. Type: `Preferences: Color Theme`
3. Select: **Nori Green**

### code-server (VSIX)

```bash
code-server --install-extension nori-green-1.0.0.vsix
```

### VS Code (desktop)

```bash
code --install-extension nori-green-1.0.0.vsix
```

Or copy the folder to `~/.vscode/extensions/nori-green`.

## Palette

| Role             | Hex       | Usage                          |
|------------------|-----------|--------------------------------|
| Background       | `#161616` | Editor, terminal, panels       |
| Foreground       | `#f2f4f8` | Default text                   |
| Cursor / Accent  | `#6fdc8c` | Cursor, active highlights      |
| Green            | `#42be65` | Strings (normal), tags, links  |
| Bright Green     | `#6fdc8c` | Strings (bright), highlights   |
| Blue             | `#78a9ff` | Functions, properties, info    |
| Magenta          | `#be95ff` | Keywords, storage, booleans    |
| Cyan             | `#08bdba` | Types, classes, built-ins      |
| Bright Cyan      | `#3ddbd9` | Interfaces, generics, regex    |
| Yellow           | `#f2cc60` | Decorators, namespaces         |
| Bright Yellow    | `#fddc69` | Numbers, constants             |
| Red              | `#f47067` | Errors, invalid, deletions     |
| Bright Red       | `#ff9cac` | Bright errors, deprecated      |
| Comment Gray     | `#8a8f98` | Comments (italic)              |

---

Built by [Tilework Technologies](https://tilework.tech) for [Nori](https://noriagentic.com)
