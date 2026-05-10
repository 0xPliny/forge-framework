<p align="center">
  <a href="https://github.com/0xPliny/forge-framework">
    <img src="assets/forge-banner-dark.png" alt="FORGE Framework Banner">
  </a>
</p>

<p align="center">
    <a href="https://github.com/0xPliny/forge-framework/stargazers"><img src="https://img.shields.io/github/stars/0xPliny/forge-framework?style=for-the-badge&logo=github&color=00d4ff&logoColor=white" alt="Stars"></a>
    <a href="https://github.com/0xPliny/forge-framework/network/members"><img src="https://img.shields.io/github/forks/0xPliny/forge-framework?style=for-the-badge&logo=github&color=00d4ff&logoColor=white" alt="Forks"></a>
    <a href="https://github.com/0xPliny/forge-framework/blob/main/LICENSE"><img src="https://img.shields.io/github/license/0xPliny/forge-framework?style=for-the-badge&color=00d4ff" alt="License"></a>
</p>

# FORGE — Framework for Orchestrated, Repeatable, Governed Engineering

> **Turn raw AI capability into reliable engineering output.**

FORGE is a structured methodology for integrating AI into real engineering workflows. It provides universal thinking patterns, pluggable domain standards, AI personas, and self-improving feedback loops — all designed to make AI-assisted development **repeatable, governed, and production-grade**.

Created by **Chase Logan** — built from real-world experience deploying AI across industrial automation, legacy modernization, and enterprise software engineering.

---

## Why FORGE?

Most teams use AI as a chatbot. FORGE treats AI as an **engineering tool** with:

- **Structured workflows** — not ad-hoc prompting
- **Domain-specific standards** — not generic suggestions
- **Governance and verification** — not blind trust
- **Measurable outcomes** — not anecdotal wins

**Reported results from the framework author's deployments:**
- 21x developer efficiency improvement
- $0.002/line cost for trained AI workflows vs $0.014/line untrained
- 56x documentation speed improvement
- 240x standards-checking acceleration

These figures are from one operator's deployments across industrial automation, legacy modernization, and enterprise software — directional, not independently benchmarked. Reproduce them in your own environment with the [telemetry stack](telemetry/); see [`telemetry/METHODOLOGY.md`](telemetry/METHODOLOGY.md) for the measurement protocol.

---

## Quick Start

### 1. Choose Your Workflow

| Problem Type | Workflow | When to Use |
|---|---|---|
| **Build something new** | **R-I-S-E** | Creation, design, new features |
| **Fix or optimize** | **C-A-R-E** | Bugs, refactoring, performance |
| **Understand or document** | **HARVEST** | Documentation, research, analysis |

### 2. Load the Framework

Copy the content of [`FORGE_MASTER.md`](FORGE_MASTER.md) into any AI assistant (Claude, ChatGPT, Gemini, Cursor, Windsurf) to activate the full framework.

### 3. State Your Problem

```
"Create a REST API for inventory management with proper error handling"
```

### 4. The Framework Handles the Rest

- Classifies your problem automatically
- Selects the optimal workflow
- Applies domain standards
- Verifies the solution before delivery

---

## Framework Architecture

```
FORGE/
├── README.md                    # You are here
├── FORGE_MASTER.md              # Complete framework — paste into any AI
├── QUICK_START.md               # 5-minute getting started guide
│
├── workflows/                   # HOW to think
│   ├── rise.md                  # Research → Identify → Synthesize → Execute
│   ├── care.md                  # Context → Analyze → Respond → Evaluate
│   ├── harvest.md               # Documentation & knowledge extraction
│   ├── omega_loop.md            # Self-improving feedback loop
│   ├── problem_classifier.md    # Automatic problem categorization
│   ├── verification.md          # 5-layer correctness stack
│   ├── tree_of_thoughts.md      # Multi-path exploration
│   └── react_integration.md     # Reasoning + Acting loops
│
├── personas/                    # WHO does the work
│   ├── atlas.md                 # Deep Research specialist
│   ├── sage.md                  # Architecture & system design
│   ├── scribe.md                # Technical documentation
│   └── sentinel.md              # Security testing
│
├── core/                        # Enhancement layers
│   ├── meta_prompting.md        # Self-critique before delivery
│   ├── confidence_protocol.md   # Explicit confidence scoring
│   ├── assumption_tracker.md    # Track and validate assumptions
│   ├── orchestration.md         # Multi-agent coordination
│   └── omega_retrieval.md       # Persistent learnings query + write protocol
│
├── modules/                     # WHAT standards to follow
│   ├── domain_module_template.md
│   ├── web_development.yaml
│   ├── python_data.yaml
│   ├── general_reasoning.yaml
│   ├── research_analysis.yaml
│   └── security_testing.yaml
│
├── execution/                   # Runtime engine
│   ├── session_manager.md
│   ├── checkpoint_manager.md
│   ├── audit_system.md
│   └── error_handling.md
│
├── templates/                   # Reusable document templates
│   ├── rise/, care/, harvest/, security/, omega/
│
├── telemetry/                   # OMEGA: mechanical session log
│   ├── schema.json              # JSON Schema for sessions.jsonl
│   ├── README.md                # Privacy, opt-out, usage
│   ├── METHODOLOGY.md           # How to reproduce the README's headline figures
│   └── sessions.jsonl           # Append-only log (gitignored — local only)
│
├── learnings/                   # OMEGA: curated insights
│   ├── schema.json              # JSON Schema for learning entries
│   ├── README.md                # Schema + retrieval contract + when-to-write
│   ├── EXAMPLES.md              # Curated examples for upstream users
│   └── _index.jsonl             # Append-only learnings (gitignored)
│
├── tools/                       # Python stdlib tools (no deps)
│   ├── forge_eval.py            # Score a single session against FORGE gates
│   └── forge_report.py          # Aggregate telemetry over N days
│
├── integrations/                # IDE / runtime integrations
│   ├── browser_automation.md
│   ├── mcp_integration.md
│   ├── tool_validation.md
│   └── claude-code/             # Native Claude Code: slash commands + skill
│       ├── README.md            # Install instructions (~/.claude/...)
│       ├── commands/            # /rise, /care, /harvest, /atlas, /sage, /scribe, /sentinel
│       └── skills/forge-classifier/SKILL.md  # Auto-suggests routing
│
├── .cursorrules-templates/      # IDE governance rules
│   └── base.cursorrules
│
└── docs/                        # Built docs site (gh-pages source)
```

---

## The Core Loop

```
┌────────────┐      ┌────────────┐      ┌────────────┐      ┌────────────┐
│  CLASSIFY  │ ──→  │  EXECUTE   │ ──→  │   VERIFY   │ ──→  │   LEARN    │
│  Problem   │      │  Workflow  │      │  Solution  │      │  (OMEGA)   │
└────────────┘      └────────────┘      └────────────┘      └────────────┘
      │                  │                    │                    │
      ▼                  ▼                    ▼                    ▼
┌────────────┐   ┌─────────────────┐   ┌────────────┐      ┌────────────┐
│ 5 Categories│   │ R-I-S-E        │   │ 5 Layers   │      │ Knowledge  │
│ + Domain    │   │ C-A-R-E        │   │ Error → 0  │      │ Base       │
│ + Complexity│   │ HARVEST        │   └────────────┘      └────────────┘
└────────────┘   └─────────────────┘
```

---

## Workflows

### R-I-S-E (Research → Implement → Synthesize → Execute)

For **creation and transformation** problems. Thorough, research-first approach.

| Phase | Purpose | Output |
|---|---|---|
| **Research** | Understand requirements, constraints, prior art | Research brief |
| **Implement** | Build the solution with domain standards | Working code/artifact |
| **Synthesize** | Integrate, test, refine | Verified deliverable |
| **Execute** | Deploy, document, hand off | Production-ready output |

### C-A-R-E (Collect → Analyze → Refine → Execute)

For **repair and optimization** problems. Fast, iterative approach.

| Phase | Purpose | Output |
|---|---|---|
| **Collect** | Gather context, reproduce issue | Problem statement |
| **Analyze** | Root cause analysis | Diagnosis |
| **Refine** | Develop and test fix | Verified solution |
| **Execute** | Apply fix, verify no regressions | Resolved issue |

### HARVEST (Documentation & Understanding)

For **understanding** problems. Systematic knowledge extraction.

Extracts structured documentation from any codebase, system, or domain — producing layered output from executive summary to implementation details.

---

## Personas

Specialized AI personalities that integrate FORGE workflows:

| Persona | Role | Methodology | Best For |
|---|---|---|---|
| **Atlas** | Deep Research | HARVEST + ReAct | Comprehensive research with sources |
| **Sage** | Architecture | R-I-S-E + Tree of Thoughts | System design with trade-off analysis |
| **Scribe** | Documentation | HARVEST + Meta-Prompting | Technical writing for any audience |
| **Sentinel** | Security | R-I-S-E + C-A-R-E | Vulnerability identification |

Each persona is a **self-contained prompt** — paste into any AI assistant to activate.

---

## Domain Modules

Pluggable standards that inject domain-specific rules into any workflow:

| Module | Domain | Key Standards |
|---|---|---|
| `web_development` | React/TypeScript/FastAPI | Type safety, error handling, accessibility |
| `python_data` | Python/ML/Data Science | Type hints, reproducibility, validation |
| `general_reasoning` | Decisions & analysis | Assumptions, multiple perspectives |
| `research_analysis` | Research methodology | Source citation, limitations |
| `security_testing` | Security assessments | OWASP methodology, CVSS scoring |

**Create your own:** Use `modules/domain_module_template.md` to build domain modules for your specific tech stack, industry, or codebase.

---

## The OMEGA Loop (Self-Improvement)

Every task feeds back into the knowledge base:

```
OBSERVE → MODEL → EXECUTE → GENERATE → ANALYZE → LEARN → (repeat)
```

**Key property:** Error rate converges to zero over iterations.

```
Error(n) = Error(0) × (1 - learning_rate)^n

After 5 iterations:  40% error → 13% error
After 10 iterations: 40% error → 4% error
After 20 iterations: 40% error → 0.5% error
```

---

## 5-Layer Verification Stack

```
Layer 5: Human Judgment    → Final arbiter
Layer 4: Ensemble          → Multiple methods agree (99%+)
Layer 3: Statistical       → Benchmarks, metrics (90%+)
Layer 2: Automated Testing → Tests pass (95%+)
Layer 1: Formal            → Types, syntax, linting (100%)

Combined: 99.9%+ correctness for well-defined problems
```

---

## Tools

### FORGE Docs — AI Documentation Engine

[![FORGE Docs](https://img.shields.io/badge/FORGE_Docs-Live_Demo-00e5ff?style=for-the-badge)](https://0xpliny.github.io/ai-documentation-toolkit/)

Generate comprehensive, structured documentation for any codebase using GPT-4 and the HARVEST workflow. Three-panel dark industrial UI with animated pipeline visualization.

**[Try it →](https://0xpliny.github.io/ai-documentation-toolkit/)** | **[Source Code](https://github.com/0xPliny/ai-documentation-toolkit)**

---

## IDE Integration

### Claude Code (native)

Slash commands and a classifier skill that remove the "paste FORGE_MASTER.md into chat" friction. Once installed, invoke workflows and personas as first-class commands:

```
/rise build a notification filtering system
/care fix the race condition in the order queue
/harvest document the auth subsystem
/atlas DEEP technical — "warehouse automation patterns"
/sage FULL — "real-time notification system for 1M users"
```

The `forge-classifier` skill auto-suggests routing for unrouted tasks — describe a task without a slash command and it recommends one.

Install: see [`integrations/claude-code/README.md`](integrations/claude-code/).

### Cursor / Windsurf / other rules-file IDEs

FORGE includes `.cursorrules` templates for governing AI behavior:

```yaml
# .cursorrules example
framework: FORGE
workflow: auto-detect
domain_module: web_development
confidence_threshold: 7
verification: enabled
persona: sage
```

Works with **Cursor**, **Windsurf**, and any AI-assisted IDE that supports rules files.

---

## OMEGA: Operational Stack

The OMEGA loop (self-improvement) is operationalized by two persistent stores plus a small Python toolchain:

| Layer | What it does | Where |
|---|---|---|
| **Telemetry** | Mechanical log: every workflow invocation — classification, gates, assumptions, iterations, outcome | [`telemetry/sessions.jsonl`](telemetry/) |
| **Learnings** | Curated insights — only when something non-obvious surfaced. Queried at Phase 0 of every workflow. | [`learnings/_index.jsonl`](learnings/) |
| **Tools** | `forge_eval.py` (single-session scorer) + `forge_report.py` (N-day aggregator) | [`tools/`](tools/) |

The retrieval + write contract is in [`core/omega_retrieval.md`](core/omega_retrieval.md). With these stores active, workflow invocations compound prior insight instead of starting cold every time.

---

## Getting Started

1. **Read** [`QUICK_START.md`](QUICK_START.md) — 5 minutes
2. **Load** [`FORGE_MASTER.md`](FORGE_MASTER.md) into your AI assistant
3. **Pick a persona** from `personas/` for specialized work
4. **Create a domain module** for your tech stack using the template

---

## License

[Apache 2.0](LICENSE) — Use it, extend it, build on it.

---

## About

FORGE was developed by **Chase Logan** through hands-on experience deploying AI-driven engineering workflows across industrial automation and enterprise software. It represents a distilled, domain-agnostic methodology for making AI a reliable engineering partner — not just a code generator.

- **GitHub:** [github.com/0xPliny](https://github.com/0xPliny)
- **Framework:** FORGE v1.0

---

*FORGE: Because AI without governance is just expensive autocomplete.*
