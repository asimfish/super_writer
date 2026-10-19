# Explanation-Preserving Compression: Four-Paper Pilot

**The frozen preference gate fails.** The new guide wins against hard compression
8 / 0 / 0, but against the same 150-word-budget legacy guide the result is only
**3 wins / 2 losses / 3 ties**. Extra room explains much of the apparent gain
over the hard-compression baseline. This does not demonstrate a stable writing
improvement or successful learning of excellent-paper style.
The candidate also has one audited training-population error, shared by the
relaxed control; the displayed experimental prose is intentionally uncorrected.

[Four versions side by side](comparison.html) · [Frozen protocol](PROTOCOL.md) ·
[Machine-readable results](summary.json) · [Actual dispatches](execution.json)

## What changed

The failed [six-paper compression pilot](../compression-pilot/README.md) identified
loss of explanatory relationships under a relative no-growth rule. The new guide
protects indispensable explanations and essential co-contributions before cutting,
allocates space to a connected argument, and treats actual author/venue limits
as constraints rather than shorter length as a quality objective.

The runtime [v3 contract](../../references/writing-team.md#schema-3-meaning-and-preservation)
also checks reported relation realization and original-strength preservation.
This experiment ablates the **guide in a single revision pass**, not the complete
four-role runtime, its checker, or a model trained on papers. Both controls get
the same explicit evidence and relation priorities; no treatment has privileged
technical information. Common abstract-decision guidance is strong, so this is
an incremental test beyond that guidance and those priorities.

## Design and sources

Four new-to-this-repository evaluation papers from RSS 2025:

- [MISO](https://www.roboticsproceedings.org/rss21/p004.pdf): local and global
  neural implicit SLAM optimization.
- [Doppler Correspondence](https://www.roboticsproceedings.org/rss21/p005.pdf):
  motion-informed scan association.
- [Building Rome with Convex Optimization](https://www.roboticsproceedings.org/rss21/p032.pdf):
  scaled bundle adjustment and scalable relaxation solving.
- [V-HOP](https://www.roboticsproceedings.org/rss21/p037.pdf): model-based
  visuo-haptic pose tracking.

Two fresh source contexts read PDF body pages after the first page, OCR-extract
scanned PDFs, and visually verify selected mechanisms/tables. Receipts record
page scope and SHA-256 of PDFs/body extraction. The coordinator checked those
hashes and narrowed explanation questions before freezing; ordinary initial
drafts were not optimized. The coordinator saw proceedings abstracts in metadata
discovery, but source/writer contexts did not receive them. This cannot rule out
pretraining familiarity, and paper selection is curated rather than random.

Six fresh writer contexts produce twelve revisions, with one attempt per paper
and condition. `hard` uses the legacy guide and cannot exceed the initial draft;
`relaxed` uses the same guide with authorized growth up to 150 words; `meaning`
uses the new guide under that same cap. The 150-word cap is an experimental
editorial budget, not an official RSS requirement. No minimum or padding target.
All outputs, including any invalid/missing case or budget miss, stay accountable.
Each treatment has two two-paper blocks and equal calls, not equal token costs.

Two anonymous same-model preference contexts see prose only, without facts,
questions, plans, condition identities or original abstracts. The second reverses
labels and case order. They judge all three pairs per paper: 24 pair judgments,
including 8 judgments for each candidate/control comparison. This is not
fully counterbalanced across all three label positions or independent human review.

## Preference and length

Candidate versus relaxed control, by paper:

- MISO: two overall ties; both explain local initialization and global feature
  operations adequately.
- Doppler Correspondence: two losses. The relaxed control states the approximately
  constant-motion/small-rotation assumption; the new guide's version leaves it
  inside the less informative label "short-scan motion approximation."
- Building Rome: two wins. The candidate distinguishes SDP certification from
  recovery of the original problem's optimum and states the recovery conditions.
- V-HOP: one win, one tie. The candidate explicitly contrasts vision without
  contact and haptics under occlusion; one reviewer balances this against the
  control's concrete handover outcome.

All organization judgments are ties. Against the relaxed control, language is
1 win / 0 losses / 7 ties. Thus preference differences mainly reflect explanatory
specificity, not demonstrated improvement in paragraph organization or phrasing.
Do not turn these dependent, same-model judgments into a general win rate.

Mean counter lengths: `hard` 86.25 words, `relaxed` 136.5, `meaning` 142. All twelve
revisions meet their assigned caps. These are four samples per treatment, one
generation each, not a distribution of writing quality. Generated outputs have
not been edited after generation and no unfavorable draft was replaced.

## Reader recovery and fidelity

One fresh reader answers the frozen explanation questions from each prose unit
without facts or reference answers. It also sees two synthetic controls: true
component labels without the needed operation, and an explicit selective-update
operation. A separate evidence-grounded auditor checks actual answers and whether
the prose states or necessarily entails their relationship, rather than crediting
source-aware guesses. It also flags consequential factual errors separately.

Audited recovery is **8/8** for `meaning`, **6/8** for `relaxed`, and **6/8** for
`hard`. The new guide makes 3D-distance/depth-error meaning explicit for XM and
the no-contact/occlusion modality contrast explicit for V-HOP. Both synthetic
controls classify as intended. All requested auxiliary answer/note caps are met.

However, `relaxed` and `meaning` each have one consequential factual concern in
V-HOP: dataset coverage of eight grippers/thirteen objects is described as
training coverage despite held-out entities. This fails the candidate's fidelity
gate. A coordinator post-audit visual check of PDF page 6, Table II, confirms
eight dataset grippers versus seven training grippers. Raw answers, judgments,
inputs and generations are **not** repaired. A separate
[teaching correction](../../examples/writing-team/population-binding.md) is not a
new tested output. Follow-up writer/reviewer reminders are post-pilot engineering
changes, not part of the frozen guide ablation or evidence they fix generation.

All raw reader/auditor completions and located reasons are retained. A reader failure or
extra inferred detail is not automatically a factual error in the passage.
The reader sees all versions in one context, so cross-case inference cannot be
excluded; a single auditor is also fallible. This tests model answer recovery,
not human comprehension or an objective score of abstract quality.

## Interpretation

This pilot does not pass its preregistered continuation gate: preference and
fidelity fail; recovery, synthetic calibration and budget checks pass. The new guide
addresses a real engineering failure mode, but its distinct effect beyond a
relaxed budget remains mixed. The original-strength checks can prevent accepting
a *reported* regression; they do not make the writer's content choices insightful.
Do not add more required sentences or widen the word budget after these results.
The next question is contribution-focused selection and explanatory sufficiency
under matched budgets, with stronger blinded replication and human judgments.
These four papers are now development data for future changes.

## Reproduce the saved experiment

```bash
python evals/explanation-pilot/pilot.py check
python -m unittest discover -s tests -p test_explanation_pilot.py -v
```

`freeze.json` binds source packets, protocol, guide snapshots, code and writer
prompts before dispatch. `blind-freeze.json` and `audit-freeze.json` bind the
evaluation packets. `responses/` preserves exact model completion strings and
agent IDs; `raw/` contains their parsed JSON. `receipts.json` covers the published
archive. All generated prose is public; original paper text, PDFs, original
abstracts and private manuscripts are not redistributed. Reproduction checks
bytes, denominators and arithmetic, not semantic truth or independent authorship.
