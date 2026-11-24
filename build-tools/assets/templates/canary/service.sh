#!/system/bin/sh
# File: service.sh
# Purpose: canary main stage. Waits for boot, runs the read-only probes, writes the full report.
# Kid note: after the phone started, this looks around, writes everything it learned in the diary, and copies it.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="service"
. "$MODDIR/dbg.sh"
. "$MODDIR/guard.sh"
. "$MODDIR/probe.sh"

dbg_stage_begin
dbg_wait_boot 300
bt_guard_clear
dbg_snapshot
bt_probe
dbg_hash
dbg_check storage_probe_dir_exists test -d "$DBG_INT_DIR"
dbg_avc
dbg_wait_storage 120
dbg_log INFO "stage end"
dbg_sync
