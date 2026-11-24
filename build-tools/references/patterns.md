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
