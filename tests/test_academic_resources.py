"""Offline CLI, policy, corpus and PDF-parser contracts; not LLM quality scores."""

from __future__ import annotations

import hashlib
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
import humanize_check
import pdf_layout_check
import venue_profile
import word_guard
import writing_lookup
sys.path.insert(0, str(ROOT / "tools"))
import render_examples
import import_writing_library


def cli(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args],
                          cwd=tempfile.gettempdir(), capture_output=True, text=True,
                          encoding="utf-8", timeout=30)


class VenueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(venue_profile.CATALOG.read_text(encoding="utf-8"))

    def test_unique_exact_profiles_link_to_real_fixture_pins(self) -> None:
        specs = json.loads((ROOT / "tests/fixtures/templates/sources.json").read_text())["templates"]
        ids = {spec["id"] for spec in specs}
        profiles = self.catalog["profiles"]
        self.assertEqual(len(profiles), len({p["id"] for p in profiles}))
        self.assertEqual({p["venue"] for p in profiles}, {"ICML", "ICLR", "CVPR", "NeurIPS", "ACL", "EMNLP", "ECCV", "AAAI"})
        for p in profiles:
            self.assertLessEqual(set(p["template_ids"]), ids)
            self.assertGreater(p["body_pages"], 0)
            self.assertTrue(all(url.startswith("https://") for url in p["official_sources"]))
        for spec in specs:
            self.assertTrue((ROOT / "tests/fixtures/templates" / (spec["id"] + ".tex")).is_file())

    def test_unknown_year_does_not_fall_back(self) -> None:
        result = cli("venue_profile.py", "--venue", "ICLR", "--year", "2027", "--track", "main", "--stage", "review")
        self.assertEqual(result.returncode, 2)
        self.assertIn("No exact profile", result.stderr)

    def test_missing_year_or_stage_is_not_implicitly_selected(self) -> None:
        result = cli("venue_profile.py", "--venue", "ECCV")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no implicit", result.stderr)

    def test_selection_rejects_conflicting_id_and_filters(self) -> None:
        result = cli("venue_profile.py", "--id", "eccv-2026-main-review", "--stage", "rebuttal")
        self.assertEqual(result.returncode, 2)

    def test_eccv_rebuttal_has_distinct_template_and_total_budget(self) -> None:
        result = cli("venue_profile.py", "--id", "eccv-2026-main-rebuttal", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        p = json.loads(result.stdout)["profiles"][0]
        self.assertEqual((p["body_pages"], p["excluded_from_body"], p["template_ids"]), (1, [], ["eccv2026-rebuttal"]))

    def test_shared_acl_style_keeps_long_short_and_venue_policies_distinct(self) -> None:
        profiles = venue_profile.select(self.catalog, venue="EMNLP")
        self.assertEqual({p["body_pages"] for p in profiles}, {4, 8})
        self.assertEqual({tuple(p["template_ids"]) for p in profiles}, {("acl2026",)})

    def test_blocked_aaai_download_is_visible_not_a_fictional_pass(self) -> None:
        result = cli("venue_profile.py", "--id", "aaai-2026-main-review", "--format", "json")
        p = json.loads(result.stdout)["profiles"][0]
        self.assertEqual(p["status"], "guide-only-download-blocked")
        self.assertEqual(p["template_ids"], [])
        self.assertEqual(p["citation_modes"], [])

    def test_list_from_other_working_directory(self) -> None:
        result = cli("venue_profile.py", "--list", "--venue", "ACL")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 2)


class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = json.loads(writing_lookup.INDEX.read_text(encoding="utf-8"))

    def test_corpus_ids_provenance_and_discovery_sources_are_complete(self) -> None:
        entries = self.index["entries"]
        self.assertEqual(len(entries), 127)
        self.assertEqual(len(entries), len({entry["id"] for entry in entries}))
        sources = {s["id"] for s in self.index["sources"]}
        for entry in entries:
            self.assertLessEqual(set(entry["source_ids"]), sources)
            self.assertNotEqual(entry["provenance"]["type"], "attested_collocation")
            self.assertIn(entry["quality"]["status"], {"reviewed", "source_checked"})
            for field in ("meaning", "guidance", "avoid", "expression"):
                self.assertTrue(entry[field].strip(), (entry["id"], field))
        self.assertEqual(hashlib.sha256((ROOT / "DATA_LICENSE").read_bytes()).hexdigest(),
                         self.index["upstream"]["input_sha256"]["DATA_LICENSE"])

    def test_chinese_alias_retrieves_statistical_significance_usage(self) -> None:
        entries = writing_lookup.search(self.index, "显著提升", {"kind": "usage_note"})
        self.assertEqual(entries[0]["id"], "general.usage-note.significant.001")

    def test_technical_and_rhetorical_queries_have_distinct_scopes(self) -> None:
        technical = writing_lookup.search(self.index, "distribution shift", {"domain": "rl", "kind": "definition"})
        rhetoric = writing_lookup.search(self.index, "result boundary", {"section": "experiments", "kind": "sentence_pattern"})
        self.assertIn("rl.definition.offline-distribution-shift.001", {e["id"] for e in technical})
        self.assertIn("general.sentence-pattern.result-boundary.001", {e["id"] for e in rhetoric})
        self.assertTrue(all(e["kind"] == "definition" for e in technical))

    def test_exact_id_preserves_qualifications_and_source_pointers(self) -> None:
        ident = "general.sentence-pattern.rebuttal-no-evidence.001"
        result = cli("writing_lookup.py", "--id", ident, "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        card = json.loads(result.stdout)["entries"][0]
        self.assertEqual(card, next(e for e in self.index["entries"] if e["id"] == ident))

    def test_limits_bound_complete_json_including_source_metadata(self) -> None:
        entries = writing_lookup.search(self.index, "result", {})
        output = writing_lookup.bounded_render(self.index, entries, 20, 6000, "json")
        self.assertLessEqual(len(output) + 1, 6000)
        report = json.loads(output)
        self.assertGreater(len(report["entries"]), 0)
        self.assertTrue(all("avoid" in e and "guidance" in e for e in report["entries"]))

    def test_small_budget_never_returns_partial_card(self) -> None:
        with self.assertRaisesRegex(ValueError, "No complete matching card"):
            writing_lookup.bounded_render(self.index, self.index["entries"][:1], 1, 512, "json")

    def test_unknown_filters_fail_instead_of_searching_everything(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown domain"):
            writing_lookup.search(self.index, "result", {"domain": "made-up"})

    def test_no_match_is_not_a_dictionary_verdict(self) -> None:
        result = cli("writing_lookup.py", "zzzzUnattestedTokenzzzz")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not evidence that a term is invalid", result.stderr)

    def test_bad_limits_and_manuscript_sized_query_are_rejected(self) -> None:
        for args in (("result", "--limit", "0"), ("result", "--limit", "21"),
                     ("result", "--max-chars", "999999"), ("x" * 257,)):
            with self.subTest(args=args):
                self.assertEqual(cli("writing_lookup.py", *args).returncode, 2)

    def test_lookup_does_not_open_network(self) -> None:
        with patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")):
            entries = writing_lookup.search(self.index, "world model", {"domain": "世界模型"})
            self.assertGreater(len(entries), 0)

    def test_importer_rejects_unreviewed_or_attested_records(self) -> None:
        entry = json.loads(json.dumps(self.index["entries"][0]))
        minimal = {**self.index, "entries": [entry]}
        entry["quality"]["status"] = "candidate"
        self.assertEqual(import_writing_library.curate(minimal, [entry["id"]])["entries"], [])
        entry["quality"]["status"] = "reviewed"
        entry["provenance"]["type"] = "attested_collocation"
        self.assertEqual(import_writing_library.curate(minimal, [entry["id"]])["entries"], [])

    def test_importer_changed_bytes_fail_before_curation(self) -> None:
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b"changed upstream")):
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                import_writing_library.fetch("skills/super-library/references/index.json")


class CitationModeTests(unittest.TestCase):
    def test_lncs_numeric_bibliography_catches_word_default_mismatch(self) -> None:
        source = r"\bibliographystyle{splncs04}"
        self.assertIn("mismatch", word_guard.citation_style_finding("(Hastie, 2009)", source))
        self.assertIsNone(word_guard.citation_style_finding("[1]", source))

    def test_natbib_numeric_options_override_plainnat_name(self) -> None:
        for command in (r"\usepackage[numbers]{natbib}", r"\PassOptionsToPackage{numbers}{natbib}", r"\setcitestyle{numbers,square}"):
            source = command + "\n" + r"\bibliographystyle{plainnat}"
            with self.subTest(command=command):
                self.assertIsNotNone(word_guard.citation_style_finding("(Hastie, 2009)", source))
                self.assertIsNone(word_guard.citation_style_finding("[1]", source))

    def test_commented_numeric_option_does_not_change_author_date(self) -> None:
        source = "% \\PassOptionsToPackage{numbers}{natbib}\n\\bibliographystyle{plainnat}"
        self.assertFalse(word_guard.numeric_citation_source(source))
        self.assertIsNone(word_guard.citation_style_finding("(Hastie, 2009)", source))

    def test_later_explicit_author_year_restores_natbib_mode(self) -> None:
        source = r"\usepackage[numbers]{natbib}\setcitestyle{authoryear}\bibliographystyle{plainnat}"
        self.assertFalse(word_guard.numeric_citation_source(source))
        self.assertIsNone(word_guard.citation_style_finding("(Hastie, 2009)", source))

    def test_official_acl_package_supplies_implicit_bibliography_style(self) -> None:
        source = r"\usepackage[review]{acl}"
        self.assertEqual(word_guard.bibliography_style(source), "acl_natbib")
        self.assertIsNone(word_guard.author_year_citation_finding("(Hastie, 2009)", source))


class StyleHeuristicTests(unittest.TestCase):
    def matrix(self, path: Path) -> None:
        path.write_text("| Row | AI pattern | Detection dim | Severity | Applied change | Teaching |\n"
                        "|---|---|---|---|---|---|\n" + "\n".join(
                            f"| {i} | No material defect | D{i} | low | No change | Preserve terminology |" for i in range(1, 6)), encoding="utf-8")

    def test_uniform_technical_prose_is_advisory_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "humanize_matrix.md"
            self.matrix(path)
            result = humanize_check.check_matrix(path, "The estimator uses fixed weights. " * 10, "en")
            self.assertTrue(result.ok, result.required_findings)
            self.assertTrue(result.advisory_findings)
            self.assertNotIn("[required]", humanize_check.to_markdown(result))

    def test_explicit_legacy_enforcement_can_block_but_does_not_require_fake_severity(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "humanize_matrix.md"
            self.matrix(path)
            result = humanize_check.check_matrix(path, "The estimator uses fixed weights. " * 10, "en", enforce_heuristics=True)
            self.assertFalse(result.ok)
            self.assertFalse(any("high-severity" in finding for finding in result.required_findings))

    def test_missing_audit_structure_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            result = humanize_check.check_matrix(Path(d) / "absent.md", "Text.", "en")
            self.assertFalse(result.ok)
            self.assertEqual(result.required_findings, ["humanize_matrix.md not found"])

    def test_non_boolean_enforcement_does_not_enable_it(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "humanize_matrix.md"
            self.matrix(path)
            result = humanize_check.check_matrix(path, "Fixed technical wording. " * 10, "en", enforce_heuristics="true")
            self.assertFalse(result.enforce_heuristics)
            self.assertTrue(result.ok, result.required_findings)

    def test_invalid_configuration_fails_at_cli(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            self.matrix(Path(d) / "humanize_matrix.md")
            (Path(d) / "paper_spine_config.json").write_text("[]", encoding="utf-8")
            result = cli("humanize_check.py", d, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("JSON object", result.stderr)


class PdfLayoutTests(unittest.TestCase):
    def bbox(self, word: str = '<word xMin="10" yMin="20" xMax="100" yMax="30">Text</word>') -> str:
        return f'<html xmlns="http://www.w3.org/1999/xhtml"><body><doc><page width="612" height="792">{word}</page></doc></body></html>'

    def test_physical_bounds_accept_valid_word(self) -> None:
        self.assertEqual(pdf_layout_check.inspect_bbox(self.bbox()), (1, [], []))

    def test_overflow_and_nonfinite_boxes_fail(self) -> None:
        for value in ("900", "NaN", "Infinity"):
            _, errors, _ = pdf_layout_check.inspect_bbox(self.bbox().replace('xMax="100"', f'xMax="{value}"'))
            self.assertEqual(len(errors), 1)

    def test_image_only_page_needs_visual_review_not_false_blank_failure(self) -> None:
        pages, errors, warnings = pdf_layout_check.inspect_bbox(self.bbox(""))
        self.assertEqual((pages, errors), (1, []))
        self.assertIn("image-only", warnings[0])

    def test_no_pages_and_invalid_page_dimensions(self) -> None:
        self.assertEqual(pdf_layout_check.inspect_bbox("<doc/>"), (0, ["PDF has no inspectable pages"], []))
        with self.assertRaisesRegex(ValueError, "Invalid page"):
            pdf_layout_check.inspect_bbox(self.bbox().replace('width="612"', 'width="NaN"'))

    def test_external_xml_entities_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "entity"):
            pdf_layout_check.inspect_bbox('<!DOCTYPE doc [<!ENTITY e SYSTEM "file:///private">]><doc/>')

    def test_font_embedding_and_type3_are_distinct(self) -> None:
        header = "name type encoding emb sub uni object ID\n------------------------------------\n"
        self.assertEqual(pdf_layout_check.inspect_fonts(header + "AAAA+CMR10 Type 1 Builtin yes yes no 5 0"), ([], []))
        errors, warnings = pdf_layout_check.inspect_fonts(header + "CMR10 Type 3 Custom no no no 5 0")
        self.assertEqual(errors, ["Unembedded font: CMR10"])
        self.assertEqual(len(warnings), 1)

    def test_unknown_font_output_cannot_claim_embedding_pass(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unrecognized"):
            pdf_layout_check.inspect_fonts("header\nline\nmalformed row")

    def test_empty_font_tool_output_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unrecognized pdffonts header"):
            pdf_layout_check.inspect_fonts("")

    def test_log_distinguishes_real_failures_from_harmless_warnings(self) -> None:
        self.assertEqual(pdf_layout_check.inspect_log("Underfull \\hbox; rerunfilecheck warning"), [])
        findings = pdf_layout_check.inspect_log("Overfull \\hbox (15pt)\nLaTeX Warning: Citation `x' undefined\n! Fatal error")
        self.assertEqual(len(findings), 3)

    def test_invalid_pdf_never_invokes_poppler(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "not.pdf"
            path.write_bytes(b"not a PDF")
            with patch.object(pdf_layout_check, "run_tool", side_effect=AssertionError("must not run")):
                with self.assertRaisesRegex(ValueError, "Expected a PDF"):
                    pdf_layout_check.check(path)

    def test_pdf_receipt_binds_snapshot_and_explicit_total_page_limit(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "paper.pdf"
            original = b"%PDF-1.4\nsynthetic mock input"
            path.write_bytes(original)
            def tool(args: list[str]) -> str:
                path.write_bytes(b"%PDF-1.4\nchanged source")
                snapshot = Path(args[-2] if args[0] == "pdftotext" else args[-1])
                self.assertEqual(snapshot.read_bytes(), original)
                return self.bbox().replace("</doc>", '<page width="612" height="792"/></doc>') if args[0] == "pdftotext" else "name type encoding emb sub uni object ID\nseparator\n"
            with patch.object(pdf_layout_check, "run_tool", side_effect=tool):
                result = pdf_layout_check.check(path, max_pages=1)
            self.assertEqual(result["pdf_sha256"], hashlib.sha256(original).hexdigest())
            self.assertFalse(result["ok"])
            self.assertIn("Total PDF pages 2", result["errors"][0])


class PublishedStyleExamples(unittest.TestCase):
    def test_each_declared_relation_survives_the_authored_example(self) -> None:
        data = json.loads((ROOT / "examples/academic-style/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["cases"]), 10)
        for case in data["cases"]:
            for span in case["protected"]:
                with self.subTest(case=case["id"], span=span):
                    self.assertIn(span.casefold(), case["input"].casefold())
                    self.assertIn(span.casefold(), case["output"].casefold())
        unchanged = {c["id"] for c in data["cases"] if c["input"] == c["output"]}
        self.assertLessEqual({"retain-real-uncertainty", "keep-necessary-contrast", "no-fake-concretization"}, unchanged)


class DocumentDependencyTests(unittest.TestCase):
    def test_miktex_disables_installer_while_texlive_keeps_portable_options(self) -> None:
        for version, expected in (("MiKTeX-pdfTeX 4.10", ("--disable-installer",)), ("pdfTeX (TeX Live 2025)", ())):
            with self.subTest(version=version):
                render_examples.installer_flags.cache_clear()
                with patch.object(render_examples.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, version, "")):
                    self.assertEqual(render_examples.installer_flags("pdflatex"), expected)
        render_examples.installer_flags.cache_clear()


if __name__ == "__main__":
    unittest.main()
