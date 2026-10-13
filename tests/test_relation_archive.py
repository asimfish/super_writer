"""Targeted experiment integrity, not model prose quality or human validity."""

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "evals" / "operative-relation"


class RelationArchiveTests(unittest.TestCase):
    def test_all_raw_responses_and_pairs_are_preserved(self):
        hashes = json.loads((ROOT / "all_raw_hashes.json").read_text())
        self.assertEqual(len(hashes), 24)
        for name, expected in hashes.items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected, name)
        pairs = json.loads((ROOT / "pair_results.json").read_text())
        self.assertEqual(len({p["id"] for p in pairs}), 12)
        for pair in pairs:
            self.assertEqual(len(pair["winners"]), 2)
            for condition in ("baseline", "candidate"):
                self.assertEqual(len(pair["source"][condition]["fidelity"]), 2)
                self.assertEqual(len(pair["source"][condition]["critical_support"]), 2)

    def test_source_prose_is_not_redistributed(self):
        manifest = json.loads((ROOT / "MANIFEST.json").read_text())
        self.assertIn("selected publisher body", manifest["withheld"])
        self.assertFalse((ROOT / "inputs").exists())
        self.assertFalse((ROOT / "sources").exists())
        self.assertFalse((ROOT / "metadata").exists())
        self.assertFalse(list(ROOT.rglob("*.pdf")))
        receipts = json.loads((ROOT / "source_receipts.json").read_text())
        self.assertEqual({r["id"] for r in receipts}, {"N1", "N2"})
        for receipt in receipts:
            self.assertTrue(receipt["metadata_url"].startswith("https://"))
            for role in ("pdf", "body", "extracted"):
                self.assertEqual(len(receipt["hashes"][role]), 64)

    def test_candidate_is_a_narrow_append_only_hypothesis(self):
        baseline = (ROOT / "baseline/argument-transfer.md").read_bytes()
        candidate = (ROOT / "candidate/argument-transfer.md").read_bytes()
        self.assertTrue(candidate.startswith(baseline))
        self.assertNotEqual(candidate, baseline)
        summary = json.loads((ROOT / "summary.json").read_text())
        self.assertEqual(sum(summary["votes"].values()), 24)
        self.assertEqual(sum(summary["pair_outcomes"].values()), 12)
        self.assertEqual(summary["completed"]["source_audit_judgments"], 48)
        self.assertEqual(summary["completed"]["reader_reconstructions"], 24)


if __name__ == "__main__":
    unittest.main()
