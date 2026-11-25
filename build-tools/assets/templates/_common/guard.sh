#!/system/bin/sh
# File: guard.sh
# Purpose: bootloop guard. If boots keep failing before the module finishes, the module disables itself.
# Kid note: this is a safety switch; if the phone keeps failing to start, it turns the module off.
# Needs dbg.sh sourced first. Call bt_guard_enter at the top of post-fs-data.sh and bt_guard_clear in service.sh after boot.
# Patterns learned from YetAnotherBootloopProtector, AshLooper, abootloop and
# Bootloop-Protection: count unfinished boots, reset on boot_completed, act by
# creating the reversible "disable" file, never reboot, never touch other modules.
# See references/bootloop.md for the full before/during/after playbook.

BT_GUARD_MAX="${BT_GUARD_MAX:-3}"   # unfinished boots in a row before the module disables itself
BT_GUARD_TIMEOUT="${BT_GUARD_TIMEOUT:-180}"   # seconds of uptime without boot_completed before self-disable

# bt_guard_enter: count this boot and stamp when it started.
# Returns 1 (and creates the "disable" flag) when the limit is reached.
bt_guard_enter() {
    mkdir -p "$DBG_INT_DIR" 2>/dev/null
    _f="$DBG_INT_DIR/boot_count"
    _n=$(cat "$_f" 2>/dev/null)
    case "$_n" in ''|*[!0-9]*) _n=0 ;; esac
    _n=$((_n + 1))
    printf '%s' "$_n" > "$_f" 2>/dev/null
    printf '%s' "$(date +%s 2>/dev/null)" > "$DBG_INT_DIR/boot_start" 2>/dev/null
    dbg_log INFO "guard: unfinished-boot counter=$_n (limit $BT_GUARD_MAX)"
    if [ "$_n" -ge "$BT_GUARD_MAX" ]; then
        : > "$DBG_DIR/disable"
        dbg_log ERROR "guard: $_n boots in a row did not finish; module disabled (flag $DBG_DIR/disable)"
        bt_guard_rescue_info
        return 1
    fi
    return 0
}

# bt_guard_clear: boot finished, reset the counter.
bt_guard_clear() {
    printf '0' > "$DBG_INT_DIR/boot_count" 2>/dev/null
    dbg_log INFO "guard: boot finished, counter reset"
}

# bt_guard_check_timeout: late-start watchdog. Call from service.sh after
# dbg_wait_boot. If uptime passed the timeout and boot still has not
# completed, disable this module only and log it. Never reboots: a watchdog
# that reboots can turn a hang into a loop. Returns 1 when it disabled.
bt_guard_check_timeout() {
    [ "${DBG_FORCE_READY:-0}" = 1 ] && return 0
    [ "$(dbg_prop sys.boot_completed)" = 1 ] && return 0
    _up=$(cut -d. -f1 /proc/uptime 2>/dev/null)
    case "$_up" in ''|*[!0-9]*) return 0 ;; esac
    if [ "$_up" -ge "$BT_GUARD_TIMEOUT" ]; then
        : > "$DBG_DIR/disable"
        dbg_log ERROR "guard: boot not completed after ${_up}s (timeout ${BT_GUARD_TIMEOUT}s); module disabled (flag $DBG_DIR/disable)"
        bt_guard_rescue_info
        return 1
    fi
    dbg_log INFO "guard: boot still pending at ${_up}s (timeout ${BT_GUARD_TIMEOUT}s)"
    return 0
}

# bt_guard_rescue_info: log the manual rescue path so it is in every log.
bt_guard_rescue_info() {
    dbg_log INFO "guard: rescue: remove $DBG_DIR/disable to re-enable; or create an empty disable file in /data/adb/modules/$DBG_ID/ from recovery/adb to switch this module off"
}
