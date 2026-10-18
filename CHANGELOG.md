# Changelog

## v1.2 — 2026-10-18

Finishes the parts of FORGE that were specified but not built.

### Added

- **Learnings store tooling (OMEGA "Plan 1")** — `tools/forge_learn.py`:
  `search` (Phase 0 retrieval per `core/omega_retrieval.md`), `add`
  (validated append), `promote` (draft from a telemetry session),
  `validate`.
- **Classification learning** — `forge_learn.py correct` records a user's
  correction as a tagged learning; `hints` aggregates past corrections, with
  strong-signal promotion at 3+. The `forge-classifier` skill uses both.
- **Measured telemetry (schema v1.1)** — `tools/forge_session.py` records
  start time and git baseline at Phase 0 and, at close, fills `started_at`,
  `timestamp`, `wall_time_sec` and `git_stats`, validates and appends. New
  optional fields: `started_at`, `git_stats`, `measured`. v1.0 lines stay valid.
- `tools/forge_schema.py` — stdlib JSON Schema subset validator used by the tools.
- `tests/` — `unittest` suite for all tools, run in CI with a Markdown link check.
- `forge_report.py` reports measured wall time and churn, and how to promote
  learning candidates.
- `/harvest` can use the optional HARVEST engine (see `workflows/harvest.md`).

### Changed

- `/rise`, `/care`, `/harvest` (project and user-level copies) start the
  session clock and run retrieval with the tools at Phase 0, and emit
  telemetry and learnings through them at close.
- Domain modules: commented-out "future" tool specs are now
  `verification_commands` (or `verification_checks`) that the AI runs in
  Verification Layers 1-2; the module template matches.

### Removed

- `frameworks/` — byte-identical duplicates of five `workflows/` files.
  Links to it, and to the never-existing `universal_*.md` files, now point
  to `workflows/`.
