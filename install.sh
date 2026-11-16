#!/bin/sh
# File: install.sh
# Purpose: install the build-tools skill into Claude Code's skills folder.
# Kid note: this copies the instruction files into the place where Claude looks for skills.
set -eu

REPO="https://raw.githubusercontent.com/lionlaith7/Claude--Root-Module-Builder/main"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/build-tools"
FILES="SKILL.md README.md README.txt AI.md"

mkdir -p "$DEST"
for f in $FILES; do
    curl -fsSL "$REPO/$f" -o "$DEST/$f"
done
echo "OK: build-tools installed to $DEST"
echo "Restart Claude Code, then ask it to build a tool."
