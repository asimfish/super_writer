import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).parent
specs = [
    {
        'id': 'P1',
        'file': 'lee24y',
        'title': 'Behavior Generation with Latent Actions (VQ-BeT)',
        'venue': 'ICML 2024',
        'url': 'https://raw.githubusercontent.com/mlresearch/v235/main/assets/lee24y/lee24y.pdf',
        'start': '3. Vector-Quantized Behavior Transformers',
        'stop': '5. Related Works',
        'extraction': 'pdftotext -raw -f 3 -l 9',
        'results_scope': 'Section 4 findings: choose an informative comparison rather than enumerate tables.',
    },
    {
        'id': 'P2',
        'file': 'p056',
        'title': 'Imitation Bootstrapped Reinforcement Learning (IBRL)',
        'venue': 'RSS 2024',
        'url': 'https://roboticsproceedings.org/rss20/p056.pdf',
        'start': 'IV. IMITATION BOOTSTRAPPED RL',
        'stop': 'VII. DISCUSSION',
        'limitation_start': 'Limitations and Future Work.',
        'limitation_stop': 'VIII. ACKNOWLEDGMENTS',
        'extraction': 'pdftotext -raw -f 2 -l 10',
        'results_scope': 'Sections V-VI findings: choose an informative comparison rather than enumerate tables.',
    },
]
receipts = {}
cases = []
for spec in specs:
    source = ROOT / 'sources' / (spec['file'] + '.body-candidate.txt')
    text = source.read_text()
    begin = text.index(spec['start'])
    end = text.index(spec['stop'], begin)
    body = text[begin:end]
    if 'limitation_start' in spec:
        limit_begin = text.index(spec['limitation_start'], end)
        limit_end = text.index(spec['limitation_stop'], limit_begin)
        body += '\n[Source limitations, excluding discussion summary]\n' + text[limit_begin:limit_end]
    assert not any(line.strip() == 'Abstract' for line in body.splitlines())
    dest = ROOT / 'inputs' / (spec['id'] + '.txt')
    dest.write_text(body)
    cases.append({'id': spec['id'], 'body_file': 'inputs/' + dest.name,
                  'results_scope': spec['results_scope']})
    pdf = ROOT / 'sources' / (spec['file'] + '.pdf')
    receipts[spec['id']] = {
        'title': spec['title'], 'venue': spec['venue'],
        'official_pdf_url': spec['url'],
        'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
        'body_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
        'extraction': spec['extraction'] + '; select declared boundaries without repairing text',
        'start': spec['start'], 'stop': spec['stop'],
        'limitation_start': spec.get('limitation_start'),
        'limitation_stop': spec.get('limitation_stop'),
        'body_words_approx': len(body.split()),
    }
request = {
    'task': 'Produce a conference-style English abstract and one Results paragraph for robot-learning readers using only the supplied body material. Communicate the distinctive contribution and what an informative comparison establishes, rather than inventory every component or table. Do not invent missing motivation, facts, significance or guarantees. Use the supplied scope for Results. Put unresolved source/reporting questions in working notes rather than generic disclaimers.',
    'revision_task': 'Revise the supplied initial abstract and Results paragraph into publication-quality prose using only the same body evidence and the designated guides. Preserve supported contributions and findings; do not assume an initial claim is correct. Use one revision response. Both conditions receive identical initial drafts and evidence.',
    'abstract_words': [150, 200], 'results_words': [120, 180],
    'cases': cases,
    'output_schema': {'cases': [{'id': 'P1', 'working_notes': 'brief internal planning/revision notes, at most 120 words', 'abstract': 'text', 'results': 'text'}]},
}
(ROOT / 'request.json').write_text(json.dumps(request, indent=2) + '\n')
(ROOT / 'source_receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
print(json.dumps(receipts, indent=2))
