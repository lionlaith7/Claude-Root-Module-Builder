#!/system/bin/sh
# File: dbg.sh
# Purpose: the module's diary. Writes a debug log and copies it to /sdcard/Documents/<id>/ so it can be sent back for fixes.
# Kid note: this file writes down what the module did, like a diary, so a helper can find problems.
# Caller sets before sourcing: DBG_ID (module id), DBG_DIR (module folder), DBG_STAGE (name of the running script).
# Works in BusyBox ash (Magisk/KernelSU) and in dash/bash for local simulation. No bashisms.
# Never log secrets: do not pass passwords, tokens or personal data to dbg_log.

# Settings (override with environment variables when simulating on a PC)
DBG_INT_DIR="${DBG_INT_DIR:-/data/adb/${DBG_ID}-logs}"        # always-writable spool
DBG_DOCS_DIR="${DBG_DOCS_DIR:-/sdcard/Documents/${DBG_ID}}"   # copy the user can see and send back
DBG_MAX_BYTES="${DBG_MAX_BYTES:-262144}"                      # rotate the spool after this size
DBG_SYNC_GAP="${DBG_SYNC_GAP:-30}"                            # seconds between automatic copies
DBG_LOG="$DBG_INT_DIR/${DBG_ID}-debug.log"
DBG_LAST_SYNC=0

# Read a system property; prints nothing when getprop is missing (PC simulation).
dbg_prop() {
    if command -v getprop >/dev/null 2>&1; then getprop "$1" 2>/dev/null; fi
}

# dbg_log LEVEL message...   (LEVEL: INFO WARN ERROR DEBUG)
dbg_log() {
    _lvl="$1"; shift
    mkdir -p "$DBG_INT_DIR" 2>/dev/null || return 0
    # Rotate first so the spool cannot grow without limit.
    if [ -f "$DBG_LOG" ]; then
        _sz=$(wc -c < "$DBG_LOG" 2>/dev/null)
        if [ "$(( ${_sz:-0} + 0 ))" -gt "$DBG_MAX_BYTES" ]; then mv -f "$DBG_LOG" "$DBG_LOG.1" 2>/dev/null; fi
    fi
    printf '%s %s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S' 2>/dev/null)" "$_lvl" "${DBG_STAGE:-main}" "$*" >> "$DBG_LOG" 2>/dev/null
    return 0
}
dbg_info()  { dbg_log INFO "$*"; }
dbg_warn()  { dbg_log WARN "$*"; }
dbg_error() { dbg_log ERROR "$*"; }

# dbg_stage_begin: marks that this script started (the analysis tool reads these markers).
dbg_stage_begin() {
    dbg_log INFO "STAGE begin $DBG_STAGE pid=$$ uptime=$(cut -d' ' -f1 /proc/uptime 2>/dev/null) boot_completed=$(dbg_prop sys.boot_completed)"
}

# dbg_run cmd args... : run a command, log its exit code and the first 40 output lines.
dbg_run() {
    _out=$("$@" 2>&1); _rc=$?
    dbg_log DEBUG "run: $* -> rc=$_rc"
    if [ -n "$_out" ]; then
        printf '%s\n' "$_out" | head -n 40 | while IFS= read -r _l; do dbg_log DEBUG "  | $_l"; done
    fi
    return $_rc
}

# dbg_check NAME cmd args... : an "effect check". Logs CHECK NAME PASS or CHECK NAME FAIL.
# Use it to prove the module really did its job, e.g. dbg_check prop_set test "$(getprop x.y)" = 1
dbg_check() {
    _n="$1"; shift
    if "$@" >/dev/null 2>&1; then dbg_log INFO "CHECK $_n PASS"; return 0; fi
    dbg_log ERROR "CHECK $_n FAIL"; return 1
}

# Storage is only trusted when the system says boot finished AND the user storage tree exists.
# This avoids writing into an unmounted /sdcard mount point (the file would be lost).
dbg_storage_ready() {
    [ "${DBG_FORCE_READY:-0}" = 1 ] && return 0
    [ "$(dbg_prop sys.boot_completed)" = 1 ] || return 1
    [ -d /storage/emulated/0/Android ] || return 1
    return 0
}

# dbg_sync: copy the log to Documents. Returns 1 (and keeps the spool) when storage is not ready.
dbg_sync() {
    dbg_storage_ready || return 1
    mkdir -p "$DBG_DOCS_DIR" 2>/dev/null || return 1
    [ -w "$DBG_DOCS_DIR" ] || return 1
    cp -f "$DBG_LOG" "$DBG_DOCS_DIR/" 2>/dev/null || return 1
    if [ -f "$DBG_LOG.1" ]; then cp -f "$DBG_LOG.1" "$DBG_DOCS_DIR/" 2>/dev/null; fi
    chmod 0666 "$DBG_DOCS_DIR"/* 2>/dev/null
    DBG_LAST_SYNC=$(date +%s 2>/dev/null)
    return 0
}

# dbg_sync_soon: like dbg_sync but at most once per DBG_SYNC_GAP seconds (for loops).
dbg_sync_soon() {
    _now=$(date +%s 2>/dev/null)
    if [ "$(( ${_now:-0} - ${DBG_LAST_SYNC:-0} ))" -ge "$DBG_SYNC_GAP" ]; then dbg_sync; fi
    return 0
}

# dbg_wait_boot [seconds]: wait for sys.boot_completed (default 300 s).
dbg_wait_boot() {
    _max="${1:-300}"; _t=0
    while [ "$_t" -lt "$_max" ]; do
        if [ "${DBG_FORCE_READY:-0}" = 1 ] || [ "$(dbg_prop sys.boot_completed)" = 1 ]; then
            dbg_log INFO "BOOT completed (waited ${_t}s)"; return 0
        fi
        sleep 2; _t=$((_t + 2))
    done
    dbg_log WARN "BOOT not completed after ${_max}s"; return 1
}

# dbg_wait_storage [seconds]: wait until Documents can be written (default 120 s).
dbg_wait_storage() {
    _max="${1:-120}"; _t=0
    while [ "$_t" -lt "$_max" ]; do
        dbg_storage_ready && return 0
        sleep 3; _t=$((_t + 3))
    done
    dbg_log WARN "STORAGE not ready after ${_max}s; log stays in $DBG_INT_DIR"; return 1
}

# dbg_snapshot: one block describing the device and the root environment (no serials, no accounts).
dbg_snapshot() {
    dbg_log INFO "SNAP module_id=$DBG_ID"
    if [ -f "$DBG_DIR/module.prop" ]; then
        grep -E '^(version|versionCode)=' "$DBG_DIR/module.prop" 2>/dev/null | while IFS= read -r _l; do dbg_log INFO "SNAP $_l"; done
    fi
    dbg_log INFO "SNAP sim=${DBG_FORCE_READY:-0}"
    dbg_log INFO "SNAP kernel=$(uname -r 2>/dev/null)"
    dbg_log INFO "SNAP selinux=$(getenforce 2>/dev/null)"
    dbg_log INFO "SNAP uid=$(id -u 2>/dev/null)"
    dbg_log INFO "SNAP shell=$0 ash_standalone=${ASH_STANDALONE:-unset}"
    for _p in ro.build.version.release ro.build.version.sdk ro.product.device ro.product.model ro.product.cpu.abi ro.build.display.id ro.build.fingerprint ro.vendor.build.fingerprint; do
        dbg_log INFO "SNAP $_p=$(dbg_prop "$_p")"
    done
    dbg_log INFO "SNAP env KSU=${KSU:-unset} KSU_VER_CODE=${KSU_VER_CODE:-unset} KSU_KERNEL_VER_CODE=${KSU_KERNEL_VER_CODE:-unset} MAGISK_VER_CODE=${MAGISK_VER_CODE:-unset}"
    if [ -x /data/adb/ksud ]; then dbg_log INFO "SNAP ksud=$(/data/adb/ksud --version 2>&1 | head -n 1)"; fi
    if command -v magisk >/dev/null 2>&1; then dbg_log INFO "SNAP magisk=$(magisk -V 2>&1 | head -n 1)"; fi
    if [ "${DBG_NO_MODLIST:-0}" != 1 ] && [ -d /data/adb/modules ]; then
        dbg_log INFO "SNAP other_modules=$(ls /data/adb/modules 2>/dev/null | tr '\n' ' ')"
    fi
    grep -E 'overlay|magisk|ksu|KSU|/storage/emulated' /proc/mounts 2>/dev/null | head -n 12 | while IFS= read -r _l; do dbg_log INFO "SNAP mount $_l"; done
}

# dbg_hash: sha256 of every file of this module (ties the log to the exact zip that was built).
dbg_hash() {
    (
        cd "$DBG_DIR" 2>/dev/null || exit 0
        find . -type f ! -name '*.log' ! -path './META-INF/*' 2>/dev/null | sort | while IFS= read -r _f; do
            _h=$(sha256sum "$_f" 2>/dev/null | cut -d' ' -f1)
            dbg_log INFO "HASH ${_h:-nohash} ${_f#./}"
        done
    )
}

# dbg_avc [pattern]: recent SELinux denials (kernel log), filtered by pattern (default: denied).
dbg_avc() {
    _pat="${1:-denied}"
    _n=$(dmesg 2>/dev/null | grep 'avc:' | grep -c "$_pat")
    dbg_log INFO "AVC count=${_n:-0} pattern=$_pat"
    dmesg 2>/dev/null | grep 'avc:' | grep "$_pat" | tail -n 20 | while IFS= read -r _l; do dbg_log INFO "AVC $_l"; done
}
