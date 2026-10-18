#!/usr/bin/env python3
"""forge_learn.py — The FORGE learnings store (OMEGA Plan 1), stdlib only.

Implements the contract in core/omega_retrieval.md over learnings/_index.jsonl:

    search    Phase 0 retrieval: score, cut off at 3, top 3 by (score, date)
    add       append one validated entry (fills id, date, normalized signature)
    promote   draft an entry from a telemetry session (source: telemetry-derived)
    correct   record a classification correction (classification learning)
    hints     classification hints from past corrections for a set of keywords
    validate  check every entry against learnings/schema.json

Usage:
    python forge_learn.py search --category REPAIR --domain web_development \\
        --keywords race-condition,event-ordering
    python forge_learn.py add --file entry.json
    python forge_learn.py promote --task-id 1a2b > draft.json   # edit, then add
    python forge_learn.py correct --from CREATION --to TRANSFORMATION \\
        --keywords refactor,existing,module --domain web_development \\
        --reason "Refactoring existing code, not building new"
    python forge_learn.py hints --keywords refactor,existing
    python forge_learn.py validate
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_schema import load_schema, validate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORE = ROOT / "learnings" / "_index.jsonl"
DEFAULT_SCHEMA = ROOT / "learnings" / "schema.json"
DEFAULT_TELEMETRY = ROOT / "telemetry" / "sessions.jsonl"

MIN_SCORE = 3
TOP_N = 3
#: Corrections that agree on a category before it counts as a strong signal
#: (workflows/classification_learning.md, "Strong Signal Promotion").
STRONG_SIGNAL = 3
CORRECTION_TAG = "classification-correction"
CATEGORIES = ("CREATION", "TRANSFORMATION", "UNDERSTANDING", "REPAIR", "OPTIMIZATION")
#: Draft text that must be replaced before `add` accepts an entry.
PLACEHOLDER = "FILL IN"
NO_STORE = "No learnings store yet — proceeding without prior context."
NO_MATCH = "No matching prior learnings."


class LearnError(ValueError):
    """Invalid input; the store was not changed."""


# ----------------------------------------------------------------- helpers


def keyword(text: str) -> str:
    """Normalize to the schema's keyword pattern ^[a-z0-9_-]+$."""
    return re.sub(r"[^a-z0-9_-]+", "-", text.strip().lower()).strip("-")


def parse_keywords(raw) -> list:
    if raw is None:
        return []
    items = raw if isinstance(raw, list) else str(raw).split(",")
    seen = []
    for item in items:
        word = keyword(item)
        if word and word not in seen:
            seen.append(word)
    return seen


def normalized(category: str, domain: str, keywords: list) -> str:
    return "|".join([category, domain] + sorted(keywords))


def load_store(store: Path) -> list:
    """Entries in file order; malformed lines are skipped with a warning."""
    if not store.exists():
        return []
    entries = []
    with store.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"Warning: skipping malformed line {number}: {exc}", file=sys.stderr)
                continue
            if isinstance(entry, dict):
                entries.append(entry)
    return entries


def _contains_placeholder(value) -> bool:
    if isinstance(value, str):
        return PLACEHOLDER in value
    if isinstance(value, dict):
        return any(_contains_placeholder(v) for v in value.values())
    if isinstance(value, list):
        return any(_contains_placeholder(v) for v in value)
    return False


def complete(entry: dict) -> dict:
    """Fill the mechanical fields the contract says the writer generates."""
    entry = dict(entry)
    entry.setdefault("schema_version", "1.0")
    entry.setdefault("learning_id", str(uuid.uuid4()))
    entry.setdefault("date", date.today().isoformat())
    signature = dict(entry.get("problem_signature") or {})
    signature["keywords"] = parse_keywords(signature.get("keywords"))
    if entry.get("category") and entry.get("domain"):
        signature["normalized"] = normalized(entry["category"], entry["domain"], signature["keywords"])
    entry["problem_signature"] = signature
    return entry


def append(entry: dict, store: Path, schema: dict) -> dict:
    if _contains_placeholder(entry) or "fill-in" in json.dumps(entry.get("problem_signature")):
        raise LearnError(f"entry still contains '{PLACEHOLDER}' placeholders; edit the draft first")
    entry = complete(entry)
    errors = validate(entry, schema)
    if errors:
        raise LearnError("entry does not match learnings/schema.json:\n  " + "\n  ".join(errors))
    existing = {e.get("learning_id") for e in load_store(store)}
    if entry["learning_id"] in existing:
        raise LearnError(f"learning_id {entry['learning_id']} already exists; append, don't mutate")
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
    return entry


# ----------------------------------------------------------------- retrieval


def score(entry: dict, category: str, domain: str, keywords: list) -> int:
    """score(entry) per core/omega_retrieval.md Step 2."""
    signature = entry.get("problem_signature") or {}
    entry_keywords = set(signature.get("keywords") or [])
    return (
        (2 if category and entry.get("category") == category else 0)
        + (2 if domain and entry.get("domain") == domain else 0)
        + len(entry_keywords & set(keywords))
    )


def search(entries: list, category: str, domain: str, keywords: list,
           top: int = TOP_N, min_score: int = MIN_SCORE) -> list:
    scored = [(score(e, category, domain, keywords), e) for e in entries]
    scored = [(s, e) for s, e in scored if s >= min_score]
    # Sort by score desc, then date desc (ISO dates sort lexically).
    scored.sort(key=lambda pair: (pair[0], pair[1].get("date", "")), reverse=True)
    return [dict(e, _score=s) for s, e in scored[:top]]


def _clip(text, limit: int = 120) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_matches(matches: list) -> str:
    lines = [f"> **Prior learnings (top {len(matches)}):**"]
    for n, entry in enumerate(matches, 1):
        lines.append(
            f"> {n}. **{entry.get('date', '?')}** [{entry.get('category')}/{entry.get('domain')}, "
            f"conf {entry.get('confidence')}/10, score {entry['_score']}] — {_clip(entry.get('generalization'), 160)}"
        )
        lines.append(f">    - What worked: {_clip(entry.get('what_worked'))}")
        lines.append(f">    - What failed: {_clip(entry.get('what_failed'))}")
    return "\n".join(lines)


# ----------------------------------------------------------------- promote


def load_session(telemetry: Path, task_id: str) -> dict:
    if not telemetry.exists():
        raise LearnError(f"{telemetry} does not exist")
    sessions = []
    with telemetry.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                try:
                    sessions.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    if task_id == "last":
        if not sessions:
            raise LearnError("no sessions recorded")
        return sessions[-1]
    matches = [s for s in sessions if str(s.get("task_id", "")).startswith(task_id)]
    if not matches:
        raise LearnError(f"task_id {task_id} not found in {telemetry}")
    if len(matches) > 1:
        raise LearnError(f"task_id prefix {task_id} is ambiguous ({len(matches)} sessions)")
    return matches[0]


def draft_from_session(session: dict) -> dict:
    classification = session.get("classification") or {}
    notes = session.get("notes") or ""
    keywords = parse_keywords(re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", notes)[:6]) or []
    return {
        "schema_version": "1.0",
        "learning_id": str(uuid.uuid4()),
        "date": date.today().isoformat(),
        "source_task_id": session.get("task_id"),
        "workflow": session.get("workflow"),
        "category": classification.get("category"),
        "domain": classification.get("domain"),
        "complexity": classification.get("complexity"),
        "problem_signature": {
            "keywords": keywords if len(keywords) >= 2 else ["fill-in-keyword-1", "fill-in-keyword-2"],
            "normalized": "",
        },
        "what_worked": f"{PLACEHOLDER}: concrete approach that produced the outcome. Session notes: {notes}".strip(),
        "what_failed": f"{PLACEHOLDER}: what was tried and discarded (outcome was {session.get('outcome')}, "
                       f"{session.get('iterations', 1)} iteration(s), gates failed: {session.get('gates_failed') or 'none'})",
        "generalization": f"{PLACEHOLDER}: the conditions under which this applies",
        "confidence": min(int(classification.get("confidence") or 5), 8),
        "source": "telemetry-derived",
        "tags": [],
    }


# ----------------------------------------------------------------- classification learning


def correction_entry(original: str, corrected: str, keywords: list, domain: str,
                     reason: str, confidence: int = 7) -> dict:
    if original not in CATEGORIES or corrected not in CATEGORIES:
        raise LearnError(f"categories must be one of {', '.join(CATEGORIES)}")
    if original == corrected:
        raise LearnError("--from and --to are the same category")
    if len(keywords) < 2:
        raise LearnError("give at least 2 --keywords (the signal words that misled the classifier)")
    return {
        "workflow": "cross-cutting",
        "category": corrected,
        "domain": domain,
        "complexity": None,
        "problem_signature": {"keywords": keywords},
        "what_worked": f"Classify as {corrected}. {reason}".strip(),
        "what_failed": f"Classified as {original} from the signal words: {', '.join(keywords)}.",
        "generalization": f"When a task's signal words include {', '.join(keywords)}"
                          f"{' in ' + domain if domain != 'general' else ''}, prefer {corrected} over {original} "
                          "unless the task clearly creates something new from nothing.",
        "applies_to": [f"{corrected}:{domain}"],
        "confidence": confidence,
        "source": "manual",
        "tags": [CORRECTION_TAG, f"from:{original}", f"to:{corrected}"],
    }


def hints(entries: list, keywords: list, domain: str | None = None) -> dict:
    """Aggregate past corrections whose keywords overlap the task's keywords."""
    votes = Counter()
    evidence = []
    for entry in entries:
        tags = entry.get("tags") or []
        if CORRECTION_TAG not in tags:
            continue
        if domain and entry.get("domain") not in (domain, "general"):
            continue
        overlap = set((entry.get("problem_signature") or {}).get("keywords") or []) & set(keywords)
        if not overlap:
            continue
        from_tag = next((t[5:] for t in tags if t.startswith("from:")), None)
        votes[entry.get("category")] += 1
        evidence.append({"date": entry.get("date"), "from": from_tag, "to": entry.get("category"),
                         "matched": sorted(overlap), "learning_id": entry.get("learning_id")})
    suggestion = None
    if votes:
        category, count = votes.most_common(1)[0]
        suggestion = {"category": category, "corrections": count,
                      "strength": "strong" if count >= STRONG_SIGNAL else "weak"}
    return {"suggestion": suggestion, "votes": dict(votes), "evidence": evidence}


# ----------------------------------------------------------------- CLI


def _store_args(parser):
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE, help="path to _index.jsonl")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="path to learnings schema.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FORGE learnings store (OMEGA Plan 1).")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("search", help="Phase 0 retrieval")
    _store_args(p)
    p.add_argument("--category", default="", help="task category, e.g. CREATION")
    p.add_argument("--domain", default="", help="task domain, e.g. web_development")
    p.add_argument("--keywords", default="", help="comma-separated keywords")
    p.add_argument("--top", type=int, default=TOP_N)
    p.add_argument("--min-score", type=int, default=MIN_SCORE)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("add", help="append one entry")
    _store_args(p)
    p.add_argument("--file", default="-", help="entry JSON file, or - for stdin")

    p = sub.add_parser("promote", help="draft an entry from a telemetry session")
    p.add_argument("--task-id", required=True, help="task_id or prefix, or 'last'")
    p.add_argument("--telemetry", type=Path, default=DEFAULT_TELEMETRY)

    p = sub.add_parser("correct", help="record a classification correction")
    _store_args(p)
    p.add_argument("--from", dest="original", required=True, choices=CATEGORIES)
    p.add_argument("--to", dest="corrected", required=True, choices=CATEGORIES)
    p.add_argument("--keywords", required=True, help="comma-separated signal words")
    p.add_argument("--domain", default="general")
    p.add_argument("--reason", default="", help="the user's explanation")
    p.add_argument("--task-id", default=None, help="telemetry task_id of the misclassified session")

    p = sub.add_parser("hints", help="classification hints from past corrections")
    _store_args(p)
    p.add_argument("--keywords", required=True)
    p.add_argument("--domain", default=None)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("validate", help="validate every entry")
    _store_args(p)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "search":
            entries = load_store(args.store)
            if not entries:
                print(json.dumps([]) if args.json else NO_STORE)
                return 0
            matches = search(entries, args.category, args.domain, parse_keywords(args.keywords),
                             args.top, args.min_score)
            if args.json:
                print(json.dumps(matches, indent=2, ensure_ascii=False))
            else:
                print(render_matches(matches) if matches else NO_MATCH)
            return 0

        if args.command == "add":
            raw = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
            entry = json.loads(raw)
            if not isinstance(entry, dict):
                raise LearnError("expected one JSON object")
            saved = append(entry, args.store, load_schema(args.schema))
            print(f"Appended learning {saved['learning_id']} to {args.store}")
            return 0

        if args.command == "promote":
            print(json.dumps(draft_from_session(load_session(args.telemetry, args.task_id)),
                             indent=2, ensure_ascii=False))
            print(f"Edit every '{PLACEHOLDER}' field, then: python tools/forge_learn.py add --file draft.json",
                  file=sys.stderr)
            return 0

        if args.command == "correct":
            entry = correction_entry(args.original, args.corrected, parse_keywords(args.keywords),
                                     args.domain, args.reason)
            entry["source_task_id"] = args.task_id
            saved = append(entry, args.store, load_schema(args.schema))
            print(f"Recorded correction {args.original} -> {args.corrected} as {saved['learning_id']}")
            return 0

        if args.command == "hints":
            result = hints(load_store(args.store), parse_keywords(args.keywords), args.domain)
            if args.json:
                print(json.dumps(result, indent=2))
            elif result["suggestion"]:
                s = result["suggestion"]
                print(f"Past corrections suggest {s['category']} ({s['corrections']} correction(s), "
                      f"{s['strength']} signal). Votes: {result['votes']}")
            else:
                print("No past classification corrections match these keywords.")
            return 0

        if args.command == "validate":
            schema = load_schema(args.schema)
            if not args.store.exists():
                print(f"{args.store} does not exist (nothing to validate)")
                return 0
            problems = 0
            ids = Counter()
            with args.store.open(encoding="utf-8") as stream:
                for number, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError as exc:
                        print(f"line {number}: invalid JSON: {exc}")
                        problems += 1
                        continue
                    for error in validate(entry, schema):
                        print(f"line {number}: {error}")
                        problems += 1
                    ids[entry.get("learning_id")] += 1
            for learning_id, count in ids.items():
                if count > 1:
                    print(f"duplicate learning_id {learning_id} ({count} entries)")
                    problems += 1
            print("OK" if not problems else f"{problems} problem(s)")
            return 1 if problems else 0
    except (LearnError, OSError, json.JSONDecodeError) as exc:
        print(f"forge_learn: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
