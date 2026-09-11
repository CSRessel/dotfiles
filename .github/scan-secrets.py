"""Run Gitleaks without printing matches, values, URLs, or report artifacts."""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def private_filename(filename):
    # Recognize both home paths and chezmoi's source-name attributes.
    parts = []
    for part in PurePosixPath(filename).parts:
        part = re.sub(r"^(?:(?:private|encrypted|executable|readonly)_)+", "", part)
        if part.startswith("dot_"):
            part = "." + part[4:]
        parts.append(part.lower())
    path = "/".join(parts)
    name = parts[-1]
    if name.endswith((".example", ".sample", ".tmpl")):
        return False  # Content is still scanned by Gitleaks.
    return (
        name == ".env"
        or name.startswith(".env.")
        or name in {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", "auth.json", ".claude.json"}
        or name.endswith((".key", ".pem", ".p12", ".pfx", ".kdbx"))
        or path.endswith(
            (".aws/credentials", "gcloud/application_default_credentials.json", "sops/age/keys.txt")
        )
    )


def scan(mode):
    binary = shutil.which("gitleaks")
    if binary is None:
        print("Gitleaks is required; install the pre-commit environment or the pinned CI binary.")
        return 2
    if mode == "staged":
        names_command = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]
        arguments = ["git", "--pre-commit", "--staged"]
    elif mode == "recent":
        names_command = None
        arguments = ["git", "--log-opts=--all --since=1.year.ago"]
    else:
        names_command = ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
        arguments = ["dir"]
    blocked = []
    if names_command:
        names = subprocess.check_output(names_command).decode("utf-8", errors="replace").split("\0")
        blocked = [name for name in names if name and private_filename(name)]
    with tempfile.TemporaryDirectory(prefix="dotfiles-secret-scan-") as directory:
        report = Path(directory) / "report.json"
        command = [
            binary,
            *arguments,
            "--config",
            str(ROOT / ".gitleaks.toml"),
            "--redact",
            "--ignore-gitleaks-allow",
            "--no-banner",
            "--report-format=json",
            "--report-path",
            str(report),
            ".",
        ]
        try:
            result = subprocess.run(command, capture_output=True, timeout=180)
        except subprocess.TimeoutExpired:
            print("Secret scan timed out; commit blocked.")
            return 2
        # Never forward scanner output: even surrounding text can be private.
        if result.returncode not in (0, 1):
            print(f"Gitleaks could not complete (exit {result.returncode}); commit blocked.")
            return 2
        if result.returncode == 1 and not report.exists():
            print("Gitleaks did not produce a valid report; commit blocked.")
            return 2
        findings = json.loads(report.read_text()) if report.exists() else []
        for filename in sorted(set(blocked)):
            print(f"{json.dumps(filename)}: sensitive filename; keep credentials outside this repo")
        for hit in findings:
            print(f"{json.dumps(hit['File'])}:{hit['StartLine']}: {hit['RuleID']} (value withheld)")
        if findings or blocked or result.returncode:
            print("Review the flagged files locally. No values or report artifacts were printed.")
            return 1
    print(f"Secret/private-config scan passed ({mode}).")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["staged", "recent", "files"])
    sys.exit(scan(parser.parse_args().mode))
