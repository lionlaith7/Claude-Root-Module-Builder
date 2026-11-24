# Evidence tiers and statuses

Tag every non-trivial claim about behaviour with a tier. Never present T2-T4 as fact.

| Tier | Meaning | Example |
|---|---|---|
| T1 | Official doc or source code of the tool | Magisk docs/guides.md, module_installer.sh |
| T2 | Secondary source (blog, forum, other fork's docs) | a XDA post |
| T3 | Observed on the user's device (canary/debug log) | `PROBE shell double_bracket=no` |
| T4 | Unverified / inferred | "FinaSU probably has boot-completed.sh" |

Rules
- A T4 claim must be written as a question for the canary, not as an instruction.
- Conflicts between sources (e.g. post-fs-data 10 s vs 40 s) are reported as a conflict with both sources; design for the stricter value.
- Status words come from tools only (see SKILL.md). Offline tests reach PASS_SIMULATED at most.
- PASS_REAL needs a device log whose HASH lines equal the manifest of the zip you built. A log from an older build proves nothing about the new one.
