"""Release regressions for citation privacy, preference scope, and DOCX safety.

Run with Python >= 3.10: python -B -m unittest discover -s tests -p test_release_safety.py -v
All inputs are synthetic. Network entry points are blocked even when a fake
Crossref collaborator is supplied. Only temporary project/preferences files move.
"""

from __future__ import annotations

from contextlib import ExitStack, redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
from urllib.parse import parse_qs, unquote, urlsplit
from xml.etree import ElementTree
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_TITLE = "Public benchmark methods for synthetic experiments"
PUBLIC_REFERENCE = f'Smith, J. (2024). "{PUBLIC_TITLE}".'
PUBLIC_DOI = "10.5555/public-record"
PRIVATE_DOI = "10.1234/private-sentinel"
PRIVATE_CLAIM = f"UNPUBLISHED_SUPPORT_SENTINEL contains private results {PRIVATE_DOI}"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


class ReleaseSafetyFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.base = Path(self.stack.enter_context(
            tempfile.TemporaryDirectory(prefix="writer release safety ")
        )).resolve()
        previous_cwd = Path.cwd()
        os.chdir(self.base)
        self.stack.callback(os.chdir, previous_cwd)
        self.preferences = self.base / "isolated preferences"
        self.stack.enter_context(mock.patch.dict(os.environ, {
            "HOME": str(self.base / "home"),
            "USERPROFILE": str(self.base / "home"),
            "PAPERSPINE_CONFIG_HOME": str(self.preferences),
        }))
        self.stack.enter_context(mock.patch.object(sys, "dont_write_bytecode", True))
        self.network = [self.stack.enter_context(mock.patch(
            target, side_effect=AssertionError("Actual network access is forbidden")
        )) for target in (
            "urllib.request.urlopen", "socket.create_connection",
            "socket.socket.connect", "socket.getaddrinfo",
        )]

    def tearDown(self) -> None:
        for entrypoint in self.network:
            entrypoint.assert_not_called()

    def runtime(self, name: str):
        module_name = f"_release_safety_{name}"
        spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        self.stack.enter_context(mock.patch.dict(sys.modules, {module_name: module}))
        with mock.patch.object(sys, "path", [str(ROOT / "scripts"), *sys.path]):
            spec.loader.exec_module(module)
        return module

    def bank(self, header: list[str], row: list[str]) -> Path:
        path = self.base / "citation_support_bank.md"
        lines = [header, ["---"] * len(header), row]
        path.write_text("\n".join("| " + " | ".join(cells) + " |" for cells in lines) + "\n",
                        encoding="utf-8")
        return path


class EnglishCitationPrivacyTests(ReleaseSafetyFixture):
    def setUp(self) -> None:
        super().setUp()
        self.verifier = self.runtime("citation_verification_en")

    def verify(self, header: list[str], row: list[str], **kwargs):
        fetcher = mock.Mock(return_value=None)
        result = self.verifier.verify_citation(self.bank(header, row), _fetcher=fetcher, **kwargs)
        return result, [call.args[0] for call in fetcher.call_args_list]

    def test_reference_aliases_query_only_public_reference_text(self) -> None:
        for header in ("Reference", "Reference/BibTeX", "BibTeX", "Citation"):
            with self.subTest(header=header):
                result, urls = self.verify(
                    ["Candidate ID", "Support Claim Sentence", header, "Source Channel"],
                    ["C1", PRIVATE_CLAIM, PUBLIC_REFERENCE, "web"],
                )
                self.assertEqual(len(urls), 1)
                parsed = urlsplit(urls[0])
                self.assertEqual((parsed.scheme, parsed.netloc, parsed.path),
                                 ("https", "api.crossref.org", "/works"))
                query = parse_qs(parsed.query)["query.bibliographic"][0]
                self.assertIn(PUBLIC_TITLE, query)
                self.assertNotIn("UNPUBLISHED_SUPPORT_SENTINEL", unquote(urls[0]))
                self.assertNotIn(PRIVATE_DOI, unquote(urls[0]))
                self.assertEqual(result.entries[0].reference_text, PUBLIC_REFERENCE)

    def test_doi_lookup_uses_reference_field_not_support_doi(self) -> None:
        _, urls = self.verify(
            ["Candidate ID", "Support Claim Sentence", "Reference", "Source Channel"],
            ["C1", PRIVATE_CLAIM, f"{PUBLIC_REFERENCE} DOI: {PUBLIC_DOI}", "web"],
        )
        self.assertEqual([unquote(urlsplit(url).path) for url in urls], [f"/works/{PUBLIC_DOI}"])

    def test_missing_reference_column_never_exports_support_text(self) -> None:
        _, urls = self.verify(
            ["Candidate ID", "Support Claim Sentence", "Source Channel"],
            ["C1", PRIVATE_CLAIM, "web"],
        )
        self.assertEqual(urls, [], "A missing reference column must not fall back to the whole row")

    def test_empty_reference_cell_never_exports_support_text(self) -> None:
        _, urls = self.verify(
            ["Candidate ID", "Support Claim Sentence", "Reference", "Source Channel"],
            ["C1", PRIVATE_CLAIM, "", "web"],
        )
        self.assertEqual(urls, [])

    def test_short_row_missing_reference_cell_never_exports_support_text(self) -> None:
        _, urls = self.verify(
            ["Candidate ID", "Support Claim Sentence", "Source Channel", "Reference"],
            ["C1", PRIVATE_CLAIM, "web"],
        )
        self.assertEqual(urls, [], "A missing cell must not be reconstructed from neighboring cells")

    def test_any_row_width_mismatch_is_offline_even_with_a_reference(self) -> None:
        header = ["Candidate ID", "Reference", "Support Claim Sentence", "Source Channel"]
        for row in (["C1", PUBLIC_REFERENCE, PRIVATE_CLAIM],
                    ["C1", PUBLIC_REFERENCE, PRIVATE_CLAIM, "web", "unexpected extra cell"]):
            with self.subTest(width=len(row)):
                _, urls = self.verify(header, row)
                self.assertEqual(urls, [], "Ambiguous row alignment must not initiate any request")

    def test_misleading_column_names_are_not_reference_columns(self) -> None:
        for misleading in ("Citation Claim", "Reference Notes", "BibTeX Support Sentence"):
            with self.subTest(header=misleading):
                _, urls = self.verify(
                    ["Candidate ID", misleading, "Source Channel"], ["C1", PRIVATE_CLAIM, "web"],
                )
                self.assertEqual(urls, [], "Substring header matches must not authorize external lookup")

    def test_local_and_no_api_still_never_call_fetcher(self) -> None:
        for channel, no_api in (("local", False), ("web", True)):
            with self.subTest(channel=channel, no_api=no_api):
                result, urls = self.verify(
                    ["Candidate ID", "Reference", "Support Claim Sentence", "Source Channel"],
                    ["C1", f"{PUBLIC_REFERENCE} {PUBLIC_DOI}", PRIVATE_CLAIM, channel], no_api=no_api,
                )
                self.assertEqual(urls, [])
                self.assertEqual(result.checked_count, 0)

    def test_no_api_cli_main_never_calls_crossref(self) -> None:
        path = self.bank(["Candidate ID", "Reference", "Source Channel"],
                         ["C1", f"{PUBLIC_REFERENCE} {PUBLIC_DOI}", "web"])
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["citation_verification_en.py", str(path), "--no-api", "--json"]), \
                mock.patch.object(self.verifier, "_fetch_crossref_json", return_value=None) as fetcher, \
                redirect_stdout(output):
            returncode = self.verifier.main()
        self.assertEqual(returncode, 0)
        fetcher.assert_not_called()
        self.assertEqual(json.loads(output.getvalue())["checked_count"], 0)


class CitationQualityPrivacyTests(ReleaseSafetyFixture):
    def setUp(self) -> None:
        super().setUp()
        self.audit = self.runtime("citation_quality_audit")

    def audit_row(self, reference_header="Reference", reference=PUBLIC_REFERENCE,
                  claim=PRIVATE_CLAIM, doi="", source="", no_api=False):
        self.bank(["Candidate ID", "Support Claim Sentence", reference_header,
                   "Year", "DOI", "Source", "Source Channel"],
                  ["C1", claim, reference, "2024", doi, source, "web"])
        with mock.patch.object(self.audit, "fetch_crossref", return_value=None) as fetcher:
            report = self.audit.audit_citations(self.base, no_api=no_api, timeout=1, delay=0)
        return report, [call.args[0] for call in fetcher.call_args_list]

    def test_support_sentence_doi_is_not_extracted_or_sent(self) -> None:
        report, sent = self.audit_row()
        parsed = self.audit.parse_citation_rows(self.base / "citation_support_bank.md")
        self.assertEqual((sent, [row["doi"] for row in parsed], [entry.doi for entry in report.entries]),
                         ([], [""], [""]), "Support prose is not a source of bibliographic identifiers")

    def test_real_dois_in_explicit_bibliographic_fields_remain_valid(self) -> None:
        for field in ("Reference", "Reference/BibTeX", "Citation", "BibTeX", "DOI", "Source"):
            with self.subTest(field=field):
                kwargs = {"claim": "Synthetic support statement without identifiers."}
                if field == "DOI":
                    kwargs["doi"] = PUBLIC_DOI
                elif field == "Source":
                    kwargs["source"] = f"https://doi.org/{PUBLIC_DOI}"
                else:
                    kwargs.update(reference_header=field, reference=f"{PUBLIC_REFERENCE} {PUBLIC_DOI}")
                report, sent = self.audit_row(**kwargs)
                self.assertEqual(sent, [PUBLIC_DOI])
                self.assertEqual(report.entries[0].doi, PUBLIC_DOI)

    def test_public_source_doi_is_not_shadowed_by_private_support_doi(self) -> None:
        report, sent = self.audit_row(source=f"https://doi.org/{PUBLIC_DOI}")
        self.assertEqual(sent, [PUBLIC_DOI])
        self.assertEqual(report.entries[0].doi, PUBLIC_DOI)

    def test_missing_reference_schema_does_not_use_positional_fallback(self) -> None:
        report, sent = self.audit_row(reference_header="Citation Claim", reference="Private notes")
        self.assertEqual(sent, [], "Misleading headers must not select a citation table by substring")
        self.assertFalse(any(entry.reference == PRIVATE_CLAIM for entry in report.entries))

    def test_no_api_remains_offline(self) -> None:
        _, sent = self.audit_row(reference=f"{PUBLIC_REFERENCE} {PUBLIC_DOI}", no_api=True)
        self.assertEqual(sent, [])


class ChineseCitationPrivacyTests(ReleaseSafetyFixture):
    def setUp(self) -> None:
        super().setUp()
        self.verifier = self.runtime("citation_verification_zh")
        self.reference = ("\u5f20\u4e09, \u674e\u56db. \u5408\u6210\u57fa\u51c6\u7814\u7a76. "
                          "\u300a\u5408\u6210\u671f\u520a\u300b, 2024. DOI: " + PUBLIC_DOI)
        self.private_claim = ("\u672a\u53d1\u8868\u652f\u6301\u53e5 "
                              "\u300a\u5185\u90e8\u5b9e\u9a8c\u7b14\u8bb0\u300b 2025 " + PRIVATE_DOI)

    def test_reordered_reference_uses_only_its_own_doi(self) -> None:
        self.bank(["Candidate ID", "Support Claim Sentence", "Source Channel", "Reference"],
                  ["C1", self.private_claim, "web", self.reference])
        with mock.patch.object(self.verifier, "verify_doi", return_value=True) as fetcher, \
                mock.patch.object(self.verifier.time, "sleep"):
            result = self.verifier.check_citation_bank_zh(self.base)
        self.assertEqual([call.args[0] for call in fetcher.call_args_list], [PUBLIC_DOI])
        self.assertTrue(result.ok)
        self.assertEqual(result.checks[0].reference_text, self.reference)

    def test_missing_or_empty_reference_returns_not_ok_without_network(self) -> None:
        for empty_reference in (False, True):
            with self.subTest(empty_reference=empty_reference):
                header = ["Candidate ID", "Support Claim Sentence", "Source Channel"]
                row = ["C1", self.private_claim, "web"]
                if empty_reference:
                    header.append("Reference")
                    row.append("")
                self.bank(header, row)
                with mock.patch.object(self.verifier, "verify_doi", return_value=True) as fetcher, \
                        mock.patch.object(self.verifier.time, "sleep"):
                    result = self.verifier.check_citation_bank_zh(self.base)
                fetcher.assert_not_called()
                self.assertFalse(result.ok)


class GlobalPreferenceScopeTests(ReleaseSafetyFixture):
    def setUp(self) -> None:
        super().setUp()
        self.wizard = self.runtime("intake_wizard")

    def run_main(self, *args: str) -> int:
        with mock.patch.object(sys, "argv", ["intake_wizard.py", *args]), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return self.wizard.main()

    def existing_project(self) -> tuple[Path, dict[str, bytes]]:
        project = self.base / "paper_rewriting_output"
        project.mkdir()
        original = {
            "paper_spine_config.json": b'{ "workflow": "build_from_materials", "extra": 42 }\r\n',
            "paper_spine_config.md": b"# User-owned project config\r\n\r\nKeep these exact bytes.\r\n",
        }
        for name, data in original.items():
            (project / name).write_bytes(data)
        return project, original

    def assert_preferences_saved(self) -> None:
        data = json.loads((self.preferences / "config.json").read_text(encoding="utf-8"))
        self.assertEqual(data["ui_language"], "en")

    def test_noninteractive_global_setup_does_not_create_project_config(self) -> None:
        self.assertEqual(self.run_main("--setup-global", "--no-interactive", "--ui-language", "en"), 0)
        self.assert_preferences_saved()
        self.assertEqual(set(self.base.iterdir()), {self.preferences})

    def test_noninteractive_global_setup_preserves_existing_project_bytes(self) -> None:
        project, original = self.existing_project()
        self.assertEqual(self.run_main("--setup-global", "--no-interactive", "--ui-language", "en"), 0)
        self.assert_preferences_saved()
        self.assertEqual({path.name: path.read_bytes() for path in project.iterdir()}, original)

    def test_classic_global_setup_never_enters_project_prompts(self) -> None:
        project, original = self.existing_project()
        chosen = []

        def choose(key, *args, **kwargs):
            chosen.append(key)
            if key != "ui_language":
                self.fail(f"Global preference setup entered project prompt: {key}")
            return "en"

        stdin = io.StringIO("2\n")
        with mock.patch.object(stdin, "isatty", return_value=True), \
                mock.patch.object(sys, "stdin", stdin), \
                mock.patch.object(self.wizard, "choose", side_effect=choose), \
                mock.patch("builtins.input", side_effect=AssertionError("Unexpected project text prompt")):
            self.assertEqual(self.run_main("--setup-global", "--classic-input", "--ui-language", "zh"), 0)
        self.assertEqual(chosen, ["ui_language"])
        self.assert_preferences_saved()
        self.assertEqual({path.name: path.read_bytes() for path in project.iterdir()}, original)


class DocxFontSafetyTests(ReleaseSafetyFixture):
    def test_font_fix_changes_styles_and_theme_only_and_retains_original_backup(self) -> None:
        guard = self.runtime("word_guard")
        document = (f'<?xml version="1.0" encoding="UTF-8"?>\r\n<w:document xmlns:w="{W_NS}">'
                    '<w:body><w:p><w:r><w:t>42</w:t></w:r></w:p>'
                    '<w:p><w:r><w:t>2024</w:t></w:r></w:p>'
                    '<w:p><w:r><w:t>2025</w:t></w:r></w:p>'
                    '<w:sectPr/></w:body></w:document>').encode("utf-8")
        styles = (f'<w:styles xmlns:w="{W_NS}"><w:docDefaults><w:rPrDefault><w:rPr>'
                  '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial"/>'
                  '</w:rPr></w:rPrDefault></w:docDefaults></w:styles>').encode("utf-8")
        theme = (f'<a:theme xmlns:a="{A_NS}" name="Synthetic"><a:themeElements><a:fontScheme name="Fixture">'
                 '<a:majorFont><a:latin typeface="Calibri"/><a:ea typeface="Arial"/></a:majorFont>'
                 '<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface="Arial"/></a:minorFont>'
                 '</a:fontScheme></a:themeElements></a:theme>').encode("utf-8")
        parts = {
            "[Content_Types].xml": b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                                   b'<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                                   b'<Default Extension="xml" ContentType="application/xml"/>'
                                   b'<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                                   b'<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                                   b'<Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/></Types>',
            "_rels/.rels": b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                            b'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>',
            "word/document.xml": document,
            "word/styles.xml": styles,
            "word/theme/theme1.xml": theme,
            "word/_rels/document.xml.rels": b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                                             b'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                                             b'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/></Relationships>',
        }
        for language in ("en", "zh"):
            with self.subTest(language=language):
                path = self.base / f"synthetic {language}.docx"
                with zipfile.ZipFile(path, "w") as bundle:
                    for name, data in parts.items():
                        bundle.writestr(name, data)
                original_archive = path.read_bytes()
                self.assertTrue(guard.fix_docx_fonts(path, language))
                backup = path.with_suffix(".docx.bak_fonts")
                self.assertEqual(backup.read_bytes(), original_archive)
                guard.fix_docx_fonts(path, language)
                self.assertEqual(backup.read_bytes(), original_archive, "A repeat fix must retain the original backup")
                with zipfile.ZipFile(path) as bundle:
                    updated = {name: bundle.read(name) for name in bundle.namelist()}
                self.assertNotEqual(updated["word/styles.xml"], styles)
                self.assertNotEqual(updated["word/theme/theme1.xml"], theme)
                fonts = ElementTree.fromstring(updated["word/styles.xml"]).find(
                    ".//w:docDefaults/w:rPrDefault/w:rPr/w:rFonts", {"w": W_NS})
                self.assertIsNotNone(fonts)
                self.assertEqual(fonts.get(f"{{{W_NS}}}ascii"), "Times New Roman")
                self.assertEqual(fonts.get(f"{{{W_NS}}}eastAsia"), "SimSun" if language == "zh" else "Times New Roman")
                latin = ElementTree.fromstring(updated["word/theme/theme1.xml"]).findall(".//a:latin", {"a": A_NS})
                self.assertEqual([node.get("typeface") for node in latin], ["Times New Roman", "Times New Roman"])
                self.assertEqual(set(updated), set(parts))
                for name, data in parts.items():
                    if name not in {"word/styles.xml", "word/theme/theme1.xml"}:
                        self.assertEqual(updated[name], data, f"Font-only repair modified {name}")


if __name__ == "__main__":
    unittest.main()
