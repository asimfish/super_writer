"""Fixture integrity only: these tests do not judge abstract quality."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AbstractCalibrationTests(unittest.TestCase):
    def test_cases_are_complete_and_cover_distinct_decisions(self):
        data = json.loads((ROOT / 'evals/abstract-quality/cases.json').read_text())
        cases = data['cases']
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        self.assertEqual({case['oracle']['kind'] for case in cases},
                         {'valid_but_weaker', 'factual_failure', 'defensible_tie'})
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertTrue(case['materials'])
                self.assertTrue(case['request'])
                self.assertEqual(set(case['drafts']), {'A', 'B'})
                self.assertEqual(set(case['oracle']['fidelity']), set(case['drafts']))
                self.assertTrue(set(case['oracle']['preferred']) <= set(case['drafts']))
                self.assertTrue(case['oracle']['reason'])
                self.assertNotEqual(case['drafts']['A'], case['drafts']['B'])

    def test_oracles_distinguish_omission_from_falsehood(self):
        cases = json.loads((ROOT / 'evals/abstract-quality/cases.json').read_text())['cases']
        by_kind = {case['oracle']['kind']: case['oracle'] for case in cases}
        self.assertEqual(set(by_kind['valid_but_weaker']['fidelity'].values()), {'pass'})
        self.assertIn('fail', by_kind['factual_failure']['fidelity'].values())
        self.assertEqual(set(by_kind['defensible_tie']['preferred']), {'A', 'B'})


if __name__ == '__main__':
    unittest.main()
