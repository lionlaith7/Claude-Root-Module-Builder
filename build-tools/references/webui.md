# WebUI rules (Magisk / KernelSU)

A WebUI is `webroot/index.html` inside the module zip, opened in the manager
app's WebView. It is not a website. These rules keep it working offline, on
every manager, without hurting boot or battery.

## Structure

- Entry point is exactly `webroot/index.html`. CSS and JS are inline in that
  one file. No build step, no bundler output that needs a server.
- Self-contained: no external URLs at all. No CDN, no web fonts, no remote
  images, no analytics. The WebView may have no internet. Use system fonts
  and inline SVG/CSS for icons. Never use emoji as UI icons.
- Keep `index.html` small (under ~200 KB). Large data lives in JSON files
  the service writes, not in the HTML.
- Include `<meta name="viewport" content="width=device-width, initial-scale=1">`,
  correct `lang`/`dir` for the user's language, touch targets at least 44 px,
  and no hover-only controls. Support `prefers-color-scheme` when practical.

## Live data

- Prefer the manager JS bridge for live reads. KernelSU exposes
  `ksu.exec(cmd, options, callback)` with `callback(errno, stdout, stderr)`.
  Feature-detect it (`typeof ksu !== "undefined"`); never assume it exists.
- Fall back to relative `fetch("report.json")` of files the service wrote
  into `webroot/`. This is the Magisk path and the offline path.
- One exec per poll, reading only small `/proc` and `/sys` files
  (loadavg, meminfo, power_supply, thermal, cpufreq). No `pm`, `dumpsys`,
  `logcat` or package scans in a poll. Those belong in the hourly snapshot.
- Poll with `setInterval` at 250 ms or slower (500 ms is a good default).
  Pause when `document.hidden` (visibilitychange), resume when visible,
  and stop on unload. Never busy-loop, never `requestAnimationFrame` to poll.
  A user-facing speed selector (250/500/1000 ms) is fine; 250 ms is the floor.
- Thermal values from `/sys/class/thermal` need the same sanity filter as
  in patterns.md (plausible range, drop non-temperature zones) before
  charting — a raw max can be a voltage or a step value, not a temperature.
- WebUI polling is read-only and must not drive `service.sh`. The service
  keeps its own staggered light/heavy cycles (see bootloop.md) and capped
  history. Live charts keep their rolling buffer in JS memory only.
- Always show freshness: last-update time, a live/stale indicator, and a
  plain message when data is old or missing. A stale dashboard that looks
  live is a bug.

## Security and correctness

- No secrets in the WebUI, ever: no tokens, passwords, serials, accounts,
  or personal data. Same scope as the module itself.
- Put device strings in the DOM with `textContent`, never `innerHTML`.
  Device data is untrusted input. No `eval`, no `new Function`.
- Validate numbers before charting them. Missing sysfs files on some
  devices are normal: show a dash, do not crash, do not invent values.
- The WebUI never writes module files, never changes settings by itself,
  and never runs a command the user did not trigger or that is not a
  read-only status read.

## Compatibility

- Managers differ: KernelSU/KernelSU-Next (ksu bridge), Magisk (file
  serving, no ksu bridge), MMRL and forks in between. Test the fallback
  path, not only the bridge path.
- Simulation has no bridge and no Android sysfs. The WebUI must still load,
  show its empty states, and keep its charts from throwing.
- Real-device status (2026-11-25): SysDiag Lab v1.0.0 with a live-polling
  WebUI (250/500/1000 ms selector, bridge + file fallback) reached
  PASS_REAL on the FinaSU test device for its service/probe side. Whether
  the FinaSU manager's WebView exposes `ksu.exec` is still T4 until the
  user reports the in-WebUI bridge test result; the fallback path is the
  one proven by the log.
