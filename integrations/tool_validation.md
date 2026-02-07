# Tool Validation

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Validate tool availability before execution to prevent runtime failures.

---

## Overview

Tool Validation ensures that all required external tools are available before task execution begins. This prevents failures mid-execution and provides clear error messages when tools are missing.

---

## Core Concepts

### Tool Checking

Before execution, validate that all required tools are:

- **Installed** - Tool executable exists in PATH
- **Executable** - Tool has execute permissions
- **Correct Version** - Tool version meets requirements (if specified)
- **Accessible** - Tool can be invoked successfully

### Error Handling

When tools are missing:

- **Clear Error Messages** - Tell user exactly what's missing
- **Installation Guidance** - Provide instructions for installing missing tools
- **Graceful Degradation** - Skip optional tools, fail on required tools

---

## Implementation Pattern

### Basic Tool Checker

```javascript
import { $ } from 'zx';
import chalk from 'chalk';

class ToolChecker {
  /**
   * Check if a tool is available
   * @param {string} toolName - Tool name (e.g., 'git', 'node', 'npm')
   * @param {Object} options - Options
   * @param {string} [options.versionFlag] - Version flag (e.g., '--version')
   * @param {string} [options.minVersion] - Minimum required version
   * @returns {Promise<Object>} Check result
   */
  async checkTool(toolName, options = {}) {
    try {
      // Try to execute the tool
      const result = await $`which ${toolName}`;
      
      if (result.exitCode !== 0) {
        return {
          available: false,
          error: `Tool '${toolName}' not found in PATH`
        };
      }
      
      const toolPath = result.stdout.trim();
      
      // Check version if requested
      if (options.versionFlag) {
        try {
          const versionResult = await $`${toolName} ${options.versionFlag}`;
          const version = versionResult.stdout.trim();
          
          if (options.minVersion) {
            const meetsRequirement = this.compareVersions(version, options.minVersion);
            if (!meetsRequirement) {
              return {
                available: true,
                path: toolPath,
                version: version,
                meetsRequirement: false,
                error: `Tool '${toolName}' version ${version} does not meet minimum requirement ${options.minVersion}`
              };
            }
          }
          
          return {
            available: true,
            path: toolPath,
            version: version,
            meetsRequirement: true
          };
        } catch (error) {
          return {
            available: true,
            path: toolPath,
            version: null,
            error: `Could not determine version: ${error.message}`
          };
        }
      }
      
      return {
        available: true,
        path: toolPath
      };
    } catch (error) {
      return {
        available: false,
        error: error.message
      };
    }
  }
  
  /**
   * Check multiple tools
   * @param {Array<Object>} tools - Array of tool definitions
   * @returns {Promise<Object>} Check results
   */
  async checkTools(tools) {
    const results = {};
    const missing = [];
    const outdated = [];
    
    for (const tool of tools) {
      const result = await this.checkTool(tool.name, {
        versionFlag: tool.versionFlag,
        minVersion: tool.minVersion
      });
      
      results[tool.name] = result;
      
      if (!result.available) {
        missing.push(tool);
      } else if (result.meetsRequirement === false) {
        outdated.push(tool);
      }
    }
    
    return {
      results,
      missing,
      outdated,
      allAvailable: missing.length === 0 && outdated.length === 0
    };
  }
  
  /**
   * Compare version strings
   * @private
   * @param {string} version1 - Version to compare
   * @param {string} version2 - Minimum required version
   * @returns {boolean} True if version1 >= version2
   */
  compareVersions(version1, version2) {
    // Simple semantic version comparison
    const v1Parts = version1.split('.').map(Number);
    const v2Parts = version2.split('.').map(Number);
    
    for (let i = 0; i < Math.max(v1Parts.length, v2Parts.length); i++) {
      const v1Part = v1Parts[i] || 0;
      const v2Part = v2Parts[i] || 0;
      
      if (v1Part > v2Part) return true;
      if (v1Part < v2Part) return false;
    }
    
    return true; // Equal versions
  }
}
```

---

## Tool Definitions

### Common Tools

```javascript
const REQUIRED_TOOLS = [
  {
    name: 'git',
    versionFlag: '--version',
    minVersion: '2.0.0',
    required: true,
    installInstructions: 'Install Git from https://git-scm.com/'
  },
  {
    name: 'node',
    versionFlag: '--version',
    minVersion: '18.0.0',
    required: true,
    installInstructions: 'Install Node.js from https://nodejs.org/'
  },
  {
    name: 'npm',
    versionFlag: '--version',
    minVersion: '9.0.0',
    required: true,
    installInstructions: 'npm comes with Node.js'
  }
];

const OPTIONAL_TOOLS = [
  {
    name: 'docker',
    versionFlag: '--version',
    required: false,
    installInstructions: 'Install Docker from https://www.docker.com/'
  }
];
```

---

## Integration with Execution

### Pre-Execution Validation

```javascript
import { ToolChecker } from './tool-validation.js';

async function validateToolsBeforeExecution(config) {
  const checker = new ToolChecker();
  
  // Get required tools from config
  const requiredTools = config.tools?.required || [];
  const optionalTools = config.tools?.optional || [];
  
  // Check required tools
  const requiredResults = await checker.checkTools(requiredTools);
  
  if (!requiredResults.allAvailable) {
    console.log(chalk.red('❌ Missing required tools:'));
    for (const tool of requiredResults.missing) {
      console.log(chalk.red(`   - ${tool.name}: ${tool.installInstructions}`));
    }
    throw new Error('Required tools are missing');
  }
  
  // Check optional tools (warn but don't fail)
  const optionalResults = await checker.checkTools(optionalTools);
  if (optionalResults.missing.length > 0) {
    console.log(chalk.yellow('⚠️ Optional tools not available:'));
    for (const tool of optionalResults.missing) {
      console.log(chalk.yellow(`   - ${tool.name}: ${tool.installInstructions}`));
    }
  }
  
  return {
    required: requiredResults,
    optional: optionalResults
  };
}
```

---

## Error Messages

### Missing Tool

```
❌ Tool 'git' not found in PATH

Installation instructions:
  Install Git from https://git-scm.com/
```

### Outdated Tool

```
⚠️ Tool 'node' version 16.0.0 does not meet minimum requirement 18.0.0

Please upgrade Node.js:
  Install Node.js 18+ from https://nodejs.org/
```

---

## Related Documentation

- [MCP Integration](./mcp_integration.md) - Model Context Protocol setup
- [Browser Automation](./browser_automation.md) - Playwright patterns
- [Error Handling](../execution/error_handling.md) - Retry logic and error categories
- [Session Manager](../execution/session_manager.md) - Persistent state management

