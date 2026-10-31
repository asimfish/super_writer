"""Contracts for source-calibrated demonstrations, not a quality oracle."""

from __future__ import annotations

from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evals/abstract-natural"
SPEC = importlib.util.spec_from_file_location("natural_render", ARTIFACT / "render.py")
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)


class Elements(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.elements, self.text = [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class NaturalAbstractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ARTIFACT / "natural_candidates.json").read_text(encoding="utf-8"))

    def test_five_source_calibrated_candidates_have_shape_profiles(self):
        self.assertEqual([p["id"] for p in self.data["papers"]], ["P01", "P02", "P03", "P04", "P05"])
        self.assertEqual(self.data["status"], "developmental_source_calibrated_candidates_not_a_blind_test")
        for paper in self.data["papers"]:
            self.assertLessEqual(RENDER.word_count(paper["text_en"]), 180)
            self.assertTrue(paper["text_zh"].strip())
            self.assertEqual(set(paper["shape"]), {"opening", "progression", "abstraction", "ending"})
            self.assertTrue(all(paper["shape"].values()))
            self.assertTrue(paper["changes"].strip())

    def test_render_is_reproducible_and_keeps_three_versions(self):
        output = RENDER.render()
        self.assertEqual(output, (ARTIFACT / "comparison.html").read_text(encoding="utf-8"))
        parsed = Elements(output)
        self.assertEqual(len([x for x in parsed.elements if x[0] == "section"]), 5)
        self.assertEqual(len([x for x in parsed.elements if x[0] == "article"]), 15)
        text = "\n".join(parsed.text)
        for paper in self.data["papers"]:
            self.assertIn(paper["text_zh"], text)
            self.assertIn(paper["text_en"], text)
            for value in paper["shape"].values():
                self.assertIn(value, text)

    def test_page_is_offline_and_uses_source_links_only(self):
        output = RENDER.render()
        self.assertNotIn("<script", output.lower())
        self.assertNotIn("<img", output.lower())
        self.assertNotIn("fetch(", output.lower())
        for tag, attrs in Elements(output).elements:
            if tag == "a":
                self.assertTrue(attrs.get("href", "").startswith(("#", "https://")))

    def test_naturalized_chinese_avoids_known_english_chain_regression(self):
        text = "\n".join(p["text_zh"] for p in self.data["papers"])
        self.assertNotIn("在每项任务使用", text)
        self.assertNotIn("条件下，", text)
        self.assertIn("为什么需要音频", "\n".join(p["changes"] for p in self.data["papers"]))


if __name__ == "__main__":
    unittest.main()
