# Unified design system for module WebUIs

One design language, three sources, merged deliberately (2026-11-25):

- **FinaSU manager theme** — the look the skill's test device uses and the
  user approved on real modules: deep navy gradient, pink accent, rounded
  cards, bottom tab bar with badges, banner-backed module cards, pill
  buttons, pink switches. This is the **default dark theme**.
- **Apple HIG** (via dickwu/apple-design-skill) — principles and craft:
  purpose, agency, responsibility, familiarity, flexibility, simplicity,
  craft, delight; grouped cards, materials rules, type discipline,
  accessibility, RTL, writing.
- **Material Design 3** (via wshobson/agents mobile-android-design) —
  the Android-native system: color roles, type scale, shape scale,
  tonal elevation, navigation bar, segmented buttons, switches, motion.

Rule of the merge: **M3 supplies the role names and component anatomy,
Apple supplies the principles and restraint, FinaSU supplies the default
palette and personality.** When they conflict, Android wins on anatomy
(the WebUI runs on Android), Apple wins on restraint (one accent, no
decoration without meaning), FinaSU wins on color.

## Color tokens

Name every color by its M3 role; assign values per theme. CSS variables
in the starter template use exactly these names.

| Role | FinaSU dark (default) | Light | Meaning |
|---|---|---|---|
| `primary` | `#ff4d7e` | `#d81b60` | the one accent: primary actions, selected states |
| `on-primary` | `#ffffff` | `#ffffff` | text/icons on primary |
| `primary-container` | `#3d1f3a` | `#ffd9e4` | tonal fills: selected tab pill, chips |
| `on-primary-container` | `#ffb3c9` | `#5c0a2e` | text on primary-container |
| `background` | gradient `#0a0f24 → #121a3d → #1a1030` | `#f2f2f7` | page background (fixed, never repaints) |
| `surface` | `#171f45` | `#ffffff` | cards |
| `surface-variant` | `#1e2856` | `#e9e9f2` | inner tiles, inputs, ghost buttons |
| `on-surface` | `#f5f0f4` | `#1c1c1e` | primary text |
| `on-surface-variant` | `#b9a8c9` | `#6e6e73` | secondary text, labels |
| `outline` | `rgba(255,255,255,.08)` | `rgba(60,60,67,.18)` | hairlines, card borders |
| `error` | `#ff453a` | `#d70015` | destructive only |
| `success` (extended) | `#30d158` | `#248a3d` | ok states, enabled dots |
| `warning` (extended) | `#ff9f0a` | `#b25f00` | caution states |

Rules:
- **One accent.** `primary` is the only decorative color. Semantic
  colors (success/warning/error) carry meaning only — never decoration,
  never as the sole signal (pair with text or icon).
- Dark is the default theme (the manager is dark); light follows
  `prefers-color-scheme: light`. Never pure black backgrounds; layered
  navy/grays instead (Apple dark-mode rule, M3 tonal elevation).
- Contrast ≥ 4.5:1 for body text in both themes.
- No dynamic color in a WebView — the scheme is fixed by these tokens.

## Typography

Unified scale (px ≈ pt ≈ sp). Apple names left, M3 names right — use
either, the sizes are the same system.

| Size/weight | Apple | M3 | Use |
|---|---|---|---|
| 34/700 | Large Title | headlineLarge+ | screen title |
| 22/700 | Title | titleLarge | section titles |
| 17/600 | Headline | titleMedium (16) | card titles |
| 17/400 | Body | bodyLarge (16) | main text |
| 15/400 | Subheadline | bodyMedium (14) | secondary text |
| 13/400 | Footnote | bodySmall (12) | notes, freshness |
| 12/500 | Caption | labelMedium | tab labels, badges |

- Never below 11 px. Weights 400/500/600/700 only (no light weights).
- Numbers always `font-variant-numeric: tabular-nums` — live values must
  not jitter as digits change.
- System fonts only: `-apple-system, "Segoe UI", Roboto, "Noto Sans Arabic", sans-serif`.
- Sentence case labels; labels say what happens ("Sort now", not "OK").

## Shape and elevation

M3 shape scale, Apple card radius:

- extraSmall 4 px — chips, badges
- small 8 px — inputs, small tiles
- medium 12 px — buttons' inner radius, list rows
- large 16–20 px — cards (the FinaSU look uses 18 px)
- extraLarge 28 px — sheets, hero cards
- full (999 px) — pill buttons, switches, segmented control

Elevation is **tonal**, not shadowy: higher surfaces get lighter
(`surface` → `surface-variant`), shadows stay near-invisible. Cards get a
hairline `outline` border instead of a drop shadow.

## Components

- **Navigation bar** (M3) = **tab bar** (Apple): bottom, 3–6 destinations,
  icon + label, selected = `primary` with a `primary-container` pill
  behind the icon. Count badges (M3) on destinations that have a count.
  Translucency (`backdrop-filter: blur`) allowed here and on the header
  only — never on content cards, never stacked (Apple materials rule).
  Respect `env(safe-area-inset-bottom)`.
- **Cards**: grouped content in `surface` cards, 16 px side margins,
  14–16 px padding, hairline separators between rows inside a card.
- **Banner cards** (FinaSU): a module with a `banner=` image gets a card
  whose top area is the banner (aspect ≈ 3:1, `object-fit: cover`), name
  and actions overlaid on a scrim. Banner artwork: 1280×426 px, no text
  baked into the image, ≤ 3 MB.
- **Buttons**: one filled `primary` button per view (the main action);
  `surface-variant` tonal buttons for secondary actions; text buttons for
  tertiary. Pill shape, min-height 44 px (48 px preferred, M3 target).
- **Segmented control** (Apple) = **segmented buttons** (M3): 2–4 mutually
  exclusive choices (poll speed, mode), selected segment filled.
- **Switches**: M3 switch anatomy, `primary` track when on. Always pair
  with a text label; state must not rely on color alone.
- **Stat tiles**: big tabular number + caption label, in
  `surface-variant` tiles inside a card (battery %, counts).
- **Search field**: `surface-variant`, pill or 12 px radius, filters the
  list below it live.
- **List rows**: title + subtitle + trailing control (switch/chevron),
  48 px min height, hairline between rows.
- **Charts** (canvas): label values or axes, faint gridlines
  (`rgba(128,128,128,.3)`), series colors from semantic palette
  (blue `#0a84ff`, green `#30d158`, orange `#ff9f0a` in dark), never
  color alone. Cap stored points (e.g. 60 s rolling window).
- **Status/freshness**: always next to the data it describes — last
  update time + live/file mode. Empty states say what to do next.

## Motion and smoothness (performance is a design rule)

The user feels jank as brokenness. Budgets:

- Animate only `transform` and `opacity`. Never animate layout
  (width/height/top/margin) in a live view.
- Durations: 150–250 ms for state changes, M3 standard easing
  `cubic-bezier(.2,0,0,1)`. Respect `prefers-reduced-motion`.
- **Render in place**: update text nodes and attributes of existing DOM;
  rebuild a list only when its data actually changed (compare a cheap
  signature first). Rebuilding the whole list every poll is the classic
  WebUI jank source.
- **Canvas**: redraw at most once per poll tick, cap points, no
  gradients/shadows inside the draw loop.
- **backdrop-filter** only on the two bars, never on scrolling cards.
- Background gradient is `position: fixed` (or on body) so scrolling
  never repaints it.
- Poll tiers: bridge live reads 100–1000 ms (default 250–500 ms, one
  small exec per poll); file fallback 1–2 s; pause all polling while
  `document.hidden`. Service cadence tiers: settle after boot, light
  reads often, heavy snapshot hourly — the UI must never make the
  service work harder.
- index.html stays under ~200 KB (lint LM037); banner images ≤ 3 MB;
  JSON files the service writes stay small (cap arrays, rotate logs).

## Layout, RTL, accessibility

- 16 px side margins; content max-width ~640 px centered on wide screens.
- RTL: use logical properties everywhere (`margin-inline`,
  `inset-inline-start`, `text-align: start/end`); mirror the tab bar and
  switches; keep numbers and paths LTR with `dir="ltr"` on those fields.
- Touch targets ≥ 44×44 px (48 preferred). Focus visible. Every control
  has a text label or `aria-label`.
- Never rely on color alone for state (enabled = dot + word, or switch
  position + label).

## Writing (Apple)

- Purpose first: the screen title says what this page does.
- Labels name the action and its object ("Install from repo", "Sort now").
- Errors direct the user to the fix, never blame ("No list yet — tap
  Refresh list").
- Honest limits in plain words, next to the feature they limit.

## Where this is implemented

- `assets/templates/webroot-starter/` ships these tokens (FinaSU dark
  default + light scheme) — start every WebUI from it.
- Proven on device: HotMod v2 (6-tab FinaSU-style manager UI),
  SysDiag Lab v2 (live dashboard), Sortify v9 (settings + actions),
  all on the FinaSU test device, 2026-11-25.
