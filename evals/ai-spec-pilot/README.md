# Current AI-Spec Writing Pilot

**Completed 2026-10-13. No overall writing gain; the frozen gate fails.**
Candidate / baseline / tie votes: **3 / 10 / 11**. No pooling with earlier rounds,
no model-weight training, and no promotion of runtime writing guidance.

[All 12 pairs side by side](comparison.html) · [Recomputed summary](summary.json) ·
[Located effects and next hypotheses](../../docs/ai-spec-pilot-evaluation.md)

## Conditions and Sources

Two papers, two replicates, Abstract/Methods/Results: 12 pairs and 24 final passages.
Four fresh inherited-model writer contexts each return an actual initial response,
then exactly one edit. No parent-context fork or model override is used.

Baseline uses the pinned argument-transfer, abstract-decisions and writing-protocols
guides. Candidate adds four complete AI-spec records per unit: twelve unit-record
exposures, nine unique records. Common guides match `bfc1406` byte for byte.
No additional STE clarity guide is used.
All nine unique records are writing rules; the full 68-entry catalog and its
technical-term/claim-usage cards are not tested as a bundle here.

The [prepared protocol](PROTOCOL.md) remains unchanged as historical evidence.
[freeze.json](freeze.json) records locally frozen pre-generation inputs, source
identities, selected IDs, questions, counting rule, passes, seed and gate.
This is not external preregistration.

- R01 [DROID RSS PDF](https://www.roboticsproceedings.org/rss20/p120.pdf):
  selected body counts 76,000 successful episodes and 86 task verbs; differing
  landing/arXiv counts are not mixed into the packet.
- R02 [SIMPLER arXiv v1](https://arxiv.org/pdf/2405.05941v1):
  evaluation targets relative policy performance. Table I measures ranking
  agreement, not robot success rate. Inspected sections and PDF hashes are frozen.

Only original editorial [located facts](materials.json) are published, not source
PDFs, full extractions or author abstracts. These passages reconstruct published
research, not new scientific results from Super Writer. Papers retain their rights.

## Preferences and Gate

J02 receives reversed pair order and swapped A/B labels. Original reasons retain
those labels; only score/choice identities are [normalized](normalized_reviews.json).

- Abstract: candidate 0 / baseline 5 / tie 3.
- Methods: candidate 1 / baseline 1 / tie 6.
- Results: candidate 2 / baseline 4 / tie 2.
- DROID: candidate 0 / baseline 6 / tie 6.
- SIMPLER: candidate 3 / baseline 4 / tie 5.
- Pairs: one unanimous candidate, four unanimous baseline, four unanimous ties,
  three disagreements.

Abstract net preference is -5, Methods is 0, and the sole unanimous candidate pair
occurs only on SIMPLER. All three preference criteria fail. No consequential
candidate factual failure or final writer-budget violation is found; those two
checks cannot override the failed gate. Language scores average 4.750 candidate
versus 4.917 baseline: near-ceiling ordinal ratings, not quality percentages.

## Audited Reader Answers

Two prose-only readers answer frozen questions; a separate packet-grounded auditor
checks all 24 passages and all 96 answer/witness records.

- Both conditions: 12/12 passage-fidelity pass, with no improvement in this channel.
- Candidate: 42 recovered / 6 partial answers out of 48.
- Baseline: 40 recovered / 8 partial answers out of 48.
- All 96 witness records match exactly; no witness-check disagreement.
- Six answers exceed the 45-word cap (46-48 words): four baseline and two candidate.
  All are preserved, not trimmed, excluded or replaced. The frozen writer gate
  does not include reader-answer length.

Eight partial Abstract answers omit a ranking component present in the prose:
reader-answer omissions, not eight missing-text failures. Other partials concern
a metric direction, an omitted Pearson result, or an unrecovered qualification.
The two-answer difference is not a general comprehension improvement.
Inspect [responses](raw/) and [located audit reasons](raw/F01.json).

## Budgets and Exposure

All final passages and notes meet writer budgets. Mean final words, baseline then
candidate: Abstract 159.0 / 174.5, Methods 136.0 / 133.25, Results 138.0 / 143.0.
Equal budgets do not mean equal returned lengths.

The counter counts ASCII alphanumeric tokens joined by hyphens or apostrophes.
Common guides total 4,124 counter words; extra records add 2,773. These and byte
receipts are exposure proxies, not service tokenizer counts. The agent interface
does not expose exact token usage, independently verified model version,
temperature or generation seed; inherited configuration is used.

## Reproduce Analysis

From the repository root, Python 3.10 or newer:

```bash
python evals/ai-spec-pilot/archive.py check
python -m unittest discover -s tests -p 'test_ai_spec*.py'
```

The check rebuilds blinding, word counts, normalization, votes, audited-answer
counts and HTML in memory. [Byte receipts](receipts.json) identify experimental
artifacts. `responses/` preserves exact completion strings; `raw/` is their decoded
view. [Prompts](prompts/) and [agent identities](execution.json) record execution.
Derivation commands reject existing outputs. This reproduces analysis, not
deterministic model regeneration.

Optional offline browser check, with operator-supplied Playwright/Chromium
(set `PLAYWRIGHT_MODULE` and `CHROMIUM_PATH` when they are not locally resolved):

```bash
node tools/check_ai_spec_pilot.mjs /tmp/super-writer-pilot-browser-new
```

## Limits

All assessors inherit the same model configuration, not independent humans or
different-model validators. Readers can see both paired texts. Authorized paths
are prompt restrictions, not filesystem quarantine; access traces are unavailable.
The coordinator saw public author abstracts during metadata checks. No absence
of pretraining recall is claimed. Both papers are development material.

One auditor and reference-aspect choices are not an objective recovery oracle.
Small sample size, correlated votes, unequal guide exposure, unequal returned
lengths and reader cap deviations limit interpretation. Software checks establish
artifact integrity, not better writing.

Next hypotheses target contribution-linked evidence, controls attached to their
comparisons, evaluated-object precision, and nonrepetitive interpretation/scope.
They require a separately frozen candidate and fresh cases, not runtime admission.
