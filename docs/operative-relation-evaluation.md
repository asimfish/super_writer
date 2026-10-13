# Operative-relation revision follow-up (2026-10-11)

## Outcome

All planned assessments are saved and decoded. **No overall gain is demonstrated**:
candidate 5 preferences, baseline 5, tie 14. Twelve pairs comprise one unanimous
candidate preference, one unanimous baseline preference, four unanimous ties and
six disagreements. No candidate section is promoted to runtime guidance.

| Unit | Candidate | Baseline | Tie |
| --- | ---: | ---: | ---: |
| Abstract | 4 | 0 | 4 |
| Methods / Analysis | 1 | 2 | 5 |
| Results / example interpretation | 0 | 3 | 5 |

The abstract signal is encouraging but limited to four pairs from two papers:
one unanimous candidate preference, one unanimous tie and two candidate-versus-tie
disagreements. It is not four independent paper wins. Overall sample 1 gives
candidate 4 / baseline 1 / tie 7, whereas sample 2 gives candidate 1 / baseline 4 /
tie 7. Methods on N2 reverse direction across samples. No significance or stable
abstract superiority follows from this purposive, same-family model test.

[All twelve pairs side by side](../evals/operative-relation/comparison.html) |
[Raw archive and checks](../evals/operative-relation/README.md) |
[Full counts and exceptions](../evals/operative-relation/summary.json)

## What improves and what does not

N2 sample 1's abstract is the sole unanimously preferred candidate. Baseline
names a weighted random swap and connects it to high-residual indices; candidate
states that the candidate test point moves to a sampled position before fitting
while tags remain at their positions. Both reviewers prefer that concrete
operation-to-consequence explanation over extra coverage numbers and the
jackknife+ baseline. They explicitly classify the baseline's shorter explanation
as an omission of useful detail, not false science. N2 sample 2 and N1 sample 1
receive one candidate preference and one tie each, not unanimous gains.

N2 sample 2's Methods is the sole unanimously preferred baseline. Both versions
explain the correct swap, cutoff comparison and total-variation transfer, but
baseline's explicit mass bound for any residual vector makes its reuse under
the original distribution clearer. Candidate's compressed averaging description
does not improve that proof transition. Across Results, baseline receives three
preferences and candidate none: reasons include clearer method names, the link
between longer trajectories and low-count diversity, and the distinction between
temporal average coverage and coverage at every time point. A reminder to retain
operations does not reliably improve every kind of explanation.

All 48 body-only audit judgments mark fidelity pass and the bounded critical
objective supported, in both conditions. This is no fidelity improvement and
not exhaustive proof or citation verification. Auditors accept an abstract-level
causal summary without requiring its complete cutoff derivation, while reviewers
can still prefer a more explicit operation. Passing a broad contribution objective
does not erase that stylistic/detail distinction or establish exemplar learning.
Reader-support judgments are baseline 22 text-grounded / 2 ambiguous and candidate
23 text-grounded / 1 ambiguous. The three ambiguities concern a reader dropping
the uphill qualifier from a slope limit; they are not writer fidelity failures
or evidence of a robust reader advantage. Two auditors rating one reading are
not two independently observed reader events.

The next frontier is to test the abstract-specific operation/detail allocation
on different paper families, preserving negative Methods/Results evidence and
using reader questions whose abstraction level is fixed before generation.
These cases cannot be reused as fresh tests of a rule tuned to their outcomes.
Human blind reading remains unperformed. More universal instructions or maximal
support labels alone would not establish the desired writing improvement.

## Why this narrower test follows broad coverage

The [twelve-paper experiment](broad-writing-evaluation.md) found no overall gain.
The [subsequent synthetic calibration](evaluator-control-calibration.md) passes
its predeclared evaluator admission gate, but does not establish better prose.
This separate test examines a specific hypothesis: compression should preserve
the operation or contrast licensing a consequence, and its indispensable condition,
instead of retaining a method label or replacing an explanation with assumption lists.

Baseline is the current argument-transfer guide, including its read-back check.
Candidate appends only one narrow operation-preservation section. Abstract
decisions, section protocols, measured-event preflight and results guidance are
identical. Five baseline/shared snapshots match their canonical references before
generation. No candidate section is promoted to the runtime guide by this test.

Protocol and guides are frozen before full source-body preparation. The two papers
are purposively selected to contrast an empirical robotics operation with a
theoretical guarantee; this is not another broad efficacy sample or model training.

## Sources and exposure

| ID | Publication | Actual evaluation source |
| --- | --- | --- |
| N1 | [Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning](https://proceedings.mlr.press/v164/rudin22a.html), CoRL 2021 event / PMLR 2022 publication | Complete official ten-page PDF; complete main-body Sections 2-4 |
| N2 | [Conformal Prediction Beyond Exchangeability](https://projecteuclid.org/journals/annals-of-statistics/volume-51/issue-2/Conformal-prediction-beyond-exchangeability/10.1214/23-AOS2276.full), Annals of Statistics 2023 | Authorized [author-hosted manuscript](https://www.stat.cmu.edu/~ryantibs/papers/nexcp.pdf), after publisher access blocking; definitions plus main-body methods, theory, experiments and proofs |

N2 is a statistics journal article, not a top-conference paper. Its retrieved
manuscript has 62 physical pages, including unselected appendices; equivalence
to the journal's paginated version and an exact revision identifier are unverified.
Neither server modification time nor PDF creation time certifies a revision.
No source is substituted based on generated prose quality.

The selected bodies exclude author abstracts, contribution summaries, conclusions,
references and unrelated appendices. N2 explicitly retains necessary Introduction
definitions, including data/test-swapped sequence and total-variation notation,
not the introductory result previews. Complete relevant main-body proofs remain
available. Unrepaired extraction defects, formula layout and ambiguous figures or
tables are disclosed; assessors must not invent a numerical repair.

The two independent preparers and coordinator encounter metadata abstracts during
discovery. Preparers also inspect Introduction/section boundaries, as disclosed
in receipts, but receive neither writing guides nor prior model outputs. Writers,
editors and source auditors are restricted to declared selected bodies; they do
not receive abstracts, complete extraction, PDFs or preparer summary answers.
Prompt restrictions are not filesystem isolation or erasure of pretraining.

Exact titles were not found among the earlier repository cases before registration.
Related robotics and conformal families are development material, and model
pretraining exposure is unknown. These papers become development cases after
this round, not indefinitely reusable held-out data.

## Equal-pass and assessment design

Two fresh initial contexts per paper each write an abstract (150-200 words),
Methods/Analysis explanation (110-160), Results/example interpretation (120-180)
and notes (at most 120). Every exact initial/source/notes packet goes to a fresh
baseline and candidate editor, each making one revision at the same requested
budgets. Twelve writer contexts produce twelve initial and twenty-four final
passages, forming twelve paired units. No quality retry, extra candidate pass,
raw prose repair or output selection occurs.

Independent source preparers freeze one critical question per unit before any
generation. Writers/editors receive the same question as a bounded task objective,
without gold wording or expected answers. This avoids applying a compulsory
source inventory after seeing which paragraph function a writer selected, but
it is not an unconstrained full-paper writing test.

Four anonymous preference contexts give twenty-four judgments, with exactly
reversed A/B order for the second reviewer of each paper. Fidelity pass/concern/fail
remains separate from preference and argument/language scores. Four different
source-free reader contexts give twenty-four reconstructions with literal witnesses.
Readers never see both counterparts of a unit/sample, but may see another
replicate of the same paper; within-paper contamination remains a limit.

Four different body-only source-audit contexts give forty-eight judgments on
twenty-four final passages. They classify actual critical prose support and
whether reader answers are text-grounded, inferred, wrong, unanswered or ambiguous.
Missing explanation is not automatically false science. Successful rejection of
a contradiction does not make the writer's false claim true. Source ambiguity is
uncertain, not an invented fidelity failure.

All contexts inherit the same model family without override or parent-history
fork. Repeated judgments are clustered model outputs, not independent people or
48 independent texts. No statistical significance, acceptance prediction or
population effect is inferred from two papers. Prior-round votes are not pooled.

## Archive and verification

The final archive preserves all raw generations and judgments, frozen
protocol/guides, objectives, mappings, decoded counts and SHA-256 receipts.
PDFs, full extraction, selected publication body, source-boundary recipes and
image renders remain local; publisher accessibility does not authorize relicensing.
Replay of omitted source checks requires the original local bytes. Fresh model
reruns need an explicit runner and independently reviewed source inputs.

Ten separate helper tests exercise immutable writes, identity/path/hash drift,
source metadata variants, complete assessment counts, balanced reversal and
missing-response refusal on temporary synthetic infrastructure fixtures.
Three repository tests initially fail while this archive is absent and pass
after archival. These tests do not judge prose quality.

All 24 raw response files and 75 copied archive files match their original bytes;
all 58 frozen input/hash entries remain unchanged. The selected body assembles
exactly from three N1 and nine N2 original raw-byte spans, with no source repair.
Playwright checks 1440px desktop and 390px mobile, all 36 displayed initial/final
prose strings, filters, expandable evidence and non-overlap; screenshots are
visually inspected. Public byte verification requires no publication download.

One baseline Results passage (N1 sample 1) is 181 words against a 180-word ceiling;
all other 47 prose/note fields meet their budgets. The pair is unanimously tied,
but is retained rather than silently repaired or excluded. All assessment reasons
and reader answers meet budgets. One literal reader core witness (N2_T01) has
20 words against an 18-word limit; it is retained unchanged. This witness belongs
to a candidate Results passage, not a preferred abstract. There are no missing
responses, raw schema repairs or alternative-judgment replacements. One reader's
initial JSON selector fails before a corrected read; one auditor resolves tool
output truncation with smaller reads. Neither is a semantic retry.

Working notes in both conditions retain an unresolved source/implementation
question: experimental descriptions cite equation (14), while the nonsymmetric
random-swap guarantee is for equation (20). The generated prose separates the
conditional theorem from empirical averages rather than asserting that those
experiments implemented the randomized construction. No independent code-level
verification of the experimental implementation is claimed.

The local Python 3.14 regression gate runs 180 repository tests: 179 pass and
one PowerShell-dependent test skips because the executable is unavailable.
All eleven CLI smoke cases and both ten-test helper suites pass. Frontmatter,
compilation and diff checks pass. These validate infrastructure, not prose quality.
No new official venue template, global installation, dependency, model runner,
version bump, commit or GitHub push is introduced.
