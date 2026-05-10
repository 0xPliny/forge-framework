# FORGE Telemetry

Self-reported session logs that turn FORGE from a methodology with anecdotal claims into an evidence-producing system.

## What this is

When you invoke `/rise`, `/care`, or `/harvest` (via the [Claude Code integration](../integrations/claude-code/)), the AI appends one JSON line to `sessions.jsonl` at task close, recording:

- Classification (category, complexity, domain, confidence)
- Workflow used and persona (if any)
- Which FORGE gates passed and failed
- Assumption count, iteration count, outcome
- Prompt hash (SHA-256) — raw prompt only stored if you opt in

The schema is defined in [`schema.json`](schema.json).

## What this is NOT

- **Not a hook.** The AI emits telemetry from inside the slash command body. No `Stop` hook, no settings changes.
- **Not phoned home.** All data stays local. `sessions.jsonl` is gitignored by default.
- **Not load-bearing.** If the AI forgets to emit, nothing breaks — `forge_report.py` just doesn't see that session.

## Files

| File | Purpose |
|---|---|
| `schema.json` | JSON Schema for log lines (draft-07) |
| `sessions.jsonl` | Append-only log, one line per workflow invocation. Created on first emit. Gitignored. |
| `METHODOLOGY.md` | How the README's reported figures (21x, $0.002/line, 56x, 240x) could be reproduced with this stack |

## Tools

| Tool | What it does |
|---|---|
| [`tools/forge_eval.py`](../tools/forge_eval.py) | Score a single session against FORGE gates. Audits the AI's self-report. |
| [`tools/forge_report.py`](../tools/forge_report.py) | Aggregate over N days. Outputs a Markdown table with workflow distribution, outcome rates, average confidence, iteration clusters. |

**Requirement:** Python 3.9+ on PATH. Stdlib only — no `pip install` needed. On Windows, install from [python.org](https://www.python.org/downloads/) (the Microsoft Store stub at `WindowsApps\python.exe` is not a real Python). On Mac/Linux, Python 3 is typically pre-installed.

## Privacy

| Variable | Effect |
|---|---|
| (default) | `prompt_hash` recorded; `raw_prompt` is `null` |
| `FORGE_TELEMETRY_RAW=1` | `raw_prompt` is populated. Use only in trusted single-user environments. |
| `FORGE_TELEMETRY_DISABLED=1` | AI skips the emit step entirely |

The telemetry contains classification labels, gate names, and (optionally) raw prompts. It does not contain code, file contents, or AI output.

## Schema versioning

The first field of every line is `schema_version`. Tools key off this. v1.0 is the current schema; future versions will be additive where possible and bump the version on breaking changes.

## Quick examples

**Inspect last 5 sessions:**
```bash
tail -n 5 sessions.jsonl | python -m json.tool --json-lines
```

**See workflow distribution this week:**
```bash
python ../tools/forge_report.py --days 7
```

**Audit a single session:**
```bash
python ../tools/forge_eval.py --task-id <uuid>
```

## Wiring with Plan 1 (learnings store)

The `notes` field on each session is the seed for the future learnings store. When Plan 1 ships, `forge_report.py` will surface high-iteration tasks and outcome=failed sessions as learning candidates — those are where compounding improvement comes from.

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
