# Patterns by module category (start from the matching template)

| Idea | Kind | Notes |
|---|---|---|
| Change system properties | props | system.prop + props.list check after boot |
| One-time tweak (sysfs/proc write, setting) | basic | write, then dbg_check the value read back |
| Background watcher/loop | service | lock dir, pid check, validated config, sleep interval 10-3600 s |
| File replacement/overlay | basic | files under `system/`; verify with `ls`/`cmp` check |
| Learn what the device supports | canary | read-only probes, upload log |
| Zygisk/native hooks | (not templated) | needs a native build; ask first, test only with a rescue path |

General rules
- Always read a value back after writing it and log a CHECK.
- Config is data: parse `key=value` with grep/cut, never `source` a user-editable file.
- Validate numbers (`case ... *[!0-9]*`), clamp ranges, quote variables.
- Prefer `service.sh`. In post-fs-data do only what must precede mounting.
- Use `BT_ONCE=1` to run a loop template once in simulation.
- Bootloop avoidance: settle after boot before heavy work, stagger light and heavy cycles, cap every file you grow, one untested module per reboot. See bootloop.md.
- Thermal zones are not all temperatures (T3, 2026-11-25): on the test device some `thermal_zone*/temp` values are levels, steps or voltages (observed `soc`=274, `vbat`=4085 mV, negative step values). Convert millidegrees, then keep only plausible temperatures (about 0–120 °C) and drop zone types ending in `-lvl*`, `-step`, `-bcl*`, `-vph*`, `-ibat*`, `-vbat*` before taking a max or charting.
- `wm size` / `wm density` can fail from a module service (T3: "Failure calling service window"). Use `dumpsys display` (filtered) or the density prop instead.
- `/proc/cpuinfo` may have no Hardware/model name lines (T3 on this kernel). Identify the SoC from `ro.soc.model` / `ro.board.platform` props.
- Shell on the test device is BusyBox ash standalone: arrays=no, but `[[ ]]`, `${x//}`, `local`, arithmetic, printf and case all work (T3). Templates still stay POSIX so they run everywhere.
- Hot install / live apply (research 2026-11-25): KernelSU-family managers support official hot install — a module declares `MODULE_HOT_INSTALL_REQUEST=true` and optionally `MODULE_HOT_RUN_SCRIPT=<script>` in customize.sh, and the manager applies it without a reboot (script runs in the global mount namespace, ~30 s budget). For a container/loader module that applies other modules live: props via `resetprop` (save old values first, restore on disable), run `service.sh`/`boot-completed.sh`/`post-mount.sh` immediately, `sepolicy.rule` live only when `magiskpolicy` exists, `system/` files only via tracked bind mounts behind an explicit config flag (default off), Zygisk/native code never hot-loads (needs a soft reboot / zygote restart). Re-apply enabled modules after every boot from the loader's own service. Guard zip extraction against path escapes (check entry names for `../` or absolute paths before unzipping). Proven on the FinaSU test device 2026-11-25 (HotMod: scan/install/list via Action log).
