# HARVEST Template: JavaScript/Node.js Documentation

Use this template for **documenting JavaScript/Node.js code** automatically.

---

## Metadata

```yaml
framework: HARVEST
use_case: javascript-documentation
category: UNDERSTANDING
estimated_time: 5-30 minutes
domain: "javascript" or "nodejs" or "web_development"
```

---

## INPUT

### Target

- **File(s):** JavaScript/Node.js source files (`.js`, `.mjs`, `.ts`)
- **Scope:** Function / Class / Module / System

### Context

- **Audience:** Developers / Users / Both
- **Purpose:** Reference / Tutorial / Onboarding
- **Existing docs:** None / Partial / Outdated
- **Technology Stack:** Node.js / Browser / Both

---

## HARVEST Loop

### Phase 1: HARVEST (Extract)

Automatically extract:

- [ ] Function signatures and parameters
- [ ] Class structures and methods
- [ ] Module exports and imports
- [ ] Async/await patterns
- [ ] Error handling patterns
- [ ] Configuration options
- [ ] Dependencies (package.json)

```bash
forge harvest [file] --extract --type javascript
```

### Phase 2: ANALYZE (Understand)

Determine:

- [ ] Purpose of each component
- [ ] Relationships between modules
- [ ] Data flow (async flows)
- [ ] Error handling strategy
- [ ] Configuration patterns
- [ ] Dependency relationships

### Phase 3: RESTRUCTURE (Organize)

Apply documentation layers:

- [ ] Layer 1: High-level overview
- [ ] Layer 2: Component details
- [ ] Layer 3: Usage examples
- [ ] Layer 4: API reference

### Phase 4: VERIFY (Check)

Ensure:

- [ ] All exports documented
- [ ] Examples are accurate
- [ ] No missing components
- [ ] Terminology consistent
- [ ] Async patterns explained

### Phase 5: EXTEND (Enrich)

Add:

- [ ] Usage examples (with async/await)
- [ ] Error handling examples
- [ ] Configuration examples
- [ ] Common patterns
- [ ] Gotchas/warnings
- [ ] See also references

### Phase 6: SYNTHESIZE (Combine)

Create:

- [ ] README section
- [ ] API reference
- [ ] Quick start guide
- [ ] Cross-references to related modules

### Phase 7: TRANSFORM (Format)

Output in:

- [ ] Markdown (JSDoc-style)
- [ ] JSDoc comments
- [ ] TypeScript definitions (if applicable)

---

## OUTPUT

### Generated Documentation Structure

```markdown
# [Component Name]

## Overview

[Generated overview of component purpose and functionality]

## Quick Start

[Generated quick start example]

```javascript
// Purpose: Basic usage example
const { ComponentName } = require('./component-name');

const instance = new ComponentName(options);
await instance.method();
```

## API Reference

### Class: `ComponentName`

**Purpose:** [Description]

**Constructor:**

```javascript
new ComponentName(options)
```

**Parameters:**
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `options` | `Object` | Configuration options | Yes |

**Example:**
```javascript
const component = new ComponentName({
  setting1: 'value1',
  setting2: 42
});
```

### Method: `methodName(param1, param2)`

**Purpose:** [Description]

**Parameters:**
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `param1` | `string` | Description | Yes |
| `param2` | `number` | Description | No |

**Returns:** `Promise<Result>` - Description

**Example:**
```javascript
// Purpose: Demonstrate async method usage
const result = await component.methodName('value', 42);
console.log(result);
```

**Error Handling:**
```javascript
try {
  const result = await component.methodName('value', 42);
} catch (error) {
  console.error('Error:', error.message);
}
```

## Configuration

[Configuration options documentation]

```javascript
// Purpose: Configuration example
const config = {
  option1: 'value1',
  option2: 42,
  option3: true
};
```

## Error Handling

[Error handling patterns and examples]

## Examples

### Basic Usage

```javascript
// Purpose: Complete basic usage example
const { ComponentName } = require('./component-name');

async function example() {
  const component = new ComponentName({
    setting: 'value'
  });
  
  const result = await component.method();
  console.log(result);
}

example().catch(console.error);
```

### Advanced Usage

```javascript
// Purpose: Advanced usage with error handling
const { ComponentName } = require('./component-name');

async function advancedExample() {
  try {
    const component = new ComponentName({
      setting: 'value',
      timeout: 5000
    });
    
    const result = await component.method('param1', 'param2');
    return result;
  } catch (error) {
    if (error.code === 'TIMEOUT') {
      // Handle timeout
    } else {
      // Handle other errors
      throw error;
    }
  }
}
```

## Troubleshooting

### Common Issues

**Issue:** [Common problem]

**Solution:** [Solution steps]

**Example:**
```javascript
// Purpose: Troubleshooting example
// Fix for common issue
```

## Related Documentation

### Modules
- [Related Module](../path/to/module.md) - Description

### Configuration
- [Config File](../path/to/config.md) - Description

### Workflows
- [Workflow](../path/to/workflow.md) - Description
```

---

## JavaScript-Specific Patterns

### Async/Await Documentation

**Pattern:**
```javascript
// Purpose: Demonstrate async function usage
async function example() {
  const result = await asyncFunction();
  return result;
}
```

**Error Handling:**
```javascript
// Purpose: Demonstrate error handling in async functions
try {
  const result = await asyncFunction();
} catch (error) {
  console.error('Error:', error.message);
}
```

### Promise Chains

**Pattern:**
```javascript
// Purpose: Demonstrate promise chain usage
asyncFunction()
  .then(result => processResult(result))
  .then(finalResult => console.log(finalResult))
  .catch(error => console.error('Error:', error));
```

### Module Exports

**Pattern:**
```javascript
// Purpose: Document module exports
module.exports = {
  ComponentName,
  helperFunction,
  constants
};
```

### ES6 Modules

**Pattern:**
```javascript
// Purpose: Document ES6 module exports
export class ComponentName {
  // ...
}

export function helperFunction() {
  // ...
}

export const constants = {
  // ...
};
```

### Event Emitters

**Pattern:**
```javascript
// Purpose: Document event emitter usage
const EventEmitter = require('events');

class ComponentName extends EventEmitter {
  // ...
}

const component = new ComponentName();
component.on('event', (data) => {
  console.log('Event received:', data);
});
```

---

## QUALITY CHECK

### Completeness

- [ ] All exports documented
- [ ] All public methods documented
- [ ] Examples provided
- [ ] Edge cases noted
- [ ] Error handling documented

### Accuracy

- [ ] Descriptions match behavior
- [ ] Examples work
- [ ] Types correct (if TypeScript)
- [ ] Async patterns accurate

### JavaScript-Specific Checks

- [ ] Async/await patterns documented
- [ ] Error handling patterns explained
- [ ] Promise chains documented (if used)
- [ ] Event emitters documented (if used)
- [ ] Module exports documented

### Quality Score

**Target:** 95%+
**Achieved:** ___

---

## OMEGA Learning

**Documentation patterns:**
- JavaScript async patterns
- Error handling in Node.js
- Module export patterns

**Commonly underdocumented:**
- Error handling strategies
- Async flow patterns
- Configuration options
- Event emitter usage

```bash
forge omega learn
```

---

## Related Documentation

- [HARVEST Framework](../../frameworks/universal_harvest.md) - Documentation methodology
- [Pattern Library](../../docs/PATTERN_LIBRARY.md) - Comprehensive pattern catalog
- [JavaScript Patterns](../../docs/DOCUMENTATION_PATTERNS.md) - JavaScript-specific patterns

---

**Template Version:** 1.0
**Created:** 2025-01-XX
**Framework:** FORGE Documentation Engineering Patterns

