# Example Learning Entries

Three curated examples with commentary on what makes each entry useful. Use these as a model when capturing your own learnings.

## What makes a good entry

- **Concrete `what_worked` / `what_failed`** — name the specific decision or assumption, not "tried things"
- **Generalization that names the conditions** — "When X and Y, prefer Z because W" beats "Z is good"
- **Honest confidence** — drop 2 points for unverified assumptions; never claim 9-10 without direct verification across multiple cases
- **Keywords future-you would actually search for** — what would you grep for if you hit this problem again?

## What makes a bad entry

- Restating what's already in the code or commit message
- Claiming a single-task insight "always" applies
- Vague generalizations ("be careful with X")
- Capturing project-specific facts (those belong in code/docs, not learnings)

---

## Example 1 — `what_failed` is the whole value

```json
{
  "schema_version": "1.0",
  "learning_id": "00000000-0000-0000-0000-000000000001",
  "date": "2026-05-10",
  "source_task_id": null,
  "workflow": "care",
  "category": "REPAIR",
  "domain": "python_data",
  "complexity": "Complex",
  "problem_signature": {
    "keywords": ["race-condition", "pipeline", "event-ordering", "locking"],
    "normalized": "REPAIR|python_data|event-ordering|locking|pipeline|race-condition"
  },
  "what_worked": "Treating the bug as event-ordering not contention. Added a sequence number to events at ingest and made the consumer assert monotonicity.",
  "what_failed": "First hypothesis: row-level locking. Spent 2 iterations adding locks before noticing reads were not the problem — writes from two producers were arriving out of order.",
  "generalization": "When a 'race condition' reproduces only under load with no shared mutable state, suspect event ordering before locking. Locks fix contention; sequencing fixes ordering. Distinguish before reaching for the wrong tool.",
  "applies_to": ["REPAIR:python_data", "REPAIR:any-pipeline-domain"],
  "confidence": 8,
  "source": "manual",
  "tags": ["concurrency", "pipeline", "diagnostic-pattern"]
}
```

**Why this is useful:** The `what_failed` field captures the wrong path so future-you doesn't repeat it. The generalization names the *condition that distinguishes* contention from ordering. Confidence 8 because it's been verified in this case but not yet generalized across multiple pipeline-domain bugs.

---

## Example 2 — Capturing a tool-environment gotcha

```json
{
  "schema_version": "1.0",
  "learning_id": "00000000-0000-0000-0000-000000000002",
  "date": "2026-05-10",
  "source_task_id": null,
  "workflow": "cross-cutting",
  "category": "cross-cutting",
  "domain": "tooling",
  "complexity": null,
  "problem_signature": {
    "keywords": ["windows", "python", "path", "microsoft-store-stub", "verification"],
    "normalized": "cross-cutting|tooling|microsoft-store-stub|path|python|verification|windows"
  },
  "what_worked": "Verified Python presence with `where.exe python` before recommending Python-based tools to the user.",
  "what_failed": "Initial assumption that `python --version` working = real Python installed. The Microsoft Store stub at C:\\Users\\<u>\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe responds to invocation but does not actually run scripts — it opens an install prompt.",
  "generalization": "On Windows, before recommending Python tools, verify with `where.exe python`. If the path is under `WindowsApps\\`, it is the Store stub, not a real interpreter. Real installs from python.org land at `C:\\Python*\\` or `AppData\\Local\\Programs\\Python\\`.",
  "applies_to": ["cross-cutting:windows-environment"],
  "confidence": 9,
  "source": "post-mortem",
  "tags": ["windows", "python", "environment-check"]
}
```

**Why this is useful:** Names the *exact path* of the trap (`WindowsApps\`), the *exact verification command* (`where.exe python`), and the *exact location* of real installs. Future-you grepping for `python|windows` finds this and avoids the loop.

---

## Example 3 — Methodology insight from framework work

```json
{
  "schema_version": "1.0",
  "learning_id": "00000000-0000-0000-0000-000000000003",
  "date": "2026-05-10",
  "source_task_id": null,
  "workflow": "harvest",
  "category": "UNDERSTANDING",
  "domain": "methodology",
  "complexity": "Complex",
  "problem_signature": {
    "keywords": ["framework-audit", "gap-analysis", "aspirational", "leverage"],
    "normalized": "UNDERSTANDING|methodology|aspirational|framework-audit|gap-analysis|leverage"
  },
  "what_worked": "When auditing a methodology framework for enhancements, separated 'aspirational gaps' (concept exists in prose but no working mechanism) from 'implementation gaps' (mechanism exists but could be polished). Prioritized aspirational.",
  "what_failed": "n/a — first attempt got it right, but only because the framing was made explicit. Without the distinction, would have ranked easy polish work above structural fixes.",
  "generalization": "When asked 'how should we improve this framework/system?', the highest-leverage moves are usually aspirational gaps — claims or concepts with no working mechanism. They are also the gaps most users miss because the surface looks complete. Always ask: what does this framework *claim* to do that it has no actual mechanism for?",
  "applies_to": ["UNDERSTANDING:methodology", "UNDERSTANDING:framework-design"],
  "confidence": 8,
  "source": "post-mortem",
  "tags": ["framework-design", "audit-pattern", "leverage"]
}
```

**Why this is useful:** Captures a *transferable diagnostic question* ("what does it claim to do that has no mechanism?"). Future-you reading this when asked to audit any framework gets the question pre-loaded.

---

## Anti-pattern: a bad entry

```json
{
  "what_worked": "Used React hooks",
  "what_failed": "n/a",
  "generalization": "Hooks are good"
}
```

**Why this is useless:** No specific decision named, no condition for when it applies, no insight that isn't in any React tutorial. Don't write entries like this — they pollute the store.
