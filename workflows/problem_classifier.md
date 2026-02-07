# Problem Classifier

**Purpose:** Automatically categorize any problem into the correct workflow with confidence scoring.

---

## The 5 Universal Problem Categories

Every problem falls into one of these categories:

| Category | Signal Words | Primary Workflow |
|----------|--------------|------------------|
| **CREATION** | create, build, implement, design, develop, new | R-I-S-E |
| **TRANSFORMATION** | convert, migrate, refactor, port, upgrade, modernize | R-I-S-E |
| **UNDERSTANDING** | explain, analyze, document, research, investigate | HARVEST |
| **REPAIR** | fix, debug, troubleshoot, resolve, patch, repair | C-A-R-E |
| **OPTIMIZATION** | optimize, improve, enhance, speed up, reduce, streamline | C-A-R-E |

---

## Classification Protocol

### Step 1: Signal Word Analysis

Scan the problem statement for signal words. Match against category table.

### Step 2: Context Analysis

If signal words are ambiguous, analyze the deeper context:

```
Is the user asking to CREATE something that doesn't exist? → CREATION
Is the user asking to CHANGE something that exists? → TRANSFORMATION
Is the user asking to UNDERSTAND something? → UNDERSTANDING
Is the user asking to FIX something broken? → REPAIR
Is the user asking to MAKE something better? → OPTIMIZATION
```

### Step 3: Complexity Assessment

| Complexity | Indicators |
|---|---|
| **Simple** | Single component, well-defined, familiar domain |
| **Medium** | Multiple components, some ambiguity, known patterns |
| **Complex** | Many components, significant ambiguity, cross-domain |
| **Expert** | Novel problem, no known patterns, high stakes |

### Step 4: Confidence Scoring

Rate classification confidence 1-10:

| Score | Meaning |
|---|---|
| 9-10 | Clear signal words, unambiguous context |
| 7-8 | Strong indicators, minor ambiguity |
| 5-6 | Mixed signals, could be multiple categories |
| 3-4 | Weak indicators, significant ambiguity |
| 1-2 | Cannot determine, need clarification |

**If confidence < 7:** Ask clarifying questions before proceeding.

---

## Classification Output

```yaml
classification:
  category: "[CREATION | TRANSFORMATION | UNDERSTANDING | REPAIR | OPTIMIZATION]"
  complexity: "[Simple | Medium | Complex | Expert]"
  workflow: "[R-I-S-E | C-A-R-E | HARVEST]"
  domain: "[domain_module or general]"
  confidence: "[1-10]"
  reasoning: "[Why this classification]"
```

---

## Edge Cases

### Multi-Category Problems

Some problems span multiple categories. Handle by:

1. Identify the **primary** category (what the user cares about most)
2. Note **secondary** categories
3. Execute primary workflow first
4. Address secondary aspects within or after

### Reclassification

If during execution the problem turns out to be misclassified:

1. Stop current workflow
2. Reclassify with new information
3. Switch to correct workflow
4. Carry forward any useful work from the previous workflow

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
