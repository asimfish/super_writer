# Real-body argument-transfer pilot (2026-10-10)

## Intervention and reading scope

The preceding synthetic pilot did not establish improvement. This follow-up
adds a concrete drafting operation: expand a scientific relationship into an
explanation, then compress it without losing what makes the design or comparison
meaningful. Selected Methods passages from DPO (section 4, equations 4-7) and
PagedAttention (sections 4.1-4.3) inform that guidance. These are original
editorial observations, not imported prose or model-weight training.

Test material comes from two CoRL 2024 papers, published in PMLR 270 in 2025:
[Equivariant Diffusion Policy](https://proceedings.mlr.press/v270/wang25a.html)
(P1) and [ReMix](https://proceedings.mlr.press/v270/hejna25a.html) (P2).
Neither appears in this repository's preceding exemplar notes or development
reports. This means unexposed to documented skill development, **not** guaranteed
unseen by the model. The new guide snapshot is frozen before the coordinator
reads their body material.

Both conditions receive mechanically extracted Background/Methods, Experiments
and limitations, approximately 4,000 words per paper. Author abstracts,
introductions and conclusion summaries are excluded. Extraction retains table
and mathematical-layout artifacts; it is not a curated contribution summary.
The coordinator defines section boundaries but does not generate, select or
revise responses. PDF and body hashes identify the exact inputs.

## Protocol

- Baseline: current abstract, section and argument-transfer guides, snapshotted
  before the new explanation section.
- Candidate: identical abstract and section guidance; only the argument-transfer
  guide is replaced. This tests the additional guide text, not a complete skill
  workflow or an isolated exemplar-learner-to-writer handoff.
- Two fresh, non-forked writer contexts per condition. Each writes one abstract
  and one Results paragraph per paper, plus unscored working notes: sixteen
  passages across four untouched responses. No retries, padding or revisions.
- Frozen budgets: abstracts 150-200 words; Results 120-180. The repository
  abstract checker's token rule is used for mechanical counting.
- Two fresh reviewers see the same body sources and eight anonymous pairs,
  with reversed A/B order. No guides, notes, conditions or expected preference.
- A separate fresh source auditor reads designated body pages and rendered
  tables/figures, then checks all sixteen anonymous drafts. It does not see
  quality judgments or the condition mapping.
- The mapping is read only after both quality judgments are saved. All agents
  inherit the parent model; separate contexts are not separate model families
  or human validation. Each writer covers both papers, so samples are clustered.

The [repository artifacts](../evals/body-argument-transfer/README.md) contain raw
outputs, guide snapshots, judgments, mappings and receipts. Third-party body
text, PDFs, rendered pages and full source-text packets remain local and are
not redistributed. Public anonymous-pair records explicitly exclude source text.

## Observed result

| Pair | Reviewer 1 | Reviewer 2 |
| --- | --- | --- |
| P1 sample 1 abstract | Candidate | Candidate |
| P1 sample 1 Results | Tie | Tie |
| P1 sample 2 abstract | Baseline | Baseline |
| P1 sample 2 Results | Tie | Tie |
| P2 sample 1 abstract | Candidate | Candidate |
| P2 sample 1 Results | Tie | Baseline |
| P2 sample 2 abstract | Tie | Candidate |
| P2 sample 2 Results | Candidate | Candidate |

Sixteen judgments yield seven candidate preferences, three baseline preferences
and six ties. At the pair level, three unanimously favor the candidate, one
unanimously favors the baseline, two unanimously tie and two disagree. These
are repeated judgments of eight pairs, not sixteen independent experiments.
Do not turn the count into a general win rate or pool it with the synthetic test.

Both prose reviewers and the separate source auditor mark all drafts as
fidelity-pass against the designated body material. That is observed model
agreement, not proof of semantic correctness or an external fact certification.
Some omissions still affect argument quality without producing a clear false
claim. All raw passages meet their budgets.

One residual ambiguity deserves attention despite those passes. For P2 sample 2
abstract, the source auditor accepts "retain reported performance" as a faithful
description of the authors' aggregates, but records six full-data RT-X tasks
versus four subset tasks. That is not identical-task performance preservation.
The word "reported" does not by itself prevent a reader from making that
stronger inference. The post-pilot comparison check addresses this risk; model
fidelity-pass labels must not be treated as clearing every semantic ambiguity.

Raw word counts:

| Paper / sample | Baseline abstract / Results | Candidate abstract / Results |
| --- | --- | --- |
| P1 / 1 | 177 / 155 | 179 / 141 |
| P1 / 2 | 188 / 166 | 176 / 161 |
| P2 / 1 | 179 / 154 | 183 / 146 |
| P2 / 2 | 185 / 153 | 174 / 153 |

## What improves and what still fails

Three local explanatory choices receive unanimous candidate preferences:

1. P1 sample 1 explains why relative updates require conjugation: the current
   pose rotates too. The matched-RGB simulation comparison complements the
   matched-voxel hardware comparison, instead of leaving the architectural
   benefit to a cross-representation number alone.
2. P2 sample 1 explains why reference overfitting matters to this objective:
   near-zero reference loss destroys the informative relative-loss comparison.
   Normalization, discretization and early stopping have explanatory roles
   rather than becoming a list of safeguards.
3. P2 sample 2 Results identifies the combined retention-and-sampling intervention
   and explains why full-data and subset averages over different task sets are
   not paired measurements of the same population.

The counterexample is important. P1 sample 2 unanimously favors the baseline:
it retains the specific control operations and labels the input difference in
the cross-budget comparison. The candidate abbreviates this to "different
transformation rules" and leaves the simulation comparator's modality implicit.
An explanation guide can still yield a less informative compression.

P2 sample 1 Results also draws a baseline preference from reviewer 2: its
continued training-time weighting and task-count distinction make the tested
intervention more recoverable. Reviewer 1 ties the pair. No response is repaired
to erase these failures or disagreements.

These observations motivate two narrow post-pilot additions to the existing
rationale matrix's final check: retain the actual operation, and inspect task
population plus jointly changed factors before interpreting a comparison.
Those matrix additions are **not** part of the tested guide-only intervention;
their behavioral effect remains untested. The candidate guide snapshot itself
is unchanged after generation.

## Published abstracts as editorial references

Only after both quality judgments are saved does the coordinator read the
published abstracts. They foreground the research problem and contribution
while selecting compact evidence. These are editorial references, not another
scored condition or a quality oracle. The authors had fuller source access,
including the excluded introduction, so missing motivation cannot be charged
to a generated draft without checking its available input. No author abstract
is inserted into a packet or reproduced in the artifact set.

## Conclusion and verification

This round gives inspectable local evidence that operational explanations can
improve some drafts. It does not demonstrate stable superiority: the same P1
abstract task changes direction across replicates, and Results outcomes are
mostly ties or mixed. Broader fresh-paper coverage, repeated generations and
human reading are still needed. These papers are now development data.

Python 3.14: 174 unittest cases, 173 passes and one unavailable-PowerShell skip;
11 CLI smoke cases pass. Frontmatter and whitespace checks pass. Frozen-input,
raw-copy and anonymous-packet consistency checks pass. Software validation is
not a writing-quality score. No model training, installation, version bump,
commit, remote push or new official-template compilation occurs in this round.

Release assessment: **CONDITIONAL**. The PowerShell check is unavailable; this
pilot does not forward-test the complete revised multi-stage workflow or the
post-pilot matrix additions.
