# HARVEST Template: Legacy Code Analysis

Use this template for **understanding and documenting legacy/unfamiliar code**.

---

## Metadata

```yaml
framework: HARVEST
use_case: legacy-analysis
category: UNDERSTANDING
estimated_time: 30-120 minutes
domain: "[DOMAIN]"
```

---

## INPUT

### Target

- **Codebase:**
- **Entry point:**
- **Size:** Lines / Files

### Why

- [ ] New to project
- [ ] Need to modify
- [ ] Need to document
- [ ] Need to replace

---

## HARVEST Loop

### Phase 1: HARVEST (Surface Scan)

```bash
# Get structure overview
find . -name "*.py" | head -50
# Or for your language
```

**Findings:**

- File count:
- Main directories:
- Entry point:
- Config files:

### Phase 2: ANALYZE (Deep Dive)

#### Architecture

```
[Draw high-level structure as you understand it]
```

#### Key Components

| File/Module | Purpose | Dependencies |
|-------------|---------|--------------|
| | | |

#### Data Flow

```
[Input] → [Processing] → [Output]
```

#### Database/Storage

- Tables/Collections:
- Key relationships:

### Phase 3: RESTRUCTURE (Mental Model)

#### System Purpose
>
> [In one sentence, what does this system do?]

#### Core Concepts

| Concept | Definition | Where |
|---------|------------|-------|
| | | |

#### Critical Paths

1. **Path A:** [Most important flow]
2. **Path B:** [Second important flow]

### Phase 4: VERIFY (Validate Understanding)

- [ ] Can trace main user flow
- [ ] Understand data model
- [ ] Know where key logic lives
- [ ] Identified potential issues

### Phase 5: EXTEND (Add Context)

#### Historical Notes

- Original purpose:
- Major changes:
- Known issues:

#### Tribal Knowledge

- [Things not in the code]

### Phase 6: SYNTHESIZE (Document)

#### Quick Reference

```markdown
## [System Name]

**Purpose:** [What it does]
**Stack:** [Technologies]
**Entry:** [Where to start]

### Key Files
- `file1.py` - [Purpose]
- `file2.py` - [Purpose]

### Critical Functions
- `function_name()` - [What it does]

### Database Tables
- `table_name` - [Purpose]

### Common Tasks
- To do X: [Steps]
- To do Y: [Steps]
```

### Phase 7: TRANSFORM (Useful Outputs)

- [ ] README.md created/updated
- [ ] Architecture diagram
- [ ] Onboarding guide
- [ ] Known issues list

---

## OUTPUT

### System Overview

[Paste your synthesized documentation here]

### Architecture Diagram

```
[ASCII or Mermaid diagram]
```

### Recommended Next Steps

1.
2.
3.

---

## OMEGA Learning

**Codebase patterns discovered:**
-

**Anti-patterns found:**
-

**Documentation gap patterns:**
-

```bash
forge omega learn
```
