---
description: Vamp a project — siphon its architecture & scaffolding into an explanatory Markdown folder (never copies source)
argument-hint: <git-url-or-local-path> [--skeleton-only | --graph | --synthesize | --diff]
---

Execute the **Vamp Protocol**. Read `VAMP_PROTOCOL.md` in this workspace in full,
then follow every phase exactly: Acquire (read-only) → Survey → Distill → Emit →
Report.

Hard rules (full detail in `VAMP_PROTOCOL.md`):
- **Never copy source code verbatim** — extract structure and understanding, paraphrase in your own words; signatures and <8-line illustrative snippets only when essential.
- **Target is read-only** — shallow-clone git URLs into `.vamp-cache/`; never modify a local target.
- **Output to `vamped/<project-name>/`** using the layouts in `templates/`.
- **Respect the license**, record it, and close with confidence + assumptions + a self-critique pass.

If `$ARGUMENTS` is empty, ask for the git URL or local path before doing anything.

## Target

$ARGUMENTS
