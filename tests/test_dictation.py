"""Exercise dictation lifecycle without microphone access or a downloaded model."""
import importlib.util
import io
import os
from pathlib import Path
import signal
import subprocess
import sys
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("wsp", ROOT / "dot_config/dictation/wsp.py")
wsp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wsp)


class Model:
    def __init__(self):
        self.samples = 0
        self.stopped = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def start(self):
        pass

    def add_audio(self, samples, rate):
        self.samples += len(samples)

    def stop(self):
        self.stopped = True
        return self.update_transcription()

    def update_transcription(self):
        return SimpleNamespace(lines=[SimpleNamespace(text="Test transcript.")])


class DictationTest(unittest.TestCase):
    def exercise_recording(self, stop_signal):
        model = Model()
        children = []
        real_popen = subprocess.Popen
        # A fake recorder emits PCM until signalled. No microphone is opened.
        source = """
import signal, sys, time
signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
while True:
    sys.stdout.buffer.write(b'\\0' * 6400)
    sys.stdout.buffer.flush()
    time.sleep(0.05)
"""

        def spawn(*args, **kwargs):
            proc = real_popen([sys.executable, "-c", source], **kwargs)
            children.append(proc)
            return proc

        def notify(message):
            if message.startswith("Recording"):
                signal.raise_signal(stop_signal)

        handlers = {s: signal.getsignal(s) for s in (signal.SIGUSR1, signal.SIGTERM, signal.SIGINT)}
        try:
            with patch.object(wsp, "engine", return_value=model), \
                    patch.object(wsp, "config", return_value={"max_seconds": 5}), \
                    patch.object(wsp.subprocess, "Popen", side_effect=spawn), \
                    patch.object(wsp, "notify", side_effect=notify), \
                    patch.object(wsp, "copy_text") as copied:
                wsp.record()
                self.assertTrue(all(p.poll() is not None for p in children))
                return model, copied.call_args_list
        finally:
            for s, handler in handlers.items():
                signal.signal(s, handler)

    def test_stop_finalizes_and_copies(self):
        model, copies = self.exercise_recording(signal.SIGUSR1)
        self.assertTrue(model.stopped)
        self.assertGreater(model.samples, 0)
        self.assertEqual(copies[0].args, ("Test transcript.",))

    def test_cancel_reaps_recorder_without_copy(self):
        model, copies = self.exercise_recording(signal.SIGTERM)
        self.assertFalse(model.stopped)
        self.assertEqual(copies, [])

    def test_toggle_stops_only_our_service_main_process(self):
        with patch.object(wsp.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as run, \
                patch.object(wsp, "notify") as notify:
            wsp.control("toggle")
            self.assertIn("--signal=SIGUSR1", run.call_args.args[0])
            self.assertIn("--kill-whom=main", run.call_args.args[0])
            self.assertEqual(run.call_args.args[0][-1], wsp.UNIT)
            self.assertIn("Finishing dictation", notify.call_args.args[0])

    def test_notifications_work_without_notify_send(self):
        with patch.object(wsp.shutil, "which", return_value=None), \
                patch.object(wsp.subprocess, "run", return_value=SimpleNamespace(stdout="u 42\n")) as run:
            self.assertEqual(wsp.notify("Recording"), 42)
            command = run.call_args.args[0]
            self.assertEqual(command[0], "busctl")
            self.assertIn("org.freedesktop.Notifications", command)
            self.assertIn("Recording", command)
            self.assertTrue(run.call_args.kwargs["check"])

    def test_notification_failure_is_logged_without_stopping_dictation(self):
        failure = subprocess.CalledProcessError(1, ["busctl"], stderr="Notification service unavailable")
        with patch.object(wsp.subprocess, "run", side_effect=failure), \
                patch("sys.stderr", new_callable=io.StringIO) as log:
            self.assertIsNone(wsp.notify("Recording"))
            self.assertIn("notification failed: Notification service unavailable", log.getvalue())

    def test_start_uses_transient_service_and_session_environment(self):
        with patch.dict(os.environ, {"WAYLAND_DISPLAY": "wayland-test"}), \
                patch.object(wsp.subprocess, "run", return_value=SimpleNamespace(returncode=3)) as run:
            wsp.control("toggle")
            command = run.call_args.args[0]
            self.assertEqual(command[0], "systemd-run")
            self.assertIn("--setenv=WAYLAND_DISPLAY=wayland-test", command)
            self.assertEqual(command[-1], "record")

    def test_clipboard_owner_outlives_recording(self):
        with patch.dict(os.environ, {"WAYLAND_DISPLAY": "wayland-test"}), \
                patch.object(wsp.shutil, "which", return_value="/usr/bin/wl-copy"), \
                patch.object(wsp.subprocess, "run") as run:
            wsp.copy_text("Hello\nworld")
            command = run.call_args.args[0]
            self.assertIn("--unit=wsp-clipboard", command)
            self.assertIn("--foreground", command)
            data = next(x.split("=", 2)[2] for x in command if x.startswith("--property=StandardInputData="))
            self.assertEqual(wsp.base64.b64decode(data), b"Hello\nworld")


if __name__ == "__main__":
    unittest.main()
