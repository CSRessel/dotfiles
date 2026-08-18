from __future__ import annotations

from typing import Any
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CodexConfigMergeTest(unittest.TestCase):
    maxDiff = None

    def chezmoi_binary(self) -> str:
        chezmoi = shutil.which("chezmoi")
        self.assertIsNotNone(chezmoi)
        return str(chezmoi)

    def parse_toml(self, source: str) -> dict[str, Any]:
        result = subprocess.run(
            [
                self.chezmoi_binary(),
                "--source",
                str(REPOSITORY_ROOT),
                "execute-template",
                "--with-stdin",
                "{{ .chezmoi.stdin | fromToml | toJson }}",
            ],
            input=source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def run_merge_result(
        self, source: str, operating_system: str, home: str
    ) -> tuple[subprocess.CompletedProcess[str], str]:
        environment = os.environ.copy()
        environment["CHEZMOI_CODEX_CONFIG_OS"] = operating_system
        environment["HOME"] = home
        with tempfile.TemporaryDirectory(prefix="codex-config-merge-") as destination:
            destination_path = Path(destination)
            config_path = destination_path / ".codex" / "config.toml"
            config_path.parent.mkdir(parents=True)
            config_path.write_text(source)
            result = subprocess.run(
                [
                    self.chezmoi_binary(),
                    "--source",
                    str(REPOSITORY_ROOT),
                    "--destination",
                    destination,
                    "--persistent-state",
                    str(destination_path / "chezmoistate.boltdb"),
                    "apply",
                    "--force",
                    str(config_path),
                ],
                text=True,
                capture_output=True,
                env=environment,
                check=False,
            )
            output = config_path.read_text()
        return result, output

    def run_merge(self, source: str, operating_system: str, home: str) -> str:
        result, output = self.run_merge_result(source, operating_system, home)
        self.assertEqual(result.returncode, 0, result.stderr)
        return output

    def test_repository_tests_are_not_managed_dotfiles(self) -> None:
        result = subprocess.run(
            [
                self.chezmoi_binary(),
                "--source",
                str(REPOSITORY_ROOT),
                "managed",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        managed_tests = [
            path
            for path in result.stdout.splitlines()
            if path == "tests" or path.startswith("tests/")
        ]
        self.assertEqual(managed_tests, [])

    def test_linux_enforces_defaults_and_sccache_while_preserving_app_state(
        self,
    ) -> None:
        source = """
personality = "friendly"
model = "gpt-5.6-sol"
model_reasoning_effort = "xhigh"
approvals_reviewer = "user"
approval_policy = "never"
sandbox_mode = "danger-full-access"
default_permissions = "wrong-profile"
service_tier = "fast"

[permissions.sccache-workspace]
description = "wrong description"
extends = ":read-only"

[permissions.sccache-workspace.filesystem]
"/wrong/cache" = "write"

[permissions.sccache-workspace.network]
enabled = false

[features]
future_feature = true

[plugins."browser@openai-bundled"]
enabled = false

[plugins."future@openai-bundled"]
enabled = true

[marketplaces.openai-bundled]
last_updated = "volatile-timestamp"
source = "/runtime/marketplace"

[mcp_servers.node_repl]
command = "/runtime/node_repl"

[mcp_servers.node_repl.env]
NODE_REPL_TRUSTED_BROWSER_CLIENT_SHA256S = "volatile-hash"

[desktop]
future_setting = "preserve-me"

[projects."/home/tester/source/project"]
trust_level = "trusted"
""".lstrip()

        output = self.run_merge(source, "linux", "/home/tester")
        config = self.parse_toml(output)

        self.assertEqual(
            {
                "personality": config["personality"],
                "model_reasoning_effort": config["model_reasoning_effort"],
                "approvals_reviewer": config["approvals_reviewer"],
                "approval_policy": config["approval_policy"],
                "service_tier": config["service_tier"],
            },
            {
                "personality": "pragmatic",
                "model_reasoning_effort": "medium",
                "approvals_reviewer": "auto_review",
                "approval_policy": "on-request",
                "service_tier": "default",
            },
        )
        self.assertEqual(config["model"], "gpt-5.6-sol")
        self.assertNotIn("sandbox_mode", config)
        self.assertEqual(config["default_permissions"], "sccache-workspace")
        self.assertEqual(
            config["permissions"]["sccache-workspace"],
            {
                "description": "Workspace access with a shared sccache artifact cache.",
                "extends": ":workspace",
                "filesystem": {"/home/tester/.cache/sccache": "write"},
                "network": {"enabled": True},
            },
        )
        self.assertTrue(config["plugins"]["browser@openai-bundled"]["enabled"])
        self.assertTrue(config["plugins"]["future@openai-bundled"]["enabled"])
        self.assertTrue(config["features"]["future_feature"])
        self.assertEqual(
            config["marketplaces"]["openai-bundled"],
            {"last_updated": "volatile-timestamp", "source": "/runtime/marketplace"},
        )
        self.assertEqual(
            config["mcp_servers"]["node_repl"]["command"], "/runtime/node_repl"
        )
        self.assertEqual(
            config["mcp_servers"]["node_repl"]["env"][
                "NODE_REPL_TRUSTED_BROWSER_CLIENT_SHA256S"
            ],
            "volatile-hash",
        )
        self.assertEqual(config["desktop"]["future_setting"], "preserve-me")
        self.assertEqual(
            config["projects"],
            {"/home/tester/source/project": {"trust_level": "trusted"}},
        )
        table_headers = [line for line in output.splitlines() if line.startswith("[")]
        self.assertEqual(
            table_headers[-2:],
            ["[projects]", "[projects.'/home/tester/source/project']"],
        )

    def test_macos_enforces_workspace_and_computer_use_while_preserving_app_state(
        self,
    ) -> None:
        source = """
personality = "friendly"
model_reasoning_effort = "xhigh"
approvals_reviewer = "user"
approval_policy = "never"
default_permissions = "sccache-workspace"
sandbox_mode = "danger-full-access"
service_tier = "fast"
notify = ["wrong-notifier", "wrong-event"]

[permissions.sccache-workspace]
description = "Linux-only profile"
extends = ":workspace"

[permissions.sccache-workspace.filesystem]
"/home/tester/.cache/sccache" = "write"

[permissions.sccache-workspace.network]
enabled = true

[permissions.review-only]
extends = ":read-only"

[permissions.review-only.network]
enabled = false

[plugins."computer-use@openai-bundled"]
enabled = false

[plugins."future@openai-bundled"]
enabled = true

[marketplaces.openai-bundled]
last_updated = "volatile-timestamp"

[mcp_servers.node_repl]
command = "/Applications/Codex.app/runtime/node_repl"

[mcp_servers.node_repl.env]
BROWSER_USE_CODEX_APP_VERSION = "volatile-version"

[mcp_servers.computer-use]
command = "wrong-command"
args = ["wrong-argument"]
cwd = "/wrong/directory"
enabled = true

[desktop]
future_setting = "preserve-me"
keepRemoteControlAwakeWhilePluggedIn = false
followUpQueueMode = "interrupt"
dock-icon-preference = "wrong-icon"

[desktop.open-in-target-preferences]
global = "zed"

[desktop.open-in-target-preferences.perPath]
"/Users/tester/source/project" = "zed"

[projects."/Users/tester/source/project"]
trust_level = "trusted"
""".lstrip()

        output = self.run_merge(source, "darwin", "/Users/tester")
        config = self.parse_toml(output)

        self.assertEqual(config["personality"], "pragmatic")
        self.assertEqual(config["model_reasoning_effort"], "medium")
        self.assertEqual(config["approvals_reviewer"], "auto_review")
        self.assertEqual(config["approval_policy"], "on-request")
        self.assertEqual(config["service_tier"], "default")
        self.assertEqual(config["sandbox_mode"], "workspace-write")
        self.assertNotIn("default_permissions", config)
        self.assertEqual(
            config["permissions"],
            {
                "review-only": {
                    "extends": ":read-only",
                    "network": {"enabled": False},
                }
            },
        )
        self.assertEqual(
            config["notify"],
            [
                "/Users/tester/.codex/computer-use/Codex Computer Use.app/Contents/SharedSupport/"
                "SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient",
                "turn-ended",
            ],
        )
        self.assertTrue(config["plugins"]["computer-use@openai-bundled"]["enabled"])
        self.assertTrue(config["plugins"]["future@openai-bundled"]["enabled"])
        self.assertEqual(
            config["marketplaces"]["openai-bundled"],
            {"last_updated": "volatile-timestamp"},
        )
        self.assertEqual(
            config["mcp_servers"]["computer-use"],
            {
                "command": "./Codex Computer Use.app/Contents/SharedSupport/"
                "SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient",
                "args": ["mcp"],
                "cwd": ".",
                "enabled": False,
            },
        )
        self.assertEqual(
            config["mcp_servers"]["node_repl"]["command"],
            "/Applications/Codex.app/runtime/node_repl",
        )
        self.assertEqual(
            config["mcp_servers"]["node_repl"]["env"]["BROWSER_USE_CODEX_APP_VERSION"],
            "volatile-version",
        )
        self.assertEqual(config["desktop"]["future_setting"], "preserve-me")
        self.assertTrue(config["desktop"]["keepRemoteControlAwakeWhilePluggedIn"])
        self.assertEqual(config["desktop"]["followUpQueueMode"], "queue")
        self.assertEqual(config["desktop"]["dock-icon-preference"], "codex-system")
        self.assertEqual(
            config["desktop"]["open-in-target-preferences"]["global"], "ghostty"
        )
        self.assertEqual(
            config["desktop"]["open-in-target-preferences"]["perPath"],
            {"/Users/tester/source/project": "zed"},
        )
        self.assertEqual(
            config["projects"],
            {"/Users/tester/source/project": {"trust_level": "trusted"}},
        )

    def test_merge_is_idempotent_on_linux_and_macos(self) -> None:
        source = """
model = "gpt-5.6-sol"

[projects."/home/tester/source/project"]
trust_level = "trusted"
""".lstrip()

        for operating_system, home in (
            ("linux", "/home/tester"),
            ("darwin", "/Users/tester"),
        ):
            with self.subTest(operating_system=operating_system):
                first_output = self.run_merge(source, operating_system, home)
                second_output = self.run_merge(first_output, operating_system, home)

                self.assertEqual(second_output, first_output)

    def test_chezmoi_apply_preserves_unmanaged_projects(self) -> None:
        source = """
model = "gpt-5.6-sol"

[projects."/home/tester/source/project"]
trust_level = "trusted"
""".lstrip()
        output = self.run_merge(source, "linux", "/home/tester")
        config = self.parse_toml(output)

        self.assertEqual(config["personality"], "pragmatic")
        self.assertEqual(
            config["projects"],
            {"/home/tester/source/project": {"trust_level": "trusted"}},
        )

    def test_invalid_toml_fails_without_overwriting_the_destination(self) -> None:
        source = "[projects\n"

        result, output = self.run_merge_result(source, "linux", "/home/tester")

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(result.stderr)
        self.assertEqual(output, source)

    def test_multiline_notify_is_replaced_without_orphaned_values(self) -> None:
        source = """
notify = [
  "wrong-notifier",
  "wrong-event",
]
""".lstrip()

        output = self.run_merge(source, "darwin", "/Users/tester")
        config = self.parse_toml(output)

        self.assertEqual(
            config["notify"],
            [
                "/Users/tester/.codex/computer-use/Codex Computer Use.app/Contents/SharedSupport/"
                "SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient",
                "turn-ended",
            ],
        )

    def test_unmanaged_multiline_string_with_table_like_text_is_preserved(self) -> None:
        source = '''

[auto_review]
policy = """
[not-a-table]
Preserve this policy exactly.
"""
'''.lstrip()

        output = self.run_merge(source, "linux", "/home/tester")
        config = self.parse_toml(output)

        self.assertEqual(
            config["auto_review"]["policy"],
            "[not-a-table]\nPreserve this policy exactly.\n",
        )


if __name__ == "__main__":
    unittest.main()
