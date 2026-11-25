# Device testing and rescue

Before the first flash
1. Backup of boot/data the user cares about; know how to reach recovery or adb from a PC.
2. Rescue facts: create an empty file named `disable` in `/data/adb/modules/<id>/` (from recovery/adb shell with root, or a root file manager) to switch a module off. The bootloop guard does this automatically after 3 unfinished boots, or after 180 s without boot completing. Do not assume FinaSU has a safe mode (T4). Full before/during/after playbook: bootloop.md. Never wipe data for a module bootloop, and never run two bootloop protectors at once.
3. Install the **canary** zip first, reboot, wait, then open `Documents/<id>/<id>-debug.log` and send it.

Interpreting results: see logging.md. Record each device fact as T3 with the date.

Simulation (sandbox, no phone)
`DBG_FORCE_READY=1 BT_ONCE=1 DBG_INT_DIR=/tmp/x/int DBG_DOCS_DIR=/tmp/x/docs dash /abs/path/service.sh`
Run with an absolute path (MODDIR comes from `$0`). The log says `sim=1`, so the best status is PASS_SIMULATED.
