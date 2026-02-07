# Universal C-A-R-E Framework

**Version:** 2.0 (Universal)
**Purpose:** Fast iteration and quality assurance for any domain

---

## Overview

C-A-R-E is an **iterative refinement loop** designed for speed when the problem is understood. Use when you need rapid execution with quality control.

```
    ┌────────────────────────────────────────┐
    │                                        │
    ▼                                        │
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ CONTEXT │ → │ ANALYZE  │ → │ RESPOND  │ → │ EVALUATE │
│ Load    │   │ Break    │   │ Generate │   │ Check    │
│ State   │   │ Down     │   │ Solution │   │ Quality  │
└─────────┘   └──────────┘   └──────────┘   └─────┬────┘
                                                  │
                                           ┌──────▼──────┐
                                           │ Quality OK? │
                                           └──────┬──────┘
                                            No    │   Yes
                                      ┌───────────┴───────────┐
                                      ▼                       ▼
                              [Iterate from              [Complete]
                               Context]
```

---

## Phase 1: CONTEXT

**Goal:** Rapidly load all relevant state

### Universal Steps

1. **Load Current State**
   - What exists now?
   - What are we working with?
   - What was done previously?

2. **Understand Goal**
   - What specific change is needed?
   - What defines success?
   - What are the boundaries?

3. **Identify Constraints**
   - Time available
   - Quality requirements
   - Domain-specific constraints

### Context Checklist

- [ ] Current state understood
- [ ] Goal is specific and clear
- [ ] Constraints identified

**Time Target:** 1-2 minutes for familiar problems

---

## Phase 2: ANALYZE

**Goal:** Decompose the problem into actionable parts

### Universal Steps

1. **Break Down Task**
   - Split into discrete sub-tasks
   - Identify dependencies
   - Estimate effort for each

2. **Identify Approach**
   - What method will work?
   - What patterns apply?
   - What pitfalls to avoid?

3. **Plan Execution Order**
   - Sequence sub-tasks correctly
   - Identify parallelizable parts
   - Note verification points

### Analyze Checklist

- [ ] Task decomposed into sub-tasks
- [ ] Approach selected
- [ ] Execution order planned

**Time Target:** 2-3 minutes

---

## Phase 3: RESPOND

**Goal:** Generate the solution

### Universal Steps

1. **Execute Sub-Tasks**
   - Follow planned order
   - Apply `[DOMAIN_STANDARDS]`
   - Check each step briefly

2. **Maintain Quality**
   - Don't skip steps for speed
   - Apply standards consistently
   - Document as you go

3. **Handle Blockers**
   - If stuck, note what's blocking
   - If approach fails, analyze why
   - Adjust or escalate as needed

### Respond Checklist

- [ ] All sub-tasks completed
- [ ] Domain standards applied
- [ ] Solution is complete

**Time Target:** Variable (depends on complexity)

---

## Phase 4: EVALUATE

**Goal:** Verify quality and determine if iteration needed

### Universal Steps

1. **Apply Quality Gates**
   - Run `[QUALITY_CHECKS]` from domain module
   - Score against threshold
   - Identify gaps

2. **Check Acceptance Criteria**
   - Does output meet goal?
   - Are all requirements satisfied?
   - Are there any obvious issues?

3. **Decide: Complete or Iterate**

   ```
   IF quality_score >= threshold AND requirements_met:
       → Mark complete
   ELSE IF minor_issues:
       → Quick fix and re-evaluate
   ELSE IF approach_flawed:
       → Return to CONTEXT with lessons learned
   ```

### Evaluate Checklist

- [ ] Quality gates applied
- [ ] Acceptance criteria checked
- [ ] Decision made: complete/iterate

---

## Iteration Strategy

### When to Iterate

| Signal | Action |
|--------|--------|
| Minor quality issues | Fix in place, re-evaluate |
| Missing requirement | Return to Context, add to scope |
| Approach not working | Return to Analyze, try alternative |
| Fundamental misunderstanding | Stop C-A-R-E, switch to R-I-S-E |

### Maximum Iterations

- **Default:** 3 iterations
- **Complex problems:** 5 iterations
- **If exceeding max:** Problem may need R-I-S-E treatment

---

## Domain Module Integration

```yaml
# Example: C-A-R-E with web_development module
domain: web_development
standards:  # Applied in RESPOND
  - Components must be properly typed
  - State management follows patterns
  - Error boundaries present
quality_gates:  # Applied in EVALUATE
  completeness: 0.95
  tests_pass: true
  no_console_errors: true
```

---

## C-A-R-E vs R-I-S-E

| Use C-A-R-E When | Use R-I-S-E When |
|------------------|------------------|
| Problem is understood | Problem needs research |
| Familiar territory | New domain |
| Iteration welcome | Need to get it right first time |
| Speed matters | Thoroughness matters |
| Improving existing | Creating from scratch |

---

## C-A-R-E Quick Reference

```
CONTEXT  → Load state, understand goal, know constraints
ANALYZE  → Decompose, plan approach, order execution
RESPOND  → Execute with standards, maintain quality
EVALUATE → Check quality, decide if done or iterate
```

**Remember:** C-A-R-E is a loop. Budget for 2-3 iterations.

---

## Error Handling and Iteration Limits

### Iteration Limit Handling

C-A-R-E has a default maximum of 3 iterations. When this limit is reached without achieving acceptable quality:

#### Exceeding Iteration Limit Protocol

**Condition:** Quality score < threshold after 3 iterations

**Analysis Steps:**

1. **Assess Quality Trend**
   ```yaml
   quality_trend_analysis:
     iteration_1: 0.65
     iteration_2: 0.68
     iteration_3: 0.67
     trend: "plateaued"  # Options: improving, plateaued, declining
     gap_to_threshold: 0.17
   ```

2. **Identify Blocking Issues**
   - What prevents quality from reaching threshold?
   - Are issues fixable within C-A-R-E?
   - Is problem more complex than initially assessed?

3. **Recovery Decision**

   ```
   IF quality improving each iteration:
       → Allow 1-2 more iterations (extend limit to 5)
       → Adjust threshold if reasonable (e.g., 0.85 → 0.80)
       
   ELSE IF quality plateaued:
       → Problem may be misclassified
       → Escalate to R-I-S-E (return to RESEARCH phase)
       → Re-assess complexity
       
   ELSE IF quality declining:
       → Approach may be flawed
       → Return to ANALYZE phase
       → Try alternative approach
       → Consider escalating to R-I-S-E
       
   ELSE IF problem simpler than expected but stuck:
       → Ask user for clarification
       → Verify requirements understanding
       → Try minimal viable fix
   ```

#### Extended Iteration Limit

**When:** Quality is improving but slowly

**Conditions for Extension:**
- Quality improved in each iteration
- Gap to threshold is closing
- No fundamental approach flaws detected

**Procedure:**
- Extend limit from 3 to 5 iterations
- Continue C-A-R-E loop
- Monitor quality trend closely
- Re-evaluate if quality stops improving

#### Escalation to R-I-S-E

**When:** Problem complexity was underestimated

**Triggers:**
- Quality plateaued after 3 iterations
- Multiple blocking issues identified
- Requirements unclear or incomplete
- Root cause analysis needed

**Procedure:**
1. Document why C-A-R-E failed
2. Escalate to R-I-S-E framework
3. Start at RESEARCH phase
4. Re-classify problem complexity
5. Use gathered C-A-R-E context as starting point

**Transition Format:**
```yaml
care_to_rise_escalation:
  reason: "Quality plateaued, multiple blocking issues"
  iterations_completed: 3
  final_quality: 0.67
  blocking_issues: ["Issue 1", "Issue 2"]
  context_preserved: true
  start_phase: "RESEARCH"
```

#### Problem Re-classification

**When:** Problem was misclassified during initial classification

**Procedure:**
1. Re-run problem classification
2. Use C-A-R-E attempts as context
3. Update category/complexity if needed
4. Switch to appropriate framework
5. Start fresh with correct classification

#### User Clarification Request

**When:** Requirements unclear or conflicting

**Procedure:**
1. Pause C-A-R-E execution
2. Present current understanding
3. Ask specific clarifying questions
4. Update requirements based on response
5. Continue C-A-R-E with clarified requirements

### Phase-Specific Error Handling

#### CONTEXT Phase Failure

**When:** Cannot load current state or state is inconsistent

**Recovery:**
- Ask user to clarify current state
- Request specific files/information
- Proceed with documented assumptions
- Flag assumptions for verification

#### ANALYZE Phase Failure

**When:** Cannot decompose problem or identify approach

**Recovery:**
- Return to CONTEXT phase
- Gather more information
- Try simpler decomposition
- Consider problem may need R-I-S-E instead

#### RESPOND Phase Failure

**When:** Solution generation fails or produces invalid output

**Recovery:**
- Return to ANALYZE phase
- Try alternative approach
- Break problem into smaller steps
- Consider escalating to R-I-S-E

#### EVALUATE Phase Failure

**When:** Cannot measure quality or quality gates fail

**Recovery:**
- Fix obvious quality issues
- Re-run quality gates
- If persistent: Return to RESPOND phase
- If quality gates misconfigured: Review domain module

### Error Learning Record

All C-A-R-E failures should be logged:

```yaml
care_failure_learning:
  iterations_completed: 3
  quality_scores: [0.65, 0.68, 0.67]
  failure_reason: "Quality plateaued"
  escalation_action: "Switched to R-I-S-E"
  lesson: "Problem complexity underestimated during classification"
  pattern: "Quality plateau → Complexity misassessment"
```

### See Also

- [Error Handling Protocol](error_handling_protocol.md) - Comprehensive error handling
- [Problem Classifier](problem_classifier.md) - Re-classification procedures
- [Meta-Framework](meta_framework.md) - Escalation paths
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md) - Common C-A-R-E issues
