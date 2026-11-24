#!/system/bin/sh
# File: service.sh
# Purpose: background service. One copy only (lock folder), waits for boot, re-reads settings every cycle.
# Kid note: this keeps running in the background and does a small job again and again, one copy at a time.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="service"
. "$MODDIR/dbg.sh"
. "$MODDIR/guard.sh"

# Settings (file: $DBG_INT_DIR/config.prop, line "interval=60"). Read as data, never sourced.
DEFAULT_INTERVAL=60
LOCK="$DBG_INT_DIR/lock"

# bt_conf key default : read one value from config.prop
bt_conf() {
    _v=$(grep -E "^$1=" "$DBG_INT_DIR/config.prop" 2>/dev/null | tail -n 1 | cut -d= -f2-)
    printf '%s' "${_v:-$2}"
}

# bt_work: the job done each cycle. Replace the example.
bt_work() {
    dbg_log INFO "cycle $1: working"
}

dbg_stage_begin

# One instance only: mkdir is atomic. A stale lock (dead pid or another program) is replaced.
if ! mkdir "$LOCK" 2>/dev/null; then
    _old=$(cat "$LOCK/pid" 2>/dev/null)
    if [ -n "$_old" ] && [ -r "/proc/$_old/cmdline" ] && tr '\0' ' ' < "/proc/$_old/cmdline" | grep -q 'service.sh'; then
        dbg_log WARN "another instance is running (pid $_old); exiting"
        exit 0
    fi
    dbg_log WARN "stale lock found; taking over"
    rm -rf "$LOCK"
    mkdir "$LOCK" 2>/dev/null || { dbg_log ERROR "cannot create lock"; exit 1; }
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"; dbg_log INFO "service stopped"; dbg_sync' EXIT

dbg_wait_boot 300
bt_guard_clear
dbg_snapshot
dbg_hash
dbg_avc
dbg_wait_storage 120
dbg_sync

cycle=0
while :; do
    interval=$(bt_conf interval "$DEFAULT_INTERVAL")
    case "$interval" in ''|*[!0-9]*) interval=$DEFAULT_INTERVAL ;; esac
    [ "$interval" -lt 10 ] && interval=10
    [ "$interval" -gt 3600 ] && interval=3600
    cycle=$((cycle + 1))
    bt_work "$cycle"
    dbg_sync_soon
    [ "${BT_ONCE:-0}" = 1 ] && break
    sleep "$interval"
done
dbg_log INFO "stage end"
