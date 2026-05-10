---
description: Apply the FORGE R-I-S-E workflow (Research → Identify → Synthesize → Execute) to a creation or transformation task
argument-hint: <task description>
---

You are operating under the FORGE framework's **R-I-S-E workflow** for CREATION or TRANSFORMATION problems.

## Setup (read these before starting)

1. Workflow definition: `<FORGE_HOME>/workflows/rise.md`
2. Master spec sections for protocol context: `<FORGE_HOME>/FORGE_MASTER.md` — sections 5 (Confidence), 6 (Assumptions), 7 (Meta-Prompting), 8 (Verification), 12 (Operating Principles)

## Phase 0 — Prior learnings retrieval

If `<FORGE_HOME>/learnings/_index.jsonl` exists, search for entries whose `problem_signature` matches this task's category + domain + top keywords, and surface the top 3 before Phase 1. Otherwise, note: *"No learnings store yet — proceeding without prior context."*

## Phases 1-4

Apply R-I-S-E to the user's task below. Mandatory protocol overlays:
- Confidence Protocol on every meaningful output (1-10 + reasoning + caveats)
- Track all assumptions in the Assumptions table; high-risk ones must be validated before Phase 3
- Run Meta-Prompting self-critique before declaring Phase 4 complete
- Match Verification Stack layers to complexity (Simple: 1-2, Medium: 1-3, Complex: 1-4, Expert: 1-5)

## Closing emissions

After completing Phase 4:

**1. Telemetry (active now)** — Append one JSON line to `<FORGE_HOME>/telemetry/sessions.jsonl` matching the schema at `<FORGE_HOME>/telemetry/schema.json`. Self-report honestly:
- `task_id` (UUID4 you generate), `timestamp` (ISO 8601 UTC), `workflow: "rise"`
- `classification`: category, complexity, domain, confidence (from your Phase 0/1 work)
- `gates_passed` / `gates_failed` against the gate names in `schema.json`
- `assumptions_count`, `iterations` (default 1 for R-I-S-E), `outcome` (success / partial / failed / escalated)
- `prompt_hash`: SHA-256 of $ARGUMENTS, first 16 hex chars
- `raw_prompt`: $ARGUMENTS only if `FORGE_TELEMETRY_RAW=1`, else `null`
- `notes`: brief commentary on what worked or failed

Skip emission entirely if `FORGE_TELEMETRY_DISABLED=1`. Honesty on `gates_passed` is non-negotiable — `tools/forge_eval.py` audits self-reports. Use shell to append exactly one JSON line.

**2. Learnings (future, when Plan 1 ships)** — Append a learning entry to `<FORGE_HOME>/learnings/_index.jsonl`. Skip if the store doesn't exist yet.

---

## User task

$ARGUMENTS
