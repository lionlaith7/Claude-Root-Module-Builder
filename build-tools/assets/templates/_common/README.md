# @NAME@

@DESC@

Made with build-tools (https://github.com/lionlaith7/Claude-Root-Module-Builder).

## Debug log / سجل التشخيص

This module writes a diary of everything it does.
هذه الوحدة تكتب سجلاً بكل ما تفعله.

- File / الملف: `/sdcard/Documents/@ID@/@ID@-debug.log`
- If the file is missing, wait until the phone finished booting, then reboot once. / إذا لم يظهر الملف انتظر اكتمال الإقلاع ثم أعد التشغيل مرة.
- To get a fix, send that file back. It contains device model, Android version, kernel, SELinux mode and the names of installed modules. It has no accounts, serial numbers or passwords. / لإصلاح أي مشكلة أرسل هذا الملف. لا يحوي حسابات ولا أرقاماً تسلسلية ولا كلمات مرور.
- Bootloop rescue / الإنقاذ: create an empty file named `disable` inside `/data/adb/modules/@ID@/` (from recovery or adb), then reboot.
