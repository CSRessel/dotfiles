#!/bin/bash

target_dir="${1:-.}"

if [ ! -d "$target_dir" ]; then
  echo "Directory $target_dir does not exist."
  exit 1
fi

for file in "$target_dir"/*; do
  if [ -f "$file" ]; then
    creation_date=$(stat -c %w "$file" | cut -d ' ' -f 1)
    if [ "$creation_date" = "-" ]; then
      creation_date=$(stat -c %y "$file" | cut -d ' ' -f 1)
    fi

    if [ ${#creation_date} -eq 10 ]; then
      base_name=$(basename "$file")
      if [[ ! "$base_name" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
        mv "$file" "$target_dir/${creation_date}_$base_name"
      fi
    fi
  fi
done
