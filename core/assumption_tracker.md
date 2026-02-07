# Assumption Tracker

> **Purpose:** Make all assumptions explicit, assess their risk, and plan for when they're wrong.

## Overview

Every AI response that makes assumptions must explicitly document them. This prevents silent failures and enables faster debugging when solutions don't work as expected.

---

## The Assumption Protocol

### Required Format

Every response that relies on assumptions must include:

```markdown
## Assumptions Made

1. [Assumption] - Risk: [High/Medium/Low] - Validate by: [How]
2. [Assumption] - Risk: [High/Medium/Low] - Validate by: [How]
3. [Assumption] - Risk: [High/Medium/Low] - Validate by: [How]

## If Assumptions Are Wrong

- [Assumption 1 wrong] → [Impact and alternative approach]
- [Assumption 2 wrong] → [Impact and alternative approach]
- [Assumption 3 wrong] → [Impact and alternative approach]
```

---

## Risk Classification

| Risk Level | Definition | Requires |
|------------|------------|----------|
| **High** | If wrong, solution completely fails | Explicit validation before proceeding |
| **Medium** | If wrong, solution needs modification | Fallback approach identified |
| **Low** | If wrong, minor adjustments needed | Note for awareness only |

---

## Validation Methods

| Validation Type | Use When | Example |
|-----------------|----------|---------|
| **Ask User** | Assumption can only be verified by user | "Do you want strict TypeScript?" |
| **Check Code** | Can be verified by reading source | "Verify in config.yaml" |
| **Test Run** | Can be verified by execution | "Run unit tests to confirm" |
| **Documentation** | Can be verified in docs | "See Section 4.2 of API docs" |
| **Infer from Context** | Reasonable inference from given info | "Based on file structure..." |

---

## Common Assumption Categories

### Technical Assumptions

- Programming language/version
- Framework/library versions
- Operating system
- Database type
- API availability

### Environment Assumptions

- Development vs production
- Local vs remote execution
- Permissions/access levels
- Network connectivity

### Requirements Assumptions

- Scope boundaries
- Performance requirements
- Security requirements
- Backwards compatibility

### Domain Assumptions

- Business rules
- Data formats
- Naming conventions
- Workflow sequences

---

## Example: Code Fix With Assumptions

```markdown
## Solution

Here's the fix for the timeout issue:

```python
import asyncio

async def fetch_data(url: str, timeout: int = 30) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=timeout) as response:
            return await response.json()
```

---

## Assumptions Made

1. **Python 3.7+ is being used** - Risk: High - Validate by: Check `python --version`
2. **aiohttp is installed** - Risk: Medium - Validate by: Run `pip show aiohttp`
3. **Response is valid JSON** - Risk: Medium - Validate by: Test with actual endpoint
4. **30-second default timeout is acceptable** - Risk: Low - Validate by: Ask user

## If Assumptions Are Wrong

- **Python < 3.7** → Use `asyncio.ensure_future()` instead of `async/await` syntax, or upgrade Python
- **aiohttp not installed** → Install with `pip install aiohttp` or use `requests` library instead
- **Response not JSON** → Add content-type check and handle accordingly
- **Different timeout needed** → Adjust the `timeout` parameter default

```

---

## Integration with Other Protocols

### With Confidence Protocol
```markdown
CONFIDENCE: 7/10
REASONING: Solution works for standard cases
CAVEATS: Assumes Python 3.7+

## Assumptions Made
1. Python 3.7+ - Risk: High - Validate by: Version check
```

### With Meta-Prompting

During self-critique, explicitly check:

- "Are all assumptions documented?"
- "Are high-risk assumptions validated?"
- "Are fallbacks identified for medium+ risk?"

### With ReAct

```markdown
THOUGHT: I'm assuming the API returns JSON, but I should verify.
ACTION: READ[api/docs/endpoints.md]
OBSERVATION: Confirmed - all endpoints return application/json
```

---

## When to Skip

Assumptions don't need explicit tracking when:

- Information was directly provided by user
- Fact is universally true (e.g., "1 + 1 = 2")
- Verification would take longer than fixing if wrong

---

## Template

```markdown
## Assumptions Made

1. [What you're assuming] - Risk: [H/M/L] - Validate by: [Method]
2. [What you're assuming] - Risk: [H/M/L] - Validate by: [Method]
3. [What you're assuming] - Risk: [H/M/L] - Validate by: [Method]

## If Assumptions Are Wrong

- [Assumption 1 wrong] → [Impact]: [Alternative approach]
- [Assumption 2 wrong] → [Impact]: [Alternative approach]
- [Assumption 3 wrong] → [Impact]: [Alternative approach]
```

---

## Quick Reference

| Risk | Action Required |
|------|-----------------|
| High | Validate before proceeding or ask user |
| Medium | Document fallback approach |
| Low | Note for awareness |

**Remember:** An explicit wrong assumption is fixable. An implicit wrong assumption wastes hours.
