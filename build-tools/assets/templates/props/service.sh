#!/system/bin/sh
# File: service.sh
# Purpose: after boot, checks that every property in props.list really has the wanted value.
# Kid note: the module changes some phone settings; this file looks if they really changed and writes yes or no.
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

# props.list has lines "name=expected". system.prop (loaded by the manager) sets them; here we prove it.
if [ -f "$MODDIR/props.list" ]; then
    while IFS='=' read -r _k _v; do
        case "$_k" in ''|'#'*) continue ;; esac
        _now=$(dbg_prop "$_k")
        dbg_log INFO "prop $_k expected=$_v actual=$_now"
        dbg_check "prop_$_k" test "$_now" = "$_v"
    done < "$MODDIR/props.list"
else
    dbg_log WARN "props.list not found"
fi

dbg_avc
dbg_wait_storage 120
dbg_log INFO "stage end"
dbg_sync
