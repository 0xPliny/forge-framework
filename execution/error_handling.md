# Error Handling

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Provide robust error handling with categorized errors and retry logic.

---

## Overview

The Error Handling system provides structured error categorization, automatic retry logic for transient failures, and graceful degradation when errors cannot be recovered. All errors are logged to the audit system for forensic analysis.

---

## Error Categories

| Category | Retry | Examples | Typical Causes |
|----------|-------|----------|----------------|
| **ConfigError** | No | Invalid config, missing required fields | User input error, configuration file issues |
| **NetworkError** | Yes | Timeout, connection refused, DNS failure | Network issues, service unavailable |
| **ToolError** | Yes | External tool failure, command execution error | Tool not installed, tool crashed |
| **ValidationError** | No | Output doesn't meet requirements, invalid format | Logic error, unexpected output |
| **AIError** | Yes | LLM rate limit, context overflow, API error | API issues, quota exceeded |
| **SystemError** | No | Disk full, permission denied, out of memory | System resource issues |

---

## Retry Strategy

### Retry Configuration

```javascript
const RETRY_CONFIG = {
  NetworkError: {
    maxRetries: 3,
    backoff: 'exponential',
    initialDelay: 1000  // 1 second
  },
  ToolError: {
    maxRetries: 2,
    backoff: 'linear',
    initialDelay: 2000  // 2 seconds
  },
  AIError: {
    maxRetries: 5,
    backoff: 'exponential',
    initialDelay: 5000  // 5 seconds
  }
};

/**
 * Execute function with retry logic
 * @param {Function} fn - Function to execute
 * @param {string} errorCategory - Error category
 * @returns {Promise<any>} Function result
 */
async function withRetry(fn, errorCategory) {
  const config = RETRY_CONFIG[errorCategory];
  if (!config) {
    // No retry config - execute once
    return await fn();
  }
  
  let lastError;
  
  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // Check if error matches category
      if (!isErrorCategory(error, errorCategory)) {
        throw error; // Wrong category - don't retry
      }
      
      if (attempt < config.maxRetries) {
        const delay = calculateDelay(config, attempt);
        console.log(`⚠️ Retry attempt ${attempt + 1}/${config.maxRetries} after ${delay}ms...`);
        await sleep(delay);
      }
    }
  }
  
  throw lastError;
}

/**
 * Calculate delay based on backoff strategy
 * @param {Object} config - Retry configuration
 * @param {number} attempt - Current attempt number (0-indexed)
 * @returns {number} Delay in milliseconds
 */
function calculateDelay(config, attempt) {
  if (config.backoff === 'exponential') {
    return config.initialDelay * Math.pow(2, attempt);
  } else if (config.backoff === 'linear') {
    return config.initialDelay * (attempt + 1);
  } else {
    return config.initialDelay;
  }
}

/**
 * Sleep for specified milliseconds
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

---

## Custom Error Classes

### Base Error Class

```javascript
class ForgeError extends Error {
  constructor(message, type, retryable = false, context = {}) {
    super(message);
    this.name = 'ForgeError';
    this.type = type; // 'config', 'network', 'tool', 'validation', 'ai', 'system'
    this.retryable = retryable;
    this.context = context;
    this.timestamp = new Date().toISOString();
  }
}

// Specific error classes
class ConfigError extends ForgeError {
  constructor(message, context = {}) {
    super(message, 'config', false, context);
    this.name = 'ConfigError';
  }
}

class NetworkError extends ForgeError {
  constructor(message, context = {}) {
    super(message, 'network', true, context);
    this.name = 'NetworkError';
  }
}

class ToolError extends ForgeError {
  constructor(message, context = {}) {
    super(message, 'tool', true, context);
    this.name = 'ToolError';
  }
}

class ValidationError extends ForgeError {
  constructor(message, context = {}) {
    super(message, 'validation', false, context);
    this.name = 'ValidationError';
  }
}

class AIError extends ForgeError {
  constructor(message, context = {}) {
    super(message, 'ai', true, context);
    this.name = 'AIError';
  }
}

class SystemError extends ForgeError {
  constructor(message, context = {}) {
    super(message, 'system', false, context);
    this.name = 'SystemError';
  }
}
```

---

## Error Detection

### Categorizing Errors

```javascript
/**
 * Determine error category from error object
 * @param {Error} error - Error object
 * @returns {string} Error category
 */
function categorizeError(error) {
  const message = error.message.toLowerCase();
  
  // Network errors
  if (message.includes('network') ||
      message.includes('connection') ||
      message.includes('timeout') ||
      message.includes('econnreset') ||
      message.includes('enotfound') ||
      message.includes('econnrefused')) {
    return 'network';
  }
  
  // AI/LLM errors
  if (message.includes('rate limit') ||
      message.includes('429') ||
      message.includes('context overflow') ||
      message.includes('api error')) {
    return 'ai';
  }
  
  // Tool errors
  if (message.includes('command failed') ||
      message.includes('tool not found') ||
      message.includes('execution error')) {
    return 'tool';
  }
  
  // Validation errors
  if (message.includes('invalid') ||
      message.includes('validation failed') ||
      message.includes('does not meet requirements')) {
    return 'validation';
  }
  
  // System errors
  if (message.includes('permission denied') ||
      message.includes('disk full') ||
      message.includes('out of memory')) {
    return 'system';
  }
  
  // Default to unknown
  return 'unknown';
}

/**
 * Check if error matches category
 * @param {Error} error - Error object
 * @param {string} category - Error category
 * @returns {boolean} True if error matches category
 */
function isErrorCategory(error, category) {
  if (error.type) {
    return error.type === category;
  }
  
  return categorizeError(error) === category;
}
```

---

## Error Logging

All errors are logged to the audit system:

```javascript
import { AuditLogger } from './audit_system.js';

/**
 * Log error to audit system
 * @param {Error} error - Error object
 * @param {string} contextMsg - Context message
 * @param {string} sessionId - Session ID
 * @param {string} agentName - Agent name (if applicable)
 * @returns {Promise<void>}
 */
async function logError(error, contextMsg, sessionId, agentName = null) {
  const auditLogger = new AuditLogger(sessionId);
  await auditLogger.initialize();
  
  const errorData = {
    name: error.name || error.constructor.name,
    message: error.message,
    type: error.type || categorizeError(error),
    retryable: error.retryable || false,
    stack: error.stack,
    context: error.context || {},
    agentName,
    contextMsg
  };
  
  await auditLogger.logEvent('error', errorData);
  
  // Also log to console with appropriate color
  const prefix = error.retryable ? '⚠️' : '❌';
  const color = error.retryable ? chalk.yellow : chalk.red;
  console.log(color(`${prefix} ${contextMsg}: ${error.message}`));
  
  if (error.context && Object.keys(error.context).length > 0) {
    console.log(chalk.gray(`   Context: ${JSON.stringify(error.context)}`));
  }
}
```

---

## Graceful Degradation

When errors cannot be recovered:

```javascript
/**
 * Handle unrecoverable error
 * @param {Error} error - Error object
 * @param {string} sessionId - Session ID
 * @param {string} agentName - Agent name
 * @returns {Promise<void>}
 */
async function handleUnrecoverableError(error, sessionId, agentName) {
  // 1. Log the failure
  await logError(error, `Agent ${agentName} failed`, sessionId, agentName);
  
  // 2. Create checkpoint (if possible)
  try {
    const checkpointResult = await checkpointManager.createCheckpoint(
      sourceDir,
      `error-checkpoint-${agentName}`,
      1
    );
    
    if (checkpointResult.success) {
      console.log(chalk.blue(`✅ Checkpoint created before failure`));
    }
  } catch (checkpointError) {
    console.log(chalk.yellow(`⚠️ Could not create checkpoint: ${checkpointError.message}`));
  }
  
  // 3. Notify user with actionable guidance
  console.log(chalk.red(`\n❌ Agent '${agentName}' failed and cannot be recovered.`));
  console.log(chalk.yellow(`\nPossible actions:`));
  console.log(chalk.yellow(`  1. Check error logs: audit-logs/${sessionId}/events/`));
  console.log(chalk.yellow(`  2. Review agent output for clues`));
  console.log(chalk.yellow(`  3. Fix underlying issue and retry with --rerun ${agentName}`));
  console.log(chalk.yellow(`  4. Rollback to previous checkpoint: forge rollback <checkpoint>`));
  
  // 4. Mark agent as failed in session
  await sessionManager.markFailed(sessionId, agentName);
  
  // 5. Offer rollback options
  const checkpoints = await checkpointManager.listCheckpoints(sourceDir, sessionId);
  if (checkpoints.length > 0) {
    console.log(chalk.cyan(`\nAvailable checkpoints for rollback:`));
    checkpoints.forEach((cp, index) => {
      console.log(chalk.cyan(`  ${index + 1}. ${cp.tag} (${cp.date})`));
    });
  }
}
```

---

## Related Documentation

- [Session Manager](./session_manager.md) - Persistent state management
- [Checkpoint Manager](./checkpoint_manager.md) - Git-based checkpointing
- [Audit System](./audit_system.md) - Crash-safe logging
- [Parallel Agents](./parallel_agents.md) - Multi-agent orchestration

