# Methodology — Reproducing the FORGE Reported Figures

The main `README.md` reports four quantitative claims:

- **21x developer efficiency improvement**
- **$0.002/line cost** (trained AI workflows) vs **$0.014/line** (untrained)
- **56x documentation speed improvement**
- **240x standards-checking acceleration**

These are figures from one operator's deployments (Chase Logan's, across industrial automation, legacy modernization, and enterprise software). They are not independent benchmarks. This document defines the methodology to reproduce them in your own environment using the telemetry stack.

## Why this exists

The Confidence Protocol (`FORGE_MASTER.md` §5) demands rigor about evidence. The framework should hold itself to the same standard. Until you have your own telemetry, treat the headline figures as **directional**, not authoritative.

## How to reproduce in your own environment

### 1. Establish a baseline

Before adopting FORGE, measure 10 representative tasks **without** any framework — your normal workflow:

| Metric | How to measure |
|---|---|
| **Lines of working code per hour** | Wall time from task start to PR merge / lines added (excluding generated/boilerplate) |
| **Cost per line** | (Token cost + your hourly cost × wall time) / lines added |
| **Documentation pages per hour** | Wall time / pages produced at acceptable quality |
| **Standards-check time** | Wall time from "is this code compliant?" to verified answer |

Record manually. Tag as `baseline`.

### 2. Adopt FORGE

Install the [Claude Code integration](../integrations/claude-code/). Use `/rise`, `/care`, `/harvest` for the next 30 days of comparable tasks. Telemetry accumulates in `sessions.jsonl`.

### 3. Measure

Run `python tools/forge_report.py --days 30 --baseline baseline.csv`. The report compares the FORGE 30-day window against your baseline for each metric and produces:

| Metric | Baseline | With FORGE | Multiplier |
|---|---|---|---|
| Lines/hour | X | Y | Y/X |
| Cost/line | $A | $B | A/B |
| ... | | | |

### 4. Interpret honestly

A few notes on what these numbers do and don't mean:

- **Multipliers are domain-sensitive.** A 21x improvement on a well-understood codebase you've worked in for years will not generalize to a green-field project.
- **Survivorship bias matters.** Tasks where you abandoned mid-stream don't appear in either bucket. Track abandonment separately.
- **Quality is not in the multiplier.** Code that ships fast but breaks in prod is worse than code that ships slow and doesn't. Pair these metrics with downstream quality signals (bug rate, rework rate).
- **Claude model version moves.** Numbers from Claude Sonnet 3.5 don't apply to Claude Opus 4.7. Re-baseline when models change materially.

### 5. Publish (or don't)

If you reproduce these figures in your environment, your own data is more credible than this README. Replace the cited multipliers with your own numbers when you fork or document.

## What we don't yet measure (gaps)

The current telemetry schema captures workflow-level metrics. It does **not** yet capture:

- Wall time (requires the AI to record start/stop reliably; Plan: add to schema v1.1)
- Token cost (Claude Code may not always expose this from inside a slash command)
- Lines-of-code delta (would require a git-aware emitter)
- Quality signals downstream of merge (bug rate, rework)

These gaps matter. Until they're closed, the multipliers in the README cannot be fully reproduced from `sessions.jsonl` alone — you'll need to combine telemetry with manual measurement of the missing fields.

## Status of the headline claims

| Claim | Status |
|---|---|
| 21x developer efficiency | Reported by author. Reproducible via baseline → 30-day comparison once wall-time is in schema v1.1. |
| $0.002 vs $0.014 / line | Reported by author. Requires token-cost capture (planned). |
| 56x documentation speed | Reported by author. Reproducible for `/harvest` workflows once wall-time is captured. |
| 240x standards-checking | Reported by author. Domain-module-specific; methodology TBD. |

---

*This document exists because aspirational claims without methodology are anti-FORGE. Holding ourselves to the framework's own evidence standard.*
