# Writing Role Handoffs: Authored Development Example

All facts, the teaching exemplar, role responses and review judgments here are
original synthetic material written together. This is **not** output from four
independent agents, a blind preference result, a real experiment or proof of gain.
[Input](input.json) and [response bodies](responses.json) exercise the contract.

This is the original v1 handoff example. For the current excellent-paper and
standards comparison, see [the v2 section benchmark](benchmark.md): it includes
a compression-first abstract and related-work/experiment contrasts, with actual
selected local resources and criterion-to-prose handoffs.

## Editorial Choice

The example teaches a conditional operation: put the matched control where it
lets the reader interpret the difference. It is applicable only if author evidence
really fixes the relevant conditions. Its opposite is a list of scores with no
way to tell what differed. Another valid structure could state the result first
and immediately explain the control; matching one sentence order is not the goal.

| Stage | Inspectable output |
|---|---|
| Diagnosis | The original does not connect the scores to fixed data volume and overclaims broad generalization |
| Proposal | Explain the controlled contrast, bind score referents, narrow the implication |
| Writing | Realize those relations in the passage rather than explain them only in a plan |
| Review | Read the passage back; separately inspect coherence, the teaching choice and factual scope |

**Before**

> We collect 600 demonstrations across 12 layouts. Our policy reaches 68% success.
> The baseline achieves 51%. These findings establish broad generalization.

**Authored revision**

> To test layout coverage at fixed data volume, we train both policies on 600
> demonstrations with the same architecture, task mix and optimization budget.
> Training across 12 layouts yields 68% mean success on six held-out layouts,
> compared with 51% for training on two layouts. This comparison supports broader
> training-layout coverage for the evaluated layout shift; it does not establish
> robustness to other tasks or shifts.

This is a worked explanation of the mechanism, not a claim that this is the best
possible paragraph. In a full manuscript, conditions already established nearby
need not be repeated. Evaluation trial counts can remain in the experimental setup.

## Related-Work Transfer

The same diagnosis can apply to a paragraph that merely lists Paper A's model,
Paper B's dataset and our score. Before rewriting, the gap finder must establish
whether the sources share a task, assumption or evaluation axis. The proposer
can then organize the paragraph by that supported distinction. If tasks or data
budgets differ, the writer must not turn their scores into a head-to-head ranking.
If the source was not read, the next action is reading, not a stronger novelty claim.

## Reproduce the Handoffs

Run `python scripts/writing_loop.py examples/writing-team/input.json` from the
repository root. The next role is `gap_finder`. Use the matching body from
`responses.json` as `output`, preserving the packet's role and `input_sha256`,
and call `--response RESPONSE.json` to validate and emit the updated run.
Repeat for proposer, writer and reviewer. These are supplied responses, not model
calls; the tests replay exactly this sequence and exercise rejection paths.

An edit to evidence or a previous response invalidates downstream receipts.
In a real task, preserve raw agent responses separately; never substitute these
teaching responses or regenerate hashes to disguise stale work.

Acceptance merely records the supplied judgment. New quality evidence requires
the [separate evaluation design](../../references/writing-team.md#development-and-evaluation).
