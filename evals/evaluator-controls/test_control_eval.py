import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import control_eval as control


class ControlTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.original = control.ROOT
        self.patcher = patch.object(control, "ROOT", self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def prepared(self):
        for name in ("cases.json", "PROTOCOL.md", "control_eval.py"):
            (self.root / name).write_bytes((self.original / name).read_bytes())
        control.write("fixture_review.final.json", {"cases": [{"id": c["id"], "valid": True}
                      for c in control.read("cases.json")["cases"]]})
        control.prepare()
        mapping = control.read("mapping.json")
        for n in range(1, 5):
            packet = control.read(f"packets/reader_{n}.json")
            control.write(f"raw/reader_{n}.json", {"readings": [{"id": p["id"], "core": "fixture",
                "scope": "fixture", "core_witness": "", "scope_witness": "", "unclear": "none"} for p in packet]})
        control.prepare_audits()
        cases = {c["id"]: c for c in control.read("cases.json")["cases"]}
        for n in (1, 2):
            rows = []
            for m in mapping["pairs"]:
                case = cases[m["case"]]
                winner = case["oracle"]["preferred"][0]
                key = m[f"reviewer_{n}"]
                rows.append({"id": m["id"], "preferred": "Tie" if winner == "tie" else
                    next(k for k, v in key.items() if v == winner),
                    "fidelity": {k: case["oracle"]["fidelity"][v][0] for k, v in key.items()}, "reason": "fixture"})
            control.write(f"raw/review_{n}.json", {"reviews": rows})
        for phase in ("coarse", "fine"):
            for n in (1, 2):
                rows = []
                for m in mapping["texts"]:
                    case = cases[m["case"]]
                    expected = case["oracle"]["support"][m["variant"]]
                    row = {"id": m["id"], "fidelity": case["oracle"]["fidelity"][m["variant"]][0], "reason": "fixture"}
                    if phase == "fine":
                        row.update(critical_support=expected, reader_support="text_grounded")
                    else:
                        row.update(core_recovery=2, scope_recovery=2)
                    rows.append(row)
                control.write(f"raw/{phase}_{n}.json", {"audits": rows})
        return mapping

    def test_invalid_expected_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            control.exact([{"id": "x"}, {"id": "x"}], ["x", "x"])

    def test_raw_duplicate_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            control.exact([{"id": "x"}, {"id": "x"}], ["x", "y"])

    def test_immutable_write(self):
        control.write("one.json", {"value": 1})
        with self.assertRaises(FileExistsError):
            control.write("one.json", {"value": 2})
        self.assertEqual(control.read("one.json"), {"value": 1})

    def test_balanced_packets_without_oracle_leakage(self):
        m = self.prepared()
        p1, p2 = (control.read(f"packets/review_{n}.json") for n in (1, 2))
        for a, b in zip(p1, p2, strict=True):
            self.assertEqual(a["A"], b["B"])
            self.assertEqual(a["B"], b["A"])
            self.assertNotIn("oracle", a)
            self.assertNotIn("category", a)
        for n in range(1, 5):
            selected = [t for t in m["texts"] if t["reader"] == n]
            self.assertEqual(len(selected), 6)
            self.assertEqual(len({t["case"] for t in selected}), 6)
            self.assertEqual(sum(t["variant"] == "v1" for t in selected), 3)
            for p in control.read(f"packets/reader_{n}.json"):
                self.assertEqual(set(p), {"id", "unit", "questions", "text"})

    def test_fine_pass_and_coarse_ceiling_are_reported_separately(self):
        self.prepared()
        with contextlib.redirect_stdout(io.StringIO()):
            control.analyze()
        s = control.read("summary.json")
        self.assertTrue(s["admission"]["pass"])
        self.assertEqual(s["completed"]["preference_votes"], 24)
        self.assertEqual(s["by_rubric"]["coarse"]["relation"]["defective_flagged"], 0)
        self.assertEqual(s["by_rubric"]["fine"]["relation"]["defective_flagged"], 6)

    def test_missing_review_prevents_unblinding(self):
        self.prepared()
        (self.root / "raw/review_2.json").unlink()
        with self.assertRaisesRegex(ValueError, "no unblinding"):
            control.analyze()
        self.assertFalse((self.root / "summary.json").exists())

    def test_drift_prevents_analysis(self):
        self.prepared()
        p = self.root / "raw/reader_1.json"
        p.write_text(p.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "drift"):
            control.analyze()

    def test_boolean_is_not_a_valid_coarse_score(self):
        self.assertFalse(control.valid_score(True))
        self.assertTrue(control.valid_score(2))

    def test_always_flagging_assessor_fails_specificity(self):
        self.prepared()
        for n in (1, 2):
            data = control.read(f"raw/fine_{n}.json")
            for r in data["audits"]:
                r["critical_support"] = "missing"
            (self.root / f"raw/fine_{n}.json").write_text(json.dumps(data))
        with contextlib.redirect_stdout(io.StringIO()):
            control.analyze()
        self.assertFalse(control.read("summary.json")["admission"]["pass"])

    def test_uncertain_does_not_count_as_defect_detection(self):
        self.prepared()
        for n in (1, 2):
            data = control.read(f"raw/fine_{n}.json")
            for r in data["audits"]:
                r["critical_support"] = "uncertain"
            (self.root / f"raw/fine_{n}.json").write_text(json.dumps(data))
        with contextlib.redirect_stdout(io.StringIO()):
            control.analyze()
        self.assertFalse(control.read("summary.json")["admission"]["pass"])


if __name__ == "__main__":
    unittest.main()
