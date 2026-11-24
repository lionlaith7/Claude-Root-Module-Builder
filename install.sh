#!/bin/sh
# File: install.sh
# Purpose: install the build-tools skill folder into Claude's skills folder, safely.
# Kid note: this copies the skill to the right place and keeps a backup of any older copy.
# Usage: sh install.sh [--ref BRANCH_OR_TAG] [--sha256 HASH] [--check] [--uninstall]
# Test override: BT_SOURCE_DIR=/path/to/repo (copy from a local folder instead of downloading).
set -eu

REPO="lionlaith7/Claude-Root-Module-Builder"
REF="main"
SHA=""
MODE="install"
SKILLS="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DEST="$SKILLS/build-tools"

while [ $# -gt 0 ]; do
    case "$1" in
        --ref) REF="$2"; shift 2 ;;
        --sha256) SHA="$2"; shift 2 ;;
        --check) MODE="check"; shift ;;
        --uninstall) MODE="uninstall"; shift ;;
        *) echo "unknown option: $1" >&2; exit 2 ;;
    esac
done

if [ "$MODE" = "uninstall" ]; then
    if [ -d "$DEST" ]; then
        mv "$DEST" "$DEST.removed.$(date +%Y%m%d%H%M%S)"
        echo "OK: moved $DEST aside (delete the .removed folder when sure)"
    else
        echo "nothing to uninstall"
    fi
    exit 0
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

if [ -n "${BT_SOURCE_DIR:-}" ]; then
    mkdir -p "$TMP/src"
    cp -R "$BT_SOURCE_DIR/build-tools" "$TMP/src/build-tools"
else
    command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
    command -v tar >/dev/null 2>&1 || { echo "tar is required" >&2; exit 1; }
    curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" -o "$TMP/a.tgz"
    if [ -n "$SHA" ]; then
        GOT=$(sha256sum "$TMP/a.tgz" | cut -d' ' -f1)
        [ "$GOT" = "$SHA" ] || { echo "sha256 mismatch: got $GOT" >&2; exit 1; }
    else
        echo "NOTE: no --sha256 given; the download is not verified (a checksum from the same site would not prove authenticity either)."
    fi
    mkdir -p "$TMP/x"
    tar -xzf "$TMP/a.tgz" -C "$TMP/x"
    mkdir -p "$TMP/src"
    mv "$TMP"/x/*/build-tools "$TMP/src/build-tools"
fi

S="$TMP/src/build-tools"
[ -f "$S/SKILL.md" ] || { echo "SKILL.md missing in download" >&2; exit 1; }
NAME=$(sed -n 's/^name: *//p' "$S/SKILL.md" | head -n 1)
[ "$NAME" = "build-tools" ] || { echo "skill name '$NAME' does not match folder build-tools" >&2; exit 1; }
for f in scripts/lint_module.py scripts/build_zip.py scripts/new_module.py scripts/parse_report.py references/logging.md; do
    [ -s "$S/$f" ] || { echo "missing $f" >&2; exit 1; }
done

if [ "$MODE" = "check" ]; then
    echo "OK: download is a valid build-tools skill (not installed, --check)"
    exit 0
fi

mkdir -p "$SKILLS"
if [ -e "$DEST" ]; then
    BK="$DEST.bak.$(date +%Y%m%d%H%M%S)"
    mv "$DEST" "$BK"
    echo "Backed up old copy to $BK"
fi
mv "$S" "$DEST"
echo "OK: build-tools installed to $DEST"
echo "Restart Claude Code, then ask it to build a module."
