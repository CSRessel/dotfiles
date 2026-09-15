#!/usr/bin/env python3
"""Local whisper.cpp dictation; systemd owns recording processes, never PID files."""

import argparse
import base64
import json
import os
import selectors
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

UNIT = "wsp-dictation.service"
CONFIG = Path.home() / ".config/dictation/config.json"


def notify(message):
    """Send status through a platform backend; notification failures are nonfatal."""
    try:
        if sys.platform == "darwin":
            return notify_macos(message)
        if sys.platform.startswith("linux"):
            return notify_linux(message)
        raise NotImplementedError(f"Notifications are not implemented on {sys.platform}")
    except (
        OSError,
        subprocess.SubprocessError,
        ValueError,
        IndexError,
        NotImplementedError,
    ) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        print(f"wsp-toggle: notification failed: {detail.strip()}", file=sys.stderr)
        return None


def notify_linux(message):
    # busctl is supplied by systemd, which dictation already requires. Do not
    # silently depend on the optional notify-send/libnotify-bin package.
    command = [
        "busctl",
        "--user",
        "--timeout=5s",
        "call",
        "org.freedesktop.Notifications",
        "/org/freedesktop/Notifications",
        "org.freedesktop.Notifications",
        "Notify",
        "susssasa{sv}i",
        "Dictation",
        "0",
        "audio-input-microphone",
        "Dictation",
        message,
        "0",
        "1",
        "urgency",
        "y",
        "1",
        "4000",
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=6)
    return int(result.stdout.split()[1])


def notify_macos(message):
    """Future macOS port: Notification Center adapter, not yet validated on a Mac."""
    # Keep message text out of AppleScript source, including quotes and newlines.
    # Capture, clipboard ownership, and lifecycle still need macOS backends.
    command = [
        "/usr/bin/osascript",
        "-e",
        "on run argv",
        "-e",
        'display notification (item 1 of argv) with title "Dictation"',
        "-e",
        "end run",
        "--",
        message,
    ]
    subprocess.run(command, capture_output=True, text=True, check=True, timeout=6)
    return True


def config():
    return json.loads(CONFIG.read_text())


def engine():
    cfg = config()
    binary = Path(cfg["binary"]).expanduser()
    model = Path(cfg["model"]).expanduser()
    if not binary.is_file() or not os.access(binary, os.X_OK):
        raise RuntimeError(f"whisper.cpp executable missing: {binary}; set dictation.binary.")
    if not model.is_file():
        raise RuntimeError(f"Whisper model missing: {model}; set dictation.model.")
    return [str(binary), "-m", str(model), "-l", cfg["language"], "-nt", "-np"]


def setup():
    command = engine()
    subprocess.run([command[0], "--help"], check=True, capture_output=True, timeout=30)
    print(f"Dictation ready: whisper.cpp / {config()['model']}")


def copy_text(text):
    if os.environ.get("WAYLAND_DISPLAY") and shutil.which("wl-copy"):
        command = [shutil.which("wl-copy"), "--foreground", "--type", "text/plain;charset=utf-8"]
    elif os.environ.get("DISPLAY") and shutil.which("xclip"):
        command = [shutil.which("xclip"), "-quiet", "-selection", "clipboard"]
    else:
        raise RuntimeError(
            "No clipboard available; install wl-clipboard for Wayland or xclip for X11."
        )
    # Clipboard owners must outlive the recording unit. Give the owner its own
    # transient service; input is passed in memory, with no transcript file.
    subprocess.run(
        ["systemctl", "--user", "stop", "wsp-clipboard.service"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    launch = [
        "systemd-run",
        "--user",
        "--collect",
        "--quiet",
        "--unit=wsp-clipboard",
        "--property=Type=exec",
        "--property=StandardInput=data",
        "--property=StandardInputData=" + base64.b64encode(text.encode()).decode(),
        "--property=StandardOutput=null",
        "--property=StandardError=null",
    ]
    launch += session_environment()
    subprocess.run(launch + command, check=True, timeout=10)


def session_environment():
    return [
        f"--setenv={key}={os.environ[key]}"
        for key in (
            "DISPLAY",
            "WAYLAND_DISPLAY",
            "XDG_RUNTIME_DIR",
            "PULSE_SERVER",
            "DBUS_SESSION_BUS_ADDRESS",
            "PATH",
        )
        if key in os.environ
    ]


def transcribe(path):
    result = subprocess.run(
        engine() + ["-f", str(path)], capture_output=True, text=True, check=True
    )
    return " ".join(result.stdout.split()).strip()


def record():
    stopping = False
    cancelled = False

    def request_stop(signum, _frame):
        nonlocal stopping, cancelled
        stopping = True
        cancelled = cancelled or signum != signal.SIGUSR1

    for sig in (signal.SIGUSR1, signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, request_stop)
    engine()  # Validate the existing whisper.cpp installation before recording.
    with tempfile.TemporaryDirectory(prefix="wsp-") as temporary:
        if stopping:
            return
        audio_path = Path(temporary) / "recording.wav"
        audio = wave.open(str(audio_path), "wb")
        audio.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
        recorder = subprocess.Popen(
            [
                "parecord",
                "--raw",
                "--format=s16le",
                "--rate=16000",
                "--channels=1",
                "--latency-msec=100",
            ],
            stdout=subprocess.PIPE,
        )
        pending = b""
        deadline = time.monotonic() + config()["max_seconds"]
        stopped_at = None
        selector = selectors.DefaultSelector()
        selector.register(recorder.stdout, selectors.EVENT_READ)
        received_audio = False
        try:
            while True:
                if time.monotonic() >= deadline:
                    stopping = True
                if stopping and stopped_at is None:
                    recorder.send_signal(signal.SIGINT)
                    stopped_at = time.monotonic()
                if cancelled:
                    return
                if stopped_at is not None and time.monotonic() - stopped_at > 5:
                    raise RuntimeError("Recorder did not stop.")
                if not selector.select(timeout=0.1):
                    continue
                chunk = os.read(recorder.stdout.fileno(), 6400)
                if not chunk:
                    if not stopping:
                        raise RuntimeError(
                            "Microphone recording ended unexpectedly; check audio input."
                        )
                    break
                if not received_audio:
                    notify("Recording. Run wsp-toggle again to finish and copy.")
                    received_audio = True
                pending += chunk
                complete = len(pending) // 2 * 2
                if complete:
                    audio.writeframesraw(pending[:complete])
                    pending = pending[complete:]
            recorder.wait(timeout=5)
            if recorder.returncode not in (0, -signal.SIGINT):
                raise RuntimeError(f"Recorder failed with exit code {recorder.returncode}.")
            audio.close()  # Flush the WAV header before whisper.cpp reads it.
            notify("Transcribing with whisper.cpp…")
            text = transcribe(audio_path)
            if cancelled:
                return
            if text:
                copy_text(text)
                notify("Transcription copied. Paste it where you need it.")
            else:
                notify("No speech detected; clipboard unchanged.")
        finally:
            audio.close()
            selector.close()
            if recorder.poll() is None:
                recorder.terminate()
                try:
                    recorder.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    recorder.kill()
                    recorder.wait()
            recorder.stdout.close()


def control(action):
    active = subprocess.run(["systemctl", "--user", "is-active", "--quiet", UNIT]).returncode == 0
    if action == "status":
        print("Recording or finishing transcription" if active else "Idle")
    elif action == "cancel":
        if active:
            subprocess.run(["systemctl", "--user", "stop", UNIT], check=True)
        notify("Dictation cancelled.")
    elif active:
        subprocess.run(
            ["systemctl", "--user", "kill", "--kill-whom=main", "--signal=SIGUSR1", UNIT],
            check=True,
        )
        notify("Finishing dictation… The transcript will be copied shortly.")
    else:
        command = [
            "systemd-run",
            "--user",
            "--collect",
            "--quiet",
            f"--unit={UNIT}",
            "--property=Type=exec",
            "--property=RuntimeMaxSec=900",
            "--property=TimeoutStopSec=5",
            "--property=UMask=0077",
        ]
        command += session_environment()
        command += [sys.executable, str(Path(__file__).resolve()), "record"]
        subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        nargs="?",
        default="toggle",
        choices=["toggle", "status", "cancel", "setup", "record", "transcribe"],
    )
    parser.add_argument("wav", nargs="?")
    args = parser.parse_args()
    if args.action == "setup":
        setup()
    elif args.action == "record":
        record()
    elif args.action == "transcribe":
        if not args.wav:
            parser.error("transcribe requires a WAV file")
        print(transcribe(args.wav))
    else:
        control(args.action)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"wsp-toggle: {exc}", file=sys.stderr)
        notify("Dictation failed. Check: journalctl --user -u wsp-dictation.service")
        sys.exit(1)
