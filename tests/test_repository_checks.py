"""Check shell syntax and CI boundaries without executing any apply hooks."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryChecksTest(unittest.TestCase):
    def test_apply_hooks_parse_for_both_platforms(self):
        modules = list(json.loads((ROOT / ".chezmoidata.json").read_text())["modulePaths"])
        with tempfile.TemporaryDirectory(prefix="dotfiles-syntax-") as directory:
            home = Path(directory)
            config = home / "chezmoi.toml"
            env = {k: v for k, v in os.environ.items() if not k.startswith(("XDG_", "CHEZMOI_"))}
            env["HOME"] = directory
            base = [
                shutil.which("chezmoi"),
                "--source",
                str(ROOT),
                "--destination",
                directory,
                "--config",
                str(config),
                "--persistent-state",
                str(home / "state.db"),
            ]
            for platform in ["linux", "darwin"]:
                config.write_text(
                    '[data]\nemail = "test@example.com"\nmodules = '
                    + json.dumps(modules)
                    + '\n[data.tmuxMemory]\nhigh = "24G"\nmax = "32G"\nswap = "8G"\n'
                    + '[data.chezmoi]\nos = "'
                    + platform
                    + '"\n'
                )
                for source in sorted(ROOT.glob("run_*.sh.tmpl")):
                    with self.subTest(platform=platform, source=source.name):
                        rendered = subprocess.run(
                            base + ["execute-template", "--file", str(source)],
                            env=env,
                            text=True,
                            capture_output=True,
                            check=True,
                        ).stdout
                        if not rendered.strip():
                            continue
                        shell = "bash" if rendered.startswith("#!/bin/bash") else "sh"
                        result = subprocess.run(
                            [shell, "-n"],
                            input=rendered,
                            text=True,
                            capture_output=True,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                managed = subprocess.check_output(
                    base + ["managed"], env=env, text=True
                ).splitlines()
                for path in managed:
                    self.assertFalse(
                        path.startswith((".github", ".ruff_cache", "tests/", "docs/")), path
                    )
                    self.assertNotIn(
                        path,
                        [
                            ".editorconfig",
                            "ruff.toml",
                            "requirements-dev.txt",
                            ".pre-commit-config.yaml",
                            ".gitleaks.toml",
                        ],
                    )

    def test_literal_shell_scripts_parse(self):
        sources = [*ROOT.rglob("*.sh"), ROOT / "private_dot_local/bin/executable_wsp-toggle"]
        for source in sources:
            if ".git" in source.parts:
                continue
            with self.subTest(source=source.relative_to(ROOT)):
                content = source.read_text()
                shell = "bash" if "bash" in content.splitlines()[0] else "sh"
                result = subprocess.run([shell, "-n", str(source)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
