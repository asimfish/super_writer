import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).parent
specs = [
    {
        'id': 'P1',
        'file': 'wang25a',
        'title': 'Equivariant Diffusion Policy',
        'url': 'https://raw.githubusercontent.com/mlresearch/v270/main/assets/wang25a/wang25a.pdf',
        'start': '3   Background',
        'stop': '6    Conclusion',
        'limitation_start': 'One limitation of this work',
        'results_scope': 'Simulation and physical-robot findings in section 5; select an informative comparison rather than enumerate the tables.',
    },
    {
        'id': 'P2',
        'file': 'hejna25a',
        'title': 'ReMix: Optimizing Data Mixtures for Large Scale Imitation Learning',
        'url': 'https://raw.githubusercontent.com/mlresearch/v270/main/assets/hejna25a/hejna25a.pdf',
        'start': '3 Re-weighing Robotic Dataset Mixtures with Minimax Optimization',
        'stop': '\fAcknowledgments',
        'results_scope': 'Experimental findings in section 4; select an informative comparison rather than enumerate the tables.',
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
        limit_end = text.index('\fAcknowledgments', limit_begin)
        body += '\n[Source limitations, excluding conclusion summary]\n' + text[limit_begin:limit_end]
    assert not any(line.strip() == 'Abstract' for line in body.splitlines())
    dest = ROOT / 'inputs' / (spec['id'] + '.txt')
    dest.write_text(body)
    cases.append({'id': spec['id'], 'body_file': 'inputs/' + dest.name,
                  'results_scope': spec['results_scope']})
    pdf = ROOT / 'sources' / (spec['file'] + '.pdf')
    receipts[spec['id']] = {
        'title': spec['title'], 'official_pdf_url': spec['url'],
        'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
        'body_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
        'extraction': 'pdftotext -layout -f 2 -l 9; select declared section boundaries without repairing text',
        'body_words_approx': len(body.split()),
    }
request = {
    'task': 'Write a conference-style English abstract communicating the distinctive contribution for robot-learning readers, and one Results paragraph. Explain the design and what an informative comparison establishes using only the supplied body material. Choose evidence by function, not a summary of every component or table. Do not invent missing facts, gaps, significance or guarantees. Put unresolved reporting questions in working notes, not generic abstract disclaimers.',
    'abstract_words': [150, 200], 'results_words': [120, 180],
    'cases': cases,
    'output_schema': {'cases': [{'id': 'P1', 'working_notes': 'brief planning or author notes, at most 120 words', 'abstract': 'text', 'results': 'text'}]},
}
(ROOT / 'request.json').write_text(json.dumps(request, indent=2) + '\n')
(ROOT / 'source_receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
print(json.dumps(receipts, indent=2))
