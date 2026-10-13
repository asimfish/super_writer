import unittest

from tools.render_blind_summary import render, verdict


def summary(reviewers=1):
    scores = {d: 3.0 for d in ("contribution", "rationale", "precision", "evidence", "language")}
    return {
        "reviewers": reviewers,
        "scores": {"old": scores, "new": scores},
        "preferences": {"tie": 1},
        "per_case": {},
        "preference_agreement": None,
    }


class BlindSummaryTests(unittest.TestCase):
    def test_insufficient_reviewers_is_explicit(self):
        self.assertIn("INSUFFICIENT", verdict(summary()))

    def test_mixed_preferences_are_not_called_a_win(self):
        data = summary(2)
        data["preferences"] = {"old": 1, "new": 1}
        self.assertIn("MIXED", verdict(data))
        self.assertIn("MIXED EVIDENCE", render(data))


if __name__ == "__main__":
    unittest.main()
