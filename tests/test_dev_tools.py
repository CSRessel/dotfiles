"""Check optional tool paths and Nix precedence without modifying the real home."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DevToolsTest(unittest.TestCase):
    def test_module_and_shell_rendering(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config = home / 'config.toml'
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith(('XDG_', 'CHEZMOI_'))}
            env['HOME'] = directory
            base = [shutil.which('chezmoi'), '--source', str(ROOT),
                    '--destination', directory, '--config', str(config),
                    '--persistent-state', str(home / 'state.db')]
            for enabled in [False, True]:
                config.write_text('[data]\nemail="test@example.com"\nmodules=' +
                                  ('["dev-tools"]' if enabled else '[]') + '\n')
                paths = subprocess.check_output(base + ['managed'], env=env, text=True)
                self.assertEqual('.config/mise/config.toml' in paths, enabled)
                self.assertEqual('.config/dev-tools/env.sh' in paths, enabled)
                for name, shell in [('.bashrc', 'bash'), ('.zshrc', 'zsh')]:
                    rendered = subprocess.check_output(base + ['cat', str(home / name)], env=env, text=True)
                    self.assertEqual('.config/dev-tools/env.sh' in rendered, enabled)
                    if shutil.which(shell):
                        subprocess.run([shell, '-n'], input=rendered, text=True, check=True)

    def test_paths_are_idempotent_and_preserve_nix(self):
        for shell in ['bash', 'zsh']:
            if not shutil.which(shell):
                continue
            for nix in [False, True]:
                env = dict(os.environ, HOME='/tmp/dev-tools-test', PATH='/nix/test/bin:/usr/bin:/bin')
                for key in ['MISE_DATA_DIR', 'XDG_DATA_HOME', 'CARGO_HOME', 'IN_NIX_SHELL']:
                    env.pop(key, None)
                if nix:
                    env['IN_NIX_SHELL'] = 'impure'
                result = subprocess.check_output(
                    [shutil.which(shell), '-fc', '. "$1"; . "$1"; printf "%s" "$PATH"',
                     'test', str(ROOT / 'dot_config/dev-tools/env.sh')], env=env, text=True)
                paths = result.split(':')
                self.assertEqual(len(paths), len(set(paths)))
                shims = '/tmp/dev-tools-test/.local/share/mise/shims'
                self.assertIn(shims, paths)
                if nix:
                    self.assertEqual(paths[0], '/nix/test/bin')
                else:
                    self.assertEqual(paths[0], shims)


if __name__ == '__main__':
    unittest.main()
