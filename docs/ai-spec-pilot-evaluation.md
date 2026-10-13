# Current AI-Spec Pilot: Located Writing Effects

## Verdict
The selected AI-spec guidance **does not improve overall writing in this pilot**.
DROID and SIMPLER, two replicates and three units produce 12 pairs/24 final passages.
Candidate / baseline / tie preferences are **3 / 10 / 11**. The frozen gate fails;
default argument-transfer guidance remains unchanged.

[Complete comparison](../evals/ai-spec-pilot/comparison.html) ·
[Sources, raw records and limitations](../evals/ai-spec-pilot/README.md) ·
[Recomputed results](../evals/ai-spec-pilot/summary.json)

Abstract votes are 0 / 5 / 3, Methods 1 / 1 / 6, Results 2 / 4 / 2.
Four pairs unanimously favor baseline, one candidate, four tie and three disagree.
This is negative evidence for this context bundle, not proof that every dictionary
entry is harmful or a statistically established population effect.
The treatment selects nine writing-rule records, not the full dictionary,
claim-usage catalog or additional STE context.

## Located Differences
These observations come from the preserved reviewers' reasons, not isolated
causal tests of particular records.

- **R01_s1_abstract, unanimous baseline:** its size-matched diversity check tests
  the opening scene-diversity motivation. Candidate retains scale/co-training
  gains but omits that distinguishing evidence. More facts do not automatically
  connect a contribution to its strongest support.
- **R01_s2_abstract, unanimous baseline:** baseline attaches the common backbone
  to the training comparison. Candidate inserts `All three conditions use the
  same policy backbone.` between qualitative and quantitative results, disrupting
  the argument despite factual correctness.
- **R01_s2_results, unanimous baseline:** baseline evaluates policies trained
  with different data. Candidate says trajectories outperformed trajectories.
  The packet audit passes the contextual claim; reviewers still find the
  evaluated-object wording less exact or natural.
- **R02_s2_results, unanimous baseline:** baseline connects linear agreement,
  margin-aware ordering and the physical check. Candidate adds another caution
  after an already scoped conclusion. Necessary limits need not become repeated
  closing disclaimers.
- **R02_s1_results, unanimous candidate:** it explains the metric alongside its
  values and frames arm wrapping as a prediction test. Baseline repeats its
  interpretation more laboriously. This is a local gain, not a Results-wide one.
- **Methods disagreements:** a baseline preference concerns why nonlinear or
  narrow-range comparisons can mislead Pearson correlation; a candidate
  preference concerns explicitly naming linear association. Better definition
  and better explanatory rationale are separate decisions.

## Accuracy and Understanding
All 12 baseline and 12 candidate passages pass the independent fact-packet audit.
This is not an independent full-PDF review or a fidelity improvement.

Audited answers: candidate 42 recovered / 6 partial; baseline 40 / 8, out of 48.
Both readers recover the candidate's explicit lower-is-better direction where
one baseline Methods passage omits it. But eight Abstract partials are reader
omissions of a component present in the prose. Results trade an omitted Pearson
value against an unrecovered qualification. These counts do not establish general
comprehension improvement or an objective prose-recovery oracle.

All 96 witness records are exact. Six answers exceed 45 words: four baseline,
two candidate; all deviations are retained. All final writer passages/notes meet
the same budgets. No model response is repaired, replaced or excluded. Descriptive
language scores favor baseline 4.917 versus candidate 4.750, but are near ceiling
and ordinal.

## Engineering and Next Test
The offline harness checks complete coverage, reversed labels, original completion
strings, witnessed answers and the unchanged gate. Byte receipts protect the
archive. The horizontal view includes initial drafts, final prose, reader answers,
exact witnesses and reviewer/auditor reasons. Making failures inspectable does
not train model weights or justify runtime promotion.

A next candidate should isolate a smaller contribution-to-evidence decision using
the existing dossier/rationale matrix: bind each foregrounded promise to the
comparison that tests it, place controls with that comparison, name the evaluated
object, and interpret the result once with necessary scope rather than repeated
generic cautions. These are **post-hoc hypotheses, not tested rules**.

Freeze a new candidate before fresh cases. Keep author-abstract comparisons,
human review and non-ceiling recovery assessment separate. Do not reuse this
pilot as held-out confirmation, pool earlier votes or relax the failed gate.
