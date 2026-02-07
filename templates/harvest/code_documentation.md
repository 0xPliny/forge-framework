# HARVEST Template: Code Documentation

Use this template for **documenting existing code** automatically.

---

## Metadata

```yaml
framework: HARVEST
use_case: code-documentation
category: UNDERSTANDING
estimated_time: 5-30 minutes
domain: "[DOMAIN]"
```

---

## INPUT

### Target

- **File(s):**
- **Scope:** Function / Class / Module / System

### Context

- **Audience:** Developers / Users / Both
- **Purpose:** Reference / Tutorial / Onboarding
- **Existing docs:** None / Partial / Outdated

---

## HARVEST Loop

### Phase 1: HARVEST (Extract)

Automatically extract:

- [ ] Function signatures and parameters
- [ ] Class structures and methods
- [ ] Dependencies and imports
- [ ] Inline comments
- [ ] Error handling patterns

```bash
forge harvest [file] --extract
```

### Phase 2: ANALYZE (Understand)

Determine:

- [ ] Purpose of each component
- [ ] Relationships between components
- [ ] Data flow
- [ ] Key algorithms

### Phase 3: RESTRUCTURE (Organize)

Apply documentation layers:

- [ ] Layer 1: High-level overview
- [ ] Layer 2: Component details
- [ ] Layer 3: Usage examples

### Phase 4: VERIFY (Check)

Ensure:

- [ ] All public APIs documented
- [ ] Examples are accurate
- [ ] No missing components
- [ ] Terminology consistent

### Phase 5: EXTEND (Enrich)

Add:

- [ ] Usage examples
- [ ] Common patterns
- [ ] Gotchas/warnings
- [ ] See also references

### Phase 6: SYNTHESIZE (Combine)

Create:

- [ ] README section
- [ ] API reference
- [ ] Quick start guide

### Phase 7: TRANSFORM (Format)

Output in:

- [ ] Markdown
- [ ] JSDoc/TSDoc
- [ ] Docstrings
- [ ] Wiki format

---

## OUTPUT

### Generated Documentation

```markdown
# [Component Name]

## Overview
[Generated overview]

## Quick Start
[Generated quick start]

## API Reference

### [Function/Method Name]
**Purpose:** [Description]

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| | | |

**Returns:** [Type] - [Description]

**Example:**
\`\`\`
[Example code]
\`\`\`

## See Also
- [Related links]
```

---

## QUALITY CHECK

### Completeness

- [ ] All public APIs covered
- [ ] Examples provided
- [ ] Edge cases noted

### Accuracy

- [ ] Descriptions match behavior
- [ ] Examples work
- [ ] Types correct

### Cross-References

- [ ] Minimum 5+ cross-references per document
- [ ] Recommended 6-7 average (proven optimal)
- [ ] Grouped by category (Components, Configuration, Workflows)
- [ ] Use relative paths for portability
- [ ] Include anchor links for specific sections

**Cross-Reference Format:**
```markdown
## Related Documentation

### Components
- [Component Name](../path/to/component.md) - Brief description

### Configuration
- [Config Name](../path/to/config.md) - Brief description

### Workflows
- [Workflow Name](../path/to/workflow.md) - Brief description
```

### Quality Score

**Target:** 95%+
**Achieved:** ___

---

## OMEGA Learning

**Documentation patterns:**
-

**Commonly underdocumented:**
-

```bash
forge omega learn
```
