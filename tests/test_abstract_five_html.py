"""Presentation and corpus preservation checks, not a scientific fidelity audit."""

import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "evals/abstract-five"
SPEC = importlib.util.spec_from_file_location("abstract_five_html", ROOT / "render.py")
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class Markup(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.text = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class AbstractFiveHTMLTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
        self.html = renderer.render(self.data)
        self.markup = Markup(self.html)

    def test_generated_page_matches_committed_data(self):
        self.assertEqual(self.html, (ROOT / "comparison.html").read_text(encoding="utf-8"))

    def test_every_version_and_observation_is_preserved(self):
        text = "".join(self.markup.text)
        for paper in self.data["papers"]:
            for key in ("title", "author_summary_zh", "ours_zh"):
                self.assertIn(paper[key], text)
            for value in paper["comparison"].values():
                self.assertIn(value, text)
            for count in (paper["author_word_count"], paper["ours_word_count"]):
                self.assertIn(f"英文 {count} 词", text)

    def test_all_sections_have_navigation_sources_and_collapsed_notes(self):
        tags = self.markup.tags
        self.assertEqual(sum(tag == "article" for tag, _ in tags), 10)
        self.assertEqual(sum(tag == "section" for tag, _ in tags), 5)
        notes = [attrs for tag, attrs in tags if tag == "details"]
        self.assertEqual(len(notes), 5)
        self.assertTrue(all("open" not in attrs for attrs in notes))
        for paper in self.data["papers"]:
            self.assertTrue(any(tag == "section" and attrs.get("id") == paper["id"] for tag, attrs in tags))
            self.assertTrue(any(tag == "a" and attrs.get("href") == "#" + paper["id"] for tag, attrs in tags))
            self.assertTrue(any(tag == "a" and attrs.get("href") == paper["source_url"] for tag, attrs in tags))

    def test_page_is_offline_and_labels_the_comparator_fairly(self):
        self.assertFalse(any(tag in ("script", "iframe", "img") for tag, _ in self.markup.tags))
        self.assertFalse(any("src" in attrs for _, attrs in self.markup.tags))
        self.assertIn('lang="zh-CN"', self.html)
        self.assertIn("并非原摘要全文译文", self.html)
        self.assertIn("未新增独立评审或事实认证", self.html)

    def test_paper_text_is_escaped_and_input_not_mutated(self):
        data = copy.deepcopy(self.data)
        data["papers"][0]["ours_zh"] = '<img src=x onerror="alert(1)"> & text'
        snapshot = copy.deepcopy(data)
        markup = renderer.render(data)
        self.assertIn("&lt;img src=x", markup)
        self.assertNotIn('<img src=x', markup)
        self.assertEqual(data, snapshot)


if __name__ == "__main__":
    unittest.main()
