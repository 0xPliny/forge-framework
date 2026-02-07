# Meta-Prompting Layer

> **Meta-Prompting:** Using AI to improve AI outputs through self-critique, self-correction, and prompt optimization.

## Overview

Meta-Prompting adds a **self-improvement layer** to FORGE. Before finalizing any output, the system critiques its own work, identifies weaknesses, and refines the response. This catches errors that slip through standard frameworks.

```
┌─────────────────────────────────────────────────────────────┐
│                    Meta-Prompting Flow                       │
│                                                              │
│   [Draft Output] → [Self-Critique] → [Improve] → [Verify]   │
│                          │                           │       │
│                          ▼                           ▼       │
│                    "3 weaknesses"              "All fixed?"  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## The Meta-Prompting Protocol

### Step 1: GENERATE
Produce the initial response using the appropriate framework (R-I-S-E, C-A-R-E, etc.)

```markdown
## Draft Response
[Initial output from framework execution]
```

### Step 2: SELF-CRITIQUE
Explicitly identify weaknesses in the draft.

```markdown
## Self-Critique

Analyzing draft for weaknesses:

1. COMPLETENESS: [Is anything missing?]
   - Issue: [Specific gap identified]
   
2. ACCURACY: [Are there any errors?]
   - Issue: [Specific error identified]
   
3. CLARITY: [Is anything confusing?]
   - Issue: [Specific clarity problem]
   
4. ACTIONABILITY: [Can the user act on this?]
   - Issue: [Specific actionability gap]
   
5. EDGE CASES: [What could go wrong?]
   - Issue: [Unhandled scenario]
```

### Step 3: IMPROVE
Address each identified weakness.

```markdown
## Improvements

Addressing identified issues:

1. [Issue 1]: 
   - Fix: [How it was addressed]
   
2. [Issue 2]:
   - Fix: [How it was addressed]
   
3. [Issue 3]:
   - Fix: [How it was addressed]
```

### Step 4: VERIFY
Confirm all issues are resolved.

```markdown
## Verification

- [ ] Issue 1 resolved: [Yes/No - evidence]
- [ ] Issue 2 resolved: [Yes/No - evidence]
- [ ] Issue 3 resolved: [Yes/No - evidence]
- [ ] No new issues introduced: [Yes/No]

VERIFICATION STATUS: [PASS/FAIL]
```

### Step 5: FINALIZE
Deliver the improved response with confidence assessment.

```markdown
## Final Response

[Improved output]

---

Meta-Prompting Applied:
- Issues Found: [N]
- Issues Resolved: [N]
- Confidence Adjustment: [+X% from self-correction]
```

---

## Self-Critique Dimensions

### For Code Outputs

| Dimension | Questions to Ask |
|-----------|------------------|
| **Correctness** | Does it compile? Does it do what's intended? |
| **Edge Cases** | What happens with null, empty, max values? |
| **Error Handling** | Are errors caught and handled gracefully? |
| **Standards** | Does it follow domain coding standards? |
| **Performance** | Are there obvious inefficiencies? |
| **Security** | Are there vulnerabilities (injection, overflow)? |
| **Maintainability** | Can someone else understand and modify this? |

### For Documentation Outputs

| Dimension | Questions to Ask |
|-----------|------------------|
| **Accuracy** | Are all facts verifiable and correct? |
| **Completeness** | Are all necessary topics covered? |
| **Clarity** | Would a new reader understand this? |
| **Structure** | Is the organization logical? |
| **Examples** | Are there enough concrete examples? |
| **Currency** | Is the information up to date? |

### For Analysis Outputs

| Dimension | Questions to Ask |
|-----------|------------------|
| **Logic** | Is the reasoning sound? |
| **Evidence** | Are conclusions supported by data? |
| **Alternatives** | Were other interpretations considered? |
| **Assumptions** | Are assumptions stated and valid? |
| **Bias** | Is the analysis balanced? |
| **Actionability** | Can decisions be made from this? |

---

## Meta-Prompting Triggers

### Automatic Triggers
Apply meta-prompting automatically when:

- Output is > 500 words
- Problem was classified as COMPLEX
- Output contains code
- Output will be used in production
- High-stakes decision involved

### Manual Triggers
User can request meta-prompting:

- "Double-check this"
- "Review your answer"
- "Are you sure?"
- "What could be wrong with this?"

---

## Critique Templates

### Quick Critique (3 Questions)

```markdown
## Quick Self-Critique

1. What's the weakest part of this response?
   → [Answer]

2. What assumption am I making that might be wrong?
   → [Answer]

3. What would an expert critique about this?
   → [Answer]
```

### Deep Critique (Full Analysis)

```markdown
## Deep Self-Critique

### Strengths (What's Working)
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

### Weaknesses (What Needs Work)
1. [Weakness 1] - Severity: [High/Medium/Low]
2. [Weakness 2] - Severity: [High/Medium/Low]
3. [Weakness 3] - Severity: [High/Medium/Low]

### Missing Elements
- [What should be included but isn't]

### Potential Errors
- [What might be wrong]

### User Perspective
- Would this fully solve their problem? [Yes/No/Partially]
- What follow-up questions might they have?

### Improvement Priority
1. [Most critical fix]
2. [Second priority]
3. [Third priority]
```

---

## Prompt Optimization Protocol

When a prompt produces suboptimal results, use meta-prompting to improve it:

### Step 1: Analyze Current Prompt

```markdown
## Prompt Analysis

Current Prompt: "[The prompt that produced poor results]"

Issues Identified:
1. [Vagueness in X]
2. [Missing context about Y]
3. [Unclear output format]
```

### Step 2: Generate Variations

```markdown
## Prompt Variations

VARIATION A (More Specific):
"[Rewritten prompt with more specificity]"

VARIATION B (More Context):
"[Rewritten prompt with additional context]"

VARIATION C (Better Structure):
"[Rewritten prompt with clearer structure]"
```

### Step 3: Evaluate and Select

```markdown
## Variation Evaluation

| Variation | Clarity | Completeness | Likely Quality | Select |
|-----------|---------|--------------|----------------|--------|
| A         | 8/10    | 7/10         | 7.5/10         |        |
| B         | 7/10    | 9/10         | 8/10           | ✓      |
| C         | 9/10    | 6/10         | 7.5/10         |        |

SELECTED: Variation B
RATIONALE: [Why this variation is best]
```

### Step 4: Record Learning

```markdown
## Learning Captured

ORIGINAL_PROMPT: "[Original]"
OPTIMIZED_PROMPT: "[Improved]"
IMPROVEMENT_TYPE: [specificity/context/structure/format]
LESSON: "[What to remember for future prompts]"
```

---

## Integration with OMEGA Loop

Meta-Prompting feeds into the OMEGA Loop's learning system:

```yaml
# LEARNINGS.yaml entry from meta-prompting

- id: META_001
  timestamp: 2024-12-22T14:30:00Z
  source: meta_prompting
  category: self_correction
  
  original_issue:
    description: "Forgot to handle null case in validation function"
    severity: high
    
  correction_applied:
    description: "Added null check at function entry"
    
  pattern_identified:
    trigger: "Any validation function"
    rule: "Always check for null/undefined inputs first"
    
  future_prevention:
    checklist_item: "Null handling verified"
    auto_check: true
```

---

## Self-Correction Limits

To prevent infinite loops and over-correction:

| Limit | Value | Rationale |
|-------|-------|-----------|
| Max critique cycles | 2 | Diminishing returns after 2 |
| Max issues per cycle | 5 | Focus on critical issues |
| Time budget | 20% of total | Don't over-invest in critique |
| Confidence threshold | 7/10 | Stop when "good enough" |

---

## Example: Meta-Prompting in Action

### Original Task
"Write a function to validate email addresses"

### Draft Output
```python
def validate_email(email):
    return "@" in email and "." in email
```

### Self-Critique
```markdown
## Self-Critique

1. COMPLETENESS: Missing edge cases
   - Issue: Doesn't check for valid format, just presence of @ and .
   
2. ACCURACY: Will accept invalid emails
   - Issue: "@@.." would pass validation
   
3. EDGE CASES: Not handled
   - Issue: Empty string, None, whitespace not handled
   
4. STANDARDS: No type hints or docstring
   - Issue: Doesn't follow Python best practices
```

### Improved Output
```python
import re
from typing import Optional

def validate_email(email: Optional[str]) -> bool:
    """
    Validate an email address format.
    
    Args:
        email: The email address to validate
        
    Returns:
        True if valid email format, False otherwise
        
    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid")
        False
        >>> validate_email(None)
        False
    """
    if not email or not isinstance(email, str):
        return False
    
    # RFC 5322 simplified pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))
```

### Verification
```markdown
- [x] Edge cases handled (None, empty, whitespace)
- [x] Proper validation pattern used
- [x] Type hints added
- [x] Docstring with examples
- [x] No new issues introduced

VERIFICATION STATUS: PASS
```

---

## Template

```markdown
# Meta-Prompting Analysis

## Draft Response
[Initial output]

---

## Self-Critique

### Identified Issues
1. [Issue]: [Description] - Severity: [H/M/L]
2. [Issue]: [Description] - Severity: [H/M/L]
3. [Issue]: [Description] - Severity: [H/M/L]

---

## Improvements Applied

1. [Issue 1] → [Fix applied]
2. [Issue 2] → [Fix applied]
3. [Issue 3] → [Fix applied]

---

## Verification

- [ ] Issue 1 resolved
- [ ] Issue 2 resolved
- [ ] Issue 3 resolved
- [ ] No new issues

Status: [PASS/FAIL]

---

## Final Response

[Improved output]

---

Meta-Prompting Summary:
- Issues Found: [N]
- Issues Resolved: [N]
- Confidence: [X/10]
```
