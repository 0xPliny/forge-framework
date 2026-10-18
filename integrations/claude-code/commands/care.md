---
description: Apply the FORGE C-A-R-E workflow (Context → Analyze → Respond → Evaluate) to a repair or optimization task
argument-hint: <bug or perf issue>
---

You are operating under the FORGE framework's **C-A-R-E workflow** for REPAIR or OPTIMIZATION problems.

## Setup (read these before starting)

1. Workflow definition: `<FORGE_HOME>/workflows/care.md`
2. Master spec sections for protocol context: `<FORGE_HOME>/FORGE_MASTER.md` — sections 5 (Confidence), 6 (Assumptions), 7 (Meta-Prompting), 8 (Verification), 12 (Operating Principles)

## Phase 0 — Prior learnings retrieval

Start the session clock: `python <FORGE_HOME>/tools/forge_session.py start`. It records the start time and git baseline so telemetry is measured, not estimated.

Then retrieve prior learnings per `<FORGE_HOME>/core/omega_retrieval.md`:

```bash
python <FORGE_HOME>/tools/forge_learn.py search --category <CATEGORY> --domain <domain> --keywords <k1,k2,k3>
```

It prints the top 3 matches (score ≥ 3), *"No matching prior learnings."*, or *"No learnings store yet — proceeding without prior context."* Surface the matches before Phase 1 and verify them before relying on them. Failure patterns from prior REPAIR/OPTIMIZATION work are especially valuable here.

## Phases 1-4 (iterative loop)

Apply C-A-R-E. Honor:
- Confidence Protocol on root-cause hypotheses and the proposed fix
- Track all assumptions; do not proceed past Analyze with unvalidated high-risk assumptions
- Iteration cap: default 3, extend to 5 only if quality is improving each pass; if plateaued after 3, escalate to R-I-S-E and re-classify
- Self-critique before Evaluate; verify no regressions before declaring complete

## Closing emissions

After resolution:

**1. Telemetry** — Build one JSON object matching `<FORGE_HOME>/telemetry/schema.json` and pipe it to `python <FORGE_HOME>/tools/forge_session.py emit`. It fills `started_at`, `timestamp`, `wall_time_sec` and `git_stats` by measurement, validates the record, and appends it to `<FORGE_HOME>/telemetry/sessions.jsonl`. (If no session was started or Python is unavailable, append the line yourself and self-report those fields.) Self-report the rest honestly:
- `task_id` (UUID4 you generate), `timestamp` (ISO 8601 UTC), `workflow: "care"`
- `classification`: category (REPAIR or OPTIMIZATION), complexity, domain, confidence
- `gates_passed` / `gates_failed` against the gate names in `schema.json`
- `assumptions_count`, `iterations` (count actual loops — this matters for C-A-R-E), `outcome`
- `prompt_hash`: SHA-256 of $ARGUMENTS, first 16 hex chars
- `raw_prompt`: $ARGUMENTS only if `FORGE_TELEMETRY_RAW=1`, else `null`
- `notes`: brief commentary — for C-A-R-E especially, *what failed* during iteration is most valuable

Skip emission entirely if `FORGE_TELEMETRY_DISABLED=1`. Honesty matters — `tools/forge_eval.py` audits self-reports.

**2. Learnings** — Capture what failed during iteration; failure patterns generalize better than success patterns. Skip if nothing non-obvious surfaced. Write the entry fields per `<FORGE_HOME>/core/omega_retrieval.md` (Step 2) to a JSON file and append it with `python <FORGE_HOME>/tools/forge_learn.py add --file entry.json`; it fills the id, date and normalized signature and validates the entry. To start from this session's telemetry: `python <FORGE_HOME>/tools/forge_learn.py promote --task-id last > draft.json`.

---

## User task

$ARGUMENTS
