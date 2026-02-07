# MCP Integration

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Enable tool use via Model Context Protocol for AI agents.

---

## Overview

Model Context Protocol (MCP) is a standard protocol that enables AI models to interact with external tools and services. FORGE integrates with MCP to provide AI agents with access to a wide range of capabilities, including browser automation, filesystem operations, shell commands, and custom tools.

---

## What is MCP?

Model Context Protocol (MCP) is an open standard developed by Anthropic for AI models to securely interact with external tools and services. It provides:

- **Standardized Interface** - Consistent API for tool access across different AI models
- **Security** - Sandboxed execution environment for tools
- **Extensibility** - Easy to add new tools and capabilities
- **Type Safety** - Strong typing for tool inputs and outputs

---

## Available Tools

| Tool | Purpose | MCP Server |
|------|---------|------------|
| **browser** | Web browsing and automation | `@anthropic-ai/mcp-server-playwright` |
| **filesystem** | File read/write operations | `@anthropic-ai/mcp-server-filesystem` |
| **shell** | Command execution | `@anthropic-ai/mcp-server-shell` |
| **generate_totp** | TOTP token generation | Custom (forge-helper) |
| **save_deliverable** | Save agent deliverables | Custom (forge-helper) |

---

## Integration Pattern

### Basic MCP Setup

```javascript
import { query } from '@anthropic-ai/claude-agent-sdk';

// Configure MCP servers
const mcpServers = {
  browser: {
    command: 'npx',
    args: ['@anthropic-ai/mcp-server-playwright']
  },
  filesystem: {
    command: 'npx',
    args: ['@anthropic-ai/mcp-server-filesystem', '--path', '/path/to/allowed/dir']
  },
  shell: {
    command: 'npx',
    args: ['@anthropic-ai/mcp-server-shell']
  }
};

// Create Claude agent with MCP servers
const response = await query({
  model: 'claude-3-5-sonnet-20241022',
  messages: [
    {
      role: 'user',
      content: 'Navigate to https://example.com and take a screenshot'
    }
  ],
  mcpServers: mcpServers
});
```

### Custom MCP Server (FORGE Helper)

Create a custom MCP server for FORGE-specific tools:

```javascript
import { createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';
import { saveDeliverableTool } from './tools/save-deliverable.js';
import { generateTotpTool } from './tools/generate-totp.js';

export function createForgeHelperServer(targetDir) {
  // Store target directory for tool access
  global.__FORGE_TARGET_DIR = targetDir;

  return createSdkMcpServer({
    name: 'forge-helper',
    version: '1.0.0',
    tools: [saveDeliverableTool, generateTotpTool],
  });
}

// Example: save_deliverable tool
export const saveDeliverableTool = {
  name: 'save_deliverable',
  description: 'Save agent deliverable to target directory',
  inputSchema: {
    type: 'object',
    properties: {
      filename: {
        type: 'string',
        description: 'Filename to save'
      },
      content: {
        type: 'string',
        description: 'Content to save'
      }
    },
    required: ['filename', 'content']
  },
  execute: async ({ filename, content }) => {
    const targetDir = global.__FORGE_TARGET_DIR;
    const filePath = path.join(targetDir, filename);
    await fs.promises.writeFile(filePath, content, 'utf8');
    return { success: true, path: filePath };
  }
};
```

---

## Using MCP in FORGEs

### R-I-S-E with MCP

```javascript
// Research phase - Use browser to gather information
const researchPrompt = `
Research the topic: ${topic}
Use the browser tool to:
1. Navigate to relevant websites
2. Extract key information
3. Take screenshots of important pages
`;

// Identify phase - Use filesystem to analyze code
const identifyPrompt = `
Analyze the codebase in ${repoPath}
Use the filesystem tool to:
1. Read source files
2. Identify patterns
3. Extract key components
`;

// Synthesize phase - Use shell to run tests
const synthesizePrompt = `
Synthesize findings and run tests
Use the shell tool to:
1. Run unit tests
2. Execute linting
3. Check build status
`;

// Execute phase - Use all tools as needed
const executePrompt = `
Implement the solution
Use all available tools:
- Browser: Test web interface
- Filesystem: Write code files
- Shell: Run build commands
`;
```

### C-A-R-E with MCP

```javascript
// Context phase - Use filesystem to read logs
const contextPrompt = `
Gather context about the issue
Use the filesystem tool to:
1. Read error logs
2. Check configuration files
3. Review recent changes
`;

// Analyze phase - Use shell to run diagnostics
const analyzePrompt = `
Analyze the problem
Use the shell tool to:
1. Run diagnostic commands
2. Check system status
3. Gather metrics
`;

// Respond phase - Use filesystem to apply fixes
const respondPrompt = `
Apply the fix
Use the filesystem tool to:
1. Update configuration files
2. Modify source code
3. Save changes
`;

// Evaluate phase - Use browser to verify
const evaluatePrompt = `
Verify the fix works
Use the browser tool to:
1. Navigate to application
2. Test functionality
3. Take verification screenshots
`;
```

---

## MCP Server Configuration

### Playwright Browser Server

```javascript
const playwrightServer = {
  command: 'npx',
  args: [
    '@anthropic-ai/mcp-server-playwright',
    '--browser', 'chromium',  // or 'firefox', 'webkit'
    '--headless', 'true',     // Run in headless mode
    '--user-data-dir', '/tmp/playwright-agent1'  // Isolated profile
  ]
};
```

### Filesystem Server

```javascript
const filesystemServer = {
  command: 'npx',
  args: [
    '@anthropic-ai/mcp-server-filesystem',
    '--path', '/path/to/allowed/directory'  // Sandboxed directory
  ]
};
```

### Shell Server

```javascript
const shellServer = {
  command: 'npx',
  args: [
    '@anthropic-ai/mcp-server-shell',
    '--allowed-commands', 'git,npm,node'  // Whitelist commands
  ]
};
```

---

## Tool Usage Examples

### Browser Automation

```javascript
// Navigate to URL
const result = await agent.useTool('browser', {
  action: 'navigate',
  url: 'https://example.com'
});

// Click element
await agent.useTool('browser', {
  action: 'click',
  selector: 'button#submit'
});

// Fill form
await agent.useTool('browser', {
  action: 'fill',
  selector: 'input#username',
  value: 'testuser'
});

// Take screenshot
await agent.useTool('browser', {
  action: 'screenshot',
  path: 'screenshot.png'
});
```

### Filesystem Operations

```javascript
// Read file
const content = await agent.useTool('filesystem', {
  action: 'read',
  path: 'src/main.js'
});

// Write file
await agent.useTool('filesystem', {
  action: 'write',
  path: 'src/main.js',
  content: '// Updated code'
});

// List directory
const files = await agent.useTool('filesystem', {
  action: 'list',
  path: 'src/'
});
```

### Shell Commands

```javascript
// Execute command
const result = await agent.useTool('shell', {
  command: 'git status',
  cwd: '/path/to/repo'
});

// Run test suite
await agent.useTool('shell', {
  command: 'npm test',
  cwd: '/path/to/project'
});
```

---

## Security Considerations

### Sandboxing

- **Filesystem Access** - Limit to specific directories
- **Shell Commands** - Whitelist allowed commands
- **Browser Isolation** - Use separate user data directories per agent
- **Network Access** - Restrict to allowed domains (if possible)

### Best Practices

1. **Isolate Agents** - Each parallel agent should have its own MCP server instance
2. **Clean Up** - Remove temporary files and browser profiles after execution
3. **Validate Inputs** - Always validate tool inputs before execution
4. **Log Tool Usage** - Log all tool invocations for audit purposes

---

## Related Documentation

- [Browser Automation](./browser_automation.md) - Playwright patterns and best practices
- [Session Manager](../execution/session_manager.md) - Persistent state management
- [Parallel Agents](../execution/parallel_agents.md) - Multi-agent orchestration
- [Error Handling](../execution/error_handling.md) - Retry logic and error categories
- [R-I-S-E Framework](../frameworks/universal_rise.md) - Research → Identify → Synthesize → Execute
- [C-A-R-E Framework](../frameworks/universal_care.md) - Context → Analyze → Respond → Evaluate

