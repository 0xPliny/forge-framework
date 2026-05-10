---
description: Apply the FORGE C-A-R-E workflow (Context → Analyze → Respond → Evaluate) to a repair or optimization task
argument-hint: <bug or perf issue>
---

You are operating under the FORGE framework's **C-A-R-E workflow** for REPAIR or OPTIMIZATION problems.

## Setup (read these before starting)

1. Workflow definition: `workflows/care.md`
2. Master spec sections for protocol context: `FORGE_MASTER.md` — sections 5 (Confidence), 6 (Assumptions), 7 (Meta-Prompting), 8 (Verification), 12 (Operating Principles)

## Phase 0 — Prior learnings retrieval

If `learnings/_index.jsonl` exists, search for matching prior REPAIR/OPTIMIZATION entries — failure patterns are especially valuable here. Surface top 3 before Phase 1 per `core/omega_retrieval.md`. Otherwise, note: *"No learnings store yet — proceeding without prior context."*

## Phases 1-4 (iterative loop)

Apply C-A-R-E. Honor:
- Confidence Protocol on root-cause hypotheses and the proposed fix
- Track all assumptions; do not proceed past Analyze with unvalidated high-risk assumptions
- Iteration cap: default 3, extend to 5 only if quality is improving each pass; if plateaued after 3, escalate to R-I-S-E and re-classify
- Self-critique before Evaluate; verify no regressions before declaring complete

## Closing emissions

After resolution:

**1. Telemetry** — Append one JSON line to `telemetry/sessions.jsonl` per `telemetry/schema.json`. Self-report honestly:
- `task_id` (UUID4), `timestamp` (ISO 8601 UTC), `workflow: "care"`
- `classification`: category (REPAIR or OPTIMIZATION), complexity, domain, confidence
- `gates_passed` / `gates_failed` against the gate names in `schema.json`
- `assumptions_count`, `iterations` (count actual loops — this matters for C-A-R-E), `outcome`
- `prompt_hash`: SHA-256 of $ARGUMENTS, first 16 hex chars
- `raw_prompt`: $ARGUMENTS only if `FORGE_TELEMETRY_RAW=1`, else `null`
- `notes`: brief commentary — for C-A-R-E especially, *what failed* during iteration is most valuable

Skip emission entirely if `FORGE_TELEMETRY_DISABLED=1`.

**2. Learnings** — Append a learning entry capturing what failed during iteration; failure patterns generalize better than success patterns. Skip if nothing non-obvious surfaced.

---

## User task

$ARGUMENTS
