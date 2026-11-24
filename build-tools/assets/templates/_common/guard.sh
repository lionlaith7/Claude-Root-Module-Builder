#!/system/bin/sh
# File: guard.sh
# Purpose: bootloop guard. If boots keep failing before the module finishes, the module disables itself.
# Kid note: this is a safety switch; if the phone keeps failing to start, it turns the module off.
# Needs dbg.sh sourced first. Call bt_guard_enter at the top of post-fs-data.sh and bt_guard_clear in service.sh after boot.

BT_GUARD_MAX="${BT_GUARD_MAX:-3}"   # unfinished boots in a row before the module disables itself

# bt_guard_enter: count this boot. Returns 1 (and creates the "disable" flag) when the limit is reached.
bt_guard_enter() {
    mkdir -p "$DBG_INT_DIR" 2>/dev/null
    _f="$DBG_INT_DIR/boot_count"
    _n=$(cat "$_f" 2>/dev/null)
    case "$_n" in ''|*[!0-9]*) _n=0 ;; esac
    _n=$((_n + 1))
    printf '%s' "$_n" > "$_f" 2>/dev/null
    dbg_log INFO "guard: unfinished-boot counter=$_n (limit $BT_GUARD_MAX)"
    if [ "$_n" -ge "$BT_GUARD_MAX" ]; then
        : > "$DBG_DIR/disable"
        dbg_log ERROR "guard: $_n boots in a row did not finish; module disabled (flag $DBG_DIR/disable)"
        return 1
    fi
    return 0
}

# bt_guard_clear: boot finished, reset the counter.
bt_guard_clear() {
    printf '0' > "$DBG_INT_DIR/boot_count" 2>/dev/null
    dbg_log INFO "guard: boot finished, counter reset"
}
