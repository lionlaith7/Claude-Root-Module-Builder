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

## Design (Apple HIG-informed)

Design language learned from Apple's Human Interface Guidelines (via dickwu/apple-design-skill). A module WebUI is a utility: purpose first, then craft.

Principles: **purpose** (the one job is obvious), **agency** (status is visible, actions are reversible), **responsibility** (transparent about what is collected; nothing leaves the device), **familiarity** (grouped cards, tab bar, system patterns), **flexibility** (light+dark, RTL, larger text), **simplicity** (every element earns its place), **craft** (alignment, spacing, wording), **delight** (calm confidence, not decoration).

Concrete tokens (CSS):
- Type scale (px ≈ pt): Large Title 34/700, Title 22/700, Headline 17/600, Body 17/400, Callout 16, Subheadline 15, Footnote 13, Caption 12. Never below 11. Avoid light weights (use 400/500/600/700). Numbers always `font-variant-numeric: tabular-nums`.
- Colors: one accent only (blue: `#007aff` light, `#0a84ff` dark). Backgrounds: light `#f2f2f7` grouped with white cards; dark `#1c1c1e` base (never pure black) with `#2c2c2e` cards and `#3a3a3c` separators. Text: primary `#1c1c1e`/`#ffffff`, secondary `#6e6e73`/`#98989f`. Semantic colors only for meaning (green ok, orange warn, red error), never decoration.
- Layout: 16 px side margins, 12-16 px card padding, 16-20 px card radius, hairline separators inside groups, safe-area insets (`env(safe-area-inset-*)`) for header/tab bar.
- Controls: touch targets ≥ 44×44 px; segmented control for 2-4 mutually exclusive choices; tab bar (3-5 tabs, icon + label, selected = accent) for top-level sections; primary button = filled accent, one per view.
- Materials: functional layer (header, tab bar) may use translucency (`backdrop-filter: blur`) over content; never apply glass to content cards, never stack glass on glass.
- Charts: label axes or values, don't rely on color alone, align chart edges with card edges, keep gridlines faint.
- Feedback: status (live/stale, last update) sits next to the data it describes; confirm significant actions; empty states say what to do next.
- Accessibility: contrast ≥ 4.5:1 for body text; respect `prefers-reduced-motion` and `prefers-color-scheme`; mirror layout in RTL (logical properties: margin-inline, inset-inline).
- Writing: labels say what happens ("Refresh now", not "OK"); sentence case; errors direct the user, never blame.

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
