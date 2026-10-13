import hashlib
import json
import random
import re
from pathlib import Path


ROOT = Path(__file__).parent
request = json.loads((ROOT / 'request.json').read_text())
ids = {case['id'] for case in request['cases']}
responses = {}
counts = []
note_counts = []
hashes = {}
for condition in ('baseline', 'candidate'):
    for sample in (1, 2):
        source = ROOT / 'raw' / f'{condition}_{sample}.json'
        response = json.loads(source.read_text())
        assert len(response['cases']) == len(ids)
        assert {case['id'] for case in response['cases']} == ids
        indexed = {case['id']: case for case in response['cases']}
        responses[condition, sample] = indexed
        for case in response['cases']:
            notes = len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", case['working_notes']))
            note_counts.append({'condition': condition, 'sample': sample,
                                'case': case['id'], 'words': notes,
                                'budget_pass': notes <= 120})
            for unit in ('abstract', 'results'):
                assert isinstance(case[unit], str) and case[unit].strip()
                words = len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", case[unit]))
                budget = request[unit + '_words']
                counts.append({'condition': condition, 'sample': sample,
                               'case': case['id'], 'unit': unit, 'words': words,
                               'budget_pass': budget[0] <= words <= budget[1]})
        hashes[str(source.relative_to(ROOT))] = hashlib.sha256(source.read_bytes()).hexdigest()

initial_counts = []
for sample in (1, 2):
    source = ROOT / 'raw' / f'initial_{sample}.json'
    response = json.loads(source.read_text())
    assert len(response['cases']) == len(ids)
    assert {case['id'] for case in response['cases']} == ids
    for case in response['cases']:
        for unit in ('abstract', 'results', 'working_notes'):
            words = len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", case[unit]))
            budget = [0, 120] if unit == 'working_notes' else request[unit + '_words']
            initial_counts.append({'sample': sample, 'case': case['id'], 'unit': unit,
                                   'words': words, 'budget_pass': budget[0] <= words <= budget[1]})
    hashes[str(source.relative_to(ROOT))] = hashlib.sha256(source.read_bytes()).hexdigest()

rng = random.Random(20261012)
mapping = {}
for case in request['cases']:
    for sample in (1, 2):
        for unit in ('abstract', 'results'):
            order = ['baseline', 'candidate']
            rng.shuffle(order)
            mapping[f"{case['id']}/{sample}/{unit}"] = order

for judge in (1, 2):
    pairs = []
    for case in request['cases']:
        for sample in (1, 2):
            for unit in ('abstract', 'results'):
                key = f"{case['id']}/{sample}/{unit}"
                order = mapping[key] if judge == 1 else list(reversed(mapping[key]))
                pairs.append({'case': case['id'], 'sample': sample, 'unit': unit,
                              'drafts': {label: responses[condition, sample][case['id']][unit]
                                         for label, condition in zip(('A', 'B'), order)}})
    sources = {case['id']: (ROOT / case['body_file']).read_text() for case in request['cases']}
    packet = {'task': request['task'], 'abstract_words': request['abstract_words'],
              'results_words': request['results_words'], 'sources': sources, 'pairs': pairs}
    (ROOT / f'review_packet_{judge}.json').write_text(json.dumps(packet, indent=2) + '\n')

(ROOT / 'private_mapping.json').write_text(json.dumps(mapping, indent=2) + '\n')
(ROOT / 'word_counts.json').write_text(json.dumps(counts, indent=2) + '\n')
(ROOT / 'initial_word_counts.json').write_text(json.dumps(initial_counts, indent=2) + '\n')
(ROOT / 'note_word_counts.json').write_text(json.dumps(note_counts, indent=2) + '\n')
for name in ('PROTOCOL.md', 'request.json', 'source_receipts.json',
             'baseline/abstract-decisions.md', 'baseline/writing-protocols.md',
             'baseline/argument-transfer.md', 'candidate/argument-transfer.md', 'inputs/P1.txt', 'inputs/P2.txt'):
    hashes[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
(ROOT / 'generation_hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')
print('Eight anonymous pairs per reviewer; raw prose and working notes preserved, notes not exposed to judges.')
print(json.dumps(counts, indent=2))
