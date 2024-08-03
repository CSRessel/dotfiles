#!/bin/bash

BACKUP_FILES=(
    "$(pwd)/apt_packages_info.txt"
    "$(pwd)/apt_packages_names_all.txt"
    "$(pwd)/apt_packages_names_user.txt"
    "$(pwd)/flatpak_packages_names.txt"
    "$(pwd)/snap_packages_names.txt"
)

if [[ -n $(git status --porcelain) ]]; then
    echo "Unstaged or uncommitted changes detected. Stashing changes..."
    git stash push -m "Stashing local changes before backup commit"
    STASHED=true
else
    echo "No unstaged or uncommitted changes. No stashing required."
    STASHED=false
fi

for file in "${BACKUP_FILES[@]}"; do
    if [ -f "$file" ]; then
        git add "$file"
    else
        echo "Warning: File not found for staging - $file"
    fi
done

git commit -m "[cron] Add backup files for package lists" -m "User=$(whoami) Host=$(hostname) Date=$(date)"
git push origin main

if [ "$STASHED" = true ]; then
    echo "Restoring stashed changes..."
    git stash pop

    if [ $? -eq 0 ]; then
        echo "Backup commit and push successful. Local changes restored."
    else
        echo "Error: Failed to restore local changes from stash."
    fi
else
    echo "No local changes to restore."
fi
