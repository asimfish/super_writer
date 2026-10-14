"""Role protocol and packaging checks, not semantic writing-quality tests."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/writing-team"
SPEC = importlib.util.spec_from_file_location("writing_loop", ROOT / "scripts/writing_loop.py")
LOOP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOOP)


class WritingLoopTests(unittest.TestCase):
    def setUp(self):
        self.run = json.loads((EXAMPLE / "input.json").read_text(encoding="utf-8"))
        self.outputs = json.loads((EXAMPLE / "responses.json").read_text(encoding="utf-8"))

    def advance(self, run, output=None):
        state = LOOP.inspect_run(run)
        role = state["packet"]["role"]
        return LOOP.append_response(run, {"role": role, "input_sha256": state["input_sha256"],
                                         "output": copy.deepcopy(output or self.outputs[role])})

    def through_writer(self, run=None):
        result = self.run if run is None else run
        for _ in range(3):
            result = self.advance(result)
        return result

    def test_complete_authored_sequence_retains_reviewed_text(self):
        run = self.run
        for role in ("gap_finder", "proposer", "writer", "reviewer"):
            self.assertEqual(LOOP.inspect_run(run)["packet"]["role"], role)
            run = self.advance(run)
        state = LOOP.inspect_run(run)
        self.assertEqual(state["status"], "accepted_revision")
        self.assertEqual(state["retained_text"], self.outputs["writer"]["text"])
        self.assertEqual(self.run["events"], [])

    def test_all_review_returns_route_to_owner_and_rebuild_downstream(self):
        for target in ("gap_finder", "proposer", "writer"):
            with self.subTest(target=target):
                review = copy.deepcopy(self.outputs["reviewer"])
                review["decision"] = "return_" + target
                run = self.advance(self.through_writer(), review)
                packet = LOOP.inspect_run(run)["packet"]
                self.assertEqual(packet["role"], target)
                self.assertEqual(packet["input"]["feedback"], review)
                if target == "gap_finder":
                    self.assertNotIn("gap", packet["input"])
                    self.assertNotIn("proposal", packet["input"])
                elif target == "proposer":
                    self.assertNotIn("proposal", packet["input"])
                # A repeated gap diagnosis must witness the current, not original, text.
                if target == "gap_finder":
                    gap = copy.deepcopy(self.outputs["gap_finder"])
                    gap["draft_witness"] = self.outputs["writer"]["text"]
                    run = self.advance(run, gap)
                while LOOP.inspect_run(run)["status"] == "ready":
                    run = self.advance(run)
                self.assertEqual(LOOP.inspect_run(run)["status"], "accepted_revision")

    def test_no_change_and_missing_evidence_stop_without_rewriting(self):
        for status in ("no_change", "needs_evidence"):
            out = copy.deepcopy(self.outputs["gap_finder"])
            out["status"] = status
            result = LOOP.inspect_run(self.advance(self.run, out))
            self.assertEqual(result["status"], status)
            self.assertEqual(result["retained_text"], self.run["draft"])
        run = self.advance(self.run)
        out = copy.deepcopy(self.outputs["proposer"])
        out["status"] = "needs_evidence"
        self.assertEqual(LOOP.inspect_run(self.advance(run, out))["status"], "needs_evidence")

    def test_reviewer_stops_keep_original_and_expose_last_attempt(self):
        for decision in ("needs_evidence", "keep_original"):
            out = copy.deepcopy(self.outputs["reviewer"])
            out["decision"] = decision
            state = LOOP.inspect_run(self.advance(self.through_writer(), out))
            self.assertEqual(state["retained_text"], self.run["draft"])
            self.assertEqual(state["last_attempt_text"], self.outputs["writer"]["text"])

    def test_budget_exhaustion_cannot_promote_unreviewed_text(self):
        self.run["max_steps"] = 5
        out = copy.deepcopy(self.outputs["reviewer"])
        out["decision"] = "return_writer"
        run = self.advance(self.through_writer(), out)
        state = LOOP.inspect_run(self.advance(run))
        self.assertEqual(state["status"], "budget_exhausted")
        self.assertEqual(state["retained_text"], self.run["draft"])
        self.assertEqual(state["steps_used"], 5)

    def test_acceptance_at_exact_budget_is_allowed(self):
        self.run["max_steps"] = 4
        self.assertEqual(LOOP.inspect_run(self.advance(self.through_writer()))["status"],
                         "accepted_revision")

    def test_changed_initial_inputs_invalidate_prior_receipts(self):
        for key in ("task", "draft", "evidence", "exemplars", "max_steps"):
            run = self.advance(self.run)
            if key in ("task", "draft"):
                run[key] += " Changed."
            elif key == "evidence":
                run[key]["E1"] += " Changed."
            elif key == "exemplars":
                run[key]["S1"]["choice"] += " Changed."
            else:
                run[key] = 10
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "stale"):
                LOOP.inspect_run(run)

    def test_changed_history_even_unused_writer_ids_invalidates_review(self):
        run = self.advance(self.through_writer())
        run["events"][2]["output"]["evidence_ids"] = ["E1"]
        with self.assertRaisesRegex(ValueError, "stale"):
            LOOP.inspect_run(run)

    def test_changed_guidance_invalidates_receipts(self):
        run = self.advance(self.run)
        with patch.object(LOOP, "instructions", return_value=[{"text": "Changed guide"}]), \
                self.assertRaisesRegex(ValueError, "stale"):
            LOOP.inspect_run(run)

    def test_wrong_owner_and_foreign_hash_are_rejected(self):
        state = LOOP.inspect_run(self.run)
        event = {"role": "gap_finder", "input_sha256": state["input_sha256"],
                 "output": self.outputs["gap_finder"]}
        for key, value in (("role", "writer"), ("input_sha256", "0" * 64)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                LOOP.append_response(self.run, {**event, key: value})

    def test_unknown_ids_and_nonlocated_witnesses_are_rejected(self):
        for key, value in (("evidence_ids", ["unknown"]), ("source_ids", ["unknown"]),
                           ("draft_witness", "Not actually in the draft"),
                           ("evidence_ids", ["E1", "E1"])):
            out = {**self.outputs["gap_finder"], key: value}
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.advance(self.run, out)
        out = copy.deepcopy(self.outputs["reviewer"])
        out["judgments"]["intrinsic"]["witness"] = "Absent text"
        with self.assertRaisesRegex(ValueError, "witness"):
            self.advance(self.through_writer(), out)

    def test_acceptance_requires_all_applicable_judgments(self):
        for dimension in LOOP.DIMENSIONS:
            out = copy.deepcopy(self.outputs["reviewer"])
            out["judgments"][dimension]["status"] = "fail"
            with self.subTest(dimension=dimension), self.assertRaises(ValueError):
                self.advance(self.through_writer(), out)
        for dimension, field in (("fidelity", "evidence_ids"),
                                 ("reference_function", "source_ids")):
            out = copy.deepcopy(self.outputs["reviewer"])
            out["judgments"][dimension][field] = []
            with self.subTest(dimension=dimension), self.assertRaises(ValueError):
                self.advance(self.through_writer(), out)

    def test_no_references_means_unassessed_not_fabricated_alignment(self):
        self.run["exemplars"] = {}
        for role in ("gap_finder", "proposer"):
            self.outputs[role]["source_ids"] = []
        out = self.outputs["reviewer"]
        out["judgments"]["reference_function"].update(
            status="not_assessed", reason="No exemplar supplied.", witness="", source_ids=[])
        state = LOOP.inspect_run(self.advance(self.through_writer(), out))
        self.assertEqual(state["status"], "accepted_revision")
        out["judgments"]["reference_function"].update(status="pass", witness="To test")
        with self.assertRaisesRegex(ValueError, "exemplars"):
            self.advance(self.through_writer(), out)

    def test_correctness_without_comparative_gain_cannot_accept(self):
        for comparison in ("tie", "worse", "not_assessed"):
            out = copy.deepcopy(self.outputs["reviewer"])
            out["comparison"] = comparison
            with self.subTest(comparison=comparison), self.assertRaisesRegex(ValueError, "comparative"):
                self.advance(self.through_writer(), out)
        self.outputs["writer"]["text"] = self.run["draft"]
        out = copy.deepcopy(self.outputs["reviewer"])
        for judgment in out["judgments"].values():
            judgment["witness"] = "Our policy reaches 68% success."
        with self.assertRaisesRegex(ValueError, "Unchanged"):
            self.advance(self.through_writer(), out)

    def test_unresolved_writer_queries_block_acceptance(self):
        self.outputs["writer"]["open_queries"] = ["Was the task mix actually matched?"]
        with self.assertRaisesRegex(ValueError, "queries"):
            self.advance(self.through_writer())

    def test_reviewer_packet_has_no_diagnosis_proposal_or_prior_review(self):
        self.outputs["gap_finder"]["diagnosis"] = "DIAGNOSIS_SENTINEL"
        self.outputs["proposer"]["operation"] = "PROPOSAL_SENTINEL"
        run = self.through_writer()
        out = copy.deepcopy(self.outputs["reviewer"])
        out.update(decision="return_writer", reason="REVIEW_SENTINEL")
        run = self.advance(self.advance(run, out))
        packet = LOOP.inspect_run(run)["packet"]
        self.assertEqual(set(packet["input"]),
                         {"task", "draft", "original_draft", "evidence", "exemplars", "open_queries"})
        self.assertNotIn("SENTINEL", json.dumps(packet))

    def test_packet_has_no_mutable_alias_to_run(self):
        packet = LOOP.inspect_run(self.run)["packet"]
        packet["input"]["evidence"]["E1"] = "Altered"
        self.assertNotEqual(self.run["evidence"]["E1"], "Altered")

    def test_terminal_runs_cannot_receive_additional_events(self):
        run = self.advance(self.through_writer())
        with self.assertRaisesRegex(ValueError, "terminal"):
            LOOP.append_response(run, {})
        run["events"].append(copy.deepcopy(run["events"][-1]))
        with self.assertRaisesRegex(ValueError, "terminal"):
            LOOP.inspect_run(run)

    def test_strict_schema_rejects_hidden_oracles_and_invalid_budget(self):
        for key, value in (("oracle", "PRIVATE"), ("max_steps", True), ("max_steps", 25),
                           ("max_steps", 3), ("evidence", {}), ("schema_version", True),
                           ("events", {})):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                LOOP.inspect_run({**self.run, key: value})
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            json.loads('{"task": "first", "task": "second"}', object_pairs_hook=LOOP.unique_object)

    def test_offline_read_only_and_no_source_path_dereference(self):
        self.run["exemplars"]["S1"]["source"] = "/nonexistent/private/source"
        with patch("socket.socket", side_effect=AssertionError("No network")), \
                patch.object(Path, "write_text", side_effect=AssertionError("No writes")), \
                patch.object(Path, "write_bytes", side_effect=AssertionError("No writes")):
            self.assertEqual(LOOP.inspect_run(self.run)["status"], "ready")

    def test_release_bundle_cli_is_relocatable_and_appends_without_writing(self):
        with tempfile.TemporaryDirectory(prefix="writing team ") as temporary:
            base = Path(temporary)
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools/build_release.py"), "--output-dir", str(base / "release")],
                cwd=base, capture_output=True, text=True, encoding="utf-8", timeout=60,
                env={**os.environ, "PYTHONUTF8": "1"})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            archive, = (base / "release").glob("*.zip")
            with zipfile.ZipFile(archive) as bundle:
                bundle.extractall(base / "installed")
            installed = base / "installed/super-writer"
            command = [sys.executable, str(installed / "scripts/writing_loop.py"),
                       str(installed / "examples/writing-team/input.json")]
            result = subprocess.run(command, cwd=base, capture_output=True, text=True,
                                    encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), LOOP.inspect_run(self.run))
            state = json.loads(result.stdout)
            response = {"role": "gap_finder", "input_sha256": state["input_sha256"],
                        "output": self.outputs["gap_finder"]}
            response_path = base / "response.json"
            response_path.write_text(json.dumps(response), encoding="utf-8")
            original = (installed / "examples/writing-team/input.json").read_bytes()
            result = subprocess.run(command + ["--response", str(response_path)], cwd=base,
                                    capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = json.loads(result.stdout)
            self.assertEqual(LOOP.inspect_run(updated)["packet"]["role"], "proposer")
            self.assertEqual((installed / "examples/writing-team/input.json").read_bytes(), original)
            response_path.write_text('{"bad": true}', encoding="utf-8")
            result = subprocess.run(command + ["--response", str(response_path)], cwd=base,
                                    capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
