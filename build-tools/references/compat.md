# Compatibility matrix (what is known)

| Item | Magisk | KernelSU official | KernelSU-Next | FinaSU (user device) |
|---|---|---|---|---|
| module.prop/zip layout | T1 | T1 | T2 | T3 (2026-11-25) |
| service.sh / post-fs-data.sh | T1 | T1 | T2 | T3 (2026-11-25) |
| boot-completed.sh / post-mount.sh | - | T1 | T4 | T3 (2026-11-25, both ran) |
| Metamodules | - | T1 | T4 | metamodule + mountify present (T3) |
| action.sh | T1 | T1 | T4 | T3 (2026-11-25) |

User device facts (T3, real debug log 2026-11-25, SysDiag Lab v1.0.0, status PASS_REAL): Redmi Note 10 Pro (sweet, M2101K6G), Android 16 / API 36, FinaSU manager ksud 1.7.0 (KSU_VER_CODE 33224), kernel 4.14.357-reforge non-GKI with CONFIG_KSU_SUSFS=y, SELinux Enforcing (policyvers 31), module scripts run as `u:r:ksu:s0` in BusyBox ash standalone (BusyBox v1.36.1.1 topjohnwu), OnyxZygisk. The build fingerprint is spoofed (stock Android 13 fingerprint on a running Android 16 system): trust `ro.build.version.release`/`sdk`, never the fingerprint, for the running version.
More T3 facts from the same log:
- All five stages ran: post-fs-data (uptime ~15 s), post-mount (~16 s), service (~19 s), boot-completed (~61 s), action. `sys.boot_completed=1` at ~61 s uptime; service waited 42 s.
- `MAGISK_VER_CODE=25200` appears at install only; the `magisk` binary is missing at boot. `resetprop` is `/data/adb/ksu/bin/resetprop`. `KSU_KERNEL_VER_CODE` differed between install (33187) and service (32737): env vars are not stable across stages.
- General script dirs: post-fs-data.d, service.d and boot-completed.d exist; post-mount.d does NOT, yet the module's own post-mount.sh still ran. Module stage scripts and general `.d` dirs are independent.
- Mounting: no overlay mount lines for modules; a metamodule/mountify setup is present. Do not assume overlay.
- Shell: arrays=no; `[[ ]]`, `${x//}`, `local`, arithmetic, printf, case, atomic mkdir all yes on this BusyBox. Templates stay POSIX anyway.
- Scripts with mode 0644 (no exec bit) ran fine: the manager invokes them via sh. Exec bit is not required.
- SUSFS: `/sys/fs/susfs` does not exist even though the kernel has CONFIG_KSU_SUSFS=y. Detect SUSFS from kconfig, not from that path.
- `wm size`/`wm density` fail from a module service ("Failure calling service window"); `dumpsys display` works. /proc/cpuinfo has no Hardware/model name lines on this kernel; use `ro.soc.model`.
