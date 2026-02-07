# Tree of Thoughts (ToT) Framework

> **When to Use:** Complex problems with multiple valid approaches, strategic planning, or when the first solution path might fail.

## Overview

Tree of Thoughts extends Chain-of-Thought by exploring **multiple reasoning paths simultaneously**, evaluating each, and selecting the optimal path. Unlike linear reasoning, ToT allows backtracking and course correction.

```
                    [Problem]
                        │
           ┌────────────┼────────────┐
           ▼            ▼            ▼
       [Path A]     [Path B]     [Path C]
           │            │            │
        Evaluate     Evaluate     Evaluate
           │            │            │
         Score:7     Score:9      Score:4
           │            │            │
           └────────────┼────────────┘
                        │
                   [Select B]
                        │
                   [Develop B]
                        │
                   [Solution]
```

---

## The ToT Process

### Phase 1: DECOMPOSE
Break the problem into intermediate steps that can be evaluated independently.

```markdown
PROBLEM: [State the problem]

DECOMPOSITION:
- Step 1: [First intermediate goal]
- Step 2: [Second intermediate goal]
- Step 3: [Third intermediate goal]
- Final: [End state]

EVALUATION CRITERIA:
- Criterion 1: [How to measure success]
- Criterion 2: [How to measure success]
- Criterion 3: [How to measure success]
```

### Phase 2: BRANCH
Generate multiple distinct approaches for the first step.

```markdown
BRANCHING (Step 1):

PATH A: [Approach 1]
- Description: [What this approach does]
- Assumptions: [What must be true]
- Risk: [What could go wrong]

PATH B: [Approach 2]
- Description: [What this approach does]
- Assumptions: [What must be true]
- Risk: [What could go wrong]

PATH C: [Approach 3]
- Description: [What this approach does]
- Assumptions: [What must be true]
- Risk: [What could go wrong]
```

### Phase 3: EVALUATE
Score each path against criteria. Use explicit ratings.

```markdown
EVALUATION MATRIX:

| Path | Feasibility | Risk | Time | Quality | TOTAL |
|------|-------------|------|------|---------|-------|
| A    | 7/10        | 6/10 | 8/10 | 7/10    | 28/40 |
| B    | 9/10        | 8/10 | 7/10 | 9/10    | 33/40 |
| C    | 5/10        | 4/10 | 9/10 | 6/10    | 24/40 |

ASSESSMENT:
- Path A: [Why this score]
- Path B: [Why this score] ← HIGHEST
- Path C: [Why this score]
```

### Phase 4: PRUNE
Eliminate paths that score below threshold or have critical flaws.

```markdown
PRUNING DECISION:

THRESHOLD: 27/40 minimum

ELIMINATED:
- Path C (24/40): Below threshold, high risk of [specific issue]

REMAINING:
- Path A (28/40): Viable backup
- Path B (33/40): Primary path

RATIONALE: [Why these decisions make sense]
```

### Phase 5: EXPLORE
Develop the top path(s) one level deeper. Repeat branching if needed.

```markdown
EXPLORING PATH B:

Step 1 (Path B): [Execute first step]
Result: [What we learned]

BRANCHING (Step 2 from Path B):

PATH B1: [Sub-approach 1]
PATH B2: [Sub-approach 2]

EVALUATION:
- B1: [Score and rationale]
- B2: [Score and rationale]

SELECTED: B2

[Continue until solution reached]
```

### Phase 6: CONVERGE
Synthesize the final solution from the explored path.

```markdown
CONVERGENCE:

SELECTED PATH: B → B2 → [final steps]

SOLUTION:
[Complete solution description]

CONFIDENCE: [1-10]

ALTERNATIVE (if primary fails):
Path A provides fallback with [trade-offs]
```

---

## ToT Decision Tree

```
Is the problem complex with multiple valid approaches?
├── NO → Use standard R-I-S-E or C-A-R-E
└── YES → Continue
    │
    Can the problem be decomposed into evaluable steps?
    ├── NO → Use HARVEST for understanding first
    └── YES → Continue
        │
        Is there risk of going down a wrong path?
        ├── NO → Use Chain-of-Thought (linear)
        └── YES → Use Tree of Thoughts
```

---

## Integration with FORGE

### When Problem Classifier Returns "Complex"

```yaml
classification:
  category: CREATION
  complexity: COMPLEX
  framework: R-I-S-E
  enhancement: TREE_OF_THOUGHTS  # Add ToT layer
```

### ToT + R-I-S-E Integration

```
R-I-S-E with ToT Enhancement:

RESEARCH:
  - Standard research phase
  
IDENTIFY:
  - Identify multiple possible approaches (BRANCH)
  - Evaluate each approach (EVALUATE)
  - Select top approaches (PRUNE)
  
SYNTHESIZE:
  - Develop selected approach (EXPLORE)
  - Create fallback plan from runner-up
  
EXECUTE:
  - Implement primary path
  - Monitor for need to switch to fallback
```

---

## Example: Database Migration Strategy

### Problem
Migrate legacy SQL Server database to PostgreSQL while maintaining zero downtime.

### ToT Application

**DECOMPOSE:**
- Step 1: Schema conversion
- Step 2: Data migration
- Step 3: Application cutover
- Step 4: Validation

**BRANCH (Step 2: Data Migration):**

| Path | Approach | Description |
|------|----------|-------------|
| A | Big Bang | Stop writes, migrate all data, restart |
| B | Dual Write | Write to both DBs during transition |
| C | CDC Stream | Use Change Data Capture for continuous sync |

**EVALUATE:**

| Path | Downtime | Complexity | Risk | Rollback | TOTAL |
|------|----------|------------|------|----------|-------|
| A    | 2/10     | 8/10       | 3/10 | 9/10     | 22/40 |
| B    | 8/10     | 5/10       | 6/10 | 7/10     | 26/40 |
| C    | 9/10     | 4/10       | 7/10 | 8/10     | 28/40 |

**PRUNE:**
- Eliminate Path A (requires downtime, violates requirement)

**EXPLORE Path C:**
- Sub-branch: Debezium vs. custom CDC
- Evaluate: Debezium (mature, supported) wins

**CONVERGE:**
- Solution: CDC with Debezium, dual-write validation period, automated cutover

---

## Quality Gates for ToT

Before accepting a ToT solution:

- [ ] At least 3 paths were considered
- [ ] Evaluation criteria were explicit and measurable
- [ ] Pruning decisions have clear rationale
- [ ] A fallback path exists
- [ ] Confidence level is stated with reasoning

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too few branches | Force minimum 3 paths |
| Vague evaluation | Use numeric scores with criteria |
| Premature pruning | Keep at least 2 paths until Step 3 |
| No fallback | Always identify runner-up as backup |
| Over-branching | Limit to 3-4 paths per decision point |

---

## Template

```markdown
# ToT Analysis: [Problem Name]

## Problem Statement
[Clear description of the problem]

## Decomposition
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Evaluation Criteria
- [Criterion 1]: [Weight]
- [Criterion 2]: [Weight]
- [Criterion 3]: [Weight]

## Branch Analysis

### Path A: [Name]
- Approach: [Description]
- Pros: [List]
- Cons: [List]
- Score: [X/40]

### Path B: [Name]
- Approach: [Description]
- Pros: [List]
- Cons: [List]
- Score: [X/40]

### Path C: [Name]
- Approach: [Description]
- Pros: [List]
- Cons: [List]
- Score: [X/40]

## Pruning Decision
- Eliminated: [Path] because [reason]
- Remaining: [Paths]

## Selected Path Development
[Detailed development of chosen path]

## Solution
[Final solution]

## Fallback Plan
If primary fails: [Alternative approach]

## Confidence
Score: [1-10]
Rationale: [Why this confidence level]
```
