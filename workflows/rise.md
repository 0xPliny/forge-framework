# Universal R-I-S-E Framework

**Version:** 2.0 (Universal)
**Purpose:** Domain-agnostic systematic problem-solving methodology

---

## Overview

R-I-S-E is a 4-phase approach that works for **any problem domain**. The phases are universal; domain-specific standards are injected via modules.

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   RESEARCH   │ → │   IDENTIFY   │ → │  SYNTHESIZE  │ → │   EXECUTE    │
│   Gather     │    │   Pattern    │    │   Design     │    │  Implement   │
│   Context    │    │   Match      │    │   Solution   │    │  + Verify    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
      ↑                                                            │
      └────────────────── Iterate if needed ──────────────────────┘
```

---

## Phase 1: RESEARCH

**Goal:** Build complete understanding of the problem space

### Universal Steps

1. **Gather Available Information**
   - Read all provided context (documents, code, data)
   - Identify information sources
   - Note what is explicitly stated vs implied

2. **Identify Missing Information**
   - What facts are needed but not provided?
   - What assumptions are being made?
   - What clarifications would help?

3. **Understand Constraints**
   - Time constraints
   - Resource constraints
   - Technical constraints
   - Quality requirements

4. **Create Context Document**
   - Summarize the problem
   - List all known facts
   - Flag uncertainties

### Research Checklist

- [ ] I understand what success looks like
- [ ] I know all explicit requirements
- [ ] I've identified implicit requirements
- [ ] I understand the constraints
- [ ] I've flagged areas of uncertainty

---

## Phase 2: IDENTIFY

**Goal:** Find patterns, requirements, and potential approaches

### Universal Steps

1. **Extract Key Requirements**
   - Functional: What must it do?
   - Non-functional: How well must it do it?
   - Constraints: What can't it do?

2. **Recognize Patterns**
   - Does this match a known problem type?
   - What similar problems have I solved?
   - What approaches work for this category?

3. **Identify Risks**
   - What could go wrong?
   - What edge cases exist?
   - What dependencies are fragile?

4. **Map the Solution Space**
   - What are the possible approaches?
   - What are the trade-offs?
   - Which approach fits the constraints?

### Identify Checklist

- [ ] All requirements extracted and prioritized
- [ ] Problem type classified
- [ ] Similar problems identified
- [ ] Risks catalogued
- [ ] At least 2 potential approaches identified

---

## Phase 3: SYNTHESIZE

**Goal:** Design the solution

### Universal Steps

1. **Generate Solution Options**
   - Create at least 2-3 approaches
   - Don't dismiss ideas prematurely
   - Include conventional and creative options

2. **Evaluate Options**

   ```
   For each option:
   ├── Does it meet all requirements?
   ├── Does it respect all constraints?
   ├── What are the trade-offs?
   ├── What is the implementation complexity?
   └── What is the verification difficulty?
   ```

3. **Select Optimal Approach**
   - Choose approach with best fit
   - Document rationale for selection
   - Document why alternatives were rejected

4. **Create Implementation Plan**
   - Break into discrete steps
   - Identify dependencies between steps
   - Define success criteria for each step

### Synthesize Checklist

- [ ] Multiple options generated
- [ ] Options evaluated against requirements
- [ ] Optimal approach selected with rationale
- [ ] Implementation plan created
- [ ] Success criteria defined

---

## Phase 4: EXECUTE

**Goal:** Implement and verify the solution

### Universal Steps

1. **Implement Solution**
   - Follow implementation plan
   - Apply `[DOMAIN_STANDARDS]` (from domain module)
   - Document decisions and trade-offs

2. **Verify Incrementally**
   - Check each step against success criteria
   - Apply `[QUALITY_GATES]` (from domain module)
   - Don't proceed if verification fails

3. **Handle Failures**
   - If step fails, analyze why
   - Determine if approach is still viable
   - If not, return to SYNTHESIZE with new information

4. **Complete and Document**
   - Verify final output meets all requirements
   - Document what was done and why
   - Capture lessons learned

### Execute Checklist

- [ ] Solution implemented per plan
- [ ] Domain standards applied
- [ ] Each step verified before proceeding
- [ ] Final output meets requirements
- [ ] Solution documented

---

## Domain Module Integration

The `[PLACEHOLDERS]` in Execute phase are filled by domain modules:

```yaml
# Example: How domain module integrates
domain: web_development
standards:
  - Use TypeScript for type safety
  - Follow React hooks patterns
  - Apply proper error handling
quality_gates:
  - All components render without errors
  - No TypeScript compilation errors
  - Accessibility checks pass
```

**To apply a domain module:**

1. Load module: `forge module load [domain_name]`
2. Standards automatically inject into Execute phase
3. Quality gates apply during verification

---

## When to Use R-I-S-E

| Situation | Use R-I-S-E? | Why |
|-----------|--------------|-----|
| New complex problem | ✅ Yes | Need thorough research first |
| Unfamiliar domain | ✅ Yes | Pattern matching helps |
| High-stakes decision | ✅ Yes | Multiple options important |
| Quick familiar fix | ❌ No | Use C-A-R-E instead |
| Iterating on existing | ❌ No | Use C-A-R-E instead |

---

## R-I-S-E Quick Reference

```
RESEARCH → What do I know? What don't I know?
IDENTIFY → What patterns apply? What could go wrong?
SYNTHESIZE → What are my options? Which is best?
EXECUTE → Implement, verify, document
```

**Remember:** If execution reveals missing information, return to Research.

---

## Error Handling and Recovery

### Phase Failure Recovery

Each phase has specific error handling procedures when execution fails or produces invalid results.

#### RESEARCH Phase Failure

**When:** Cannot gather sufficient information or context is too ambiguous

**Recovery:**
1. Ask user for specific missing information
2. Identify explicit information gaps
3. Proceed with documented assumptions if user unavailable
4. Flag all assumptions and uncertainties in confidence assessment
5. Continue to IDENTIFY phase with reduced confidence

**Example:**
```yaml
research_failure:
  issue: "Missing API documentation for endpoint X"
  action: "Documented assumption: API follows RESTful conventions"
  confidence_impact: -0.1
  flag_for_verification: true
```

#### IDENTIFY Phase Failure

**When:** Cannot identify patterns, requirements unclear, or no similar problems found

**Recovery:**
1. Return to RESEARCH phase to gather more information
2. Try alternative analysis approaches:
   - Break problem into smaller sub-problems
   - Analyze by functional area rather than holistically
   - Look for partial pattern matches
3. If still failing: Consider problem may be simpler than expected
   - Switch to C-A-R-E framework if problem appears straightforward
   - Or escalate to Layer 2 (Orchestration) for decomposition

**Decision Tree:**
```
IDENTIFY Phase Fails
    │
    ├─→ Missing Information?
    │   └─→ Return to RESEARCH
    │
    ├─→ Problem Too Complex?
    │   └─→ Escalate to Layer 2 (decompose)
    │
    ├─→ Problem Simpler Than Expected?
    │   └─→ Switch to C-A-R-E
    │
    └─→ Novel Problem Type?
        └─→ Escalate to Layer 3 (GENESIS)
```

#### SYNTHESIZE Phase Failure

**When:** Cannot generate viable solution options or all options fail evaluation

**Recovery:**
1. Return to IDENTIFY phase for better pattern recognition
2. Re-analyze requirements and constraints
3. Consider breaking problem into smaller sub-problems
4. Escalate to Layer 2 (Orchestration) for multi-framework approach
5. If truly novel: Consider Layer 3 (GENESIS) for new framework creation

**Alternative Approaches:**
- Simplify requirements if possible
- Relax constraints if acceptable
- Look for partial solutions that can be combined
- Consider incremental approach rather than complete solution

#### EXECUTE Phase Failure

**When:** Implementation fails, produces invalid results, or violates constraints

**Recovery:**
1. **Immediate Issues (syntax, types, obvious errors):**
   - Fix immediately
   - Re-verify from Layer 1 (Formal verification)

2. **Logic or Design Issues:**
   - Return to SYNTHESIZE phase
   - Re-evaluate solution approach
   - Try alternative implementation strategy

3. **Requirements Misunderstood:**
   - Return to IDENTIFY phase
   - Re-analyze requirements
   - Verify understanding with user

4. **Domain Standards Violations:**
   - Review domain module standards
   - Fix violations
   - Verify compliance

**Recovery Flow:**
```
EXECUTE Phase Fails
    │
    ├─→ Syntax/Type Error?
    │   └─→ Fix → Re-verify Layer 1
    │
    ├─→ Logic Error?
    │   └─→ Return to SYNTHESIZE
    │
    ├─→ Requirements Misunderstood?
    │   └─→ Return to IDENTIFY
    │
    └─→ Domain Standards Violation?
        └─→ Fix → Re-verify
```

### Iteration and Escalation

**When to Iterate Within R-I-S-E:**
- Quality below threshold after EXECUTE
- Requirements refined during execution
- Better approach discovered

**When to Escalate:**
- R-I-S-E stuck after multiple iterations
- Problem requires multiple frameworks (→ Layer 2)
- No framework fits (→ Layer 3)

**Maximum Iterations:**
- No hard limit, but track iterations
- After 3+ iterations without progress: Escalate or switch approach
- After 5+ iterations: Strongly consider escalation

### Error Logging

All phase failures should be logged for OMEGA Loop learning:

```yaml
rise_failure_learning:
  phase: "SYNTHESIZE"
  failure_type: "no_viable_solutions"
  problem_signature: "[keywords, domain, complexity]"
  recovery_action: "Returned to IDENTIFY"
  outcome: "Success/Failure"
  lesson: "What to do differently next time"
```

### See Also

- [Error Handling Protocol](error_handling_protocol.md) - Comprehensive error handling framework
- [Meta-Framework](meta_framework.md) - Escalation to Layer 2 or Layer 3
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md) - Common R-I-S-E issues
