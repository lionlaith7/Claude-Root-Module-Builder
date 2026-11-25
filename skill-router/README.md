# skill-router

**Use the right skill for every task.**

When an agent has hundreds of skills installed, the failure mode is not
missing a skill — it is using the wrong one, stacking five conflicting
ones, or working from memory when a skill already encodes the answer.
`skill-router` is the small meta-skill that fixes that.

## What it does

1. **Classify** the task (domain, action, constraints).
2. **Search** the installed skill catalog with several phrasings — never
   conclude "no skill exists" from memory.
3. **Read** the top candidates' `SKILL.md` bodies, not just snippets.
4. **Pick** one primary skill plus at most two supporting ones, with clear
   precedence: user-named skill > domain skill > workflow skills.
5. **Follow** the picked skills; where they conflict with the user's
   instruction, the user wins; where they conflict with safety, safety wins.
6. **No fit?** Research first, solve, and save reusable workflows as new
   skills.

It also carries the delivery discipline its author uses: substantive
replies inside an `.md` file attachment, module files as plain `.zip`,
cloud-upload fallback with links when attachments fail.

## Install

```bash
npx skills add lionlaith7/Claude-Root-Module-Builder --skill skill-router
```

Or copy the `skill-router/` folder into your agent's skills directory.

## Version

v1.0.0 (2026-11-25). Written after installing 500+ skills from the major
public packs and learning that an unrouted catalog is just noise.

By Laith Harb ([lionlaith7](https://github.com/lionlaith7)), Jordan.
