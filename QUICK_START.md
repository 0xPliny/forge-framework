# FORGE Quick Start Guide

> Get productive with FORGE in 5 minutes.

---

## Step 1: Classify Your Problem

Ask yourself: **What am I trying to do?**

| If you want to... | Use this workflow |
|---|---|
| Build something new | **R-I-S-E** |
| Convert or migrate something | **R-I-S-E** |
| Fix a bug or improve performance | **C-A-R-E** |
| Document or understand something | **HARVEST** |

---

## Step 2: Load the Framework

Copy the entire content of [`FORGE_MASTER.md`](FORGE_MASTER.md) and paste it into your AI assistant as the first message in a new conversation.

**Works with:** Claude, ChatGPT, Gemini, Cursor, Windsurf, or any LLM-based tool.

---

## Step 3: State Your Problem

Just describe what you need. The framework will automatically:

1. Classify the problem type
2. Select the right workflow
3. Apply domain standards (if a module is loaded)
4. Execute phase by phase
5. Verify before delivering

### Examples

```
"Create a notification filtering system with React and TypeScript"
→ Classified as CREATION → R-I-S-E workflow → web_development module

"Fix the race condition in the order processing queue"
→ Classified as REPAIR → C-A-R-E workflow → general module

"Document how the authentication system works"
→ Classified as UNDERSTANDING → HARVEST workflow → architectural layer
```

---

## Step 4: Use a Persona (Optional)

For specialized work, load a persona instead of (or in addition to) the master framework:

| Persona | File | Best For |
|---|---|---|
| **Atlas** | `personas/atlas.md` | Deep research with sourced findings |
| **Sage** | `personas/sage.md` | System architecture and design decisions |
| **Scribe** | `personas/scribe.md` | Technical documentation at any level |
| **Sentinel** | `personas/sentinel.md` | Security assessment and testing |

Copy the persona file content and paste into your AI assistant.

---

## Step 5: Load Domain Standards (Optional)

If you work in a specific tech stack, load the relevant domain module:

```
DOMAIN: web_development
```

Available modules:
- `web_development` — React, TypeScript, FastAPI
- `python_data` — Python, pandas, ML
- `general_reasoning` — Logic, decisions, analysis
- `research_analysis` — Research methodology
- `security_testing` — Security assessments

**Create your own:** Copy `modules/domain_module_template.md` and fill in your stack's standards.

---

## What You Get

Every FORGE output includes:

- **Confidence scores** — How certain the AI is about each part
- **Assumption tracking** — What was assumed and the risk if wrong
- **Self-critique** — The AI challenges its own work before delivery
- **Verification** — Layered checking from syntax to human review
- **Learning capture** — Insights stored for future tasks

---

## Next Steps

- **Go deeper:** Read the workflow files in `workflows/`
- **Customize:** Create domain modules for your tech stack
- **Integrate:** Use `.cursorrules` templates for IDE governance
- **Contribute:** Submit domain modules, templates, or improvements

---

*FORGE: Framework for Orchestrated, Repeatable, Governed Engineering*
