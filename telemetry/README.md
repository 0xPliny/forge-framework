# FORGE Telemetry

Session logs that turn FORGE from a methodology with anecdotal claims into an evidence-producing system. Since schema v1.1, time and code churn are measured by `tools/forge_session.py`; the rest is self-reported by the AI and audited by `tools/forge_eval.py`.

## What this is

When you invoke `/rise`, `/care`, or `/harvest` (via the [Claude Code integration](../integrations/claude-code/)), the AI appends one JSON line to `sessions.jsonl` at task close, recording:

- Classification (category, complexity, domain, confidence)
- Workflow used and persona (if any)
- Which FORGE gates passed and failed
- Assumption count, iteration count, outcome
- Prompt hash (SHA-256) — raw prompt only stored if you opt in
- **Measured (v1.1):** start time, wall time and git churn (files changed, lines added/removed), listed in the `measured` field

The schema is defined in [`schema.json`](schema.json).

## What this is NOT

- **Not a hook.** The slash command runs `forge_session.py start` at Phase 0 and pipes its record to `forge_session.py emit` at close. No `Stop` hook, no settings changes.
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
| [`tools/forge_report.py`](../tools/forge_report.py) | Aggregate over N days. Outputs a Markdown table with workflow distribution, outcome rates, average confidence, iteration clusters, and measured wall time and churn. |
| [`tools/forge_session.py`](../tools/forge_session.py) | `start` records time and git baseline in `.forge-session.json`; `emit` adds measured fields, validates and appends the record. |
| [`tools/forge_schema.py`](../tools/forge_schema.py) | Stdlib validator: `python tools/forge_schema.py telemetry/schema.json telemetry/sessions.jsonl`. |

**Requirement:** Python 3.9+ on PATH. Stdlib only — no `pip install` needed. On Windows, install from [python.org](https://www.python.org/downloads/) (the Microsoft Store stub at `WindowsApps\python.exe` is not a real Python). On Mac/Linux, Python 3 is typically pre-installed.

## Privacy

| Variable | Effect |
|---|---|
| (default) | `prompt_hash` recorded; `raw_prompt` is `null` |
| `FORGE_TELEMETRY_RAW=1` | `raw_prompt` is populated. Use only in trusted single-user environments. |
| `FORGE_TELEMETRY_DISABLED=1` | AI skips the emit step entirely; `forge_session.py emit` writes nothing |

The telemetry contains classification labels, gate names, line counts, a start commit hash, and (optionally) raw prompts. It does not contain code, file names, file contents, or AI output.

## Schema versioning

The first field of every line is `schema_version`. Tools key off this. **v1.1** is current and is additive: it adds the optional `started_at`, `git_stats` and `measured` fields, so v1.0 lines remain valid. Breaking changes will bump the major version.

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

## Wiring with the learnings store

The `notes` field on each session is the seed for the learnings store. `forge_report.py` lists high-iteration and non-success sessions as learning candidates, and `python tools/forge_learn.py promote --task-id <id>` turns one into a draft entry for `learnings/_index.jsonl`. Those sessions are where compounding improvement comes from.

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
