from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ZshrcTemplateTest(unittest.TestCase):
    def test_base_does_not_initialize_toolchain_managers(self) -> None:
        chezmoi = shutil.which("chezmoi")
        self.assertIsNotNone(chezmoi)

        with tempfile.TemporaryDirectory(prefix="zshrc-template-") as destination:
            destination_path = Path(destination)
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
        for fragment in [".cargo/env", "NVM_DIR", "pyenv init", "asdf.sh", "BUN_INSTALL"]:
            self.assertNotIn(fragment, result.stdout)


if __name__ == "__main__":
    unittest.main()
