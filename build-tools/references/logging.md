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
2. Stages missing? That stage never ran: wrong file name, or manager lacks it. (T3: a missing exec bit does NOT stop a stage on FinaSU — the manager runs scripts via sh.)
3. FAIL checks / ERROR lines: fix the code at that line's stage.
4. AVC lines: they are system-wide, not module-only (observed 2026-11-25: AVC count=50, none from the module's own context). Filter by `scontext` and by paths under the module before blaming the module or writing a rule. See selinux-mounting.md.
5. HASH mismatch: the user ran an older zip; ask for a re-install. Exception: files the module rewrites at runtime (e.g. `webroot/*.json` copied from Documents) always mismatch; that one is expected.
6. boots>1 without BOOT completed: bootloop suspicion; check the `disable` file. Nuance (T3): a quick manual reboot right after install also increments the guard counter — observed counter=2 on a healthy module whose first boot was interrupted by a second reboot. One interrupted boot is not a loop; look for repeated STAGE begin without BOOT completed.
7. Early-boot wall-clock timestamps can be bogus before time sync (observed `1975-04-01`); order those lines by `uptime=`. The guard's `boot_start` epoch stamp has the same limit; the timeout check itself uses uptime and is unaffected.

Privacy: the log has no serials, accounts or tokens. Set `DBG_NO_MODLIST=1` to hide the other-modules list. Never add secrets to logs. Never publish a raw device log: AVC lines carry other apps' package names and paths, and SNAP lists installed module names. Publish aggregated facts only.
