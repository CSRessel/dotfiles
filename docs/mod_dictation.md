# Dictation

The `dictation` module provides `wsp-toggle`: run once to record, again to finish
and copy the transcript. It builds whisper.cpp with Vulkan acceleration and
`ggml-base.en.bin` model. Audio is recorded first, then transcribed locally when
you stop. This favors the previous dictation quality over streaming speed.
No cloud account is required and no audio is uploaded.

The old `local-scripts` module is retired. `add_iso_prefixes.sh` and
`open_github.sh` are always installed by the base; the Docker prune helper is
removed. Remove `"local-scripts"` from old machine selections and add
`"dictation"` only where speech input is wanted.

## Setup

Add `"dictation"` to `[data].modules` with `chezmoi edit-config`, then run
`chezmoi apply`. On Pop!OS/Ubuntu, the module installs missing system packages
with `sudo apt-get`, clones [whisper.cpp](https://github.com/ggml-org/whisper.cpp)
at pinned release **v1.9.4**, builds the CLI, and downloads the `base.en` model.
The first apply needs network access and may ask for your sudo password.

Everything lives under `~/.local/share/wsp`:

- Source: `~/.local/share/wsp/whisper.cpp`
- Executable: `~/.local/share/wsp/whisper.cpp/build/bin/whisper-cli`
- Model: `~/.local/share/wsp/models/ggml-base.en.bin`

Builds use two jobs. Subsequent installer runs reuse the checkout, incremental
build, and downloaded model. Downloads are checksum-verified before installation.
Local source edits cause setup to stop rather than overwrite them.

On other Linux distributions, install Python 3, PulseAudio utilities (`parecord`),
systemd, Git, CMake, a C++ toolchain, curl, Vulkan headers/loader, `glslc`, SPIR-V headers, GPU Vulkan
drivers, and `wl-clipboard` (Wayland) or `xclip` (X11) before applying.
Set `vulkan = false` under `[data.dictation]` for a CPU-only build.
Moonshine and its Python environment are no longer used.

```sh
wsp-toggle                 # Start; wait for the Recording notification
wsp-toggle                 # Stop, finish transcription, copy; then paste normally
wsp-toggle cancel          # Discard the current recording
wsp-toggle status
wsp-toggle transcribe /path/to/mono.wav  # File test; prints text, leaves clipboard alone
```

Audio is stored in a private temporary WAV file, with a five-minute recording
limit. The file is deleted after completion, cancellation, or a handled error.
The model is released after each transcription. A transient systemd unit owns the recorder, so
there are no shared `/tmp` audio files or stale PID files. A separate transient
clipboard owner keeps the result available after recording ends. Notifications
show loading, recording, finishing, and completion state, not transcript contents.
They use the desktop's D-Bus notification service through systemd's `busctl`;
`notify-send` is not required. Notification delivery failures are logged instead
of silently ignored. Errors are available
with `journalctl --user -u wsp-dictation.service`.

The notification interface dispatches to separate Linux and macOS backends.
The macOS adapter uses `osascript` and passes message text as arguments rather
than interpolating it into AppleScript. It is groundwork for a future port,
not a claim of macOS support: only its command construction is tested here.
Notification Center permissions and banner delivery still need Mac validation;
recording, clipboard ownership, process lifecycle, and installation remain
Linux-specific, and chezmoi still excludes this module on macOS. See Apple's
[notification scripting guide](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/DisplayNotifications.html).

## Optional Pop!OS shortcuts

When both `de-cosmic` and `dictation` are enabled, the managed COSMIC `custom`
shortcuts file binds **Super+Shift+D** to `~/.local/bin/wsp-toggle`, with the home
path expanded for each machine. Press once to record, again to finish and copy.
Additional managed custom bindings belong in that same template.

To omit the dictation binding while keeping both modules, set
`cosmicShortcut = false` under `[data.dictation]` in `chezmoi edit-config`, then
apply. The `dictation` module alone installs no desktop shortcut.

On older GNOME-based Pop!OS, add `/home/YOUR_USER/.local/bin/wsp-toggle` (using
your actual home path) under **Settings → Keyboard → View and Customize Shortcuts
→ Custom Shortcuts**, with `Super+Shift+D` if unused.

## Model configuration

Optional machine-specific settings in `chezmoi edit-config`:

```toml
[data.dictation]
language = "en"
# Optional: use an existing installation instead of the managed defaults.
# binary = "~/my-whisper/build/bin/whisper-cli"
# model = "~/my-models/ggml-base.en.bin"
vulkan = true
```

`model` is a GGML model file path, not a Moonshine model name. Remove any old
`model = "medium-streaming"` override to use the restored default. Run
`chezmoi apply` after changing settings. A custom `binary` skips the managed build;
a custom `model` skips the download. `wsp-toggle setup` only checks the paths.
Transcription begins after stopping; allow time for whisper.cpp to finish.

Disabling the module stops chezmoi management; it does not uninstall the runtime
or remove an existing desktop shortcut. Cancel recording and remove the shortcut
when retiring the setup.
