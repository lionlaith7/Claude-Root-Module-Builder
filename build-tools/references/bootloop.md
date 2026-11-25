# Bootloop protection: avoid, detect, recover

Learned from YetAnotherBootloopProtector, AshLooper/AshReXcue, abootloop and
Keinta15/Bootloop-Protection. All four act the same safe way: they create a
`disable` file in a module folder. None wipes `/data`. A `disable` file is
reversible, which is why this skill uses it too.

## 1. Avoid a bootloop in the first place (prevention)

A bootloop is almost always self-inflicted at build time. Before flashing:

- Keep `post-fs-data.sh` tiny. It blocks boot (Magisk cap 35 s, older docs
  and KernelSU say 10 s). Only work that must happen before mounting belongs
  there, and even that must finish in well under a second. Heavy commands
  (`pm`, `dumpsys`, `logcat`, `dmesg`, package scans) never run there.
- Prefer `service.sh` (late_start, non-blocking). Wait for
  `sys.boot_completed=1`, then settle before heavy work (template default:
  10 s settle, skipped in simulation). Stagger work: a light cycle of fast
  `/proc` and `/sys` reads every 1-5 min, heavy snapshots hourly or on demand.
- One change at a time on a new device. Flash the canary first, read its log,
  then the real module. Never flash two untested modules in one reboot.
- Validate every write by reading it back (`dbg_check`). A bad `system.prop`
  value, a wrong overlay path or a broken `sepolicy.rule` can loop before any
  watchdog runs.
- No loops without a sleep, no busy polling, no unbounded files. Cap history
  and logs (the diary rotates at 256 KB). A module that fills `/data` or spins
  a CPU core can hang boot just as surely as a crash.
- Never run two bootloop protectors at once. AshReXcue warns explicitly:
  overlapping watchdogs and timers can cause the loops they claim to fix.
  This skill ships one guard per module (self-disable only). A system-wide
  protector, if the user wants one, is a separate, single choice.

## 2. Detect a bootloop (what the guard does)

Two independent signals, both in the templates:

- **Unfinished-boot counter (post-fs-data).** `guard.sh` increments
  `/data/adb/<id>-logs/boot_count` at every boot and stamps `boot_start`.
  `service.sh` resets it to 0 only after boot completes. Three unfinished
  boots in a row creates `<module>/disable` and the module turns itself off.
  This is the marker1-marker3 pattern from YetAnotherBootloopProtector.
- **Boot-completed timeout (late_start).** `bt_guard_check_timeout` in
  `guard.sh`: if uptime passes the timeout (default 180 s) and
  `sys.boot_completed` is still not 1, the module disables itself and logs
  an ERROR. It does not reboot: a watchdog that reboots can turn a hang into
  a loop. YetAnotherBootloopProtector uses a 2 min timeout with 5 s polling;
  Bootloop-Protection watches the Zygote PID 3 times every 15 s plus one
  confirm check; AshReXcue counts 3 framework restarts in one boot. This
  skill keeps the simpler, safer subset: counter + timeout, no PID watching,
  because PID watching needs a long-running monitor that can itself fail.

Self-disable only: a build-tools module never disables other modules. The
four protectors disable all modules (or, in AshReXcue, only the module that
changed since the last clean boot). Disabling others from inside a normal
module hides the culprit and can break the user's security modules.

## 3. Before a risky flash (prepare)

1. Backup of boot/data the user cares about. Know how to reach recovery or
   adb from a PC, and confirm `/data` is readable there (encrypted `/data`
   that recovery cannot decrypt removes the recovery rescue path).
2. Know the rescue file: an empty file named `disable` in
   `/data/adb/modules/<id>/` switches that module off at the next boot.
   Magisk and KernelSU both honour it. Removing the file re-enables it.
3. Install a protector, if wanted, **before** the risky module, not after.
   abootloop is useless if first installed while already looping.
4. Flash one module, reboot once, wait for the log in
   `Documents/<id>/<id>-debug.log`, and read it before flashing the next.

## 4. During a bootloop (act)

In order, least destructive first:

1. **Wait.** The guard needs up to 3 unfinished boots, and a timeout
   watchdog needs its timeout. A single slow boot is not a loop. SysDiag v1
   looped once and then booted: the counter cleared on the finished boot.
2. **Let the guard act.** After 3 unfinished boots the module disables
   itself and the phone boots without it. Then read the log: the last
   `STAGE begin` without a matching `BOOT completed` is the suspect stage.
3. **Manual disable from recovery/adb.** Create the `disable` file for the
   suspect module (or, as a last resort, for every module), then reboot.
   abootloop's `disableall.zip` recovery flash does the every-module
   version. It is safe for data and disruptive for setup, so it is last.
4. **Key-combo / safe-mode paths are device-specific.** Do not assume a
   manager has a safe mode (tier T4). Only use a combo the user has tested
   on their own device before the loop.

Never wipe `/data` or factory-reset for a module bootloop. Every protector
above recovers without it, and so does this skill.

## 5. After recovery (learn)

1. Re-enable modules one at a time, rebooting between each, so the culprit
   is identified instead of guessed. Protectors that disable everything
   (YetAnotherBootloopProtector, Bootloop-Protection) record what they
   disabled and offer an Action button to re-enable from that list.
2. Send the debug log back. `parse_report.py` flags boots without
   `BOOT completed`; read the last CHECK/ERROR/AVC lines before that point.
3. Fix the cause, not the symptom: move heavy work out of post-fs-data,
   add the settle delay, stagger the cycles, or drop the bad prop/overlay.
   Bump `versionCode`, rebuild, and re-test with the canary first if the
   device is new.
4. If the loop was not caused by a module (bad `system.prop`, early
   post-fs-data crash before the guard runs, direct system-file edits),
   late-start watchdogs may never act. Say so plainly and use the
   recovery `disable` path. That limit is stated by the protectors too.

## 6. What this skill will not do

- Disable, move or delete other modules or scripts. Self-disable only.
- Reboot the phone from a watchdog. Hangs are logged and self-disabled;
  rebooting is the user's or the system's decision.
- Back up or write partitions, wipe data, or factory-reset as a "fix".
- Run a second, competing bootloop watchdog alongside the guard.
