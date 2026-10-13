# Writing Evaluation Evidence

These are local, curated model-judged experiments, not a stable leaderboard or
evidence of improved conference acceptance. Broad coverage and subsequent evaluator
calibration still do not establish human effectiveness. Software tests
do not measure prose quality. No model weights are trained by the skill.

- [Abstract-only transfer confirmation](docs/abstract-transfer-evaluation.md):
  six papers, two samples and twelve equal-pass pairs under the exact preceding
  candidate. Preferences are candidate 10 / baseline 6 / tie 8; two unanimous
  candidate pairs, one baseline, one tie and eight disagreements. Both sample
  strata and four papers net favor candidate, but the frozen continuation gate
  fails because A06_s2 unanimously favors baseline. All source fidelity,
  critical-support and reader-grounding labels pass equally, with no measured
  advantage in those channels. No runtime promotion or pooled cross-round vote.
  [All abstracts and raw judgments](evals/abstract-transfer/comparison.html).

- [Operative-relation follow-up](docs/operative-relation-evaluation.md): two real
  paper cases, two samples, three units and twelve equal-pass pairs. Votes are
  candidate 5 / baseline 5 / tie 14; pairs include one unanimous candidate,
  one unanimous baseline, four ties and six disagreements. Abstract votes are
  4 / 0 / 4, with unfavorable Methods/Results evidence. All 48 source audits
  support the bounded objective and mark fidelity pass in both conditions;
  this is no fidelity improvement. No overall gain or runtime promotion.
  [Complete comparison](evals/operative-relation/comparison.html).

- [Evaluator-control calibration](docs/evaluator-control-calibration.md): twelve
  original synthetic pairs, nine consequential defects and three valid neutral
  alternatives. All 18 defective-pair preferences favor faithful prose; fine
  auditors detect all 18 defective-text judgments and flag none of 30 faithful
  or neutral judgments. Prespecified admission gate passes, not a writing-gain
  claim. Coarse fidelity also detects false metric claims despite successful
  reader recovery; do not confuse those two channels.
  [All controls and raw judgments](evals/evaluator-controls/comparison.html).

- [Broad equal-pass revision evaluation](docs/broad-writing-evaluation.md):
  twelve papers, six domains, three samples and three writing units; 108 pairs,
  216 final passages. Anonymous votes are candidate 12, baseline 20, tie 184;
  one pair unanimously favors candidate, four baseline, 81 tie and 22 disagree.
  No overall gain. All 216 primary and 216 supplementary source/reader audits
  are preserved separately; coarse understanding scores are near ceiling.
  [Complete side-by-side view](evals/broad-writing/comparison-complete.html).

- [Equal-pass read-back revision pilot](docs/readback-revision-evaluation.md):
  two papers, two shared initial drafts each, one revision per condition and
  eight pairs; two unanimously favor the candidate, one the baseline, two tie
  and three disagree. Separate source auditing flags one passage per condition,
  including a preferred candidate. No stable abstract or general gain claim.

- [Real-body argument-transfer pilot](docs/body-argument-transfer-evaluation.md):
  two CoRL papers, two fresh generations per condition, eight paired units;
  three unanimously favor the candidate, one favors the baseline, two tie and
  two disagree. Source auditing finds no explicit mismatch; no stable gain claim.
- [Argument-transfer pilot](docs/argument-transfer-evaluation.md): three original
  synthetic topics, abstracts and Results, separate writer/reviewer contexts;
  one candidate preference and eleven ties, without an overall gain claim.
- [Embodied comparison, round 2](docs/embodied-writing-evaluation.md): three papers,
  one generation per condition; no overall improvement demonstrated.
- [Embodied follow-up, round 3](docs/embodied-writing-round3.md): two different
  papers, two generations per condition; new Octo abstracts preferred, mixed
  FAST outcomes and an unresolved contribution omission.
- [Calibration cases](evals/abstract-quality/README.md): original public fixtures
  for distinguishing factual errors, evidence omissions and defensible ties.
- [Contribution-priority diagnostic](docs/contribution-priority-evaluation.md):
  three synthetic counterfactual cases; both versions follow explicit priorities,
  with an unresolved unsupported-objective allocation issue.
- [Real embodied abstract evaluation](docs/real-embodied-abstract-evaluation.md):
  three RSS papers with source-baseline comparison; mixed result.
- [Claim-scope diagnostic](docs/claim-scope-evaluation.md): three synthetic
  genre/evidence cases; directional signal only.
- [Verification scope](docs/validation.md): reproducible software checks and
  explicit boundaries on what they establish.

Conditions differ across rounds; do not pool their preference counts. Papers
used to revise a candidate become development data for subsequent rounds.
Human blind review, calibrated non-ceiling understanding measures and fresh-paper
tests of separately frozen changes remain necessary before a general
effectiveness claim. Broad coverage and repeated generation alone do not suffice.
