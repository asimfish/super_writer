# Academic Style, With Evidence Boundaries

These ten original English/Chinese cases illustrate the integrated expression
contract. Inputs and outputs are authored demonstrations, not accepted-paper
excerpts, a detector benchmark or an independent agent test. Numbers in the
significance and model-comparison cases are constructed inputs; only the kNN
example's separately linked measurements are actual computations.

| Input | Recommended output | What must survive |
|---|---|---|
| It is worth noting that the model reduces mean MSE from 0.1083 to 0.0851 on the in-domain grid across five fixed seeds. | The model reduces mean MSE from 0.1083 to 0.0851 on the in-domain grid across five fixed seeds. | Metric, direction, scope and seeds |
| The observations are consistent with the proposed mechanism, although the design does not identify a causal effect. | Keep unchanged. | Necessary causal uncertainty |
| The bound controls prediction range, not prediction error. | Keep unchanged. | A useful mathematical distinction |
| 值得注意的是，离线强化学习中的分布偏移仍未解决；当前实验只覆盖两个固定数据集。 | 离线强化学习中的分布偏移仍未解决；当前实验只覆盖两个固定数据集。 | 专业术语、否定和实验范围 |

[All ten inputs, outputs and notes](cases.json) ·
[Computed kNN study](../knn-regression/) ·
[Editing contract](../../references/academic-expression.md)

Tests check that these outputs retain their declared protected spans, including
number-entity bindings. This validates the examples, not a general semantic
preservation algorithm. Diagnosis-only, unknown-year and prompt-injection
scenarios are separate [behavior cases](../../evals/activation.json).
