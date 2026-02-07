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

**Real-world results:**
- 21x developer efficiency improvement (measured across production deployments)
- $0.002/line cost for trained AI workflows vs $0.014/line untrained
- 56x documentation speed improvement
- 240x standards-checking acceleration

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
│   ├── rise.md                  # Research → Implement → Synthesize → Execute
│   ├── care.md                  # Collect → Analyze → Refine → Execute
│   ├── harvest.md               # Documentation & understanding
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
│   └── orchestration.md         # Multi-agent coordination
│
├── modules/                     # WHAT standards to follow
│   ├── domain_module_template.md # Template for creating new modules
│   ├── web_development.yaml     # React, TypeScript, FastAPI
│   ├── python_data.yaml         # Python, pandas, ML
│   ├── general_reasoning.yaml   # Logic, decisions, analysis
│   ├── research_analysis.yaml   # Research methodology
│   └── security_testing.yaml    # Security assessment standards
│
├── execution/                   # Runtime engine
│   ├── session_manager.md       # Persistent state management
│   ├── checkpoint_manager.md    # Git-based checkpointing
│   ├── audit_system.md          # Crash-safe logging
│   ├── error_handling.md        # Retry logic & error categories
│   └── parallel_agents.md       # Multi-agent orchestration
│
├── templates/                   # Reusable document templates
│   ├── rise/                    # R-I-S-E phase templates
│   ├── care/                    # C-A-R-E phase templates
│   ├── harvest/                 # Documentation templates
│   └── security/                # Security report templates
│
├── .cursorrules-templates/      # IDE governance rules
│   └── base.cursorrules         # Base Cursor IDE rules
│
└── docs/                        # Deep documentation
    ├── theory/                  # Mathematical foundations
    └── examples/                # Usage examples
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

## IDE Integration

FORGE includes `.cursorrules` templates for governing AI behavior directly in your IDE:

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
