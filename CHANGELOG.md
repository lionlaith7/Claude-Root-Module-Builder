# Changelog

## 3.6.0
- Research-first step (workflow step 0): before any new feature, search for prior art (existing modules, skills, repos, manager docs), adopt patterns deliberately, and state what the research changed. Added at the skill author's request after the bootloop-protector and Apple-design research rounds proved the value.

## 3.5.0
- Visual identity for the repo: generated artwork in `assets/images/` (banner, workflow loop, SysDiag Lab WebUI in dark and light), embedded in the README so visitors see what the skill produces before reading a word. Images follow the same Apple HIG-informed tokens as the WebUI design (charcoal, one blue accent, no text baked into artwork).

## 3.4.0
- Repo presentation fixed: the GitHub About description described generic DevOps modules; it now describes what build-tools actually is (Android root modules for Magisk/KernelSU/FinaSU/APatch, debug logs, bootloop protection, Apple-style WebUI, every-agent support), and repo topics were added (magisk, kernelsu, android, root-module, claude-skill, ai-agent, agent-skills, webui, bootloop).
- README rewritten per Apple writing principles (purpose first, clear hierarchy, concise labels, just what is necessary): one-line purpose, install, use, what you get, testing status, safety, condensed history with a CHANGELOG link. English, Arabic and Chinese sections kept in sync.

## 3.3.0
- Multi-agent support: the skill follows the open Agent Skills format and now documents installation for every major agent. New repo-root `INSTALL.md` (skills CLI `npx skills add`, Claude Code, Claude.ai, Codex, Cursor, Windsurf, Gemini CLI/Antigravity, Muse, generic) and a repo-root `AGENTS.md` adapter pointing at `build-tools/SKILL.md`. README Install section rewritten accordingly (EN/AR/ZH kept in sync).
- Apple HIG-informed WebUI design: new design section in `references/webui.md` (eight design principles; type scale 34/22/17/15/13/12 with tabular numbers; one accent color; grouped-card tokens for light `#f2f2f7`/white and dark `#1c1c1e`/`#2c2c2e`; 44 px touch targets; tab bar and segmented controls; materials/translucency rules; chart and feedback guidance; accessibility and RTL), learned from Apple's Human Interface Guidelines via dickwu/apple-design-skill. The `--webui` starter template was redesigned to those tokens, and SysDiag Lab v1.2.0 ships the same design.
- Richer SKILL.md frontmatter description (folded, trigger-rich) for reliable agent activation.

## 3.2.0
- First real-device verification: SysDiag Lab v1.0.0 debug log from the test device (Redmi Note 10 Pro / sweet, Android 16, FinaSU ksud 1.7.0) analysed with parse_report.py: PASS_REAL, 12/12 CHECKs PASS, 0 errors. Device facts from that log are now T3 across compat.md, anatomy.md, logging.md, patterns.md, device-testing.md, selinux-mounting.md, bootloop.md, evidence.md and webui.md. No raw log published; aggregated facts only.
- Log-derived fixes and clarifications: all five boot stages confirmed on FinaSU (boot-completed and post-mount included); install-time env vars do not all survive to boot stages; script exec bit not required; SUSFS detected via kconfig, not /sys/fs/susfs; thermal zones need a plausible-range filter (some zones are levels/voltages, not temperatures); `wm` fails from a module service (use dumpsys display); /proc/cpuinfo may lack Hardware/model name; AVC log lines are system-wide and must be filtered by context before blaming a module; early-boot timestamps can predate time sync (order by uptime); a quick manual reboot after install spends guard budget (observed counter=2 on a healthy module); build fingerprint can be spoofed (trust ro.build.version.*).
- Versioning rule added: each published update adds 0.1 (3.1 -> 3.2 -> 3.3) with a changelog entry. AI.md test instructions corrected (no tests/ directory exists; test by scaffolding, linting, dash simulation and parse_report). evals updated for the now-known FinaSU facts.
- Tooling improvements from the same log: parse_report.py now splits AVC counts into system-wide vs module-context, and treats runtime-rewritten webroot data files as expected hash differences instead of a different build; lint_module.py gained LM035 (wm in a service), LM036/LM037/LM039 (WebUI external URLs, size, innerHTML) and LM038 (thermal reads without a plausible-range filter); new_module.py gained `--webui` with a compliant webroot starter; the service template gained boot-completed.sh that clears the guard at boot completion (canary marker does the same); new tests/test_all.py verifies the whole toolchain offline.

## 3.1.0
- Bootloop protection: new references/bootloop.md (avoid / detect / recover, learned from YetAnotherBootloopProtector, AshLooper, abootloop and Bootloop-Protection); mandatory bootloop-risk classification in the plan; guard.sh template gained a boot-start stamp, a 180 s boot-completed timeout self-disable and rescue info; service template gained a 10 s settle. Self-disable only: never disables other modules, never reboots.
- WebUI rules: new references/webui.md (self-contained index.html, zero external URLs, live reads via the manager JS bridge with file fallback, 500 ms polling paused while hidden, textContent only, freshness indicator) and a WebUI section in SKILL.md.

## 3.0.0
- Skill is now a folder `build-tools/` (name equals folder, per the Agent Skills spec); SKILL.md shortened, details moved to `references/`.
- New: mandatory debug log in every module (`dbg.sh`), copied to `Documents/<id>/` when storage is ready; bootloop guard (`guard.sh`).
- New tools: `new_module.py`, `lint_module.py`, `build_zip.py` (deterministic zip + sha256 manifest), `parse_report.py`.
- New templates: basic, service, props, canary.
- Tested offline only (structure and dash simulation). Not tested on a real device yet.
- Installer rewritten: staged, backs up, `--check`, `--uninstall`.

## 2.0
- Previous generic tool-building skill.
