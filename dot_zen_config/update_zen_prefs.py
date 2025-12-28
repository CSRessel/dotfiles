import json
import os
import sys
import shutil

# --- Configuration ---

# 1. Determine Profile Directory
# If an argument is passed, use it; otherwise default to current directory
if len(sys.argv) > 1:
    PROFILE_DIR = sys.argv[1]
else:
    PROFILE_DIR = "."

# Input: The file with your custom shortcuts (assumed to be in the SAME folder as this script)
# We use os.path.dirname(__file__) to ensure we look where the script is, not where the shell is.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_ZEN_SHORTCUTS = os.path.join(SCRIPT_DIR, "added-zen-keyboard-shortcuts.json")
SOURCE_EXT_SHORTCUTS = os.path.join(SCRIPT_DIR, "added-extension-shortcuts.json")

# Targets:
TARGET_USER_JS = os.path.join(PROFILE_DIR, "prefs.js")
TARGET_ZEN_SHORTCUTS = os.path.join(PROFILE_DIR, "zen-keyboard-shortcuts.json")
TARGET_EXT_SETTINGS = os.path.join(PROFILE_DIR, "extension-settings.json")


def create_backup(file_path):
    """
    Creates a backup of the file at file_path with a .bak extension.
    """
    if os.path.exists(file_path):
        backup_path = f"{file_path}.bak"
        try:
            shutil.copy2(file_path, backup_path)
            print(
                f"📦 Backup: Saved current state to '{os.path.basename(backup_path)}'"
            )
        except IOError as e:
            print(f"⚠️  Warning: Failed to create backup for '{file_path}': {e}")
    else:
        # File doesn't exist yet, so no backup needed
        pass


def load_json_file(filepath):
    """Helper to safely load a JSON file."""
    if not os.path.exists(filepath):
        print(f"Warning: Source file '{filepath}' not found. Skipping update.")
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON in '{filepath}': {e}")
        return None


def update_keyboard_shortcuts():
    """
    Reads SOURCE_ZEN_SHORTCUTS and merges it into TARGET_ZEN_SHORTCUTS.
    """
    new_shortcuts = load_json_file(SOURCE_ZEN_SHORTCUTS)
    if not new_shortcuts:
        print("Skipping Zen Keyboard Shortcuts (Source not found or invalid).")
        return

    current_shortcuts = load_json_file(TARGET_ZEN_SHORTCUTS) or {}

    # Merge logic
    current_shortcuts.update(new_shortcuts)
    create_backup(TARGET_ZEN_SHORTCUTS)
    try:
        with open(TARGET_ZEN_SHORTCUTS, "w", encoding="utf-8") as f:
            json.dump(current_shortcuts, f, indent=2)
        print(f"Shortcuts: Merged into '{TARGET_ZEN_SHORTCUTS}'.")
    except IOError as e:
        print(f"Error writing to '{TARGET_ZEN_SHORTCUTS}': {e}")


def update_extension_settings():
    """
    Merges extension shortcuts into extension-settings.json.

    Expects SOURCE_EXT_SHORTCUTS to look like:
    {
      "commands": {
         "_execute_action": { "precedenceList": [ { "id": "...", "value": { "shortcut": "..." } } ] }
      }
    }
    """
    new_settings = load_json_file(SOURCE_EXT_SHORTCUTS)
    if not new_settings or "commands" not in new_settings:
        print("Skipping Extension Settings (Source not found or invalid structure).")
        return

    current_settings = load_json_file(TARGET_EXT_SETTINGS) or {}

    # Ensure structure exists in target
    if "commands" not in current_settings:
        current_settings["commands"] = {}

    # Iterate through the new commands map
    for cmd_key, cmd_data in new_settings["commands"].items():

        # If the command key (e.g., "_execute_action") doesn't exist in target, add it entirely
        if cmd_key not in current_settings["commands"]:
            current_settings["commands"][cmd_key] = cmd_data
            continue

        # If it exists, we must merge the "precedenceList"
        target_prec_list = current_settings["commands"][cmd_key].get(
            "precedenceList", []
        )
        new_prec_list = cmd_data.get("precedenceList", [])

        for new_item in new_prec_list:
            new_id = new_item.get("id")

            # Find if this extension ID already has an entry in the target list
            found = False
            for i, target_item in enumerate(target_prec_list):
                if target_item.get("id") == new_id:
                    # Update existing entry with new values (shortcut, enabled status, etc.)
                    # We merge keys to preserve things like installDate if missing in source
                    target_item.update(new_item)
                    target_prec_list[i] = target_item
                    found = True
                    break

            # If not found, append the new item
            if not found:
                target_prec_list.append(new_item)

        # Save the updated list back to the structure
        current_settings["commands"][cmd_key]["precedenceList"] = target_prec_list

    create_backup(TARGET_EXT_SETTINGS)
    try:
        with open(TARGET_EXT_SETTINGS, "w", encoding="utf-8") as f:
            # Firefox prefs are usually compact, but indent=2 is safer for manual reading later
            json.dump(current_settings, f, indent=2)
        print(f"Ext Settings: Updated '{os.path.basename(TARGET_EXT_SETTINGS)}'.")
    except IOError as e:
        print(f"Error writing Extension Settings: {e}")


def update_user_js_prefs():
    """
    Updates specific preferences in user.js.
    """
    if not os.path.exists(TARGET_USER_JS):
        print(f"Error: '{TARGET_USER_JS}' not found.")
        return

    with open(TARGET_USER_JS, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    updated_pref = False

    for line in lines:
        if '"browser.tabs.insertAfterCurrent"' in line:
            new_lines.append('user_pref("browser.tabs.insertAfterCurrent", true);\n')
            updated_pref = True
            continue
        new_lines.append(line)

    if not updated_pref:
        new_lines.append('user_pref("browser.tabs.insertAfterCurrent", true);\n')
    print(
        f"Preferences: Updated 'browser.tabs.insertAfterCurrent' in '{TARGET_USER_JS}'."
    )

    create_backup(TARGET_USER_JS)
    with open(TARGET_USER_JS, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def main():
    print(f"--- Updating Zen Profile: {PROFILE_DIR} ---")
    print("... Updating keyboard shortcuts")
    update_keyboard_shortcuts()
    print("... Updating extension shortcuts")
    update_extension_settings()
    print("... Updating user prefs")
    update_user_js_prefs()
    print("--- Update Complete ---")


if __name__ == "__main__":
    main()
