#!/system/bin/sh
# File: boot-completed.sh
# Purpose: canary stage marker for managers that run a script when boot finished (not all do).
# Kid note: if this line appears in the diary, the manager has a "phone is ready" step.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="boot-completed"
. "$MODDIR/dbg.sh"

dbg_stage_begin
dbg_log INFO "stage end"
dbg_sync
