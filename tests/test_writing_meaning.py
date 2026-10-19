"""Authored v3 contract probes, not evidence that generated writing improved."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("meaning_loop", ROOT / "scripts/writing_loop.py")
loop = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(ROOT / "scripts"), *sys.path]):
    SPEC.loader.exec_module(loop)


class MeaningContractTests(unittest.TestCase):
    def setUp(self):
        base = Path(__file__).resolve().parents[1] / "examples/writing-team"
        self.run = json.loads((base / "benchmark-input.json").read_text(encoding="utf-8"))
        self.outputs = json.loads((base / "benchmark-responses.json").read_text(encoding="utf-8"))
        self.run["schema_version"] = 3
        self.run["benchmark"]["budget"]["max_delta_words"] = None
        self.run["benchmark"]["relations"] = {
            "M1": {"meaning": "Update observed cells instead of rebuilding the whole map.",
                   "evidence_ids": ["E1"], "original_witness": ""}}
        self.check = {"status": "stated", "witness": "instead of rebuilding the map",
                      "readback": "Selective updating avoids rebuilding the entire map."}
        for role in ("writer", "reviewer"):
            self.outputs[role]["relation_checks"] = {"M1": copy.deepcopy(self.check)}
        for ident, row in self.outputs["reviewer"]["assessments"].items():
            original = self.outputs["gap_finder"]["assessments"][ident]
            row.update(original_status=original["status"], original_witness=original["draft_witness"])

    def advance(self, run, output=None):
        state = loop.inspect_run(run)
        role = state["packet"]["role"]
        return loop.append_response(run, {"role": role, "input_sha256": state["input_sha256"],
                                         "output": copy.deepcopy(output or self.outputs[role])})

    def through(self, count):
        run = self.run
        for _ in range(count):
            run = self.advance(run)
        return run

    def test_compatible_complete_v3_run(self):
        self.assertEqual(loop.inspect_run(self.through(4))["status"], "accepted_revision")

    def test_decimal_metrics_do_not_consume_sentence_budget(self):
        self.assertEqual(loop.writing_benchmark.sentence_count(
            "The error is 1.46 mm at 32 FPS. The baseline reaches 2.14 mm."), 2)
        self.assertEqual(loop.writing_benchmark.sentence_count("Version 3.0 uses 0.25 m"), 1)
        self.assertEqual(loop.writing_benchmark.sentence_count(""), 0)

    def test_expansion_within_absolute_budget_can_restore_explanation(self):
        out = self.outputs["writer"]
        out["text"] += " The selective update retains unchanged cells between observations."
        words = loop.writing_benchmark.word_count(out["text"])
        out["compression"].update(revision_words=words, delta_words=words - 44,
                                  removed_or_merged=[])
        out["compression"]["added_clauses"].append("retains unchanged cells")
        self.assertGreater(words, 44)
        self.advance(self.through(2))

    def test_explicit_no_expansion_is_still_binding(self):
        self.run["benchmark"]["budget"]["max_delta_words"] = 0
        out = self.outputs["writer"]
        out["text"] += " The selective update retains unchanged cells between observations."
        words = loop.writing_benchmark.word_count(out["text"])
        out["compression"].update(revision_words=words, delta_words=words - 44)
        with self.assertRaisesRegex(ValueError, "change in word count"):
            self.advance(self.through(2))

    def test_absolute_limit_cannot_be_disabled(self):
        self.run["benchmark"]["budget"]["max_words"] = 39
        with self.assertRaisesRegex(ValueError, "word budget"):
            self.advance(self.through(2))

    def test_relation_input_requires_evidence_and_real_original_witness(self):
        for changes in ({"evidence_ids": []}, {"evidence_ids": ["unknown"]},
                        {"meaning": ""}, {"original_witness": "NOT IN ORIGINAL"}):
            run = copy.deepcopy(self.run)
            run["benchmark"]["relations"]["M1"].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                loop.inspect_run(run)
        self.run["benchmark"]["relations"] = {}
        with self.assertRaisesRegex(ValueError, "1..3"):
            loop.inspect_run(self.run)

    def test_writer_cannot_substitute_notes_for_prose(self):
        for checks in ({}, {"M1": {**self.check, "witness": "NOT IN PROSE"}},
                       {"M1": {**self.check, "status": "keyword_present"}}):
            out = copy.deepcopy(self.outputs["writer"])
            out["relation_checks"] = checks
            with self.subTest(checks=checks), self.assertRaises(ValueError):
                self.advance(self.through(2), out)

    def test_missing_relation_stops_acceptance_even_when_priority_criteria_pass(self):
        out = copy.deepcopy(self.outputs["reviewer"])
        out["relation_checks"]["M1"].update(status="missing", witness="")
        with self.assertRaisesRegex(ValueError, "Missing meaning"):
            self.advance(self.through(3), out)
        out["decision"] = "return_writer"
        self.advance(self.through(3), out)

    def test_existing_lower_priority_gap_may_remain(self):
        out = copy.deepcopy(self.outputs["reviewer"])
        out["assessments"]["C5"].update(status="gap", original_status="gap")
        self.assertEqual(loop.inspect_run(self.advance(self.through(3), out))["status"],
                         "accepted_revision")

    def test_new_lower_priority_gap_cannot_hide_behind_deferral(self):
        out = copy.deepcopy(self.outputs["reviewer"])
        out["assessments"]["C5"]["status"] = "gap"
        with self.assertRaisesRegex(ValueError, "newly introduced gap"):
            self.advance(self.through(3), out)

    def test_previously_clear_criterion_cannot_become_inapplicable(self):
        out = copy.deepcopy(self.outputs["reviewer"])
        out["assessments"]["C5"].update(status="not_applicable", draft_witness="")
        with self.assertRaisesRegex(ValueError, "cannot regress"):
            self.advance(self.through(3), out)

    def test_candidate_cannot_be_accepted_with_unassessed_nonpriority_criterion(self):
        out = copy.deepcopy(self.outputs["reviewer"])
        out["assessments"]["C5"].update(status="not_assessed", draft_witness="")
        with self.assertRaisesRegex(ValueError, "Unassessed candidate"):
            self.advance(self.through(3), out)

    def test_original_status_needs_its_own_literal_witness(self):
        out = copy.deepcopy(self.outputs["reviewer"])
        out["assessments"]["C5"]["original_witness"] = "NOT IN ORIGINAL"
        with self.assertRaisesRegex(ValueError, "Original assessment witness"):
            self.advance(self.through(3), out)

    def test_returned_writer_counts_against_original_not_last_attempt(self):
        run = self.through(3)
        review = copy.deepcopy(self.outputs["reviewer"])
        review["decision"] = "return_writer"
        run = self.advance(run, review)
        packet = loop.inspect_run(run)["packet"]
        self.assertNotEqual(packet["input"]["draft"], packet["input"]["original_draft"])
        run = self.advance(run)
        self.assertEqual(loop.inspect_run(self.advance(run))["status"], "accepted_revision")

    def test_v2_keeps_its_explicit_relative_cap_contract(self):
        self.run["schema_version"] = 2
        del self.run["benchmark"]["relations"]
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            loop.inspect_run(self.run)

    def test_relation_change_invalidates_receipts_and_review_hides_writer_readback(self):
        run = self.through(1)
        run["benchmark"]["relations"]["M1"]["meaning"] += " Changed."
        with self.assertRaisesRegex(ValueError, "stale"):
            loop.inspect_run(run)
        self.outputs["writer"]["relation_checks"]["M1"]["readback"] = "PRIVATE_WRITER_REASON"
        packet = loop.inspect_run(self.through(3))["packet"]
        self.assertNotIn("PRIVATE_WRITER_REASON", json.dumps(packet))
        self.assertNotIn("relation_checks", packet["input"])


if __name__ == "__main__":
    unittest.main()
