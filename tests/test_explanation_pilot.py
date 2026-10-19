"""Archive integrity and denominators; semantic model judgments remain fallible."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evals/explanation-pilot"
SPEC = importlib.util.spec_from_file_location("explanation_pilot", ARCHIVE / "pilot.py")
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


class ExplanationPilotTests(unittest.TestCase):
    def test_archive_reproduces_without_model_calls(self):
        self.assertEqual(pilot.check()["status"], "pass")

    def test_identical_evidence_priorities_and_budgets_in_relaxed_control(self):
        for block in (1, 2):
            hard, relaxed, meaning = [pilot.read(ARCHIVE / "prompts" / f"{c}-{block}.json")
                                      for c in pilot.CONDITIONS]
            self.assertEqual(relaxed["cases"], meaning["cases"])
            self.assertEqual(hard["guides"], relaxed["guides"])
            self.assertEqual(relaxed["guides"][0], meaning["guides"][0])
            self.assertNotEqual(relaxed["guides"][1], meaning["guides"][1])
            for first, second in zip(hard["cases"], relaxed["cases"]):
                self.assertEqual({k: v for k, v in first.items() if k != "max_words"},
                                 {k: v for k, v in second.items() if k != "max_words"})
                self.assertEqual(first["max_words"], pilot.count(first["initial_draft"]))
                self.assertEqual(second["max_words"], 150)
                self.assertNotIn("questions", second)
                self.assertNotIn("answer", second)

    def test_source_scope_excludes_first_page(self):
        for paper in pilot.read(ARCHIVE / "materials.json")["papers"]:
            receipt = paper["source_receipt"]
            pages = receipt.get("read_pdf_page_numbers", receipt.get("read_pdf_pages"))
            self.assertNotIn(1, pages)
            self.assertEqual(len(receipt["pdf_sha256"]), 64)
            self.assertEqual(len(receipt["body_excerpt_sha256"]), 64)

    def test_preference_packets_are_prose_only_and_reversed(self):
        outputs = pilot.revisions()
        mapping = pilot.read(ARCHIVE / "blind/mapping.json")
        first, second = [pilot.read(ARCHIVE / "blind" / f"{j}.json")["cases"]
                         for j in ("J01", "J02")]
        self.assertEqual([c["id"] for c in first], [c["id"] for c in second[::-1]])
        for judge, cases in (("J01", first), ("J02", second)):
            for case in cases:
                self.assertEqual(set(case), {"id", "versions"})
                for label, text in case["versions"].items():
                    self.assertEqual(text, outputs[(case["id"], mapping[judge][case["id"]][label])]["text"])
        for ident in mapping["J01"]:
            self.assertEqual(list(mapping["J01"][ident].values()), list(mapping["J02"][ident].values())[::-1])

    def test_saved_denominators_include_every_passage_pair_and_answer(self):
        summary = pilot.analyze()
        self.assertEqual(len(summary["words"]), 12)
        self.assertEqual(len(summary["pairs"]), 24)
        for control in summary["comparisons"].values():
            for dimension in control.values():
                self.assertEqual(sum(dimension.values()), 8)
        for condition in summary["recovery"].values():
            self.assertEqual(sum(condition.values()), 8)

    def test_duplicate_pair_and_missing_answer_are_rejected(self):
        original = pilot.read
        for target in ("J01", "R01", "A01"):
            def altered(path):
                value = original(path)
                if path == ARCHIVE / "raw" / f"{target}.json":
                    value = copy.deepcopy(value)
                    if target == "J01":
                        value["cases"][0]["pairs"][1] = value["cases"][0]["pairs"][0]
                    else:
                        value["cases"][0]["answers"].pop()
                return value
            with self.subTest(target=target), patch.object(pilot, "read", side_effect=altered), \
                    self.assertRaises(AssertionError):
                pilot.analyze()

    def test_consequential_error_veto_is_not_hidden_by_preference(self):
        original = pilot.read
        mapping = original(ARCHIVE / "blind/mapping.json")["reader"]
        candidate = next(ident for ident, case in mapping.items() if case["condition"] == "meaning")

        def altered(path):
            value = original(path)
            if path == ARCHIVE / "raw/A01.json":
                value = copy.deepcopy(value)
                case = next(c for c in value["cases"] if c["id"] == candidate)
                case["factual_errors"].append({"claim": case["id"], "evidence_ids": [],
                                                "reason": "Injected recorded consequential error."})
            return value
        with patch.object(pilot, "read", side_effect=altered):
            summary = pilot.analyze()
            self.assertFalse(summary["gate"]["fidelity"])
            self.assertFalse(summary["gate"]["passed"])
            self.assertTrue(any(e["case"] == candidate for e in summary["factual_errors"]))

    def test_frozen_inputs_cannot_be_changed_after_generation(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            (base / "freeze.json").write_text(json.dumps({"inputs": {"packet.json": "old"}}))
            (base / "packet.json").write_text("changed")
            with patch.object(pilot, "ROOT", base), self.assertRaisesRegex(ValueError, "Frozen input changed"):
                pilot.verify_freeze()


if __name__ == "__main__":
    unittest.main()
