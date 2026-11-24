# SELinux and mounting

- SELinux is enforcing on the test device (T3 from manager screen). A denial shows as `avc: denied { ... } scontext=... tcontext=...` in dmesg/logcat; dbg_avc copies them into the log.
- Fix with the narrowest rule in `sepolicy.rule`: `allow <source> <target> <class> { perm }`. Never `permissive` globally. Do not guess contexts; copy them from the AVC line.
- Files you create at runtime in `/data/adb/...` get the `adb_data_file` context; apps cannot read them. Output meant for the user goes through dbg_sync to Documents.
- Mounting: built-in Magic Mount on FinaSU (screen, T3). KernelSU-Next documents Magic Mount and OverlayFS with a toggle (T2). Hide-list/SUSFS modules can affect visibility of mounts; check `PROBE` mount lines in the canary log.
- `/system` is not written directly. Put files in `system/` of the module; the manager mounts them.
- Android 16 / API 36 specifics are T4 until a canary log from the device exists.
