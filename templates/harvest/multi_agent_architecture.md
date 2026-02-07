# HARVEST Template: Multi-Agent Architecture Documentation

Use this template for **documenting multi-agent systems** automatically.

---

## Metadata

```yaml
framework: HARVEST
use_case: multi-agent-architecture
category: UNDERSTANDING
estimated_time: 10-60 minutes
domain: "ai" or "multi-agent" or "distributed"
```

---

## INPUT

### Target

- **File(s):** Agent definitions, orchestration code, communication protocols
- **Scope:** Agent / Agent System / Architecture

### Context

- **Audience:** Developers / Architects / Both
- **Purpose:** Reference / Architecture Guide / Onboarding
- **Existing docs:** None / Partial / Outdated
- **Agent Types:** AI Agents / Service Agents / Process Agents

---

## HARVEST Loop

### Phase 1: HARVEST (Extract)

Automatically extract:

- [ ] Agent definitions and roles
- [ ] Agent communication patterns
- [ ] Orchestration logic
- [ ] Message formats
- [ ] Agent dependencies
- [ ] Phase/workflow definitions
- [ ] Agent capabilities

```bash
forge harvest [file] --extract --type multi-agent
```

### Phase 2: ANALYZE (Understand)

Determine:

- [ ] Agent roles and responsibilities
- [ ] Communication patterns
- [ ] Orchestration flow
- [ ] Message passing mechanisms
- [ ] Agent dependencies
- [ ] Phase/workflow structure
- [ ] Error handling across agents

### Phase 3: RESTRUCTURE (Organize)

Apply documentation layers:

- [ ] Layer 1: Architecture overview
- [ ] Layer 2: Agent details
- [ ] Layer 3: Communication patterns
- [ ] Layer 4: Orchestration flow

### Phase 4: VERIFY (Check)

Ensure:

- [ ] All agents documented
- [ ] Communication patterns accurate
- [ ] Orchestration flow correct
- [ ] No missing agents
- [ ] Terminology consistent

### Phase 5: EXTEND (Enrich)

Add:

- [ ] Agent interaction examples
- [ ] Communication examples
- [ ] Orchestration examples
- [ ] Error handling examples
- [ ] Common patterns
- [ ] Gotchas/warnings

### Phase 6: SYNTHESIZE (Combine)

Create:

- [ ] Architecture overview
- [ ] Agent catalog
- [ ] Communication diagram
- [ ] Orchestration flow diagram
- [ ] Cross-references between agents

### Phase 7: TRANSFORM (Format)

Output in:

- [ ] Markdown
- [ ] Architecture diagrams (Mermaid)
- [ ] Agent relationship diagrams

---

## OUTPUT

### Generated Documentation Structure

```markdown
# Multi-Agent Architecture

## Overview

[Generated overview of multi-agent system]

## Architecture Overview

[High-level architecture description]

```
┌─────────────────────────────────────────────────────────┐
│                  Orchestration Layer                     │
│              (Main Orchestrator/Coordinator)            │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│   Agent 1    │ │   Agent 2    │ │   Agent 3    │
│  (Role/Type) │ │  (Role/Type) │ │  (Role/Type) │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Agent Catalog

### Agent: [Agent Name]

**Role:** [Agent role and responsibility]

**Type:** [AI Agent / Service Agent / Process Agent]

**Capabilities:**
- Capability 1
- Capability 2
- Capability 3

**Inputs:**
- Input 1: Description
- Input 2: Description

**Outputs:**
- Output 1: Description
- Output 2: Description

**Communication:**
- Receives from: [Agent Names]
- Sends to: [Agent Names]
- Message format: [Format description]

**Example:**
```javascript
// Purpose: Demonstrate agent usage
const agent = new AgentName(config);
const result = await agent.execute(input);
```

## Communication Patterns

### Pattern: [Pattern Name]

**Description:** [How agents communicate]

**Flow:**
```
Agent A → Message → Agent B → Response → Agent A
```

**Example:**
```javascript
// Purpose: Demonstrate communication pattern
const message = {
  type: 'request',
  payload: data
};

const response = await agentB.handleMessage(message);
```

## Orchestration Flow

### Phase: [Phase Name]

**Description:** [Phase purpose]

**Agents Involved:**
- Agent 1: Role
- Agent 2: Role
- Agent 3: Role

**Flow:**
```
1. Orchestrator → Agent 1: Start phase
2. Agent 1 → Agent 2: Request data
3. Agent 2 → Agent 1: Provide data
4. Agent 1 → Orchestrator: Phase complete
```

**Example:**
```javascript
// Purpose: Demonstrate orchestration flow
async function executePhase() {
  await orchestrator.startPhase('phase-name');
  const result1 = await agent1.execute();
  const result2 = await agent2.process(result1);
  await orchestrator.completePhase('phase-name', result2);
}
```

## Agent Dependencies

```
Agent A depends on:
  - Agent B (for data)
  - Agent C (for processing)

Agent B depends on:
  - Agent D (for validation)
```

## Error Handling

### Agent-Level Errors

**Pattern:** [How agents handle errors]

**Example:**
```javascript
// Purpose: Demonstrate agent error handling
try {
  const result = await agent.execute(input);
} catch (error) {
  await orchestrator.handleAgentError(agent, error);
}
```

### System-Level Errors

**Pattern:** [How system handles agent failures]

**Example:**
```javascript
// Purpose: Demonstrate system error handling
if (agent.failed) {
  await orchestrator.failoverToBackup(agent);
}
```

## Examples

### Basic Multi-Agent Workflow

```javascript
// Purpose: Complete multi-agent workflow example
async function executeWorkflow() {
  // Phase 1: Initialization
  await agent1.initialize();
  await agent2.initialize();
  
  // Phase 2: Processing
  const data = await agent1.collect();
  const processed = await agent2.process(data);
  
  // Phase 3: Completion
  await agent3.finalize(processed);
}
```

### Agent Communication

```javascript
// Purpose: Demonstrate agent-to-agent communication
class AgentA {
  async communicateWithAgentB(data) {
    const message = {
      from: 'AgentA',
      to: 'AgentB',
      type: 'request',
      payload: data
    };
    
    const response = await this.messageBus.send(message);
    return response;
  }
}
```

## Troubleshooting

### Common Issues

**Issue:** Agent not responding

**Solution:**
1. Check agent status
2. Verify communication channel
3. Check agent logs
4. Restart agent if needed

**Issue:** Message delivery failure

**Solution:**
1. Verify message format
2. Check agent availability
3. Verify message bus connectivity
4. Retry with exponential backoff

## Related Documentation

### Agents
- [Agent 1](../agents/agent1.md) - Description
- [Agent 2](../agents/agent2.md) - Description

### Orchestration
- [Orchestrator](../orchestration/orchestrator.md) - Description

### Communication
- [Message Bus](../communication/message-bus.md) - Description
```

---

## Multi-Agent Specific Patterns

### Agent Definition Pattern

```javascript
// Purpose: Document agent definition
class AgentName {
  constructor(config) {
    this.config = config;
    this.role = 'agent-role';
    this.capabilities = ['capability1', 'capability2'];
  }
  
  async execute(input) {
    // Agent logic
  }
}
```

### Orchestration Pattern

```javascript
// Purpose: Document orchestration pattern
class Orchestrator {
  async executeWorkflow(phases) {
    for (const phase of phases) {
      await this.executePhase(phase);
    }
  }
  
  async executePhase(phase) {
    const agents = phase.agents;
    const results = await Promise.all(
      agents.map(agent => agent.execute())
    );
    return results;
  }
}
```

### Communication Pattern

```javascript
// Purpose: Document communication pattern
class MessageBus {
  async send(message) {
    const agent = this.getAgent(message.to);
    return await agent.handleMessage(message);
  }
}
```

---

## QUALITY CHECK

### Completeness

- [ ] All agents documented
- [ ] All communication patterns documented
- [ ] Orchestration flow documented
- [ ] Examples provided
- [ ] Error handling documented

### Accuracy

- [ ] Agent roles accurate
- [ ] Communication patterns correct
- [ ] Orchestration flow verified
- [ ] Examples work

### Multi-Agent Specific Checks

- [ ] Agent dependencies documented
- [ ] Communication patterns explained
- [ ] Orchestration flow clear
- [ ] Error handling comprehensive
- [ ] Agent interactions documented

### Quality Score

**Target:** 95%+
**Achieved:** ___

---

## OMEGA Learning

**Documentation patterns:**
- Multi-agent architecture patterns
- Agent communication patterns
- Orchestration patterns

**Commonly underdocumented:**
- Agent dependencies
- Communication protocols
- Error handling across agents
- Orchestration flow details

```bash
forge omega learn
```

---

## Related Documentation

- [HARVEST Framework](../../frameworks/universal_harvest.md) - Documentation methodology
- [Pattern Library](../../docs/PATTERN_LIBRARY.md) - Comprehensive pattern catalog
- [Architecture Patterns](../../docs/DOCUMENTATION_PATTERNS.md) - Architecture-specific patterns

---

**Template Version:** 1.0
**Created:** 2025-01-XX
**Framework:** FORGE Documentation Engineering Patterns

