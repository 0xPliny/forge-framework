# Session Manager

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Manage persistent state across task execution, enabling pause/resume and crash recovery.

---

## Overview

The Session Manager provides persistent state management for FORGE execution, enabling tasks to be paused, resumed, and recovered after crashes. It maintains session state across multiple phases and agents, tracking progress, checkpoints, and metrics.

---

## Core Concepts

### Session State

A session represents a single execution instance of a FORGE task. Each session contains:

- **Session ID** - Unique identifier (UUID) for the session
- **Start Time** - Timestamp when session was created
- **Current Phase** - The phase currently being executed (e.g., "research", "identify", "synthesize", "execute")
- **Completed Agents/Steps** - List of agents or steps that have successfully completed
- **Failed Agents/Steps** - List of agents or steps that have failed
- **Checkpoint References** - Map of agent names to git commit hashes for rollback
- **Metrics** - Timing, costs, and attempt counts
- **Status** - Current status: `in-progress`, `completed`, `failed`

### State Persistence

Session state is persisted to disk using atomic writes:

- **Storage Location:** `.forge-session.json` (or `.forge-store.json` for multiple sessions)
- **Atomic Writes:** Write to temporary file, then rename to prevent corruption
- **Immediate Flush:** State is saved immediately after each change
- **Format:** JSON with human-readable formatting (2-space indent)

### Session Lifecycle

1. **Initialize** - Create new session or resume existing session
2. **Execute** - Run phases/agents, updating state as progress is made
3. **Checkpoint** - Save state at key points (after each phase/agent)
4. **Complete** - Mark session as finished when all work is done
5. **Cleanup** - Archive or delete session data (optional)

---

## Implementation Pattern

### Basic Session Manager Class

```javascript
class SessionManager {
  constructor(sessionDir) {
    this.sessionDir = sessionDir;
    this.storeFile = path.join(sessionDir, '.forge-store.json');
    this.state = null;
  }
  
  /**
   * Initialize session - create new or resume existing
   * @param {Object} config - Session configuration
   * @param {string} config.taskName - Name of the task
   * @param {string} [config.sessionId] - Existing session ID to resume
   * @returns {Promise<Object>} Session object
   */
  async initialize(config) {
    // Check for existing session
    if (config.sessionId) {
      const existing = await this.getSession(config.sessionId);
      if (existing && existing.status !== 'completed') {
        console.log(`📝 Resuming existing session: ${existing.id.substring(0, 8)}...`);
        this.state = existing;
        return existing;
      }
    }
    
    // Create new session
    const sessionId = crypto.randomUUID();
    const session = {
      id: sessionId,
      taskName: config.taskName,
      status: 'in-progress',
      completedAgents: [],
      failedAgents: [],
      checkpoints: {},
      createdAt: new Date().toISOString(),
      lastActivity: new Date().toISOString()
    };
    
    await this.saveSession(session);
    this.state = session;
    return session;
  }
  
  /**
   * Get session by ID
   * @param {string} sessionId - Session ID
   * @returns {Promise<Object|null>} Session object or null
   */
  async getSession(sessionId) {
    const store = await this.loadStore();
    return store.sessions[sessionId] || null;
  }
  
  /**
   * Update session state
   * @param {string} sessionId - Session ID
   * @param {Object} updates - Fields to update
   * @returns {Promise<Object>} Updated session
   */
  async updateSession(sessionId, updates) {
    const store = await this.loadStore();
    
    if (!store.sessions[sessionId]) {
      throw new Error(`Session ${sessionId} not found`);
    }
    
    store.sessions[sessionId] = {
      ...store.sessions[sessionId],
      ...updates,
      lastActivity: new Date().toISOString()
    };
    
    await this.saveStore(store);
    return store.sessions[sessionId];
  }
  
  /**
   * Create checkpoint after agent/phase completion
   * @param {string} sessionId - Session ID
   * @param {string} agentName - Agent or phase name
   * @param {string} checkpointCommit - Git commit hash (if using git checkpointing)
   * @returns {Promise<Object>} Updated session
   */
  async checkpoint(sessionId, agentName, checkpointCommit = null) {
    const session = await this.getSession(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found`);
    }
    
    const updates = {
      completedAgents: [...new Set([...session.completedAgents, agentName])],
      checkpoints: {
        ...session.checkpoints,
        [agentName]: checkpointCommit
      }
    };
    
    // Check if all agents are completed
    const totalAgents = this.getTotalAgents();
    if (updates.completedAgents.length === totalAgents) {
      updates.status = 'completed';
    }
    
    return await this.updateSession(sessionId, updates);
  }
  
  /**
   * Rollback session to specific agent checkpoint
   * @param {string} sessionId - Session ID
   * @param {string} targetAgent - Agent to rollback to
   * @returns {Promise<Object>} Updated session
   */
  async rollbackTo(sessionId, targetAgent) {
    const session = await this.getSession(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found`);
    }
    
    if (!session.checkpoints[targetAgent]) {
      throw new Error(`No checkpoint found for agent '${targetAgent}'`);
    }
    
    // Find agents that need to be removed (those after target)
    const targetOrder = this.getAgentOrder(targetAgent);
    const agentsToRemove = this.getAgentsAfter(targetOrder);
    
    const updates = {
      completedAgents: session.completedAgents.filter(
        agent => !agentsToRemove.includes(agent)
      ),
      failedAgents: session.failedAgents.filter(
        agent => !agentsToRemove.includes(agent)
      ),
      checkpoints: Object.fromEntries(
        Object.entries(session.checkpoints).filter(
          ([agent]) => !agentsToRemove.includes(agent)
        )
      )
    };
    
    return await this.updateSession(sessionId, updates);
  }
  
  /**
   * Load store from disk
   * @private
   * @returns {Promise<Object>} Store object
   */
  async loadStore() {
    try {
      if (!await fs.pathExists(this.storeFile)) {
        return { sessions: {} };
      }
      
      const content = await fs.readFile(this.storeFile, 'utf8');
      const store = JSON.parse(content);
      
      // Validate store structure
      if (!store || typeof store !== 'object' || !store.sessions) {
        console.log('⚠️ Invalid session store format, creating new store');
        return { sessions: {} };
      }
      
      return store;
    } catch (error) {
      console.log(`⚠️ Failed to load session store: ${error.message}, creating new store`);
      return { sessions: {} };
    }
  }
  
  /**
   * Save store to disk atomically
   * @private
   * @param {Object} store - Store object
   * @returns {Promise<void>}
   */
  async saveStore(store) {
    const tempFile = `${this.storeFile}.tmp`;
    await fs.writeJSON(tempFile, store, { spaces: 2 });
    await fs.move(tempFile, this.storeFile, { overwrite: true });
  }
}
```

---

## Integration with FORGEs

### R-I-S-E Execution

Use session management in R-I-S-E to checkpoint after each phase:

```javascript
// Research phase
await sessionManager.checkpoint(sessionId, 'research', researchCommit);

// Identify phase
await sessionManager.checkpoint(sessionId, 'identify', identifyCommit);

// Synthesize phase
await sessionManager.checkpoint(sessionId, 'synthesize', synthesizeCommit);

// Execute phase
await sessionManager.checkpoint(sessionId, 'execute', executeCommit);
```

### C-A-R-E Execution

Use session management in C-A-R-E to checkpoint after each step:

```javascript
// Context step
await sessionManager.checkpoint(sessionId, 'context', contextCommit);

// Analyze step
await sessionManager.checkpoint(sessionId, 'analyze', analyzeCommit);

// Respond step
await sessionManager.checkpoint(sessionId, 'respond', respondCommit);

// Evaluate step
await sessionManager.checkpoint(sessionId, 'evaluate', evaluateCommit);
```

### OMEGA Loop

Persist learnings across sessions:

```javascript
// Save learnings to session
await sessionManager.updateSession(sessionId, {
  learnings: {
    patterns: [...],
    antiPatterns: [...],
    optimizations: [...]
  }
});

// Load learnings in next session
const previousSession = await sessionManager.getSession(previousSessionId);
const learnings = previousSession.learnings || {};
```

---

## Session Recovery

### Detecting Incomplete Sessions

On startup, check for incomplete sessions:

```javascript
async function detectIncompleteSessions() {
  const store = await sessionManager.loadStore();
  const incomplete = Object.values(store.sessions).filter(
    session => session.status === 'in-progress'
  );
  
  return incomplete;
}
```

### Resuming Sessions

Resume an incomplete session:

```javascript
const incompleteSessions = await detectIncompleteSessions();
if (incompleteSessions.length > 0) {
  console.log(`Found ${incompleteSessions.length} incomplete session(s)`);
  
  // Let user select session to resume
  const sessionToResume = await selectSession(incompleteSessions);
  
  // Resume from last checkpoint
  const lastCompletedAgent = sessionToResume.completedAgents[
    sessionToResume.completedAgents.length - 1
  ];
  console.log(`Resuming from: ${lastCompletedAgent}`);
}
```

---

## Concurrency Safety

When using parallel agents, use mutexes to prevent race conditions:

```javascript
import { SessionMutex } from './utils/concurrency.js';

const sessionMutex = new SessionMutex();

async function markAgentCompleted(sessionId, agentName, checkpointCommit) {
  const unlock = await sessionMutex.lock(sessionId);
  
  try {
    // Get fresh session data under lock
    const session = await sessionManager.getSession(sessionId);
    
    // Update session state
    await sessionManager.checkpoint(sessionId, agentName, checkpointCommit);
  } finally {
    unlock();
  }
}
```

---

## Related Documentation

- [Checkpoint Manager](./checkpoint_manager.md) - Git-based checkpointing
- [Audit System](./audit_system.md) - Crash-safe logging
- [Parallel Agents](./parallel_agents.md) - Multi-agent orchestration
- [Error Handling](./error_handling.md) - Retry logic and error categories
- [R-I-S-E Framework](../frameworks/universal_rise.md) - Research → Identify → Synthesize → Execute
- [C-A-R-E Framework](../frameworks/universal_care.md) - Context → Analyze → Respond → Evaluate
- [OMEGA Loop](../frameworks/omega_loop.md) - Self-improvement system

