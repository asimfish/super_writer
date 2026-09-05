"""Regressions for venue-compatible writing checks, not manuscript quality scores."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import artifact_check
import citation_bank_check
import section_economy_check
import word_guard
import latex_guard
import progress_check


def citation_table(count: int = 1, year: int = 2000) -> str:
    header = ["Candidate ID", "Reference/BibTeX", "Year", "Recency", "Supports Section",
              "Support Claim Sentence", "Why This Paper Fits", "Source", "Source Channel",
              "Verified", "Verification Note"]
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    for index in range(count):
        row = [str(index), "@article{synthetic" + str(index) + ",title={Test fixture}}",
               str(year), "foundational", "Introduction",
               "This locally supplied synthetic citation exists only to test collection policy, not a scientific claim.",
               "Bounded policy fixture.", "local", "local", "yes", "Synthetic test only."]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def manuscript(count: int) -> str:
    body = "This paragraph describes evidence and its limitations. " * 30
    return "\\begin{document}\n" + "\n".join(
        "\\section{Section " + str(index) + "}\n" + body for index in range(count)
    ) + "\n\\end{document}\n"


class WritingContractTests(unittest.TestCase):
    def run_cli(self, script: str, args: list[str], cwd: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *args], cwd=cwd,
            capture_output=True, text=True, encoding="utf-8", timeout=30,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_official_author_date_styles_are_not_rewritten_to_numeric(self) -> None:
        for style in ("plainnat", "icml2026", "iclr2026_conference", "acl_natbib",
                      "styles/icml2026", "styles/iclr2026_conference"):
            with self.subTest(style=style):
                tex = "\\bibliographystyle{" + style + "}"
                self.assertIsNone(word_guard.author_year_citation_finding("Prior work (Samuel, 1959).", tex))

    def test_numeric_source_still_rejects_author_date_word_export(self) -> None:
        message = word_guard.citation_style_finding(
            "Prior work (Samuel, 1959).", "\\bibliographystyle{unsrt}",
        )
        self.assertIn("mismatch", message.lower())

    def test_cvpr_numeric_source_still_rejects_author_date_word_export(self) -> None:
        self.assertIsNotNone(word_guard.citation_style_finding(
            "Prior work (Samuel, 1959).", "\\bibliographystyle{ieeenat_fullname}"))

    def test_handwritten_author_year_reference_is_not_a_numeric_style_requirement(self) -> None:
        findings = latex_guard.check_citation_format("\\begin{document}\nPrior work (Samuel, 1959).\n\\end{document}")
        self.assertTrue(findings)
        self.assertTrue(all(item.severity == "warning" for item in findings))

    def test_native_author_year_commands_do_not_trigger_format_findings(self) -> None:
        source = "\\begin{document}\nPrior work \\citep{samuel1959}.\n\\end{document}"
        self.assertEqual(latex_guard.check_citation_format(source), [])

    def test_final_gate_passes_only_explicit_editorial_policies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "final_paper").mkdir()
            (root / "final_paper/main.tex").write_text(manuscript(7), encoding="utf-8")
            for config, enforce in (({}, False), ({"max_sections": 8, "citation_enforce_heuristics": True}, True)):
                with self.subTest(config=config), patch.object(progress_check, "_run_script", return_value=(0, "", "")) as runner:
                    progress_check._run_final_audit_gate(root, config)
                    calls = {call.args[1]: call.args[2] for call in runner.call_args_list}
                    self.assertEqual("--max-sections" in calls["section_economy_check.py"], enforce)
                    self.assertEqual("--enforce-heuristics" in calls["citation_bank_check.py"], enforce)

    def test_final_gate_does_not_silently_replace_an_invalid_explicit_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "final_paper").mkdir()
            (root / "final_paper/main.tex").write_text(manuscript(1), encoding="utf-8")
            with patch.object(progress_check, "_run_script", return_value=(0, "", "")):
                ok, _, failures = progress_check._run_final_audit_gate(root, {"max_sections": "invalid"})
            self.assertFalse(ok)
            self.assertIn("max_sections must be a positive JSON integer", failures)

    def test_invalid_collection_arguments_fail_without_a_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for args in (["--recent-ratio", "nan"], ["--recent-ratio", "1.1"], ["--target-count", "0"]):
                with self.subTest(args=args):
                    result = self.run_cli("citation_bank_check.py", args, root)
                    self.assertEqual(result.returncode, 2)
                    self.assertNotIn("Traceback", result.stderr)

    def test_seven_sections_are_advisory_without_an_explicit_budget(self) -> None:
        with tempfile.TemporaryDirectory(prefix="writer section ") as temporary:
            root = Path(temporary)
            source = root / "paper.tex"
            source.write_text(manuscript(7), encoding="utf-8")
            result = self.run_cli("section_economy_check.py", [str(source), "--json"], root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["section_count"], 7)
            self.assertTrue(any(f["severity"] == "warning" for f in report["findings"]))

    def test_explicit_section_budget_remains_enforced(self) -> None:
        count, findings = section_economy_check.check(manuscript(7), 6)
        self.assertEqual(count, 7)
        self.assertTrue(any(f.severity == "error" for f in findings))

    def test_appendix_and_comments_do_not_consume_body_section_budget(self) -> None:
        source = manuscript(6).replace("\\end{document}",
            "% \\section{Not a section}\n\\appendix\n\\section{Additional proofs}\n\\end{document}")
        count, findings = section_economy_check.check(source, 6)
        self.assertEqual(count, 6)
        self.assertFalse(any(f.severity == "error" for f in findings))

    def test_invalid_section_budget_fails_with_a_cli_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "paper.tex"
            source.write_text(manuscript(1), encoding="utf-8")
            result = self.run_cli("section_economy_check.py", [str(source), "--max-sections", "0"], root)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_foundational_small_bank_has_advisories_not_quality_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "citation_support_bank.md"
            path.write_text(citation_table(), encoding="utf-8")
            result = citation_bank_check.validate(path, 20, 3, 3, 0.8)
            self.assertTrue(result.ok, result.findings)
            self.assertEqual(len(result.warnings), 2)
            issues, warnings = artifact_check.validate_citation_support_bank(root, {})
            self.assertEqual(issues, [])
            self.assertEqual(len(warnings), 2)

    def test_explicit_collection_policy_can_block_the_same_bank(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "citation_support_bank.md"
            path.write_text(citation_table(), encoding="utf-8")
            result = self.run_cli("citation_bank_check.py", [str(path), "--enforce-heuristics", "--json"], root)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(json.loads(result.stdout)["ok"])
            issues, warnings = artifact_check.validate_citation_support_bank(
                root, {"citation_enforce_heuristics": True},
            )
            self.assertEqual(len(issues), 2)
            self.assertEqual(warnings, [])

    def test_empty_bank_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "citation_support_bank.md"
            path.write_text(citation_table(0), encoding="utf-8")
            self.assertFalse(citation_bank_check.validate(path, 20, 3, 3, 0.8).ok)
            issues, _ = artifact_check.validate_citation_support_bank(root, {})
            self.assertTrue(any("no" in message.lower() and "row" in message.lower() for message in issues))

    def test_citation_rows_after_the_collection_target_are_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "citation_support_bank.md"
            path.write_text(citation_table(3, 2026) + "| broken | short |\n", encoding="utf-8")
            result = citation_bank_check.validate(path, 1, 3, 3, 0.8)
            self.assertFalse(result.ok)
            issues, _ = artifact_check.validate_citation_support_bank(root, {"citation_target_count": 1})
            self.assertTrue(any("weak rows" in message for message in issues))


if __name__ == "__main__":
    unittest.main()
