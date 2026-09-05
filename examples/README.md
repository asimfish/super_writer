# Public Examples / 公开样文

These are original educational artifacts, not accepted papers, private manuscripts,
or evidence of acceptance-rate gains. The three extended examples were authored
with AI assistance and checked against their materials. They are worked answers,
not independent blind evaluations.

| Example | What to inspect | Evidence | Documents |
|---|---|---|---|
| [Toy regression](knn-regression/) | Protocol, positive and adverse results, bounded interpretation | Executable experiment, 20 per-seed records, aggregation JSON | [Markdown](knn-regression/manuscript.md), [PDF](knn-regression/manuscript.pdf), [Word](knn-regression/manuscript.docx) |
| [Theory note](theory-note/) | Assumptions, proof, counterexample | Direct proof and exact-rational checks; no novelty claim | [Markdown](theory-note/manuscript.md), [PDF](theory-note/manuscript.pdf), [Word](theory-note/manuscript.docx) |
| [Reviewer response](review-response/) | Correct a claim, explain sample SD, acknowledge an unrun baseline | Constructed comments linked to the regression manuscript | [Markdown](review-response/response.md), [PDF](review-response/response.pdf), [Word](review-response/response.docx) |
| [Minimal claim revision](synthetic-study/) | Narrow an over-strong sentence | Hand-invented tutorial counts, explicitly labeled | [Evidence](synthetic-study/evidence-to-claim.md), [PDF](synthetic-study/manuscript.pdf), [Word](synthetic-study/manuscript.docx) |

## Reproduce

From the source repository root:

```bash
python3 examples/knn-regression/experiment.py
python3 -m unittest discover -s tests -p test_examples.py -v
```

The first command writes only to stdout. Floating-point results are checked
within `1e-12`; table entries use four decimal places. Sample SD is across five
training seeds, not across evaluation grid points.

With Pandoc, TeX and Poppler installed:

```bash
python3 tools/render_examples.py --output-dir build/rendered-examples
```

This recreates the extended examples as TeX, PDF, Word, extracted text and PNGs.
It checks compilation, unresolved references, overfull boxes and real document
guards, with TeX shell escape disabled. To explicitly refresh published artifacts,
use `--output-dir examples` and inspect every changed page before committing.

## Use as an Exercise

Supply the request and raw materials only. Withhold the finished manuscript,
writing decisions and response so the answer does not leak into evaluation.
Assess factual preservation, claim scope, omitted adverse results and invented
experiments. Record the host, model, prompt, input revision and actual output;
do not infer a behavioral pass from routing JSON or these worked examples.

样文使用通用可读版式，不是特定会议的正式投稿文件。真实投稿还需核对会议、年份、
赛道、页数、匿名、声明和补充材料要求。教材只提供书目信息，不分发原书内容。
