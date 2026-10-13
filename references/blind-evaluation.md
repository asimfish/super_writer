# Blind Abstract Evaluation

Use when deciding whether a revised abstract is better than a prior version.
This protocol separates source fidelity from prose preference and does not treat
either as evidence of acceptance probability.

## Reviewer Packet

Give reviewers:

- the same frozen evidence packet for both candidates: ordinarily a fact summary,
  or a declared source body for a prespecified source-grounded review;
- two candidates with randomized labels A/B;
- the target word budget and venue context, if applicable;
- no author abstract supplied as gold wording, condition identities, generation
  prompts, or prior judgments. If original prose is explicitly a comparator,
  disclose that design rather than calling the author answer withheld.

Keep the A/B mapping outside the review page. Preserve untouched review exports
and resolve the mapping only after all reviews are collected.

For body-only generation, record the supplied sections and excluded material.
Withholding an author abstract does not rule out model pretraining exposure.
Preserve raw generations, including budget violations, and keep working notes
out of preference packets. When practical, audit factual claims separately
against primary source tables and conditions; prose-review agreement alone is
not source verification.

## Rating Dimensions

Rate each candidate from 1 to 5 on:

| Dimension | Question |
| --- | --- |
| Contribution clarity | Can the reader state what the paper adds? |
| Motivation/design rationale | Is the problem and reason for the design recoverable without invented gaps? |
| Technical precision | Are terms, metrics, units, and experimental objects exact? |
| Evidence calibration | Do comparisons and conclusion strength match the supplied evidence? |
| Language quality | Is the prose direct, cohesive, conventional, and free of empty promotion? |

Require a preferred candidate or a tie and one decisive reason. Do not ask which
candidate is longer or more similar to the source abstract. A reviewer may mark a
candidate factually unacceptable even when its language is fluent.

## Analysis

Report separately:

1. factual failures and their severity;
2. dimension ratings by version after unblinding; any ordinal-score means are
   descriptive, not a calibrated quality measure;
3. pairwise preferences and ties;
4. reviewer disagreements and reasons;
5. word-budget violations and missing evidence.

Do not convert one sample per paper into a win rate. Repeat across contribution
types and independent reviewers. If a candidate wins language but loses evidence
calibration, do not call the revision an overall improvement without stating the
tradeoff.

## Check Whether the Measurement Can Discriminate

Near-universal ties or maximal understanding scores can mean similar drafts,
a strong baseline, or an insensitive assessment. Do not assume which explanation
is true or keep adding papers solely to accumulate high scores. Use separately
reviewed negative controls and valid alternatives before relying on the measure.
Include a true but explanation-poor passage, a changed metric or claim condition,
and a supported paraphrase or nonessential omission. A legitimate stylistic
preference between valid alternatives is not a false factual judgment.

For a consequential reader question, freeze what the unit is supposed to make
recoverable before generation, without requiring an exemplar's wording or every
source fact. Let a fresh reader answer from prose alone. A separately grounded
auditor checks whether the actual text states or necessarily entails the answer;
source familiarity or a reader's correct guess cannot supply missing text.
Distinguish missing support, contradicted support, source/layout uncertainty and
reader-added specificity. An omitted explanation can weaken writing while all
remaining scientific claims are true.

Keep prose truth separate from reader recovery: a reader can correctly notice
that a paragraph's numbers contradict its main claim. That successful reading
does not make the claim true. Conversely, a correct answer guessed from source
knowledge does not make an omitted explanation recoverable from the prose.

Calibrate both defect detection and false flags on valid prose, then retain
all outcomes and disagreements. Predeclare admission thresholds before judging;
do not lower them after observing failure or pick a favorable rubric afterward.
A constructed-control pass is permission to test a measurement further, not
validated human comprehension, successful exemplar learning or better writing.
