# build-tools

**A Claude skill that builds Android root modules (Magisk, KernelSU, KernelSU-Next, FinaSU) for any idea, and makes every module write a debug log you can send back for fixing.**

Original skill by Laith Harb (https://github.com/lionlaith7) · Maintained by Laith Harb (lionlaith7), Jordan.

## What is new in 3.2
- **Tested on a real device:** SysDiag Lab v1.0.0 log from the test device (Redmi Note 10 Pro / sweet, Android 16, FinaSU ksud 1.7.0) reached `PASS_REAL` (12/12 checks PASS, 0 errors). Device facts from that log are documented as T3 in `build-tools/references/compat.md`.
- Bootloop protection playbook (`references/bootloop.md`): avoid / detect / recover, guard timeout, self-disable only.
- WebUI rules (`references/webui.md`): self-contained `webroot/index.html`, zero external URLs, live bridge reads with file fallback, 250 ms polling floor.
- Log-derived corrections: all five boot stages confirmed on FinaSU; thermal zones need a plausible-range filter; `wm` fails from a module service; AVC lines are system-wide (filter by context); early-boot timestamps can predate time sync; quick reboots spend guard budget; fingerprints can be spoofed.
- Versioning: each published update adds 0.1 (3.1 -> 3.2 -> 3.3), with a CHANGELOG.md entry.

## What was new in 3.0
- Specialised in root modules; the module's job can be anything.
- **Debug log in every module:** `/sdcard/Documents/<id>/<id>-debug.log` (spooled in `/data/adb/<id>-logs/` early in boot). Upload it to Claude to improve the module.
- Tools: `new_module.py` (scaffold), `lint_module.py` (rules), `build_zip.py` (same input = same zip, plus sha256 manifest), `parse_report.py` (reads the log, prints the status).
- Templates: `basic`, `service`, `props`, `canary` (read-only probe that documents what your phone supports).
- Bootloop guard: after 3 unfinished boots the module disables itself.
- Honest statuses: `PASS_STRUCTURAL`, `PASS_SIMULATED`, `PASS_PARTIAL`, `PASS_REAL`, `NOT_TESTED`, `FAIL`. Only a log from a real phone whose hashes match the zip gives `PASS_REAL`.

## Install
```sh
git clone https://github.com/lionlaith7/Claude-Root-Module-Builder
sh Claude-Root-Module-Builder/install.sh      # --check, --uninstall, --ref, --sha256 available
```
Or zip the `build-tools/` folder (the folder name must stay `build-tools`) and upload it as a skill.

## Use
Ask Claude: "Build a KernelSU module that ...". Install the zip, reboot, then send `Documents/<id>/<id>-debug.log` back.
First time on a new phone: ask for the **canary** module and send its log.

## Status of testing
Tested offline: structure, lint, deterministic build, shell simulation (dash). **Tested on a real device** (2026-11-25): Redmi Note 10 Pro (sweet), Android 16, FinaSU — SysDiag Lab v1.0.0 reached `PASS_REAL` via its debug log. Other devices still start with the canary.

## Safety
No malware or spyware modules. Keep a rescue path: an empty `disable` file in `/data/adb/modules/<id>/`.

## Credits and license
See NOTICE.md (Magisk installer, GPL-3.0). This repository has no LICENSE file yet.

---
## العربية
مهارة لـ Claude تبني مديولات روت (Magisk / KernelSU / FinaSU) لأي فكرة. كل مديول يكتب سجل أخطاء في `Documents/<id>/<id>-debug.log` لترفعه إلى Claude للتحسين. فيها أدوات فحص وبناء وتحليل سجل، وقوالب (basic, service, props, canary)، وحماية من bootloop (بعد 3 إقلاعات فاشلة يتعطل المديول). تم الاختبار على هاتف حقيقي (Redmi Note 10 Pro، FinaSU) ووصلت وحدة SysDiag Lab إلى PASS_REAL. الاسم الصحيح لمجلد المهارة: `build-tools`.

## 中文
这是一个 Claude 技能，可为任何想法构建 Android root 模块（Magisk / KernelSU / FinaSU）。每个模块都会把调试日志写到 `Documents/<id>/<id>-debug.log`，上传给 Claude 即可改进。包含检查、打包、日志分析工具，模板（basic、service、props、canary），以及防启动循环保护（3 次未完成启动后自动禁用）。已在真机上测试（Redmi Note 10 Pro、FinaSU），SysDiag Lab 达到了 PASS_REAL。技能文件夹名必须是 `build-tools`。
