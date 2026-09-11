#!/usr/bin/env python3
"""Local streaming dictation; systemd owns recording processes, never PID files."""
import argparse
import array
import base64
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import sys
import time

UNIT = "wsp-dictation.service"
CONFIG = Path.home() / ".config/dictation/config.json"
MODEL = Path.home() / ".local/share/wsp/model.json"


def notify(message):
    # busctl is supplied by systemd, which dictation already requires. Do not
    # silently depend on the optional notify-send/libnotify-bin package.
    command = ["busctl", "--user", "--timeout=5s", "call",
               "org.freedesktop.Notifications", "/org/freedesktop/Notifications",
               "org.freedesktop.Notifications", "Notify", "susssasa{sv}i",
               "Dictation", "0", "audio-input-microphone", "Dictation", message,
               "0", "1", "urgency", "y", "1", "4000"]
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                check=True, timeout=6)
        return int(result.stdout.split()[1])
    except (OSError, subprocess.SubprocessError, ValueError, IndexError) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        print(f"wsp-toggle: notification failed: {detail.strip()}", file=sys.stderr)
        return None


def config():
    return json.loads(CONFIG.read_text())


def setup():
    from moonshine_voice import ModelArch
    from moonshine_voice.download import get_model_for_language
    cfg = config()
    arch = ModelArch[cfg["model"].replace("-", "_").upper()]
    path, arch = get_model_for_language(cfg["language"], arch)
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    temporary = MODEL.with_suffix(".tmp")
    temporary.write_text(json.dumps({"path": path, "arch": arch.value,
                                     "language": cfg["language"], "model": cfg["model"]}))
    temporary.replace(MODEL)
    print(f"Dictation ready: {cfg['language']} / {cfg['model']}")


def engine():
    from moonshine_voice import ModelArch, Transcriber
    saved = json.loads(MODEL.read_text())
    cfg = config()
    if any(saved[key] != cfg[key] for key in ("language", "model")):
        raise RuntimeError("Model selection changed; run wsp-toggle setup first.")
    # No network lookup at recording time. Two-second updates reduce repeated
    # decoding; stop() still immediately finalizes the last partial phrase.
    return Transcriber(saved["path"], ModelArch(saved["arch"]), update_interval=2,
                       options={"return_audio_data": "false", "decode_incomplete_lines": "false"})


def copy_text(text):
    if os.environ.get("WAYLAND_DISPLAY") and shutil.which("wl-copy"):
        command = [shutil.which("wl-copy"), "--foreground", "--type", "text/plain;charset=utf-8"]
    elif os.environ.get("DISPLAY") and shutil.which("xclip"):
        command = [shutil.which("xclip"), "-quiet", "-selection", "clipboard"]
    else:
        raise RuntimeError("No clipboard available; install wl-clipboard for Wayland or xclip for X11.")
    # Clipboard owners must outlive the recording unit. Give the owner its own
    # transient service; input is passed in memory, with no transcript file.
    subprocess.run(["systemctl", "--user", "stop", "wsp-clipboard.service"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    launch = ["systemd-run", "--user", "--collect", "--quiet", "--unit=wsp-clipboard",
              "--property=Type=exec", "--property=StandardInput=data",
              "--property=StandardInputData=" + base64.b64encode(text.encode()).decode(),
              "--property=StandardOutput=null", "--property=StandardError=null"]
    launch += session_environment()
    subprocess.run(launch + command, check=True, timeout=10)


def session_environment():
    return [f"--setenv={key}={os.environ[key]}" for key in
            ("DISPLAY", "WAYLAND_DISPLAY", "XDG_RUNTIME_DIR", "PULSE_SERVER",
             "DBUS_SESSION_BUS_ADDRESS", "PATH") if key in os.environ]


def transcribe(path):
    from moonshine_voice import load_wav_file
    audio, rate = load_wav_file(path)
    with engine() as model:
        model.start()
        for offset in range(0, len(audio), rate // 10):
            model.add_audio(audio[offset:offset + rate // 10], rate)
        transcript = model.stop()
        if transcript is None:
            raise RuntimeError("Speech recognition failed while finalizing.")
        return " ".join(line.text.strip() for line in transcript.lines).strip()


def record():
    stopping = False
    cancelled = False

    def request_stop(signum, _frame):
        nonlocal stopping, cancelled
        stopping = True
        cancelled = cancelled or signum != signal.SIGUSR1

    for sig in (signal.SIGUSR1, signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, request_stop)
    notify("Loading speech model…")
    with engine() as model:
        if stopping:
            return
        model.start()
        recorder = subprocess.Popen(
            ["parecord", "--raw", "--format=float32le", "--rate=16000", "--channels=1",
             "--latency-msec=100"], stdout=subprocess.PIPE)
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
                        raise RuntimeError("Microphone recording ended unexpectedly; check audio input.")
                    break
                if not received_audio:
                    notify("Recording. Run wsp-toggle again to finish and copy.")
                    received_audio = True
                pending += chunk
                complete = len(pending) // 4 * 4
                if complete:
                    samples = array.array("f", pending[:complete])
                    if sys.byteorder != "little":
                        samples.byteswap()
                    model.add_audio(samples, 16000)
                    pending = pending[complete:]
            transcript = model.stop()
            if transcript is None:
                raise RuntimeError("Speech recognition failed while finalizing.")
            text = " ".join(line.text.strip() for line in transcript.lines).strip()
            if text:
                copy_text(text)
                notify("Transcription copied. Paste it where you need it.")
            else:
                notify("No speech detected; clipboard unchanged.")
        finally:
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
        subprocess.run(["systemctl", "--user", "kill", "--kill-whom=main",
                        "--signal=SIGUSR1", UNIT], check=True)
        notify("Finishing dictation… The transcript will be copied shortly.")
    else:
        command = ["systemd-run", "--user", "--collect", "--quiet", f"--unit={UNIT}",
                   "--property=Type=exec", "--property=RuntimeMaxSec=360",
                   "--property=TimeoutStopSec=5", "--property=UMask=0077"]
        command += session_environment()
        command += [sys.executable, str(Path(__file__).resolve()), "record"]
        subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", default="toggle",
                        choices=["toggle", "status", "cancel", "setup", "record", "transcribe"])
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
