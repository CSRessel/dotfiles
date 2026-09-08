"""Exercise module boundaries and recoverable deletion without touching the real home."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BaseSettingsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dotfiles-base-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(("XDG_", "CHEZMOI_"))}
        self.env["HOME"] = str(self.home)
        self.config = self.home / "chezmoi.toml"
        self.config.write_text('[data]\nemail = "test@example.com"\nmodules = []\n')
        self.base = [shutil.which("chezmoi"), "--source", str(ROOT),
                     "--destination", str(self.home), "--config", str(self.config),
                     "--persistent-state", str(self.home / "state.db")]

    def cm(self, *args, ok=True):
        p = subprocess.run(self.base + list(args), env=self.env,
                           capture_output=True, text=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stderr)
        return p

    def test_base_and_selected_modules(self):
        paths = self.cm("managed").stdout.splitlines()
        for path in [".bashrc", ".bash_profile", ".zshrc", ".gitconfig", ".tmux.conf"]:
            self.assertIn(path, paths)
        for path in [".codex", ".config/ghostty", ".config/systemd", ".claude"]:
            self.assertNotIn(path, paths)
        self.config.write_text('[data]\nemail = "test@example.com"\n'
                               'modules = ["ghostty", "codex"]\n')
        paths = self.cm("managed").stdout.splitlines()
        self.assertIn(".config/ghostty/config", paths)
        self.assertIn(".codex/config.toml", paths)
        self.assertNotIn(".claude/settings.json", paths)

    def test_macos_excludes_linux_policy(self):
        self.config.write_text('[data]\nmodules = ["tmux-memory", "user-oom-policy", "ghostty"]\n')
        self.base += ["--override-data", json.dumps({"chezmoi": {"os": "darwin"}})]
        paths = self.cm("managed").stdout.splitlines()
        self.assertIn(".bashrc", paths)
        self.assertIn(".config/ghostty/config", paths)
        self.assertFalse(any(path.startswith(".config/systemd") for path in paths))

    def test_memory_limits_are_explicit(self):
        self.config.write_text('[data]\nmodules = ["tmux-memory"]\n')
        target = str(self.home / ".config/systemd/user/tmux-spawn-.scope.d/50-oom-protection.conf")
        p = self.cm("cat", target, ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.config.write_text('[data]\nmodules = ["tmux-memory"]\n'
                               '[data.tmuxMemory]\nhigh = "6G"\nmax = "8G"\nswap = "2G"\n')
        rendered = self.cm("cat", target).stdout
        for expected in ["MemoryHigh=6G", "MemoryMax=8G", "MemorySwapMax=2G"]:
            self.assertIn(expected, rendered)
        self.assertNotIn(".config/systemd/user.conf.d/10-oom-policy.conf",
                         self.cm("managed").stdout)

    def test_init_preserves_module_selection(self):
        self.cm("init", "--promptDefaults")
        self.config.write_text('[data]\nemail = "test@example.com"\nmodules = ["ghostty"]\n')
        self.cm("init", "--no-tty")
        self.assertIn('"ghostty"', self.config.read_text())

    def test_aliases_and_trash_on_available_shells(self):
        aliases = self.home / "aliases.sh"
        aliases.write_text(self.cm("cat", str(self.home / ".sh_aliases")).stdout)
        bindir = self.home / "bin"
        bindir.mkdir()
        for name in ["gio", "trash", "bat", "lvim", "podman", "minikube"]:
            exe = bindir / name
            exe.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$TRASH_LOG"\n')
            exe.chmod(0o755)
        env = dict(self.env, PATH=str(bindir), TRASH_LOG=str(self.home / "trash.log"))
        target = self.home / "keep me"
        target.write_text("must survive")
        for shell in [shutil.which("bash"), shutil.which("zsh")]:
            if not shell:
                continue
            script = '''source "$1"
for name in cat vim docker kubectl cp df tmux; do
    if alias "$name" >/dev/null 2>&1; then exit 10; fi
done
alias rm >/dev/null || exit 11
uname() { printf 'Linux\\n'; }
safe_rm -rf -- "$2" || exit 12
safe_rm --unsupported "$2" 2>/dev/null && exit 13
uname() { printf 'Darwin\\n'; }
safe_rm -- "$2" || exit 14
'''
            p = subprocess.run([shell, "-fc", script, "test", str(aliases), str(target)],
                               env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(target.exists())
            self.assertIn(str(target), (self.home / "trash.log").read_text())
        # No backend must never silently fall back to permanent deletion.
        for name in ["gio", "trash"]:
            (bindir / name).unlink()
        p = subprocess.run([shutil.which("bash"), "-fc",
                            'source "$1"; uname() { printf "Linux\\n"; }; safe_rm "$2"',
                            "test", str(aliases), str(target)], env=env,
                           capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertTrue(target.exists())


if __name__ == "__main__":
    unittest.main()
