# Dictation

The `dictation` module provides `wsp-toggle`: run once to record, again to finish
and copy the transcript. It uses Moonshine Voice 0.1.5 and the English Tiny
Streaming model by default. Recognition runs locally on the CPU while you speak;
it does not require a cloud account or upload audio. Model files download during
setup and stay outside the dotfiles repository.

The old `local-scripts` module is retired. `add_iso_prefixes.sh` and
`open_github.sh` are always installed by the base; the Docker prune helper is
removed. Remove `"local-scripts"` from old machine selections and add
`"dictation"` only where speech input is wanted.

## Setup

Add `"dictation"` to `[data].modules` with `chezmoi edit-config`, then run
`chezmoi apply`. The installer requires `uv` (available from `dev-tools`), Python 3,
`parecord`, a systemd user session, and a clipboard tool. On Pop!OS:

```sh
sudo apt install pulseaudio-utils wl-clipboard
```

Use `xclip` instead of `wl-clipboard` on X11. On apt-based systems, the installer
can download and unpack a missing `wl-clipboard` under `~/.local/share/wsp/clipboard`
without sudo; this private copy is used only by `wsp-toggle`.
The installer creates an isolated
runtime in `~/.local/share/wsp/venv`, downloads the model into Moonshine's user
cache, and records the resolved model path in `~/.local/share/wsp/model.json`.
Recording uses that local path without a network lookup. If the cache is cleared,
run `wsp-toggle setup` to restore it.

```sh
wsp-toggle                 # Start; wait for the Recording notification
wsp-toggle                 # Stop, finish transcription, copy; then paste normally
wsp-toggle cancel          # Discard the current recording
wsp-toggle status
wsp-toggle transcribe /path/to/mono.wav  # File test; prints text, leaves clipboard alone
```

Audio is streamed in memory, with a five-minute recording limit. The model is
released after each recording. A transient systemd unit owns the recorder, so
there are no shared `/tmp` audio files or stale PID files. A separate transient
clipboard owner keeps the result available after recording ends. Notifications
show loading, recording, finishing, and completion state, not transcript contents.
They use the desktop's D-Bus notification service through systemd's `busctl`;
`notify-send` is not required. Notification delivery failures are logged instead
of silently ignored. Errors are available
with `journalctl --user -u wsp-dictation.service`.

## Optional Pop!OS shortcuts

When both `cosmic` and `dictation` are enabled, the managed COSMIC `custom`
shortcuts file binds **Super+Shift+D** to `~/.local/bin/wsp-toggle`, with the home
path expanded for each machine. Press once to record, again to finish and copy.
Additional managed custom bindings belong in that same template.

To omit the dictation binding while keeping both modules, set
`cosmicShortcut = false` under `[data.dictation]` in `chezmoi edit-config`, then
apply. The `dictation` module alone installs no desktop shortcut.

On older GNOME-based Pop!OS, add `/home/YOUR_USER/.local/bin/wsp-toggle` (using
your actual home path) under **Settings → Keyboard → View and Customize Shortcuts
→ Custom Shortcuts**, with `Super+Shift+D` if unused.

## Models and performance

Optional machine-specific settings in `chezmoi edit-config`:

```toml
[data.dictation]
language = "en"
model = "tiny-streaming"
```

`small-streaming` and `medium-streaming` trade more compute for accuracy. Only
language/model combinations published by Moonshine are supported. After changing
these settings, `chezmoi apply` downloads the selected model. No old Whisper build
paths or shell aliases are needed.

The default is a speed-first choice for the Intel Core Ultra 5 325 machine tested
here, not a claim of universally fastest recognition. Review the
[model catalog](https://moonshine-voice.readthedocs.io/en/latest/models/available-models/)
and [streaming API](https://moonshine-voice.readthedocs.io/en/latest/using/transcription/).
Published benchmark results from other hardware do not predict your latency.
On this machine, the standard whisper.cpp 11-second JFK sample took about 2.0s
of total compute with Tiny Streaming and 4.1s with Small Streaming, feeding audio
in 100ms chunks. Finalization took about 0.5s and 0.8s respectively. These are
single-sample throughput checks, not an accuracy evaluation or a benchmark
against every backend. Small correctly recognized “Americans” where Tiny produced
“America”. Partial-line decoding is disabled because only the final clipboard
result is needed. This avoids repeatedly decoding text that will be replaced.

Disabling the module stops chezmoi management; it does not uninstall the runtime
or remove an existing desktop shortcut. Cancel recording and remove the shortcut
when retiring the setup.
