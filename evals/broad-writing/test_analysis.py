import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


experiment = module("experiment")
analyze = module("analyze")


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        for mod in (experiment, analyze):
            original = mod.ROOT
            mod.ROOT = root
            self.addCleanup(setattr, mod, "ROOT", original)
        for folder in ("raw", "packets"):
            (root / folder).mkdir()
        domains = [{"id": f"D{n}", "domain": f"fixture{n}", "papers":
                    [[f"P{2*n-1:02d}", "one", "https://example.com/1"],
                     [f"P{2*n:02d}", "two", "https://example.com/2"]]} for n in range(1, 7)]
        experiment.write("domains.json", domains)
        experiment.write("frozen_hashes.json", {})
        experiment.write("source_hashes.json", {})
        experiment.write("initial_hashes.json", {})
        for domain in domains:
            did = domain["id"]
            ids = [p[0] for p in domain["papers"]]
            for sample in range(1, 4):
                for condition in ("initial", "baseline", "candidate"):
                    cases = [{"id": pid, "notes": "note", **{
                        unit: f"{condition} {pid} " + "word " * low
                        for unit, (low, _) in experiment.UNITS.items()}} for pid in ids]
                    if did == "D1" and sample == 1 and condition == "candidate":
                        cases[0]["results"] = "short"
                    experiment.write(f"raw/{condition}_{did}_{sample}.json", {"cases": cases})
        experiment.packets()
        self.maps = experiment.read("private_mapping.json")
        readers = experiment.read("private_reader_mapping.json")
        for domain in domains:
            did = domain["id"]
            pairs = [p for p in self.maps if p["domain"] == did]
            for reviewer in (1, 2):
                rows = [{"id": p["id"], "winner": next(label for label, c in
                          p[f"reviewer_{reviewer}"].items() if c == "candidate"),
                         "A": {"fidelity": "pass", **{k: 4 for k in analyze.SCORES}},
                         "B": {"fidelity": "pass", **{k: 4 for k in analyze.SCORES}},
                         "reason": "fixture"} for p in pairs]
                experiment.write(f"raw/review_{did}_{reviewer}.json", {"reviews": rows})
            domain_readers = [r for r in readers if r["domain"] == did]
            for reader in (1, 2):
                rows = [{"id": r["id"], "core_relation": "fixture", "scope": "fixture",
                         "witness": "word", "unclear": "none"} for r in domain_readers if r["reader"] == reader]
                experiment.write(f"raw/reader_{did}_{reader}.json", {"readings": rows})
            rows = [{"id": r["id"], "fidelity": "concern" if r["pair"] == "P01_s1_results"
                      and r["condition"] == "candidate" else "pass", "core_recovery": 2,
                     "scope_recovery": 2, "failure_types": ["none"], "reason": "fixture"}
                    for r in domain_readers]
            experiment.write(f"raw/audit_{did}.json", {"audits": rows})

    def test_full_counts_decoding_concerns_and_budget_sensitivity(self):
        with contextlib.redirect_stdout(io.StringIO()):
            analyze.main()
        result = experiment.read("summary.json")
        self.assertEqual(result["overall"]["votes"], {"candidate": 216})
        self.assertEqual(result["pair_outcomes"], {"unanimous_candidate": 108})
        self.assertEqual(result["overall"]["source_audit"]["candidate"], {"pass": 107, "concern": 1})
        self.assertEqual(len(result["source_concerned_unanimous_preferences"]), 1)
        self.assertEqual(result["budget_sensitivity"]["eligible_pairs"], 107)
        self.assertEqual(result["budget_sensitivity"]["votes"], {"candidate": 214})
        self.assertEqual(result["conditional_bootstrap"]["interval"], [1.0, 1.0])
        self.assertEqual(len(experiment.read("decoded_audits.json")), 216)

    def test_incomplete_assessment_blocks_unblinding(self):
        (experiment.ROOT / "raw/review_D6_2.json").unlink()
        with self.assertRaisesRegex(ValueError, "no unblinding"):
            analyze.main()
        self.assertFalse((experiment.ROOT / "summary.json").exists())

    def test_changed_raw_is_rejected(self):
        path = experiment.ROOT / "raw/candidate_D1_1.json"
        path.write_text(path.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "generation drift"):
            analyze.main()

    def test_invalid_boolean_rating_is_rejected(self):
        self.assertFalse(analyze.valid_score(True, 5))
        self.assertFalse(analyze.valid_score(6, 5))
        self.assertTrue(analyze.valid_score(2, 2))

    def test_duplicate_audit_is_rejected(self):
        path = experiment.ROOT / "raw/audit_D1.json"
        data = json.loads(path.read_text())
        data["audits"][1]["id"] = data["audits"][0]["id"]
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Incomplete/duplicate"):
            analyze.main()

    def test_supplementary_audits_do_not_replace_primary(self):
        with contextlib.redirect_stdout(io.StringIO()):
            analyze.main()
        compare = module("compare_audits")
        original = compare.ROOT
        compare.ROOT = experiment.ROOT
        self.addCleanup(setattr, compare, "ROOT", original)
        (experiment.ROOT / "supplemental").mkdir()
        for d in range(1, 7):
            data = experiment.read(f"raw/audit_D{d}.json")
            for row in data["audits"]:
                if row["fidelity"] == "concern":
                    row["fidelity"] = "pass"
            experiment.write(f"supplemental/audit_D{d}.json", data)
        with contextlib.redirect_stdout(io.StringIO()):
            compare.main()
        result = experiment.read("supplemental/summary.json")
        self.assertEqual(result["agreement"]["fidelity"], 215)
        self.assertEqual(result["primary"]["candidate"]["fidelity"].get("concern"), 1)
        self.assertEqual(result["text_only"]["candidate"]["fidelity"], {"pass": 108})
        self.assertEqual(len(result["differences"]), 1)
        self.assertEqual(experiment.read("summary.json")["overall"]["source_audit"]["candidate"].get("concern"), 1)

    def test_supplementary_missing_response_is_not_silently_dropped(self):
        compare = module("compare_audits")
        original = compare.ROOT
        compare.ROOT = experiment.ROOT
        self.addCleanup(setattr, compare, "ROOT", original)
        with self.assertRaisesRegex(ValueError, "incomplete"):
            compare.main()


if __name__ == "__main__":
    unittest.main()
