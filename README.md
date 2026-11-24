# build-tools

**A Claude skill that builds Android root modules (Magisk, KernelSU, KernelSU-Next, FinaSU) for any idea, and makes every module write a debug log you can send back for fixing.**

Original skill by Laith Harb (https://github.com/lionlaith7) · Maintained by Laith Harb (lionlaith7), Jordan.

## What is new in 3.0
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
Tested offline: structure, lint, deterministic build, shell simulation (dash). **Not yet tested on a real device** (target: Redmi Note 10 Pro, Infinity X, FinaSU).

## Safety
No malware or spyware modules. Keep a rescue path: an empty `disable` file in `/data/adb/modules/<id>/`.

## Credits and license
See NOTICE.md (Magisk installer, GPL-3.0). This repository has no LICENSE file yet.

---
## العربية
مهارة لـ Claude تبني مديولات روت (Magisk / KernelSU / FinaSU) لأي فكرة. كل مديول يكتب سجل أخطاء في `Documents/<id>/<id>-debug.log` لترفعه إلى Claude للتحسين. فيها أدوات فحص وبناء وتحليل سجل، وقوالب (basic, service, props, canary)، وحماية من bootloop (بعد 3 إقلاعات فاشلة يتعطل المديول). الاختبار تم على الحاسوب بالمحاكاة فقط، ولم يُجرَّب على الهاتف بعد. الاسم الصحيح لمجلد المهارة: `build-tools`.

## 中文
这是一个 Claude 技能，可为任何想法构建 Android root 模块（Magisk / KernelSU / FinaSU）。每个模块都会把调试日志写到 `Documents/<id>/<id>-debug.log`，上传给 Claude 即可改进。包含检查、打包、日志分析工具，模板（basic、service、props、canary），以及防启动循环保护（3 次未完成启动后自动禁用）。目前仅在电脑上做了模拟测试，尚未在真机上测试。技能文件夹名必须是 `build-tools`。
