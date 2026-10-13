"""Infrastructure-not-writing tests: every passage and judgment is synthetic."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PILOT_PATH = ROOT / "evals" / "ai-spec-pilot" / "pilot.py"
SPEC = importlib.util.spec_from_file_location("ai_spec_pilot", PILOT_PATH)
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


def words(count):
    return " ".join(["synthetic"] * count)


def writer(with_notes=True):
    cases = []
    for paper in ("R01", "R02"):
        case = {"id": paper, "abstract": words(150), "methods": words(110),
                "results": words(120)}
        if with_notes:
            case["notes"] = {unit: "Synthetic editorial note." for unit in pilot.UNITS}
        cases.append(case)
    return {"writer_id": "W01", "replicate": 1, "cases": cases}


def packet():
    return {"pairs": [
        {"id": f"{paper}_s{sample}_{unit}", "paper": paper, "sample": sample,
         "unit": unit, "A": "Synthetic passage A.", "B": "Synthetic passage B."}
        for paper in ("R01", "R02") for sample in (1, 2) for unit in pilot.UNITS
    ]}


def mapping():
    return {
        pair["id"]: ({"A": "candidate", "B": "baseline"} if index % 2 == 0
                     else {"A": "baseline", "B": "candidate"})
        for index, pair in enumerate(packet()["pairs"])
    }


def review(reviewer_id="J01", preferences=None):
    conditions = mapping()
    pairs = []
    for pair in packet()["pairs"]:
        preferred = (preferences or {}).get(pair["id"], "tie")
        if preferred != "tie":
            preferred = next(side for side, condition in conditions[pair["id"]].items()
                             if condition == preferred)
        pairs.append({
            "id": pair["id"], "preferred": preferred,
            "A": {dimension: 3 for dimension in pilot.DIMENSIONS},
            "B": {dimension: 4 for dimension in pilot.DIMENSIONS},
            "reason": "Synthetic infrastructure fixture, not a writing judgment.",
        })
    return {"reviewer_id": reviewer_id, "pairs": pairs}


def passing_reviews():
    preferences = {"R01_s1_abstract": "candidate", "R02_s1_methods": "candidate"}
    return [review("J01", preferences), review("J02", preferences)]


class WordCountTests(unittest.TestCase):
    def test_contract_regex_handles_hyphens_apostrophes_and_numbers(self):
        text = "It's model-based O\u2019Brien's R01 3.5 foo_bar -- \u4e2d\u6587"
        self.assertEqual(pilot.count_words(text), 8)
        self.assertEqual(pilot.count_words(" \n \t"), 0)

    def test_nonstring_count_is_rejected(self):
        for value in (None, 3, [], {}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                pilot.count_words(value)


class WriterValidationTests(unittest.TestCase):
    def test_valid_final_counts_and_no_mutation(self):
        data = writer()
        before = copy.deepcopy(data)
        result = pilot.validate_writer(data)
        self.assertEqual(result["phase"], "final")
        self.assertEqual(result["budget_violations"], [])
        self.assertEqual(result["word_counts"]["R01"]["abstract"], 150)
        self.assertEqual(result["word_counts"]["R02"]["notes"]["methods"], 3)
        self.assertEqual(data, before)

    def test_initial_omits_notes_and_ignores_all_budgets(self):
        data = writer(with_notes=False)
        data["cases"][0]["abstract"] = words(300)
        self.assertEqual(pilot.validate_writer(data, "initial")["budget_violations"], [])
        data["cases"][1]["notes"] = {unit: words(61) for unit in pilot.UNITS}
        self.assertEqual(pilot.validate_writer(data, "initial")["budget_violations"], [])
        with self.assertRaises(ValueError):
            pilot.validate_writer(data, "final")

    def test_each_budget_boundary_and_note_limit(self):
        for unit, (low, high) in pilot.BUDGETS.items():
            for count, expected in ((low - 1, 1), (low, 0), (high, 0), (high + 1, 1)):
                with self.subTest(unit=unit, count=count):
                    data = writer()
                    data["cases"][0][unit] = words(count)
                    self.assertEqual(len(pilot.validate_writer(data)["budget_violations"]),
                                     expected)
        for count, expected in ((60, 0), (61, 1)):
            data = writer()
            data["cases"][0]["notes"]["abstract"] = words(count)
            self.assertEqual(len(pilot.validate_writer(data)["budget_violations"]), expected)

    def test_budget_deviations_preserve_raw_text_and_are_located(self):
        data = writer()
        original = " \n" + words(191) + "\t "
        data["cases"][0]["abstract"] = original
        data["cases"][1]["methods"] = words(109)
        data["cases"][1]["notes"]["results"] = words(61)
        before = copy.deepcopy(data)
        violations = pilot.validate_writer(data)["budget_violations"]
        self.assertEqual(data, before)
        self.assertEqual(data["cases"][0]["abstract"], original)
        self.assertEqual([(v["paper"], v["field"], v["words"], v["min"], v["max"])
                          for v in violations],
                         [("R01", "abstract", 191, 150, 190),
                          ("R02", "methods", 109, 110, 150),
                          ("R02", "notes.results", 61, 0, 60)])
        self.assertTrue(all(v["writer_id"] == "W01" and v["sample"] == 1
                            and v["phase"] == "final" for v in violations))

    def test_missing_duplicate_and_unknown_papers_are_rejected(self):
        for ids in (("R01",), ("R01", "R01"), ("R01", "R99"), ("R01", "R02", "R03")):
            with self.subTest(ids=ids):
                data = writer()
                data["cases"] = [dict(copy.deepcopy(data["cases"][0]), id=paper)
                                 for paper in ids]
                with self.assertRaises(ValueError):
                    pilot.validate_writer(data)

    def test_schema_rejects_empty_nonstring_and_missing_fields(self):
        for unit in pilot.UNITS:
            for bad in ("", " \n ", None, 4, False, [], {}):
                for notes in (False, True):
                    with self.subTest(unit=unit, bad=bad, notes=notes):
                        data = writer()
                        target = data["cases"][0]["notes"] if notes else data["cases"][0]
                        target[unit] = bad
                        with self.assertRaises(ValueError):
                            pilot.validate_writer(data)
            for notes in (False, True):
                data = writer()
                target = data["cases"][0]["notes"] if notes else data["cases"][0]
                del target[unit]
                with self.assertRaises(ValueError):
                    pilot.validate_writer(data)

    def test_identity_phase_and_top_level_schema(self):
        for field, bad in (("writer_id", ""), ("writer_id", 1), ("replicate", True),
                           ("replicate", 1.0), ("replicate", 0), ("replicate", 3),
                           ("cases", {}), ("cases", None)):
            data = writer()
            data[field] = bad
            with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                pilot.validate_writer(data)
        for bad in (None, [], "writer"):
            with self.assertRaises(ValueError):
                pilot.validate_writer(bad)
        with self.assertRaises(ValueError):
            pilot.validate_writer(writer(), "draft")
        data = writer()
        data["extra"] = "not part of this schema"
        with self.assertRaises(ValueError):
            pilot.validate_writer(data)

    def test_second_replicate_and_reversed_paper_order_are_valid(self):
        data = writer()
        data["replicate"] = 2
        data["cases"].reverse()
        data["cases"][0]["results"] = words(161)
        result = pilot.validate_writer(data)
        self.assertEqual(result["budget_violations"][0]["paper"], "R02")
        self.assertEqual(result["budget_violations"][0]["sample"], 2)


class PairAndReviewValidationTests(unittest.TestCase):
    def setUp(self):
        self.meta = pilot.validate_pairs(packet())

    def test_complete_packet_returns_only_anonymous_metadata(self):
        self.assertEqual(len(self.meta), 12)
        self.assertEqual(self.meta["R01_s1_abstract"],
                         {"paper": "R01", "sample": 1, "unit": "abstract"})
        self.assertNotIn("A", self.meta["R01_s1_abstract"])
        original = review()
        before = copy.deepcopy(original)
        pilot.validate_review(original, self.meta)
        self.assertEqual(original, before)

    def test_packet_requires_unique_complete_known_ids_and_matching_metadata(self):
        mutations = (
            lambda p: p["pairs"].pop(),
            lambda p: p["pairs"].append(copy.deepcopy(p["pairs"][0])),
            lambda p: p["pairs"][0].update(id="R99_s1_abstract"),
            lambda p: p["pairs"][0].update(paper="R02"),
            lambda p: p["pairs"][0].update(sample=True),
            lambda p: p["pairs"][0].update(sample=1.0),
            lambda p: p["pairs"][0].update(sample=3),
            lambda p: p["pairs"][0].update(unit="discussion"),
            lambda p: p["pairs"][0].update(A=" "),
            lambda p: p["pairs"][0].update(B=None),
            lambda p: p["pairs"][0].pop("B"),
        )
        for mutate in mutations:
            data = packet()
            mutate(data)
            with self.subTest(data=data["pairs"][0]), self.assertRaises(ValueError):
                pilot.validate_pairs(data)

    def test_review_rejects_missing_duplicate_and_unknown_ids(self):
        for kind in ("missing", "duplicate", "replacement", "extra"):
            data = review()
            if kind == "missing":
                data["pairs"].pop()
            elif kind == "duplicate":
                data["pairs"][1]["id"] = data["pairs"][0]["id"]
            elif kind == "replacement":
                data["pairs"][0]["id"] = "R99_s1_abstract"
            else:
                data["pairs"].append(dict(data["pairs"][0], id="other-study"))
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                pilot.validate_review(data, self.meta)

    def test_scores_require_all_five_dimensions_and_exact_integer_range(self):
        for side in ("A", "B"):
            for dimension in pilot.DIMENSIONS:
                for bad in (True, False, 1.0, 5.0, "3", 0, 6, None, [], {}):
                    data = review()
                    data["pairs"][0][side][dimension] = bad
                    with self.subTest(side=side, dimension=dimension, bad=bad):
                        with self.assertRaises(ValueError):
                            pilot.validate_review(data, self.meta)
                data = review()
                del data["pairs"][0][side][dimension]
                with self.assertRaises(ValueError):
                    pilot.validate_review(data, self.meta)
            for valid in (1, 5):
                data = review()
                data["pairs"][0][side] = {d: valid for d in pilot.DIMENSIONS}
                pilot.validate_review(data, self.meta)

    def test_preference_reason_and_reviewer_schema(self):
        for field, bad in (("preferred", "candidate"), ("preferred", None),
                           ("reason", ""), ("reason", " \t"), ("reason", 3),
                           ("A", []), ("B", None)):
            data = review()
            data["pairs"][0][field] = bad
            with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                pilot.validate_review(data, self.meta)
        for bad in ("", " ", False, None):
            data = review()
            data["reviewer_id"] = bad
            with self.assertRaises(ValueError):
                pilot.validate_review(data, self.meta)
        for field in ("reviewer_id", "pairs"):
            data = review()
            del data[field]
            with self.assertRaises(ValueError):
                pilot.validate_review(data, self.meta)

    def test_malformed_containers_and_unknown_schema_fields_are_rejected(self):
        for validate, valid in ((pilot.validate_pairs, packet()),
                                (pilot.validate_review, review())):
            for bad in (None, [], "raw response"):
                with self.subTest(validate=validate.__name__, bad=bad):
                    with self.assertRaises(ValueError):
                        validate(bad)
            for pairs in (None, {}, [None], ["pair"]):
                data = copy.deepcopy(valid)
                data["pairs"] = pairs
                with self.assertRaises(ValueError):
                    validate(data)
            for target in ("top", "pair"):
                data = copy.deepcopy(valid)
                container = data if target == "top" else data["pairs"][0]
                container["other-study"] = "not allowed"
                with self.assertRaises(ValueError):
                    validate(data)
        data = review()
        data["pairs"][0]["A"]["other-score"] = 3
        with self.assertRaises(ValueError):
            pilot.validate_review(data)


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.meta = pilot.validate_pairs(packet())
        self.mapping = mapping()

    def summarize(self, reviews, **kwargs):
        return pilot.summarize(reviews, self.mapping, self.meta, **kwargs)

    def test_ties_do_not_count_as_candidate_wins(self):
        result = self.summarize([review("J01"), review("J02")])
        self.assertEqual(result["overall"]["votes"],
                         {"baseline": 0, "candidate": 0, "tie": 24})
        self.assertEqual(result["overall"]["candidate_minus_baseline"], 0)
        self.assertEqual(len(result["overall"]["unanimous"]["tie"]), 12)
        self.assertEqual(result["overall"]["disagreements"], [])
        self.assertFalse(result["gate"]["passed"])
        self.assertEqual(len(result["gate"]["reasons"]), 3)

    def test_unblinding_group_totals_unanimity_and_disagreement(self):
        first = review("J01", {"R01_s1_abstract": "candidate",
                               "R02_s1_methods": "candidate",
                               "R01_s1_results": "baseline"})
        second = review("J02", {"R01_s1_abstract": "candidate",
                                "R02_s1_methods": "baseline"})
        result = self.summarize([second, first])
        self.assertEqual(result["reviewer_ids"], ["J01", "J02"])
        self.assertEqual(result["overall"]["votes"],
                         {"baseline": 2, "candidate": 3, "tie": 19})
        self.assertEqual(result["overall"]["candidate_minus_baseline"], 1)
        self.assertEqual(result["per_unit"]["abstract"]["candidate_minus_baseline"], 2)
        self.assertEqual(result["per_unit"]["methods"]["candidate_minus_baseline"], 0)
        self.assertEqual(result["per_paper"]["R01"]["votes"],
                         {"baseline": 1, "candidate": 2, "tie": 9})
        self.assertEqual(result["overall"]["unanimous"]["candidate"],
                         ["R01_s1_abstract"])
        self.assertEqual(result["overall"]["disagreements"],
                         ["R01_s1_results", "R02_s1_methods"])
        self.assertEqual(result["pairs"]["R02_s1_methods"]["preferences"],
                         {"J01": "candidate", "J02": "baseline"})
        self.assertEqual(result["pairs"]["R01_s1_results"]["outcome"], "disagreement")
        for grouping in ("per_unit", "per_paper"):
            for condition in ("baseline", "candidate", "tie"):
                self.assertEqual(sum(bucket["votes"][condition]
                                     for bucket in result[grouping].values()),
                                 result["overall"]["votes"][condition])

    def test_gate_pass_requires_cross_paper_support_and_never_promotes(self):
        result = self.summarize(passing_reviews())
        self.assertTrue(result["gate"]["passed"])
        self.assertTrue(all(result["gate"]["criteria"].values()))
        self.assertFalse(result["gate"]["automatic_runtime_promotion"])
        self.assertEqual(result["scope"], "ai-spec-pilot-only")
        self.assertTrue(any("correlated" in limit for limit in result["limits"]))
        self.assertTrue(any("further validation" in reason
                            for reason in result["gate"]["reasons"]))

    def test_two_unanimous_pairs_on_one_paper_cannot_pass(self):
        preferences = {"R01_s1_abstract": "candidate", "R01_s1_methods": "candidate"}
        result = self.summarize([review("J01", preferences), review("J02", preferences)])
        self.assertEqual(len(result["overall"]["unanimous"]["candidate"]), 2)
        self.assertFalse(result["gate"]["passed"])
        self.assertFalse(result["gate"]["criteria"]["unanimous_candidate_across_papers"])
        self.assertEqual(len(result["gate"]["reasons"]), 1)

    def test_abstract_and_methods_must_both_have_positive_net_votes(self):
        for bad_unit in ("abstract", "methods"):
            preferences = {"R01_s1_results": "candidate", "R02_s1_results": "candidate",
                           "R01_s1_abstract": "candidate", "R02_s1_methods": "candidate"}
            preferences[f"R01_s1_{bad_unit}"] = "baseline"
            preferences[f"R02_s1_{bad_unit}"] = "baseline"
            result = self.summarize([review("J01", preferences), review("J02", preferences)])
            with self.subTest(unit=bad_unit):
                self.assertFalse(result["gate"]["passed"])
                self.assertFalse(result["gate"]["criteria"][f"{bad_unit}_net_positive"])

    def test_one_unanimous_pair_and_other_disagreements_cannot_pass(self):
        first = review("J01", {"R01_s1_abstract": "candidate", "R02_s1_methods": "candidate"})
        second = review("J02", {"R01_s1_abstract": "candidate"})
        result = self.summarize([first, second])
        self.assertGreater(result["per_unit"]["methods"]["candidate_minus_baseline"], 0)
        self.assertFalse(result["gate"]["passed"])

    def test_consequential_failures_and_either_conditions_budgets_block_gate(self):
        for condition in ("baseline", "candidate"):
            diagnostics = pilot.validate_writer(writer())
            raw = writer()
            raw["cases"][0]["notes"]["abstract"] = words(61)
            violations = pilot.validate_writer(raw)["budget_violations"]
            violations[0]["condition"] = condition
            before = copy.deepcopy(violations)
            result = self.summarize(passing_reviews(), budget_violations=violations)
            self.assertFalse(result["gate"]["passed"])
            self.assertEqual(result["budget_violations"], before)
            self.assertEqual(violations, before)
            self.assertFalse(result["gate"]["criteria"]["no_final_budget_deviations"])
            self.assertEqual(diagnostics["budget_violations"], [])
        failures = [{"paper": "R02", "unit": "methods", "reason": "Synthetic failure."}]
        result = self.summarize(passing_reviews(), consequential_candidate_failures=failures)
        self.assertFalse(result["gate"]["passed"])
        self.assertEqual(result["consequential_candidate_failures"], failures)

    def test_exactly_two_unique_reviewer_ids_required(self):
        for reviews in ([], [review()], [review(), review()],
                        [review("J01"), review("J02"), review("J03")],
                        [review("J01"), review(" J01 ")]):
            with self.subTest(count=len(reviews)), self.assertRaises(ValueError):
                self.summarize(reviews)

    def test_mapping_and_metadata_cannot_pool_unknown_studies_or_omit_pairs(self):
        for kind in ("missing", "extra", "duplicate-condition", "unknown-condition", "extra-side"):
            conditions = copy.deepcopy(self.mapping)
            if kind == "missing":
                conditions.pop("R01_s1_abstract")
            elif kind == "extra":
                conditions["old-study"] = {"A": "baseline", "B": "candidate"}
            elif kind == "duplicate-condition":
                conditions["R01_s1_abstract"]["B"] = conditions["R01_s1_abstract"]["A"]
            elif kind == "unknown-condition":
                conditions["R01_s1_abstract"]["B"] = "previous-study"
            else:
                conditions["R01_s1_abstract"]["C"] = "baseline"
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                pilot.summarize(passing_reviews(), conditions, self.meta)
        for kind in ("missing", "extra", "mismatch"):
            meta = copy.deepcopy(self.meta)
            if kind == "missing":
                meta.pop("R01_s1_abstract")
            elif kind == "extra":
                meta["old-study"] = {"paper": "R99", "sample": 1, "unit": "abstract"}
            else:
                meta["R01_s1_abstract"]["paper"] = "R02"
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                pilot.summarize(passing_reviews(), self.mapping, meta)

    def test_summary_revalidates_reviews_and_preserves_inputs(self):
        reviews = passing_reviews()
        before = copy.deepcopy((reviews, self.mapping, self.meta))
        self.summarize(reviews)
        self.assertEqual((reviews, self.mapping, self.meta), before)
        reviews[0]["pairs"][0]["id"] = "unknown"
        with self.assertRaises(ValueError):
            self.summarize(reviews)

    def test_all_nine_pairwise_preferences_and_vote_conservation(self):
        for first in ("baseline", "candidate", "tie"):
            for second in ("baseline", "candidate", "tie"):
                with self.subTest(first=first, second=second):
                    identifier = "R02_s2_methods"
                    result = self.summarize([review("J01", {identifier: first}),
                                             review("J02", {identifier: second})])
                    pair = result["pairs"][identifier]
                    self.assertEqual(pair["votes"], {
                        condition: (int(first == condition) + int(second == condition))
                        for condition in ("baseline", "candidate", "tie")})
                    self.assertEqual(pair["outcome"], first if first == second else "disagreement")
                    self.assertEqual(sum(result["overall"]["votes"].values()), 24)
                    self.assertEqual(sum(len(ids) for ids in result["overall"]["unanimous"].values())
                                     + len(result["overall"]["disagreements"]), 12)
                    if first == second:
                        self.assertIn(identifier, result["per_unit"]["methods"]["unanimous"][first])
                    else:
                        self.assertIn(identifier, result["per_paper"]["R02"]["disagreements"])

    def test_input_order_does_not_change_summary(self):
        reviews = passing_reviews()
        expected = self.summarize(reviews)
        for data in reviews:
            data["pairs"].reverse()
        reviews.reverse()
        reversed_mapping = dict(reversed(list(self.mapping.items())))
        reversed_meta = dict(reversed(list(self.meta.items())))
        self.assertEqual(pilot.summarize(reviews, reversed_mapping, reversed_meta), expected)

    def test_malformed_audit_records_are_not_silently_treated_as_empty(self):
        for field in ("budget_violations", "consequential_candidate_failures"):
            for value in (False, 0, "", {}, ()):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    self.summarize(passing_reviews(), **{field: value})

    def test_full_pair_metadata_and_invalid_metadata_containers(self):
        full_meta = {pair["id"]: pair for pair in packet()["pairs"]}
        self.assertEqual(pilot.summarize(passing_reviews(), self.mapping, full_meta),
                         self.summarize(passing_reviews()))
        for bad in (None, [], "metadata"):
            with self.assertRaises(ValueError):
                pilot.summarize(passing_reviews(), self.mapping, bad)
        for field, value in (("id", "conflicting-id"), ("sample", True),
                             ("unit", None), ("paper", ""), ("A", None)):
            meta = copy.deepcopy(full_meta)
            meta["R01_s1_abstract"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                pilot.summarize(passing_reviews(), self.mapping, meta)


class CLITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-spec-infrastructure-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write_json(self, name, data):
        path = self.root / name
        with path.open("x", encoding="utf-8") as stream:
            json.dump(data, stream)
        return path

    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, "-B", str(PILOT_PATH), *map(str, arguments)],
                              capture_output=True, text=True, timeout=10, cwd=self.root)

    def summary_arguments(self, reviews=None):
        reviews = passing_reviews() if reviews is None else reviews
        review_paths = [self.write_json(f"review-{index}.json", data)
                        for index, data in enumerate(reviews)]
        return ["--reviews", *review_paths, "--mapping", self.write_json("mapping.json", mapping()),
                "--pairs", self.write_json("pairs.json", packet())]

    def test_writer_stdout_and_initial_mode(self):
        path = self.write_json("writer.json", writer())
        result = self.run_cli("--writer", path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["budget_violations"], [])
        initial = self.write_json("initial.json", writer(with_notes=False))
        result = self.run_cli("--writer", initial, "--phase", "initial")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["phase"], "initial")

    def test_writer_budget_violation_succeeds_and_preserves_source_bytes(self):
        data = writer()
        data["cases"][0]["results"] = words(161)
        path = self.write_json("writer.json", data)
        before = path.read_bytes()
        result = self.run_cli("--writer", path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["budget_violations"]), 1)
        self.assertEqual(path.read_bytes(), before)

    def test_summary_cli_uses_only_supplied_synthetic_inputs(self):
        arguments = self.summary_arguments()
        output = self.root / "summary.json"
        result = self.run_cli(*arguments, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(output.read_text(encoding="utf-8"))
        self.assertTrue(summary["gate"]["passed"])
        self.assertFalse(summary["gate"]["automatic_runtime_promotion"])
        self.assertEqual(summary["pair_count"], 12)

    def test_cli_supplied_budget_and_failure_records_block_gate(self):
        arguments = self.summary_arguments()
        violations = self.write_json("budgets.json", [{"condition": "baseline", "words": 191}])
        failures = self.write_json("failures.json", [{"reason": "Synthetic failure."}])
        result = self.run_cli(*arguments, "--budget-violations", violations,
                              "--consequential-candidate-failures", failures)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertFalse(summary["gate"]["passed"])
        self.assertEqual(len(summary["gate"]["reasons"]), 2)

    def test_output_exclusive_and_does_not_overwrite_input_or_existing_summary(self):
        path = self.write_json("writer.json", writer())
        existing = self.write_json("existing.json", {"keep": "unchanged"})
        for output in (path, existing):
            before = output.read_bytes()
            result = self.run_cli("--writer", path, "--output", output)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), before)

    def test_exclusive_output_rejects_dangling_symlink(self):
        path = self.write_json("writer.json", writer())
        target = self.root / "target.json"
        try:
            target.symlink_to(self.root / "absent.json")
        except (OSError, NotImplementedError):
            if sys.platform == "win32":
                self.skipTest("Windows symlink creation requires an enabled privilege.")
            raise
        result = self.run_cli("--writer", path, "--output", target)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "absent.json").exists())

    def test_cli_gate_failure_is_reported_not_a_schema_error(self):
        result = self.run_cli(*self.summary_arguments([review("J01"), review("J02")]))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["gate"]["passed"])

    def test_invalid_inputs_do_not_create_output(self):
        for name, raw in (("malformed", "{bad"), ("duplicate-key", '{"writer_id":"W01","writer_id":"W02"}'),
                          ("nonfinite", '{"value":NaN}')):
            path = self.root / f"{name}.json"
            with path.open("x", encoding="utf-8") as stream:
                stream.write(raw)
            output = self.root / f"{name}-output.json"
            result = self.run_cli("--writer", path, "--output", output)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            self.assertNotIn("Traceback", result.stderr)
        arguments = self.summary_arguments([review("J01"), review("J01")])
        output = self.root / "invalid-review-output.json"
        result = self.run_cli(*arguments, "--output", output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_cli_missing_paths_and_incomplete_or_mixed_modes_are_rejected(self):
        path = self.write_json("writer.json", writer())
        for arguments in ([], ["--writer", self.root / "missing.json"],
                          ["--reviews", path], ["--writer", path, "--reviews", path],
                          ["--writer", path, "--mapping", path],
                          ["--writer", path, "--phase", "draft"]):
            with self.subTest(arguments=arguments):
                result = self.run_cli(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)

    def test_cli_unknown_review_id_and_invalid_utf8_do_not_create_output(self):
        reviews = passing_reviews()
        reviews[0]["pairs"][0]["id"] = "other-study"
        output = self.root / "summary.json"
        result = self.run_cli(*self.summary_arguments(reviews), "--output", output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())
        path = self.root / "invalid-utf8.json"
        with path.open("xb") as stream:
            stream.write(b"\xff")
        result = self.run_cli("--writer", path, "--output", output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
