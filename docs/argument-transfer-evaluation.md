# Argument-transfer development pilot (2026-10-10)

## Question and intervention

Can learning an exemplar's writing decision make prose explain why evidence
answers a contribution, rather than merely list measurements? The new guide
maps a located choice to a reader question, applicable author evidence and an
action in the final text. It reuses the existing dossier and rationale matrix.

The baseline receives snapshots of the existing abstract-decision and
experimental-prose guides. The candidate receives those same snapshots plus
the new argument-transfer guide. Both receive identical facts and priorities.
This comparison tests that additional guidance, not the entire revised skill
workflow or a claim that more exemplar papers have been learned.

## Protocol and artifacts

- Three original synthetic development cases: visual-grasping scheduling,
  score-weighting diagnosis and a camera-mount benchmark.
- One fresh, non-forked writer context per condition; one generation containing
  three abstracts and three Results paragraphs. No retries or response edits.
- Abstract budget: 130-180 words. Results budget: 90-140 words.
- Two fresh, non-forked reviewer contexts see the facts and six anonymous pairs.
  Their A/B display order is reversed. Neither receives condition identities,
  writing guides, prior conclusions or an expected preference.
- The rubric reports fidelity, four ordinal writing dimensions and a preference
  or tie with a located reason. Fidelity takes precedence over fluent wording.
- The version mapping is read only after both judgments are saved. All four
  agents use the inherited parent model; separate contexts do not create
  independent model families or independent human review.

The [artifact directory](../evals/argument-transfer/README.md) contains the
requests, guide snapshots, untouched responses, anonymous packets, mapping and
generation hashes. All research results in these cases are synthetic; no private
author manuscript or third-party abstract is redistributed.

## Observed result

| Pair | Reviewer 1 | Reviewer 2 |
| --- | --- | --- |
| C1 scheduling abstract | Candidate | Tie |
| C1 scheduling Results | Tie | Tie |
| C2 weighting abstract | Tie | Tie |
| C2 weighting Results | Tie | Tie |
| C3 benchmark abstract | Tie | Tie |
| C3 benchmark Results | Tie | Tie |

Across twelve judgments there is one candidate preference and eleven ties;
no pair has a unanimous directional preference. These are repeated judgments of
six pairs, not twelve independent writing experiments. Both reviewers mark every
draft as fidelity-pass against the supplied packet. A coordinator reading found
no additional packet mismatch, but this is not external fact verification or a
validated semantic oracle. All twelve raw passages meet the frozen word budgets:

| Case | Baseline abstract / Results | Candidate abstract / Results |
| --- | --- | --- |
| C1 | 162 / 107 | 158 / 118 |
| C2 | 154 / 101 | 151 / 109 |
| C3 | 156 / 111 | 148 / 104 |

The particular improvement identified by reviewer 1 is inspectable. Both C1
abstracts preserve the timings, task outcomes and dropped-frame tradeoff. The
candidate adds:

> The contrast indicates that decoder acceleration alone does not reproduce
> the scheduler's observed task outcome.

That sentence explains the diagnostic function of the faster-decoder comparator
without attributing the gain to freshness alone. Reviewer 2 still ties the pair:
the baseline makes the retention-versus-timeliness tradeoff explicit, and both
are defensible explanations of the same evidence. Keep that disagreement.

Both conditions already explain C2's ranking reversal through unchanged outputs
and changed weights. Both explain C3's held-out-mount gap and data-dependent
adaptation. Merely changing order or adding another explanation does not
establish an advantage when the baseline already performs those functions.

## Interpretation and next test

This pilot does **not** demonstrate a stable writing-quality improvement. The
new guide provides an explicit planning and handoff mechanism, and one reviewer
identifies a local explanatory advantage. That is narrower than outperforming
the baseline. Near-ceiling ordinal ratings also limit this pilot's discrimination;
do not turn them into a headline average or a superiority percentage.

The clear author priorities and compact fact packets may have made both
conditions' planning easier; this is an inference, not a measured cause of ties.
The next behavioral test should use previously unexposed real-paper body material
without its abstract, less pre-organized author notes, repeated generations and
separate source auditing. It should inspect the actual comparisons and sentences,
not reward number removal, fixed move labels or generic caution. These three
cases are now development data, not a future unseen test set.

The [same-evidence worked example](../examples/argument-transfer/README.md) is a
separate, manually authored teaching comparison, not one of these blind outputs.
The preceding September 18 same-context writing/self-audit is corrected in
[its report](embodied-writing-round4.md); do not pool it with this pilot.

## Software verification

Python 3.14: 174 unittest cases, 173 passes and one unavailable-PowerShell skip;
11 CLI smoke cases pass. Skill frontmatter validation passes under system Python
with its existing PyYAML. Whitespace checks pass. These verify software behavior
and artifact integrity, not scholarly quality. No installation, version bump,
commit, remote push or new official-template compilation is part of this update.

Release assessment: **CONDITIONAL**. Portable checks and artifact consistency
pass; the PowerShell check is unavailable and a forward-test of the complete
revised multi-stage workflow is not performed here. The guide-only pilot above
must not be presented as that full-workflow evidence.
