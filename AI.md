# AI.md — build-tools (skill)

Identity: build-tools, a skill for building tools and apps (online or offline) with tested, documented, readable output.
Platform: any agent that loads SKILL.md. Offline: no network calls by the skill itself.

## Files
- SKILL.md: the full instructions (rules, steps, docs set, quality features). Read this first.
- README.md: GitHub-facing docs (English, Arabic, Chinese).
- README.txt: plain-text docs for people (English, Arabic, Chinese).
- AI.md: this file.

## Invariants
- A feature ships only if its test ran and passed.
- Credits keep the original developer and add the new one.
- Versions match across module.prop, docs, and CHANGELOG.

## Signatures
- Skill: build-tools, version 1.1.
- Models used in development: claude-sonnet-5-5 (main build), claude-haiku-5-5 (later revisions).
- Skill developer: Laith Harb, username lionlaith7, Jordan.
- Original developer: none for this skill.
