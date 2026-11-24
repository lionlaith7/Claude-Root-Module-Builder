#!/system/bin/sh
# File: post-mount.sh
# Purpose: canary stage marker for managers that run a script after modules are mounted (not all do).
# Kid note: if this line appears in the diary, the manager has this extra start-up step.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="post-mount"
. "$MODDIR/dbg.sh"

dbg_stage_begin
dbg_log INFO "stage end"
