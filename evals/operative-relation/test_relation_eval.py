"""Synthetic infrastructure checks, not semantic model judgments."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import relation_eval as relation


class RelationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        original = relation.ROOT
        self.patch = patch.object(relation, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        (self.root / "relation_eval.py").write_bytes((original / "relation_eval.py").read_bytes())
        papers = [{"id": f"N{n}", "title": f"Fixture {n}"} for n in (1, 2)]
        relation.write("papers.json", papers)
        relation.write("guide_hashes.json", {})
        for p in papers:
            pid = p["id"]
            meta = {"id": pid, "title": p["title"], "source_paths": {
                "pdf": f"sources/{pid}.pdf", "extracted": f"sources/{pid}.raw.txt",
                "body": f"inputs/{pid}.txt", "recipe": f"sources/{pid}.extract.py"}, "hashes": {}}
            for name, key in ((f"sources/{pid}.pdf", "pdf"), (f"sources/{pid}.raw.txt", "extracted"),
                              (f"inputs/{pid}.txt", "body")):
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture bytes, not a real paper")
                meta["hashes"][key] = hashlib.sha256(path.read_bytes()).hexdigest()
            (self.root / f"sources/{pid}.extract.py").write_text("# synthetic fixture\n")
            relation.write(f"metadata/{pid}.json", meta)
            relation.write(f"anchors/{pid}.json", {"units": {u: {"question": f"question {u}"} for u in relation.UNITS}})

    def complete(self):
        relation.initial()
        for p in relation.read("papers.json"):
            pid = p["id"]
            for sample in (1, 2):
                for c in ("initial", "baseline", "candidate"):
                    case = {"id": pid, "notes": "fixture", **{u: "word " * low for u, (low, high) in relation.UNITS.items()}}
                    relation.write(f"raw/{c}_{pid}_{sample}.json", case)
        relation.editors()
        relation.assessments()
        m = relation.read("mapping.json")
        for p in relation.read("papers.json"):
            pid = p["id"]
            pairs = [k for k in m if k["paper"] == pid]
            for n in (1, 2):
                relation.write(f"raw/review_{pid}_{n}.json", {"reviews": [{"id": k["id"], "preferred": "Tie",
                    "A": {"fidelity": "pass", "argument": 4, "language": 4}, "B": {"fidelity": "pass", "argument": 4, "language": 4},
                    "reason": "fixture"} for k in pairs]})
                relation.write(f"raw/reader_{pid}_{n}.json", {"readings": [{"id": k[f"reader_{n}"]["id"],
                    "core": "fixture", "scope": "fixture", "core_witness": "word", "scope_witness": "", "unclear": "none"} for k in pairs]})
        relation.audits()
        for p in relation.read("papers.json"):
            pid = p["id"]
            rows = relation.read(f"packets/audit_{pid}.json")
            for n in (1, 2):
                relation.write(f"raw/audit_{pid}_{n}.json", {"audits": [{"id": r["id"], "fidelity": "pass",
                    "critical_support": "supported", "reader_support": "text_grounded", "reason": "fixture"} for r in rows]})

    def test_full_counts_and_ties_are_retained(self):
        self.complete()
        with contextlib.redirect_stdout(io.StringIO()):
            relation.analyze()
        s = relation.read("summary.json")
        self.assertEqual(s["votes"], {"tie": 24})
        self.assertEqual(s["pair_outcomes"], {"unanimous_tie": 12})
        self.assertEqual(s["completed"]["source_audit_judgments"], 48)
        self.assertEqual(len(relation.read("all_raw_hashes.json")), 24)

    def test_source_identity_cannot_silently_change(self):
        path = self.root / "metadata/N1.json"
        m = json.loads(path.read_text())
        m["title"] = "wrong paper"
        path.write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            relation.initial()

    def test_reversed_pairs_and_reader_counterpart_separation(self):
        self.complete()
        for pid in ("N1", "N2"):
            one, two = (relation.read(f"packets/review_{pid}_{n}.json") for n in (1, 2))
            for a, b in zip(one, two, strict=True):
                self.assertEqual(a["A"], b["B"])
                self.assertEqual(a["B"], b["A"])
            for n in (1, 2):
                selected = [m for m in relation.read("mapping.json") if m["paper"] == pid]
                self.assertEqual(len({m[f"reader_{n}"]["id"] for m in selected}), 6)
                self.assertEqual(sum(m[f"reader_{n}"]["condition"] == "candidate" for m in selected), 3)

    def test_missing_response_prevents_unblinding(self):
        self.complete()
        (self.root / "raw/audit_N2_2.json").unlink()
        with self.assertRaisesRegex(ValueError, "no unblinding"):
            relation.analyze()

    def test_task_objective_drift_is_detected(self):
        self.complete()
        p = self.root / "requests/N1.json"
        p.write_text(p.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "drift"):
            relation.analyze()

    def test_duplicate_ids_fail_closed(self):
        with self.assertRaises(ValueError):
            relation.exact([{"id": "x"}, {"id": "x"}], ["x", "y"])

    def test_alternate_metadata_paths_preserve_original_bytes(self):
        path = self.root / "metadata/N2.json"
        meta = json.loads(path.read_text())
        source = meta.pop("source_paths")
        meta["paths"] = {"original_pdf": source["pdf"], "original_raw_extraction": source["extracted"],
                         "body": source["body"], "recipe": source["recipe"]}
        path.write_text(json.dumps(meta))
        relation.initial()
        self.assertIn("sources/N2.raw.txt", relation.read("source_hashes.json"))
        self.assertFalse((self.root / "sources/N2.extracted.txt").exists())

    def test_unhashed_writer_body_cannot_be_substituted(self):
        meta = relation.read("metadata/N1.json")
        meta["source_paths"]["body"] = "other.txt"
        with self.assertRaisesRegex(ValueError, "differs from hashed body"):
            relation.source_artifacts(meta, "N1")

    def test_source_hash_mismatch_fails_closed(self):
        (self.root / "sources/N1.raw.txt").write_text("changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            relation.initial()

    def test_output_is_not_repaired_or_overwritten(self):
        relation.write("one.json", {"value": 1})
        with self.assertRaises(FileExistsError):
            relation.write("one.json", {"value": 2})
        self.assertEqual(relation.read("one.json"), {"value": 1})


if __name__ == "__main__":
    unittest.main()
