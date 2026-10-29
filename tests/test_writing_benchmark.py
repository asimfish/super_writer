"""Section benchmarking contracts; fixture judgments are authored, not model outcomes."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/writing-team"
SPEC = importlib.util.spec_from_file_location("benchmarked_loop", ROOT / "scripts/writing_loop.py")
LOOP = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(ROOT / "scripts"), *sys.path]):
    SPEC.loader.exec_module(LOOP)
BENCHMARK = LOOP.writing_benchmark


class WritingBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.run = json.loads((EXAMPLE / "benchmark-input.json").read_text(encoding="utf-8"))
        self.outputs = json.loads((EXAMPLE / "benchmark-responses.json").read_text(encoding="utf-8"))

    def advance(self, run, output=None):
        state = LOOP.inspect_run(run)
        role = state["packet"]["role"]
        return LOOP.append_response(run, {"role": role, "input_sha256": state["input_sha256"],
                                         "output": copy.deepcopy(output or self.outputs[role])})

    def through(self, count):
        run = self.run
        for _ in range(count):
            run = self.advance(run)
        return run

    def test_concise_fixture_preserves_strengths_and_traces_edits(self):
        gap = self.outputs["gap_finder"]
        self.assertEqual(gap["assessments"]["C5"]["status"], "meets")
        self.assertEqual(gap["selected_criteria"], ["C1", "C2", "C3"])
        self.assertEqual(set(self.outputs["writer"]["implementations"]), set(gap["selected_criteria"]))
        self.assertEqual(LOOP.inspect_run(self.through(4))["status"], "accepted_revision")
        self.assertLess(BENCHMARK.word_count(self.outputs["writer"]["text"]),
                        BENCHMARK.word_count(self.run["draft"]))
        self.assertNotIn("\n", self.outputs["writer"]["text"])

    def test_compression_budget_rejects_a_more_complete_but_longer_rewrite(self):
        out = copy.deepcopy(self.outputs["writer"])
        out["text"] += " The measured computational benefit concerns map updating rather than end-to-end navigation latency."
        out["compression"].update(original_words=44, revision_words=53, delta_words=9)
        with self.assertRaisesRegex(ValueError, "change in word count"):
            self.advance(self.through(2), out)

    def test_packet_contains_exact_complete_existing_resources(self):
        context = LOOP.inspect_run(self.run)["packet"]["input"]
        resources = context["writing_resources"]
        self.assertEqual(context["benchmark_basis"], "standards_and_exemplars")
        self.assertEqual(set(resources), {"abstract", "ai.rule.operation", "ai.rule.quantities",
                                         "general.sentence-pattern.quantify.001"})
        protocol = BENCHMARK.writing_guide.report_for(BENCHMARK.writing_guide.load_index(),
                                                     "abstract", "empirical-method")
        self.assertEqual(resources["abstract"], protocol)
        index = json.loads((ROOT / "references/ai-writing-spec.json").read_text(encoding="utf-8"))
        entry = next(x for x in index["entries"] if x["id"] == "ai.rule.operation")
        self.assertEqual(resources["ai.rule.operation"]["entries"], [entry])
        self.assertTrue(resources["ai.rule.operation"]["entries"][0]["exceptions"])
        # A local synthesis is allowed to have no paper source; never invent one.
        self.assertEqual(resources["ai.rule.operation"]["entries"][0]["source_notes"], entry["source_notes"])
        self.assertEqual(resources["ai.rule.operation"]["entries"][0]["source_ids"], entry["source_ids"])
        self.assertNotIn("benchmark-responses.json", json.dumps(context))

    def test_abstract_related_work_experiment_and_table_protocols_are_selectable(self):
        for section, protocol, variant in (
            ("abstract", "abstract", "theory"),
            ("related_work", "related_work", "taxonomy-first"),
            ("experiments", "experiments", "real-robot"),
            ("experiments", "experiments.analysis", "result-paragraph"),
            ("experiments", "experiments.table.main_results", "method-by-task"),
        ):
            run = copy.deepcopy(self.run)
            run["benchmark"].update(section=section, protocol=protocol, variant=variant)
            for criterion in run["benchmark"]["criteria"].values():
                criterion["resource_ids"] = [protocol]
            with self.subTest(protocol=protocol, variant=variant):
                packet = LOOP.inspect_run(run)["packet"]
                report = packet["input"]["writing_resources"][protocol]
                self.assertEqual(report["guide"]["section"], section)
                self.assertEqual([t["id"] for t in report["guide"]["templates"]], [variant])

    def test_invalid_resource_section_and_unbounded_selection_fail(self):
        for key, value in (("protocol", "../../private"), ("variant", "unknown"),
                           ("section", "related_work"), ("ai_spec_ids", ["unknown"]),
                           ("library_ids", ["unknown"]), ("ai_spec_ids", ["ai.rule.operation"] * 7),
                           ("ai_spec_ids", ["ai.rule.operation"] * 2)):
            run = copy.deepcopy(self.run)
            run["benchmark"][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                LOOP.inspect_run(run)

    def test_functional_sentence_card_reaches_existing_role_packet_unchanged(self):
        self.run["benchmark"]["ai_spec_ids"].append("ai.pattern.result-answer")
        self.run["benchmark"]["criteria"]["C1"]["resource_ids"].append("ai.pattern.result-answer")
        packet = LOOP.inspect_run(self.run)["packet"]["input"]
        card = packet["writing_resources"]["ai.pattern.result-answer"]["entries"][0]
        catalog = json.loads((ROOT / "references/ai-writing-spec.json").read_text())
        self.assertEqual(card, next(e for e in catalog["entries"] if e["id"] == card["id"]))
        self.assertIn("question", card["discourse"])
        self.assertTrue(card["evidence_required"])

    def test_target_answer_priority_and_compression_budget_are_required(self):
        for changes in (
            {"target_answer": ""},
            {"priority_criteria": []},
            {"priority_criteria": ["C1", "C2", "C3", "C4"]},
            {"budget": {**self.run["benchmark"]["budget"], "max_words": 0}},
            {"budget": {**self.run["benchmark"]["budget"], "max_delta_words": -1}},
            {"budget": {**self.run["benchmark"]["budget"], "unexpected": True}},
        ):
            run = copy.deepcopy(self.run)
            run["benchmark"].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                LOOP.inspect_run(run)

    def test_criteria_need_located_basis_and_valid_dimensions(self):
        for changes in ({"resource_ids": [], "source_ids": []}, {"resource_ids": ["unknown"]},
                        {"source_ids": ["unknown"]}, {"dimension": "paper_fame"},
                        {"expectation": ""}, {"applicability": ""}, {"oracle": "SECRET"}):
            run = copy.deepcopy(self.run)
            run["benchmark"]["criteria"]["C1"].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                LOOP.inspect_run(run)

    def test_assessments_must_cover_profile_without_fabricated_witnesses(self):
        for kind in ("missing", "extra", "bad_witness", "unknown_evidence"):
            out = copy.deepcopy(self.outputs["gap_finder"])
            if kind == "missing":
                del out["assessments"]["C6"]
            elif kind == "extra":
                out["assessments"]["fake"] = out["assessments"]["C1"]
            elif kind == "bad_witness":
                out["assessments"]["C1"]["draft_witness"] = "This sentence was never written."
            else:
                out["assessments"]["C1"]["evidence_ids"] = ["UNKNOWN"]
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.advance(self.run, out)

    def test_good_alternative_cannot_be_selected_as_a_defect(self):
        out = copy.deepcopy(self.outputs["gap_finder"])
        out["assessments"]["C1"]["status"] = "valid_alternative"
        with self.assertRaisesRegex(ValueError, "Only a diagnosed gap"):
            self.advance(self.run, out)

    def test_nonpriority_gap_must_be_explicitly_deferred(self):
        out = copy.deepcopy(self.outputs["gap_finder"])
        out["assessments"]["C5"]["status"] = "gap"
        with self.assertRaisesRegex(ValueError, "selected or explicitly deferred"):
            self.advance(self.run, out)
        out["deferred_criteria"] = ["C5"]
        self.assertEqual(LOOP.inspect_run(self.advance(self.run, out))["status"], "ready")

    def test_no_change_cannot_hide_unassessed_or_known_gaps(self):
        out = copy.deepcopy(self.outputs["gap_finder"])
        out.update(status="no_change", selected_criteria=[])
        with self.assertRaisesRegex(ValueError, "no_change"):
            self.advance(self.run, out)
        for value in out["assessments"].values():
            value["status"] = "meets"
        out["assessments"]["C1"].update(status="not_assessed", draft_witness="")
        with self.assertRaisesRegex(ValueError, "no_change"):
            self.advance(self.run, out)
        out["status"] = "needs_sources"
        self.assertEqual(LOOP.inspect_run(self.advance(self.run, out))["status"], "needs_sources")

    def test_proposer_cannot_drop_or_replace_selected_criteria(self):
        for value in (["C1"], ["C1", "C2", "C4"], ["UNKNOWN"]):
            out = {**self.outputs["proposer"], "criterion_ids": value}
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.advance(self.through(1), out)

    def test_writer_must_locate_each_realized_operation_or_query_blocker(self):
        for kind in ("missing", "wrong_witness", "blocked_without_query"):
            out = copy.deepcopy(self.outputs["writer"])
            if kind == "missing":
                del out["implementations"]["C1"]
            elif kind == "wrong_witness":
                out["implementations"]["C1"]["witness"] = "Absent realization"
            else:
                out["implementations"]["C1"].update(status="blocked", witness="")
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.advance(self.through(2), out)
        out["open_queries"] = ["Author evidence needed for this operation."]
        run = self.advance(self.through(2), out)
        with self.assertRaisesRegex(ValueError, "queries"):
            self.advance(run)

    def test_reviewer_sees_target_but_not_prior_assessments_or_implementation_notes(self):
        self.outputs["gap_finder"]["assessments"]["C1"]["difference"] = "PRIVATE_DIAGNOSIS"
        self.outputs["writer"]["implementations"]["C1"]["note"] = "PRIVATE_IMPLEMENTATION"
        packet = LOOP.inspect_run(self.through(3))["packet"]
        self.assertEqual(packet["role"], "reviewer")
        self.assertIn("benchmark", packet["input"])
        self.assertIn("writing_resources", packet["input"])
        self.assertNotIn("PRIVATE_", json.dumps(packet))

    def test_acceptance_rechecks_priority_and_allows_explicitly_deferred_gaps(self):
        for status in ("gap", "not_assessed"):
            out = copy.deepcopy(self.outputs["reviewer"])
            row = out["assessments"]["C1"]
            row["status"] = status
            if status == "not_assessed":
                row["draft_witness"] = ""
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, "priority"):
                self.advance(self.through(3), out)
        out = copy.deepcopy(self.outputs["reviewer"])
        out["assessments"]["C5"]["status"] = "gap"
        self.assertEqual(LOOP.inspect_run(self.advance(self.through(3), out))["status"],
                         "accepted_revision")

    def test_standards_only_does_not_claim_exemplar_based_review(self):
        self.run["exemplars"] = {}
        for row in self.run["benchmark"]["criteria"].values():
            row["source_ids"] = []
        packet = LOOP.inspect_run(self.run)["packet"]
        self.assertEqual(packet["input"]["benchmark_basis"], "standards_only")

    def test_resource_or_criterion_change_invalidates_old_handoffs(self):
        run = self.through(1)
        with patch.object(BENCHMARK, "load_resources", wraps=BENCHMARK.load_resources) as loader:
            resources = BENCHMARK.load_resources(self.run["benchmark"], self.run["exemplars"])
            resources["ai.rule.operation"]["entries"][0]["guidance"] += " Changed."
            loader.side_effect = None
            loader.return_value = resources
            with self.assertRaisesRegex(ValueError, "stale"):
                LOOP.inspect_run(run)
        run["benchmark"]["criteria"]["C1"]["expectation"] += " Changed."
        with self.assertRaisesRegex(ValueError, "stale"):
            LOOP.inspect_run(run)

    def test_resource_projection_is_read_only_and_packet_mutation_is_isolated(self):
        with patch("socket.socket", side_effect=AssertionError("No network")), \
                patch.object(Path, "write_text", side_effect=AssertionError("No writes")):
            packet = LOOP.inspect_run(self.run)["packet"]
        packet["input"]["benchmark"]["criteria"]["C1"]["expectation"] = "Altered"
        packet["input"]["writing_resources"]["abstract"]["guide"]["moves"] = []
        fresh = LOOP.inspect_run(self.run)["packet"]
        self.assertNotEqual(fresh["input"]["benchmark"]["criteria"]["C1"]["expectation"], "Altered")
        self.assertTrue(fresh["input"]["writing_resources"]["abstract"]["guide"]["moves"])

    def test_release_bundle_v2_cli_has_self_contained_resource_lookup(self):
        with tempfile.TemporaryDirectory(prefix="section benchmark ") as temporary:
            base = Path(temporary)
            result = subprocess.run([sys.executable, str(ROOT / "tools/build_release.py"),
                                     "--output-dir", str(base / "release")], cwd=base,
                                    capture_output=True, text=True, encoding="utf-8", timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            archive, = (base / "release").glob("*.zip")
            with zipfile.ZipFile(archive) as bundle:
                bundle.extractall(base / "installed")
            installed = base / "installed/super-writer"
            result = subprocess.run([sys.executable, str(installed / "scripts/writing_loop.py"),
                                     str(installed / "examples/writing-team/benchmark-input.json")],
                                    cwd=base, capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), LOOP.inspect_run(self.run))


if __name__ == "__main__":
    unittest.main()
