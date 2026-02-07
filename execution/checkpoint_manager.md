# Checkpoint Manager

**Version:** 1.0.0  
**Last Updated:** 2025-01-XX  
**Purpose:** Enable rollback and recovery using git-based checkpointing.

---

## Overview

The Checkpoint Manager provides git-based checkpointing capabilities, allowing tasks to be rolled back to any previous checkpoint. This enables safe experimentation, error recovery, and the ability to retry failed operations without losing completed work.

---

## Core Concepts

### Checkpoint Creation

Checkpoints are created at key points during execution:

- **After Phase Completion** - Save state after each R-I-S-E or C-A-R-E phase
- **After Agent Completion** - Save state after each parallel agent completes
- **Before Risky Operations** - Create checkpoint before operations that might fail
- **On User Request** - Allow manual checkpoint creation

Each checkpoint:
- Creates a git commit with all current changes
- Tags the commit for easy reference
- Includes metadata in the commit message
- Returns the commit hash for session tracking

### Rollback

Rollback restores the workspace to a previous checkpoint:

- **Find Checkpoint** - Locate the git commit/tag for the checkpoint
- **Reset Working Directory** - Use `git reset --hard` to restore files
- **Clean Untracked Files** - Use `git clean -fd` to remove untracked files
- **Preserve Audit Logs** - Audit logs are never rolled back (they're append-only)
- **Update Session State** - Mark agents/steps as rolled back in session state

### Recovery

The checkpoint system enables recovery from failures:

- **Detect Incomplete Sessions** - Find sessions that didn't complete
- **Offer Rollback Options** - Present available checkpoints to user
- **Resume from Last Good State** - Continue execution from checkpoint

---

## Implementation Pattern

### Basic Checkpoint Manager Class

```javascript
import { $ } from 'zx';
import chalk from 'chalk';

class CheckpointManager {
  /**
   * Create a git checkpoint
   * @param {string} sourceDir - Git repository directory
   * @param {string} description - Checkpoint description
   * @param {number} [attempt=1] - Attempt number (for retries)
   * @returns {Promise<Object>} Checkpoint result with commit hash
   */
  async createCheckpoint(sourceDir, description, attempt = 1) {
    console.log(chalk.blue(`📍 Creating checkpoint for ${description} (attempt ${attempt})`));
    
    try {
      // Check for uncommitted changes
      const status = await $`cd ${sourceDir} && git status --porcelain`;
      const hasChanges = status.stdout.trim().length > 0;
      
      // Stage all changes
      await $`cd ${sourceDir} && git add -A`;
      
      // Create commit with metadata
      const commitMessage = `📍 Checkpoint: ${description} (attempt ${attempt})`;
      await $`cd ${sourceDir} && git commit -m ${commitMessage} --allow-empty`;
      
      // Get commit hash
      const commitHash = await $`cd ${sourceDir} && git rev-parse HEAD`;
      const hash = commitHash.stdout.trim();
      
      // Tag for easy reference
      const tagName = `forge-${this.sessionId}-${description.replace(/\s+/g, '-')}`;
      await $`cd ${sourceDir} && git tag ${tagName} ${hash}`;
      
      if (hasChanges) {
        console.log(chalk.blue(`✅ Checkpoint created with uncommitted changes staged`));
      } else {
        console.log(chalk.blue(`✅ Empty checkpoint created (no workspace changes)`));
      }
      
      return { success: true, commitHash: hash, tagName };
    } catch (error) {
      console.log(chalk.yellow(`⚠️ Checkpoint creation failed: ${error.message}`));
      return { success: false, error: error.message };
    }
  }
  
  /**
   * Rollback workspace to specific checkpoint
   * @param {string} sourceDir - Git repository directory
   * @param {string} checkpointName - Checkpoint name or commit hash
   * @param {string} reason - Reason for rollback
   * @returns {Promise<Object>} Rollback result
   */
  async rollbackTo(sourceDir, checkpointName, reason = 'retry preparation') {
    console.log(chalk.yellow(`🔄 Rolling back workspace for ${reason}`));
    
    try {
      // Find checkpoint commit (by tag or hash)
      let commitHash;
      try {
        // Try as tag first
        const tagRef = await $`cd ${sourceDir} && git rev-parse ${checkpointName}`;
        commitHash = tagRef.stdout.trim();
      } catch {
        // Try as commit hash
        commitHash = checkpointName;
      }
      
      // Show what we're about to remove
      const status = await $`cd ${sourceDir} && git status --porcelain`;
      const changes = status.stdout.trim().split('\n').filter(line => line.length > 0);
      
      // Reset to checkpoint commit
      await $`cd ${sourceDir} && git reset --hard ${commitHash}`;
      
      // Clean untracked files
      await $`cd ${sourceDir} && git clean -fd`;
      
      if (changes.length > 0) {
        console.log(chalk.yellow(`✅ Rollback completed - removed ${changes.length} contaminated changes`));
      } else {
        console.log(chalk.yellow(`✅ Rollback completed - no changes to remove`));
      }
      
      return { success: true, commitHash };
    } catch (error) {
      console.log(chalk.red(`❌ Rollback failed: ${error.message}`));
      return { success: false, error: error.message };
    }
  }
  
  /**
   * List all checkpoints for a session
   * @param {string} sourceDir - Git repository directory
   * @param {string} sessionId - Session ID
   * @returns {Promise<Array>} List of checkpoints with metadata
   */
  async listCheckpoints(sourceDir, sessionId) {
    try {
      // Get all tags for this session
      const tags = await $`cd ${sourceDir} && git tag -l forge-${sessionId}-*`;
      const tagList = tags.stdout.trim().split('\n').filter(tag => tag.length > 0);
      
      const checkpoints = [];
      
      for (const tag of tagList) {
        // Get commit hash for tag
        const commitHash = await $`cd ${sourceDir} && git rev-parse ${tag}`;
        const hash = commitHash.stdout.trim();
        
        // Get commit message
        const commitMessage = await $`cd ${sourceDir} && git log -1 --format=%B ${hash}`;
        const message = commitMessage.stdout.trim();
        
        // Get commit date
        const commitDate = await $`cd ${sourceDir} && git log -1 --format=%ci ${hash}`;
        const date = commitDate.stdout.trim();
        
        checkpoints.push({
          tag,
          commitHash: hash,
          message,
          date
        });
      }
      
      return checkpoints.sort((a, b) => new Date(b.date) - new Date(a.date));
    } catch (error) {
      console.log(chalk.yellow(`⚠️ Failed to list checkpoints: ${error.message}`));
      return [];
    }
  }
}
```

---

## Checkpoint Naming Convention

Checkpoints use a consistent naming convention:

- **Format:** `forge-{session-id}-{phase}-{step}`
- **Example:** `forge-abc123-rise-research`
- **Example:** `forge-abc123-care-context`

This allows easy identification and filtering of checkpoints by session and phase.

---

## Concurrency Safety

When using parallel agents, use a semaphore to prevent git lock conflicts:

```javascript
class GitSemaphore {
  constructor() {
    this.queue = [];
    this.running = false;
  }
  
  async acquire() {
    return new Promise((resolve) => {
      this.queue.push(resolve);
      this.process();
    });
  }
  
  release() {
    this.running = false;
    this.process();
  }
  
  process() {
    if (!this.running && this.queue.length > 0) {
      this.running = true;
      const resolve = this.queue.shift();
      resolve();
    }
  }
}

const gitSemaphore = new GitSemaphore();

async function createCheckpointWithLock(sourceDir, description) {
  await gitSemaphore.acquire();
  
  try {
    return await checkpointManager.createCheckpoint(sourceDir, description);
  } finally {
    gitSemaphore.release();
  }
}
```

---

## Retry Logic

Handle git lock conflicts with retry logic:

```javascript
async function createCheckpointWithRetry(sourceDir, description, maxRetries = 5) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await checkpointManager.createCheckpoint(sourceDir, description, attempt);
    } catch (error) {
      const isLockError = error.message.includes('index.lock') ||
                         error.message.includes('unable to lock');
      
      if (isLockError && attempt < maxRetries) {
        const delay = Math.pow(2, attempt - 1) * 1000; // Exponential backoff
        console.log(chalk.yellow(`⚠️ Git lock conflict (attempt ${attempt}/${maxRetries}). Retrying in ${delay}ms...`));
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      
      throw error;
    }
  }
}
```

---

## Integration with Session Manager

Checkpoints are tracked in session state:

```javascript
// Create checkpoint and update session
const checkpointResult = await checkpointManager.createCheckpoint(
  sourceDir,
  'research-phase',
  1
);

if (checkpointResult.success) {
  await sessionManager.checkpoint(
    sessionId,
    'research',
    checkpointResult.commitHash
  );
}
```

---

## Related Documentation

- [Session Manager](./session_manager.md) - Persistent state management
- [Audit System](./audit_system.md) - Crash-safe logging
- [Parallel Agents](./parallel_agents.md) - Multi-agent orchestration
- [Error Handling](./error_handling.md) - Retry logic and error categories

