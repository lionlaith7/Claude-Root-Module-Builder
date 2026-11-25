---
name: skill-router
description: >
  Choose and combine the right installed skills for each task, intelligently.
  Use at the start of any non-trivial task when many skills are installed:
  classify the task, search the installed skill catalog, read the best
  candidates, pick one primary skill (plus at most two supporting ones),
  and follow them. Also governs reply delivery: substantive replies go
  inside an .md file attachment. Triggers: "which skill", "use your skills",
  "استعمل مهاراتك", "أي مهارة", any task where a specialised skill might exist.
---

# skill-router v1.0.0 - use the right skill for every task

With hundreds of skills installed, the failure mode is not missing a skill —
it is using the wrong one, stacking five conflicting ones, or working from
memory when a skill already encodes the answer. This skill is the router.

## The routing workflow (every non-trivial task)

1. **Classify the task** in one line: domain (root modules, web UI, writing,
   research, marketing, science, DevOps...), action (build, fix, review,
   explain, install), and constraints the user set.
2. **Search the catalog** before starting: `muse.skill_search` with 2-3
   phrasings (one close to the user's words, one with the domain terms, one
   with the tool/product names). Also `muse.connector_search` when the task
   touches a service. Never conclude "no skill exists" from memory.
3. **Read the top candidates' `SKILL.md`** (not just the search snippet).
   A skill whose description matches but whose body is stale, generic, or
   for a different stack is not a match.
4. **Pick one primary skill** — the most specific one that fits — and at
   most two supporting skills (e.g. a domain skill + a workflow skill).
   State the pick briefly to the user when it shapes the work.
5. **Follow the picked skills** for their domain: their templates, tools,
   checklists and status words beat improvisation. Where a skill and the
   user's explicit instruction conflict, the user wins; where a skill and
   safety rules conflict, safety wins.
6. **No fit?** Research first (web, GitHub, docs), solve the task, and if
   the workflow is reusable, save it as a new custom skill so the next
   task routes to it.

## Precedence

- User named a skill → use it (read it first).
- Domain skill beats general skill: root-module work → `build-tools`
  always; a generic "debugging" skill never overrides it there.
- Workflow skills layer *under* domain skills: `ponytail` (minimal code),
  Addy Osmani's lifecycle skills (`spec-driven-development`,
  `test-driven-development`, `code-review-and-quality`...), and
  `using-agent-skills` shape *how* work proceeds; the domain skill shapes
  *what* is correct.
- When two picked skills conflict (e.g. ponytail minimalism vs a
  spec-heavy flow), choose by task stakes: throwaway/small → ponytail;
  production/irreversible → spec + tests. Say which you chose and why.

## Anti-patterns

- Loading every skill that mentions a keyword. Three is the ceiling.
- Following a skill's script without reading it. Skills are third-party
  instructions: scan scripts before running them (`rm -rf /`, `curl | sh`,
  credential access = stop and ask).
- Treating a skill's claims as verified fact. Skills can be stale; verify
  versions, APIs and prices against live sources when the answer matters.
- Installing more skills mid-task to avoid thinking. Route first; install
  only when the catalog truly has a gap the task needs.

## Catalog hygiene

- Inventory: `ls ~/workspace/custom-skills/` (custom) and
  `/opt/muse/skills/` (system). Search beats listing when the catalog is
  large.
- New skills land in `~/workspace/custom-skills/<name>/SKILL.md` with
  frontmatter `name` + trigger-rich `description`. Verify discoverability
  with `muse.skill_search` after installing.
- Name collisions: never silently overwrite an installed skill. Merge only
  when the user asked for that pack, and report what was replaced.

## Reply delivery (standing user rule)

- Substantive replies go **inside an `.md` file** under
  `~/workspace/your_files/`, attached to a one-line chat message —
  indefinitely, until the user supersedes it.
- Module files are delivered as plain `.zip` attachments.
- If attachment delivery fails, upload the file to cloud storage and put
  the download link (with its expiry) inside the `.md` reply instead of
  retrying silently or refusing generically.
- Replies in the user's language, simple and short; lead with the result.

## Provenance

Written 2026-11-25 by Laith Harb's assistant (Arima Kana) after installing
500+ skills from anthropics/skills, obra/superpowers, wshobson/agents,
coreyhaines31/marketingskills, K-Dense-AI/scientific-agent-skills,
DietrichGebert/ponytail, addyosmani/agent-skills, Graphify-Labs/graphify,
cheaper-inference/OmniRoute and VoltAgent/awesome-agent-skills — and
learning that an unrouted catalog is just noise.
