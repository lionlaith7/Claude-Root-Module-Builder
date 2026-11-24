#!/system/bin/sh
# File: service.sh
# Purpose: main boot script (non-blocking). Does the module's one-time work and proves it with a check.
# Kid note: after the phone finished starting, this does the module's job once and writes the result in the diary.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="service"
. "$MODDIR/dbg.sh"
. "$MODDIR/guard.sh"

dbg_stage_begin
dbg_wait_boot 300
bt_guard_clear
dbg_snapshot
dbg_hash

# ---- YOUR WORK (replace the example) ----
mkdir -p "$DBG_INT_DIR"
date > "$DBG_INT_DIR/last_run"
dbg_check last_run_written test -s "$DBG_INT_DIR/last_run"
# ---- END OF YOUR WORK ----

dbg_avc
dbg_wait_storage 120
dbg_log INFO "stage end"
dbg_sync
