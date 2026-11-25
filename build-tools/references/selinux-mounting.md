# SELinux and mounting

- SELinux is enforcing on the test device (T3, real log 2026-11-25, policyvers 31). A denial shows as `avc: denied { ... } scontext=... tcontext=...` in dmesg/logcat; dbg_avc copies them into the log. Those lines are system-wide: in the first real log all 50 AVCs belonged to other apps/system, none to the module. Filter by `scontext` (module scripts run as `u:r:ksu:s0` on FinaSU) and module paths before writing any rule.
- Fix with the narrowest rule in `sepolicy.rule`: `allow <source> <target> <class> { perm }`. Never `permissive` globally. Do not guess contexts; copy them from the AVC line.
- Files you create at runtime in `/data/adb/...` get the `adb_data_file` context; apps cannot read them. Output meant for the user goes through dbg_sync to Documents. The module dir itself carried `u:object_r:system_file:s0` on the test device (T3).
- Mounting: on the test device there were no overlay mount lines for modules and a metamodule/mountify setup was present (T3, 2026-11-25). KernelSU-Next documents Magic Mount and OverlayFS with a toggle (T2). Hide-list/SUSFS modules can affect visibility of mounts; check `PROBE` mount lines in the canary log. SUSFS detection: use `CONFIG_KSU_SUSFS` from kconfig — `/sys/fs/susfs` did not exist on a SUSFS kernel (T3).
- `/system` is not written directly. Put files in `system/` of the module; the manager mounts them.
- Android 16 / API 36 specifics are T3 on the test device since the 2026-11-25 real log (PASS_REAL); on any other device they stay T4 until its canary log exists.
