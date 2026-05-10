# FORGE Learnings Store

The persistent memory layer that makes the OMEGA loop real. Without this store, every conversation starts cold and the framework's "self-improving" claim is aspirational. With it, prior insight compounds.

## What this is

`_index.jsonl` is an append-only log of non-obvious insights from completed FORGE tasks. Each entry captures **what worked, what failed, and when this learning generalizes**. Workflow commands (`/rise`, `/care`, `/harvest`) read it at Phase 0 and write to it at task close.

The schema is in [`schema.json`](schema.json) (JSON Schema draft-07).

## What this is NOT

- **Not a transcript log.** That's `telemetry/sessions.jsonl`. Telemetry captures every workflow invocation mechanically; learnings are curated insights only.
- **Not a knowledge base.** It's not for project facts ("the API endpoint is at /v1/foo"). It's for *meta-learnings* about how to do work better.
- **Not a substitute for `git log` / code comments.** The fix is in the code; the learning is *why this kind of fix is the right move in this kind of situation*.

## Files

| File | Purpose | Committed? |
|---|---|---|
| `schema.json` | JSON Schema for entries | yes |
| `README.md` | this file | yes |
| `EXAMPLES.md` | curated example entries with commentary on why each is useful | yes |
| `_index.jsonl` | append-only log; one entry per learning | **no** (gitignored — personal store) |
| `<learning_id>.md` | optional deep-dive companion files | no (gitignored except by allowlist) |

`_index.jsonl` is local. Your learnings reflect *your* work and won't generalize to another operator's environment. That's by design.

## Schema (one line per entry)

| Field | Type | Required |
|---|---|---|
| `schema_version` | `"1.0"` | yes |
| `learning_id` | UUID4 | yes |
| `date` | `YYYY-MM-DD` | yes |
| `source_task_id` | UUID from telemetry, or null | no |
| `workflow` | `rise` / `care` / `harvest` / `cross-cutting` | yes |
| `category` | FORGE category | yes |
| `domain` | string | yes |
| `complexity` | FORGE complexity, or null | no |
| `problem_signature` | `{keywords, normalized}` | yes |
| `what_worked` | string | yes |
| `what_failed` | string | yes |
| `generalization` | when this applies | yes |
| `applies_to` | array of category:domain pairs | no |
| `confidence` | 1-10 | yes |
| `source` | `telemetry-derived` / `manual` / `post-mortem` | yes |
| `tags` | free-form array | no |
| `deep_dive_path` | optional `.md` companion path | no |

## Retrieval contract

Defined in [`../core/omega_retrieval.md`](../core/omega_retrieval.md). In short:

1. **At Phase 0:** Workflow commands grep `_index.jsonl` for entries whose `problem_signature.normalized` overlaps with the current task's category + domain + top keywords.
2. **Top 3** matches by overlap count (ties broken by recency) are surfaced to the AI before Phase 1.
3. **At task close:** If something non-obvious was learned, append a new entry. Skip if the task was routine (no new insight beyond the existing store).

The retrieval is intentionally simple (string matching) for v1. Embeddings are a future enhancement when entry count justifies it (~100+).

## When to write a learning

✅ **Write** when:
- An assumption broke and required revision
- A non-obvious approach worked surprisingly well
- A common-looking task had a hidden constraint
- You'd want a future you to read this before doing similar work

❌ **Skip** when:
- Task was routine — nothing new surfaced
- The learning is already in the store (read first to check)
- The insight is project-specific facts, not transferable methodology

Discipline matters. A store full of obvious entries is worse than a sparse store of valuable ones.

## Wiring with telemetry

`telemetry/sessions.jsonl` is the substrate. `tools/forge_report.py` already surfaces high-iteration and non-success sessions as "learnings-store candidates" — those are where insight tends to live. A future `tools/forge_promote.py` could convert a flagged session into a learning entry interactively.

## Privacy

Same posture as telemetry: all data stays local. `_index.jsonl` is gitignored. No phone-home.

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
