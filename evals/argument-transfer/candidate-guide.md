# Learn Writing Decisions and Transfer Their Function

Use when learning from exemplar papers, rebuilding a section, or fixing prose
that lists components or measurements without an argument. Apply within the
existing dossier, blueprint and rationale matrix; a bounded paragraph request
can keep the same decisions in brief notes. No additional approval or artifact
tree is required.

## From Observation to a Writing Decision

Match exemplars by the work the passage does: explains a mechanism, diagnoses
an assumption, defines a resource, or establishes a cost-quality tradeoff.
Task similarity and venue are useful, but neither determines the right argument.
Read the actual passage; abstract-only reading supports abstract observations,
not a claim about the paper's Methods or Results organization.

For a useful pattern, record this chain in the dossier or existing plan:

| Source location and observed choice | Reader question before/after | Why that choice works | Our evidence and applicability | Text action and final location |
| --- | --- | --- | --- | --- |
| Specific passage; paraphrase its information function | What uncertainty it resolves | Relationship it makes visible, rather than an adjective | Author evidence IDs; assumptions shared or missing | What to explain, contrast, move, omit or qualify; then locate it in prose |

A citation plus "use a clear motivation" is not a transfer decision. Neither is
a matching sentence length. A single well-matched choice can be useful; recurring
choices are observations, not mandatory venue rules. Record a non-transfer when
our evidence cannot support the exemplar's claim or proof structure.

### Three Located Observations

These are independent editorial interpretations of author abstracts, checked
2026-10-10. Linked works retain their rights; no source sentences are reproduced.

| Exemplar and location | Observed writing choice | Conditional transfer |
| --- | --- | --- |
| [DPO](https://arxiv.org/abs/2305.18290), abstract: reward parameterization and policy extraction | The mathematical relationship explains why a complicated optimization pipeline can be simplified. The algorithm name follows that reason. | Explain the insight that permits our simplification before listing removed steps. Without a supported derivation, present design intent and measured behavior instead of implying equivalence. |
| [PagedAttention](https://arxiv.org/abs/2309.06180), abstract: dynamic cache waste through the throughput comparison | Memory allocation is connected to attainable batch size, making the chosen throughput comparison meaningful. Its latency condition stays attached to that comparison. | Explain the relevant bottleneck and how the proposed action addresses it. Use the actual timing boundary and quality tradeoff; a component's local speedup does not establish end-to-end benefit. |
| [Mirage](https://proceedings.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html), abstract: alternative metric explanation and complementary tests | Different analyses test the same explanation instead of becoming unrelated result summaries. The conclusion remains tied to the studied outputs and metric choices. | For a diagnosis, organize evidence around competing interpretations and what changes while other factors stay fixed. Do not turn a scoped alternative explanation into a universal refutation. |

Select a relevant choice, not all three. Do not transplant an exemplar's numbers,
novelty, causal claim, or unusually distinctive phrasing into our manuscript.

## Plan the Reader's Change in Understanding

Before drafting a unit, state in the existing rationale row:

- the question the reader should be able to answer after this unit;
- the answer licensed by our evidence, including any consequential exception;
- the comparison, derivation or observation that distinguishes that answer from
  a plausible alternative;
- why this unit belongs here and what question remains for the next unit.

Allocate text to those functions. Numerical density has no fixed target: multiple
numbers are appropriate when each supports a distinct promise or changes the
interpretation. Repeated table entries can remain in the table. Do not hide an
adverse result, uncertainty or co-contribution to make the narrative simpler.

For Methods, explain an operational obstacle and the role of a design choice;
keep intended function distinct from an experimentally isolated cause. For
Results, give a finding and the informative comparison, then the bounded reading
that follows. A negative or mixed finding can be the answer. For Discussion,
resolve the earlier question rather than repeat the results inventory.

Draft from these decisions and the author's facts, with source wording put aside.
Adapt order and paragraph boundaries to the argument. Do not force an explanatory
sentence into every paragraph when the surrounding text already supplies it.

## Verify the Transfer in Final Prose

Use the existing Final Text Check and logic audit to locate the implemented
choice and its evidence. Read the paragraph's topic sentence and conclusion:
can they tell the reader what was learned and why it matters to this paper?
Then restore the intervening comparisons: do they actually support that answer?

Three useful counterfactuals reveal weak prose:

1. If all method names and numbers were removed, is a paper-specific insight
   still recoverable, or could this paragraph describe almost any paper?
2. If the central comparison disappeared, would the conclusion still seem to
   follow? If so, the prose may be decorating a claim rather than justifying it.
3. If an unsupported mechanism explanation were removed, would the interpretation
   remain valid? If not, narrow it or request the missing evidence.

These are semantic reading tests, not automatic pass/fail heuristics. A precise
theorem or a data-defining number may itself be the insight. Keyword presence,
rewritten-word ratios and filled tables cannot establish successful learning.
Revise the failed relation in the plan and prose; do not repair it by adding
generic transitions, stronger adjectives or a blanket disclaimer.

See the [worked comparison](../examples/argument-transfer/README.md) for one
factually valid inventory and an argument built from the same evidence.
