# Contribution-Priority Alignment

Date: 2026-09-13. This is a bounded synthetic diagnostic, not another real-paper
holdout or evidence of conference acceptance gains.

## Design Finding and Change

The inherited contribution guide demanded a single Core contribution and an
abstract of five sentences in fixed order, conflicting with the flexible
abstract-decision guide. Its full-paper framing could also demote an independent
co-contribution to implementation detail. These are observed instruction
conflicts, not a proven cause of the preceding FAST omission.

The update removes the fixed sentence requirement, permits a central argument
with independently valuable co-contributions, and connects author priorities to
the existing rationale row and final-text check. Retention means a reader can
recover the contribution and its supporting scope, not merely find a tool name.
No new artifact, required column, guard schema or approval gate is introduced;
bounded abstract work can reuse supplied author decisions and brief working notes.

## Diagnostic Setup

Three original synthetic probes test equal contribution priorities, a method-only
priority, and a desired reuse claim with its evidence removed. The first two
use identical facts; only author priorities change. Each uses one fresh-context
old and new writer, yielding six abstracts of 120-160 words with separate notes.
Writers receive no oracle. Baseline is the preceding uncommitted candidate,
not HEAD; both load SKILL.md, contribution.md, abstract-decisions.md and
writing-rationale-matrix.md. Nine hashes freeze the eight resource snapshots and
probe data before generation. No model weights are trained, no tools are allowed
to writers, and no output is revised or resampled. Model and reasoning settings
are inherited without overrides or fixed seeds; exact backend revision is not
recorded. Two fresh-context judges compare anonymous pairs in reversed order.

These probes are deliberately constructed around the known failure and become
public development fixtures. They are not unfamiliar scientific papers or a
causal ablation of author clarification versus skill instructions. Author input
is explicit in both conditions, so success cannot be attributed to the new guide.

## Observed Behavior

All six raw responses parse as the requested JSON and meet their word budgets.
Both versions retain the two prioritized contributions with separate simulation
policy and excluded-simulator compression scopes. Both omit the reusable
checkpoint from the method-priority abstract while preserving its notes.
Neither fabricates a release or transfer result in the missing-evidence case.
However, both include the desired future contribution in that abstract as an
explicitly unestablished objective, despite the request to draft only supported
content. The coordinator treats this as a scope/allocation defect, not an invented
experimental result; one judge accepts a brief objective here while the other
would move it to notes. Preserve that disagreement rather than labeling unanimous
failure. The negative case also leaves the intended transfer capability ambiguous:
encoder reuse and policy-success transfer require different evaluation evidence.

Both judges tie the versions on the two supported-priority cases and prefer the
new version on the missing-evidence case. Its advantage is explicit confirmation
that neither release nor transfer is established; the old version's reference to
a released checkpoint can presuppose release even though transfer is called an
objective. This is a modest clarity result on one synthetic example, not evidence
of a general writing-quality advantage or a proven fix for real-paper omissions.

## Verification and Boundaries

Python3.14:164 unittest cases,163 passed and one PowerShell-unavailable skip;
11 smoke cases passed, as did compilation, frontmatter validation and diff checks.
The new integrity test verifies identical facts across the priority counterfactual
and removal of only the designated reuse evidence in the negative case. It does
not grade generated text. Runtime scripts, schema, activation description,
dependencies, imported pins and licenses are unchanged. Entrypoint routing now
links the priority guidance. No private papers or third-party prose were imported.

Release assessment: CONDITIONAL. Instructions are aligned and local compatibility
checks pass, but general effectiveness and human review remain unverified. No
global installation, version bump, commit, push or remote CI was performed.
Next evaluation should compare under-specified versus explicit author decisions
on new materials and check evidence-only drafts without changing frozen outputs.
