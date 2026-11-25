# AI.md - build-tools

## Identity
- Name: build-tools (Claude skill), version 3.1.0
- Purpose: build, lint, package and debug Android root modules (Magisk, KernelSU, KernelSU-Next, FinaSU) for any idea. Every module writes a debug log to Documents.
- Folder name must equal the skill name: `build-tools`.

## File map
- `SKILL.md`: short instructions (workflow, rules, statuses).
- `references/`: evidence, anatomy, logging, selinux-mounting, patterns, device-testing, compat, safety, bootloop, webui.
- `scripts/`: `new_module.py`, `lint_module.py`, `build_zip.py`, `parse_report.py` (Python 3 stdlib only; run with `python3 -I`).
- `assets/templates/`: `_common` (dbg.sh, guard.sh, customize.sh, uninstall.sh, module.prop, official update-binary) plus kinds basic, service, props, canary.
- `evals/evals.json`: test prompts with expectations.

## Data flow
request -> scaffold -> edit YOUR WORK block -> lint -> build zip + manifest -> user installs -> log in Documents/<id>/ -> parse_report -> fix.

## Invariants
- Status words are printed by tools; never typed by the model.
- Offline tests give PASS_SIMULATED at most; PASS_REAL needs a device log whose hashes match the manifest.
- update-binary is the unmodified Magisk module_installer.sh.
- Logs never contain secrets. No malware/spyware modules.
- Never overwrite user files; back up first.

## How to test
`python3 -I tests/test_all.py` (needs dash or sh).

## Signatures
- Skill: build-tools 3.1.0. Developer: Laith Harb, GitHub lionlaith7, Jordan.
- Models used in development: claude-sonnet-5-5, claude-haiku-5-5.
