# OMEGA Retrieval Protocol

The canonical contract for how an AI queries and writes the FORGE learnings store. This document operationalizes the OMEGA Loop (FORGE_MASTER §9) — without it, OMEGA is conceptual; with it, learning compounds.

> **Store location:** `learnings/_index.jsonl`
> **Schema:** `learnings/schema.json`
> **Examples:** `learnings/EXAMPLES.md`

---

## Phase 0 — Retrieve Prior Learnings (Before Workflow Phase 1)

Every workflow command (`/rise`, `/care`, `/harvest`) runs this protocol before its first phase.

### Step 1: Distill the task signature

From the user's task, extract:

- **Category** — `CREATION` / `TRANSFORMATION` / `UNDERSTANDING` / `REPAIR` / `OPTIMIZATION`
- **Domain** — the domain module name or free-form domain label (`web_development`, `python_data`, `ai_tooling`, etc.)
- **Top 3-5 keywords** — lowercase, hyphenated where multi-word (`race-condition`, `event-ordering`, `auth-flow`)

### Step 2: Search `_index.jsonl`

If the file does not exist or is empty, note: *"No learnings store yet — proceeding without prior context."* and continue to Phase 1.

Otherwise, read the file (it is JSONL — one JSON object per line) and score each entry:

```
score(entry) =
    (entry.category == task.category ? 2 : 0)
  + (entry.domain == task.domain ? 2 : 0)
  + count(entry.problem_signature.keywords ∩ task.keywords)
```

Use any tool (Bash + Python, Read + manual scan, or PowerShell). The exact mechanism doesn't matter — what matters is the ranking.

### Step 3: Surface top 3 (with cutoff)

Take entries with `score ≥ 3`, sort by `(score desc, date desc)`, take top 3.

Present them to yourself before Phase 1, in the format:

> **Prior learnings (top {N}):**
> 1. **{date}** [{category}/{domain}, conf {n}/10] — {one-line summary derived from `generalization` field}
>    - What worked: {what_worked, truncated to ~120 chars}
>    - What failed: {what_failed, truncated to ~120 chars}

If no entry scores ≥ 3, note: *"No matching prior learnings."* and continue.

### Step 4: Use them — but verify

Prior learnings are *context*, not commandments. Specifically:

- **Trust the `generalization` field over `what_worked`** — what worked once may be specific; the generalization names the conditions.
- **Verify file paths, function names, flags before recommending them** — memories drift; code moves.
- **Consider conflicting learnings honestly** — if two entries disagree, the more recent + higher confidence wins, but flag the conflict.
- **A prior learning that says "X is wrong" is more durable than one that says "X is right"** — failure modes generalize better than success patterns.

---

## Closing Step — Write a Learning Entry (After Workflow Final Phase)

Run after every workflow completion. The decision is **whether to write**, not how.

### Step 1: Ask "did anything non-obvious surface?"

Write an entry if **any** of these are true:

- An assumption broke and required revision
- A non-obvious approach worked surprisingly well
- A common-looking task had a hidden constraint
- You'd want a future you to read this before doing similar work
- A prior learning from the store was invalidated or refined

Skip if:
- Task was routine — nothing new surfaced
- The insight is already in the store (search first)
- The insight is project-specific facts, not transferable methodology

**Discipline matters.** A store of 50 sharp entries beats a store of 500 routine ones. Quality over volume.

### Step 2: Construct the entry

Per `learnings/schema.json`. Required fields:

| Field | Source |
|---|---|
| `learning_id` | UUID4 you generate |
| `date` | Today's date, `YYYY-MM-DD` |
| `source_task_id` | The task_id from the telemetry session you just emitted, if any |
| `workflow` | The workflow you just ran |
| `category` / `domain` / `complexity` | From the classification done at task start |
| `problem_signature.keywords` | Same keywords you used for retrieval, refined if better keywords emerged from the work |
| `problem_signature.normalized` | `category|domain|sorted-keywords` joined by `|` |
| `what_worked` | Concrete decision/approach that produced the outcome |
| `what_failed` | What was tried and discarded, what assumptions broke. Use `"n/a"` only if truly nothing |
| `generalization` | The conditions under which this applies. The most important field. |
| `confidence` | 1-10 per FORGE Confidence Protocol — how sure are you this generalizes beyond this one task? |
| `source` | `telemetry-derived` if from a sessions.jsonl entry; `manual` if added directly; `post-mortem` if retrospective |

### Step 3: Append

Write exactly one JSON line (no trailing newline issues, no pretty-printing) to `learnings/_index.jsonl`. Use whatever shell tool fits your environment (Bash `>>`, PowerShell `Add-Content`, Python `open(..., 'a')`).

### Step 4: Optional — write a deep dive

If the learning is rich enough that 200 chars of `what_failed` undersells it, write a companion file at `learnings/<learning_id>.md` with the full story, and set `deep_dive_path` on the entry. Most learnings don't need this.

---

## Anti-patterns

These erode the store. Avoid:

| Anti-pattern | Why it hurts |
|---|---|
| Capturing project facts ("the API endpoint is at /v1/foo") | Belongs in code/docs, not learnings |
| Restating commit messages | Already in `git log` |
| "Use React hooks" — vague generalizations | No condition for when this applies; useless |
| Writing an entry for every task | Pollutes the store; retrieval surfaces noise |
| Confidence 10 on a single-case insight | Violates the Confidence Protocol; degrades trust in the store |
| Updating prior entries silently | Append, don't mutate. If a prior entry is wrong, write a new entry that supersedes it and reference the old `learning_id` in `tags`. |

---

## Future enhancements (v2+)

- **Embedding-based retrieval** when entry count exceeds ~100 — string matching becomes brittle at scale
- **`tools/forge_promote.py`** — interactively convert a flagged telemetry session into a learning entry
- **Cross-store search** — surface learnings from other operators if/when a shared community store emerges (requires schema interop work)
- **Learning decay** — weight recent learnings higher; archive entries that haven't matched any task in N months

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
