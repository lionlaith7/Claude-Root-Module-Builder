#!/system/bin/sh
# File: boot-completed.sh
# Purpose: runs when boot finished (KernelSU-family managers; not all run it).
# Clears the bootloop guard as soon as boot is proven complete, so a slow or
# interrupted service start does not spend guard budget. service.sh clears
# it too; clearing twice is harmless.
# Kid note: the phone finished starting, so the safety counter resets here.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="boot-completed"
. "$MODDIR/dbg.sh"
. "$MODDIR/guard.sh"

dbg_stage_begin
bt_guard_clear
dbg_log INFO "stage end"
dbg_sync
