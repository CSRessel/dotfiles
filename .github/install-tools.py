"""Install checksum-pinned CI binaries into an explicit directory (Linux x86_64)."""

import argparse
import hashlib
import io
import json
import platform
import tarfile
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("tools", nargs="+")
    args = parser.parse_args()
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        parser.error("the pinned release archives target Linux x86_64")
    manifest = json.loads(Path(__file__).with_name("tools.json").read_text())
    args.directory.mkdir(parents=True, exist_ok=True)
    for name in args.tools:
        spec = manifest[name]
        with urllib.request.urlopen(spec["url"], timeout=60) as response:
            archive = response.read()
        if hashlib.sha256(archive).hexdigest() != spec["sha256"]:
            raise RuntimeError(f"{name}: release checksum mismatch")
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
            member = bundle.getmember(spec["member"])
            if not member.isfile():
                raise RuntimeError(f"{name}: expected a regular executable")
            executable = bundle.extractfile(member)
            if executable is None:
                raise RuntimeError(f"{name}: executable missing from release")
            target = args.directory / name
            target.write_bytes(executable.read())
            target.chmod(0o755)
        print(f"Installed {name}: checksum verified")


if __name__ == "__main__":
    main()
