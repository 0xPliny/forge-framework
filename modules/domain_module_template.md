# Domain Module Template

**Version:** 1.0
**Purpose:** Standard structure for creating pluggable domain modules

---

## Overview

Domain modules inject domain-specific standards, quality gates, and personas into universal frameworks. This template defines the required structure.

---

## Module Structure

```yaml
# File: modules/[domain_name].yaml

# ============================================
# METADATA
# ============================================
metadata:
  name: "[domain_name]"
  version: "1.0"
  description: "[What this domain covers]"
  author: "[Who created it]"
  last_updated: "[Date]"

# When to auto-select this module
applicable_to:
  file_extensions:
    - "[.ext1]"
    - "[.ext2]"
  keywords:
    - "[keyword1]"
    - "[keyword2]"
  context_signals:
    - "[paths, tools, or other signals]"

# ============================================
# STANDARDS
# ============================================
standards:
  # Things that MUST be done
  required:
    - id: "REQ-001"
      name: "[Standard Name]"
      description: "[What must be done]"
      example: "[Show correct usage]"
      
    - id: "REQ-002"
      name: "[Standard Name]"
      description: "[What must be done]"
      example: "[Show correct usage]"

  # Things that MUST NOT be done
  forbidden:
    - id: "FORBID-001"
      pattern: "[What to avoid]"
      reason: "[Why it's forbidden]"
      alternative: "[What to do instead]"
      
    - id: "FORBID-002"
      pattern: "[What to avoid]"
      reason: "[Why it's forbidden]"
      alternative: "[What to do instead]"

  # Best practices (recommended but not required)
  recommended:
    - id: "REC-001"
      name: "[Practice Name]"
      description: "[Why it's recommended]"
      example: "[Show usage]"

# ============================================
# QUALITY GATES
# ============================================
quality_gates:
  completeness:
    threshold: 0.95  # 0.0 to 1.0
    measures:
      - "[How to measure completeness in this domain]"
      - "[Specific checks for completeness]"
    
  accuracy:
    threshold: 0.98
    measures:
      - "[How to verify accuracy]"
      - "[Domain-specific accuracy checks]"
    
  consistency:
    threshold: 0.90
    measures:
      - "[What consistency means here]"
      - "[How to check for consistency]"
  
  # Add domain-specific gates as needed
  custom_gates:
    - name: "[Gate Name]"
      threshold: "[value]"
      measures:
        - "[How to check]"

# ============================================
# PERSONAS
# ============================================
personas:
  - name: "[Persona Name]"
    role: "[What this persona does]"
    expertise: 
      - "[Skill 1]"
      - "[Skill 2]"
    style: "[How this persona communicates/works]"
    when_to_use: "[Conditions for activating]"
    
    # Full persona prompt (optional - can link to file)
    prompt: |
      You are [persona description].
      
      Your expertise includes:
      - [expertise areas]
      
      You follow these principles:
      - [principles]

# ============================================
# PATTERNS
# ============================================
common_patterns:
  - name: "[Pattern Name]"
    category: "[Category: structure, behavior, integration]"
    problem: "[What problem does it solve]"
    solution: |
      [How to apply this pattern]
    example: |
      [Code or process example]

# ============================================
# ANTI-PATTERNS
# ============================================
anti_patterns:
  - name: "[Anti-pattern Name]"
    description: "[What it is]"
    why_bad: "[Why to avoid]"
    alternative: "[What to do instead]"
    detection: "[How to spot it]"

# ============================================
# TOOLS & COMMANDS
# ============================================
tools:
  standards_check:
    command: "[Command to run standards check]"
    expected_output: "[What success looks like]"
    
  quality_score:
    command: "[Command to get quality score]"
    expected_output: "[Score format]"

# ============================================
# EXAMPLES
# ============================================
examples:
  # Example of a well-done solution in this domain
  good_example:
    description: "[What this demonstrates]"
    code: |
      [Example code or content]
    why_good:
      - "[Reason 1]"
      - "[Reason 2]"
  
  # Example of what to avoid
  bad_example:
    description: "[What this shows]"
    code: |
      [Example of problematic code]
    why_bad:
      - "[Problem 1]"
      - "[Problem 2]"
    fixed: |
      [Corrected version]
```

---

## Creating a New Module

### Step 1: Identify Domain

- What file types does it cover?
- What keywords signal this domain?
- What context identifies it?

### Step 2: Define Standards

- What MUST be done? (required)
- What MUST NOT be done? (forbidden)
- What SHOULD be done? (recommended)

### Step 3: Set Quality Gates

- How do you measure completeness?
- How do you verify accuracy?
- What does consistency mean?
- Are there domain-specific checks?

### Step 4: Create Personas

- Who is the expert in this domain?
- What is their expertise?
- How do they work/communicate?

### Step 5: Document Patterns

- What patterns solve common problems?
- What anti-patterns cause issues?
- What examples illustrate correct usage?

### Step 6: Test the Module

- Apply to sample problems
- Verify standards catch violations
- Check quality gates trigger appropriately
- Confirm persona guidance is useful

---

## Module Validation Checklist

Before publishing a module:

- [ ] Metadata complete and accurate
- [ ] At least 3 required standards defined
- [ ] At least 2 forbidden patterns defined
- [ ] Quality gates have reasonable thresholds
- [ ] At least 1 persona defined with prompt
- [ ] At least 2 common patterns documented
- [ ] At least 1 anti-pattern documented
- [ ] Good and bad examples provided
- [ ] Tested on 3+ representative problems
- [ ] Documentation is clear and complete

---

## Module Loading

```bash
# Load a module
forge module load [domain_name]

# View loaded module
forge module show

# List available modules
forge module list

# Validate a module
forge module validate [path/to/module.yaml]
```

---

## Integration with Frameworks

When a module is loaded, its contents inject into frameworks:

### In R-I-S-E (Execute phase)

```
Execute with [DOMAIN_STANDARDS] ← From module.standards
Apply [QUALITY_GATES] ← From module.quality_gates
Use [PERSONA] as guide ← From module.personas
```

### In C-A-R-E (Respond + Evaluate phases)

```
Respond: Apply [DOMAIN_STANDARDS] ← From module.standards
Evaluate: Check [QUALITY_GATES] ← From module.quality_gates
```

### In Problem Classifier

```
Match [applicable_to] to detect domain ← From module.applicable_to
```
