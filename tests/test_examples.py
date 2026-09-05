"""Recompute public example numbers and exercise the shipped document artifacts."""

from __future__ import annotations

import csv
from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path
import statistics
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
spec = importlib.util.spec_from_file_location("toy_experiment", EXAMPLES / "knn-regression" / "experiment.py")
experiment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(experiment)
sys.path.insert(0, str(ROOT / "scripts"))
from _paper_spine_utils import markdown_tables


class ExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows, cls.summary = experiment.run()

    def test_public_csv_reproduces_per_seed_measurements(self) -> None:
        with (EXAMPLES / "knn-regression/materials/results.csv").open(encoding="utf-8", newline="") as stream:
            stored = list(csv.DictReader(stream))
        self.assertEqual(len(stored), 20)
        for expected, actual in zip(self.rows, stored):
            self.assertEqual((actual["seed"], actual["domain"], actual["k"]),
                             (str(expected["seed"]), expected["domain"], str(expected["k"])))
            self.assertAlmostEqual(float(actual["mse"]), expected["mse"], delta=1e-12)

    def test_public_summary_uses_seed_level_sample_standard_deviation(self) -> None:
        stored = json.loads((EXAMPLES / "knn-regression/materials/summary.json").read_text(encoding="utf-8"))
        self.assertEqual(stored["seeds"], list(experiment.SEEDS))
        for row in stored["results"]:
            values = [r["mse"] for r in self.rows if (r["domain"], r["k"]) == (row["domain"], row["k"])]
            mean = sum(values) / len(values)
            sd = (sum((value - mean) ** 2 for value in values) / (len(values) - 1)) ** 0.5
            self.assertAlmostEqual(row["mean_mse"], mean, delta=1e-12)
            self.assertAlmostEqual(row["sample_sd"], sd, delta=1e-12)

    def test_manuscript_table_matches_computed_rounding(self) -> None:
        manuscript = (EXAMPLES / "knn-regression/manuscript.md").read_text(encoding="utf-8")
        table = markdown_tables(manuscript)[0]
        self.assertEqual(len(table), 5)
        for actual, expected in zip(table[1:], self.summary["results"]):
            self.assertEqual(actual[0].lower().replace("-", "_"), expected["domain"])
            self.assertEqual(actual[1:], [str(expected["k"]), f"{expected['mean_mse']:.4f}", f"{expected['sample_sd']:.4f}"])

    def test_single_neighbor_and_full_neighborhood_have_direct_oracles(self) -> None:
        training = [(0.0, 2.0), (0.4, 6.0), (1.0, -2.0)]
        self.assertEqual(experiment.predict(training, 0.3, 1), 6.0)
        self.assertEqual(experiment.predict(training, 0.3, 3), statistics.mean([2.0, 6.0, -2.0]))

    def test_equal_distance_ties_use_training_order(self) -> None:
        self.assertEqual(experiment.predict([(0.0, 2.0), (1.0, 9.0)], 0.5, 1), 2.0)

    def test_invalid_neighbor_count_is_rejected(self) -> None:
        for k in (0, -1, 3):
            with self.subTest(k=k), self.assertRaises(ValueError):
                experiment.predict([(0.0, 2.0), (1.0, 9.0)], 0.5, k)

    def test_extrapolation_predictions_are_constant_for_a_fixed_training_set(self) -> None:
        training = [(0.0, 2.0), (0.3, 6.0), (0.7, -2.0)]
        for k in (1, 2, 3):
            values = [experiment.predict(training, x, k) for x in (1.0, 2.0, 10.0)]
            self.assertEqual(values, [values[0]] * 3)

    def test_rational_examples_obey_the_theory_note_range_bound(self) -> None:
        for values in itertools.product((-3, 0, 2), repeat=3):
            for numerators in itertools.product(range(3), repeat=3):
                total = sum(numerators)
                if total == 0:
                    continue
                average = sum(Fraction(w, total) * y for w, y in zip(numerators, values))
                self.assertLessEqual(min(values), average)
                self.assertLessEqual(average, max(values))

    def test_theory_note_counterexamples_do_not_support_accuracy_or_signed_weights(self) -> None:
        self.assertEqual(sum(w * y for w, y in zip((-1, 2), (0, 1))), 2)
        inaccurate_average = Fraction(1, 2) * 100 + Fraction(1, 2) * 100
        self.assertEqual((inaccurate_average - 0) ** 2, 10000)

    def test_shipped_examples_pass_real_latex_and_word_clis(self) -> None:
        for name, stem in (("knn-regression", "manuscript"), ("theory-note", "manuscript"),
                           ("review-response", "response")):
            directory = EXAMPLES / name
            for script, args in (
                ("latex_guard.py", [str(directory / f"{stem}.tex"), "--json"]),
                ("word_guard.py", [str(directory / f"{stem}.docx"), "--tex", str(directory / f"{stem}.tex"), "--json"]),
            ):
                with self.subTest(example=name, script=script):
                    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args],
                                            cwd=ROOT, capture_output=True, text=True, timeout=30)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_measured_values_survive_pdf_text_and_word_export(self) -> None:
        directory = EXAMPLES / "knn-regression"
        pdf_text = (directory / "manuscript.txt").read_text(encoding="utf-8")
        with zipfile.ZipFile(directory / "manuscript.docx") as archive:
            document = ET.fromstring(archive.read("word/document.xml"))
        word_text = " ".join(document.itertext())
        for row in self.summary["results"]:
            for value in (row["mean_mse"], row["sample_sd"]):
                token = f"{value:.4f}"
                self.assertIn(token, pdf_text)
                self.assertIn(token, word_text)


if __name__ == "__main__":
    unittest.main()
