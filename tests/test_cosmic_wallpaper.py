"""Exercise wallpaper generation through chezmoi in disposable homes."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CosmicWallpaperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="cosmic wallpaper'-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.source = self.home / "source"
        self.source.mkdir()
        for name in (".chezmoidata.json", ".chezmoiignore",
                     "run_before_cosmic_wallpaper.sh.tmpl"):
            shutil.copy2(ROOT / name, self.source / name)
        for name in (".chezmoitemplates", "docs/assets/cosmic",
                     "dot_config/cosmic/com.system76.CosmicBackground"):
            shutil.copytree(ROOT / name, self.source / name)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("XDG_", "CHEZMOI_"))}
        self.env["HOME"] = str(self.home)
        self.config = self.home / "chezmoi.toml"
        self.config.write_text('[data]\nmodules = ["cosmic"]\n')
        self.hostname = "shelyn"
        self.os = "linux"

    def cm(self, *args: str) -> subprocess.CompletedProcess[str]:
        data = self.config.read_text()
        config = self.home / "runtime.json"
        values = tomllib.loads(data)
        values["data"]["email"] = "test@example.com"
        values["data"]["chezmoi"] = {"hostname": self.hostname, "os": self.os}
        config.write_text(json.dumps(values))
        return subprocess.run(
            [shutil.which("chezmoi") or "chezmoi", "--source", str(self.source),
             "--destination", str(self.home), "--config", str(config),
             "--persistent-state", str(self.home / "state.db"),
             *args],
            env=self.env, capture_output=True, text=True)

    def apply_wallpaper(self) -> Path:
        target = self.home / ".config/cosmic/com.system76.CosmicBackground/v1/all"
        result = self.cm("apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        match = re.search(r'source: Path\("([^"\n]+)"\)', target.read_text())
        self.assertIsNotNone(match)
        assert match is not None
        output = Path(match[1])
        self.assertTrue(output.is_relative_to(self.home), str(output))
        self.assertTrue(output.is_file())
        return output

    def test_repeat_apply_is_cached_and_deleted_image_recovers(self) -> None:
        output = self.apply_wallpaper()
        content, modified = output.read_bytes(), output.stat().st_mtime_ns
        self.assertEqual(self.apply_wallpaper(), output)
        self.assertEqual(output.stat().st_mtime_ns, modified)
        output.unlink()
        self.assertEqual(self.apply_wallpaper().read_bytes(), content)

    def test_hostname_changes_color_and_preserves_dimensions(self) -> None:
        first = self.apply_wallpaper()
        self.hostname = "desna"
        second = self.apply_wallpaper()
        self.assertNotEqual(first, second)
        self.assertNotEqual(first.read_bytes(), second.read_bytes())
        source = ROOT / "docs/assets/cosmic/phytoplankton_bloom_nasa_oli2_20240121.jpg"
        identify = ["magick", "identify"] if shutil.which("magick") else ["identify"]
        for image in (first, second):
            dimensions = subprocess.check_output(identify + ["-format", "%wx%h", str(image)])
            self.assertEqual(dimensions, subprocess.check_output(
                identify + ["-format", "%wx%h", str(source)]))

    def test_renderer_failure_leaves_config_and_image_unchanged(self) -> None:
        original = self.apply_wallpaper()
        target = self.home / ".config/cosmic/com.system76.CosmicBackground/v1/all"
        original_config = target.read_bytes()
        self.hostname = "failed-render"
        # Inject a failing external executable; exercise real chezmoi error ordering.
        bindir = self.home / "bin"
        bindir.mkdir()
        renderer = bindir / "magick"
        renderer.write_text("#!/bin/sh\nexit 42\n")
        renderer.chmod(0o755)
        self.env["PATH"] = str(bindir) + os.pathsep + self.env["PATH"]
        result = self.cm("apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.read_bytes(), original_config)
        self.assertEqual(list(original.parent.iterdir()), [original])

    def test_disabled_module_and_non_linux_do_not_generate(self) -> None:
        for modules, operating_system in (([], "linux"), (["cosmic"], "darwin")):
            self.config.write_text('[data]\nmodules = ' + json.dumps(modules) + '\n')
            self.os = operating_system
            result = self.cm("apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((self.home / ".config/cosmic").exists())


if __name__ == "__main__":
    unittest.main()
