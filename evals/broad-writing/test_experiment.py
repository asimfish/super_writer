import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


spec = importlib.util.spec_from_file_location("experiment", Path(__file__).with_name("experiment.py"))
experiment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(experiment)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.old_root = experiment.ROOT
        experiment.ROOT = Path(self.temp.name)
        self.addCleanup(setattr, experiment, "ROOT", self.old_root)
        for folder in ("raw", "packets"):
            (experiment.ROOT / folder).mkdir()
        self.domains = [{"id": "D1", "domain": "fixture", "papers":
                         [["P01", "one", "https://example.com/1"],
                          ["P02", "two", "https://example.com/2"]]}]
        experiment.write("domains.json", self.domains)
        for sample in range(1, 4):
            for condition in ("initial", "baseline", "candidate"):
                experiment.write(f"raw/{condition}_D1_{sample}.json", {"cases": [
                    {"id": pid, "notes": "note", **{
                        unit: f"{condition} {pid} {sample} {unit} " + "word " * (low + 1)
                        for unit, (low, _) in experiment.UNITS.items()}}
                    for pid in ("P01", "P02")]})

    def test_immutable_write(self):
        with self.assertRaises(FileExistsError):
            experiment.write("domains.json", [])
        self.assertEqual(experiment.read("domains.json"), self.domains)

    def test_reversal_balance_and_counterpart_separation(self):
        experiment.packets()
        one = experiment.read("packets/review_D1_1.json")
        two = experiment.read("packets/review_D1_2.json")
        self.assertEqual(len(one), 18)
        for a, b in zip(one, two, strict=True):
            self.assertEqual(a["id"], b["id"])
            self.assertEqual(a["A"], b["B"])
            self.assertEqual(a["B"], b["A"])
        readers = experiment.read("private_reader_mapping.json")
        for number in (1, 2):
            subset = [r for r in readers if r["reader"] == number]
            self.assertEqual(len(subset), 18)
            self.assertEqual(sum(r["condition"] == "candidate" for r in subset), 9)
        for pair in one:
            found = [r for r in readers if r["pair"] == pair["id"]]
            self.assertEqual(len(found), 2)
            self.assertEqual({r["condition"] for r in found}, {"baseline", "candidate"})
            self.assertEqual({r["reader"] for r in found}, {1, 2})
        self.assertEqual(len(experiment.read("generation_hashes.json")), 9)
        self.assertEqual(len(experiment.read("word_counts.json")), 72)

    def test_duplicate_ids_fail_closed(self):
        path = experiment.ROOT / "raw/baseline_D1_1.json"
        data = json.loads(path.read_text())
        data["cases"][1]["id"] = "P01"
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            experiment.packets()

    def test_missing_field_fails_closed(self):
        path = experiment.ROOT / "raw/baseline_D1_1.json"
        data = json.loads(path.read_text())
        del data["cases"][0]["methods"]
        path.write_text(json.dumps(data))
        with self.assertRaises(KeyError):
            experiment.packets()


if __name__ == "__main__":
    unittest.main()
