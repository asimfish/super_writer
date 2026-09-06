# Worked Protocol Application / 协议应用样例

This authored example applies `experiments.analysis / result-paragraph` to the
existing [synthetic regression materials](../knn-regression/materials/protocol.md).
It is not a blind agent evaluation, a new experiment or an accepted-paper excerpt.
Unlike the arbitrary numbers in table-render fixtures, these MSE values were
computed by the public [experiment script](../knn-regression/experiment.py).

## Select the Unit

```bash
python3 scripts/writing_guide.py experiments.analysis --variant result-paragraph
python3 scripts/writing_lookup.py "result boundary" --section experiments --limit 2
```

Run from the repository root; for an installed skill, resolve scripts under
its directory. The protocol supplies a structure, not the results below.

## Evidence Before Prose

| Check | Status | Author material or boundary |
|---|---|---|
| Question and comparator | Present | k=1 versus k=5, same 40 training observations within each seed |
| Main observation | Present | In-domain mean MSE: 0.1083 versus 0.0851 |
| Adverse observation | Present | Extrapolation mean MSE: 2.6891 versus 3.7012 |
| Aggregation | Present | Five fixed training seeds; mean and sample SD across fits |
| Significance | Missing / not performed | No inferential test; omit "statistically significant" |
| External validity | Missing / not tested | No real-world benchmark or claim of general robustness |
| Component ablation | Not applicable | Two neighborhood sizes, not a factorial component experiment |

Read the [per-seed results](../knn-regression/materials/results.csv) and
[aggregation](../knn-regression/materials/summary.json), not a sentence card, to
establish the numbers. Missing evidence narrows the text; it does not need to be
replaced by an invented experiment or a paragraph of excuses.

## Bounded Result Paragraph

> Across five fixed training seeds, five-neighbor regression has lower mean MSE
> than one-neighbor regression on the in-domain grid (0.0851 versus 0.1083).
> The ordering reverses on the extrapolation grid (3.7012 versus 2.6891).
> These measurements support an in-domain advantage under the stated synthetic
> protocol, not robustness beyond the training range; no significance test was
> performed.

中文核对：比较对象、两个测试域、五个训练种子、MSE 方向和未做显著性检验均保留。
这是一个局部结果段，不替代正文的实验设置、完整结果表或样本标准差说明。
完整上下文见 [worked manuscript](../knn-regression/manuscript.md)。

## When the Requested Table Has Missing Data

The [efficiency protocol](../../references/writing-protocols.md) additionally
requires hardware, precision, batch and measurement conditions. None of the
above MSE results supplies latency, throughput, memory or training cost. Keep
those `SL_*` cells unresolved or omit the unsupported table; do not reuse the
source-only compiler's synthetic `0.50` fixture values. A successful PDF build
cannot turn a placeholder into a measurement.
