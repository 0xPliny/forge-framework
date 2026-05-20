# The Vamp Protocol

> **What this is.** The complete operating instructions for *vamping* a project.
> Any AI assistant (Claude Code, Cursor, or otherwise) that has this workspace
> loaded executes this protocol on demand. There is no separate program — **the
> assistant is the engine.**

**Vamp** siphons the *scaffolding, architecture, and understanding* of a target
project and emits a clean folder of Markdown that explains how it works — so you
can fork the *ideas* and build on top of them. You vamp the **essence**, never
the source code.

---

## The Cardinal Rule

> **Extract structure and understanding. Never copy source code verbatim.**

- Describe responsibilities, patterns, signatures, and data flow **in your own words.**
- Function/class/endpoint **signatures** are fine. Implementation bodies are not.
- If a snippet is genuinely necessary to explain a pattern, keep it **under ~8 lines**, label it as illustrative, and prefer pseudocode.
- This keeps a vamp on the right side of fair use — the same footing as any
  "how this project works" write-up. Always respect the target's `LICENSE`;
  record it in the output.

---

## Trigger

The protocol fires when the user says any of:

- `vamp <target>` — full vamp (default)
- `vamp <target> --skeleton-only` — emit only the empty folder mirror
- `vamp <target> --graph` — emit only the dependency/data-flow Mermaid diagram
- `vamp <a> <b> [...] --synthesize` — multi-repo synthesis into one hybrid architecture doc
- `vamp <old-ref> <new-ref> --diff` — architectural diff between two versions of one repo
- `/vamp <target>` — the Claude Code slash command (same as above)

`<target>` is a **git URL** or a **local path**.

---

## Phase 0 — Acquire (read-only, always)

1. **Git URL** → shallow clone into the workspace cache:
   `git clone --depth=1 <url> .vamp-cache/<project-name>`
   (For `--diff`, clone the two refs into `.vamp-cache/<name>@<ref>` each.)
2. **Local path** → scan **in place, read-only**. Never write to, move, or
   modify anything inside the target. Treat it as immutable.
3. Confirm the target acquired cleanly before continuing. If the clone fails
   (network, auth, bad URL), stop and report — do not fabricate structure.

`.vamp-cache/` is git-ignored; clean it up when the vamp finishes.

---

## Phase 1 — Survey

Walk the tree and build a structural map. **Ignore** noise directories and
generated artifacts:

```
.git  .hg  .svn  node_modules  bower_components  vendor  .venv  venv  env
__pycache__  .pytest_cache  .mypy_cache  .ruff_cache  dist  build  out
target  bin  obj  .next  .nuxt  .svelte-kit  .turbo  coverage  .gradle
.idea  .vscode  .DS_Store  *.lock-cache  *.min.*  *.map
```

Then:

- **Map** the directory tree (depth-limited; collapse large leaf dirs with counts).
- **Detect languages** by extension and file counts.
- **Detect stack** from manifests and signal files:
  `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `Cargo.toml`,
  `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `*.csproj`,
  `Dockerfile`, `docker-compose.yml`, `Makefile`, `.github/workflows/*`,
  `next.config.*`, `vite.config.*`, `tsconfig.json`, `tauri.conf.json`, etc.
- **Identify entry points** (`main`, `index`, `app`, `cli`, `server`, `__main__`).

---

## Phase 2 — Distill

Read the key files **for understanding only**. Determine:

- **High-level architecture** — what layers/services exist and how they relate.
- **Module responsibilities** — what each major directory/package owns.
- **Data flow** — how a request / command / event travels through the system.
- **Configuration patterns** — env vars, config files, secrets handling, defaults.
- **Extension points** — where a new developer would plug in features.
- **External dependencies** — what they are and *why* they're there (not just a list).

Apply the **Confidence Protocol** as you go: when you infer something you can't
directly confirm from a file, say so. Don't present inference as fact.

---

## Phase 3 — Emit

Create `vamped/<project-name>/` in the workspace. Fill the templates in
`templates/` (do not just copy them empty):

```
vamped/<project-name>/
├── architecture.md      # high-level design, layers, key decisions
├── data-flow.md         # how data/control moves through the system (+ Mermaid)
├── dependencies.md      # external deps and the role each plays
├── setup.md             # how to install, configure, and run from scratch
├── components/          # one Markdown file per major module/directory
│   ├── <module-a>.md
│   └── <module-b>.md
└── skeleton/            # empty mirror of the structure, ready to build into
    ├── <dir>/.keep
    └── <dir>/README.md  # one-line stub: what goes here
```

**Mode overrides:**
- `--skeleton-only` → emit just `skeleton/`.
- `--graph` → emit just a Mermaid diagram (`vamped/<name>/graph.md`).
- `--synthesize` → emit a single merged `architecture.md` plus a
  `comparison.md` table of how each source handles each concern.
- `--diff` → emit `architecture-diff.md`: what changed structurally between refs.

The `skeleton/` mirror reproduces the **folder layout only** — empty dirs with
`.keep` files and one-line README stubs. No source, no copied config.

---

## Phase 4 — Report

Close every vamp with:

1. **Summary** — what was vamped, the detected stack, and the standout
   architectural ideas worth stealing.
2. **Confidence** — `CONFIDENCE: [1-10] | REASONING: [why]` on the overall vamp,
   and flag any section that's inference rather than confirmed.
3. **Assumptions** — list any with `ASSUMPTION: … | RISK: [H/M/L] | IF WRONG: …`.
4. **License note** — the target's license and the reminder that you extracted
   understanding, not code.
5. **Cleanup** — remove `.vamp-cache/` clones.

---

## FORGE alignment

This protocol *is* a HARVEST workflow (Extract → Analyze → Restructure → Verify →
Synthesize) wearing a cool name. When this workspace lives inside the FORGE repo,
honor FORGE's house rules: confidence scoring, assumption tracking, and a quick
self-critique pass before declaring a vamp done — *"what did I infer that I
couldn't confirm, and did I copy anything I shouldn't have?"*
