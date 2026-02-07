# C-A-R-E Template: Bug Fix

Use this template for **fixing bugs** with fast iteration.

---

## Metadata

```yaml
framework: C-A-R-E
use_case: bug-fix
category: REPAIR
estimated_time: 15-60 minutes
domain: "[DOMAIN]"
iteration: 1
```

---

## CONTEXT

### Bug Report

- **Symptom:** [What's happening that shouldn't?]
- **Expected:** [What should happen instead?]
- **Reported by:**
- **Severity:** Critical / High / Medium / Low
- **Reproducible:** Always / Sometimes / Rarely

### Environment

- File(s):
- Version/Branch:
- Steps to reproduce:
  1.
  2.
  3.

### Known Working State

- Last worked: [When/version]
- Recent changes: [What changed?]

### Load Domain Standards

```bash
forge module load [domain]
```

---

## ANALYZE

### Root Cause Hypothesis
>
> [What do you think is causing this?]

### Investigation Steps

- [ ] Reproduce the bug
- [ ] Check logs/errors:
- [ ] Trace the code path:
- [ ] Identify the specific line/function:

### Root Cause Found
>
> **The bug is caused by:** [Explain]
> **Location:** [File:line]

### Fix Approach

- [ ] Simple fix (change few lines)
- [ ] Moderate fix (refactor needed)
- [ ] Complex fix (design change needed) → Consider R-I-S-E

---

## RESPOND

### The Fix

```
[Show the code change]
```

**File:**
**Lines changed:**

### Standards Applied

- [ ] [Standard 1]
- [ ] [Standard 2]

### Regression Prevention

- [ ] Added test for this case
- [ ] Checked similar code paths
- [ ] Documented the fix

---

## EVALUATE

### Does It Work?

- [ ] Bug no longer reproduces
- [ ] Expected behavior confirmed
- [ ] No new errors introduced

### Verification

```bash
forge verify [file] --domain [domain]
```

- [ ] Layer 1 (Formal): Pass
- [ ] Layer 2 (Tests): Pass

### Quality Check

- [ ] Fix is minimal (no unnecessary changes)
- [ ] Code is clean
- [ ] Standards followed

---

## Iteration Check

**Quality Score:** ___ / 10

If < 8: Return to ANALYZE with new information:

- What was missed:
- New hypothesis:

If ≥ 8: COMPLETE ✓

---

## OMEGA Learning

**Pattern/Anti-pattern identified:**
-

**Prevent similar bugs by:**
-

```bash
forge omega learn
```
