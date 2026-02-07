# C-A-R-E Template: Code Review

Use this template when **reviewing code** for quality and correctness.

---

## Metadata

```yaml
framework: C-A-R-E
use_case: code-review
category: UNDERSTANDING
estimated_time: 15-45 minutes
domain: "[DOMAIN]"
```

---

## CONTEXT

### PR/Change Information

- **Title:**
- **Author:**
- **Files changed:**
- **Lines added/removed:** +___/ -___

### Purpose of Change
>
> [What is this change trying to accomplish?]

### Load Domain Standards

```bash
forge module load [domain]
```

---

## ANALYZE

### Correctness

- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] No obvious bugs

### Standards Compliance

```bash
forge check [files] --domain [domain]
```

- [ ] Required standards followed
- [ ] No forbidden patterns
- [ ] Recommended practices applied

### Design

- [ ] Approach is reasonable
- [ ] No over-engineering
- [ ] No under-engineering
- [ ] Consistent with codebase

### Testing

- [ ] Tests added/updated
- [ ] Tests cover key paths
- [ ] Tests are meaningful (not just coverage)

### Performance

- [ ] No obvious performance issues
- [ ] No memory leaks
- [ ] Appropriate complexity

### Security

- [ ] No security vulnerabilities
- [ ] Input validation present
- [ ] Secrets handled properly

---

## RESPOND

### Summary

**Overall:** ✅ Approve / 🔄 Request Changes / ❌ Reject

### Comments by Priority

#### Must Fix (Blocking)

1.

#### Should Fix (Non-blocking)

1.

#### Consider (Optional)

1.

#### Praise (What's Good)

1.

### Example Fixes (if applicable)

```
[Suggested code improvements]
```

---

## EVALUATE

### Review Quality Check

- [ ] All files reviewed
- [ ] Feedback is constructive
- [ ] Suggestions are actionable
- [ ] Praised good work

### Discussion Points

- [ ] Discussed with author if needed
- [ ] Questions answered

---

## OMEGA Learning

**Patterns seen (good or bad):**
-

**Common issues to watch for:**
-

```bash
forge omega learn
```
