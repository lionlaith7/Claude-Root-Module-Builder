#!/system/bin/sh
# File: probe.sh
# Purpose: read-only questions to the phone: which tools, shell features, mounts and policies exist.
# Kid note: this file only looks around the phone and writes what it sees; it changes nothing.
# Needs dbg.sh sourced. Everything here is read-only.

# bt_try_shell NAME 'code': run code in a subshell, log yes/no
bt_try_shell() {
    if ( eval "$2" ) >/dev/null 2>&1; then dbg_log INFO "PROBE shell $1=yes"; else dbg_log INFO "PROBE shell $1=no"; fi
}

bt_local_test() { local q=1; [ "$q" = 1 ]; }

bt_probe() {
    for _t in sha256sum md5sum find sort cut tr grep awk sed head tail wc stat readlink zcat curl wget nc resetprop getprop setprop dmesg logcat mount id su ksud magisk busybox; do
        _p=$(command -v "$_t" 2>/dev/null)
        dbg_log INFO "PROBE tool $_t=${_p:-missing}"
    done
    bt_try_shell double_bracket '[[ a == a ]]'
    bt_try_shell arrays 'a=(1 2); [ "${a[1]}" = 2 ]'
    bt_try_shell replace_expansion 'x=abc; [ "${x//b/X}" = aXc ]'
    bt_try_shell echo_dash_e '[ "$(echo -e "a\tb")" != "-e a	b" ]'
    if bt_local_test 2>/dev/null; then dbg_log INFO "PROBE shell local=yes"; else dbg_log INFO "PROBE shell local=no"; fi
    dbg_log INFO "PROBE exe=$(readlink /proc/$$/exe 2>/dev/null) bash_version=${BASH_VERSION:-none} path=$PATH"
    if command -v busybox >/dev/null 2>&1; then dbg_log INFO "PROBE busybox=$(busybox 2>&1 | head -n 1)"; fi
    dbg_log INFO "PROBE adb_dir=$(ls -A /data/adb 2>/dev/null | tr '\n' ' ')"
    dbg_log INFO "PROBE selinux_self=$(cat /proc/self/attr/current 2>/dev/null) id_z=$(id -Z 2>/dev/null)"
    dbg_log INFO "PROBE module_dir_ctx=$(ls -Zd "$DBG_DIR" 2>/dev/null)"
    dbg_log INFO "PROBE storage=$(ls -ld /sdcard /storage/emulated/0 /storage/emulated/0/Documents 2>&1 | tr '\n' ';')"
    for _p in ro.product.first_api_level ro.build.type ro.build.tags ro.boot.verifiedbootstate ro.boot.slot_suffix ro.debuggable ro.secure; do
        dbg_log INFO "PROBE prop $_p=$(dbg_prop "$_p")"
    done
    if command -v zcat >/dev/null 2>&1 && [ -r /proc/config.gz ]; then
        zcat /proc/config.gz 2>/dev/null | grep -E '^CONFIG_(OVERLAY_FS|FUSE_FS|SDCARD_FS|KSU|SECURITY_SELINUX)[A-Z_]*=' | head -n 12 | while IFS= read -r _l; do dbg_log INFO "PROBE kconfig $_l"; done
    else
        dbg_log INFO "PROBE kconfig=unavailable"
    fi
    dbg_log INFO "PROBE modules_update=$(ls -A /data/adb/modules_update 2>/dev/null | tr '\n' ' ')"
}
