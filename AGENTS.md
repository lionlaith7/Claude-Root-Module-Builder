# AGENTS.md

This repository contains two agent skills by Laith Harb:

- **build-tools** — an expert builder of Android root modules (Magisk, KernelSU, KernelSU-Next, FinaSU, APatch).
- **skill-router** — a meta-skill that picks and combines the right installed skills per task (classify → search the catalog → read candidates → one primary + at most two supporting), with precedence rules and catalog hygiene. See `skill-router/SKILL.md`.

For any root-module work (creating, scaffolding, linting, building, debugging or explaining a module, its boot scripts, system.prop, sepolicy, overlays, WebUI, canary probes, bootloop rescue, or a module debug log):

1. Follow `build-tools/SKILL.md` — it is the single source of truth for the workflow, rules and status words.
2. Load the reference files it names from `build-tools/references/` when the task touches them (bootloop, WebUI, logging, SELinux, device testing, compatibility, safety).
3. Use the tools in `build-tools/scripts/` (`new_module.py`, `lint_module.py`, `build_zip.py`, `parse_report.py`) instead of hand-writing module files. Verify the toolchain offline with `python3 -I build-tools/tests/test_all.py`.
4. Never claim a test status the tools did not print. `PASS_REAL` requires a real-device debug log whose hashes match the built zip.

Install instructions for Claude Code, Codex, Cursor, Windsurf, Gemini/Antigravity, Copilot and other agents: see `INSTALL.md`.
