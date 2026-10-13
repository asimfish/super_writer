import unittest

from tools.check_abstract_contract import check


class AbstractContractTests(unittest.TestCase):
    def test_accepts_in_range_text_with_fact_anchors(self):
        text = " ".join(["12", "46.9%", "four robot-manipulation benchmarks", "planned"] + ["evidence"] * 146)
        result = check(text, {
            "min_words": 150,
            "max_words": 190,
            "required": ["12", "46.9%", "four robot-manipulation benchmarks", "planned"],
        })
        self.assertTrue(result["ok"])
        self.assertEqual(result["word_count"], 153)

    def test_rejects_length_and_unsupported_phrase(self):
        result = check("Reliable results.", {
            "min_words": 10,
            "max_words": 20,
            "forbidden": ["reliable"],
        })
        self.assertFalse(result["ok"])
        self.assertTrue(any("word_count" in error for error in result["errors"]))
        self.assertIn("forbidden phrase: reliable", result["errors"])


if __name__ == "__main__":
    unittest.main()
