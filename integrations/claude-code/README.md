# FORGE × Claude Code Integration

Native [Claude Code](https://claude.com/claude-code) bindings for the FORGE framework. Removes the "paste FORGE_MASTER.md into chat" friction — invoke FORGE workflows and personas as first-class slash commands instead.

## What's in this directory

```
integrations/claude-code/
├── README.md                         # this file
├── commands/                         # slash commands
│   ├── rise.md                       # /rise — R-I-S-E workflow (creation/transformation)
│   ├── care.md                       # /care — C-A-R-E workflow (repair/optimization)
│   ├── harvest.md                    # /harvest — HARVEST workflow (understanding)
│   ├── atlas.md                      # /atlas — Deep Research persona
│   ├── sage.md                       # /sage — Architecture persona
│   ├── scribe.md                     # /scribe — Documentation persona
│   └── sentinel.md                   # /sentinel — Security persona
└── skills/
    └── forge-classifier/
        └── SKILL.md                  # auto-suggests routing for unrouted tasks
```

## Install

### 1. Decide where you want this active

| Scope | Install path | When to use |
|---|---|---|
| **User-level** (all projects) | `~/.claude/commands/` and `~/.claude/skills/` | Recommended — FORGE applies across projects |
| **Project-level** (one repo) | `<project>/.claude/commands/` and `<project>/.claude/skills/` | When only one repo should use FORGE |

On Windows, `~/.claude/` is `C:\Users\<you>\.claude\`.

### 2. Copy the files

```bash
# User-level (Linux/Mac)
cp -r commands/*  ~/.claude/commands/
cp -r skills/*    ~/.claude/skills/

# User-level (Windows PowerShell)
Copy-Item commands/* "$env:USERPROFILE\.claude\commands\" -Recurse
Copy-Item skills/*   "$env:USERPROFILE\.claude\skills\"   -Recurse
```

### 3. Replace the `<FORGE_HOME>` placeholder

Every file references `<FORGE_HOME>/...` paths. Replace with the absolute path to your local clone of `forge-framework`.

```bash
# Linux/Mac — replace in place
find ~/.claude/commands ~/.claude/skills -type f -name '*.md' \
  -exec sed -i 's|<FORGE_HOME>|/path/to/forge-framework|g' {} +

# Windows PowerShell
Get-ChildItem "$env:USERPROFILE\.claude\commands","$env:USERPROFILE\.claude\skills" -Recurse -Filter *.md |
  ForEach-Object {
    (Get-Content $_.FullName) -replace '<FORGE_HOME>','C:\path\to\forge-framework' |
      Set-Content $_.FullName
  }
```

### 4. Verify

In Claude Code, type `/` — you should see `/rise`, `/care`, `/harvest`, `/atlas`, `/sage`, `/scribe`, `/sentinel` listed. The `forge-classifier` skill will auto-suggest routing whenever you describe an unrouted engineering task.

## Usage

### Workflow commands

```
/rise Build a notification filtering system in React + TypeScript
/care Fix the race condition in the order processing queue
/harvest Document how the authentication system works
```

Each command reads its workflow file from `<FORGE_HOME>` and applies it to your task with the full Confidence/Assumption/Meta-Prompting/Verification protocol stack.

### Persona commands

```
/atlas DEEP technical — "Best practices for warehouse automation inventory optimization"
/sage FULL — "Real-time notification system for 1M daily users"
/scribe COMPREHENSIVE Tutorial for beginners — "How to use the equipment monitoring API"
/sentinel scope: owned web app — "OWASP Top 10 assessment"
```

Each persona command loads the full persona file and adopts the role.

### Auto-classification (forge-classifier skill)

If you describe a task without invoking a slash command, the skill suggests the right route:

> *User:* "I need to refactor the payment service to use the new async API"
>
> *Claude (via skill):* **FORGE classification:** TRANSFORMATION / Complex / web_development (confidence 8/10). **Suggested:** `/rise` — refactoring this scope benefits from the Research → Identify → Synthesize → Execute pass. Or proceed without — your call.

The skill suggests once per task and never nags.

## Design notes

- **No hook required.** The skill's `description` field triggers proactive invocation when the prompt matches engineering-task language. A `UserPromptSubmit` hook would be redundant.
- **`$FORGE_HOME` placeholder over hardcoded paths.** Lets users install without forking the integration.
- **Slash commands inline the workflow body via Read** rather than copying it. Keeps the commands small and stays in sync with the canonical workflow files.
- **Phase 0 retrieval is wired but no-ops** until the persistent learnings store (Plan 1) is built. When that ships, every workflow invocation auto-loads relevant prior learnings.

## Troubleshooting

**Slash commands don't appear after copying.** Restart Claude Code, then type `/` to refresh the command list.

**`forge-classifier` skill never triggers.** Confirm the file is at `~/.claude/skills/forge-classifier/SKILL.md` (not `~/.claude/skills/SKILL.md`). The directory name must match the `name:` frontmatter field.

**Commands fail with "file not found".** The `<FORGE_HOME>` placeholder wasn't replaced. Re-run step 3 of install.

---

*Part of the FORGE Framework — https://github.com/0xPliny/forge-framework*
