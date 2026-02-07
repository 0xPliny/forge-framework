# HARVEST Workflow — Documentation & Knowledge Extraction

**Version:** 2.0 (Universal)
**Purpose:** Domain-agnostic systematic documentation and knowledge extraction methodology

---

## Overview

H-A-R-V-E-S-T is a 7-phase approach for **extracting knowledge from existing artifacts** and **transforming it into structured documentation**. It works for any domain; domain-specific standards are injected via modules.

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ HARVEST  │→ │ ANALYZE  │→ │RESTRUCTURE│→ │  VERIFY  │→ │  EXTEND  │→ │SYNTHESIZE│→ │TRANSFORM │
│ Extract  │  │ Patterns │  │ Template │  │ Accuracy │  │ Examples │  │  Links   │  │  Output  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
      ↑                                                                                   │
      └─────────────────────────── Iterate until 95%+ quality ────────────────────────────┘
```

---

## When to Use HARVEST

### Use HARVEST For:

- Documenting existing code, systems, or processes
- Extracting knowledge from legacy systems
- Creating reference documentation
- Building knowledge bases
- Onboarding documentation
- API documentation generation
- Understanding unfamiliar codebases

### Do NOT Use HARVEST For:

- Creating new systems (use R-I-S-E)
- Quick bug fixes (use C-A-R-E)
- Designing architecture (use R-I-S-E)
- Problems requiring implementation (use R-I-S-E or C-A-R-E)

---

## Phase 1: HARVEST (Extract)

**Goal:** Gather all raw information from source artifacts

**Maximum Duration:** 25% of total time budget

### Universal Steps

1. **Identify Source Artifacts**
   - Source code files
   - Existing documentation (even if outdated)
   - Configuration files
   - Database schemas
   - API specifications
   - Log files and error messages
   - Comments and inline documentation

2. **Extract Raw Information**
   - Function signatures and parameters
   - Class structures and relationships
   - Data types and schemas
   - Configuration keys and values
   - Dependencies and imports
   - Error codes and status values

3. **Catalog Entities**
   - Create list of all identifiable entities
   - Note entity types (process, table, function, config)
   - Record source location for each entity

4. **Flag Gaps**
   - What entities are referenced but not found?
   - What documentation is missing entirely?
   - What appears incomplete?

### HARVEST Checklist

- [ ] All source artifacts identified
- [ ] Entity list complete
- [ ] Entity types categorized
- [ ] Source locations recorded
- [ ] Gaps flagged for follow-up

---

## Phase 2: ANALYZE (Understand)

**Goal:** Understand structure, patterns, and relationships

**Maximum Duration:** 20% of total time budget

### Universal Steps

1. **Identify Structure** — How are entities organized? What is the hierarchy?
2. **Map Relationships** — Which entities call/use which? What are the data flows?
3. **Recognize Patterns** — What design patterns are used? What naming conventions exist?
4. **Determine Purpose** — Why does each entity exist? What would break without it?

---

## Phase 3: RESTRUCTURE (Organize)

**Goal:** Apply documentation template and organize content

**Maximum Duration:** 15% of total time budget

### Standard Document Structure

```markdown
# [Entity/Topic Name]

## Overview
[1-2 sentence description]

## Purpose
[Why this exists, what problem it solves]

## [Detail Sections - vary by entity type]

## Configuration
[If applicable]

## Error Handling
[If applicable]

## Examples
[Working examples]

## Troubleshooting
[Common issues and solutions]

## Related Documentation
[Cross-references]
```

---

## Phase 4: VERIFY (Validate)

**Goal:** Ensure accuracy against source material

**Maximum Duration:** 15% of total time budget

### Confidence Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| **High** | Verified directly from source | Code inspection, running tests |
| **Medium** | Inferred from context | Pattern matching, documentation |
| **Low** | Assumption based on limited info | Missing source, outdated docs |

---

## Phase 5: EXTEND (Enrich)

**Goal:** Add practical examples, edge cases, and troubleshooting

**Maximum Duration:** 10% of total time budget

- Add working examples (code snippets, queries, commands)
- Document edge cases and boundary conditions
- Add troubleshooting guidance
- Include non-obvious behaviors and common mistakes

---

## Phase 6: SYNTHESIZE (Connect)

**Goal:** Create cross-references and build the knowledge graph

**Maximum Duration:** 10% of total time budget

- Build entity index with searchable entries
- Inject cross-references (target: 5+ per document)
- Create navigation (table of contents, quick reference links)
- Generate relationship diagrams (Mermaid, ERDs, state machines)

---

## Phase 7: TRANSFORM (Output)

**Goal:** Generate final documentation in target format

**Maximum Duration:** 5% of total time budget

- Apply final formatting (syntax highlighting, table alignment)
- Generate output in target format (Markdown, HTML, PDF)
- Validate all links and references
- Run final quality check

---

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Completeness** | ≥ 95% | Entities documented / Total entities |
| **Accuracy** | ≥ 98% | Facts verified / Total facts |
| **Cross-references** | ≥ 5 per doc | Average links per document |
| **Consistency** | ≥ 90% | Style compliance score |

---

## HARVEST Quick Reference

```
HARVEST    → Extract raw information from all sources
ANALYZE    → Understand structure, patterns, relationships
RESTRUCTURE → Organize into documentation templates
VERIFY     → Cross-check against source material
EXTEND     → Add examples, edge cases, troubleshooting
SYNTHESIZE → Build cross-references and knowledge graph
TRANSFORM  → Generate final output in target format
```

**Remember:** Iterate until quality reaches 95%+. Each pass improves coverage and accuracy.

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
