"""Exercise actual scanner rules and staged-only behavior with synthetic values."""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github/scan-secrets.py"
spec = importlib.util.spec_from_file_location("secret_checks", SCRIPT)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class PrivateFilenameTest(unittest.TestCase):
    def test_sensitive_names_and_chezmoi_attributes(self):
        for path in [
            ".env",
            "private_dot_env.production",
            "private_dot_aws/credentials",
            "dot_codex/private_auth.json",
            "private_dot_ssh/private_id_ed25519",
            "backup.p12",
        ]:
            self.assertTrue(checks.private_filename(path), path)
        for path in [
            ".env.example",
            "dot_claude/settings.json",
            "dot_ssh/id_ed25519.pub",
            "config.toml",
        ]:
            self.assertFalse(checks.private_filename(path), path)


@unittest.skipUnless(
    shutil.which("gitleaks"), "install the pinned Gitleaks binary for scanner tests"
)
class SecretChecksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dotfiles-scan-test-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        subprocess.run(["git", "init", "-q", str(self.repo)], env=self.env, check=True)

    def stage(self, name, content):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        subprocess.run(["git", "add", "--", name], cwd=self.repo, env=self.env, check=True)

    def scan(self, mode="staged"):
        return subprocess.run(
            [sys.executable, str(SCRIPT), mode],
            cwd=self.repo,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_private_urls_and_literal_secrets_are_blocked_without_values_in_output(self):
        # Construct fixtures so their literal URLs never enter this repository's history.
        cases = {
            "private-network-url": "https://" + "10.42.0.7/private",
            "private-hostname-url": "https://" + "service.corp/private",
            "private-endpoint-setting": 'host = "' + "172.16.1.4" + '"',
            "aws-account-url": "https://" + "123456789012.signin.aws.amazon.com",
            "url-credentials": "postgres://" + "person:synthetic-password@db.example.com/data",
            "sensitive-url-parameter": "https://example.com/?" + "token=synthetic-private-value",
            "literal-secret-setting": 'password = "' + "synthetic-private-value" + '"',
        }
        for rule, value in cases.items():
            with self.subTest(rule=rule):
                self.stage("settings.txt", value + "\n")
                result = self.scan()
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(rule, result.stdout)
                self.assertNotIn(value, result.stdout + result.stderr)
                self.assertNotIn("synthetic-private-value", result.stdout + result.stderr)

    def test_staged_secret_cannot_be_hidden_by_clean_worktree(self):
        private_url = "https://" + "10.42.0.7/private"
        self.stage("settings.txt", private_url + "\n")
        (self.repo / "settings.txt").write_text("https://example.com\n")
        self.assertEqual(self.scan().returncode, 1)
        self.stage("settings.txt", "https://example.com\n")
        (self.repo / "settings.txt").write_text(private_url + "\n")
        self.assertEqual(self.scan().returncode, 0)
        self.assertEqual(self.scan("files").returncode, 1)

    def test_empty_credential_file_is_blocked(self):
        self.stage("private_dot_aws/credentials", "")
        result = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertIn("sensitive filename", result.stdout)


if __name__ == "__main__":
    unittest.main()
