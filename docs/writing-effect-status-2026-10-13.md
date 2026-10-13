# Writing Effect: Current Evidence and Next Test

## Current Verdict

**No stable writing-quality improvement has been demonstrated.** The current
68-entry AI specification and selective STE-context integration have engineering
and authored contrast tests, but no new independently generated/assessed writing
trial. They must not inherit older candidates' results.

This update recomputes counts from existing saved results; it is not a fresh
generation, a new blind test, or another set of observations. Original responses,
votes, frozen guides and source receipts are unchanged.

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

## Next Test Is Not Yet Executed

The [next-round protocol](../evals/ai-spec-pilot/PROTOCOL.md) proposes an incremental
test of current AI-spec guidance against the same strong common writing guide,
with Abstract, Methods and Results, two replicates and anonymized comparisons.
It is not a rerun that can retroactively pass the earlier failed gate.

Public-source candidates are DROID (dataset/resource contribution) and SIMPLER
(evaluation methodology). A repository search found no occurrences of these
titles in prior development/evaluation records; that is not a guarantee against
model recall. They become development material once inspected. DROID's public
[RSS landing abstract](https://roboticsproceedings.org/rss20/p120.html) and
[current arXiv metadata](https://arxiv.org/abs/2403.12945) give different dataset
counts; source versions must be reconciled before any fact packet is frozen.
[SIMPLER v1](https://arxiv.org/html/2405.05941v1) is confirmed; the attempted v2 HTML URL does not exist. Source preparation
must not mix versions or infer facts from search summaries.

Independent sub-agent generation/review has been requested but not authorized
in the current turn. No agent is dispatched, no draft or judgment is fabricated,
and no new preference count is reported. Materials and mappings are not yet
frozen; the protocol is explicitly a prepared design, not an executed result.

## Engineering Is a Separate Outcome

The first public commit's Windows atlas tests failed across drive letters. The
fix in [`04a655e`](https://github.com/asimfish/super_writer/commit/04a655ec3530b00f2c61332214837c43cc682370)
retains same-drive relative links and uses encoded file URIs across drives.
[Its CI](https://github.com/asimfish/super_writer/actions/runs/38387644453) now
passes all five jobs: Linux 3.10/3.12, macOS 3.12, Windows 3.12 and document/template
fixtures. Locally, 223 of 224 tests pass, with one PowerShell-unavailable skip. That closes
a portability defect, not the writing-effectiveness question.
