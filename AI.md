# AI.md — build-tools

## Identity
- Name: build-tools (Claude skill)
- Version: 2.0
- Purpose: guide Claude to build small tools that work, are tested, and are documented.
- Platform: any (phone modules, scripts, CLIs, web pages).

## File map
- `SKILL.md`: the full instructions (rules, steps, code rules, docs set, phone module rules).
- `README.md`: GitHub guide (English) for this skill.
- `README.txt`: plain-text guide (English, Arabic, Chinese).
- `install.sh`: downloads SKILL.md, README.md, README.txt, AI.md into the Claude skills folder.

## Data flow
- Input: the user's request.
- Output: a tool folder with code, README.md, README.txt, AI.md, CHANGELOG.md, and a package.
- No state is stored by this skill.

## Invariants
- Do not ship a feature that has no passing test.
- Keep original credits; add the new developer's name.
- Never overwrite user files unless asked.

## How to test this skill
- `sh -n install.sh`
- Run `install.sh` with `CLAUDE_SKILLS_DIR` set to an empty folder; check the four files exist and are not empty.

## Signatures
- Skill: build-tools 2.0.
- Developer: Laith Harb, GitHub lionlaith7, Jordan.
- Models used in development: claude-sonnet-5-5, claude-haiku-5-5.
