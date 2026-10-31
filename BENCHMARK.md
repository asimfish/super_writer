# Writing Evaluation Evidence

These are local, curated model-judged experiments, not a stable leaderboard or
evidence of improved conference acceptance. Broad coverage and subsequent evaluator
calibration still do not establish human effectiveness. Software tests
do not measure prose quality. No model weights are trained by the skill.

**Current status (2026-10-29): no stable writing-quality improvement is demonstrated.**
The latest explanation-preserving pilot improves model answer recovery, but
fails preference and fidelity gates. New contract checks are engineering changes,
not quality promotion. Conditions differ across rounds and are not pooled.

- [Evidence-selection developmental follow-up](evals/abstract-argument/README.md):
  five already-known embodied papers, new argument-driven candidates and Chinese
  author/prior/new views. This responds to user-observed metric inventories and
  flat progression, not a new blind trial. Source-derived pattern observations
  and changed length budgets are disclosed. The old five-paper self-assigned
  factual pass labels are not independent certification. No preference votes
  from this demonstration are added to the frozen pilots below.
  Independent source reading found one task-ranking conflict in the raw Sparsh
  draft; the displayed factual correction and original failure are both retained.

- [Source-calibrated naturalness follow-up](evals/abstract-natural/README.md):
  five known embodied papers rewritten after reading their official abstracts.
  The candidates transfer abstraction level, move sequence and ending function;
  they are not blind evidence or a preference result. This is a separate
  developmental pass from the evidence-selection follow-up above.

- [Explanation-preserving guide ablation](evals/explanation-pilot/README.md):
  four fresh-to-this-repository RSS 2025 papers and twelve generated abstracts.
  Against a 150-word-budget legacy control, the candidate is 3 / 2 / 3 overall;
  against hard no-growth compression it is 8 / 0 / 0. Audited model recovery is
  8/8 versus both controls' 6/8, but candidate and relaxed control each confuse
  whole-dataset with training-population counts in one passage. Preference and
  fidelity gates fail. This tests a guide, not the complete v3 role loop.
  [All four versions](evals/explanation-pilot/comparison.html).

- [Compression-first pilot](evals/compression-pilot/README.md): six RSS 2025
  papers, twelve Abstract/Results units, thirty-six revisions. Candidate versus
  previous guidance is 9 / 15 / 0 overall, Abstracts 2 / 10 / 0, Results 7 / 5 / 0.
  The author-original comparison is separately exploratory and length-confounded.
  The frozen gate fails; shorter abstracts lose important explanatory substance.

- [Current AI-spec pilot](docs/ai-spec-pilot-evaluation.md): DROID and SIMPLER,
  two replicates and three units, 12 pairs/24 final passages. Abstract votes
  are 0 / 5 / 3, Methods 1 / 1 / 6, Results 2 / 4 / 2. One unanimous candidate
  pair, four baseline, four ties, three disagreements. All 24 packet-fidelity
  checks pass; audited reader answers are candidate 42 recovered/6 partial,
  baseline 40/8, not an objective comprehension gain. Six reader cap deviations
  remain visible. No default-guide change or pooling with preceding rounds.
  [Complete horizontal comparison](evals/ai-spec-pilot/comparison.html).

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
