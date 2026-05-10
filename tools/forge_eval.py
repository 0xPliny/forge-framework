#!/usr/bin/env python3
"""forge_eval.py — Score a single FORGE session against protocol gates.

Usage:
    python forge_eval.py --last
    python forge_eval.py --task-id <uuid>
    python forge_eval.py --task-id <uuid> --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GATES_BASE = [
    "classification",
    "confidence_protocol",
    "assumption_tracking",
    "meta_prompting",
    "phase_0_retrieval",
]

VERIFICATION_BY_COMPLEXITY = {
    "Simple": ["verification_layer_1", "verification_layer_2"],
    "Medium": ["verification_layer_1", "verification_layer_2", "verification_layer_3"],
    "Complex": [
        "verification_layer_1",
        "verification_layer_2",
        "verification_layer_3",
        "verification_layer_4",
    ],
    "Expert": [
        "verification_layer_1",
        "verification_layer_2",
        "verification_layer_3",
        "verification_layer_4",
        "verification_layer_5",
    ],
}

OUTCOME_MODIFIER = {
    "success": 1.0,
    "partial": 0.85,
    "escalated": 0.70,
    "failed": 0.50,
}


def expected_gates(complexity: str) -> set:
    verification = VERIFICATION_BY_COMPLEXITY.get(
        complexity, VERIFICATION_BY_COMPLEXITY["Medium"]
    )
    return set(GATES_BASE) | set(verification)


def score_session(session: dict) -> dict:
    complexity = session["classification"]["complexity"]
    expected = expected_gates(complexity)
    passed = set(session.get("gates_passed", [])) & expected
    missing = expected - passed

    gate_score = 100.0 * len(passed) / len(expected) if expected else 0.0
    outcome = session.get("outcome", "success")
    outcome_mod = OUTCOME_MODIFIER.get(outcome, 1.0)
    final_score = round(gate_score * outcome_mod, 1)

    return {
        "task_id": session["task_id"],
        "workflow": session["workflow"],
        "complexity": complexity,
        "category": session["classification"]["category"],
        "domain": session["classification"]["domain"],
        "outcome": outcome,
        "expected_gates": sorted(expected),
        "passed_gates": sorted(passed),
        "missing_gates": sorted(missing),
        "gate_score": round(gate_score, 1),
        "outcome_modifier": outcome_mod,
        "final_score": final_score,
    }


def load_sessions(file: Path) -> list:
    if not file.exists():
        print(f"Error: {file} does not exist", file=sys.stderr)
        sys.exit(1)
    sessions = []
    with file.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                sessions.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Warning: skipping malformed line {n}: {e}", file=sys.stderr)
    return sessions


def find_session(sessions: list, task_id: str = None, last: bool = False) -> dict:
    if not sessions:
        print("Error: no sessions found", file=sys.stderr)
        sys.exit(1)
    if last:
        return sessions[-1]
    if task_id:
        for s in sessions:
            if s["task_id"] == task_id or s["task_id"].startswith(task_id):
                return s
        print(f"Error: task_id {task_id} not found", file=sys.stderr)
        sys.exit(1)
    print("Error: must provide --task-id or --last", file=sys.stderr)
    sys.exit(1)


def render_md(result: dict) -> str:
    lines = [
        f"# FORGE Session Eval — `{result['task_id'][:8]}`",
        "",
        f"- **Workflow:** `/{result['workflow']}`",
        f"- **Category:** {result['category']}",
        f"- **Complexity:** {result['complexity']}",
        f"- **Domain:** {result['domain']}",
        f"- **Outcome:** {result['outcome']}",
        "",
        f"## Score: **{result['final_score']}/100**",
        "",
        f"Gate score: {result['gate_score']} × outcome modifier: {result['outcome_modifier']}",
        "",
        "## Gates Passed",
        "",
    ]
    for g in result["passed_gates"]:
        lines.append(f"- [x] {g}")
    if result["missing_gates"]:
        lines.append("")
        lines.append("## Gates Missing")
        lines.append("")
        for g in result["missing_gates"]:
            lines.append(f"- [ ] {g}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Score a FORGE session against protocol gates."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "telemetry" / "sessions.jsonl",
        help="Path to sessions.jsonl (default: ../telemetry/sessions.jsonl)",
    )
    parser.add_argument("--task-id", help="UUID of the session to score (prefix-match OK)")
    parser.add_argument("--last", action="store_true", help="Score the most recent session")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    if not args.task_id and not args.last:
        parser.error("Provide --task-id <uuid> or --last")

    sessions = load_sessions(args.file)
    session = find_session(sessions, task_id=args.task_id, last=args.last)
    result = score_session(session)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_md(result))


if __name__ == "__main__":
    main()
