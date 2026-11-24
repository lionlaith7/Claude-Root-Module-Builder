#!/system/bin/sh
# File: post-fs-data.sh
# Purpose: canary stage marker. Records that this stage ran and when. Blocking stage: keep it tiny.
# Kid note: this only says "I was here" very early in the start-up, with the time.
MODDIR=${0%/*}
DBG_ID="@ID@"
DBG_DIR="$MODDIR"
DBG_STAGE="post-fs-data"
. "$MODDIR/dbg.sh"
. "$MODDIR/guard.sh"

dbg_stage_begin
bt_guard_enter || exit 0
dbg_log INFO "probe: KSU=${KSU:-unset} ASH_STANDALONE=${ASH_STANDALONE:-unset} ZYGISK_ENABLED=${ZYGISK_ENABLED:-unset}"
dbg_log INFO "stage end"
