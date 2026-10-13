# Writing Effect: Current Evidence and Next Test

## Current Verdict

**No stable writing-quality improvement has been demonstrated.** The current
68-entry AI specification now has a separate selected-guidance pilot:
candidate 3 / baseline 10 / tie 11 on 12 DROID/SIMPLER pairs. Its frozen gate
fails, and default guidance remains unchanged. See the
[new trial and located losses](ai-spec-pilot-evaluation.md); older candidates'
results are not inherited or pooled.

The earlier-round diagnosis below recomputes existing saved results; it adds no
observations to those rounds. Their original responses, votes, frozen guides
and source receipts remain unchanged. The newly executed pilot is separate.

## What the Existing Experiments Say

The [broad equal-pass comparison](../evals/broad-writing/summary.json) contains
12 papers, three samples per paper and three units: 108 pairs and 216 preference
votes. Candidate / baseline / tie votes are **12 / 20 / 184**. Each pair has two
judges; correlated votes and samples are not independent paper observations.

- Abstract: 36 pairs; votes 4 / 7 / 61. Twenty-five pairs are unanimous ties and
  eleven are disagreements; none is a unanimous win for either condition.
- Methods: 36 pairs; votes 5 / 11 / 56. Twenty-five unanimous ties, six
  disagreements, one unanimous candidate preference and four unanimous baseline
  preferences. All four unanimous baseline outcomes in the broad round occur here.
- Results: 36 pairs; votes 3 / 2 / 67. Thirty-one unanimous ties and five
  disagreements; none is a unanimous win for either condition.

The [six-paper abstract confirmation](../evals/abstract-transfer/summary.json)
has 12 pairs and 24 votes: **10 / 6 / 8**. Two pairs unanimously favor the
candidate, one the baseline, one ties, and eight disagree. The prespecified
continuation gate fails because of the unanimous baseline counterexample.
Do not pool its votes with the broad round or describe the numerical lead as
significance, general effectiveness or admission of the failed candidate.

In the broad round, descriptive mean language scores are **4.875 in both
conditions**. Argument and selection means favor the baseline. These ordinal
scores are near ceiling, come from same-family model judges and are not a
calibrated measure of reader performance. Ties may reflect similar prose,
strong baselines or limited discrimination; the data do not identify which.

## Located Failure Signals

These are the two reviewers' saved reasons in
[decoded votes](../evals/broad-writing/decoded_votes.json), not a fresh source
audit or the coordinator's independent scientific verification:

- `P04_s2_methods`: the baseline makes sequential draft generation and parallel
  target checking explicit; the candidate compresses the execution schedule.
- `P06_s2_methods`: the baseline connects projection refresh to changing useful
  directions and its tradeoff; the candidate closes with an assumption list.
- `P06_s3_methods`: the baseline explains the one-sided projection/storage
  relation; the candidate leaves the matrix-dimension choice underspecified.
- `P12_s3_methods`: both reviewers flag a missing initialization condition in
  the candidate's boundedness statement; the separate source audit also marks
  this candidate as a concern and its baseline as a pass.

The narrow inference is that some losing passages omit reader-facing operations,
conditions or rationale while retaining plausible terminology. This does not
prove why the candidate protocol caused them, or that a larger dictionary will
repair them. New testing must separate faithful claims, explicit recoverable
relationships and style preference.

## Prepared Test Now Executed

The [prepared protocol](../evals/ai-spec-pilot/PROTOCOL.md) is retained unchanged.
After explicit user authorization, the [execution archive](../evals/ai-spec-pilot/README.md)
freezes common guides, four relevant records per unit, original located facts,
reader questions, budgets, edit passes and decision rules before generation.
Four writer contexts complete actual initial responses and one edit each;
two reviewers, two readers and a separate auditor assess the saved final texts.
This cannot retroactively pass any preceding gate.

DROID uses the [RSS PDF body](https://www.roboticsproceedings.org/rss20/p120.pdf)
with 76k successful episodes and 86 task verbs, excluding differing landing/arXiv
counts. SIMPLER uses [arXiv v1](https://arxiv.org/pdf/2405.05941v1).
The earlier attempted v2 HTML URL did not exist and was not used.
Inspected sections and source hashes are recorded. These are development cases,
not a guarantee against model recall; the coordinator saw public abstracts.

New preferences are Abstract 0 / 5 / 3, Methods 1 / 1 / 6, Results 2 / 4 / 2
(candidate / baseline / tie). Both conditions pass all packet-fidelity checks.
All final writers meet budgets; six reader answers exceed their cap and remain
unaltered. No raw response is replaced. The one unanimous candidate pair does
not satisfy cross-paper support, and neither required unit net favors candidate.

## Engineering Is a Separate Outcome

The first public commit's Windows atlas tests failed across drive letters. The
fix in [`04a655e`](https://github.com/asimfish/super_writer/commit/04a655ec3530b00f2c61332214837c43cc682370)
retains same-drive relative links and uses encoded file URIs across drives.
[Its CI](https://github.com/asimfish/super_writer/actions/runs/38387644453) now
passes all five jobs: Linux 3.10/3.12, macOS 3.12, Windows 3.12 and document/template
fixtures. Locally, 223 of 224 tests pass, with one PowerShell-unavailable skip. That closes
a portability defect, not the writing-effectiveness question.
