# Error Handling Protocol

**Version:** 1.0  
**Purpose:** Comprehensive error handling framework for all FORGE components

---

## Overview

This protocol defines how the FORGE handles errors, failures, and exceptional conditions across all components. It ensures graceful degradation, recovery procedures, and clear escalation paths.

---

## Error Categories

### 1. Classification Errors

**Definition:** Errors that occur during problem classification

**Sub-categories:**
- Low confidence after clarification attempts
- Ambiguous problem statements
- Multi-category problems
- Domain detection failures

### 2. Framework Execution Errors

**Definition:** Errors that occur during framework phase execution

**Sub-categories:**
- Phase failure (invalid output, exception)
- Timeout or resource exhaustion
- Invalid intermediate results
- Dependency failures

### 3. Verification Errors

**Definition:** Failures detected during verification layers

**Sub-categories:**
- Layer 1 (Formal) failures
- Layer 2 (Testing) failures
- Layer 3 (Statistical) failures
- Layer 4 (Ensemble) failures
- Layer 5 (Human) rejections

### 4. Domain Module Errors

**Definition:** Errors related to domain module loading or application

**Sub-categories:**
- Module not found
- Invalid module format
- Standard conflict resolution failures
- Quality gate configuration errors

### 5. System Errors

**Definition:** Infrastructure or framework-level errors

**Sub-categories:**
- Knowledge base access failures
- Learning persistence failures
- Resource exhaustion
- Unexpected exceptions

---

## Error Handling Principles

### 1. Fail Gracefully

- Never crash silently
- Always provide actionable error messages
- Preserve context for recovery
- Log errors for analysis

### 2. Provide Recovery Paths

- Offer alternative approaches
- Suggest next steps
- Enable manual override
- Support partial recovery

### 3. Maintain User Control

- Allow user to override decisions
- Provide escape hatches
- Support abort and restart
- Enable checkpoint/resume

### 4. Learn from Failures

- Log all errors for OMEGA Loop learning
- Identify patterns in failures
- Improve error handling over time
- Prevent repeated failures

---

## Classification Error Handling

### Scenario: Low Confidence After Clarification

**Condition:** Classification confidence remains < 0.7 after 2 clarification attempts

**Handling Protocol:**

1. **Acknowledge Uncertainty**
   ```
   "I'm uncertain about the exact classification. Based on available information,
   I'm proceeding with [CATEGORY] with low confidence (X%)."
   ```

2. **Default to Safest Option**
   - If category uncertain: Default to CREATION with R-I-S-E framework (most thorough)
   - If domain uncertain: Default to general_reasoning domain
   - Document the uncertainty clearly

3. **Enable User Override**
   - Allow user to explicitly specify category/domain/framework
   - Accept manual classification override
   - Proceed with user-specified path

4. **Record for Learning**
   - Log the ambiguous classification
   - Store user's eventual correction (if provided)
   - Use for future classification improvement

**Example:**
```yaml
classification_error:
  type: "low_confidence_after_clarification"
  confidence: 0.45
  attempts: 2
  default_action: "CREATION with R-I-S-E"
  user_override_allowed: true
  learning_recorded: true
```

### Scenario: Ambiguous Problem Statement

**Condition:** Problem statement contains conflicting signals or multiple problem types

**Handling Protocol:**

1. **Decompose Problem**
   - Identify distinct sub-problems
   - Classify each separately
   - Escalate to Layer 2 (Orchestration) if multiple frameworks needed

2. **Ask Clarifying Question**
   - Present identified sub-problems
   - Ask user to prioritize or clarify primary goal
   - Proceed with primary classification

3. **Default Strategy**
   - If decomposition reveals multiple categories: Use Layer 2 orchestration
   - If user clarifies: Use clarified classification
   - If still ambiguous: Default to R-I-S-E (most thorough)

### Scenario: Domain Detection Failure

**Condition:** No clear domain signals detected, or conflicting domain signals

**Handling Protocol:**

1. **Ask User**
   - List detected signals (if any)
   - Ask user to specify domain explicitly

2. **Default to General**
   - Use general_reasoning domain if no user input
   - Document domain uncertainty

3. **Proceed with Caution**
   - Explicitly state domain assumptions
   - Warn that domain-specific standards won't be applied
   - Suggest domain module creation if pattern emerges

---

## Framework Execution Error Handling

### General Protocol

**When any framework phase fails:**

1. **Capture Error Context**
   - Phase that failed
   - Input to the phase
   - Error message or exception
   - Attempted approach

2. **Determine Recovery Strategy**

   ```
   IF fix is obvious AND low risk:
       → Apply fix and retry phase
   ELSE IF approach is flawed:
       → Return to previous phase
       → Try alternative approach
   ELSE IF missing information:
       → Return to RESEARCH phase (R-I-S-E)
       → Or ask user for clarification
   ELSE IF fundamental problem:
       → Escalate to Layer 2 or Layer 3
       → Consider framework switch
   ```

3. **Log for Learning**
   - Record failure pattern
   - Identify root cause
   - Update OMEGA Loop learning base

### R-I-S-E Phase Failures

#### RESEARCH Phase Failure

**Scenario:** Cannot gather sufficient information

**Handling:**
- Ask user for additional context
- Identify specific information gaps
- Proceed with documented assumptions
- Flag uncertainty in confidence assessment

#### IDENTIFY Phase Failure

**Scenario:** Cannot identify patterns or requirements

**Handling:**
- Return to RESEARCH phase
- Gather more information
- Try alternative analysis approaches
- Consider switching to C-A-R-E if problem simpler than expected

#### SYNTHESIZE Phase Failure

**Scenario:** Cannot generate viable solution options

**Handling:**
- Return to IDENTIFY phase for better pattern recognition
- Consider breaking problem into smaller sub-problems
- Escalate to Layer 2 (Orchestration) for decomposition
- Consider Layer 3 (GENESIS) if truly novel problem type

#### EXECUTE Phase Failure

**Scenario:** Implementation fails or produces invalid results

**Handling:**
- Return to SYNTHESIZE for alternative approach
- Check if requirements were misunderstood
- Verify domain standards were correctly applied
- Consider breaking into smaller implementation steps

### C-A-R-E Iteration Failures

#### Exceeding Iteration Limit

**Condition:** C-A-R-E reaches 3 iterations without acceptable quality

**Handling Protocol:**

1. **Analyze Failure Pattern**
   - Is quality improving each iteration?
   - What prevents quality from reaching threshold?
   - Is the problem misclassified?

2. **Escalation Decision**

   ```
   IF quality improving but slow:
       → Allow 1-2 more iterations
       → Adjust quality threshold if reasonable
   ELSE IF quality not improving:
       → Escalate to R-I-S-E (problem may be more complex)
       → Return to RESEARCH phase
   ELSE IF problem misclassified:
       → Re-classify problem
       → Switch to appropriate framework
   ```

3. **Record Learning**
   - Log why C-A-R-E failed
   - Identify classification or complexity assessment errors
   - Update classifier for future accuracy

**Example:**
```yaml
care_iteration_failure:
  iterations: 3
  quality_scores: [0.65, 0.68, 0.67]
  threshold: 0.85
  analysis: "Quality plateaued, not improving"
  action: "Escalate to R-I-S-E"
  learning: "Problem complexity underestimated during classification"
```

### HARVEST Quality Threshold Failures

#### Quality Below Threshold After 5 Iterations

**Condition:** HARVEST quality score remains < 95% after 5 iterations

**Handling Protocol:**

1. **Assess Quality Gap**
   - What specific quality issues remain?
   - Are gaps in completeness, accuracy, or structure?
   - Is source material insufficient?

2. **Recovery Options**

   ```
   IF source material insufficient:
       → Document gaps explicitly
       → Mark sections as incomplete
       → Proceed with available information
       → Note: "Documentation incomplete due to missing sources"
   ELSE IF structural issues:
       → Try alternative template
       → Simplify structure
       → Focus on most critical sections
   ELSE IF accuracy issues:
       → Request user verification
       → Mark uncertain sections
       → Provide source references for user review
   ```

3. **Accept Partial Quality**
   - Document quality score achieved
   - Note remaining gaps
   - Allow user to proceed with review/editing
   - Schedule follow-up improvement if needed

---

## Verification Error Handling

### Layer-Specific Failures

#### Layer 1 (Formal) Failures

**Types:**
- Syntax errors
- Type errors
- Linting violations

**Handling:**
- Fix immediately (usually straightforward)
- Re-verify from Layer 1 after fix
- No escalation needed (these are structural issues)

#### Layer 2 (Testing) Failures

**Types:**
- Unit test failures
- Integration test failures
- Coverage below threshold

**Handling:**
1. Identify failing tests
2. Return to EXECUTE phase
3. Fix implementation issues
4. Re-run all verification layers from Layer 1

#### Layer 3 (Statistical) Failures

**Types:**
- Performance regression
- Memory issues
- Coverage drop

**Handling:**
1. Analyze regression cause
2. Return to SYNTHESIZE or EXECUTE phase
3. Consider alternative implementation
4. Verify fix doesn't break other metrics

#### Layer 4 (Ensemble) Failures

**Types:**
- Methods disagree
- Independent review finds issues
- Invariants violated

**Handling:**
1. Investigate disagreement source
2. Return to appropriate earlier phase
3. Consider fundamental approach change
4. May require Layer 5 (Human) judgment

#### Layer 5 (Human) Rejections

**Types:**
- Design concerns
- UX issues
- Business logic problems

**Handling:**
1. Document specific concerns
2. Return to SYNTHESIZE phase for redesign
3. Consider alternative approaches
4. May require problem re-classification

### Verification Failure Recovery Flow

```
Verification Failure Detected
    │
    ▼
Identify Failed Layer
    │
    ▼
Analyze Root Cause
    │
    ├─→ Obvious Fix? → Apply Fix → Re-verify from Layer 1
    │
    ├─→ Approach Flawed? → Return to SYNTHESIZE
    │
    ├─→ Implementation Issue? → Return to EXECUTE
    │
    └─→ Requirements Unclear? → Return to RESEARCH
```

---

## Domain Module Error Handling

### Module Not Found

**Condition:** Requested domain module doesn't exist

**Handling:**
1. Default to general_reasoning domain
2. Warn user that domain-specific standards won't be applied
3. Suggest creating domain module using template
4. Proceed with universal patterns only

### Invalid Module Format

**Condition:** Domain module YAML is malformed or invalid

**Handling:**
1. Log validation errors
2. Fall back to general_reasoning domain
3. Report specific validation errors to user
4. Suggest module format correction

### Standards Conflict

**Condition:** Multiple domains loaded with conflicting standards

**Handling:**
1. Use primary domain standards
2. Apply secondary domain standards where non-conflicting
3. Document conflicts explicitly
4. Allow user to resolve conflicts manually
5. See multi_domain_orchestration.md for detailed conflict resolution

---

## System Error Handling

### Knowledge Base Access Failure

**Condition:** Cannot read or write to knowledge base

**Handling:**
1. Proceed without learning retrieval
2. Warn user that OMEGA Loop learning is disabled
3. Attempt to log learning for later persistence
4. Continue framework execution normally

### Resource Exhaustion

**Condition:** Timeout, memory limit, or other resource constraints

**Handling:**
1. Save current state/checkpoint
2. Report resource constraint to user
3. Suggest problem decomposition
4. Recommend using Layer 2 (Orchestration) for complex problems
5. Allow user to resume from checkpoint

### Unexpected Exceptions

**Condition:** Unhandled exception or unexpected error

**Handling:**
1. Capture full error context (stack trace, state)
2. Log error for analysis
3. Present user-friendly error message
4. Suggest recovery options:
   - Retry from last successful phase
   - Restart with simpler problem decomposition
   - Report error for framework improvement
5. Preserve any work completed before error

---

## Error Reporting Format

### Standard Error Report

```yaml
error_report:
  timestamp: "2025-12-20T14:30:00Z"
  error_type: "[Classification|Framework|Verification|Domain|System]"
  error_subtype: "[Specific error category]"
  
  context:
    problem_statement: "[Original problem]"
    classification: "[If applicable]"
    framework: "[If applicable]"
    phase: "[If applicable]"
    domain: "[If applicable]"
  
  error_details:
    message: "[Human-readable error message]"
    technical_details: "[Technical error information]"
    stack_trace: "[If applicable]"
  
  recovery_attempts:
    - attempt: 1
      action: "[What was tried]"
      result: "[Success/Failure]"
  
  recommended_actions:
    - "[Action 1]"
    - "[Action 2]"
  
  user_options:
    - "[Option 1]"
    - "[Option 2]"
  
  learning_recorded: true/false
```

---

## Integration with OMEGA Loop

All errors are integrated into the OMEGA Loop learning system:

### During OMEGA.ANALYZE Phase

- Analyze error patterns
- Identify root causes
- Extract lessons learned

### During OMEGA.LEARN Phase

- Record error handling successes
- Record error handling failures
- Update error handling protocols
- Improve framework robustness

### Error Learning Record Format

```yaml
error_learning:
  error_type: "[Error category]"
  error_context: "[When/where it occurred]"
  
  what_worked:
    - recovery_action: "[Action that succeeded]"
      reuse_when: "[Similar conditions]"
  
  what_failed:
    - recovery_action: "[Action that failed]"
      lesson: "[What to do differently]"
      avoid_when: "[Conditions to avoid this action]"
  
  pattern_identified:
    - pattern: "[Common error pattern]"
      prevention: "[How to prevent]"
      detection: "[How to detect early]"
```

---

## User Communication

### Error Messages Principles

1. **Clear and Actionable**
   - Explain what went wrong
   - Explain why it happened (if known)
   - Suggest what to do next

2. **Non-Technical Language**
   - Avoid jargon when possible
   - Use technical terms only when necessary
   - Provide context for technical terms

3. **Confidence Statements**
   - Include confidence in error diagnosis
   - Acknowledge uncertainty when present
   - Provide verification recommendations

### Example Error Messages

**Good:**
```
"Classification confidence is low (45%) after 2 clarification attempts. 
I'm proceeding with CREATION category using R-I-S-E framework as the 
safest default. If this is incorrect, please specify the correct category 
and I'll adjust the approach.

Confidence: 6/10 - Based on limited problem information"
```

**Bad:**
```
"ERROR: Classification failed. Confidence < threshold."
```

---

## Quick Reference

### Error Handling Decision Tree

```
Error Detected
    │
    ├─→ Classification Error?
    │   └─→ Low confidence → Default to safest + user override
    │
    ├─→ Framework Phase Error?
    │   └─→ Return to previous phase or escalate
    │
    ├─→ Verification Error?
    │   └─→ Return to appropriate framework phase
    │
    ├─→ Domain Module Error?
    │   └─→ Fall back to general_reasoning
    │
    └─→ System Error?
        └─→ Save state, report, suggest recovery
```

### Recovery Strategy Selection

```
IF error is fixable within current phase:
    → Fix and continue
ELSE IF error requires previous phase:
    → Return to previous phase
ELSE IF error indicates wrong framework:
    → Switch framework or escalate layer
ELSE IF error is fundamental:
    → Escalate to Layer 2 or Layer 3
ELSE:
    → Save state, report error, allow user decision
```

---

## See Also

- [Problem Classifier](problem_classifier.md) - Classification error handling
- [Universal R-I-S-E](universal_rise.md) - R-I-S-E phase error handling
- [Universal C-A-R-E](universal_care.md) - C-A-R-E iteration error handling
- [Universal HARVEST](universal_harvest.md) - HARVEST quality error handling
- [Verification Framework](verification_framework.md) - Verification failure recovery
- [Multi-Domain Orchestration](../core/multi_domain_orchestration.md) - Conflict resolution
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md) - Common error scenarios

---

**Version:** 1.0  
**Last Updated:** December 2024

