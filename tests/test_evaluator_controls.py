"""Archive/fixture integrity, not semantic validation or writing quality."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "evals" / "evaluator-controls"


class EvaluatorControlTests(unittest.TestCase):
    def test_control_groups_and_case_ids_are_complete(self):
        cases = json.loads((ROOT / "cases.json").read_text())["cases"]
        self.assertEqual(len({c["id"] for c in cases}), 12)
        for category in ("relation", "metric", "condition"):
            self.assertEqual(sum(c["category"] == category for c in cases), 3)
        for c in cases:
            self.assertEqual(set(c["variants"]), {"v1", "v2"})
            self.assertTrue(c["evidence"])
            self.assertTrue(c["question"])
            self.assertTrue(c["relation"])

    def test_neutral_controls_do_not_force_stylistic_equivalence(self):
        cases = json.loads((ROOT / "cases.json").read_text())["cases"]
        neutral = {c["category"]: c for c in cases if c["category"].startswith("neutral")}
        identical = neutral["neutral_identical"]
        self.assertEqual(identical["variants"]["v1"], identical["variants"]["v2"])
        self.assertEqual(identical["oracle"]["preferred"], ["tie"])
        for key in ("neutral_paraphrase", "neutral_omission"):
            self.assertEqual(set(neutral[key]["oracle"]["preferred"]), {"v1", "v2", "tie"})
            self.assertEqual(neutral[key]["oracle"]["support"], {"v1": "supported", "v2": "supported"})

    def test_saved_raw_responses_match_archive_byte_receipts(self):
        import hashlib

        hashes = json.loads((ROOT / "all_raw_hashes.json").read_text())
        self.assertEqual(len(hashes), 10)
        for name, expected in hashes.items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected, name)
        summary = json.loads((ROOT / "summary.json").read_text())
        self.assertEqual(summary["completed"]["preference_votes"], 24)
        self.assertEqual(summary["completed"]["reader_reconstructions"], 24)
        self.assertEqual(summary["completed"]["coarse_judgments"], 48)
        self.assertEqual(summary["completed"]["fine_judgments"], 48)


if __name__ == "__main__":
    unittest.main()
