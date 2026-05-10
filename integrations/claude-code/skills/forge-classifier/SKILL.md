---
name: forge-classifier
description: Classify engineering tasks per the FORGE framework taxonomy and recommend a workflow (R-I-S-E, C-A-R-E, or HARVEST) plus optional persona. Use proactively when the user describes any non-trivial engineering task — building something new, converting/migrating, fixing a bug, optimizing performance, documenting a system, or researching a topic — AND they have NOT already invoked /rise, /care, /harvest, /atlas, /sage, /scribe, or /sentinel. Suggest routing once per task; do not nag. Skip for conversational, trivial, or single-step asks.
---

# FORGE Task Classifier

## Purpose

Help the user route engineering tasks to the correct FORGE workflow and persona. **Suggest, don't execute** — the user picks whether to invoke the recommended slash command.

## When to invoke

✅ Invoke when the user describes an engineering task and hasn't already routed it via slash command.
❌ Skip when:
- The user already invoked `/rise`, `/care`, `/harvest`, `/atlas`, `/sage`, `/scribe`, or `/sentinel`
- Task is conversational ("hi", "what's this codebase about?")
- Task is trivial (rename a variable, run one command, answer yes/no, lookup a file)
- The user has explicitly asked you to skip routing for the session

## Step 1: Classify

Read `<FORGE_HOME>/FORGE_MASTER.md` (Section 1: Problem Classification) for the canonical taxonomy.

Determine:

| Field | Options |
|---|---|
| **Category** | CREATION \| TRANSFORMATION \| UNDERSTANDING \| REPAIR \| OPTIMIZATION |
| **Complexity** | Simple \| Medium \| Complex \| Expert |
| **Domain** | web_development \| python_data \| general_reasoning \| research_analysis \| security_testing \| other |
| **Confidence** | 1-10 in the classification |

Signal-word cheat sheet (from FORGE_MASTER.md §1):
- *create, build, implement, design* → CREATION
- *convert, migrate, refactor, port* → TRANSFORMATION
- *explain, analyze, document, research* → UNDERSTANDING
- *fix, debug, troubleshoot, resolve* → REPAIR
- *optimize, improve, enhance, speed up* → OPTIMIZATION

If classification confidence < 7, ask **one** clarifying question before recommending. Do not interrogate.

## Step 2: Map to workflow + persona

| Category | Workflow | Default persona suggestion |
|---|---|---|
| CREATION | `/rise` | `/sage` if architecture-heavy |
| TRANSFORMATION | `/rise` | `/sage` for redesign work |
| UNDERSTANDING | `/harvest` | `/atlas` for research, `/scribe` for docs |
| REPAIR | `/care` | — |
| OPTIMIZATION | `/care` | — |
| Security work (any category) | `/rise` or `/care` | `/sentinel` |

## Step 3: Recommend (one short message, then defer)

Output exactly this format, then stop:

> **FORGE classification:** {category} / {complexity} / {domain} (confidence {n}/10)
> **Suggested workflow:** `/{workflow}` — {one-sentence reason tied to the task}
> **Optional persona:** `/{persona}` if you want {specialty}.
>
> Or proceed without — your call.

Then **stop**. Do not invoke the slash command yourself. Do not re-suggest if the user proceeds without it. One classification per task is the rule.

## Edge cases

- **Ambiguous category** (e.g., "improve this so it also handles X" — could be OPTIMIZATION or CREATION): name both possibilities, recommend the dominant one.
- **Multiple categories in sequence** (e.g., "research best practices then build it"): suggest the first workflow only; user can re-route after.
- **User pushes back on classification**: defer immediately, do not argue. Their judgment overrides.
