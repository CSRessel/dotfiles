# Expected packages

Personal Pop!OS desktop baseline. Reference only: chezmoi does not install this
list. Fonts belong to the [fonts module](mod_fonts.md).

## Apt

Shell, Git tools, Neovim, JSON/YAML utilities, archives, keyboard diagnostics,
and native Firefox:

```sh
sudo apt update && sudo apt install -y ca-certificates curl git zsh tmux tree neovim gh jq yq unzip evtest fd-find firefox entr
```

### Docker Engine

Use the distribution's `docker.io` package from the existing apt sources.
This installation was verified on this Pop!OS 24.04 machine:

```sh
sudo apt update
sudo apt install --no-install-recommends docker.io
sudo systemctl start docker
sudo /usr/bin/docker info
```

Updates come through apt. The explicit `/usr/bin/docker` path selects the
system-installed CLI. This baseline does not configure Docker's upstream apt
repository or install Docker Desktop. Compose and Buildx are separate additions;
the commands above verify the Engine and CLI only.

## COSMIC Store / Flatpak

The same user-scoped Flathub apps available through COSMIC Store: Zen, Bitwarden,
Obsidian, Zed, VLC, Calibre, Tor Browser Launcher and Chrome. Requires the Store's
existing `flathub` remote. Firefox remains the default browser.

```sh
flatpak install --user flathub app.zen_browser.zen com.bitwarden.desktop md.obsidian.Obsidian dev.zed.Zed org.videolan.VLC com.calibre_ebook.calibre org.torproject.torbrowser-launcher com.google.Chrome
```

## Native installs

Entries must link to the tool's official website or installation documentation.
Do not copy installer commands or pin versions here: commands can quickly become
outdated, and embedded download URLs can suffer from link rot.
Tailscale and ChatGPT use native installers, even when backed by apt packages.

- [Ghostty — ghostty-ubuntu](https://github.com/mkasberg/ghostty-ubuntu): community native `.deb` for Pop!OS 24.04; updates use the same installer.
- [mise](https://mise.jdx.dev/installing-mise.html): installs the manager; then follow [development tools setup](dev-tools.md#setup-and-updates).
- [direnv](https://direnv.net/docs/installation.html)
- [Nix](https://nixos.org/download/#nix): install manually for project flakes.
- [Oh My Zsh](https://ohmyz.sh/#install)
- [Tailscale](https://tailscale.com/docs/install/linux)
- [ChatGPT desktop](https://learn.chatgpt.com/docs/linux/linux-app)
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Claude Code CLI](https://code.claude.com/docs/en/quickstart)

## Desktop defaults

The Linux-only `desktop-apps` module merges `~/.config/mimeapps.list`:

| Role | Default |
| --- | --- |
| Web browser | Firefox |
| Music and video | VLC |
| GUI text editor | Zed |

[The modifier](../dot_config/modify_mimeapps.list) selects only installed desktop
entries, preferring native entries when available. Missing apps leave existing
associations intact; a later apply picks up newly installed apps. Other defaults
and association groups are preserved; INI formatting and comments are not.
Text/empty files use Zed; HTML uses Firefox. Audio/video types follow the local
MIME database, plus COSMIC's music associations.

COSMIC's [Default Applications implementation](https://github.com/pop-os/cosmic-settings/blob/master/cosmic-settings/src/pages/applications/default_apps.rs)
uses these same XDG associations for browser, music, video and editor. There is
no separate RON preference for these roles. File manager, terminal and mail defaults
remain local. This module works independently of `cosmic`.
