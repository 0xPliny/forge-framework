# Agent Orchestration

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Coordinate multiple AI agents across phases for complex task execution.

---

## Overview

Agent Orchestration manages the execution of multiple AI agents across sequential and parallel phases. It ensures agents execute in the correct order, handle dependencies, and coordinate state updates safely.

---

## Core Concepts

### Agent Definition

Each agent has:

- **Name** - Unique identifier
- **Phase** - Which phase the agent belongs to
- **Prerequisites** - Other agents that must complete first
- **Tools** - MCP servers or external tools needed
- **Output** - Deliverables produced by the agent

### Phase Organization

Phases are executed sequentially, agents within phases can run in parallel:

```yaml
phases:
  - name: research
    parallel: true
    agents: [research-web, research-code]
    
  - name: identify
    parallel: false
    agents: [identify-patterns]
    
  - name: synthesize
    parallel: false
    agents: [synthesize-solution]
    
  - name: execute
    parallel: true
    agents: [execute-code, execute-tests]
```

---

## Orchestration Flow

### 1. Dependency Resolution

Build a dependency graph to determine execution order:

```javascript
function buildDependencyGraph(agents) {
  const graph = new Map();
  
  for (const agent of agents) {
    graph.set(agent.name, {
      agent,
      dependencies: agent.prerequisites || [],
      dependents: []
    });
  }
  
  // Build reverse dependencies
  for (const [name, node] of graph) {
    for (const dep of node.dependencies) {
      if (graph.has(dep)) {
        graph.get(dep).dependents.push(name);
      }
    }
  }
  
  return graph;
}
```

### 2. Phase Execution

Execute phases sequentially, agents within phases in parallel:

```javascript
async function executePhases(phases, context) {
  for (const phase of phases) {
    console.log(`Executing phase: ${phase.name}`);
    
    if (phase.parallel) {
      // Execute all agents concurrently
      const results = await Promise.all(
        phase.agents.map(agent => executeAgent(agent, context))
      );
      context.deliverables = mergeResults(results);
    } else {
      // Execute agents sequentially
      for (const agent of phase.agents) {
        const result = await executeAgent(agent, context);
        context.deliverables = { ...context.deliverables, ...result };
      }
    }
    
    // Checkpoint after phase
    await checkpointManager.createCheckpoint(
      context.sourceDir,
      `${phase.name}-complete`
    );
  }
}
```

### 3. State Coordination

Use mutexes to prevent race conditions:

```javascript
import { SessionMutex } from '../execution/utils/concurrency.js';

const sessionMutex = new SessionMutex();

async function markAgentCompleted(sessionId, agentName) {
  const unlock = await sessionMutex.lock(sessionId);
  
  try {
    await sessionManager.checkpoint(sessionId, agentName);
  } finally {
    unlock();
  }
}
```

---

## Integration with FORGEs

### R-I-S-E Orchestration

```javascript
const phases = [
  {
    name: 'research',
    parallel: true,
    agents: ['research-web', 'research-code', 'research-docs']
  },
  {
    name: 'identify',
    parallel: true,
    agents: ['identify-patterns', 'identify-anti-patterns']
  },
  {
    name: 'synthesize',
    parallel: false,  // Needs all research and identification
    agents: ['synthesize-solution']
  },
  {
    name: 'execute',
    parallel: true,
    agents: ['execute-code', 'execute-tests', 'execute-docs']
  }
];
```

### C-A-R-E Orchestration

```javascript
const phases = [
  {
    name: 'context',
    parallel: true,
    agents: ['context-logs', 'context-metrics', 'context-code']
  },
  {
    name: 'analyze',
    parallel: true,
    agents: ['analyze-performance', 'analyze-security']
  },
  {
    name: 'respond',
    parallel: false,  // Needs all analysis
    agents: ['respond-fix']
  },
  {
    name: 'evaluate',
    parallel: true,
    agents: ['evaluate-tests', 'evaluate-metrics']
  }
];
```

---

## Related Documentation

- [Parallel Agents](../execution/parallel_agents.md) - Multi-agent orchestration patterns
- [Session Manager](../execution/session_manager.md) - Persistent state management
- [Checkpoint Manager](../execution/checkpoint_manager.md) - Git-based checkpointing
- [R-I-S-E Framework](../frameworks/universal_rise.md) - Research → Identify → Synthesize → Execute
- [C-A-R-E Framework](../frameworks/universal_care.md) - Context → Analyze → Respond → Evaluate

