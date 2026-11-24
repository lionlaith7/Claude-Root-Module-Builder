# Logging and debugging spec

Files in every module: `dbg.sh` (diary library), `guard.sh` (bootloop guard).

Paths
- Spool (always writable early): `/data/adb/<id>-logs/<id>-debug.log`, rotates to `.1` at 256 KB.
- Copy for the user: `/sdcard/Documents/<id>/<id>-debug.log`, written only when `sys.boot_completed=1` and `/storage/emulated/0/Android` exists. Before that the log stays in the spool (storage is not mounted early in boot).
- If the user cannot find it: run the module Action button (canary has one) or read the spool with a root file manager.

Line format: `YYYY-MM-DD HH:MM:SS LEVEL [stage] message`

Markers parse_report.py understands
- `SNAP key=value` device facts (module_id, version, sim, kernel, selinux, uid, shell, env, other_modules)
- `STAGE begin <stage> pid= uptime= boot_completed=`
- `CHECK <name> PASS` / `CHECK <name> FAIL` (FAIL also logs an ERROR)
- `HASH <sha256> <relpath>` for each shipped file
- `AVC ...` SELinux denial lines from dmesg
- `BOOT completed`, `PROBE ...` (canary)

How to analyse an uploaded log
1. `python3 -I scripts/parse_report.py LOG --manifest MANIFEST`.
2. Stages missing? That stage never ran: wrong file name, not executable, or manager lacks it.
3. FAIL checks / ERROR lines: fix the code at that line's stage.
4. AVC lines: see selinux-mounting.md; add the narrowest `sepolicy.rule`.
5. HASH mismatch: the user ran an older zip; ask for a re-install.
6. boots>1 without BOOT completed: bootloop suspicion; check the `disable` file.

Privacy: the log has no serials, accounts or tokens. Set `DBG_NO_MODLIST=1` to hide the other-modules list. Never add secrets to logs.
