---
description: Apply the FORGE HARVEST workflow (Extract → Analyze → Restructure → Verify → Extend → Synthesize → Transform) for documentation and knowledge extraction
argument-hint: <what to document or understand>
---

You are operating under the FORGE framework's **HARVEST workflow** for UNDERSTANDING problems — documentation, knowledge extraction, codebase comprehension.

## Setup (read these before starting)

1. Workflow definition: `<FORGE_HOME>/workflows/harvest.md`
2. Master spec sections for protocol context: `<FORGE_HOME>/FORGE_MASTER.md` — sections 5 (Confidence), 6 (Assumptions), 7 (Meta-Prompting), 8 (Verification), 12 (Operating Principles)

## Phase 0 — Prior learnings retrieval

If `<FORGE_HOME>/learnings/_index.jsonl` exists, search for prior HARVEST entries on similar domains/codebases. Surface top 3 before Phase 1. Otherwise, note: *"No learnings store yet — proceeding without prior context."*

## Engine (optional) — the `harvest` tool

If `harvest --help` succeeds, run the phases with the [HARVEST engine](https://github.com/0xPliny/harvest) instead of reading sources by hand. Run `harvest phases` for the full map. The essentials:

- **Extract:** `harvest extract <target> --graph -o harvested/<name>`. For Electron/ASAR apps, .NET assemblies and SQLite files it also runs REA (Reverse Engineer Anything) when `rea` is installed (`--rea` forces it). Read `MANIFEST.json` warnings and `REA.md` before Phase 2.
- **Analyze:** `harvest inspect` / `harvest search`; `harvest reverse <target>` for the methodology. If REA's MCP server (`rea`) is connected, trace compiled code with its tools (`trace_application_feature`, `xrefs`, `batch_decompile`).
- **Verify:** `harvest evidence init review.json` then `harvest evidence import review.json harvested/<name>/REA.md`. Carry REA's stated `confidence` and `limitations` into the Confidence Protocol.
- **Transform:** `harvest export harvested/<name> -o overview.html`. Review `SENSITIVE.md` before sharing anything.

Cite blueprint `file:line` locations and REA Evidence files (`rea/*.json`) as sources. If `harvest` is not installed, continue manually. Do not install it without asking the user.

## Phases 1-7

Apply HARVEST. Hard rules from the workflow file:
- Every claim must be traceable to source — no speculation as fact
- Confidence Protocol on every uncertain finding; mark gaps as `UNKNOWN` or `NEEDS VERIFICATION`
- Iterate until quality reaches 95%+ (completeness, accuracy, cross-references, consistency)
- Time-budget the phases per the percentages in `harvest.md` (Extract 25%, Analyze 20%, Restructure 15%, Verify 15%, Extend 10%, Synthesize 10%, Transform 5%)

## Closing emissions

After delivery:

**1. Telemetry (active now)** — Append one JSON line to `<FORGE_HOME>/telemetry/sessions.jsonl` matching the schema at `<FORGE_HOME>/telemetry/schema.json`. Self-report honestly:
- `task_id` (UUID4 you generate), `timestamp` (ISO 8601 UTC), `workflow: "harvest"`
- `classification`: category (UNDERSTANDING), complexity, domain, confidence
- `gates_passed` / `gates_failed` against the gate names in `schema.json`
- `assumptions_count`, `iterations` (refinement passes; HARVEST iterates until 95%+ quality), `outcome`
- `prompt_hash`: SHA-256 of $ARGUMENTS, first 16 hex chars
- `raw_prompt`: $ARGUMENTS only if `FORGE_TELEMETRY_RAW=1`, else `null`
- `notes`: brief commentary on which extraction sources were richest, which patterns generalized

Skip emission entirely if `FORGE_TELEMETRY_DISABLED=1`. Honesty matters — `tools/forge_eval.py` audits self-reports.

**2. Learnings (future, when Plan 1 ships)** — Append a learning entry capturing which extraction sources were richest and which patterns generalized. Skip if the store doesn't exist yet.

---

## User task

$ARGUMENTS
