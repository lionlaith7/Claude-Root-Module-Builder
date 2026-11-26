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

# skill-router v1.1.0 - use the right skill for every task

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
   - One of the phrasings must use **likely skill-name vocabulary**, not
     only paraphrases (see Lessons: paraphrases alone routinely miss).
3. **Read the top candidates' `SKILL.md`** (not just the search snippet).
   A skill whose description matches but whose body is stale, generic, or
   for a different stack is not a match. An empty or near-empty body counts
   as no match — move on. If the body defers to `references/` files, read
   the relevant one before acting.
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
- **Safe active-catalog ceiling (measured 2026-11-25):** at 8,070 active
  folders in `~/workspace/custom-skills/`, every process spawn failed with
  `E2BIG` ("Argument list too long") — exec, browser search and subagent
  exec all broke. 4,738–4,740 active folders ran cleanly for a full 24h
  self-test (48 routing runs, zero E2BIG). Keep the active catalog well
  below 8,000; if E2BIG appears, move folders out of `custom-skills/`
  immediately. Inactive overflow lives in
  `~/workspace/skills-archive/awesome/` (3,332 folders) — do not restore
  it en masse; pull individual skills back only when a task needs one.

## Reply delivery (standing user rule)

- Substantive replies go **inside an `.md` file** under
  `~/workspace/your_files/`, attached to a one-line chat message —
  indefinitely, until the user supersedes it.
- Module files are delivered as plain `.zip` attachments.
- If attachment delivery fails, upload the file to cloud storage and put
  the download link (with its expiry) inside the `.md` reply instead of
  retrying silently or refusing generically.
- Replies in the user's language, simple and short; lead with the result.

## Lessons from 24h of self-testing (2026-11-25 → 2026-11-26)

Evidence base: 24 routing scenarios × 2 passes (48 graded runs), every 2
hours, routing only (no task execution). Full log:
`~/workspace/modules/skill-router-tests/log.md`. What held up, what broke:

- **Skill-name phrasing retrieves; paraphrases fail.** Search weights
  title/description over body content. "CI CD automation", "planning task
  breakdown", "API interface design", "code quality review",
  "performance optimization", "humanize", "touch up product photo"
  reliably rank the right skill #1. Natural paraphrases ("quality gates",
  "decompose feature", "pagination idempotency", "measure fix verify",
  "sound natural", "merchandise photo") often miss the expected skill
  entirely. Rule: always include one query built from the likely skill
  name / domain term, not only the user's words.
- **Polysemy traps dominate false positives.** "Module" → Terraform/
  Holoscan, "chart" → Helm charts, "library" → Terraform/ad libraries,
  "shell" → app-shell, "profile" → HPC profiling or social profiles,
  "trends" → market trends, "interface" → API/agent interfaces,
  "technical" → technical SEO, "design" → design systems, "add" /
  "continuous" / "script" → noise. Expect the top hits to be the wrong
  sense of the word; that is normal, not a search failure.
- **Reading the body is load-bearing, not optional.** It repeatedly
  prevented catastrophic picks: `performance-profiling` profiles HPC
  MPI simulations (not web pages), `mobile-android-design` is Jetpack
  Compose (not HTML WebUI), `helm-chart-scaffolding` is Kubernetes,
  `marketplace-gate` judges code repos (not product photos), `ci` wires
  one specific tool. Title/snippet match ≠ fit. Thin bodies that defer
  to `references/` must have those files read too.
- **Catalog hygiene traps are real.** `exploratory-data-analysis` is
  indexed but its `SKILL.md` is 0 bytes — treat an empty body as no
  match. Duplicate clusters (humanizer ×4+, SEO ×8+, ADR ×5, TDD ×3)
  crowd results: pick the most complete primary, at most one
  complementary supporting skill, then stop. Near-duplicates drift
  (action versions, default paths) — the primary wins conflicts.
- **Distinguish a true gap from a recall failure.** No general
  library-comparison skill exists (`fresh-library-docs` is only a
  partial input), and no ham-radio/APRS skill exists — both are correct
  research-first fallbacks. When every top-8 body is a different
  domain, stop rephrasing and fall back. When the right skill exists
  but ranks low (bootloop debugging, task breakdown), precedence rules
  and catalog knowledge recover it — search alone is not enough.
- **`build-tools` recall is fragile; the precedence rule carries it.**
  Bare "module", "WebUI dashboard", "service.sh" and "web interface"
  lose it; "KernelSU / root module / Magisk / FinaSU" and "disable
  guard" find it at rank 1. "Root-module work → build-tools always"
  is a hard rule, not a tie-breaker. Module scripts are POSIX sh
  (BusyBox ash) — generic Bash advice never overrides build-tools there.
- **Resolve conflicts by stakes and scope, out loud.** Throwaway vs
  production (prototype+ponytail vs spec-driven+hardening),
  simplification of existing code vs scope discipline
  (code-simplification governs the refactor, ponytail governs what not
  to add), clarification output (interview-me for intent, deep-clarify
  only once a spec document is wanted), framework vs specialist
  (seo-audit over on-page-seo-checker), process + domain layer
  (security-and-hardening + bash-defensive-patterns for shell audits).
  State the choice and what was deferred.
- **Adapt skills; do not follow them literally.** TDD's RED-first step
  does not fit characterization tests for untested code (they pass by
  design). `security-and-hardening` is web-OWASP-centric; only its
  injection/secrets/validation sections transfer to shell. Heavyweight
  skills (`ad-angle-miner`, `security-audit`) should be steered to
  their light path for small tasks and escalated only at scale.
- **Non-interactive runs change the routing.** `interview-me` forbids
  use in CI/scheduled/autonomous contexts. In a detached run, an
  underspecified request is a blocker to report to the user — never
  guess, and never "interview" nobody.
- **Catalog size is a hard operational limit** (see Catalog hygiene):
  8,070 active folders broke all process spawns; ~4,740 is proven
  safe. Routing quality means nothing if the runtime cannot spawn.

## Provenance

Written 2026-11-25 by Laith Harb's assistant (Arima Kana) after installing
500+ skills from anthropics/skills, obra/superpowers, wshobson/agents,
coreyhaines31/marketingskills, K-Dense-AI/scientific-agent-skills,
DietrichGebert/ponytail, addyosmani/agent-skills, Graphify-Labs/graphify,
cheaper-inference/OmniRoute and VoltAgent/awesome-agent-skills — and
learning that an unrouted catalog is just noise.

v1.1.0 (2026-11-26): added the Lessons section and the safe-catalog rule
from the 24h self-test (48 graded routing runs, log in
`~/workspace/modules/skill-router-tests/log.md`).
