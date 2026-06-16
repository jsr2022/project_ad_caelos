#!/bin/bash

# This script is used to clear the __pycache__ directories in the project. It finds all __pycache__ directories and removes them.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBMODULE_DIR="$SCRIPT_DIR/adcaelos"
TARGET_DIR="__pycache__"

echo "clearing __pycache__ in adcaelos repository."
top_level_pycache="$SCRIPT_DIR/$TARGET_DIR"



if [ -d "$top_level_pycache" ]; then
    echo "Removing top-level __pycache__ directory: $top_level_pycache"
    rm -rf "$top_level_pycache"
fi

find "$SUBMODULE_DIR" -type d -name "$TARGET_DIR" | while read -r dir; do
    echo "Removing __pycache__ directory: $dir"
    rm -rf "$dir"
done