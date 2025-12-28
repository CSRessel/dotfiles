#!/bin/bash

# --- Configuration ---

# 1. Set the path to the Python script
PYTHON_SCRIPT="update_zen_prefs.py"

# 2. Set the zen root path
if [ ! -d "$ZEN_ROOT" ]; then
    # Fallback to the path provided in prompt if standard fails
    ZEN_ROOT="$HOME/.var/app/app.zen_browser.zen/.zen" 
fi
if [ ! -d "$ZEN_ROOT" ]; then
    echo "Zen Flatpak directory not found. Skipping configuration."
    exit 0
fi

# 3. Find the most recently modified profile folder
ZEN_PROFILE_DIR=$(find "$ZEN_ROOT" -mindepth 2 -maxdepth 2 -name "prefs.js" -printf '%T@ %h\n' | sort -n | tail -1 | cut -d' ' -f2-)

# Or explicitly set the path.
# This is usually in ~/.zen/<random_string>.Default (Linux/Mac).
# MODIFY THIS LINE TO MATCH YOUR ACTUAL PATH:
# ZEN_PROFILE_DIR="$HOME/.zen/YOUR_PROFILE_ID.default" 

# --- Verification ---

# Check if Python is installed
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Error: Python 3 is not installed."
    exit 1
fi

# Check if the Zen Profile directory exists
if [ ! -d "$ZEN_PROFILE_DIR" ]; then
    echo "❌ Error: The Zen Profile directory was not found at:"
    echo "   $ZEN_PROFILE_DIR"
    echo "   Please edit 'run_update.sh' and set the correct ZEN_PROFILE_DIR."
    exit 1
fi

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: Could not find '$PYTHON_SCRIPT' in the current directory."
    exit 1
fi

# --- Execution ---

echo "🚀 Starting Update..."
echo "   Script:  $PYTHON_SCRIPT"
echo "   Profile: $ZEN_PROFILE_DIR"

# Call the python script and pass the profile path as the first argument
$PYTHON_CMD "$PYTHON_SCRIPT" "$ZEN_PROFILE_DIR"

# Check exit status
if [ $? -eq 0 ]; then
    echo "✨ All operations completed successfully."
else
    echo "⚠️  The script exited with an error."
    exit 1
fi
