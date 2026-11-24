#!/system/bin/sh
# File: post-fs-data.sh
# Purpose: earliest boot stage. It BLOCKS the boot, so it only counts the boot for the bootloop guard.
# Kid note: this runs very early while the phone starts, so it must be quick and do almost nothing.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="post-fs-data"
. "$MODDIR/dbg.sh"
. "$MODDIR/guard.sh"

dbg_stage_begin
bt_guard_enter || exit 0
# Put here only work that MUST happen before modules are mounted. Use resetprop -n, never setprop.
dbg_log INFO "stage end"
