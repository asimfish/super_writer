import unittest

from tools.aggregate_blind_review import aggregate, preference_agreement, validate_review


DIMENSIONS = ("contribution", "rationale", "precision", "evidence", "language")


def review(preferred="A"):
    scores = {dimension: "4" for dimension in DIMENSIONS}
    return {
        "reviewer_id": "reviewer-fixture",
        "cases": {
            "paper": {
                "A": dict(scores),
                "B": {dimension: "2" for dimension in DIMENSIONS},
                "preferred": preferred,
                "reason": "The evidence-calibrated candidate is clearer.",
            }
        }
    }


class BlindReviewAggregationTests(unittest.TestCase):
    def test_unblinds_scores_using_mapping(self):
        mapping = {"paper": {"A": "old", "B": "new"}}
        result = aggregate([review()], mapping)
        self.assertEqual(result["scores"]["old"]["precision"], 4.0)
        self.assertEqual(result["scores"]["new"]["precision"], 2.0)
        self.assertEqual(result["preferences"], {"old": 1})
        self.assertEqual(result["per_case"]["paper"]["delta_new_minus_old"]["precision"], -2.0)

    def test_rejects_incomplete_review(self):
        mapping = {"paper": {"A": "old", "B": "new"}}
        broken = review()
        del broken["cases"]["paper"]["B"]["language"]
        broken["cases"]["paper"]["reason"] = ""
        errors = validate_review(broken, mapping)
        self.assertIn("invalid score: paper/B/language", errors)
        self.assertIn("missing reason: paper", errors)

    def test_missing_reviewer_id_is_rejected(self):
        mapping = {"paper": {"A": "old", "B": "new"}}
        broken = review()
        broken["reviewer_id"] = ""
        self.assertIn("missing reviewer_id", validate_review(broken, mapping))

    def test_rejects_extra_case_and_invalid_mapping(self):
        mapping = {"paper": {"A": "old", "B": "new"}}
        broken = review()
        broken["cases"]["extra"] = broken["cases"]["paper"]
        self.assertIn("unexpected case: extra", validate_review(broken, mapping))
        invalid = {"paper": {"A": "old", "B": "old"}}
        self.assertIn("invalid mapping: paper", validate_review(review(), invalid))

    def test_reports_pairwise_preference_agreement(self):
        mapping = {"paper": {"A": "old", "B": "new"}}
        second = review("B")
        second["reviewer_id"] = "reviewer-2"
        self.assertEqual(
            preference_agreement([review(), second], mapping),
            {"pairs": 1, "agreements": 0, "exact_agreement": 0.0},
        )


if __name__ == "__main__":
    unittest.main()
