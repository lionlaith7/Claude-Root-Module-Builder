#!/system/bin/sh
# File: uninstall.sh
# Purpose: runs when the manager removes the module; cleans only what this module created.
# Kid note: when you remove the module, this tidies up its own small files and keeps the diary.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="uninstall"
. "$MODDIR/dbg.sh"

dbg_stage_begin
dbg_log INFO "uninstall: module is being removed"
dbg_sync
# Remove only runtime state we created. The log in Documents is kept on purpose.
rm -rf "$DBG_INT_DIR/lock" "$DBG_INT_DIR/boot_count"
