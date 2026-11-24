# Changelog

## 3.0.0
- Skill is now a folder `build-tools/` (name equals folder, per the Agent Skills spec); SKILL.md shortened, details moved to `references/`.
- New: mandatory debug log in every module (`dbg.sh`), copied to `Documents/<id>/` when storage is ready; bootloop guard (`guard.sh`).
- New tools: `new_module.py`, `lint_module.py`, `build_zip.py` (deterministic zip + sha256 manifest), `parse_report.py`.
- New templates: basic, service, props, canary.
- Tested offline only (structure and dash simulation). Not tested on a real device yet.
- Installer rewritten: staged, backs up, `--check`, `--uninstall`.

## 2.0
- Previous generic tool-building skill.
