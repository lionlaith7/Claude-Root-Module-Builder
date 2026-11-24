# File: customize.sh
# Purpose: install-time script (sourced by the module installer). Logs the install and sets permissions.
# Kid note: this runs once when you flash the module; it writes the first lines of the diary.
# Rules: this file is sourced, so never call exit here; use abort "message" to stop an install.

SKIPUNZIP=0
DBG_ID="@ID@"
DBG_DIR="$MODPATH"
DBG_STAGE="install"
. "$MODPATH/dbg.sh"

ui_print "- @NAME@ @VERSION@"
dbg_stage_begin
dbg_log INFO "install: API=${API:-?} ARCH=${ARCH:-?} BOOTMODE=${BOOTMODE:-?} KSU=${KSU:-no} KSU_VER_CODE=${KSU_VER_CODE:-} MAGISK_VER_CODE=${MAGISK_VER_CODE:-} zip=$(basename "$ZIPFILE")"
dbg_snapshot

# Add your own install checks here, for example:
# [ "${API:-0}" -ge 29 ] || abort "Needs Android 10 or newer"

set_perm_recursive "$MODPATH" 0 0 0755 0644
dbg_hash
dbg_log INFO "install: done"
if dbg_sync; then
    ui_print "- Debug log: /sdcard/Documents/$DBG_ID/$DBG_ID-debug.log"
else
    ui_print "- Debug log is kept in $DBG_INT_DIR and is copied to Documents after the first boot"
fi
