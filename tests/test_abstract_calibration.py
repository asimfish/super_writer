"""Fixture integrity only: these tests do not judge abstract quality."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AbstractCalibrationTests(unittest.TestCase):
    def test_priority_probe_preserves_counterfactual_inputs(self):
        data = json.loads((ROOT / 'evals/abstract-quality/priority-probes.json').read_text())
        facts = {f['id']: f['text'] for f in data['facts']}
        self.assertEqual(len(facts), len(data['facts']))
        cases = {c['id']: c for c in data['cases']}
        self.assertEqual(set(cases), {'paired-contributions', 'method-priority',
                                     'priority-without-evidence'})
        selected = {}
        for name, case in cases.items():
            with self.subTest(case=name):
                self.assertTrue(set(case['omit_fact_ids']) <= set(facts))
                self.assertTrue(case['author_decision'])
                self.assertTrue(case['oracle']['required_meanings'])
                self.assertTrue(case['oracle']['forbidden'])
                selected[name] = {key: value for key, value in facts.items()
                                  if key not in case['omit_fact_ids']}
        self.assertEqual(selected['paired-contributions'], selected['method-priority'])
        self.assertNotEqual(cases['paired-contributions']['author_decision'],
                            cases['method-priority']['author_decision'])
        self.assertEqual(set(selected['paired-contributions']) -
                         set(selected['priority-without-evidence']), {'F3'})

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

    def test_follow_up_cases_cover_the_observed_embodied_failure_modes(self):
        data = json.loads((ROOT / 'evals/abstract-quality/cases.json').read_text())
        cases = {case['id']: case for case in data['cases']}
        expected = {
            'baseline-training-regimes',
            'design-rationale-under-compression',
            'method-first-or-gap-first',
        }
        self.assertTrue(expected <= set(cases))
        self.assertEqual(cases['baseline-training-regimes']['oracle']['fidelity']['B'], 'fail')
        self.assertEqual(cases['design-rationale-under-compression']['oracle']['preferred'], ['B'])
        self.assertEqual(cases['method-first-or-gap-first']['oracle']['preferred'], ['A', 'B'])

    def test_oracles_distinguish_omission_from_falsehood(self):
        cases = json.loads((ROOT / 'evals/abstract-quality/cases.json').read_text())['cases']
        for case in cases:
            oracle = case['oracle']
            with self.subTest(case=case['id']):
                if oracle['kind'] == 'valid_but_weaker':
                    self.assertEqual(set(oracle['fidelity'].values()), {'pass'})
                elif oracle['kind'] == 'factual_failure':
                    self.assertIn('fail', oracle['fidelity'].values())
                elif oracle['kind'] == 'defensible_tie':
                    self.assertEqual(set(oracle['preferred']), {'A', 'B'})


if __name__ == '__main__':
    unittest.main()
