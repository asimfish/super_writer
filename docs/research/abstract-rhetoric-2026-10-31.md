# Source-Calibrated Abstract Rhetoric

## Reason for the Pass

The previous evidence-selection pass reduced some result inventories but still
produced prose that read like compressed Methods and Results sections. The user
identified a separate failure: the writing was less natural than the paper
authors' abstracts. The issue was information level and sentence rhythm, not
only number selection.

## Sources and Scope

The following official PMLR abstract pages were read on 2026-10-31:

- [EquiBot](https://proceedings.mlr.press/v270/yang25a.html)
- [Sparsh](https://proceedings.mlr.press/v270/higuera25a.html)
- [ManiWAV](https://proceedings.mlr.press/v270/liu25c.html)
- [PoliFormer](https://proceedings.mlr.press/v270/zeng25a.html)
- [OKAMI](https://proceedings.mlr.press/v270/li25a.html)

Only abstract-level organization was used in this pass. The full papers and the
earlier body-derived evidence packets remain separate sources. No source abstract
is reproduced in the repository. Linked papers retain their rights.

## Reusable Observation

Across these examples, the abstract keeps a stable level of description: it makes
a problem, capability or resource salient; states the contribution; gives the
evidence at a matching level; and ends with transfer, a second contribution or a
practical implication. The sequence varies by paper. A resource paper can open
with the resource; a system paper can open with capability; neither requires a
fixed four-sentence template.

The previous candidates often descended into details that the source abstracts
did not need: normalization steps, sensor rates, per-task success values, rollout
counts and failure caveats. The correction is not to delete all mechanisms or
numbers. It is to keep one mechanism when it explains the contribution, use a
benchmark-level result when it answers the claim, and move implementation detail
back to the appropriate section.

Chinese translation needs a separate read. English modifier chains should be
reordered into Chinese clause structure, but words that strengthen scope or
causality must not be added for fluency. The naturalized examples keep technical
bindings and label source conflicts separately.

## Integration

`references/abstract-rhetoric.md` is included in the abstract writing packet after
the existing abstract decisions. It supplies a source-shaped profile and a
naturalness diagnostic; it does not add a mandatory artifact, sentence quota or
lexical imitation rule. The five-paper artifact in `evals/abstract-natural/`
preserves prior candidates and labels the new versions as known-case development.

This round is not a blind comparison and does not establish a writing-quality
gain. A future evaluation must freeze source access, budgets and profiles before
testing unseen papers with fresh readers.
