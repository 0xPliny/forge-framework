# Audit System

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Provide forensic logging with crash safety and self-healing.

---

## Overview

The Audit System provides crash-safe, append-only logging for all execution activities. It ensures that even if a process crashes, all events are preserved and can be used to reconstruct the execution state. The system is self-healing, meaning it can reconcile state discrepancies on startup.

---

## Core Principles

### Append-Only Logging

- **Never Modify Existing Logs** - Once written, log entries are immutable
- **Immediate Flush** - Each write is immediately flushed to disk
- **Survives Process Termination** - Logs persist even if the process crashes
- **Atomic Writes** - Use temporary files and rename to prevent corruption

### Self-Healing

- **Reconcile State on Startup** - Compare audit logs with session state
- **Audit Logs are Source of Truth** - Session state follows audit logs
- **Detect Discrepancies** - Find agents marked complete in audit but not in session (or vice versa)
- **Automatic Correction** - Update session state to match audit logs

### Forensic Completeness

- **Log All Attempts** - Success and failure are both logged
- **Capture Timing** - Record start time, end time, and duration for each operation
- **Capture Costs** - Track API costs, tool costs, and resource usage
- **Preserve Rolled-Back Entries** - Even rolled-back operations are logged (marked as rolled-back)

---

## Directory Structure

```
audit-logs/
└── {session-id}/
    ├── session.json           # Comprehensive metrics and session state
    ├── prompts/               # Prompt snapshots (one per agent)
    │   ├── research.txt
    │   ├── identify.txt
    │   └── ...
    ├── events/                # Event-by-event logs (one file per agent attempt)
    │   ├── 001-research-attempt-1.jsonl
    │   ├── 002-identify-attempt-1.jsonl
    │   ├── 003-research-attempt-2.jsonl  # Retry attempt
    │   └── ...
    └── deliverables/          # Output artifacts
        ├── research-report.md
        ├── identify-patterns.json
        └── ...
```

---

## Event Types

| Event Type | Description | When Logged |
|------------|-------------|-------------|
| `session_start` | New session initialized | When session is created |
| `phase_begin` | Phase execution started | Start of R-I-S-E or C-A-R-E phase |
| `phase_end` | Phase execution completed | End of phase |
| `agent_start` | Agent execution started | Start of agent/step |
| `agent_end` | Agent execution completed | End of agent/step (success or failure) |
| `step_begin` | Step within phase started | Start of sub-step |
| `step_end` | Step completed | End of sub-step |
| `tool_start` | External tool execution started | Before running tool |
| `tool_end` | External tool execution completed | After tool completes |
| `llm_request` | LLM API request made | Before sending request |
| `llm_response` | LLM API response received | After receiving response |
| `error` | Error occurred | When error is caught |
| `checkpoint` | Checkpoint created | After checkpoint is created |
| `rollback` | Rollback performed | When rollback occurs |

---

## Implementation Pattern

### Basic Audit Logger Class

```javascript
import fs from 'fs';
import { path } from 'zx';

class AuditLogger {
  constructor(sessionId) {
    this.sessionId = sessionId;
    this.logDir = `audit-logs/${sessionId}`;
    this.eventCounter = 0;
    this.stream = null;
    this.isOpen = false;
  }
  
  /**
   * Initialize audit logger (create directories, open log file)
   * @returns {Promise<void>}
   */
  async initialize() {
    // Create directory structure
    await fs.promises.mkdir(`${this.logDir}/events`, { recursive: true });
    await fs.promises.mkdir(`${this.logDir}/prompts`, { recursive: true });
    await fs.promises.mkdir(`${this.logDir}/deliverables`, { recursive: true });
    
    // Create session.json if it doesn't exist
    const sessionJsonPath = `${this.logDir}/session.json`;
    if (!await fs.promises.pathExists(sessionJsonPath)) {
      await fs.promises.writeJSON(sessionJsonPath, {
        sessionId: this.sessionId,
        status: 'in-progress',
        startTime: new Date().toISOString(),
        metrics: {
          totalDuration: 0,
          totalCost: 0,
          agents: {}
        }
      }, { spaces: 2 });
    }
    
    this.isOpen = true;
  }
  
  /**
   * Log an event (atomic write with immediate flush)
   * @param {string} type - Event type
   * @param {Object} data - Event data
   * @returns {Promise<void>}
   */
  async logEvent(type, data) {
    const event = {
      id: ++this.eventCounter,
      timestamp: new Date().toISOString(),
      type,
      data
    };
    
    // Atomic write: write to temp file, then rename
    const tempPath = `${this.logDir}/events/.tmp-${event.id}`;
    const finalPath = `${this.logDir}/events/${String(event.id).padStart(6, '0')}-${type}.json`;
    
    await fs.promises.writeFile(tempPath, JSON.stringify(event, null, 2));
    await fs.promises.rename(tempPath, finalPath);
  }
  
  /**
   * Log event to JSONL file (for streaming logs)
   * @param {string} agentName - Agent name
   * @param {number} attemptNumber - Attempt number
   * @param {string} type - Event type
   * @param {Object} data - Event data
   * @returns {Promise<void>}
   */
  async logEventToStream(agentName, attemptNumber, type, data) {
    const logPath = `${this.logDir}/events/${agentName}-attempt-${attemptNumber}.jsonl`;
    
    const event = {
      timestamp: new Date().toISOString(),
      type,
      data
    };
    
    // Append to JSONL file with immediate flush
    const stream = fs.createWriteStream(logPath, { flags: 'a' });
    stream.write(JSON.stringify(event) + '\n');
    stream.end();
    
    // Wait for stream to finish
    await new Promise((resolve) => {
      stream.on('finish', resolve);
    });
  }
  
  /**
   * Save prompt snapshot
   * @param {string} agentName - Agent name
   * @param {string} promptContent - Full prompt content
   * @returns {Promise<void>}
   */
  async savePrompt(agentName, promptContent) {
    const promptPath = `${this.logDir}/prompts/${agentName}.txt`;
    await fs.promises.writeFile(promptPath, promptContent, 'utf8');
  }
  
  /**
   * Update session metrics
   * @param {string} agentName - Agent name
   * @param {Object} metrics - Metrics to update
   * @param {number} metrics.duration_ms - Duration in milliseconds
   * @param {number} metrics.cost_usd - Cost in USD
   * @param {boolean} metrics.success - Whether succeeded
   * @returns {Promise<void>}
   */
  async updateMetrics(agentName, metrics) {
    const sessionJsonPath = `${this.logDir}/session.json`;
    
    // Read current session data
    const sessionData = await fs.promises.readJSON(sessionJsonPath);
    
    // Update metrics
    sessionData.metrics.agents[agentName] = {
      ...sessionData.metrics.agents[agentName],
      ...metrics,
      lastUpdated: new Date().toISOString()
    };
    
    sessionData.metrics.totalDuration += metrics.duration_ms || 0;
    sessionData.metrics.totalCost += metrics.cost_usd || 0;
    
    // Atomic write
    const tempPath = `${sessionJsonPath}.tmp`;
    await fs.promises.writeJSON(tempPath, sessionData, { spaces: 2 });
    await fs.promises.rename(tempPath, sessionJsonPath);
  }
}
```

---

## Self-Healing Reconciliation

The audit system can reconcile discrepancies between audit logs and session state:

```javascript
/**
 * Reconcile session state with audit logs
 * @param {string} sessionId - Session ID
 * @returns {Promise<Object>} Reconciliation report
 */
async function reconcileSession(sessionId) {
  const auditLogger = new AuditLogger(sessionId);
  await auditLogger.initialize();
  
  // Load session state
  const session = await sessionManager.getSession(sessionId);
  
  // Load audit metrics
  const sessionJsonPath = `audit-logs/${sessionId}/session.json`;
  const auditData = await fs.promises.readJSON(sessionJsonPath);
  
  const report = {
    promotions: [],  // Agents completed in audit but not in session
    demotions: [],   // Agents rolled-back in audit but still in session
    failures: []     // Agents failed in audit but not marked failed
  };
  
  // PART 1: PROMOTIONS
  // Find agents completed in audit but not in session
  const auditCompleted = Object.entries(auditData.metrics.agents)
    .filter(([_, agentData]) => agentData.status === 'success')
    .map(([agentName]) => agentName);
  
  const missing = auditCompleted.filter(
    agent => !session.completedAgents.includes(agent)
  );
  
  for (const agentName of missing) {
    await sessionManager.checkpoint(sessionId, agentName, null);
    report.promotions.push(agentName);
  }
  
  // PART 2: DEMOTIONS
  // Find agents rolled-back in audit but still in session
  const auditRolledBack = Object.entries(auditData.metrics.agents)
    .filter(([_, agentData]) => agentData.status === 'rolled-back')
    .map(([agentName]) => agentName);
  
  const toRemove = session.completedAgents.filter(
    agent => auditRolledBack.includes(agent)
  );
  
  if (toRemove.length > 0) {
    await sessionManager.rollbackTo(sessionId, toRemove[0]);
    report.demotions.push(...toRemove);
  }
  
  // PART 3: FAILURES
  // Find agents failed in audit but not marked failed
  const auditFailed = Object.entries(auditData.metrics.agents)
    .filter(([_, agentData]) => agentData.status === 'failed')
    .map(([agentName]) => agentName);
  
  const failedToAdd = auditFailed.filter(
    agent => !session.failedAgents.includes(agent)
  );
  
  for (const agentName of failedToAdd) {
    await sessionManager.markFailed(sessionId, agentName);
    report.failures.push(agentName);
  }
  
  return report;
}
```

---

## Concurrency Safety

Use mutexes to prevent race conditions when updating session.json:

```javascript
import { SessionMutex } from './utils/concurrency.js';

const sessionMutex = new SessionMutex();

async function updateMetricsWithLock(sessionId, agentName, metrics) {
  const unlock = await sessionMutex.lock(sessionId);
  
  try {
    // Reload metrics (in case of parallel updates)
    const auditLogger = new AuditLogger(sessionId);
    await auditLogger.initialize();
    
    // Update metrics
    await auditLogger.updateMetrics(agentName, metrics);
  } finally {
    unlock();
  }
}
```

---

## Related Documentation

- [Session Manager](./session_manager.md) - Persistent state management
- [Checkpoint Manager](./checkpoint_manager.md) - Git-based checkpointing
- [Parallel Agents](./parallel_agents.md) - Multi-agent orchestration
- [Error Handling](./error_handling.md) - Retry logic and error categories

