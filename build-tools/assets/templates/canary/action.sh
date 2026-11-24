#!/system/bin/sh
# File: action.sh
# Purpose: runs when you tap the Action button of the module (if the manager has one). Copies the log now.
# Kid note: tap the button and the diary is copied to Documents right away.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="action"
. "$MODDIR/dbg.sh"

dbg_stage_begin
if dbg_sync; then
    echo "Log copied to $DBG_DOCS_DIR"
else
    echo "Storage not ready; log is in $DBG_INT_DIR"
fi
dbg_log INFO "stage end"
