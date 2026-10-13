"""Synthetic checks for blinding and recovery provenance, not writing outcomes."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ai_spec_archive", ROOT / "evals/ai-spec-pilot/archive.py")
archive = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archive)


def packet():
    return {"pairs": [{"id": "R01_s1_abstract", "paper": "R01", "sample": 1,
                       "unit": "abstract", "A": "A clear synthetic relation.",
                       "B": "A different synthetic relation."}]}


def questions():
    return {"questions": {"R01": {"abstract": [{"id": "a1", "question": "Synthetic question?"}]}}}


def reader(identifier="T01"):
    return {"reader_id": identifier, "answers": [
        {"id": "R01_s1_abstract", "side": side, "question_id": "a1", "status": "recoverable",
         "answer": "Synthetic answer.", "witnesses": ["synthetic relation"]} for side in ("A", "B")]}


def audit():
    return {"auditor_id": "F01", "passages": [
        {"id": "R01_s1_abstract", "side": s, "status": "pass", "consequential": False, "issues": []}
        for s in ("A", "B")], "recovery": [
        {"reader_id": r, "id": "R01_s1_abstract", "side": s, "question_id": "a1",
         "status": "recovered", "witness_supported": True, "reason": "Synthetic check."}
        for r in ("T01", "T02") for s in ("A", "B")]}


class RecoveryValidationTests(unittest.TestCase):
    def test_exact_witness_checks_do_not_mutate_reader(self):
        data = reader()
        before = copy.deepcopy(data)
        checks = archive.validate_reader(data, packet(), questions())
        self.assertTrue(all(c["exact"] for c in checks))
        self.assertEqual(data, before)

    def test_nonexact_and_empty_witnesses_remain_reported_outcomes(self):
        data = reader()
        data["answers"][0]["witnesses"] = ["reader-added words"]
        data["answers"][1]["witnesses"] = []
        checks = archive.validate_reader(data, packet(), questions())
        self.assertFalse(checks[0]["exact"])
        self.assertTrue(checks[1]["empty"])

    def test_reader_duplicate_missing_unknown_status_and_bad_witness_rejected(self):
        for mutation in (lambda d: d["answers"].pop(),
                         lambda d: d["answers"].append(d["answers"][0]),
                         lambda d: d["answers"][0].update(status="excellent"),
                         lambda d: d["answers"][0].update(witnesses=[3]),
                         lambda d: d.update(reader_id="T03")):
            data = reader()
            mutation(data)
            with self.assertRaises(ValueError):
                archive.validate_reader(data, packet(), questions())

    def check_audit(self, data, readers=None):
        return archive.validate_audit(data, packet(), questions(), readers or [reader(), reader("T02")],
                                      {"papers": [{"id": "R01", "facts": [{"id": "D01"}]}]})

    def test_complete_synthetic_audit(self):
        self.assertEqual(self.check_audit(audit()), [])

    def test_auditor_nonexact_witness_acceptance_is_reported_not_hidden(self):
        data = reader()
        data["answers"][0]["witnesses"] = ["unsupported witness"]
        result = self.check_audit(audit(), [data, reader("T02")])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["reader_id"], "T01")

    def test_incomplete_audit_and_inconsistent_pass_rejected(self):
        for mutation in (lambda d: d["passages"].pop(), lambda d: d["recovery"].pop(),
                         lambda d: d["passages"][0].update(consequential=True),
                         lambda d: d["recovery"][0].update(witness_supported=1),
                         lambda d: d["recovery"][0].update(status="great")):
            data = audit()
            mutation(data)
            with self.assertRaises(ValueError):
                self.check_audit(data)

    def test_concern_requires_exact_witness_and_known_fact(self):
        data = audit()
        row = data["passages"][0]
        row.update(status="concern", consequential=True,
                   issues=[{"witness": "synthetic relation", "fact_ids": ["D01"], "reason": "Synthetic issue."}])
        self.assertEqual(self.check_audit(data), [])
        for field, value in (("witness", "not in prose"), ("fact_ids", ["D02"])):
            invalid = copy.deepcopy(data)
            invalid["passages"][0]["issues"][0][field] = value
            with self.assertRaises(ValueError):
                self.check_audit(invalid)


class ProvenanceTests(unittest.TestCase):
    def test_reversal_normalizes_scores_and_preferences_not_reason_text(self):
        data = {"reviewer_id": "J02", "pairs": [{"id": "synthetic", "preferred": "A",
                "A": {"language": 2}, "B": {"language": 4}, "reason": "A is preferred in reversed labels."}]}
        before = copy.deepcopy(data)
        normalized = archive.normalize_review(data)
        self.assertEqual(normalized["pairs"][0]["preferred"], "B")
        self.assertEqual(normalized["pairs"][0]["A"]["language"], 4)
        self.assertEqual(normalized["pairs"][0]["reason"], data["pairs"][0]["reason"])
        self.assertEqual(data, before)

    def test_frozen_input_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "synthetic.txt"
            path.write_text("Synthetic input", encoding="utf-8")
            archive.write_new(root / "freeze.json", {"inputs": {"synthetic.txt": {
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}}})
            archive.verify_freeze(root)
            path.write_text("Changed synthetic input", encoding="utf-8")
            with self.assertRaises(ValueError):
                archive.verify_freeze(root)

    def test_derived_output_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "output.json"
            archive.write_new(path, {"synthetic": True})
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                archive.write_new(path, {"synthetic": False})
            self.assertEqual(path.read_bytes(), before)

    def test_archive_rejects_link_before_permissive_windows_open(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "target.json"
            absent = Path(temp) / "absent.json"
            try:
                target.symlink_to(absent)
            except (OSError, NotImplementedError):
                if sys.platform == "win32":
                    self.skipTest("Windows symlink creation requires an enabled privilege.")
                raise
            original_open = Path.open
            reached_output = []

            def follow_output(path, *args, **kwargs):
                if path == target:
                    reached_output.append(path)
                    path = path.resolve()
                return original_open(path, *args, **kwargs)

            with mock.patch.object(Path, "open", follow_output):
                with self.assertRaises(FileExistsError):
                    archive.write_new(target, {"synthetic": True})
            self.assertEqual(reached_output, [])
            self.assertFalse(absent.exists())
            self.assertTrue(target.is_symlink())


class PublishedArchiveTests(unittest.TestCase):
    def test_frozen_inputs_and_pinned_common_guides(self):
        freeze = archive.verify_freeze()
        self.assertEqual(len(freeze["inputs"]), 16)
        self.assertEqual(freeze["seed"], 20261013)
        self.assertEqual(freeze["passes"], ["initial", "one edit"])
        for unit, identifiers in freeze["selected_records"].items():
            self.assertEqual(len(identifiers), 4)
            selected = archive.read(archive.ROOT / "guides/selected-ai-records.json")
            self.assertEqual(identifiers, [e["id"] for e in selected["units"][unit]])

    def test_anonymous_packets_and_reversal_equal_frozen_seed(self):
        canonical, reverse, mapping = archive.blind_data()
        self.assertEqual(archive.read(archive.ROOT / "mapping.json"), mapping)
        self.assertEqual(archive.read(archive.ROOT / "blind/reader.json"), canonical)
        self.assertEqual(archive.read(archive.ROOT / "blind/J01.json"), canonical)
        self.assertEqual(archive.read(archive.ROOT / "blind/J02.json"), reverse)
        self.assertEqual(len(canonical["pairs"]), 12)
        for row in canonical["pairs"]:
            self.assertEqual(set(row), {"id", "paper", "sample", "unit", "A", "B"})

    def test_all_decoded_views_equal_original_completion_strings(self):
        names = [f"W{i:02d}_{phase}" for i in range(1, 5) for phase in ("initial", "final")]
        names += ["J01", "J02", "T01", "T02", "F01"]
        for name in names:
            response = archive.read(archive.ROOT / "responses" / f"{name}.json")
            self.assertEqual(json.loads(response["completion"]), archive.read(archive.ROOT / "raw" / f"{name}.json"))

    def test_saved_summary_and_html_are_derived_not_authored_outcomes(self):
        summary, counts, reviews = archive.analyze()
        self.assertEqual(archive.read(archive.ROOT / "summary.json"), summary)
        self.assertEqual(archive.read(archive.ROOT / "word_counts.json"), counts)
        self.assertEqual(archive.read(archive.ROOT / "normalized_reviews.json"), reviews)
        self.assertEqual((archive.ROOT / "comparison.html").read_text(encoding="utf-8"), archive.render())
        self.assertFalse(summary["gate"]["automatic_runtime_promotion"])

    def test_public_archive_excludes_full_source_pdfs(self):
        self.assertFalse(list(archive.ROOT.rglob("*.pdf")))
        self.assertFalse(list(archive.ROOT.rglob("*.zip")))

    def test_published_experimental_bytes_match_receipts(self):
        self.assertEqual(archive.read(archive.ROOT / "receipts.json"), archive.artifact_receipts())


if __name__ == "__main__":
    unittest.main()
