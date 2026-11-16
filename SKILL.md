---
name: build-tools
description: Builds a small tool, app or script that really works, then tests it before sharing. For phone modules (Magisk, KernelSU), scripts, command tools and web pages. Adds a simple README, AI notes and credits.
---

# build-tools

Goal: a tool that works. Nothing extra, nothing untested.

## Four rules
1. **Works, or it is not shipped.** Every feature gets a test that really runs. If a feature cannot be tested, leave it out and say why.
2. **Short and clear.** Read only the lines you need. Show test results as counts and failing names only.
3. **Give credit.** Keep the original maker's name and link, then add the new maker. Format: `Original by <name> (<link>) · Enhanced by <name> (<username>)`. Check the license before reusing code.
4. **Start now.** Pick sensible defaults. Ask only when a wrong guess is costly and cannot be undone.

## Steps
1. **Pick the kind:** online or offline; phone module, web page, command tool or script.
2. **Say what done means:** one sentence, plus checks you can run.
3. **Build the smallest version that works.** Add one feature at a time, each with a test.
4. **Test in a copy of the real setup:**
   - Shell scripts: run with `sh` and `bash --posix`; run `sh -n` on each file; use file names with spaces, Arabic, quotes and long names.
   - Web pages: open them in Playwright; fake the phone bridge.
   - Package: unzip the final file somewhere new, check permissions, run it on a copy.
   - Delete sandbox files afterward.
5. **Share** the package, the docs below, and a short final message: what works, what was left out and why, and test counts.

## Code rules (for people, AI and children)
- One job per file. Keep files under about 400 lines.
- Start each file with three lines: `File:` (name), `Purpose:` (one sentence), `Kid note:` (one simple sentence, as if for a 10-year-old).
- Name functions with a verb (`move_item`, `check_power`). Name variables by what they hold.
- Add a short comment above each tricky part, saying *why*, not *what*.
- Keep settings and paths at the top of each file.
- No dead code, no commented-out blocks, no unused variables.

## Docs to ship
| File | For | Language | What it has |
|---|---|---|---|
| `README.md` | GitHub visitors | English, Arabic, Chinese | What it is, install, use, settings table, limits, credits, license |
| `README.txt` | People on the device | English, Arabic, Chinese | Same as README, plain text, short sentences |
| `AI.md` | AI models | English | Map of the files, data flow, rules that must not break, how to test, signatures |
| `CHANGELOG.md` | Everyone | English | Only changes that were tested |

Each language says the same thing. Do not let one language be much longer than the others.

### AI.md
Let a model change the tool without reading every file. Include: identity, file map with functions, data flow, invariants, test commands, and signatures (skill name and version, models used with exact IDs, developer name, username and country, original developer and link).

## Phone module specifics (Magisk / KernelSU)
- `module.prop` has a `versionCode` that goes up every release.
- Provide both `META-INF/com/google/android/update-binary` and `updater-script` (containing `#MAGISK`) so both managers install it.
- Use plain `sh` only: no `[[`, arrays, `local`, or GNU-only flags.
- Never write to an unmounted storage folder. Check the device number against `/storage`.
- Never overwrite or delete user files unless asked.
- Settings are read as data, validated, with a backup and defaults as fallback.
- Background service: one instance only (pid file), wait for `sys.boot_completed`, re-read settings each cycle.

## Other rules
- **Offline tools** make no network calls. Say so in the README.
- **Online tools** list every site they contact and what data they send. Never send personal data.
- **Every release** bumps the version everywhere, and a test checks that they match.
- **Every tool** has a `selftest` command that prints OK, WARN or FAIL lines.
- **Anything that moves files** needs Undo and a dry-run mode.
- **Log lines** start with `INFO`, `WARN` or `ERROR`.
- **Docs numbers** (defaults, limits) must match the code. Check them before shipping.

## Final message
Short. Lead with the file. Then: test counts, what was left out and why, and one next step only if it matters.
