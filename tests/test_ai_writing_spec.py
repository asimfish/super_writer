"""Original specification contracts, not evidence of improved manuscript quality."""

from __future__ import annotations

import copy
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import writing_lookup


def cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts/writing_lookup.py"), *args],
        cwd=tempfile.gettempdir(), capture_output=True, text=True,
        encoding="utf-8", timeout=30,
    )


class AISpecTests(unittest.TestCase):
    def spec(self) -> dict:
        return json.loads((ROOT / "references/ai-writing-spec.json").read_text())

    def test_exact_ai_entry_keeps_conditions_and_counterexamples_cli(self) -> None:
        result = cli("--catalog", "ai-spec", "--id", "ai.usage.significant", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["catalog"], "ai-spec")
        original = next(e for e in self.spec()["entries"] if e["id"] == "ai.usage.significant")
        self.assertEqual(report["entries"], [original])
        self.assertNotIn("upstream_commit", report)

    def test_catalog_validates_and_counts_are_distinct(self) -> None:
        spec = self.spec()
        writing_lookup.validate_ai_spec(spec)
        kinds = {k: sum(e["kind"] == k for e in spec["entries"]) for k in spec["taxonomy"]["kinds"]}
        self.assertEqual(kinds, {"writing_rule": 19, "claim_usage": 15, "technical_term": 34})
        library = json.loads(writing_lookup.INDEX.read_text())
        self.assertEqual(len(library["entries"]), 130)
        self.assertTrue(set(e["id"] for e in library["entries"]).isdisjoint(e["id"] for e in spec["entries"]))

    def test_defaults_remain_the_pinned_library(self) -> None:
        result = cli("--id", "general.usage-note.significant.001", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("upstream_commit", report)
        self.assertNotIn("catalog", report)
        self.assertEqual(report["entries"][0]["id"], "general.usage-note.significant.001")

    def test_topic_and_level_intersect_with_existing_filters(self) -> None:
        result = cli("动作分块", "--catalog", "ai-spec", "--topic", "具身控制",
                     "--level", "词语", "--kind", "technical_term", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads(result.stdout)["entries"]
        self.assertEqual(entries[0]["id"], "ai.term.action-chunking")
        for entry in entries:
            self.assertIn("embodied_control", entry["topics"])
            self.assertIn("word", entry["levels"])
        result = cli("--catalog", "ai-spec", "--id", "ai.term.action-chunking", "--level", "document")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_facets_do_not_silently_fall_back_in_legacy_catalogs(self) -> None:
        for args in (("result", "--topic", "statistics"),
                     ("--catalog", "ai-spec", "result", "--topic", "unknown")):
            result = cli(*args)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")

    def test_v1_records_remain_readable_without_new_facets(self) -> None:
        spec = self.spec()
        spec["schema_version"] = "1"
        for field in ("topics", "levels"):
            spec["taxonomy"].pop(field, None)
        for field in ("topic", "level"):
            spec["taxonomy"]["filter_aliases"].pop(field, None)
        for entry in spec["entries"]:
            for field in ("topics", "levels", "source_notes"):
                entry.pop(field, None)
        writing_lookup.validate_ai_spec(spec)
        self.assertEqual(len(writing_lookup.search(spec, "", {}, "ai.term.zero-shot")), 1)
        with self.assertRaisesRegex(ValueError, "not supported"):
            writing_lookup.search(spec, "zero-shot", {"topic": "learning_regimes"})

    def test_v2_facets_and_source_notes_are_checked(self) -> None:
        base = self.spec()
        mutations = [
            lambda s: s["taxonomy"].pop("topics"),
            lambda s: s["entries"][0].update(topics=[]),
            lambda s: s["entries"][0].update(topics=["unknown"]),
            lambda s: s["entries"][0].update(levels=["unknown"]),
            lambda s: s["entries"][0].update(source_notes=[{"source_id": "missing", "location": "Abstract", "observation": "Context"}]),
        ]
        for mutate in mutations:
            spec = copy.deepcopy(base)
            mutate(spec)
            with self.assertRaises(ValueError):
                writing_lookup.validate_ai_spec(spec)
        spec = self.spec()
        entry = next(e for e in spec["entries"] if e["source_ids"])
        entry["source_notes"] = []
        with self.assertRaises(ValueError):
            writing_lookup.validate_ai_spec(spec)
        for notes in (None, [{"source_id": entry["source_ids"][0]}],
                      [{"source_id": entry["source_ids"][0], "location": "", "observation": "context"}],
                      [{"source_id": entry["source_ids"][0], "location": "Abstract", "observation": []}]):
            entry["source_notes"] = notes
            with self.assertRaises(ValueError):
                writing_lookup.validate_ai_spec(spec)
        entry["source_notes"] = [copy.deepcopy(n) for n in next(
            e for e in base["entries"] if e["id"] == entry["id"])["source_notes"]]
        entry["source_notes"].append(copy.deepcopy(entry["source_notes"][0]))
        with self.assertRaises(ValueError):
            writing_lookup.validate_ai_spec(spec)

    def test_curated_boundary_cases_keep_the_misleading_reading_and_exception(self) -> None:
        cases = {
            "ai.term.action-chunking": ("six-action", "one step", "fresh observations"),
            "ai.term.open-loop": ("joint servo", "low-level feedback", "low-level servo"),
            "ai.term.closed-loop": ("logged camera", "not fed", "proprioceptive feedback"),
            "ai.term.in-context-learning": ("without updating", "optimization step", "adapter training"),
            "ai.term.offline-reinforcement-learning": ("followed by online", "later online", "hybrid pipeline"),
            "ai.term.preference-optimization": ("machine-labeled", "label provenance", "reward representation"),
            "ai.usage.causal": ("does not isolate", "not isolated", "model class"),
        }
        for entry_id, (supported, error, exception) in cases.items():
            with self.subTest(entry_id=entry_id):
                result = cli("--catalog", "ai-spec", "--id", entry_id, "--format", "json")
                self.assertEqual(result.returncode, 0, result.stderr)
                entry = json.loads(result.stdout)["entries"][0]
                self.assertIn(supported, " ".join(entry["examples"]))
                self.assertIn(error, " ".join(x["why"] for x in entry["counter_examples"]))
                self.assertIn(exception, " ".join(entry["exceptions"]))

    def test_markdown_preserves_source_locations_and_facet_labels(self) -> None:
        result = cli("--catalog", "ai-spec", "--id", "ai.term.action-chunking")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = next(e for e in self.spec()["entries"] if e["id"] == "ai.term.action-chunking")
        self.assertIn("Topics: embodied_control; levels: word, sentence", result.stdout)
        for note in entry["source_notes"]:
            self.assertIn(note["location"], result.stdout)
            self.assertIn(note["observation"], result.stdout)

    def test_grounding_alias_and_new_facets_retrieve_complete_record(self) -> None:
        result = cli("视觉定位", "--catalog", "ai-spec", "--domain", "多模态",
                     "--topic", "支持与忠实性", "--level", "词语",
                     "--kind", "technical_term", "--limit", "1", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = json.loads(result.stdout)["entries"][0]
        original = next(e for e in self.spec()["entries"] if e["id"] == "ai.term.visual-grounding")
        self.assertEqual(entry, original)
        self.assertIn("multimodal", entry["domains"])
        self.assertIn("grounding_faithfulness", entry["topics"])

    def test_grounding_and_horizon_examples_preserve_the_construct_boundary(self) -> None:
        cases = {
            "ai.rule.evaluation-target": ("not explanation faithfulness", "prediction process", "named metric"),
            "ai.rule.evidence-modality": ("does not establish absence", "incomplete", "negative evidence"),
            "ai.rule.failure-localization": ("does not isolate", "cause", "controlled intervention"),
            "ai.usage.grounded": ("not tested", "input", "grounded planning"),
            "ai.usage.faithful": ("not evaluated", "plausibility", "source consistency"),
            "ai.usage.hallucination-free": ("observed", "universal", "finite evaluation"),
            "ai.term.factual-precision": ("8 of 10", "completeness", "abstentions"),
            "ai.term.citation-recall": ("three of four", "uncited", "jointly support"),
            "ai.term.citation-precision": ("both citations", "individually", "minimal"),
            "ai.term.object-hallucination": ("object", "attributes", "reference coverage"),
            "ai.term.visual-grounding": ("box", "input", "segmentation"),
            "ai.term.robotic-affordance": ("estimated", "guarantee", "task-specific"),
            "ai.term.task-chain-success": ("3 of 12", "conditional", "prefix"),
            "ai.term.long-horizon": ("four-subgoal", "prediction horizon", "domain-specific"),
        }
        for entry_id, (supported, error, exception) in cases.items():
            with self.subTest(entry_id=entry_id):
                result = cli("--catalog", "ai-spec", "--id", entry_id, "--format", "json")
                self.assertEqual(result.returncode, 0, result.stderr)
                entry = json.loads(result.stdout)["entries"][0]
                self.assertIn(supported, " ".join(entry["examples"]))
                self.assertIn(error, " ".join(x["why"] for x in entry["counter_examples"]))
                self.assertIn(exception, " ".join(entry["exceptions"]))
                self.assertTrue(entry["source_notes"])

    def test_worked_chain_metrics_are_not_marginal_task_rates(self) -> None:
        initial_chains = 12
        prefixes = [12, 9, 6, 3]
        self.assertLessEqual(prefixes[0], initial_chains)
        self.assertEqual(prefixes, sorted(prefixes, reverse=True))
        full_chain_rate = prefixes[-1] / initial_chains
        mean_prefix_length = sum(prefixes) / initial_chains
        last_step_conditional_rate = prefixes[-1] / prefixes[-2]
        self.assertEqual(full_chain_rate, 0.25)
        self.assertEqual(mean_prefix_length, 2.5)
        self.assertEqual(last_step_conditional_rate, 0.5)
        worked = (ROOT / "examples/ai-writing-spec/grounding-and-horizon.md").read_text()
        for fragment in ("12, 9, 6, 3", "3/12 = 25%", "30/12 = 2.5", "3/6 = 50%"):
            self.assertIn(fragment, worked)
        self.assertIn("not CALVIN results", worked)
        for entry_id in ("ai.rule.result-answer", "ai.rule.failure-localization", "ai.term.task-chain-success"):
            self.assertIn("#" + entry_id, worked)

    def test_chinese_term_and_kind_select_the_ai_sense(self) -> None:
        result = cli("零样本", "--catalog", "ai-spec", "--kind", "technical_term", "--limit", "1", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["entries"][0]["id"], "ai.term.zero-shot")

    def test_context_absorption_keeps_order_and_its_conditional_exception(self) -> None:
        result = cli("复现步骤", "--catalog", "ai-spec", "--topic", "evaluation_protocol",
                     "--level", "sentence", "--kind", "writing_rule", "--limit", "1", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        entry = report["entries"][0]
        self.assertEqual(entry["id"], "ai.rule.procedure-order")
        self.assertEqual(entry, next(e for e in self.spec()["entries"] if e["id"] == entry["id"]))
        self.assertIn("After verifying", entry["examples"][0])
        self.assertIn("retain the final archive", entry["examples"][0])
        self.assertIn("order", entry["counter_examples"][0]["why"])
        self.assertIn("simultaneous", " ".join(entry["exceptions"]))
        source = next(s for s in report["terminology_context_sources"] if s["id"] == "marmot-ste-context")
        self.assertIn("afd2875fe08cf5586dd0b2116b24190308c8b7db", source["url"])
        self.assertIn("not an authoritative", source["read_scope"])

    def test_definition_absorbs_reference_resolution_without_a_duplicate_id(self) -> None:
        result = cli("--catalog", "ai-spec", "--id", "ai.rule.definition", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = json.loads(result.stdout)["entries"][0]
        self.assertIn("maximum observation age", entry["examples"][0])
        self.assertIn("only the student is updated", " ".join(entry["examples"]))
        self.assertIn("ambiguous antecedent", " ".join(e["why"] for e in entry["counter_examples"]))
        self.assertIn("unambiguous pronouns", " ".join(entry["exceptions"]))
        self.assertIn("marmot-ste-context", entry["source_ids"])
        self.assertNotIn("ai.rule.reference-resolution", {e["id"] for e in self.spec()["entries"]})

    def test_context_guide_preserves_academic_and_literal_exceptions(self) -> None:
        guide = " ".join((ROOT / "references/clarity-context.md").read_text().split())
        examples = " ".join((ROOT / "examples/ai-writing-spec/clarity-context.md").read_text().split())
        for text in ("Passive voice", "known actor", "running mean", "standard term",
                     "not execute", "domain review", "not been performed", "STE-compliant"):
            self.assertIn(text, guide)
        for text in ("only the student is updated", "time-varying environments",
                     "After verifying", "CHECKPOINT_MISMATCH", "has been accumulating"):
            self.assertIn(text, examples)
        self.assertIn("references/clarity-context.md", (ROOT / "SKILL.md").read_text())

    def test_markdown_keeps_examples_conditions_and_exceptions(self) -> None:
        result = cli("--catalog", "ai-spec", "--id", "ai.term.fine-tuning")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = next(e for e in self.spec()["entries"] if e["id"] == "ai.term.fine-tuning")
        for field in ("conditions", "exceptions", "evidence_required", "examples"):
            for value in entry[field]:
                self.assertIn(value, result.stdout)
        for example in entry["counter_examples"]:
            self.assertIn(example["text"], result.stdout)
            self.assertIn(example["why"], result.stdout)

    def test_small_budget_fails_without_partial_json(self) -> None:
        result = cli("--catalog", "ai-spec", "--id", "ai.usage.significant", "--format", "json", "--max-chars", "512")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("No complete matching card", result.stderr)

    def test_unknown_catalog_and_cross_catalog_ids_never_fall_back(self) -> None:
        for args in (("--catalog", "missing", "result"),
                     ("--catalog", "ai-spec", "--id", "general.usage-note.significant.001"),
                     ("--id", "ai.usage.significant"),
                     ("--catalog", "ai-spec", "result", "--kind", "sentence_pattern")):
            with self.subTest(args=args):
                result = cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_invalid_semantic_and_reference_records_are_rejected(self) -> None:
        base = self.spec()
        mutations = [
            lambda s: s["entries"].append(copy.deepcopy(s["entries"][0])),
            lambda s: s["entries"][0].update(status="approved"),
            lambda s: s["entries"][0].update(status=[]),
            lambda s: s["entries"][0].update(status={}),
            lambda s: s["entries"][0].update(conditions=[]),
            lambda s: s["entries"][0].update(exceptions=[]),
            lambda s: s["entries"][0].update(examples=[]),
            lambda s: s["entries"][0].update(counter_examples=[{"text": "Unqualified claim."}]),
            lambda s: s["entries"][0].update(source_ids=["missing"]),
            lambda s: s["entries"][0].update(owner="references/../private/secret.md"),
            lambda s: s["entries"][0].update(domains=["invented"]),
            lambda s: s["aliases"].update({"broken": "not-a-list"}),
        ]
        for number, mutate in enumerate(mutations):
            with self.subTest(mutation=number):
                spec = copy.deepcopy(base)
                mutate(spec)
                with self.assertRaises(ValueError):
                    writing_lookup.validate_ai_spec(spec)

    def test_related_library_ids_are_real_without_importing_more_cards(self) -> None:
        ids = {e["id"] for e in json.loads(writing_lookup.INDEX.read_text())["entries"]}
        for entry in self.spec()["entries"]:
            self.assertLessEqual(set(entry.get("related_library_ids", [])), ids)

    def test_malformed_filter_aliases_fail_at_validation(self) -> None:
        for aliases in ([], {"domain": []}, {"domain": {"rl": []}},
                        {"domain": {"rl": "invented"}}, {"unknown": {}},
                        {"domain": {"": "general"}}):
            with self.subTest(aliases=aliases):
                spec = self.spec()
                spec["taxonomy"]["filter_aliases"] = aliases
                with self.assertRaises(ValueError):
                    writing_lookup.validate_ai_spec(spec)

    def test_source_urls_are_parseable_https_without_credentials(self) -> None:
        for url in ("https://", "https:///missing-host", "https://user:secret@example.com/paper",
                    "https://example.com/paper\nnext", "http://example.com/paper"):
            with self.subTest(url=url):
                spec = self.spec()
                spec["sources"][0]["url"] = url
                with self.assertRaises(ValueError):
                    writing_lookup.validate_ai_spec(spec)

    def test_budget_keeps_complete_records_including_sources(self) -> None:
        spec = self.spec()
        entries = writing_lookup.search(spec, "evaluation", {})
        rendered = writing_lookup.bounded_render(spec, entries, 20, 6000, "json")
        self.assertLessEqual(len(rendered) + 1, 6000)
        for entry in json.loads(rendered)["entries"]:
            self.assertEqual(entry, next(e for e in spec["entries"] if e["id"] == entry["id"]))

    def test_oversized_and_corrupt_catalogs_fail_with_empty_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "spec.json"
            for content in (b"x" * (2 * 1024 * 1024 + 1), b'{"entries":', b"[]"):
                source.write_bytes(content)
                stdout, stderr = io.StringIO(), io.StringIO()
                with patch.object(writing_lookup, "AI_SPEC", source), \
                        patch.object(sys, "argv", ["writing_lookup", "--catalog", "ai-spec", "--id", "ai.rule.scope"]), \
                        contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as exit_status:
                        writing_lookup.main()
                self.assertEqual(exit_status.exception.code, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("Lookup failed", stderr.getvalue())

    def test_all_exact_ids_are_retrievable_in_full(self) -> None:
        spec = self.spec()
        for entry in spec["entries"]:
            matches = writing_lookup.search(spec, "", {}, entry["id"])
            report = json.loads(writing_lookup.bounded_render(spec, matches, 1, 12000, "json"))
            self.assertEqual(report["entries"], [entry])

    def test_lookup_is_read_only_without_network_or_child_processes(self) -> None:
        code = '''
import os, sys
sys.path.insert(0, sys.argv[1])
import writing_lookup
def audit(event, args):
    if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn"}:
        raise RuntimeError("Forbidden external effect")
    if event == "open" and args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT):
        raise RuntimeError("Forbidden write")
sys.addaudithook(audit)
sys.argv = ["writing_lookup", "--catalog", "ai-spec", "--id", "ai.term.fine-tuning", "--format", "json"]
raise SystemExit(writing_lookup.main())
'''
        result = subprocess.run([sys.executable, "-B", "-c", code, str(ROOT / "scripts")],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["entries"][0]["id"], "ai.term.fine-tuning")


if __name__ == "__main__":
    unittest.main()
