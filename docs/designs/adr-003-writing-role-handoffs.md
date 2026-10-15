# ADR-003: Bounded Writing Roles and Feedback

## Status

Accepted for opt-in development, 2026-10-15. No quality promotion or model training.
Extends existing exemplar learning and rationale rows, not their default rules.

## Problem and Alternatives

The latest writing pilot failed its promotion gate despite good factual fidelity.
Selecting relevant evidence, turning it into an operative relationship, and making
that relationship readable are different failure points. One undifferentiated
"improve the paragraph" prompt obscures the responsible stage.

| Option | Benefit | Cost / limitation |
|---|---|---|
| Add more prose instructions to the existing writer | Smallest change | Cannot inspect whether a diagnosis or edit plan reached the writer |
| Introduce a full autonomous retrieval/training service | Explicit roles, scalable corpus access | Provider, storage, permissions, licensing and evaluation scope exceed this skill |
| Reuse existing resources with scoped role packets and a replay checker | Inspectable handoffs and targeted returns; host/provider independent | Host still dispatches; schemas cannot establish semantic quality |

Choose the third. The IdeaScientist design is a conceptual reference; no code,
prompts, training rubrics, weights or dataset rows are incorporated. See the
[pinned source study](../research/ideascientist-2026-10-15.md).

## Interfaces and Ownership

`references/writing-team.md` owns the shared contract. Five role cards own the
orchestrator, diagnosis, editorial proposal, prose realization and read-back.
The existing exemplar learner supplies located choices. Existing dossier and
rationale matrix own the durable writing rationale; the optional JSON run owns
only actual handoff receipts and candidate states.

`scripts/writing_loop.py` replays events, validates exact ownership/input hashes,
projects next-stage context and returns a stop or next role. It cannot call an
agent, fetch a paper, write a manuscript, sandbox the host or certify entailment.
Non-acceptance retains the original. Any revised evidence/guidance starts a new
run so a previous review cannot be silently reused on different inputs.

Independent semantic review is an execution property, not a role name. Sequential
self-review must be labeled. A reference-free assessment remains possible;
reference-function transfer is then unassessed, not assigned a favorable score.

## Acceptance and Consequences

Tests must cover all return targets, no-change/missing-evidence stops, stale
upstream state, role order, false reference passes, non-located witnesses,
unresolved author queries, exhausted budgets, and relocated release execution.
An authored worked example explains the editorial choice without representing
a new blind trial. No default corpus, frozen guide or archived evaluation changes.

The corpus remains an external discovery source. A future bounded index requires
its own import/license/filtering decision; a full download or automated admission
is not a side effect of loading this workflow.

## Section Benchmark Extension

The author's clarification broadens diagnosis beyond comprehension failures.
A positive, section-specific benchmark now precedes diagnosis when excellent-paper
writing is requested. Reuse existing protocol, AI-spec and language-card APIs;
do not fork a new norms database or treat writing-resource counts as quality.
Schema v2 includes selected resources, a target reader answer, priority criteria
and a relative compression budget in every role's context, with fresh
criterion-level review and criterion-to-edit traceability.
Schema v1 remains readable for intrinsic diagnosis. Changed guidance invalidates
old receipts as designed; preserve old raw runs rather than rewriting hashes.

Compare content selection, argument organization, evidence presentation, expression,
clarity and applicable formatting. A clear passage can still have a meaningful
quality gap; a different effective structure can be a valid alternative. The
revision order is deletion, merge, reordering, then minimal addition: a longer,
checklist-complete rewrite is rejected when it exceeds the relative budget.
Norms without exemplars support standards-based review, not claims about learning
from excellent papers. Official formatting still needs the exact current authority.
The new helper loads only selected existing bundled records, not source URLs or
arbitrary local paths, and adds no network, model execution or manuscript writes.
