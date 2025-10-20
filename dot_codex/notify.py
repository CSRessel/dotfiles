import json
import subprocess
import sys


def main() -> int:
    """
    And in your ~/.codex/config.toml

    notify = ["python3", "/home/clifford/.codex/notify.py"]
    model = "gpt-5-codex"
    model_reasoning_effort = "medium"
    """
    if len(sys.argv) != 2:
        print("Usage: notify.py <NOTIFICATION_JSON>")
        return 1

    try:
        notification = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        return 1

    match notification_type := notification.get("type"):
        case "agent-turn-complete":
            assistant_message = notification.get("last-assistant-message")
            if assistant_message:
                title = f"Codex: {assistant_message}"
            else:
                title = "Codex: Turn Complete!"
            input_messages = notification.get("input_messages", [])
            message = " ".join(input_messages)
            title += message
        case _:
            print(f"not sending a push notification for: {notification_type}")
            return 0

    subprocess.check_output(
        [
            "notify-send",
            "-a",
            "codex",
            "-u",
            "normal",
            "-t",
            "5",
            title,
            message,
        ]
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
