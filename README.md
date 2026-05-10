<div align="center">

<pre align="center">
███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
█████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
  R E L I A B L E   A I   E N G I N E E R I N G
</pre>

### 🎯 Turn raw AI capability into reliable engineering output.

`status` &nbsp;🟢 **Stable v1.1** &nbsp;&nbsp; `license` &nbsp;📄 **Apache 2.0** &nbsp;&nbsp; `scope` &nbsp;🌐 **Open Source** &nbsp;&nbsp; `author` &nbsp;👤 **Chase Logan**

<p>
  <a href="https://github.com/0xPliny/forge-framework/stargazers"><img src="https://img.shields.io/github/stars/0xPliny/forge-framework?style=for-the-badge&logo=github&color=00d4ff&logoColor=white" alt="Stars"></a>
  <a href="https://github.com/0xPliny/forge-framework/network/members"><img src="https://img.shields.io/github/forks/0xPliny/forge-framework?style=for-the-badge&logo=github&color=00d4ff&logoColor=white" alt="Forks"></a>
  <a href="https://github.com/0xPliny/forge-framework/blob/main/LICENSE"><img src="https://img.shields.io/github/license/0xPliny/forge-framework?style=for-the-badge&color=00d4ff" alt="License"></a>
</p>

<p>
  <a href="FORGE_MASTER.md">📖 Master Spec</a> ·
  <a href="QUICK_START.md">⚡ Quick Start</a> ·
  <a href="integrations/claude-code/">🛠️ Claude Code</a> ·
  <a href="learnings/">🧠 OMEGA Loop</a> ·
  <a href="https://github.com/0xPliny/forge-framework/issues">💬 Issues</a>
</p>

<em>Structured workflows, governed personas, and a self-improving feedback loop —<br/>
for AI-assisted engineering that's repeatable and production-grade.</em>

</div>

---

## ✨ What is FORGE?

Most teams use AI as a chatbot — a clever autocomplete you re-prompt until something works. **FORGE** treats AI as an **engineering tool** with phase gates, confidence scoring, assumption tracking, and a learning loop that compounds across sessions.

Built on three pillars:

- 🔁 **Workflows** — `R-I-S-E` for creation, `C-A-R-E` for repair, `HARVEST` for understanding. Phase gates instead of ad-hoc prompting.
- 🎭 **Personas** — Atlas (research), Sage (architecture), Scribe (docs), Sentinel (security). Self-contained specialists with their own methodology.
- 🧠 **OMEGA Loop** — Telemetry log + curated learnings store. Every workflow queries prior insight at Phase 0 and writes new learnings at task close. Self-improvement is operational, not aspirational.

---

## 🎬 Demo

### See `/rise` in action

A real workflow run, condensed. The same pattern works for `/care` (repair) and `/harvest` (understanding).

```text
$ /rise Build a notification filtering system for industrial equipment alerts

╭──────────────────────────────────────────────────────────────────────────╮
│  FORGE  /  R-I-S-E Workflow                              confidence 8/10 │
╰──────────────────────────────────────────────────────────────────────────╯

▸ Phase 0  ·  Prior Learnings  ·  3 matches in learnings/
   • 2026-04-22  "Equipment alert systems benefit from priority queues over
                  flat queues — confirmed in 3 prior implementations"  9/10
   • 2026-03-11  "Industrial timeouts default ≥30s, not 5s like web norms —
                  radio relays + PLCs need wider windows"              8/10
   • 2026-02-04  "Isolate alert ingest from notification dispatch —
                  coupling caused cascade failures last project"       9/10

▸ Phase 1  ·  Research
   Functional      real-time ingest · severity classification · dedup
   Non-functional  <2s p99 dispatch · 99.9% uptime · audit trail
   Constraints     existing PostgreSQL · no message broker available
   Assumptions     4 tracked  (1 high-risk: dedup window = 60s)

▸ Phase 2  ·  Identify  (Tree of Thoughts: 3 approaches scored)
   A. Polling with PostgreSQL LISTEN/NOTIFY              7.2
   B. WAL-streaming via pg-logical-replication           8.1  ← selected
   C. Hybrid (poll + stream)                             6.8
   Reason: strong fit per prior learnings, lower latency

▸ Phase 3  ·  Synthesize
   Implementation outline + verification plan generated
   Verification layers required (Complex): 1 · 2 · 3 · 4

▸ Phase 4  ·  Execute
   ✓ Layer 1  formal       types · schema · lint
   ✓ Layer 2  automated    24 tests pass
   ✓ Layer 3  statistical  p99 = 1.4s under 10K alert/sec load
   ✓ Layer 4  ensemble     two implementations agree on dedup output

▸ Self-Critique
   Q: What might be wrong?    → Dedup window 60s is policy-doc derived;
                                 could change.  Flagged as high-risk.
   Q: Edge cases?             → Network partition during WAL replication
                                 needs test.

▸ Closing emissions
   → telemetry/sessions.jsonl    +1 entry   gates_passed: 8/8 · success
   → learnings/_index.jsonl      +1 entry   "WAL streaming for sub-2s
                                              industrial alerts: confirmed"
```

### Without FORGE vs With FORGE

| Same prompt — different rigor | ❌ Without FORGE | ✅ With FORGE |
|---|---|---|
| **Output** | "Here's a notification system: `[code]`" | Phase 0 retrieves 3 prior learnings · 4 phases with gates |
| **Confidence** | Implied | `8/10` with reasoning + caveats |
| **Assumptions** | Invisible | 4 tracked · 1 flagged high-risk |
| **Approaches considered** | One | Three scored via weighted matrix |
| **Verification** | If you remember to ask | Layers 1-4 mandatory for Complex tasks |
| **Self-critique** | Skipped | Required before delivery |
| **What worked?** | Lost when the chat scrolls away | Written to `learnings/` · queryable next time |

---

## 🚀 Features

- 🔁 **Three Workflows** — `R-I-S-E` (Research → Identify → Synthesize → Execute) for creation and transformation. `C-A-R-E` (Context → Analyze → Respond → Evaluate) for repair and optimization. `HARVEST` for documentation and knowledge extraction.
- 🎭 **Four Specialist Personas** — `Atlas` for deep research, `Sage` for architecture, `Scribe` for technical writing, `Sentinel` for security testing. Each is a self-contained role you load with a single command.
- ⚡ **Native Claude Code** — Slash commands `/rise`, `/care`, `/harvest`, plus `/atlas`, `/sage`, `/scribe`, `/sentinel`. A `forge-classifier` skill auto-suggests routing for unrouted tasks.
- 🧠 **OMEGA Loop** — `telemetry/sessions.jsonl` records every workflow invocation. `learnings/_index.jsonl` stores curated insights. Workflows retrieve prior learnings at Phase 0; new insights are appended at close. Grep-searchable from day one.
- 📊 **Honest Confidence** — Every meaningful output carries a 1-10 confidence score with reasoning and caveats. Drop 2 points per unverified assumption. Aggregate = minimum component.
- 🧩 **Domain Modules** — Pluggable standards for `web_development`, `python_data`, `general_reasoning`, `research_analysis`, `security_testing`. Inject mandatory checks per stack.
- 🔍 **5-Layer Verification** — Formal (types/lint) → Automated (tests) → Statistical (benchmarks) → Ensemble (multi-method agreement) → Human. Layers required scale with complexity.
- 🤝 **Multi-Agent Chains** — Atlas → Sage → Scribe → Sentinel for complex projects. Each persona inherits all FORGE protocols.

---

## ⚡ Quick Start

### 🌟 Option 1 — Native Claude Code  *(recommended)*

Install slash commands and the classifier skill at the user level so FORGE works across all your projects.

```powershell
# Windows
git clone https://github.com/0xPliny/forge-framework.git E:\forge-framework
Copy-Item E:\forge-framework\integrations\claude-code\commands\* "$env:USERPROFILE\.claude\commands\" -Recurse
Copy-Item E:\forge-framework\integrations\claude-code\skills\*   "$env:USERPROFILE\.claude\skills\"   -Recurse
```

```bash
# macOS / Linux
git clone https://github.com/0xPliny/forge-framework.git ~/forge-framework
cp -r ~/forge-framework/integrations/claude-code/commands/* ~/.claude/commands/
cp -r ~/forge-framework/integrations/claude-code/skills/*   ~/.claude/skills/
```

Then replace the `<FORGE_HOME>` placeholder in the copied files with your absolute path. Full instructions: [`integrations/claude-code/README.md`](integrations/claude-code/) →

In Claude Code, type `/` — you should see `/rise`, `/care`, `/harvest`, `/atlas`, `/sage`, `/scribe`, `/sentinel`. ✨

### 🤖 Option 2 — Any AI Assistant

Copy the contents of [`FORGE_MASTER.md`](FORGE_MASTER.md) and paste it as the first message in a new conversation with Claude / ChatGPT / Gemini / Cursor / Windsurf. The AI activates the full framework on read.

### 🧰 Option 3 — IDE Rules Files

Drop [`.cursorrules-templates/base.cursorrules`](.cursorrules-templates/base.cursorrules) into your project root for Cursor / Windsurf governance.

```yaml
# .cursorrules
framework: FORGE
workflow: auto-detect
domain_module: web_development
confidence_threshold: 7
verification: enabled
persona: sage
```

📘 [Complete getting-started guide →](QUICK_START.md)

---

## 🔄 How it works

```
╭─────────────╮      ╭─────────────╮      ╭─────────────╮      ╭─────────────╮
│  CLASSIFY   │ ───▶ │   EXECUTE   │ ───▶ │   VERIFY    │ ───▶ │    LEARN    │
│   Problem   │      │  Workflow   │      │  Solution   │      │   (OMEGA)   │
╰─────────────╯      ╰─────────────╯      ╰─────────────╯      ╰─────────────╯
       │                    │                    │                    │
       ▼                    ▼                    ▼                    ▼
  5 categories          R-I-S-E              5 layers           telemetry/
  + complexity          C-A-R-E             error → 0          + learnings/
  + domain              HARVEST                              (queried at Phase 0
                                                              of next task)
```

1. **🏷️ Classify** — Every task is sorted into one of 5 categories (CREATION, TRANSFORMATION, UNDERSTANDING, REPAIR, OPTIMIZATION) with a complexity tier and a domain. Confidence < 7 → AI asks before proceeding.
2. **⚙️ Execute** — The right workflow runs with phase gates. Assumptions are tracked, confidence is scored on every output, and high-risk assumptions must be validated before late-phase work.
3. **🔍 Verify** — Verification layers required scale with complexity (1-2 for Simple, 1-5 for Expert). No skipping the stack.
4. **🧠 Learn** — Telemetry line emitted at task close. If something non-obvious surfaced, a learning entry is written. The next task starts by querying that store.

---

## 🔁 Workflows

| Workflow | When to use | What you get |
|---|---|---|
| 🟢 **R-I-S-E** | Build, design, migrate, refactor | Research brief → Tree-of-Thoughts approaches → scored selection → verified deliverable |
| 🟡 **C-A-R-E** | Bugs, performance, optimization | Reproducible problem → root cause → fix verified against baseline → no regressions |
| 🔵 **HARVEST** | Documentation, codebase comprehension, knowledge extraction | Layered docs (executive / architectural / implementation) at 95%+ quality |

📂 [Workflow specs →](workflows/)

---

## 🎭 Personas

| Persona | Role | Methodology | Best for |
|---|---|---|---|
| 🔭 **Atlas** | Deep Research | HARVEST + ReAct | Comprehensive sourced research |
| 🏛️ **Sage** | Architecture | R-I-S-E + Tree of Thoughts | System design with trade-offs |
| ✍️ **Scribe** | Documentation | HARVEST + Meta-Prompting | Tech writing for any audience |
| 🛡️ **Sentinel** | Security | R-I-S-E + C-A-R-E | OWASP / CVSS vulnerability work |

Each is a self-contained prompt — paste the file or invoke the slash command. 📂 [Persona library →](personas/)

---

## 🎯 Where FORGE shines

- 🏭 **Industrial automation** — Equipment alerting, dispatcher systems, PLC-adjacent integrations where wide timeouts and explicit assumptions matter
- 🔧 **Legacy modernization** — HARVEST extracts knowledge from old codebases; R-I-S-E + Sage designs the replacement; Sentinel audits the result
- 🛡️ **Security assessments** — Sentinel + R-I-S-E walks OWASP Top 10 with CVSS scoring and reproducible PoCs
- 📚 **Documentation generation** — HARVEST + Scribe produces layered docs from any codebase at 95%+ accuracy with confidence scores per claim
- 🤝 **Multi-agent orchestration** — Chain Atlas → Sage → Scribe → Sentinel with state passed via the persona contract
- ⚖️ **Compliance-driven work** — Confidence Protocol + Assumption Tracking produce the audit trail that policy-bound teams need

---

## 🧠 OMEGA: the self-improvement loop

The framework's central claim — that error rate converges over iterations — is operationalized by two persistent stores plus a small Python toolchain:

| Layer | Purpose | Where |
|---|---|---|
| 📊 **Telemetry** | Every workflow invocation: classification, gates, assumptions, iterations, outcome | [`telemetry/`](telemetry/) |
| 🧠 **Learnings** | Curated insights — only when something non-obvious surfaced. Queried at Phase 0. | [`learnings/`](learnings/) |
| 🛠️ **Tools** | `forge_eval.py` (single-session scorer) · `forge_report.py` (N-day aggregator) | [`tools/`](tools/) |

The retrieval and write contract lives in [`core/omega_retrieval.md`](core/omega_retrieval.md). Both stores stay local by default — your learnings reflect your work and aren't designed to ship.

---

## 📊 Reported results

> ⚠️ These figures are from the framework author's deployments across industrial automation, legacy modernization, and enterprise software — directional, not independently benchmarked.

- 🚀 **21x** developer efficiency improvement
- 💰 **$0.002 / line** for trained AI workflows vs **$0.014 / line** untrained
- 📚 **56x** documentation speed improvement
- ⚡ **240x** standards-checking acceleration

Reproduce them in your environment with the [telemetry stack](telemetry/) — see [`telemetry/METHODOLOGY.md`](telemetry/METHODOLOGY.md) for the measurement protocol.

---

## 📚 Documentation

- 📖 [`FORGE_MASTER.md`](FORGE_MASTER.md) — Complete framework, paste into any AI →
- ⚡ [`QUICK_START.md`](QUICK_START.md) — 5-minute getting started →
- 🔁 [`workflows/`](workflows/) — R-I-S-E, C-A-R-E, HARVEST specs + error handling →
- 🎭 [`personas/`](personas/) — Atlas, Sage, Scribe, Sentinel →
- 🧬 [`core/`](core/) — Confidence protocol, assumption tracker, meta-prompting, OMEGA retrieval →
- 🧩 [`modules/`](modules/) — Domain standards (web, python_data, security, etc.) →
- 📊 [`telemetry/`](telemetry/) — Schema, privacy, methodology →
- 🧠 [`learnings/`](learnings/) — Schema, retrieval contract, examples →
- 🛠️ [`integrations/claude-code/`](integrations/claude-code/) — Native slash commands + classifier skill →

---

## 🛠️ Tools

### FORGE Docs — AI Documentation Engine

[![FORGE Docs](https://img.shields.io/badge/FORGE_Docs-Live_Demo-00e5ff?style=for-the-badge)](https://0xpliny.github.io/ai-documentation-toolkit/)

Generate comprehensive, structured documentation for any codebase using GPT-4 and the HARVEST workflow.

🌐 [Try it →](https://0xpliny.github.io/ai-documentation-toolkit/) &nbsp;·&nbsp; 💾 [Source →](https://github.com/0xPliny/ai-documentation-toolkit)

---

## 💬 Community

### 🆘 Have questions or hit a snag?

- 🐛 File an [issue →](https://github.com/0xPliny/forge-framework/issues)
- 📖 Read the [Master Spec →](FORGE_MASTER.md)

### 🤝 Contributing

FORGE is intentionally minimal at the core but extensible at the edges. Good first contributions:

- 🧩 **New domain modules** — Use [`modules/domain_module_template.md`](modules/domain_module_template.md) for your stack
- 🎭 **Additional personas** — Follow the structure of [`personas/atlas.md`](personas/atlas.md)
- 📋 **Workflow templates** — Add to `templates/rise/`, `templates/care/`, `templates/harvest/`
- 🔌 **Integrations** — Add a directory under `integrations/` (Cursor rules, JetBrains, Vim, etc.)

PRs welcome. Open an issue first for substantial changes.

---

## 📜 License

[Apache 2.0](LICENSE) — Use it, extend it, build on it.

---

## 👤 About

FORGE was developed by **[Chase Logan](https://github.com/0xPliny)** through hands-on experience deploying AI-driven engineering workflows across industrial automation and enterprise software. It distills domain-agnostic patterns for making AI a reliable engineering partner — not just a code generator.

🌐 [GitHub →](https://github.com/0xPliny) &nbsp;·&nbsp; 🏷️ Framework v1.1

<div align="center">

---

*FORGE: because AI without governance is just expensive autocomplete.* ⚙️

</div>
