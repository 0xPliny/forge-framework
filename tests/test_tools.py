"""Tests for FORGE's stdlib tools. Run: python -m unittest discover tests"""

from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import forge_eval  # noqa: E402
import forge_learn  # noqa: E402
import forge_report  # noqa: E402
import forge_schema  # noqa: E402
import forge_session  # noqa: E402

TELEMETRY_SCHEMA = forge_schema.load_schema(ROOT / "telemetry" / "schema.json")
LEARNINGS_SCHEMA = forge_schema.load_schema(ROOT / "learnings" / "schema.json")


def session_record(**overrides) -> dict:
    record = {
        "schema_version": "1.0",
        "task_id": "11111111-2222-4333-8444-555555555555",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "classification": {"category": "REPAIR", "complexity": "Medium", "domain": "web_development",
                           "confidence": 8},
        "workflow": "care",
        "assumptions_count": 2,
        "iterations": 3,
        "gates_passed": ["classification", "confidence_protocol", "assumption_tracking", "meta_prompting",
                         "phase_0_retrieval", "verification_layer_1", "verification_layer_2"],
        "gates_failed": ["verification_layer_3"],
        "outcome": "partial",
        "prompt_hash": "0123456789abcdef",
        "notes": "Race condition in event ordering; retry backoff masked it",
    }
    record.update(overrides)
    return record


def learning(**overrides) -> dict:
    entry = {
        "workflow": "care",
        "category": "REPAIR",
        "domain": "web_development",
        "problem_signature": {"keywords": ["race-condition", "event-ordering", "retry"]},
        "what_worked": "Logged event sequence numbers before changing timing",
        "what_failed": "Adding sleeps hid the race instead of fixing it",
        "generalization": "Intermittent ordering bugs: instrument order first, then fix",
        "confidence": 7,
        "source": "manual",
    }
    entry.update(overrides)
    return entry


class TempDir(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class SchemaValidatorTests(unittest.TestCase):
    def test_v10_and_v11_records_validate(self):
        self.assertEqual(forge_schema.validate(session_record(), TELEMETRY_SCHEMA), [])
        v11 = session_record(schema_version="1.1", started_at="2026-10-18T10:00:00Z", wall_time_sec=12.5,
                             git_stats={"files_changed": 1, "lines_added": 2, "lines_removed": 0},
                             measured=["wall_time_sec", "git_stats"])
        self.assertEqual(forge_schema.validate(v11, TELEMETRY_SCHEMA), [])

    def test_errors_are_reported(self):
        bad = session_record(workflow="nope", extra=1, prompt_hash="XYZ")
        del bad["outcome"]
        errors = " ".join(forge_schema.validate(bad, TELEMETRY_SCHEMA))
        for fragment in ("'nope' not in", "unexpected field 'extra'", "missing required field 'outcome'",
                         "does not match"):
            self.assertIn(fragment, errors)

    def test_types_formats_and_bounds(self):
        schema = {"type": "object", "properties": {
            "n": {"type": "integer", "minimum": 1}, "d": {"type": "string", "format": "date"},
            "t": {"type": "string", "format": "date-time"}, "a": {"type": "array", "minItems": 2,
                                                               "items": {"type": "string"}}}}
        self.assertEqual(forge_schema.validate({"n": 1, "d": "2026-01-02", "t": "2026-01-02T03:04:05Z",
                                                "a": ["x", "y"]}, schema), [])
        errors = forge_schema.validate({"n": True, "d": "2026-13-40", "t": "2026-01-02", "a": ["x", 3]}, schema)
        self.assertEqual(len(errors), 4, errors)

    def test_agrees_with_jsonschema_when_installed(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed (CI installs it)")
        good = [session_record(), session_record(schema_version="1.1", measured=["git_stats"],
                                                 git_stats={"files_changed": 0, "lines_added": 0, "lines_removed": 0})]
        bad = [session_record(workflow="nope"), session_record(git_stats={"files_changed": -1, "lines_added": 0,
                                                                          "lines_removed": 0})]
        for record in good:
            jsonschema.validate(record, TELEMETRY_SCHEMA)
            self.assertEqual(forge_schema.validate(record, TELEMETRY_SCHEMA), [])
        for record in bad:
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(record, TELEMETRY_SCHEMA)
            self.assertNotEqual(forge_schema.validate(record, TELEMETRY_SCHEMA), [])

    def test_cli_on_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "s.jsonl"
            data.write_text(json.dumps(session_record()) + "\n\n" + "{broken\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()) as out:
                code = forge_schema.main([str(ROOT / "telemetry" / "schema.json"), str(data)])
            self.assertEqual(code, 1)
            self.assertIn("line 3: invalid JSON", out.getvalue())


class LearnStoreTests(TempDir):
    def setUp(self):
        super().setUp()
        self.store = self.tmp / "_index.jsonl"

    def add(self, **overrides):
        return forge_learn.append(learning(**overrides), self.store, LEARNINGS_SCHEMA)

    def test_add_fills_mechanical_fields_and_validates(self):
        saved = self.add(problem_signature={"keywords": ["Race Condition", "event_ordering", "race-condition"]})
        self.assertEqual(saved["problem_signature"]["keywords"], ["race-condition", "event_ordering"])
        self.assertEqual(saved["problem_signature"]["normalized"],
                         "REPAIR|web_development|event_ordering|race-condition")
        lines = self.store.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(forge_schema.validate(json.loads(lines[0]), LEARNINGS_SCHEMA), [])

    def test_add_rejects_invalid_duplicates_and_placeholders(self):
        with self.assertRaises(forge_learn.LearnError):
            self.add(confidence=11)
        saved = self.add()
        with self.assertRaises(forge_learn.LearnError):
            self.add(learning_id=saved["learning_id"])
        with self.assertRaises(forge_learn.LearnError):
            self.add(generalization="FILL IN: later")
        self.assertEqual(len(self.store.read_text().splitlines()), 1)

    def test_search_scoring_cutoff_and_order(self):
        self.add(date="2026-01-01")                                     # score 2+2+2 = 6
        self.add(date="2026-05-01")                                     # same score, newer
        self.add(domain="python_data", date="2026-06-01")               # 2+0+2 = 4
        self.add(category="CREATION", domain="python_data", date="2026-07-01",
                 problem_signature={"keywords": ["race-condition", "unrelated"]})  # 0+0+1 = 1 -> cut
        entries = forge_learn.load_store(self.store)
        matches = forge_learn.search(entries, "REPAIR", "web_development", ["race-condition", "event-ordering"])
        self.assertEqual([m["_score"] for m in matches], [6, 6, 4])
        self.assertEqual(matches[0]["date"], "2026-05-01")
        self.assertIn("Prior learnings (top 3)", forge_learn.render_matches(matches))

    def test_search_cli_messages(self):
        with redirect_stdout(io.StringIO()) as out:
            forge_learn.main(["search", "--store", str(self.store), "--category", "REPAIR"])
        self.assertIn(forge_learn.NO_STORE, out.getvalue())
        self.add()
        with redirect_stdout(io.StringIO()) as out:
            forge_learn.main(["search", "--store", str(self.store), "--category", "CREATION",
                              "--domain", "x", "--keywords", "nothing"])
        self.assertIn(forge_learn.NO_MATCH, out.getvalue())

    def test_promote_drafts_and_requires_editing(self):
        telemetry = self.tmp / "sessions.jsonl"
        telemetry.write_text(json.dumps(session_record()) + "\n", encoding="utf-8")
        draft = forge_learn.draft_from_session(forge_learn.load_session(telemetry, "1111"))
        self.assertEqual(draft["source"], "telemetry-derived")
        self.assertEqual(draft["source_task_id"], session_record()["task_id"])
        with self.assertRaises(forge_learn.LearnError):
            forge_learn.append(draft, self.store, LEARNINGS_SCHEMA)
        for key in ("what_worked", "what_failed", "generalization"):
            draft[key] = "edited"
        draft["problem_signature"] = {"keywords": ["race-condition", "retry"]}
        forge_learn.append(draft, self.store, LEARNINGS_SCHEMA)
        self.assertEqual(forge_learn.load_session(telemetry, "last")["workflow"], "care")
        with self.assertRaises(forge_learn.LearnError):
            forge_learn.load_session(telemetry, "ffff")

    def test_validate_cli(self):
        self.add()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(forge_learn.main(["validate", "--store", str(self.store)]), 0)
        with self.store.open("a") as stream:
            stream.write('{"schema_version": "1.0"}\n')
        with redirect_stdout(io.StringIO()):
            self.assertEqual(forge_learn.main(["validate", "--store", str(self.store)]), 1)


class ClassificationLearningTests(TempDir):
    def setUp(self):
        super().setUp()
        self.store = self.tmp / "_index.jsonl"

    def correct(self, keywords="refactor,existing,module", to="TRANSFORMATION", domain="web_development"):
        return forge_learn.main(["correct", "--store", str(self.store), "--from", "CREATION", "--to", to,
                                 "--keywords", keywords, "--domain", domain, "--reason", "existing code"])

    def test_corrections_are_valid_tagged_learnings(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.correct(), 0)
        entry = forge_learn.load_store(self.store)[0]
        self.assertEqual(forge_schema.validate(entry, LEARNINGS_SCHEMA), [])
        self.assertIn(forge_learn.CORRECTION_TAG, entry["tags"])
        self.assertIn("from:CREATION", entry["tags"])

    def test_weak_then_strong_signal(self):
        with redirect_stdout(io.StringIO()):
            self.correct()
        result = forge_learn.hints(forge_learn.load_store(self.store), ["refactor", "legacy"], "web_development")
        self.assertEqual(result["suggestion"], {"category": "TRANSFORMATION", "corrections": 1, "strength": "weak"})
        with redirect_stdout(io.StringIO()):
            self.correct("refactor,legacy")
            self.correct("refactor,port", domain="general")
        result = forge_learn.hints(forge_learn.load_store(self.store), ["refactor"], "web_development")
        self.assertEqual(result["suggestion"]["strength"], "strong")
        self.assertEqual(forge_learn.hints(forge_learn.load_store(self.store), ["refactor"], "python_data")
                         ["suggestion"]["corrections"], 1)  # only the 'general' one applies

    def test_bad_corrections_rejected(self):
        with self.assertRaises(forge_learn.LearnError):
            forge_learn.correction_entry("CREATION", "CREATION", ["a", "b"], "general", "")
        with self.assertRaises(forge_learn.LearnError):
            forge_learn.correction_entry("CREATION", "REPAIR", ["only"], "general", "")


@unittest.skipUnless(shutil.which("git"), "git not installed")
class SessionTests(TempDir):
    def git(self, *args):
        subprocess.run(["git", "-C", str(self.tmp), "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
                       check=True, capture_output=True)

    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        (self.tmp / "a.txt").write_text("one\ntwo\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "init")

    def test_measures_time_and_churn(self):
        state = forge_session.start(self.tmp)
        self.assertFalse(state["baseline_dirty"])
        (self.tmp / "a.txt").write_text("one\nTWO\nthree\n", encoding="utf-8")
        (self.tmp / "b.py").write_text("x = 1\ny = 2\n", encoding="utf-8")
        later = datetime.fromisoformat(state["started_at"].replace("Z", "+00:00")) + timedelta(seconds=90)
        result = forge_session.measure(self.tmp, forge_session.load_state(self.tmp), now=later)
        self.assertEqual(result["wall_time_sec"], 90.0)
        self.assertEqual(result["git_stats"]["files_changed"], 2)
        self.assertEqual(result["git_stats"]["lines_added"], 4)
        self.assertEqual(result["git_stats"]["lines_removed"], 1)
        self.assertEqual(result["git_stats"]["new_untracked_files"], 1)

    def test_emit_validates_appends_and_clears(self):
        forge_session.start(self.tmp, task_id="aaaaaaaa-1111-4111-8111-111111111111")
        telemetry = self.tmp / "out" / "sessions.jsonl"
        record = session_record()
        del record["task_id"], record["timestamp"]
        saved = forge_session.emit(self.tmp, record, telemetry, ROOT / "telemetry" / "schema.json")
        self.assertEqual(saved["schema_version"], "1.1")
        self.assertEqual(saved["task_id"], "aaaaaaaa-1111-4111-8111-111111111111")
        self.assertIn("git_stats", saved["measured"])
        line = json.loads(telemetry.read_text(encoding="utf-8"))
        self.assertEqual(forge_schema.validate(line, TELEMETRY_SCHEMA), [])
        self.assertFalse(forge_session.state_path(self.tmp).exists())

    def test_invalid_record_writes_nothing(self):
        forge_session.start(self.tmp)
        telemetry = self.tmp / "sessions.jsonl"
        with self.assertRaises(forge_session.SessionError):
            forge_session.emit(self.tmp, {"workflow": "rise"}, telemetry, ROOT / "telemetry" / "schema.json")
        self.assertFalse(telemetry.exists())
        self.assertTrue(forge_session.state_path(self.tmp).exists())

    def test_guards(self):
        forge_session.start(self.tmp)
        with self.assertRaises(forge_session.SessionError):
            forge_session.start(self.tmp)
        forge_session.start(self.tmp, force=True)
        forge_session.state_path(self.tmp).unlink()
        with self.assertRaises(forge_session.SessionError):
            forge_session.load_state(self.tmp)

    def test_disabled_env_writes_nothing(self):
        forge_session.start(self.tmp)
        telemetry = self.tmp / "sessions.jsonl"
        record = self.tmp / "r.json"
        record.write_text(json.dumps(session_record()), encoding="utf-8")
        os.environ["FORGE_TELEMETRY_DISABLED"] = "1"
        try:
            with redirect_stdout(io.StringIO()):
                code = forge_session.main(["--project", str(self.tmp), "emit", "--file", str(record),
                                           "--telemetry", str(telemetry)])
        finally:
            del os.environ["FORGE_TELEMETRY_DISABLED"]
        self.assertEqual(code, 0)
        self.assertFalse(telemetry.exists())

    def test_outside_git_measures_time_only(self):
        plain = Path(tempfile.mkdtemp())
        try:
            state = forge_session.start(plain)
            self.assertIsNone(state["start_commit"])
            result = forge_session.measure(plain, state)
            self.assertIsNone(result["git_stats"])
            self.assertNotIn("git_stats", result["measured"])
        finally:
            shutil.rmtree(plain, ignore_errors=True)


class EvalAndReportTests(TempDir):
    def test_eval_scores_against_complexity_gates(self):
        result = forge_eval.score_session(session_record())
        self.assertIn("verification_layer_3", result["missing_gates"])
        self.assertEqual(result["outcome_modifier"], 0.85)

    def test_report_includes_measured_and_candidates(self):
        telemetry = self.tmp / "sessions.jsonl"
        measured = session_record(task_id="22222222-2222-4222-8222-222222222222", schema_version="1.1",
                                  outcome="success", iterations=1, wall_time_sec=600,
                                  git_stats={"files_changed": 3, "lines_added": 40, "lines_removed": 5},
                                  measured=["wall_time_sec", "git_stats"])
        unmeasured = session_record(wall_time_sec=99999)
        telemetry.write_text("\n".join(json.dumps(r) for r in (measured, unmeasured)) + "\n", encoding="utf-8")
        report = forge_report.render_md(forge_report.load_sessions(telemetry, 30), 30)
        self.assertIn("Measured sessions (v1.1):** 1 of 2", report)
        self.assertIn("median 10.0 min", report)   # the self-reported 99999 s is ignored
        self.assertIn("+40 / -5 lines", report)
        self.assertIn("forge_learn.py promote", report)


class RepositoryConsistencyTests(unittest.TestCase):
    LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

    def markdown_files(self):
        for path in ROOT.rglob("*.md"):
            parts = path.relative_to(ROOT).parts
            if parts[0] in (".git", "docs", "node_modules"):
                continue
            yield path

    def test_relative_markdown_links_resolve(self):
        broken = []
        for path in self.markdown_files():
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for target in self.LINK.findall(text):
                if re.match(r"^(https?:|mailto:|#)", target) or "<" in target:
                    continue
                file_part = target.split("#", 1)[0]
                if file_part and not (path.parent / file_part).exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [], "broken links:\n" + "\n".join(broken))

    def test_command_copies_stay_in_sync(self):
        """User-level copies differ from project copies only by the <FORGE_HOME>/ prefix and known wording."""
        for name in ("rise", "care", "harvest"):
            project = (ROOT / ".claude" / "commands" / f"{name}.md").read_text(encoding="utf-8")
            user = (ROOT / "integrations" / "claude-code" / "commands" / f"{name}.md").read_text(encoding="utf-8")
            for tool in ("forge_session.py start", "forge_learn.py search", "forge_session.py emit",
                         "forge_learn.py add"):
                self.assertIn(tool, project, f"{name}: project copy lacks {tool}")
                self.assertIn(tool, user, f"{name}: user copy lacks {tool}")
            self.assertNotIn("Plan 1", user + project)

    def test_no_duplicate_frameworks_folder(self):
        self.assertFalse((ROOT / "frameworks").exists())


if __name__ == "__main__":
    unittest.main()
