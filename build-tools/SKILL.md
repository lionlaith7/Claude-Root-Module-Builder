---
name: build-tools
description: >
  Expert builder of Android root modules for Magisk, KernelSU, KernelSU-Next and forks
  (FinaSU, APatch), with mandatory debug logging, bootloop protection and honest test
  statuses. Use it to create, scaffold, lint, build, debug or explain a root module:
  service.sh, post-fs-data.sh, boot-completed.sh, post-mount.sh, system.prop,
  sepolicy.rule, overlays, action.sh, WebUI (webroot/index.html), canary probes,
  bootloop rescue, or reading a module debug log the user uploaded. Triggers include
  "module", "Magisk", "KernelSU", "root module", "post-fs-data", "boot script",
  "bootloop", "debug log", "مديول", "وحدة", "روت", "ماجيسك", "سجل الأخطاء".
  Not for ordinary apps. Verified on a real device (PASS_REAL, 2026-11-25).
---

# build-tools v3.6 - root module expert

Reply in the user's language (Arabic: simple, short). Phone users read little: lead with the result.

## What this skill does
Builds a working Magisk/KernelSU module for ANY idea (specialised in root modules, general in what the module does), teaches how it works when asked, and closes the loop: **every module writes a diary (debug log) the user uploads back for fixing.**

## Workflow (follow in order)
0. **Research first.** Before any new feature, search for prior art: existing modules, skills, repos and docs that solve part of the problem (GitHub, module repos, manager docs). Read what they do, note what to adopt and what to avoid, and let the findings shape the plan. Never build from memory alone when a search can check it; never copy code blindly — learn the pattern, then implement it in this skill's templates and rules. State briefly what the research changed.
1. **Profile.** Ask only what you lack: manager + version, Android version, ROM, kernel/SELinux. Known test device (T3, real log 2026-11-25, PASS_REAL): Redmi Note 10 Pro (sweet, M2101K6G), Android 16 / API 36, FinaSU ksud 1.7.0 (KSU_VER_CODE 33224), kernel 4.14.357 with SUSFS, SELinux Enforcing, OnyxZygisk. All five stages run there (post-fs-data, post-mount, service, boot-completed, action). Facts and limits: references/compat.md. Unknown details = tier T4 (see references/evidence.md). Do not ask again for docs the user declined.
2. **Plan.** One paragraph: what the module does, which stage runs it (prefer `service.sh`; `post-fs-data.sh` blocks boot), what can brick, the rescue path. Classify bootloop risk (early stage, props, overlays, sepolicy, native code = high) and say how it is avoided; see references/bootloop.md. Refuse malware/spyware/anti-theft-bypass; see references/safety.md.
3. **Scaffold.** `python3 -I scripts/new_module.py --list`, then `--kind basic|service|props|canary --id ID --name NAME --desc TEXT --out DIR` (add `--webui` for a compliant `webroot/` starter). Never hand-write the logging files; templates include `dbg.sh`, `guard.sh`, the official `update-binary`.
4. **Implement** inside the `YOUR WORK` block. Rules: POSIX `sh` (BusyBox ash), `MODDIR=${0%/*}`, LF endings, `resetprop -n` never `setprop` in post-fs-data, `abort` never `exit` in customize.sh, no `install.sh`, no custom logic in update-binary, every action followed by a `dbg_check NAME cmd` that proves it. Bootloop avoidance: post-fs-data stays tiny and finishes in well under a second; heavy commands (`pm`, `dumpsys`, `logcat`, `dmesg`) never run there or right at boot; wait for boot, settle, then stagger work (light fast reads often, heavy snapshots hourly); no loop without a sleep; cap every file you grow. See references/bootloop.md.
5. **Lint + build.** `python3 -I scripts/lint_module.py DIR` then `python3 -I scripts/build_zip.py DIR --out OUT`. Fix every ERROR. The tool prints the status; never write a status yourself.
6. **Deliver** the zip + manifest, the one-line install steps, the rescue plan, and where the log appears. The rescue plan is mandatory and concrete: backup first, one module per reboot, the `disable` file path for this module, and what to do if it loops (wait for the guard, then recovery `disable`, never wipe data). See references/bootloop.md.
7. **Feedback loop.** User sends the log from `Documents/<id>/<id>-debug.log`. Run `python3 -I scripts/parse_report.py LOG --manifest MANIFEST`, read the ERROR/CHECK/AVC lines, fix, bump versionCode, rebuild. See references/logging.md. Bootloop triage: boots without `BOOT completed` mean the last `STAGE begin` is the suspect; fix the cause (move work later, settle, stagger, drop the bad prop/overlay), not the symptom.

## Mandatory logging (every module)
- Spool: `/data/adb/<id>-logs/<id>-debug.log` (rotates at 256 KB). Copy: `/sdcard/Documents/<id>/<id>-debug.log` only when storage is truly ready.
- Lines: `YYYY-MM-DD HH:MM:SS LEVEL [stage] message`. Content: SNAP device facts, STAGE markers, CHECK PASS/FAIL, HASH of every file, AVC denials, BOOT completed. No serials, accounts, or secrets.
- The lint rules LM030-LM034 enforce it. `--skip-log-policy` exists only for non-module use; do not use it for modules.
- Bootloop guard: 3 boots without finishing creates `disable`; the module turns itself off. A late-start timeout check (`bt_guard_check_timeout`, default 180 s without `sys.boot_completed=1`) also self-disables. The guard never reboots and never touches other modules.

## Bootloop protection (mandatory)
- **Avoid:** tiny post-fs-data, settle after boot, staggered light/heavy work, one untested module per reboot, canary first on a new device.
- **Detect:** unfinished-boot counter in post-fs-data, reset on `boot_completed`, plus the timeout check above. Patterns learned from YetAnotherBootloopProtector, AshLooper, abootloop and Bootloop-Protection.
- **Recover:** wait for the guard, then the recovery `disable` file, then re-enable one module at a time. Never wipe data, never run two protectors at once.
- Full playbook: references/bootloop.md. Read it before any high-risk module (props, overlays, sepolicy, native code, early-stage work).

## WebUI (when the module has one)
- Entry: `webroot/index.html`, self-contained, zero external URLs (no CDN, fonts, images). System fonts, inline SVG icons, viewport meta, correct `lang`/`dir`.
- Design follows Apple HIG principles (see references/webui.md): clear hierarchy, one accent color, grouped cards, tabular numbers, light+dark, 44 px touch targets, status near the content it describes.
- Live data via the manager JS bridge when present (`ksu.exec`, feature-detected), falling back to relative `fetch` of JSON files the service wrote. One read-only exec per poll, small `/proc`+`/sys` reads only, 500 ms default, paused while hidden. Polling never drives `service.sh` and never writes files.
- Always show freshness (last update + live/stale state). Device strings go in with `textContent`, never `innerHTML`. No secrets in the WebUI.
- Full rules: references/webui.md. Read it before writing any WebUI.

## Versioning
Each published update adds 0.1 to the previous version (3.1 -> 3.2 -> 3.3). Every update gets a CHANGELOG.md entry at the repo root, and the version strings in SKILL.md and AI.md move together.

## Status words (printed by tools only)
`PASS_STRUCTURAL` files look right | `PASS_SIMULATED` ran under dash in a sandbox | `PASS_PARTIAL` some proof missing | `PASS_REAL` log from a real phone whose hashes match the built zip, zero errors, checks pass | `NOT_TESTED` | `FAIL`. Without a user log, the best you may say is PASS_SIMULATED. Say "not tested on your phone" plainly.

## Facts that decide success
- Layout: zip root has `module.prop`, optional `customize.sh`, `post-fs-data.sh`, `service.sh`, `uninstall.sh`, `system/`, `sepolicy.rule`, `system.prop`, `action.sh`; plus `META-INF/com/google/android/{update-binary,updater-script}`.
- module.prop: id (`^[a-zA-Z][a-zA-Z0-9._-]+$`), name, version, versionCode (int), author, description.
- Stages: post-fs-data blocks (Magisk master: 40 s, script cap 35 s; older docs and KernelSU say 10 s - keep it tiny); service is non-blocking; KernelSU adds `boot-completed.sh`, `post-mount.sh`. Which exist on FinaSU is probed by the canary, not assumed.
- Details: references/anatomy.md, references/selinux-mounting.md, references/patterns.md.

## First run on a new device
Build the **canary** module (`--kind canary`), have the user install it with a rescue plan (references/device-testing.md), upload its log, and use the PROBE lines as device truth (tier T3).

## References (read when needed)
evidence.md, anatomy.md, logging.md, selinux-mounting.md, patterns.md, device-testing.md, compat.md, safety.md, bootloop.md, webui.md
