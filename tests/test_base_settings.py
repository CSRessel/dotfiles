"""Exercise module boundaries and recoverable deletion without touching the real home."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP_CONFIGS = [
    ".config/ghostty/config", ".config/kitty/kitty.conf", ".config/lvim/config.lua",
    ".config/Code/User/settings.json", ".config/marimo/marimo.toml",
    ".config/tridactyl/tridactylrc", ".nethackrc", ".config/nix/nix.conf",
    ".claude/settings.json",
    ".codex/config.toml", ".codex/notify.py",
]
RETIRED_CONFIGS = [
    ".config/alacritty/alacritty.toml", ".config/k9s/config.yml",
    ".config/k9s/monokai.yaml", ".config/pypoetry/config.toml",
    ".warp/themes/catppuccin.yaml",
    ".gemini/settings.json", ".gemini/GEMINI.md", ".config/opencode/opencode.json",
    ".config/opencode/.gitignore", ".config/opencode/plugin/notification.ts",
    ".config/opencode/providers/.keep",
]


class BaseSettingsTest(unittest.TestCase):
    def setUp(self) -> None:
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

    def cm(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
        p = subprocess.run(self.base + list(args), env=self.env,
                           capture_output=True, text=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stderr)
        return p

    def test_base_and_selected_modules(self) -> None:
        paths = self.cm("managed").stdout.splitlines()
        for path in [".bashrc", ".bash_profile", ".zshrc", ".gitconfig", ".tmux.conf"]:
            self.assertIn(path, paths)
        for path in [".local/bin/add_iso_prefixes.sh", ".local/bin/open_github.sh"]:
            self.assertIn(path, paths)
        for path in APP_CONFIGS:
            self.assertIn(path, paths)
        for path in [".local/bin/reclaim_docker_space.sh", ".local/bin/wsp-toggle", ".config/dictation"]:
            self.assertNotIn(path, paths)
        for path in [".config/systemd", ".gemini", ".config/opencode", ".config/keyboard-remapping"]:
            self.assertNotIn(path, paths)
        self.config.write_text('[data]\nemail = "test@example.com"\n'
                               'modules = ["fonts"]\n')
        paths = self.cm("managed").stdout.splitlines()
        self.assertIn(".config/ghostty/config", paths)
        self.assertIn(".codex/config.toml", paths)
        self.assertIn(".claude/settings.json", paths)
        self.assertIn(".config/fontconfig/conf.d/60-dotfiles-fonts.conf", paths)
        self.assertNotIn(".config/cosmic", paths)

    def test_macos_excludes_linux_policy(self) -> None:
        self.config.write_text('[data]\nmodules = ["memory-protection", "dictation"]\n'
                               '[data.chezmoi]\nos = "darwin"\n')
        paths = self.cm("managed").stdout.splitlines()
        self.assertIn(".bashrc", paths)
        for path in APP_CONFIGS:
            self.assertIn(path, paths)
        self.assertFalse(any(path.startswith(".config/systemd") for path in paths))
        self.assertNotIn(".local/bin/wsp-toggle", paths)
        self.assertNotIn(".config/dictation", paths)

    def test_retired_configs_removed_without_other_app_files(self) -> None:
        # Stale module selections must not keep retired configs alive.
        self.config.write_text('[data]\nemail = "test@example.com"\n'
                               'modules = ["warp", "alacritty", "k9s", "poetry", "gemini", "opencode"]\n')
        targets = [self.home / path for path in RETIRED_CONFIGS]
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("old managed config\n")
            (target.parent / "keep-local").write_text("local app state\n")
        self.cm("apply", "--force", "--exclude=scripts", *(str(path) for path in targets))
        for target in targets:
            self.assertFalse(target.exists())
            self.assertEqual((target.parent / "keep-local").read_text(), "local app state\n")

    def test_dictation_is_independent(self) -> None:
        self.config.write_text('[data]\nmodules = ["dictation"]\n')
        paths = self.cm("managed").stdout.splitlines()
        self.assertIn(".local/bin/wsp-toggle", paths)
        self.assertIn(".config/dictation/wsp.py", paths)
        self.assertNotIn(".config/cosmic", paths)
        rendered = self.cm("cat", str(self.home / ".config/dictation/config.json")).stdout
        self.assertIn('"medium-streaming"', rendered)

    def test_memory_limits_are_explicit(self) -> None:
        self.config.write_text('[data]\nmodules = ["memory-protection"]\n')
        target = str(self.home / ".config/systemd/user/tmux-spawn-.scope.d/50-oom-protection.conf")
        p = self.cm("cat", target, ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.config.write_text('[data]\nemail = "test@example.com"\nmodules = ["memory-protection"]\n'
                               '[data.tmuxMemory]\nhigh = "6G"\nmax = "8G"\nswap = "2G"\n')
        rendered = self.cm("cat", target).stdout
        for expected in ["MemoryHigh=6G", "MemoryMax=8G", "MemorySwapMax=2G"]:
            self.assertIn(expected, rendered)
        policy = ".config/systemd/user.conf.d/10-oom-policy.conf"
        self.assertIn(policy, self.cm("managed").stdout.splitlines())
        self.assertIn("DefaultOOMPolicy=continue", self.cm("cat", str(self.home / policy)).stdout)
        # Reinitialization must retain the machine's explicit limits.
        self.cm("init", "--no-tty")
        self.assertIn('"memory-protection"', self.config.read_text())
        self.assertEqual(self.cm("cat", target).stdout, rendered)

    def test_linux_keyboard_remapping_is_independent(self) -> None:
        self.config.write_text('[data]\nmodules = ["keyboard-remapping"]\n'
                               '[data.chezmoi]\nos = "linux"\n')
        rule = ".config/keyboard-remapping/linux/90-builtin-keyboard.hwdb"
        paths = self.cm("managed").stdout.splitlines()
        self.assertIn(rule, paths)
        self.assertNotIn(".config/cosmic", paths)
        self.assertNotIn(".config/keyboard-remapping/darwin", paths)
        rendered = self.cm("cat", str(self.home / rule)).stdout
        self.assertIn("pnLaptop13Pro_IntelCoreUltraSeries3_", rendered)
        for mapping in ["b8=esc", "3a=leftctrl", "1d=volumedown", "01=capslock", "36=rightalt"]:
            self.assertIn("KEYBOARD_KEY_" + mapping, rendered)
        script = self.cm("cat", str(self.home / "keyboard_remapping_linux.sh")).stdout
        p = subprocess.run(["sh", "-n"], input=script, text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('source_file="$HOME/' + rule + '"', script)
        self.assertIn("target=/etc/udev/hwdb.d/90-builtin-keyboard.hwdb", script)
        old = self.home / ".config/builtin-keyboard/90-builtin-keyboard.hwdb"
        old.parent.mkdir(parents=True)
        old.write_text(rendered)
        (old.parent / "keep-local").write_text("local state")
        self.cm("apply", "--exclude=scripts", "--parent-dirs", str(old), str(self.home / rule))
        self.assertFalse(old.exists())
        self.assertEqual((self.home / rule).read_text(), rendered)
        self.assertTrue((old.parent / "keep-local").exists())

    def test_desktop_and_remapping_platform_boundaries(self) -> None:
        for operating_system in ["linux", "darwin"]:
            for modules in [[], ["keyboard-remapping"], ["de-macos"], ["de-cosmic"],
                            ["de-cosmic", "de-macos", "keyboard-remapping"]]:
                with self.subTest(os=operating_system, modules=modules):
                    self.config.write_text('[data]\nmodules = ' + json.dumps(modules) + '\n'
                                           '[data.chezmoi]\nos = "' + operating_system + '"\n')
                    paths = self.cm("managed").stdout.splitlines()
                    self.assertEqual(".config/cosmic" in paths,
                                     operating_system == "linux" and "de-cosmic" in modules)
                    self.assertEqual(".config/keyboard-remapping" in paths,
                                     operating_system == "linux" and "keyboard-remapping" in modules)
                    for filename, expected in [
                        ("run_once_mac_keyboard_shortcuts.sh.tmpl",
                         operating_system == "darwin" and "de-macos" in modules),
                        ("run_once_after_keyboard_remapping_linux.sh.tmpl",
                         operating_system == "linux" and "keyboard-remapping" in modules),
                    ]:
                        script = self.cm("execute-template", "--file", str(ROOT / filename)).stdout
                        self.assertEqual(bool(script.strip()), expected)
                        if expected:
                            p = subprocess.run(["bash", "-n"], input=script, text=True, capture_output=True)
                            self.assertEqual(p.returncode, 0, p.stderr)

    def test_init_preserves_module_selection(self) -> None:
        self.cm("init", "--promptDefaults")
        self.config.write_text('[data]\nemail = "test@example.com"\nmodules = ["fonts"]\n')
        self.cm("init", "--no-tty")
        self.assertIn('"fonts"', self.config.read_text())

    def test_aliases_and_trash_on_available_shells(self) -> None:
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
