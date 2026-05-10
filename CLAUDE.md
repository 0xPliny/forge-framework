# Working in the FORGE Repo

This file tells Claude Code (and anyone using an AI coding assistant) how to be useful when working **inside** the `forge-framework` repository itself — contributing, maintaining, or extending it.

> Building **with** FORGE in your own project? You're in the wrong file. Read [`README.md`](README.md) and install the [Claude Code integration](integrations/claude-code/) at the user level instead.

---

## What this repo is

FORGE — Framework for Orchestrated, Repeatable, Governed Engineering. A methodology for AI-assisted engineering with structured workflows (`R-I-S-E`, `C-A-R-E`, `HARVEST`), specialist personas (Atlas, Sage, Scribe, Sentinel), and a self-improving feedback loop (OMEGA). The canonical spec is [`FORGE_MASTER.md`](FORGE_MASTER.md).

## Project-level slash commands

This repo ships its own `.claude/` directory. The moment you open the repo in Claude Code, these commands are available with **no install step**:

- `/rise <task>` — Apply R-I-S-E workflow
- `/care <task>` — Apply C-A-R-E workflow
- `/harvest <task>` — Apply HARVEST workflow
- `/atlas <request>` — Activate Atlas (Deep Research)
- `/sage <request>` — Activate Sage (Architecture)
- `/scribe <request>` — Activate Scribe (Documentation)
- `/sentinel <request>` — Activate Sentinel (Security)

The `forge-classifier` skill auto-suggests routing if you describe a task without invoking a slash command. Project-level commands use **relative paths** to the workflow/persona files in this repo, so they work out of the box.

## Working norms in this repo

When making changes, follow FORGE's own protocols on FORGE itself — eat your own dog food:

- **For new features** → invoke `/rise` (it's a CREATION task)
- **For bug fixes** → invoke `/care`
- **For docs improvements** → invoke `/harvest` or `/scribe`
- **Confidence Protocol applies** — score every meaningful claim 1-10 with reasoning; never claim 9-10 without direct verification
- **Track assumptions** — high-risk assumptions must be validated before merging
- **Run meta-prompting** before opening a PR — challenge your own changes

## Key files to know

| File | Purpose |
|---|---|
| [`FORGE_MASTER.md`](FORGE_MASTER.md) | Canonical spec — paste-into-any-AI activator. **Edit with care; this is the public contract.** |
| [`README.md`](README.md) | Public face of the project |
| [`workflows/`](workflows/) | R-I-S-E, C-A-R-E, HARVEST workflow definitions |
| [`personas/`](personas/) | Atlas, Sage, Scribe, Sentinel |
| [`core/`](core/) | Confidence protocol, assumption tracker, meta-prompting, OMEGA retrieval |
| [`telemetry/`](telemetry/) | OMEGA mechanical log (schema + privacy + methodology) |
| [`learnings/`](learnings/) | OMEGA curated insights store |
| [`tools/`](tools/) | `forge_eval.py` (per-session scorer) and `forge_report.py` (N-day aggregator) |
| [`integrations/claude-code/`](integrations/claude-code/) | User-level install for Claude Code |

## Operational stack tools

```bash
# Score the last FORGE session against protocol gates
python tools/forge_eval.py --last

# Aggregate the last 30 days of telemetry into a Markdown report
python tools/forge_report.py --days 30
```

Requires Python 3.9+. Stdlib only — no `pip install`.

## Line endings

The repo stores files as LF in git but Windows users see CRLF in their working copy via `core.autocrlf=true`. There is no `.gitattributes` enforcing line endings. If you see git diffs that show entire files changed with no apparent content change, it's almost always line endings — use `diff --strip-trailing-cr` to confirm.

## Contributing

Open an issue for substantive changes before opening a PR. Good first contributions:

- New domain modules (use [`modules/domain_module_template.md`](modules/domain_module_template.md))
- Additional personas (follow [`personas/atlas.md`](personas/atlas.md) structure)
- Workflow templates in `templates/rise/`, `templates/care/`, `templates/harvest/`
- Integrations under `integrations/` (JetBrains, Vim, etc.)

Apache 2.0. Use it, extend it, build on it.
