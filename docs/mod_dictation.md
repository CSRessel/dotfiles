# Dictation

The `dictation` module provides `wsp-toggle`: run once to record, again to finish
and copy the transcript. It uses Moonshine Voice 0.1.5 and the English Medium
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

The notification interface dispatches to separate Linux and macOS backends.
The macOS adapter uses `osascript` and passes message text as arguments rather
than interpolating it into AppleScript. It is groundwork for a future port,
not a claim of macOS support: only its command construction is tested here.
Notification Center permissions and banner delivery still need Mac validation;
recording, clipboard ownership, process lifecycle, and installation remain
Linux-specific, and chezmoi still excludes this module on macOS. See Apple's
[notification scripting guide](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/DisplayNotifications.html).

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
model = "medium-streaming"
```

`medium-streaming` prioritizes accuracy; choose `small-streaming` or
`tiny-streaming` for lower compute use. Only
language/model combinations published by Moonshine are supported. After changing
these settings, `chezmoi apply` downloads the selected model. No old Whisper build
paths or shell aliases are needed.

Moonshine's [model catalog](https://moonshine-voice.readthedocs.io/en/latest/models/available-models/)
reports average English word error rates of 6.65% for Medium, 7.84% for Small,
and 12.00% for Tiny on its floating-point reference models. This installation uses
quantized models, whose accuracy differs; those figures are not a guarantee for
personal dictation.

On the Intel Core Ultra 5 325, a live-paced test of the 11-second whisper.cpp JFK
sample fed 100ms audio chunks at their actual arrival times. Tiny finished about
0.40s after the audio ended; Medium finished about 1.19s after it ended, about
0.79s extra. Model loading took 0.84s and 0.48s respectively in that run (cache
state affects startup). Medium correctly recognized “Americans” where Tiny
produced “America”. This single sample checks responsiveness, not overall
accuracy. Longer phrases and machine load can increase the delay.

Partial-line decoding is disabled because only the final clipboard result is
needed. This avoids repeatedly decoding text that will be replaced. See the
[streaming API](https://moonshine-voice.readthedocs.io/en/latest/using/transcription/).

Disabling the module stops chezmoi management; it does not uninstall the runtime
or remove an existing desktop shortcut. Cancel recording and remove the shortcut
when retiring the setup.
