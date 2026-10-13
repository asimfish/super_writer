"""Archive integrity and frozen continuation logic, not human writing quality."""

import hashlib
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evals" / "abstract-transfer"


def read(name):
    return json.loads((ARCHIVE / name).read_text())


class EntryPointVerifierTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("public_verifier", ARCHIVE / "verify_public.py")
        self.verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.verifier)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        entries = ["README.md", "README.en.md", "BENCHMARK.md", "UPSTREAM.md", "docs/validation.md",
            "docs/broad-writing-evaluation.md", "docs/evaluator-control-calibration.md",
            "docs/operative-relation-evaluation.md", "docs/abstract-transfer-evaluation.md",
            "evals/broad-writing/README.md", "evals/evaluator-controls/README.md",
            "evals/operative-relation/README.md", "evals/abstract-transfer/README.md", "examples/README.md"]
        for name in entries:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("")

    def test_existing_directory_and_file_are_distinct_valid_links(self):
        (self.repo / "materials").mkdir()
        (self.repo / "sample.txt").write_text("fixture")
        (self.repo / "README.md").write_text("[directory](materials/) [file](sample.txt)")
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.verifier.main(self.repo)
        result = json.loads(stream.getvalue())
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["local_file_destinations"], 1)
        self.assertEqual(result["local_directory_destinations"], 1)

    def test_missing_directory_still_fails_closed(self):
        (self.repo / "README.md").write_text("[missing directory](absent/)")
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream), self.assertRaises(SystemExit) as raised:
            self.verifier.main(self.repo)
        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(json.loads(stream.getvalue())["missing"], [{"entry": "README.md", "target": "absent/"}])


class AbstractTransferArchiveTests(unittest.TestCase):
    def test_every_response_and_pair_is_preserved(self):
        hashes = read("all_raw_hashes.json")
        self.assertEqual(len(hashes), 36)
        for name, expected in hashes.items():
            self.assertEqual(hashlib.sha256((ARCHIVE / name).read_bytes()).hexdigest(), expected, name)
        pairs = read("pair_results.json")
        self.assertEqual(len({p["id"] for p in pairs}), 12)
        for pair in pairs:
            self.assertEqual(len(pair["winners"]), 2)
            for condition in ("baseline", "candidate"):
                for channel in ("fidelity", "critical_support", "reader_support"):
                    self.assertEqual(len(pair["source"][condition][channel]), 2)
        self.assertEqual(read("summary.json")["completed"]["source_audit_judgments"], 48)

    def test_sources_are_receipts_not_redistributed_papers(self):
        for folder in ("sources", "inputs", "metadata"):
            self.assertFalse((ARCHIVE / folder).exists())
        self.assertFalse(list(ARCHIVE.rglob("*.pdf")))
        receipts = read("source_receipts.json")
        self.assertEqual({r["id"] for r in receipts}, {f"A{i:02d}" for i in range(1, 7)})
        for receipt in receipts:
            self.assertTrue(receipt["metadata_url"].startswith("https://"))
            for role in ("pdf", "extracted", "body", "recipe"):
                self.assertEqual(len(receipt["hashes"][role]), 64)
            self.assertNotIn("segments", receipt)

    def test_intervention_identity_and_gate_are_not_retrofitted(self):
        previous = ROOT / "evals" / "operative-relation"
        for condition in ("baseline", "candidate"):
            self.assertEqual((ARCHIVE / condition / "argument-transfer.md").read_bytes(),
                             (previous / condition / "argument-transfer.md").read_bytes())
        self.assertEqual((ARCHIVE / "baseline/argument-transfer.md").read_bytes(),
                         (ROOT / "references/argument-transfer.md").read_bytes())
        mapping = read("mapping.json")
        self.assertEqual(len(mapping), 12)
        for m in mapping:
            self.assertEqual(m["reviewer_1"]["A"], m["reviewer_2"]["B"])
            self.assertNotEqual(m["reader_1"]["condition"], m["reader_2"]["condition"])
        summary = read("summary.json")
        self.assertEqual(sum(summary["votes"].values()), 24)
        self.assertEqual(sum(summary["pair_outcomes"].values()), 12)
        gate = summary["continuation_gate"]
        self.assertEqual(gate["eligible_for_further_abstract_validation"], all(gate["criteria"].values()))
        papers = summary["by_paper"]
        samples = summary["by_sample"]
        self.assertEqual(gate["criteria"]["four_papers_net_candidate"],
                         sum(r.get("candidate", 0) > r.get("baseline", 0) for r in papers.values()) >= 4)
        self.assertEqual(gate["criteria"]["both_samples_net_candidate"],
                         all(r.get("candidate", 0) > r.get("baseline", 0) for r in samples.values()))


if __name__ == "__main__":
    unittest.main()
