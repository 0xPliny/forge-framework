---
description: Apply the FORGE R-I-S-E workflow (Research → Identify → Synthesize → Execute) to a creation or transformation task
argument-hint: <task description>
---

You are operating under the FORGE framework's **R-I-S-E workflow** for CREATION or TRANSFORMATION problems.

## Setup (read these before starting)

1. Workflow definition: `<FORGE_HOME>/workflows/rise.md`
2. Master spec sections for protocol context: `<FORGE_HOME>/FORGE_MASTER.md` — sections 5 (Confidence), 6 (Assumptions), 7 (Meta-Prompting), 8 (Verification), 12 (Operating Principles)

## Phase 0 — Prior learnings retrieval

Start the session clock: `python <FORGE_HOME>/tools/forge_session.py start`. It records the start time and git baseline so telemetry is measured, not estimated.

Then retrieve prior learnings per `<FORGE_HOME>/core/omega_retrieval.md`:

```bash
python <FORGE_HOME>/tools/forge_learn.py search --category <CATEGORY> --domain <domain> --keywords <k1,k2,k3>
```

It prints the top 3 matches (score ≥ 3), *"No matching prior learnings."*, or *"No learnings store yet — proceeding without prior context."* Surface the matches before Phase 1 and verify them before relying on them.

## Phases 1-4

Apply R-I-S-E to the user's task below. Mandatory protocol overlays:
- Confidence Protocol on every meaningful output (1-10 + reasoning + caveats)
- Track all assumptions in the Assumptions table; high-risk ones must be validated before Phase 3
- Run Meta-Prompting self-critique before declaring Phase 4 complete
- Match Verification Stack layers to complexity (Simple: 1-2, Medium: 1-3, Complex: 1-4, Expert: 1-5)

## Closing emissions

After completing Phase 4:

**1. Telemetry** — Build one JSON object matching `<FORGE_HOME>/telemetry/schema.json` and pipe it to `python <FORGE_HOME>/tools/forge_session.py emit`. It fills `started_at`, `timestamp`, `wall_time_sec` and `git_stats` by measurement, validates the record, and appends it to `<FORGE_HOME>/telemetry/sessions.jsonl`. (If no session was started or Python is unavailable, append the line yourself and self-report those fields.) Self-report the rest honestly:
- `task_id` (UUID4 you generate), `timestamp` (ISO 8601 UTC), `workflow: "rise"`
- `classification`: category, complexity, domain, confidence (from your Phase 0/1 work)
- `gates_passed` / `gates_failed` against the gate names in `schema.json`
- `assumptions_count`, `iterations` (default 1 for R-I-S-E), `outcome` (success / partial / failed / escalated)
- `prompt_hash`: SHA-256 of $ARGUMENTS, first 16 hex chars
- `raw_prompt`: $ARGUMENTS only if `FORGE_TELEMETRY_RAW=1`, else `null`
- `notes`: brief commentary on what worked or failed

Skip emission entirely if `FORGE_TELEMETRY_DISABLED=1`. Honesty on `gates_passed` is non-negotiable — `tools/forge_eval.py` audits self-reports. Use shell to append exactly one JSON line.

**2. Learnings** — If something non-obvious surfaced (assumption broke, hidden constraint, surprising approach worked), record it. Skip routine tasks — discipline matters. Write the entry fields per `<FORGE_HOME>/core/omega_retrieval.md` (Step 2) to a JSON file and append it with `python <FORGE_HOME>/tools/forge_learn.py add --file entry.json`; it fills the id, date and normalized signature and validates the entry. To start from this session's telemetry: `python <FORGE_HOME>/tools/forge_learn.py promote --task-id last > draft.json`.

---

## User task

$ARGUMENTS
