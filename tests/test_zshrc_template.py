from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ZshrcTemplateTest(unittest.TestCase):
    @unittest.skipUnless(
        sys.platform.startswith("linux"), "Linux-specific sccache configuration"
    )
    def test_linux_sccache_uses_a_per_codex_thread_socket(self) -> None:
        chezmoi = shutil.which("chezmoi")
        self.assertIsNotNone(chezmoi)

        with tempfile.TemporaryDirectory(prefix="zshrc-template-") as destination:
            destination_path = Path(destination)
            sccache = destination_path / ".cargo" / "bin" / "sccache"
            sccache.parent.mkdir(parents=True)
            sccache.touch()
            result = subprocess.run(
                [
                    str(chezmoi),
                    "--source",
                    str(REPOSITORY_ROOT),
                    "--destination",
                    destination,
                    "--persistent-state",
                    str(destination_path / "chezmoistate.boltdb"),
                    "cat",
                    str(destination_path / ".zshrc"),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        socket_block = """if [[ -n "${CODEX_THREAD_ID:-}" ]]; then
  export SCCACHE_SERVER_UDS="/tmp/sccache-${CODEX_THREAD_ID}.sock"
fi"""
        self.assertIn(socket_block, result.stdout)

        zsh = shutil.which("zsh")
        self.assertIsNotNone(zsh)
        environment = os.environ.copy()
        environment.pop("SCCACHE_SERVER_UDS", None)
        environment["CODEX_THREAD_ID"] = "thread-123"
        configured = subprocess.run(
            [
                str(zsh),
                "-fc",
                f'{socket_block}\nprint -r -- "${{SCCACHE_SERVER_UDS-unset}}"',
            ],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )
        self.assertEqual(configured.returncode, 0, configured.stderr)
        self.assertEqual(configured.stdout, "/tmp/sccache-thread-123.sock\n")

        environment.pop("CODEX_THREAD_ID")
        unconfigured = subprocess.run(
            [
                str(zsh),
                "-fc",
                f'{socket_block}\nprint -r -- "${{SCCACHE_SERVER_UDS-unset}}"',
            ],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )
        self.assertEqual(unconfigured.returncode, 0, unconfigured.stderr)
        self.assertEqual(unconfigured.stdout, "unset\n")


if __name__ == "__main__":
    unittest.main()
