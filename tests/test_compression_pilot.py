"""Verify pilot provenance, blinding, denominators and rejection of damaged records."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evals/compression-pilot"
SPEC = importlib.util.spec_from_file_location("compression_pilot_archive", ARCHIVE / "pilot.py")
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


class CompressionPilotTests(unittest.TestCase):
    def test_frozen_inputs_and_saved_completions_are_intact(self):
        pilot.verify_freeze()
        for path in (ARCHIVE / "responses").glob("*.json"):
            response = pilot.read(path)
            self.assertEqual(json.loads(response["completion"]),
                             pilot.read(ARCHIVE / "raw" / path.name))

    def test_conditions_share_the_same_evidence_drafts_and_questions(self):
        for block in (1, 2):
            packets = [pilot.read(ARCHIVE / "prompts" / f"{c}-{block}.json")
                       for c in pilot.CONDITIONS]
            self.assertEqual(packets[0]["cases"], packets[1]["cases"])
            self.assertEqual(packets[0]["cases"], packets[2]["cases"])
            self.assertEqual(packets[0]["writing_resources"], packets[1]["writing_resources"])
            self.assertEqual(packets[2]["guides"], [])

    def test_blinding_reverses_order_and_preserves_exact_prose(self):
        outputs = pilot.generations()
        mapping = pilot.read(ARCHIVE / "mapping.json")
        first = pilot.read(ARCHIVE / "blind/J01.json")["cases"]
        second = pilot.read(ARCHIVE / "blind/J02.json")["cases"]
        self.assertEqual([p["id"] for p in first], [p["id"] for p in reversed(second)])
        for judge, cases in (("J01", first), ("J02", second)):
            self.assertEqual(len(cases), 12)
            for case in cases:
                self.assertEqual(set(case), {"id", "unit", "contribution", "facts", "questions", "versions"})
                labels = mapping[f'{judge}/{case["id"]}']
                self.assertEqual(set(labels.values()), {*pilot.CONDITIONS, "initial"})
                for side, condition in labels.items():
                    self.assertEqual(case["versions"][side], outputs[case["id"], condition]["text"])

    def test_saved_analysis_and_display_reproduce(self):
        summary = pilot.analyze()
        self.assertEqual(summary, pilot.read(ARCHIVE / "summary.json"))
        self.assertEqual(pilot.render(summary), (ARCHIVE / "comparison.html").read_text())
        self.assertEqual(summary["passages"], 36)
        for comparison in summary["votes"].values():
            self.assertEqual(sum(comparison.values()), 24)
        for condition in summary["recovery"].values():
            self.assertEqual(sum(condition.values()), 48)

    def test_changed_frozen_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            (base / "freeze.json").write_text(json.dumps({"inputs": {"fact.json": "unchanged"}}))
            (base / "fact.json").write_text("changed")
            with patch.object(pilot, "ROOT", base), self.assertRaisesRegex(ValueError, "Frozen input changed"):
                pilot.verify_freeze()

    def test_duplicate_comparison_is_rejected(self):
        original = pilot.read

        def altered(path):
            data = original(path)
            if path == ARCHIVE / "raw/J01.json":
                data = copy.deepcopy(data)
                rows = data["cases"][0]["comparisons"]
                rows[1] = rows[0]
            return data

        with patch.object(pilot, "read", side_effect=altered), self.assertRaises(AssertionError):
            pilot.analyze()

    def test_consequential_candidate_factual_concern_is_retained(self):
        original = pilot.read
        mapping = original(ARCHIVE / "mapping.json")

        def altered(path):
            data = original(path)
            if path == ARCHIVE / "raw/J01.json":
                data = copy.deepcopy(data)
                case = data["cases"][0]
                labels = mapping[f'J01/{case["id"]}']
                side = next(s for s, condition in labels.items() if condition == "compression")
                assessment = case["versions"][side]
                prose = pilot.generations()[case["id"], "compression"]["text"]
                assessment.update(fidelity="concern", consequential=True, issues=[{
                    "witness": prose[:30], "fact_ids": ["F01"],
                    "reason": "Injected recorded factual failure for the gate test."}])
            return data

        with patch.object(pilot, "read", side_effect=altered):
            summary = pilot.analyze()
            injected = [row for row in summary["fidelity_concerns"]
                        if any(issue["reason"].startswith("Injected recorded") for issue in row["issues"])]
            self.assertEqual(len(injected), 1)
            self.assertEqual(injected[0]["condition"], "compression")
            self.assertTrue(injected[0]["consequential"])
            self.assertFalse(summary["gate_pass"])


if __name__ == "__main__":
    unittest.main()
