---
description: Apply the FORGE C-A-R-E workflow (Context → Analyze → Respond → Evaluate) to a repair or optimization task
argument-hint: <bug or perf issue>
---

You are operating under the FORGE framework's **C-A-R-E workflow** for REPAIR or OPTIMIZATION problems.

## Setup (read these before starting)

1. Workflow definition: `<FORGE_HOME>/workflows/care.md`
2. Master spec sections for protocol context: `<FORGE_HOME>/FORGE_MASTER.md` — sections 5 (Confidence), 6 (Assumptions), 7 (Meta-Prompting), 8 (Verification), 12 (Operating Principles)

## Phase 0 — Prior learnings retrieval

If `<FORGE_HOME>/learnings/_index.jsonl` exists, search for matching prior REPAIR/OPTIMIZATION entries — failure patterns are especially valuable here. Surface top 3 before Phase 1. Otherwise, note: *"No learnings store yet — proceeding without prior context."*

## Phases 1-4 (iterative loop)

Apply C-A-R-E. Honor:
- Confidence Protocol on root-cause hypotheses and the proposed fix
- Track all assumptions; do not proceed past Analyze with unvalidated high-risk assumptions
- Iteration cap: default 3, extend to 5 only if quality is improving each pass; if plateaued after 3, escalate to R-I-S-E and re-classify
- Self-critique before Evaluate; verify no regressions before declaring complete

## Closing emissions

After resolution:

**1. Telemetry (active now)** — Append one JSON line to `<FORGE_HOME>/telemetry/sessions.jsonl` matching the schema at `<FORGE_HOME>/telemetry/schema.json`. Self-report honestly:
- `task_id` (UUID4 you generate), `timestamp` (ISO 8601 UTC), `workflow: "care"`
- `classification`: category (REPAIR or OPTIMIZATION), complexity, domain, confidence
- `gates_passed` / `gates_failed` against the gate names in `schema.json`
- `assumptions_count`, `iterations` (count actual loops — this matters for C-A-R-E), `outcome`
- `prompt_hash`: SHA-256 of $ARGUMENTS, first 16 hex chars
- `raw_prompt`: $ARGUMENTS only if `FORGE_TELEMETRY_RAW=1`, else `null`
- `notes`: brief commentary — for C-A-R-E especially, *what failed* during iteration is most valuable

Skip emission entirely if `FORGE_TELEMETRY_DISABLED=1`. Honesty matters — `tools/forge_eval.py` audits self-reports.

**2. Learnings (future, when Plan 1 ships)** — Append a learning entry — especially capture *what failed* during iteration, not just what worked. Skip if the store doesn't exist yet.

---

## User task

$ARGUMENTS
