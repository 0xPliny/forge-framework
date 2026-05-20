# 🧛 Vamp

> Siphon the **scaffolding, architecture, and understanding** of any project
> into a clean folder of Markdown — so it's yours to build on. You vamp the
> *essence*, never the source code.

Vamp is not a program you install. It's an **AI workspace**: open this folder in
**Claude Code** or **Cursor**, point it at a repo, and the assistant does the
vamping by following the [Vamp Protocol](VAMP_PROTOCOL.md). No SDK, no API key,
no token bill of its own — the assistant *is* the engine.

---

## How to use it

### Claude Code
1. Open this `vamp/` folder as your workspace (`claude` from inside it).
2. Run the slash command:
   ```
   /vamp https://github.com/some/cool-project
   ```
   …or just type: `vamp https://github.com/some/cool-project`
3. Find your results in `vamped/cool-project/`.

### Cursor
1. Open this folder in Cursor — `.cursorrules` loads automatically.
2. In chat: `vamp https://github.com/some/cool-project`
3. Results land in `vamped/cool-project/`.

A target can be a **git URL** *or* a **local path** (`vamp ../my-other-project`).

---

## What you get

```
vamped/<project>/
├── architecture.md   # high-level design, layers, decisions worth stealing
├── data-flow.md      # how data/control moves (with a Mermaid diagram)
├── dependencies.md   # external deps and why each one is there
├── setup.md          # install / configure / run from scratch
├── components/        # one file per major module
└── skeleton/          # empty folder mirror — start building immediately
```

## Modes

| Command | Result |
|---|---|
| `vamp <target>` | Full vamp (everything above) |
| `vamp <target> --skeleton-only` | Just the empty `skeleton/` mirror |
| `vamp <target> --graph` | Just a Mermaid dependency/data-flow diagram |
| `vamp <a> <b> --synthesize` | Merge several repos into one hybrid architecture |
| `vamp <old> <new> --diff` | What changed architecturally between two versions |

---

## The one rule

**Vamp extracts understanding, not code.** It paraphrases architecture, patterns,
and data flow in plain English; it never copies source verbatim. It always
records the target's license. This is the same footing as any "how this project
works" write-up — respect licenses and you're golden.

---

## Why it's a FORGE thing

Under the hood, the Vamp Protocol is FORGE's **HARVEST** workflow (extract →
analyze → restructure → synthesize) with a sharper name and a fixed output shape.
It honors the same house rules: honest confidence scores, tracked assumptions,
and a self-critique pass before it calls a vamp done.

> Built to be lifted out: copy the `vamp/` folder anywhere — or make it its own
> repo — and it works the same.
