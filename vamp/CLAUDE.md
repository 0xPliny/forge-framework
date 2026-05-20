# Vamp — workspace brain

This folder is a **Vamp workspace**. When it's open in Claude Code, you act as
the vamp engine.

**On any of these, execute the Vamp Protocol — read `VAMP_PROTOCOL.md` in full first, then follow it exactly:**

- `vamp <git-url-or-path>` — full vamp
- `vamp <target> --skeleton-only | --graph` — partial modes
- `vamp <a> <b> --synthesize` — multi-repo synthesis
- `vamp <old> <new> --diff` — architectural diff
- the `/vamp` slash command (see `.claude/commands/vamp.md`)

If the user just says "vamp" with no target, ask for the git URL or local path.

## Non-negotiables (full detail in `VAMP_PROTOCOL.md`)

- **Never copy source code verbatim.** Extract structure and understanding;
  paraphrase; signatures and <8-line illustrative snippets only when essential.
- **Treat the target as read-only.** Clone git URLs shallow into `.vamp-cache/`;
  scan local paths in place without modifying them.
- **Output goes to `vamped/<project-name>/`** using the layouts in `templates/`.
- **Respect the target's license** and record it in the output.
- Close with a confidence score, assumptions, and a self-critique pass.

> Designed to be used as the workspace root (or its own repo). It currently
> lives inside `forge-framework/` — lift the `vamp/` folder out whenever you
> want it standalone.
