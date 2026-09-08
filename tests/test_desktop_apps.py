"""Default associations without changing the user's desktop."""
import configparser
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DesktopAppsTest(unittest.TestCase):
    def test_merge_availability_and_repeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            apps = root / 'data/applications'
            apps.mkdir(parents=True)
            (root / 'data/mime').mkdir()
            (root / 'data/mime/types').write_text('video/webm\naudio/flac\nimage/png\n')
            env = dict(os.environ, HOME=tmp, XDG_DATA_HOME=str(root / 'data'), XDG_DATA_DIRS=str(root / 'empty'))
            def merge(value):
                return subprocess.check_output(['python3', str(ROOT / 'dot_config/modify_mimeapps.list')], input=value, text=True, env=env)
            original = '[Default Applications]\ntext/html=old.desktop;\nx-scheme-handler/codex=chatgpt.desktop;\nimage/png=viewer.desktop;\n[Added Associations]\ntext/plain=other.desktop;\n'
            self.assertEqual(merge(original), original)
            for name in ['firefox.desktop', 'org.videolan.VLC.desktop', 'dev.zed.Zed.desktop']:
                (apps / name).write_text('[Desktop Entry]\nType=Application\nName=Test\nExec=true\n')
            result = merge(original)
            parsed = configparser.ConfigParser(interpolation=None)
            parsed.read_string(result)
            defaults = parsed['Default Applications']
            self.assertEqual(defaults['text/html'], 'firefox.desktop;')
            self.assertEqual(defaults['text/plain'], 'dev.zed.Zed.desktop;')
            self.assertEqual(defaults['video/mp4'], 'org.videolan.VLC.desktop;')
            self.assertEqual(defaults['x-scheme-handler/codex'], 'chatgpt.desktop;')
            self.assertEqual(defaults['image/png'], 'viewer.desktop;')
            self.assertEqual(parsed['Added Associations']['text/plain'], 'other.desktop;')
            self.assertEqual(merge(result), result)


if __name__ == '__main__':
    unittest.main()
