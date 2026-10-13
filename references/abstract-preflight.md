# Abstract Preflight: Evidence Lock Before Prose

Use this short pass before drafting or blind-comparing an empirical abstract.
It is a writing contract, not a substitute for checking the paper's tables.

## Freeze the Fact Rows

For every result that may appear in the abstract, record one row:

| Claim | Metric/unit | Evaluation setting | Baseline/protocol | Evidence verb | Allowed strength |
| --- | --- | --- | --- | --- | --- |
| result | success, throughput, memory, etc. | task, benchmark, hardware | training regime and comparison recipe | evaluate/find/observe | bounded conclusion |

Do not merge rows merely because they share a task. In particular, distinguish
pretrained models fine-tuned with default recipes from policies trained from
scratch, and distinguish action-generation throughput from end-to-end latency.
Keep `absolute` and `relative` gains explicit. If a paper reports a mixed group
of baselines, attach the comparison to each group rather than inventing a shared
protocol.

The metric row must identify the measured event, not just a unit such as
"success %". Follow the
[outcome-definition check](results-validation.md#check-what-the-metric-counts)
before compressing a final-stage observation into a whole-trajectory claim.

## Freeze the Argument Rows

Write one short line for each item:

1. The concrete problem or unresolved choice, if the source supports one.
2. The design rationale: what obstacle the design is intended to address.
3. The contribution that is actually established.
4. The decisive evidence and its scope.

The rationale is not automatically a causal finding. Saying that a pretrained
encoder supplies semantic representations does not prove that pretraining caused
an observed gain unless the evidence isolates it. Conversely, do not delete a
supported rationale just to save words while retaining a list of components.

## Draft and Audit

The abstract may be method-first or gap-first. Choose the order that makes the
argument easiest to recover; do not manufacture a gap to satisfy a template.
Before accepting a draft, check:

- every number has its metric, unit, setting and comparison condition nearby;
- every baseline group retains its actual training protocol;
- `evaluate`, `study`, `observe`, and `find` are not upgraded without evidence;
- the conclusion states a supported implication rather than a new label such as
  `reliable`, `unified`, or `general-purpose`;
- the final text stays within the agreed word budget without padding;
- missing reporting information is an author query, not a guessed manuscript fact.

For blind evaluation, provide the writer only the frozen fact and argument rows.
Keep source links, original wording, candidate labels, and prior judge decisions
outside the writer packet. Store the untouched output before any repair.

For an evaluation with explicit lexical constraints, optionally encode them as
JSON and run
`tools/check_abstract_contract.py` before blind review. The checker is deliberately
small: it verifies the agreed word range, required fact anchors, and explicitly
flagged expressions. A phrase check cannot distinguish negation, a correct
paraphrase or a number assigned to the wrong entity; interpret its findings
against the evidence. Do not require every available number or penalize a valid
omission solely to pass it. Check retained meaning and argument using
[argument transfer](argument-transfer.md). A passing contract is not a semantic
fidelity verdict or a quality score.
