# Install build-tools (any AI agent)

`build-tools` follows the open Agent Skills format (`SKILL.md` with YAML frontmatter in a folder named `build-tools`), so it works with every agent that supports skills or rules files. Pick your agent below. The skill folder must keep the name `build-tools`.

## Fastest: skills CLI (all agents)

```bash
npx skills add lionlaith7/Claude-Root-Module-Builder
```

Works for Claude Code, Codex, Cursor, Antigravity, OpenCode, Windsurf and every other agent the [skills CLI](https://skills.sh) supports. Variations:

```bash
npx skills add lionlaith7/Claude-Root-Module-Builder -a claude-code   # one agent only
npx skills add lionlaith7/Claude-Root-Module-Builder -g               # user-wide
npx skills add lionlaith7/Claude-Root-Module-Builder --list           # preview
npx skills update build-tools                                         # update later
```

## Claude Code

```bash
git clone https://github.com/lionlaith7/Claude-Root-Module-Builder ~/.claude/skills/build-tools-src
cp -r ~/.claude/skills/build-tools-src/build-tools ~/.claude/skills/build-tools
```

Or use the bundled installer from a clone:

```sh
git clone https://github.com/lionlaith7/Claude-Root-Module-Builder
sh Claude-Root-Module-Builder/install.sh      # --check, --uninstall, --ref, --sha256 available
```

Claude Code reads skills from `.claude/skills/` (project) or `~/.claude/skills/` (user). The skill triggers on module requests and is also available as `/build-tools`.

## Claude.ai / Muse app

Zip the `build-tools/` folder (the folder name must stay `build-tools`) and upload it as a skill in Settings > Skills.

## Codex (OpenAI)

```bash
npx skills add lionlaith7/Claude-Root-Module-Builder -a codex
```

Or add the repo as a submodule and point `AGENTS.md` at it:

```bash
git submodule add https://github.com/lionlaith7/Claude-Root-Module-Builder.git .build-tools
```

```markdown
## Root modules

Follow `.build-tools/build-tools/SKILL.md` for any Magisk/KernelSU module work,
and load the relevant `.build-tools/build-tools/references/*.md` files it names.
```

## Cursor

```bash
npx skills add lionlaith7/Claude-Root-Module-Builder -a cursor
```

Or clone the repo into your project and add to `.cursor/rules` (or `.cursorrules`):

```markdown
For Android root module work, follow build-tools/SKILL.md and its references/.
```

## Windsurf

```bash
npx skills add lionlaith7/Claude-Root-Module-Builder -a windsurf
```

Or add the same two lines to `.windsurfrules`.

## Gemini CLI / Antigravity

```bash
npx skills add lionlaith7/Claude-Root-Module-Builder -a antigravity
```

Or clone into `.agents/skills/build-tools` in your project (or the global `~/.gemini/antigravity/` config), and keep a `GEMINI.md` line pointing at `build-tools/SKILL.md`.

## Muse / VS Code

Muse reads `AGENTS.md` and skills. Clone the repo into your workspace and keep the repo-root `AGENTS.md` (it points at `build-tools/SKILL.md`), or copy the `build-tools/` folder into `.github/skills/` if your setup supports it.

## Any other agent (generic)

The skill is plain Markdown plus Python tools with no network or account requirements:

1. Clone this repo anywhere your agent can read files.
2. Tell the agent: "Follow `build-tools/SKILL.md` for root module work; load the reference files it names when needed."
3. The tools run anywhere Python 3 and a POSIX shell exist: `python3 -I build-tools/scripts/new_module.py --list`, `lint_module.py`, `build_zip.py`, `parse_report.py`. Verify the toolchain offline with `python3 -I build-tools/tests/test_all.py`.

## Use

Ask your agent: "Build a KernelSU module that ...". Install the zip, reboot, then send `Documents/<id>/<id>-debug.log` back.
First time on a new phone: ask for the **canary** module and send its log.
