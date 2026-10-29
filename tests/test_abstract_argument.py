"""Developmental artifact contracts, not automatic judgments of writing quality."""

from __future__ import annotations

import copy
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evals/abstract-argument"
SPEC = importlib.util.spec_from_file_location("argument_comparison", ARTIFACT / "render.py")
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Elements(HTMLParser):
    def __init__(self, value: str):
        super().__init__()
        self.elements, self.text = [], []
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class AbstractArgumentTests(unittest.TestCase):
    def setUp(self):
        self.candidates = load(ARTIFACT / "candidates.json")
        self.baseline = load(ARTIFACT / "baseline.json")
        self.authors = load(ROOT / "evals/abstract-five/results.json")
        self.audit = load(ARTIFACT / "audit.json")
        self.corrections = load(ARTIFACT / "corrections.json")
        self.recheck = load(ARTIFACT / "correction-audit.json")

    def page(self):
        return RENDERER.render(self.candidates, self.baseline, self.authors, self.audit,
                               self.corrections, self.recheck)

    def test_five_candidates_use_preserved_facts_and_applicable_pattern_ids(self):
        expected = {"P01", "P02", "P03", "P04", "P05"}
        self.assertEqual([p["id"] for p in self.candidates["papers"]], sorted(expected))
        evidence = {p["id"]: {e["id"] for e in p["evidence"]}
                    for p in load(ARTIFACT / "evidence.json")["papers"]}
        catalog = {e["id"]: e for e in load(ROOT / "references/ai-writing-spec.json")["entries"]}
        for paper in self.candidates["papers"]:
            self.assertLessEqual(RENDERER.word_count(paper["text_en"]),
                                 self.candidates["generation"]["budget_max_words"])
            self.assertTrue(paper["text_zh"].strip())
            self.assertTrue(set(paper["evidence_ids"]) <= evidence[paper["id"]])
            self.assertTrue(1 <= len(paper["pattern_ids"]) <= 6)
            for ident in paper["pattern_ids"]:
                self.assertEqual(catalog[ident]["kind"], "sentence_pattern")
                self.assertIn("abstract", catalog[ident]["sections"])
            for selection in paper["selection"]:
                self.assertIn(selection["action"], {"retain", "summarize", "omit"})
                self.assertTrue(set(selection["evidence_ids"]) <= evidence[paper["id"]])
        self.assertEqual(self.candidates["status"], "developmental_candidates_not_a_blind_test")

    def test_baseline_counts_are_recounted_not_silently_relabelled(self):
        originals = {p["id"]: p for p in self.authors["papers"]}
        for paper in self.baseline["papers"]:
            self.assertEqual(paper["recounted_words"], RENDERER.word_count(paper["text_en"]))
            self.assertEqual(paper["old_displayed_words"], originals[paper["id"]]["ours_word_count"])
        self.assertIn("不是等预算", self.page())
        self.assertIn("不作为本轮的独立认证", self.page())

    def test_audit_is_separate_from_a_quality_or_human_certification(self):
        self.assertEqual({p["id"] for p in self.audit["papers"]},
                         {p["id"] for p in self.candidates["papers"]})
        self.assertIn("not human", self.audit["scope"])
        for paper in self.audit["papers"]:
            self.assertIn(paper["status"], {"no_issue_found_in_checked_claims", "issues_found",
                                          "unable_to_verify"})
            self.assertTrue(paper["readback_zh"].strip())
            self.assertTrue(paper["summary_zh"].strip())
            self.assertIn(paper["translation"]["status"], {"no_issue_found", "issues_found"})
            if paper["issues"]:
                self.assertEqual(paper["status"], "issues_found")

    def test_historical_outputs_keep_hashes_without_freezing_live_guides(self):
        receipt = load(ARTIFACT / "receipts.json")
        for name, expected in receipt["artifacts_sha256"].items():
            self.assertEqual(len(expected), 64)
            if name.startswith("evals/abstract-five/"):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected, name)
        self.assertEqual(receipt["quality_status"], "not_measured")
        for name, expected in receipt["retained_artifacts_sha256"].items():
            self.assertEqual(hashlib.sha256((ARTIFACT / name).read_bytes()).hexdigest(), expected, name)
        self.assertIn("source-derived", receipt["source_access_limits"])

    def test_html_reproduces_and_preserves_all_three_versions(self):
        output = self.page()
        self.assertEqual(output, (ARTIFACT / "comparison.html").read_text(encoding="utf-8"))
        parsed = Elements(output)
        sections = [a for tag, a in parsed.elements if tag == "section"]
        articles = [a for tag, a in parsed.elements if tag == "article"]
        self.assertEqual(len(sections), 5)
        self.assertEqual(len(articles), 15)
        text = "\n".join(parsed.text)
        for author, prior, new in zip(self.authors["papers"], self.baseline["papers"],
                                      self.candidates["papers"]):
            for value in (author["author_summary_zh"], author["ours_zh"], prior["text_en"],
                          new["text_zh"], new["text_en"], new["thesis_zh"]):
                self.assertIn(value, text)
            for value in new["progression_zh"]:
                self.assertIn(value, text)

    def test_navigation_offline_content_and_collapsed_evidence_notes(self):
        parsed = Elements(self.page())
        ids = {attrs["id"] for _, attrs in parsed.elements if "id" in attrs}
        for tag, attrs in parsed.elements:
            self.assertNotIn(tag, {"script", "img", "iframe", "link"})
            if tag == "a" and attrs.get("href", "").startswith("#"):
                self.assertIn(attrs["href"][1:], ids)
            if tag == "details":
                self.assertNotIn("open", attrs)

    def test_source_correction_preserves_raw_draft_and_rejects_stale_replacement(self):
        raw = next(p for p in self.candidates["papers"] if p["id"] == "P02")
        repair = self.corrections["papers"][0]
        fixed = RENDERER.corrected(raw, repair)
        self.assertNotIn("and textiles", fixed["text_en"])
        self.assertIn("about 463,000", fixed["text_en"])
        self.assertIn("and textiles", raw["text_en"])
        self.assertIn("约 463,000", fixed["text_zh"])
        self.assertIn("保留的首轮候选", self.page())
        self.assertIn(self.recheck["papers"][0]["summary_zh"], "\n".join(Elements(self.page()).text))
        for field in ("text_en", "text_zh"):
            wrong = {**raw, field: raw[field] + " changed"}
            with self.assertRaisesRegex(ValueError, "no longer matches"):
                RENDERER.corrected(wrong, repair)

    def test_prose_and_notes_are_escaped(self):
        candidate = copy.deepcopy(self.candidates)
        payload = '<script>alert("bad")</script> & <img src=x>'
        candidate["papers"][0]["text_zh"] = payload
        candidate["papers"][0]["author_notes_zh"] = [payload]
        output = RENDERER.render(candidate, self.baseline, self.authors)
        self.assertNotIn(payload, output)
        self.assertIn("&lt;script&gt;", output)
        self.assertIn(payload, "\n".join(Elements(output).text))


if __name__ == "__main__":
    unittest.main()
