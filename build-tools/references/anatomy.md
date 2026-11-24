# Module anatomy (T1: Magisk docs, module_installer.sh)

```
<id>.zip
  module.prop            id name version versionCode author description (LF endings)
  customize.sh           sourced by the installer: use abort, never exit
  post-fs-data.sh        blocking, early; resetprop -n only
  service.sh             non-blocking, after boot starts (preferred)
  uninstall.sh           runs on removal
  system/ ...            files overlaid onto /system (Magic Mount / overlay)
  system.prop            properties (name=value) loaded by the manager
  sepolicy.rule          extra SELinux rules (one per line)
  action.sh              Action button (newer managers)
  META-INF/com/google/android/update-binary   = official module_installer.sh, unchanged
  META-INF/com/google/android/updater-script  = #MAGISK
```
- Scripts run in BusyBox ash standalone mode. Use `MODDIR=${0%/*}`, never a hardcoded `/data/adb/modules/<id>`.
- No `install.sh` in new modules (legacy). No logic in update-binary.
- Replace/remove system files: `.replace` marker in a folder, whiteout (char device 0:0) for deletion; prefer adding over replacing.
- Install variables inside customize.sh: `MODPATH`, `TMPDIR`, `ZIPFILE`, `BOOTMODE`, `MAGISK_VER_CODE`, `API`, `ARCH`; under KernelSU also `KSU`, `KSU_VER_CODE` (`MAGISK_VER_CODE` is fixed at 25200 there).
- `set_perm_recursive "$MODPATH" 0 0 0755 0644` after copying.
- Boot timing: post-fs-data blocks the boot (Magisk master docs: 40 s, scripts capped at 35 s; older docs/KernelSU official: 10 s). `setprop` there can deadlock: use `resetprop -n`.
- Extras on KernelSU official: `boot-completed.sh`, `post-mount.sh`, metamodules. Metamodules do NOT apply to FinaSU (built-in Magic Mount). Treat all of these as T4 on FinaSU until the canary shows the stage lines.
