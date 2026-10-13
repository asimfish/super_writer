import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
request = json.loads((ROOT / 'request.json').read_text())
responses = [json.loads((ROOT / 'raw' / f'writer_{i}.json').read_text()) for i in (1, 2)]
expected = {case['id'] for case in request['cases']}
for response in responses:
    assert len(response['cases']) == len(expected)
    assert {case['id'] for case in response['cases']} == expected
    assert all(isinstance(c[k], str) and c[k].strip() for c in response['cases'] for k in ('abstract', 'results'))
indexed = [{c['id']: c for c in response['cases']} for response in responses]
rng = random.Random(20261010)
permutation = {}
for case in request['cases']:
    for unit in ('abstract', 'results'):
        order = [0, 1]
        rng.shuffle(order)
        permutation[f"{case['id']}/{unit}"] = order

for judge in (1, 2):
    pairs = []
    for case in request['cases']:
        for unit in ('abstract', 'results'):
            order = permutation[f"{case['id']}/{unit}"]
            if judge == 2:
                order = list(reversed(order))
            pairs.append({'case': case['id'], 'unit': unit,
                          'drafts': {label: indexed[i][case['id']][unit]
                                     for label, i in zip(('A', 'B'), order)}})
    (ROOT / f'review_packet_{judge}.json').write_text(json.dumps({'request': request, 'pairs': pairs}, indent=2) + '\n')

(ROOT / 'private_mapping.json').write_text(json.dumps(permutation, indent=2) + '\n')
hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
          for path in [ROOT / 'request.json', ROOT / 'raw' / 'writer_1.json', ROOT / 'raw' / 'writer_2.json']}
(ROOT / 'generation_hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')
print('Two anonymous review packets prepared from untouched responses.')
