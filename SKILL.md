---
name: build-tools
description: Use when creating or improving any tool or app idea, online or offline, including Magisk/KernelSU modules, scripts, CLIs, and web tools. Enforces working tested output, readable code, a GitHub README, a machine-readable AI.md, a human README.txt, trilingual docs, and developer credits.
---

# Build Tools

Goal: a tool that works. No padding, no untested features.

## Rules
1. **Works 100% or is not shipped.** Every feature needs a test that ran. Drop untestable features and list them, with the reason, in the final message.
2. **Minimal tokens.** Read only needed line ranges (grep first). Never reprint whole files. Summarize test output as counts plus failing names.
3. **Credit everyone.** Keep the original developer's name and link, then add the new one. Format: `Original by <name> (<link>) · Enhanced by <name> (<username>)`. Check the original license before reusing code.
4. **Start immediately.** Choose sensible defaults. Ask only when a wrong guess is costly and irreversible.

## Steps
1. **Classify:** offline or online; platform (Android module, web page, CLI, script).
2. **Define done:** one-sentence goal plus checkable acceptance criteria.
3. **Build the smallest working version,** then add features one at a time, each with its test.
4. **Test in a sandbox that mirrors the real environment:**
   - Shell: run under `dash` and `bash --posix`; `sh -n` every script; use fixtures with awkward names (spaces, Arabic, quotes, long names).
   - Web: drive the page with Playwright; mock native bridges.
   - Package: unpack the final archive, run it on a copy, check permissions and executable bits.
   - Remove sandbox paths afterward.
5. **Deliver** the package plus the docs below, and a final message: what works, what was dropped and why, test counts.

## Code organization (readable by developers, AI models, and children)
- One responsibility per file. Keep files under about 400 lines; split otherwise.
- Header comment on every file: `# File: <name>`, `# Purpose: <one sentence>`, `# Kid note: <one simple sentence, like explaining to a 10-year-old>`.
- Name functions as verbs (`move_item`, `check_power`). Name variables for their content, never single letters except loop counters.
- One short comment above each non-obvious block: say why, not what.
- Put constants and paths at the top of the file, in one place.
- Keep a single entry point; other files only provide functions.
- No dead code, no commented-out blocks, no unused variables.

## Docs set (required for every shipped tool)
| File | Audience | Language | Content |
|---|---|---|---|
| `README.md` | GitHub visitors | English, Arabic, Chinese in sections | Description, install, usage, config table, limits, credits, license |
| `README.txt` | Humans on the device | English, Arabic, Chinese in sections | Plain-text version of the README, no markdown, short sentences |
| `AI.md` | AI models | Any (English preferred) | Machine-oriented map of the tool; see below |
| `CHANGELOG.md` | Everyone | English | Only tested changes |

Keep each language equivalent in meaning. Do not make one language longer than the others.

### AI.md (for models, not people)
Write it so a model can understand and modify the tool without reading every file. Include:
- **Identity:** name, version, purpose in one sentence, platform, online or offline.
- **File map:** each file with its role and the functions it defines.
- **Data flow:** inputs, outputs, where state lives (config, status, logs, journals).
- **Invariants:** rules the code must never break (for example, never overwrite a user file).
- **Entry points and how to test.**
- **Signatures:**
  - Skill used: `build-tools` (version).
  - Models used in development: list each model ID actually used.
  - Developer: name, username, country.
  - Original developer and link, if any.

## README and docs rules
- No marketing text. Install and usage first.
- Every number in the docs (defaults, limits) must match the code. Verify before shipping.

## Magisk / KernelSU specifics
- `module.prop` with a `versionCode` that increases every release.
- `META-INF/com/google/android/update-binary` and `updater-script` (content `#MAGISK`) so it installs on both managers.
- POSIX `sh` only: no `[[`, arrays, `local`, `awk`, or GNU-only flags.
- Never write to an unmounted storage stub; compare the device number against `/storage`.
- Never overwrite user files. Never delete user data unless explicitly asked.
- Config is shell-sourced: validate with `sh -n`, fall back to `.bak`, then defaults. Quote values and escape `\ " $` and backtick.
- Background service: single instance (pid file), wait for `sys.boot_completed`, re-read config each cycle, exit cleanly on kill.
- WebUI: support both `ksu.exec` signatures and Promise returns. Keep i18n keys identical across languages, checked by test.

## Offline vs online
- Offline: no network calls; state that in the README.
- Online: list every domain contacted and what data is sent. Make network use optional where possible. Never send personal data.

## Extra quality features
- **Version bump rule:** every shipped change bumps the version in all places (module.prop, docs, CHANGELOG). A test checks that they match.
- **Self-check command:** every tool offers a `selftest` (or equivalent) that reports OK, WARN, or FAIL lines.
- **Undo for anything that moves or deletes user data.**
- **Dry-run mode** for any action that changes files.
- **Log lines** start with a level (`INFO`, `WARN`, `ERROR`) so they can be filtered.

## Final message
Short. Lead with the deliverable. Then: tests passed (counts), features dropped and why, and one next step only if it matters.
