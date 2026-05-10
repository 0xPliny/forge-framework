#!/usr/bin/env python3
"""forge_report.py — Aggregate FORGE telemetry into a report.

Usage:
    python forge_report.py                  # last 30 days, Markdown
    python forge_report.py --days 7
    python forge_report.py --days 90 --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_eval import score_session  # noqa: E402


def load_sessions(file: Path, days: int) -> list:
    if not file.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    sessions = []
    with file.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                s = json.loads(line)
                ts = datetime.fromisoformat(s["timestamp"].replace("Z", "+00:00"))
                if ts >= cutoff:
                    sessions.append(s)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: skipping malformed line {n}: {e}", file=sys.stderr)
    return sessions


def render_md(sessions: list, days: int) -> str:
    if not sessions:
        return (
            f"# FORGE Report — Last {days} Days\n\n"
            f"No sessions found in the window.\n"
        )

    workflows = Counter(s["workflow"] for s in sessions)
    outcomes = Counter(s["outcome"] for s in sessions)
    domains = Counter(s["classification"]["domain"] for s in sessions)
    categories = Counter(s["classification"]["category"] for s in sessions)
    complexities = Counter(s["classification"]["complexity"] for s in sessions)
    confidences = [s["classification"]["confidence"] for s in sessions]
    scores = [score_session(s)["final_score"] for s in sessions]

    iterations = [
        (s["task_id"], s["iterations"], s["workflow"])
        for s in sessions
        if s.get("iterations", 1) > 1
    ]
    iterations.sort(key=lambda x: -x[1])

    failed = [
        s for s in sessions if s.get("outcome") in ("failed", "partial", "escalated")
    ]

    total = len(sessions)
    success_rate = 100.0 * outcomes.get("success", 0) / total

    lines = [
        f"# FORGE Report — Last {days} Days",
        "",
        f"- **Total sessions:** {total}",
        f"- **Success rate:** {success_rate:.0f}%",
        f"- **Avg classification confidence:** {mean(confidences):.1f}/10",
        f"- **Avg gate score:** {mean(scores):.1f}/100",
        "",
        "## Workflow Distribution",
        "",
        "| Workflow | Count | % |",
        "|---|---:|---:|",
    ]
    for wf, n in workflows.most_common():
        lines.append(f"| `/{wf}` | {n} | {100*n/total:.0f}% |")

    lines += ["", "## Category Distribution", "", "| Category | Count |", "|---|---:|"]
    for cat, n in categories.most_common():
        lines.append(f"| {cat} | {n} |")

    lines += [
        "",
        "## Complexity Distribution",
        "",
        "| Complexity | Count |",
        "|---|---:|",
    ]
    for cmplx, n in complexities.most_common():
        lines.append(f"| {cmplx} | {n} |")

    lines += ["", "## Outcome Distribution", "", "| Outcome | Count | % |", "|---|---:|---:|"]
    for out, n in outcomes.most_common():
        lines.append(f"| {out} | {n} | {100*n/total:.0f}% |")

    lines += ["", "## Domain Distribution", "", "| Domain | Count |", "|---|---:|"]
    for dom, n in domains.most_common():
        lines.append(f"| {dom} | {n} |")

    if iterations:
        lines += [
            "",
            "## High-Iteration Tasks (learnings-store candidates)",
            "",
            "| Task ID | Workflow | Iterations |",
            "|---|---|---:|",
        ]
        for tid, n, wf in iterations[:5]:
            lines.append(f"| `{tid[:8]}` | `/{wf}` | {n} |")

    if failed:
        lines += [
            "",
            "## Non-Success Sessions (learnings-store candidates)",
            "",
            "| Task ID | Workflow | Outcome | Notes |",
            "|---|---|---|---|",
        ]
        for s in failed[:10]:
            note = (s.get("notes") or "").replace("|", "\\|")[:60]
            lines.append(
                f"| `{s['task_id'][:8]}` | `/{s['workflow']}` | {s['outcome']} | {note} |"
            )

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate FORGE telemetry into a report."
    )
    parser.add_argument(
        "--days", type=int, default=30, help="Window in days (default: 30)"
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "telemetry" / "sessions.jsonl",
        help="Path to sessions.jsonl (default: ../telemetry/sessions.jsonl)",
    )
    parser.add_argument("--format", choices=["md", "json"], default="md")
    args = parser.parse_args()

    sessions = load_sessions(args.file, args.days)

    if args.format == "json":
        print(json.dumps(sessions, indent=2))
    else:
        print(render_md(sessions, args.days))


if __name__ == "__main__":
    main()
