#!/usr/bin/env python3
"""forge_session.py — Measure a FORGE session instead of self-reporting it.

Telemetry schema v1.1: the AI no longer estimates wall time or code churn.

    start   record start time, git HEAD and the working-tree baseline
            in .forge-session.json (gitignored) in the project folder
    stop    print the measured fields: started_at, wall_time_sec, git_stats
    emit    read the AI's telemetry JSON (stdin or --file), add the measured
            fields, validate against telemetry/schema.json, append one line
            to telemetry/sessions.jsonl, and clear the session state

Usage:
    python tools/forge_session.py start
    python tools/forge_session.py stop
    echo '{...telemetry...}' | python tools/forge_session.py emit

Measured values replace self-reported ones and are listed in `measured`.
Respects FORGE_TELEMETRY_DISABLED=1 (emit writes nothing).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_schema import load_schema, validate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TELEMETRY = ROOT / "telemetry" / "sessions.jsonl"
DEFAULT_SCHEMA = ROOT / "telemetry" / "schema.json"
STATE_NAME = ".forge-session.json"
UNTRACKED_LINE_LIMIT = 5_000_000  # bytes per new file counted for lines_added


class SessionError(RuntimeError):
    """Nothing was written."""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.isoformat(timespec="seconds").replace("+00:00", "Z")


def _git(project: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(["git", "-C", str(project), *args], capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return completed.stdout if completed.returncode == 0 else None


def _untracked(project: Path) -> list:
    out = _git(project, "ls-files", "--others", "--exclude-standard", "-z")
    return [p for p in (out or "").split("\0") if p]


def _numstat(project: Path, commit: str) -> tuple:
    """(files, added, removed) between `commit` and the working tree; binary files count as files only."""
    out = _git(project, "diff", "--numstat", commit) or ""
    files = added = removed = 0
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        files += 1
        if parts[0].isdigit():
            added += int(parts[0])
        if parts[1].isdigit():
            removed += int(parts[1])
    return files, added, removed


def _count_lines(path: Path) -> int:
    try:
        if path.stat().st_size > UNTRACKED_LINE_LIMIT:
            return 0
        data = path.read_bytes()
    except OSError:
        return 0
    if b"\0" in data[:8192]:
        return 0  # binary
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def state_path(project: Path) -> Path:
    return Path(project) / STATE_NAME


def start(project: Path, task_id: str | None = None, force: bool = False) -> dict:
    path = state_path(project)
    if path.exists() and not force:
        raise SessionError(f"{path} exists: a session is already running (use --force to restart it)")
    head = (_git(project, "rev-parse", "HEAD") or "").strip() or None
    state = {
        "task_id": task_id or str(uuid.uuid4()),
        "started_at": _iso(_now()),
        "start_commit": head,
        "baseline_dirty": bool((_git(project, "status", "--porcelain") or "").strip()) if head else False,
        "untracked_at_start": _untracked(project) if head else [],
    }
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    if head and _git(project, "check-ignore", "-q", STATE_NAME) is None:
        print(f"note: {STATE_NAME} is not gitignored in this project; add it to .gitignore "
              "so session state is never committed", file=sys.stderr)
    return state


def load_state(project: Path) -> dict:
    path = state_path(project)
    if not path.exists():
        raise SessionError(f"no running session ({path} not found); run `forge_session.py start` first")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise SessionError(f"{path} is corrupt: {exc}") from exc


def measure(project: Path, state: dict, now: datetime | None = None) -> dict:
    now = now or _now()
    started = datetime.fromisoformat(state["started_at"].replace("Z", "+00:00"))
    result = {
        "task_id": state["task_id"],
        "started_at": state["started_at"],
        "timestamp": _iso(now),
        "wall_time_sec": round(max((now - started).total_seconds(), 0.0), 1),
        "git_stats": None,
        "measured": ["started_at", "wall_time_sec", "timestamp"],
    }
    commit = state.get("start_commit")
    if commit:
        files, added, removed = _numstat(project, commit)
        before = set(state.get("untracked_at_start") or [])
        new_files = [p for p in _untracked(project) if p not in before and Path(p).name != STATE_NAME]
        result["git_stats"] = {
            "files_changed": files + len(new_files),
            "lines_added": added + sum(_count_lines(Path(project) / p) for p in new_files),
            "lines_removed": removed,
            "new_untracked_files": len(new_files),
            "baseline_dirty": bool(state.get("baseline_dirty")),
            "start_commit": commit,
        }
        result["measured"].append("git_stats")
    return result


def emit(project: Path, record: dict, telemetry: Path, schema_path: Path) -> dict:
    state = load_state(project)
    measured = measure(project, state)
    record = dict(record)
    record["schema_version"] = "1.1"
    record.setdefault("task_id", measured["task_id"])
    for key in ("started_at", "timestamp", "wall_time_sec", "git_stats", "measured"):
        record[key] = measured[key]
    errors = validate(record, load_schema(schema_path))
    if errors:
        raise SessionError("telemetry does not match telemetry/schema.json:\n  " + "\n  ".join(errors))
    telemetry.parent.mkdir(parents=True, exist_ok=True)
    with telemetry.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    state_path(project).unlink()
    return record


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Measure FORGE sessions (telemetry v1.1).")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="project folder (default: cwd)")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start")
    p.add_argument("--task-id", default=None)
    p.add_argument("--force", action="store_true", help="replace a running session's state")
    sub.add_parser("stop", help="print measured fields (session keeps running)")
    p = sub.add_parser("emit")
    p.add_argument("--file", default="-", help="telemetry JSON file, or - for stdin")
    p.add_argument("--telemetry", type=Path, default=DEFAULT_TELEMETRY)
    p.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    sub.add_parser("abort", help="discard the running session without emitting")
    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            state = start(args.project, args.task_id, args.force)
            print(json.dumps({"task_id": state["task_id"], "started_at": state["started_at"],
                              "start_commit": state["start_commit"]}))
        elif args.command == "stop":
            print(json.dumps(measure(args.project, load_state(args.project)), indent=2))
        elif args.command == "abort":
            load_state(args.project)
            state_path(args.project).unlink()
            print("Session discarded.")
        elif args.command == "emit":
            if os.environ.get("FORGE_TELEMETRY_DISABLED") == "1":
                state_path(args.project).unlink(missing_ok=True)
                print("FORGE_TELEMETRY_DISABLED=1: nothing written.")
                return 0
            raw = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
            record = json.loads(raw)
            if not isinstance(record, dict):
                raise SessionError("expected one JSON object")
            saved = emit(args.project, record, args.telemetry, args.schema)
            print(f"Appended session {saved['task_id']} to {args.telemetry} "
                  f"(measured: {', '.join(saved['measured'])})")
    except (SessionError, OSError, json.JSONDecodeError) as exc:
        print(f"forge_session: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
