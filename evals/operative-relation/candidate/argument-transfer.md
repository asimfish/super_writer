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

## Expand the Choice into an Explanation, Then Compress

If a plan still reads as a component or measurement list, sketch the scientific
relationship before drafting polished prose. Keep this in the existing rationale
row or brief working notes, not a new mandatory artifact. State the object or
decision, the obstacle, and the operation that changes it. The reader should
understand what the design does even without knowing its name. Then compress
that explanation to fit the requested unit; do not compress away the relationship
while retaining all component names.

Two Methods passages make this more concrete. These are independent editorial
observations of the cited sections, read on 2026-10-10, not copied wording:

- [DPO, section 4, equations 4-7](https://arxiv.org/pdf/2305.18290): the policy
  relation is substituted into pairwise preference probabilities; the common
  normalization term cancels. The exposition explains what makes direct policy
  fitting possible before presenting the objective. Transfer the permitted
  operation and its consequence, not an unsupported claim of equivalent optima.
- [PagedAttention, sections 4.1-4.3](https://arxiv.org/pdf/2309.06180): block-wise
  attention and a logical-to-physical map permit non-contiguous cache storage
  and incremental allocation. A decoding walk-through makes the interaction
  visible. Transfer an operational explanation connecting components, not merely
  the analogy to virtual memory or a claim that each component is faster.

For a Results unit, identify which plausible reading the comparator distinguishes
and which condition can change the finding. Put that relation beside the finding,
rather than appending "these results demonstrate effectiveness" to a table
inventory. A budget-matched comparator and a stronger differently trained model
answer different questions; neither can silently stand in for the other.

For example, the same project's observation scheduler and faster decoder are
not just two implementation names: their different timing and task outcomes
allow a comparison of decoder acceleration with the scheduling change as
evaluated. They do not isolate observation freshness as the cause. A prose action
should convey that distinction rather than simply reproduce three timings.

Qualify the claim where its interpretation depends on the condition. Do not
automatically end every paragraph with exclusions unrelated to its main claim,
or suppress a limitation that changes that claim. In a short abstract, one
well-chosen operational relation may be sufficient; no quota of "because"
sentences, mechanisms, numbers or disclaimers establishes an argument.

## Verify the Transfer in Final Prose

Use the existing Final Text Check and logic audit to locate the implemented
choice and its evidence. Read the paragraph's topic sentence and conclusion:
can they tell the reader what was learned and why it matters to this paper?
Then restore the intervening comparisons: do they actually support that answer?

### Read Back the Claim Before Checking the Plan

A correct plan can hide a loss in the draft: the writer supplies a missing
relationship from memory and marks a sentence complete because its terms remain.
For a claim-bearing unit, briefly put the plan aside and reconstruct the answer
from the prose alone. What changes, through what operation, with what consequence?
For a finding, what is compared, on which population or budget, and what follows?
Do not fill gaps using working notes or outside knowledge. An informative
definition, negative result or scoped comparison can be the answer; a mechanistic
explanation is not required when the evidence does not provide one.

Now compare that read-back with the evidence and the intended reader question.
Check the strongest reasonable interpretation, not only a charitable reading:
could the claim imply an isolated cause, paired population or general guarantee
that the comparison does not establish? Conversely, can the reader recover the
specific insight rather than a label such as "structure-aware"? Distinguish an
intentional omission from an essential relation lost during compression. An
abstract need not explain every component; preserve the relation that makes its
central contribution intelligible, or narrow the promise.

Repair the smallest affected passage: replace a component inventory with the
operative relationship, or replace an ambiguous outcome with the actual scoped
comparison. Re-read the repaired sentence in its paragraph; an appended caveat
cannot repair a stronger contradictory claim earlier in the text. Preserve
supported co-contributions and adverse findings. Do not add unsupported reasons,
extra numbers or a fixed explanatory sentence to every unit.

In the existing `Final Text Check`, record the final location, the relationship
recoverable there, and its evidence anchor. A location or repeated method name
alone is insufficient. For a bounded editing request, brief internal notes are
enough; this check does not require a new table or artifact. It is a semantic
self-review, not proof of reader comprehension or independent verification.

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

## Protect the Operative Relation During Compression

When shortening a claim-bearing passage, identify the operation or contrast
that lets its conclusion follow and any condition without which that conclusion
changes. Keep those in the claim's clause or adjacent explanation before
retaining a method label, extra measurement or assumption inventory. A component
name does not state its order of execution, object of transformation or reason
for the outcome. An accurate assumption list does not explain what the method
does under those assumptions.

If the edit removes a verb, dependency or comparison condition, read what remains
as an executable or inferential statement: can a reader tell what happens and
why this consequence is licensed, rather than supplying the step from expertise?
Restore the smallest missing operation/condition or narrow the claim. Rebalance
the existing word budget; do not append a generic caveat while leaving an
unscoped guarantee earlier. Preserve mixed evidence and co-contributions, and
do not invent a mechanism or force one into a purely descriptive finding.
