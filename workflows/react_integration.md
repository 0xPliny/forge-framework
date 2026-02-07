# ReAct Integration — Reasoning + Acting

**Purpose:** When you need information you don't have, use iterative reasoning and action loops to gather it.

---

## Overview

ReAct (Reasoning + Acting) is an enhancement layer that can be applied within any FORGE workflow phase. It provides a structured loop for gathering missing information through action and observation.

```
THOUGHT → ACTION → OBSERVATION → (repeat) → ANSWER
```

---

## The ReAct Loop

### Step 1: THOUGHT

Articulate what you need to know and why:

```
THOUGHT: I need to understand the authentication flow because the user
mentioned JWT tokens but I don't know the token lifecycle.
```

### Step 2: ACTION

Choose an action to gather information:

| Action | Use When |
|--------|----------|
| **SEARCH** | Need to find sources on a topic |
| **EXECUTE** | Need to run code or commands |
| **VERIFY** | Need to confirm a claim |
| **READ** | Need to extract information from a source |
| **QUERY** | Need to ask a clarifying question |
| **TEST** | Need to validate behavior |

```
ACTION: SEARCH — "JWT token refresh flow best practices"
```

### Step 3: OBSERVATION

Record what you found:

```
OBSERVATION: JWT refresh tokens should be stored securely, rotated on use,
and have a longer expiry than access tokens. Access tokens: 15 min.
Refresh tokens: 7 days.
```

### Step 4: Assess

Decide if you have enough information or need another cycle:

```
ASSESSMENT: I now understand the token lifecycle. Confidence: 8/10.
Proceeding with implementation.
```

---

## Integration with FORGE Workflows

### In R-I-S-E

- **Research phase:** Use ReAct to fill knowledge gaps
- **Implement phase:** Use ReAct to resolve technical unknowns
- **Synthesize phase:** Use ReAct to verify integration assumptions

### In C-A-R-E

- **Collect phase:** Use ReAct to gather context
- **Analyze phase:** Use ReAct to investigate root causes

### In HARVEST

- **Extract phase:** Use ReAct to find missing source artifacts
- **Verify phase:** Use ReAct to cross-check facts

---

## Limits

- **Maximum cycles:** 5 for deep research, 3 for quick tasks
- **If stuck after max cycles:** Document what's still unknown and proceed with assumptions
- **Always track:** What was searched, what was found, what's still missing

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
