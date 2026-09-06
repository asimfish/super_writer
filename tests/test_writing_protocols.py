"""Bounded writing-resource contracts, not model writing-quality scores."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import writing_guide
sys.path.insert(0, str(ROOT / "tools"))
import import_writing_library
import check_table_templates


def cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROOT / "scripts/writing_guide.py"), *args],
                          cwd=tempfile.gettempdir(), capture_output=True, text=True,
                          encoding="utf-8", timeout=30)


class WritingGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = writing_guide.load_index()

    def test_list_distinguishes_protocols_variants_and_table_assets(self) -> None:
        result = cli("--list", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(len(report["guides"]), 16)
        self.assertEqual(sum(len(g["variants"]) for g in report["guides"]), 30)
        self.assertEqual(sum(g["table_file"] is not None for g in report["guides"]), 5)
        self.assertNotIn("review", {g["id"] for g in report["guides"]})

    def test_chinese_alias_selects_one_guide_and_keeps_evidence_contract(self) -> None:
        result = cli("引言", "--variant", "theory-analysis", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["guide"]["id"], "introduction")
        self.assertEqual([t["id"] for t in report["guide"]["templates"]], ["theory-analysis"])
        self.assertTrue(report["guide"]["inputs"])
        self.assertTrue(report["guide"]["avoid"])
        self.assertTrue(report["guide"]["verification"])
        self.assertIn("missing", " ".join(report["application_contract"]))

    def test_undersized_budget_fails_without_partial_output(self) -> None:
        result = cli("experiments", "--max-chars", "512", "--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("complete", result.stderr)

    def test_unknown_or_conflicting_selectors_fail_closed(self) -> None:
        for args in (("review",), ("unknown",), ("abstract", "--variant", "real-robot"),
                     ("--list", "abstract"), ("--list", "--variant", "theory"),
                     ("../outside",), ("x" * 257,), ("abstract", "--max-chars", "50001")):
            with self.subTest(args=args):
                result = cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_analysis_marks_unbundled_card_without_inventing_content(self) -> None:
        result = cli("experiments.analysis", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("general.phrase.results-suggest.001", report["unbundled_card_ids"])
        self.assertNotIn("general.phrase.results-suggest.001", report["available_card_ids"])

    def test_table_lookup_keeps_placeholders_and_does_not_write(self) -> None:
        result = cli("效率表", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["table"]["file"], "efficiency.tex")
        self.assertIn("SL_VALUE", report["table"]["latex"])
        self.assertIn("SL_HARDWARE", report["table"]["latex"])
        self.assertIn("booktabs", report["table"]["requires"])

    def test_every_alias_and_variant_preserves_all_checks_within_default_budget(self) -> None:
        for guide in self.index["guides"]:
            for alias in guide["aliases"]:
                self.assertEqual(writing_guide.report_for(self.index, alias, None)["guide"], guide)
            for variant in guide["templates"]:
                with self.subTest(guide=guide["id"], variant=variant["id"]):
                    report = writing_guide.report_for(self.index, guide["id"], variant["id"])
                    for field in ("inputs", "avoid", "verification", "moves", "domain_overlays"):
                        self.assertEqual(report["guide"].get(field), guide.get(field))
                    markdown = writing_guide.render(report, "markdown")
                    for text in (*guide["inputs"], *guide["avoid"], *guide["verification"],
                                 *(check for move in guide["moves"] for check in move["checks"]),
                                 *(check for overlay in guide.get("domain_overlays", []) for check in overlay["checks"])):
                        self.assertIn(text, markdown)
                    self.assertLessEqual(len(markdown) + 1, 16000)
                    self.assertLessEqual(len(writing_guide.render(report, "json")) + 1, 16000)
            self.assertLessEqual(len(writing_guide.render(writing_guide.report_for(self.index, guide["id"], None), "json")) + 1, 16000)

    def test_related_card_availability_matches_actual_bundled_corpus(self) -> None:
        cards = json.loads((ROOT / "references/writing-library.json").read_text(encoding="utf-8"))
        ids = {entry["id"] for entry in cards["entries"]}
        self.assertEqual(set(self.index["available_card_ids"]), ids)
        for guide in self.index["guides"]:
            report = writing_guide.report_for(self.index, guide["id"], None)
            self.assertEqual(set(report["available_card_ids"]), set(guide["related_entry_ids"]) & ids)
            self.assertEqual(set(report["unbundled_card_ids"]), set(guide["related_entry_ids"]) - ids)

    def test_table_hashes_and_license_match_import_metadata(self) -> None:
        license_bytes = (ROOT / "references/table-templates/LICENSE").read_bytes()
        self.assertEqual(hashlib.sha256(license_bytes).hexdigest(), import_writing_library.PINS["LICENSE"])
        for template in self.index["tables"]:
            table = writing_guide.table_resource(template)
            self.assertEqual(template["upstream_sha256"], import_writing_library.PINS[template["upstream_path"]])
            self.assertIn("SL_", table["latex"])
            self.assertNotIn(r"\vspace", table["latex"])
            self.assertNotIn(r"\resizebox", table["latex"])

    def test_table_path_and_digest_fail_closed(self) -> None:
        template = self.index["tables"][0]
        for filename in ("../LICENSE", "/etc/passwd", r"..\LICENSE", "other.tex"):
            with self.subTest(filename=filename), self.assertRaisesRegex(ValueError, "allowlisted"):
                writing_guide.table_resource({**template, "file": filename})
        with tempfile.TemporaryDirectory() as temporary:
            references = Path(temporary)
            directory = references / "table-templates"
            directory.mkdir()
            target = directory / template["file"]
            with self.assertRaisesRegex(ValueError, "regular"):
                writing_guide.table_resource(template, references)
            target.write_bytes(b"changed table")
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                writing_guide.table_resource(template, references)
            target.write_bytes(b"x" * (64 * 1024 + 1))
            with self.assertRaisesRegex(ValueError, "size limit"):
                writing_guide.table_resource(template, references)

    def test_symlink_table_or_directory_is_rejected(self) -> None:
        template = self.index["tables"][0]
        with tempfile.TemporaryDirectory() as temporary:
            references = Path(temporary)
            directory = references / "table-templates"
            directory.mkdir()
            target = directory / template["file"]
            try:
                target.symlink_to(ROOT / "references/table-templates" / template["file"])
            except OSError as exc:
                self.skipTest(f"Symlink privilege unavailable: {exc}")
            with self.assertRaisesRegex(ValueError, "regular"):
                writing_guide.table_resource(template, references)
            target.unlink()
            directory.rmdir()
            directory.symlink_to(ROOT / "references/table-templates", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                writing_guide.table_resource(template, references)

    def test_import_failure_never_writes_partial_generated_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(import_writing_library, "ROOT", root), \
                 patch.object(sys, "argv", ["import_writing_library.py", "--write"]), \
                 patch.object(import_writing_library, "fetch", side_effect=[b"{}", ValueError("changed pin")]), \
                 self.assertRaises(SystemExit) as raised:
                import_writing_library.main()
            self.assertEqual(raised.exception.code, 1)
            self.assertEqual(list(root.iterdir()), [])

    def test_reproduction_preserves_original_protocol_records(self) -> None:
        cards = json.loads((ROOT / "references/writing-library.json").read_text(encoding="utf-8"))
        tables = {t["file"]: (ROOT / "references/table-templates" / t["file"]).read_bytes() for t in self.index["tables"]}
        index = {"writing_guides": {"guides": [*self.index["guides"], {"id": "review"}]},
                 "table_templates": {"templates": [{key: t[key] for key in ("id", "label", "file", "guide_id", "requires")}
                                                   for t in self.index["tables"]]}}
        self.assertEqual(import_writing_library.curate_protocols(index, cards, tables), self.index)
        index["writing_guides"]["guides"].append(self.index["guides"][0])
        with self.assertRaisesRegex(ValueError, "inventory changed"):
            import_writing_library.curate_protocols(index, cards, tables)

    def test_new_related_work_cards_are_explicit_original_sentence_patterns(self) -> None:
        cards = json.loads((ROOT / "references/writing-library.json").read_text(encoding="utf-8"))
        entries = {entry["id"]: entry for entry in cards["entries"]}
        for ident in ("emb.sentence-pattern.related-work-memory-geometry.001",
                      "rl.sentence-pattern.related-work-regime.001",
                      "wm.sentence-pattern.related-work-generation-control.001"):
            self.assertEqual(entries[ident]["kind"], "sentence_pattern")
            self.assertEqual(entries[ident]["provenance"]["type"], "original_pattern")
            self.assertTrue(entries[ident]["avoid"])

    def test_render_fixtures_are_explicitly_synthetic_and_layout_specific(self) -> None:
        for template in self.index["tables"]:
            source = writing_guide.table_resource(template)["latex"]
            single = check_table_templates.fixture(source, "single-column")
            wide = check_table_templates.fixture(source, "two-column-wide")
            self.assertIn("SYNTHETIC RENDER FIXTURE (not measured results)", single)
            self.assertIn(r"\begin{table}", single)
            self.assertIn(r"\begin{table*}", wide)
            self.assertIn("twocolumn", wide)
            self.assertIn("SL_VALUE", source)
        with self.assertRaisesRegex(ValueError, "Unknown fixture placeholders"):
            check_table_templates.fixture("SL_UNREVIEWED", "single-column")
        with self.assertRaisesRegex(ValueError, "Unknown fixture layout"):
            check_table_templates.fixture("", "narrow-column")


if __name__ == "__main__":
    unittest.main()
