# Compression-first writing pilot

**The frozen gate fails.** Compression improves economy, but Abstract preference
against previous guidance is **2 wins / 10 losses**. Results preference is
**7 wins / 5 losses**. Runtime guides were not revised or promoted during testing.

Six RSS 2025 papers, twelve Abstract/Results units, and thirty-six actual revisions
were generated on 2026-10-18. Four-way anonymous comparison includes the shared
initial draft. Conditions are previous guidance at `3f9d99c`, compression-first
guidance at `870a205`, and ordinary editorial revision.

[All passages side by side](comparison.html) · [Recomputed results](summary.json) ·
[Frozen protocol](PROTOCOL.md) · [Input receipts](freeze.json)

## Results

Counts below are correlated reviewer votes, not independent papers. Each unit has
one revision per condition and two same-model reviewers.

| Compression compared with | Wins | Losses | Ties |
|---|---:|---:|---:|
| Previous guidance, all units | 9 | 15 | 0 |
| Previous guidance, Abstract | 2 | 10 | 0 |
| Previous guidance, Results | 7 | 5 | 0 |
| Ordinary editorial revision, all units | 16 | 6 | 2 |
| Shared initial draft, all units | 24 | 0 | 0 |

| Mean words | Shared draft | Previous guidance | Compression | Ordinary revision |
|---|---:|---:|---:|---:|
| Abstract | 100.2 | 139.7 | 90.8 | 140.5 |
| Results | 78.7 | 109.3 | 71.5 | 107.8 |

Compression beats previous guidance on economy in all 24 votes, but clarity is
6 wins / 15 losses / 3 ties. The preferred previous abstracts explain more of the
scientific relationship: tokenizer reconstruction versus online feedback,
reciprocal hand-arm reconstruction, or near-zero importance weights motivating
resampling. The candidate sometimes retains the right labels and answers while
losing that explanatory substance. The Results gains instead come from removing
irrelevant score inventories and selecting the comparison that answers the
paragraph's question. Neither pattern licenses a universal length rule.

All three revised conditions receive 48/48 fully recovered question assessments;
the initial drafts receive 22 recovered / 26 partial. Thus this measurement does
not distinguish their writing quality. Reviewers know the evidence, so recovery
can also reflect source-informed inference rather than prose alone.

One candidate exceeds its frozen relative budget: R04 Results has 85 words versus
an 84-word original. It is retained unchanged. Both reviewers flag one technical
error in the shared R05 initial abstract: landmark construction omits adding scene
points to predicted offsets. All revisions repair it. The two flags concern the
same passage, not two distinct errors. Therefore gains against the initial draft
partly include factual repair and cannot be interpreted as pure style gains.
No consequential factual concern is recorded for the revised passages.
Of 192 reviewer answers, 32 exceed the requested 25-word answer cap under the
declared counter; all are retained. No reviewer-reason or writer-note cap is
exceeded. These auxiliary answer limits are outside the frozen writer gate.

The gate fails on preference against the previous system, especially Abstract,
and on the candidate budget deviation. A pass on recovery or economy cannot
override those failures.

## Comparison with author abstracts

The separately declared [exploratory study](REFERENCE_STUDY.md) compares the saved
candidate with each original author abstract, after all primary writing finished.
Two fresh reviewers give the candidate **5 wins / 7 losses** overall;
organization is **4 wins / 7 losses / 1 tie**, language **3 / 8 / 1**, and economy
**9 / 0 / 3**. [Saved judgments and mapping](reference-summary.json) retain all
reasons. Original texts stay private; [source receipts](reference-manifest.json)
publish their hashes, lengths and URLs.

Both reviewers prefer the author on RDP, ArticuBot and DemoGen. Their recurring
reason is a clearer problem-to-design-to-contribution progression. Our candidate
can interrupt that progression with deployment prerequisites, a narrow baseline
exception or a closing implementation qualification. The author RDP abstract
also motivates both demonstration collection and reactive control; our input's
contribution statement privileges the controller, so this difference partly
originates in evidence prioritization before drafting. Both reviewers prefer our
candidate on Sim-and-Real Co-Training and CordViP, where selective comparative
evidence improves on generic outcome language. Safety-control judgments disagree.

Author abstracts range from 147 to 250 counter words, while candidates use 78-96.
The author had the full paper and our writers had selected facts and a short
initial draft. This comparison identifies remaining gaps; it does not isolate a
causal effect of the candidate rules or establish that shorter prose is worse.

The next hypothesis is to protect the indispensable explanatory relationship
and confirmed co-contributions before compressing. A relative no-expansion rule
should not substitute for deciding which information earns space. It remains a
hypothesis requiring fresh inputs; these six papers are now development material.

## Materials and execution

Two fresh source-preparation contexts read pages 2-10 of the primary PDFs and
produced original, located fact paraphrases and readable initial drafts. They
checked numerical tables visually. First pages and author abstracts were excluded
from writer packets. Full PDFs and OCR outputs remain outside the repository.

- [Reactive Diffusion Policy](https://www.roboticsproceedings.org/rss21/p052.pdf)
- [Sim-and-Real Co-Training](https://www.roboticsproceedings.org/rss21/p109.pdf)
- [CordViP](https://www.roboticsproceedings.org/rss21/p110.pdf)
- [Safe Beyond the Horizon](https://www.roboticsproceedings.org/rss21/p112.pdf)
- [ArticuBot](https://www.roboticsproceedings.org/rss21/p156.pdf)
- [DemoGen](https://www.roboticsproceedings.org/rss21/p157.pdf)

The first three papers form one writer block and the other three form another.
Each condition has one new context per block; each writer returns six revisions
in one batch. Model and reasoning settings are inherited without overrides.
[Execution records](execution.json) record identities and exact dispatch messages;
[responses](responses/) preserve completion strings and [raw](raw/) contains their
decoded JSON. No prose-quality retry is performed.

The two system conditions receive the same facts, drafts, questions, protocols,
AI rules, and existing exemplar notes. The candidate also receives the compression
guide and revised role cards. Ordinary editorial revision receives the common
facts and a concision/clarity instruction. Absolute ceilings are 160 words for
Abstract and 130 for Results; the candidate additionally cannot exceed the
initial draft. The conditions therefore have different effective length limits
and guidance exposure. This tests the bundle, not the isolated effect of one rule
or independent execution of the full four-role writing loop.

Two fresh reviewers see anonymous A/B/C/D versions, common evidence and reader
questions. The second sees reversed unit order and reversed labels. Neither sees
condition identities, prompts, writer notes, word counts or the acceptance gate.
Each compares all six pairs, checks factual fidelity, and answers two questions
with exact prose witnesses. Recovery is evidence-aware reviewer assessment,
rather than an independent prose-only reading study.

## Reproduce

Python 3.10 or newer, from the repository root:

```bash
python evals/compression-pilot/pilot.py check
python evals/compression-pilot/reference_archive.py check
python evals/compression-pilot/audit.py check
python -m unittest discover -s tests -p test_compression_pilot.py
```

The check verifies frozen inputs and recomputes votes, lengths, recovery, fidelity
concerns and HTML. It reproduces saved analysis, not deterministic model output.
Preparation and analysis commands create new outputs exclusively; keep raw runs
instead of overwriting them. Optional browser checks require local Playwright and
Chromium:

```bash
python evals/compression-pilot/check_browser.py /tmp/compression-browser-new
```

## Limits

Each paper has one generation per condition, with two correlated same-model
reviewers. Votes are not independent papers or human preferences. Source choice,
fact selection, initial drafts and reader questions are editorial decisions.
Some questions are multipart and may favor detailed answers. An omitted detail
can reduce recovery without making a shorter abstract bad scientific prose.
Prompt-scoped access is not filesystem quarantine; model pretraining recall is
not excluded. Absence from earlier repository experiments is not proof that a
model has never seen a paper. No target-author abstract is a gold comparator here.

All budget violations, disagreements and negative results are retained. Runtime
guidance remains at the tested commit throughout this pilot. Better preferences
in this sample would not establish that the system has learned excellent-paper
writing in general.
