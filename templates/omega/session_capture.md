# OMEGA Template: Session Learning Capture

Use this template to **capture learnings at the end of a session**.

---

## Metadata

```yaml
framework: OMEGA
use_case: session-capture
timestamp: "[YYYY-MM-DD HH:MM]"
session_duration: "[X minutes]"
```

---

## SESSION SUMMARY

### Problems Solved

| Problem | Category | Framework | Quality |
|---------|----------|-----------|---------|
| | | | |

### Total

- Problems:
- Iterations:
- Time:

---

## LEARNING EXTRACTION

### Patterns That Worked

#### Pattern 1: [Name]

- **Problem type:**
- **Solution approach:**
- **Why it worked:**
- **Reuse when:**

```yaml
# Add to knowledge base
pattern:
  name: "[Name]"
  category: "[structure|behavior|integration]"
  applies_to: "[problem types]"
  implementation: |
    [Steps]
```

#### Pattern 2: [Name]

- **Problem type:**
- **Solution approach:**
- **Why it worked:**
- **Reuse when:**

---

### What Didn't Work

#### Failed Attempt 1

- **What I tried:**
- **Why it failed:**
- **Root cause:**
- **Lesson:**
- **Avoid when:**

```yaml
# Add to knowledge base
anti_pattern:
  name: "[Name]"
  failure_mode: "[How it fails]"
  avoid_when: "[Conditions]"
  alternative: "[What to do instead]"
```

#### Failed Attempt 2

- **What I tried:**
- **Why it failed:**
- **Lesson:**

---

### New Discoveries

#### Discovery 1

- **What I learned:**
- **Implications:**
- **Future use:**

#### Discovery 2

- **What I learned:**
- **Implications:**

---

## METRICS

### Quality Scores

| Metric | Target | Achieved |
|--------|--------|----------|
| Completeness | 95% | |
| Accuracy | 98% | |
| Consistency | 90% | |
| **Overall** | 95% | |

### Efficiency

- Time to first solution:
- Total time:
- Iterations average:
- Rework:

### Error Analysis

- Errors caught by Layer 1:
- Errors caught by Layer 2:
- Errors caught by Layer 3+:
- Errors that escaped:

---

## KNOWLEDGE BASE UPDATE

### Add to Patterns Library

```bash
forge learn add pattern "[pattern yaml]"
```

### Add to Anti-Patterns Library

```bash
forge learn add anti-pattern "[anti-pattern yaml]"
```

### Export Session Learnings

```bash
forge omega export --session "[session-id]"
```

---

## NEXT SESSION PREPARATION

### Incomplete Tasks

1.
2.

### Follow-Up Questions

1.
2.

### Learnings to Apply

- From this session:
- From past sessions: `forge learn show --recent`

---

## OMEGA Loop Completion

```bash
# Mark session complete and save learnings
forge omega end

# Verify learnings saved
forge learn stats
```

**Session Error Rate:** ___
**Compared to Domain Average:** Better / Same / Worse
**Learning Rate λ:**___ (estimated from improvement over session)
