build-tools 3.0 - Claude skill for Android root modules (Magisk / KernelSU / FinaSU)
By Laith Harb (lionlaith7), Jordan.

ENGLISH
- Builds a module for any idea. Every module writes a debug log:
  /sdcard/Documents/<id>/<id>-debug.log  (kept early in /data/adb/<id>-logs/)
- Send that log to Claude to improve the module.
- Tools in build-tools/scripts: new_module.py, lint_module.py, build_zip.py, parse_report.py
- Templates: basic, service, props, canary.
- After 3 unfinished boots the module disables itself (file "disable").
- Tested offline only (structure + shell simulation). Not tested on a real phone yet.
- Install: sh install.sh  (folder name must be build-tools)

العربية
- يبني مديول لأي فكرة. كل مديول يكتب سجل أخطاء في:
  /sdcard/Documents/<id>/<id>-debug.log  (ويُحفظ مبكرا في /data/adb/<id>-logs/)
- أرسل السجل إلى Claude لتحسين المديول.
- الأدوات في build-tools/scripts: new_module.py و lint_module.py و build_zip.py و parse_report.py
- القوالب: basic و service و props و canary.
- بعد 3 إقلاعات غير مكتملة يعطل المديول نفسه (ملف disable).
- الاختبار تم على الحاسوب فقط (بنية + محاكاة). لم يُجرَّب على الهاتف بعد.
- التثبيت: sh install.sh (اسم المجلد يجب أن يكون build-tools)

中文
- 可为任何想法构建模块。每个模块都会写调试日志：
  /sdcard/Documents/<id>/<id>-debug.log（启动早期保存在 /data/adb/<id>-logs/）
- 把日志发给 Claude 即可改进模块。
- 工具位于 build-tools/scripts：new_module.py、lint_module.py、build_zip.py、parse_report.py
- 模板：basic、service、props、canary。
- 3 次未完成启动后模块自动禁用（文件 disable）。
- 仅在电脑上做了测试（结构 + 模拟），尚未在真机上测试。
- 安装：sh install.sh（文件夹名必须为 build-tools）
