"""Synthetic contract tests, never scientific evaluation outcomes."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import abstract_eval as ev


class TransferTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = ev.ROOT
        ev.ROOT = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(setattr, ev, "ROOT", self.old)
        self.papers = [{"id": f"A{i:02d}", "title": f"Synthetic paper {i}",
                        "group": f"G{(i + 1) // 2}"} for i in range(1, 7)]
        ev.write("papers.json", self.papers)
        (ev.ROOT / "abstract_eval.py").write_bytes(Path(ev.__file__).read_bytes())
        ev.write("guide_hashes.json", {})
        for p in self.papers:
            pid = p["id"]
            paths = {"pdf": f"sources/{pid}.pdf", "extracted": f"sources/{pid}.raw.txt",
                     "body": f"inputs/{pid}.txt", "recipe": f"sources/{pid}.extract.py"}
            for role, name in paths.items():
                path = ev.ROOT / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"source evidence" if role in {"extracted", "body"} else b"fixture")
            ev.write(f"metadata/{pid}.json", {**p, "blocker": None, "paths": paths,
                "hashes": {role: ev.sha(name) for role, name in paths.items()},
                "body_separator": "two LF bytes", "segments": [{"order": 1,
                    "raw_start_byte": 0, "raw_end_byte": 15, "body_start_byte": 0,
                    "body_end_byte": 15, "sha256": hashlib.sha256(b"source evidence").hexdigest()}]})
            ev.write(f"anchors/{pid}.json", {"id": pid, "critical_question": "What operation enables the contribution?",
                "source_locator": "Synthetic methods", "expected_relation": "A synthetic relation."})

    def replace(self, name, obj):
        (ev.ROOT / name).write_text(json.dumps(obj))

    def generated(self):
        ev.initial()
        for task in ev.read("tasks.initial.json"):
            rows = [{"id": p["id"], "abstract": " ".join(["evidence"] * 160), "notes": "fixture"}
                    for p in self.papers if p["group"] == task["group"]]
            ev.write(task["output"], {"cases": rows})
        ev.editors()
        for task in ev.read("tasks.editors.json"):
            rows = ev.read(f"raw/initial_{task['group']}_{task['sample']}.json")
            ev.write(task["output"], rows)

    def assessed(self, winner="tie", concern=False, fail=False, boolean=False, overage=False):
        self.generated()
        if overage:
            name = "raw/candidate_G1_1.json"
            obj = ev.read(name)
            obj["cases"][0]["abstract"] = " ".join(["evidence"] * 201)
            self.replace(name, obj)
        ev.assessments()
        mapping = ev.read("mapping.json")
        for task in ev.read("tasks.assessments.json"):
            packet = ev.read(f"packets/{task['phase']}_{task['group']}_{task['number']}.json")
            if task["phase"] == "reader":
                obj = {"readings": [{"id": r["id"], "core": "fixture", "scope": "fixture",
                         "core_witness": "evidence", "scope_witness": "", "unclear": "none"} for r in packet]}
            else:
                rows = []
                for r in packet:
                    m = next(m for m in mapping if m["id"] == r["id"])
                    labels = m[f"reviewer_{task['number']}"]
                    pref = "Tie" if winner == "tie" else next(k for k, c in labels.items() if c == winner)
                    rows.append({"id": r["id"], "preferred": pref, **{k: {"fidelity": "fail" if c == "candidate" and fail else "concern" if c == "candidate" and concern else "pass",
                        "argument": True if boolean else 4, "language": 4} for k, c in labels.items()}, "reason": "fixture"})
                obj = {"reviews": rows}
            ev.write(task["output"], obj)
        ev.audits()
        for task in ev.read("tasks.audits.json"):
            packet = ev.read(f"packets/audit_{task['group']}.json")
            ev.write(task["output"], {"audits": [{"id": r["id"], "fidelity": "pass", "critical_support": "supported",
                "reader_support": "text_grounded", "reason": "fixture"} for r in packet]})

    def analyze(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ev.analyze()
        return ev.read("summary.json")

    def test_ties_have_full_counts_and_no_advancement(self):
        self.assessed()
        result = self.analyze()
        self.assertEqual(result["votes"], {"tie": 24})
        self.assertEqual(result["completed"]["source_audit_judgments"], 48)
        self.assertFalse(result["continuation_gate"]["eligible_for_further_abstract_validation"])

    def test_candidate_unanimity_can_pass_operational_gate(self):
        self.assessed("candidate")
        self.assertTrue(self.analyze()["continuation_gate"]["eligible_for_further_abstract_validation"])

    def test_anonymity_reversal_balance_and_no_writer_questions(self):
        self.generated()
        ev.assessments()
        mapping = ev.read("mapping.json")
        for m in mapping:
            self.assertEqual(m["reviewer_1"]["A"], m["reviewer_2"]["B"])
            self.assertNotEqual(m["reader_1"]["condition"], m["reader_2"]["condition"])
        for g in ev.groups():
            for n in (1, 2):
                assigned = [m[f"reader_{n}"]["condition"] for m in mapping if m["group"] == g]
                self.assertEqual(assigned.count("candidate"), 2)
        for task in ev.read("tasks.initial.json") + ev.read("tasks.editors.json"):
            self.assertNotIn("What operation enables", task["message"])
            self.assertNotIn("Synthetic paper", task["message"])

    def test_duplicate_expected_ids_rejected(self):
        with self.assertRaises(ValueError):
            ev.exact([{"id": "a"}, {"id": "a"}], ["a", "a"])

    def test_source_bytes_drift_rejected(self):
        (ev.ROOT / "inputs/A01.txt").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            ev.initial()

    def test_source_span_receipt_rejected(self):
        meta = ev.read("metadata/A01.json")
        meta["segments"][0]["raw_end_byte"] = 14
        self.replace("metadata/A01.json", meta)
        with self.assertRaisesRegex(ValueError, "span changed"):
            ev.initial()

    def test_missing_assessment_never_unblinds(self):
        self.assessed()
        (ev.ROOT / "raw/audit_G3_2.json").unlink()
        with self.assertRaisesRegex(ValueError, "no unblinding"):
            self.analyze()
        self.assertFalse((ev.ROOT / "summary.json").exists())

    def test_question_drift_never_unblinds(self):
        self.assessed()
        (ev.ROOT / "anchors/A01.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Frozen artifact drift"):
            self.analyze()

    def test_new_fidelity_concern_blocks_candidate_wins(self):
        self.assessed("candidate", concern=True)
        result = self.analyze()["continuation_gate"]
        self.assertEqual(len(result["new_concerns"]), 24)
        self.assertFalse(result["eligible_for_further_abstract_validation"])

    def test_fidelity_failure_blocks_candidate_wins(self):
        self.assessed("candidate", fail=True)
        result = self.analyze()["continuation_gate"]
        self.assertEqual(result["candidate_fidelity_fail_labels"], 24)
        self.assertFalse(result["eligible_for_further_abstract_validation"])

    def test_opposite_sample_direction_blocks_gate(self):
        self.assessed("candidate")
        for g in ev.groups():
            for n in (1, 2):
                name = f"raw/review_{g}_{n}.json"
                obj = ev.read(name)
                for r in obj["reviews"]:
                    if r["id"].endswith("s2"):
                        r["preferred"] = "B" if r["preferred"] == "A" else "A"
                self.replace(name, obj)
        self.assertFalse(self.analyze()["continuation_gate"]["criteria"]["both_samples_net_candidate"])

    def test_candidate_overage_preserved_and_blocks_gate(self):
        self.assessed("candidate", overage=True)
        result = self.analyze()
        self.assertEqual(result["completed"]["pairs"], 12)
        self.assertEqual(len(result["generation_budget_violations"]), 1)
        self.assertFalse(result["continuation_gate"]["criteria"]["all_candidate_abstracts_within_budget"])
        self.assertFalse(result["continuation_gate"]["eligible_for_further_abstract_validation"])

    def test_bool_score_invalid_not_integer_one(self):
        self.assessed(boolean=True)
        with self.assertRaisesRegex(ValueError, "Invalid review rating"):
            self.analyze()

    def test_immutable_output(self):
        with self.assertRaises(FileExistsError):
            ev.write("papers.json", [])


if __name__ == "__main__":
    unittest.main()
