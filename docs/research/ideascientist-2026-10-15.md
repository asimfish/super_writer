# IdeaScientist: Source Study and Writing Adaptation

Reviewed 2026-10-15. This is source analysis plus an original local design, not a
replication of the authors' results or an import of their implementation.

## Sources and Reading Scope

| Source | Pin / scope actually inspected |
|---|---|
| [Paper](https://arxiv.org/html/2610.04074v1) | v1, sections 3-4 and relevant harness, reward and evaluation appendices |
| [Code](https://github.com/jiarui-liu/IdeaScientist/tree/82a98a08772eab08d11fd097445afa4a8eaaa5b3) | `82a98a08772eab08d11fd097445afa4a8eaaa5b3`; README, LICENSE, orchestrator; targeted role/tool definitions, reward common/reference/report logic and vault field/corpus interfaces |
| [Public data card](https://huggingface.co/datasets/Jerry999/SvalbardIdeaVault/blob/64ab36be959afab06066f8c1e7ea292dba9362e5/README.md) | revision `64ab36be959afab06066f8c1e7ea292dba9362e5`; card and file metadata, not all corpus rows |

Source code was read in a temporary checkout, not installed or executed. No
trained model, corpus index, full data download or claimed experiment was run.

## What Transfers from the Harness

The [orchestrator](https://github.com/jiarui-liu/IdeaScientist/blob/82a98a08772eab08d11fd097445afa4a8eaaa5b3/ideascientist/harness/orchestrator.py)
coordinates separate intermediate artifacts and can revisit earlier stages.
Gap discovery, cross-setting mechanism adaptation and proposal writing are distinct
responsibilities. An adversarial reviewer and targeted paper reader support them.
The code restricts tool access by role; the orchestrator's role is narrower than
an unrestricted writer. This is stronger than merely naming several agents.

Our adaptation separates a *writing* diagnosis from an *editorial* proposal and
its prose realization. It does not turn an unsupported research idea into an
established contribution. The useful analogy is between reader problems: for
example, how to distinguish data diversity from volume, not how to borrow another
paper's scientific result. The local checker enforces artifact order and freshness,
not upstream-equivalent tool isolation.

## The Three Reward Components

The paper's training reward combines reference-free quality, reference-grounded
substantive alignment, and deterministic citation-ID F1. They are not three kinds
of reference matching. Its stated aggregation is
`0.85 * validity_gate * mean(free, reference, citation) + 0.15 * process`.
Role-specific rubrics and process checks matter; this is not a universal writing
score. The code's [reward primitives](https://github.com/jiarui-liu/IdeaScientist/blob/82a98a08772eab08d11fd097445afa4a8eaaa5b3/ideascientist/rewards/common.py)
expose component breakdowns and gating rather than only a final number.

We use three *separate editorial judgments*: intrinsic argument quality,
functional transfer from an applicable exemplar, and fidelity to author evidence.
We do not import the coefficients, citation overlap as prose quality, RL stack or
rubric text. A different valid writing solution must not be penalized for failing
to imitate a reference. An unresolved evidence error blocks acceptance regardless
of fluency. This is a design hypothesis requiring a new controlled writing trial.

## What the Large Corpus Is and Is Not

The paper reports 2.77M decomposed ideas and a 14,500/200/277 benchmark partition.
The pinned public card reports **2,669,631** records: 14,149 train, 195 validation,
272 test and 2,655,015 corpus. These are author-reported counts, not independently
recounted here; the differing snapshots are unresolved. Do not advertise that we
have installed 2.77M writing templates.

The card exposes bibliographic metadata plus generated `problem_definition`,
`intuition` and `proposal_masked`. It also exposes the original `abstract`.
Generated analyses may be wrong or incomplete. The public format is not identical
to the internal four retrieval views in [vault/fields.py](https://github.com/jiarui-liu/IdeaScientist/blob/82a98a08772eab08d11fd097445afa4a8eaaa5b3/ideascientist/vault/fields.py).
The corpus is broad across arXiv, not a curated collection of excellent AI writing.

Its appropriate place here is **paper discovery**. A future bounded index can
search same-problem records for comparison and analogous-challenge records for
editorial inspiration. Admission to our writing resources requires reading the
source passage, recording its function and conditions, checking author evidence,
constructing an original counterexample, and checking duplication. Keep source
metadata, generated idea records and verified writing observations distinct.

For a held-out study, reserve target IDs and all their versions before collection;
filter dates explicitly, do not assume `corpus` means pre-cutoff. Missing or
ambiguous dates must be excluded or manually resolved, not coerced into old dates.
The public viewer currently reports a timestamp parse failure for a year-only
value; no claim is made that every row satisfies the advertised date shape.
Do not expose held-out abstracts, masked proposals or target-derived annotations
to writers. A masked-results field is not a blanket leakage guarantee. A temporal
retrieval cutoff also does not establish absence from model pretraining.

## License and Capability Boundary

The code repository's [LICENSE](https://github.com/jiarui-liu/IdeaScientist/blob/82a98a08772eab08d11fd097445afa4a8eaaa5b3/LICENSE)
is CC BY-NC 4.0. The paper is CC BY 4.0. The data card distinguishes CC0 metadata
from CC BY 4.0 generated annotations; underlying papers retain their own rights.
These are different assets, not one repository-wide permission.

Our MIT repository receives only independently written conceptual adaptation,
source links, role instructions, original code and synthetic examples. No upstream
prompts/code, dataset rows, model weights or paper prose are vendored. Runtime
adds no network, credentials, crawler, automatic training or global installation.

Implementation: [ADR-003](../designs/adr-003-writing-role-handoffs.md),
[role workflow](../../references/writing-team.md), and
[authored development example](../../examples/writing-team/README.md).
