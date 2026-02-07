# Browser Automation

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Enable AI agents to interact with web applications.

---

## Overview

Browser Automation enables AI agents to interact with web applications through programmatic control of a web browser. FORGE integrates with Playwright via MCP to provide comprehensive browser automation capabilities.

---

## Capabilities

- **Navigate** - Navigate to URLs and manage browser history
- **Interact** - Click buttons, fill forms, select options
- **Extract** - Read content, extract text, capture screenshots
- **Wait** - Wait for elements, network requests, or conditions
- **Debug** - Access console messages, network requests, and page state
- **Authenticate** - Handle login forms, cookies, and sessions

---

## Integration with Playwright

### Via MCP (Recommended)

```javascript
import { query } from '@anthropic-ai/claude-agent-sdk';

// Configure Playwright MCP server
const mcpServers = {
  browser: {
    command: 'npx',
    args: [
      '@anthropic-ai/mcp-server-playwright',
      '--browser', 'chromium',
      '--headless', 'true',
      '--user-data-dir', '/tmp/playwright-agent1'
    ]
  }
};

// Use browser tools via MCP
const response = await query({
  model: 'claude-3-5-sonnet-20241022',
  messages: [
    {
      role: 'user',
      content: 'Navigate to https://example.com and click the login button'
    }
  ],
  mcpServers: mcpServers
});
```

### Direct Playwright (Advanced)

```javascript
import { chromium } from 'playwright';

// Launch browser
const browser = await chromium.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

// Create new page
const page = await browser.newPage();

// Navigate
await page.goto('https://example.com');

// Interact
await page.click('button#login');
await page.fill('input#username', 'testuser');
await page.fill('input#password', 'password123');
await page.click('button#submit');

// Extract
const title = await page.title();
const content = await page.textContent('div#content');

// Screenshot
await page.screenshot({ path: 'screenshot.png' });

// Close
await browser.close();
```

---

## Common Patterns

### Navigation

```javascript
// Navigate to URL
await agent.useTool('browser', {
  action: 'navigate',
  url: 'https://example.com'
});

// Navigate back
await agent.useTool('browser', {
  action: 'navigate_back'
});

// Wait for navigation
await agent.useTool('browser', {
  action: 'wait_for',
  condition: 'networkidle'
});
```

### Form Interaction

```javascript
// Fill input field
await agent.useTool('browser', {
  action: 'fill',
  selector: 'input#username',
  value: 'testuser'
});

// Select dropdown
await agent.useTool('browser', {
  action: 'select',
  selector: 'select#country',
  value: 'US'
});

// Upload file
await agent.useTool('browser', {
  action: 'upload',
  selector: 'input[type="file"]',
  file: '/path/to/file.pdf'
});

// Submit form
await agent.useTool('browser', {
  action: 'click',
  selector: 'button[type="submit"]'
});
```

### Content Extraction

```javascript
// Get page title
const title = await agent.useTool('browser', {
  action: 'evaluate',
  script: 'document.title'
});

// Extract text content
const text = await agent.useTool('browser', {
  action: 'evaluate',
  script: 'document.querySelector("#content").textContent'
});

// Get all links
const links = await agent.useTool('browser', {
  action: 'evaluate',
  script: 'Array.from(document.querySelectorAll("a")).map(a => a.href)'
});
```

### Screenshots and Snapshots

```javascript
// Take screenshot
await agent.useTool('browser', {
  action: 'screenshot',
  path: 'screenshot.png',
  fullPage: true  // Capture full page, not just viewport
});

// Get accessibility snapshot
const snapshot = await agent.useTool('browser', {
  action: 'snapshot'  // Returns accessibility tree
});
```

### Waiting and Debugging

```javascript
// Wait for element
await agent.useTool('browser', {
  action: 'wait_for',
  selector: 'div#content',
  timeout: 5000
});

// Wait for text
await agent.useTool('browser', {
  action: 'wait_for',
  text: 'Loading complete',
  timeout: 10000
});

// Get console messages
const messages = await agent.useTool('browser', {
  action: 'console_messages'
});

// Get network requests
const requests = await agent.useTool('browser', {
  action: 'network_requests'
});
```

---

## Use Cases in FORGE

### 1. Research Phase (R-I-S-E)

Gather information from web sources:

```javascript
const researchPrompt = `
Research the topic: ${topic}
Use the browser to:
1. Navigate to relevant websites
2. Extract key information
3. Take screenshots of important pages
4. Follow links to related resources
`;
```

### 2. Verification Phase

Test web applications:

```javascript
const verifyPrompt = `
Verify the application works correctly
Use the browser to:
1. Navigate to the application
2. Test key functionality
3. Verify UI elements render correctly
4. Check for errors in console
`;
```

### 3. Documentation

Screenshot UI for documentation:

```javascript
const docPrompt = `
Document the user interface
Use the browser to:
1. Navigate through all pages
2. Take screenshots of each page
3. Extract UI element descriptions
4. Create documentation with images
`;
```

### 4. Security Testing

Execute web exploits (with proper authorization):

```javascript
const securityPrompt = `
Test for security vulnerabilities
Use the browser to:
1. Navigate to target application
2. Attempt injection attacks
3. Test authentication bypass
4. Document findings with screenshots
`;
```

---

## Best Practices

### Isolation

- **Separate Browser Instances** - Each parallel agent should have its own browser instance
- **Isolated User Data** - Use separate `--user-data-dir` for each agent
- **Clean Up** - Close browsers and clean up temporary files after execution

### Error Handling

```javascript
try {
  await agent.useTool('browser', {
    action: 'navigate',
    url: 'https://example.com'
  });
} catch (error) {
  if (error.message.includes('timeout')) {
    // Retry with longer timeout
    await agent.useTool('browser', {
      action: 'navigate',
      url: 'https://example.com',
      timeout: 30000
    });
  } else {
    throw error;
  }
}
```

### Performance

- **Headless Mode** - Use headless mode for faster execution
- **Resource Limits** - Disable images/videos if not needed
- **Connection Pooling** - Reuse browser instances when possible

---

## Related Documentation

- [MCP Integration](./mcp_integration.md) - Model Context Protocol setup
- [Session Manager](../execution/session_manager.md) - Persistent state management
- [Parallel Agents](../execution/parallel_agents.md) - Multi-agent orchestration
- [R-I-S-E Framework](../frameworks/universal_rise.md) - Research → Identify → Synthesize → Execute
- [C-A-R-E Framework](../frameworks/universal_care.md) - Context → Analyze → Respond → Evaluate

