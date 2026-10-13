# Broad writing revision evaluation (2026-10-11)

## Result first

**No overall writing improvement was demonstrated.** This completed comparison
uses twelve real papers, six domains, three samples per paper and three writing
units: Abstract, Methods/Analysis and Results. Two anonymous reviewers cast
216 votes on 108 equal-pass pairs: candidate 12, baseline 20, tie 184. Only one
pair unanimously favors the candidate; four favor the baseline, 81 tie and
22 have reviewer disagreement. These are model judgments, not quality gains.

[Read all 108 pairs side by side](../evals/broad-writing/comparison-complete.html)
or inspect the [artifact index](../evals/broad-writing/README.md). Initial drafts,
final prose, disagreements and failures remain unchanged. The author abstracts
are not a scored condition and are not redistributed.

## Question and frozen design

Does an additional final-prose read-back and measured-outcome-definition check
improve a strong editor's explanation, rather than merely its working notes?
The [original protocol](../evals/broad-writing/PROTOCOL.md), guide snapshots and
budgets were frozen before body preparation or generation. This tests a bounded
guidance bundle, not a complete skill workflow, venue formatting, model-weight
training or a separate causal effect for either check.

Baseline uses the pre-read-back argument guide and pre-outcome-definition
abstract preflight/Results guide. Candidate uses their current counterparts.
Shared abstract and writing-protocol guidance is identical. Initial writers
use the shared guidance. For each sample, two fresh editors receive the same
initial prose, notes and selected source body, with exactly one revision each.
The candidate has no extra revision or word budget. Notes are allowed to both
editors but are not supplied to anonymous reviewers or readers.

| Stage | Fresh contexts | Outputs |
| --- | ---: | ---: |
| Source preparation | 6 | 12 selected bodies and 72 editorial grounding anchors |
| Initial drafting | 18 | 108 passages plus 36 case-level notes |
| Baseline/candidate revision | 36 | 216 final passages plus 72 case-level notes |
| Anonymous preference | 12 | 216 pair judgments |
| Prose-only reading | 12 | 216 individual reconstructions |
| Primary source/understanding audit | 6 | 216 audit judgments |
| Supplementary text-only audit | 6 | 216 separate audit judgments |

There are 84 primary output contexts, six supplementary output contexts and
six source-preparation contexts: 96 in total. Source preparation is not a prose
condition. Supplementary auditing is not part of the original primary protocol.
Every context inherits the same model family, without a model override or
forked parent history. Fresh contexts do not establish independent model
families, erased pretraining knowledge or human independence.

Within each domain, one writer/editor context covers two papers and all three
units. The three samples use fresh contexts, not three revisions of a selected
winner. Reviewers see 18 pairs per domain with exactly reversed A/B order;
initial drafts, notes, guides and condition names are withheld. All planned
primary responses were saved before decoding condition mappings. No output
was repaired, padded, selected or regenerated for quality.

## Source coverage and boundaries

| Domain | Papers and publication family |
| --- | --- |
| Robotics | P01 [Diffusion Meets DAgger](https://www.roboticsproceedings.org/rss20/p048.html), RSS 2024; P13 [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://www.roboticsproceedings.org/rss19/p016.html), RSS 2023 |
| Efficient inference | P03 [FlashAttention-2](https://openreview.net/forum?id=mZn2Xyh9Ec), ICLR 2024; P04 [Speculative Decoding](https://proceedings.mlr.press/v202/leviathan23a.html), ICML 2023 |
| Adaptation/training | P05 [DoRA](https://research.nvidia.com/labs/lpr/publication/liu2024dora/), ICML 2024; P06 [GaLore](https://arxiv.org/abs/2403.03507), ICML 2024 |
| Language evaluation/retrieval | P07 [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), TACL 2024; P08 [Self-RAG](https://openreview.net/forum?id=hSyW5go0v8), ICLR 2024 |
| Vision/graphics | P09 [ConvNeXt](https://openaccess.thecvf.com/content/CVPR2022/html/Liu_A_ConvNet_for_the_2020s_CVPR_2022_paper.html), CVPR 2022; P10 [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/), SIGGRAPH/TOG 2023 |
| Uncertainty/theory | P11 [Conformal Risk Control](https://openreview.net/forum?id=33XGfHLtZg), ICLR 2024; P12 [Adaptive Conformal Inference](https://arxiv.org/abs/2106.00170), NeurIPS 2021 |

This covers seven venue/publication families, not seven official format tests.
Sampling is purposive, two papers per domain, not representative random
sampling. Repository searches found no documented exact-title/registered-alias
case before generation; FlashAttention-2 overlaps the previously studied
FlashAttention family, and P13 has related action-chunking concept exposure in
the imported library. Model-pretraining exposure is unknown for every paper.
These papers are development data for subsequent changes, not future holdouts.

P02 ScrewMimic was excluded after three bounded official-PDF download attempts
left incomplete bytes and no usable body/anchors. P13 replaced it **before any
generation**, for availability only. The original registry, planned prompts and
[failure/replacement receipts](../evals/broad-writing/replacements.json) remain
archived. Original protocol references to P02 are preserved, not silently edited.

The twelve selected bodies contain 61,165 whitespace-delimited words, ranging
from 3,541 to 8,968 per paper. They retain complete relevant Methods/Analysis,
Experiments and located limitations, including related supplementary sections
where declared. Abstracts, Introductions, summary conclusions, references and
unrelated appendices are excluded. Source preparers/coordinator may see author
abstracts in discovery metadata; writer/editor inputs do not include them.
Poppler 26.03.0 raw extraction is not repaired or normalized. Frozen anchors
locate a core relationship and consequential scope per unit; they are not a
mandatory result inventory, gold wording or a copied author abstract.

Official ICLR proceedings PDFs replace blocked OpenReview downloads for
P03/P08/P11. P10 explicitly uses the pinned arXiv v1 fallback, not a claim to
have reproduced the final publisher version. P11's finalized official download
removes a trailing remainder from an earlier overlapping transfer, using the
official response/PDF length and EOF; it does not rewrite internal PDF bytes.
P09 includes its official supplement. P13's original table/prose task-count
inconsistency and annotation/extraction warnings are retained. Receipts include
URLs, version boundaries, hashes, section/page/byte ranges and extraction recipes
in [source_receipts.json](../evals/broad-writing/source_receipts.json).

Some definitions occur in an excluded Introduction, for example P11's initial
risk-control display and P12's CQR definition. Retained proofs/analysis provide
some corresponding support, but the body-only task is not whole-paper context.
Flattened equations, checkbox tables and graphical evidence remain limitations.
The primary auditors could inspect permitted PDF layouts; the supplementary
auditors deliberately could not.

## Anonymous preference outcomes

| Domain | Candidate | Baseline | Tie |
| --- | ---: | ---: | ---: |
| Robotics | 3 | 4 | 29 |
| Efficient inference | 3 | 4 | 29 |
| Adaptation/training | 2 | 6 | 28 |
| Language evaluation/retrieval | 0 | 0 | 36 |
| Vision/graphics | 4 | 1 | 31 |
| Uncertainty/theory | 0 | 5 | 31 |
| **Total** | **12** | **20** | **184** |

| Unit | Candidate | Baseline | Tie |
| --- | ---: | ---: | ---: |
| Abstract | 4 | 7 | 61 |
| Methods/Analysis | 5 | 11 | 56 |
| Results | 3 | 2 | 67 |

Sample 1 has candidate/baseline/tie counts 1/4/67, sample 2 has 8/9/55 and
sample 3 has 3/7/62. Paper-level outcomes, ordinal ratings and every located
reason are in [summary.json](../evals/broad-writing/summary.json) and
[decoded_votes.json](../evals/broad-writing/decoded_votes.json). No domain or
unit is removed because its result is inconvenient.

The mean signed preference, first averaged within paper with candidate +1,
baseline -1 and tie 0, is -0.0370. The frozen 10,000-draw, within-domain
paper-cluster bootstrap (seed 20261013) gives a descriptive interval
[-0.0741, 0]. This is conditional on twelve curated papers, not a population
significance test or proof that the skill generally worsens writing. Contexts
cover two papers in one domain, so within-domain assessor/generation dependence
also remains; 216 votes are not 216 independent experiments. Do not pool earlier
pilots or supplementary source labels with this primary outcome.

Baseline/candidate ordinal means are contribution 5.000/4.995, argument
4.958/4.903, selection 4.903/4.856 and language 4.875/4.875. Near-ceiling model
ratings do not quantify a percentage quality gain or validate human quality.

### The five unanimous non-ties

These cases illustrate all unanimous directional outcomes, not selected winners.
They motivate hypotheses, not proven causes of the aggregate outcome.

- [P04/sample 2 Methods](../evals/broad-writing/comparison-complete.html#P04_s2_methods):
  both reviewers prefer baseline. It explicitly connects sequential drafting
  to concurrent target verification and the latency expression; candidate
  compresses the execution schedule into implications.
- [P06/sample 2 Methods](../evals/broad-writing/comparison-complete.html#P06_s2_methods):
  both prefer baseline. It explains why refreshing a gradient projection
  follows useful directions and has a frequency/cost tradeoff. Candidate's
  assumption list is accurate but less explanatory.
- [P06/sample 3 Methods](../evals/broad-writing/comparison-complete.html#P06_s3_methods):
  both prefer baseline. It retains the dimension-dependent projection rule and
  resulting moment-space dimensions. Candidate's generic reference to matrix
  dimensions loses an operational rule, not merely another number.
- [P10/sample 2 Methods](../evals/broad-writing/comparison-complete.html#P10_s2_methods):
  both prefer candidate and flag baseline's display/gradient-cutoff wording as
  conflating fitting and viewing. Primary and supplementary source auditors
  nevertheless mark both passages pass. That cross-assessor disagreement remains
  visible; an audit pass does not certify away the reviewers' localized concern.
- [P12/sample 3 Methods](../evals/broad-writing/comparison-complete.html#P12_s3_methods):
  both prefer baseline. Candidate omits the initialization condition needed
  before asserting the adaptive parameter bound. Both source audit rounds also
  mark the candidate concern, with partial scope recovery.

The substantive lesson is not to append more cautions. An editor must preserve
the operation that permits a consequence and the condition that makes a claim
true. Accurate assumption lists alone can weaken an explanation by replacing
its reason or execution sequence. The bundle test does not identify which
instruction, model behavior or compression choice caused each loss.

## Prose-only understanding and source auditing

Two fresh reader contexts per domain receive individual anonymous paragraphs,
generic unit-appropriate questions and no source, title metadata, anchors, guide,
notes or scores. Each sees nine baseline and nine candidate texts and never
both versions of the same unit/sample. They can see other replicates of the
same paper; this contamination and model recall are not eliminated. Source
auditors then judge the written claims and the separate readers' reconstructions.
Core/scope scores are 0 absent/wrong, 1 partial and 2 recoverable; fidelity is
pass/concern/fail and is not substituted for a prose preference.

| Audit round | Condition | Fidelity pass / concern / fail | Core mean (0-2) | Scope mean (0-2) |
| --- | --- | ---: | ---: | ---: |
| Primary | Baseline | 107 / 1 / 0 | 2.0000 | 1.9907 |
| Primary | Candidate | 107 / 1 / 0 | 2.0000 | 1.9907 |
| Supplementary text-only | Baseline | 107 / 1 / 0 | 2.0000 | 1.9815 |
| Supplementary text-only | Candidate | 107 / 1 / 0 | 1.9907 | 1.9907 |

Primary auditors award core 2 to **every one of the 216 reconstructions**.
This measure is non-discriminating here, not evidence that the new guidance
improves understanding or that every text has learned excellent writing.
The quality reviewers separately record 211 pass/5 concern ratings for baseline
and 213 pass/3 concern for candidate (216 ratings per condition), illustrating
that prose reviewers and source auditors need not agree.

Primary concerns are baseline P01/sample 1 Abstract's apparently guaranteed
overshoot avoidance, rather than conditional mitigation, and candidate
P12/sample 3 Methods' missing initialization condition. The first receives
partial scope recovery and writer-error/text-ambiguity labels; the second
receives a missing-text label. These are preserved judgments, not repaired prose.

### Supplementary access-limited replication

Primary auditors D2, D4 and D6 reported accidental visibility of excluded
summary, Related Work or introductory PDF text. Their claim not to have used
it cannot be verified. The [supplementary protocol](../evals/broad-writing/supplemental/PROTOCOL.md)
was registered after primary responses were saved but before their judgments
were read/decoded. It replicates **all six domains**, not just convenient cases,
in six fresh contexts using locked body inputs, frozen anchors and identical
anonymous text/reader packets. PDFs, full extractions, metadata, guides, primary
scores, preferences and mappings are not supplied. This is input withholding,
not cryptographic filesystem isolation or erased pretraining knowledge.

All 216 supplementary judgments are retained separately. Fidelity labels agree
on 214 texts, core scores on 215 and scope scores on 213; six texts differ in
at least one label/score/failure type. No primary label is replaced or pooled
with a more favorable supplementary judgment. The
[separate summary and original reasons](../evals/broad-writing/supplemental/summary.json)
preserve the disagreements.

The supplementary auditor clears the primary P01 abstract concern, but flags
baseline P06/sample 2 Results because flattened checkbox entries do not verify
the claimed shared per-layer update setting. That is source-layout uncertainty,
not an established numerical or writer error; primary PDF inspection supports
the setting. A P07 reading adds an exact sequence length to prose that only says
within the training window. One P10 reading says real-time reconstruction where
prose distinguishes rendering from a minutes-long fitting budget. These are
reader-side issues, not invented author results. P12's candidate concern persists.
Assessor variation and removal of PDF layout can both explain differences;
the replication cannot isolate the effect of accidental exposure.

## Budgets and operational deviations

Abstracts must be 150-200 words, Methods/Analysis 110-160, Results 120-180 and
case-level notes at most 120. All 108 initial passages, 216 final passages and
108 note fields pass: **432 fields**, with no schema failures or generation
repairs/retries. Baseline/candidate mean words are 177.61/175.22 for Abstract,
142.06/141.39 for Methods and 160.31/159.08 for Results. Notes average
80.31/86.81; more notes are not evidence of better prose or a larger allowance.

Assessment compliance is not perfect. Twenty-two reader responses exceed their
90-word total budget. One reader witness lowercases an initial capital, failing
the literal-substring requirement without demonstrating a scientific error.
Three reviewer reasons exceed 65 words (68, 67 and 67); primary and supplementary
audit reasons meet their 90-word budgets. These responses are neither dropped
nor edited, and the primary scores/counts are not recomputed to hide them.
See [verification.json](../evals/broad-writing/verification.json),
[reader diagnostics](../evals/broad-writing/reader_diagnostics.json) and
[assessment word counts](../evals/broad-writing/assessment_word_counts.json).

## Artifact and software verification

The public archive contains 84 byte-identical primary raw files and six
supplementary raw files, frozen guide snapshots, original judgments, source
receipts/extraction recipes, decoded mappings, execution receipts, helpers and
portable prompts. Condition maps were private during assessment and are public
only for inspection afterward. Source PDFs, raw/body publisher prose, rendered
pages and source-containing packets stay local and are not relicensed.

A 21-token source-overlap diagnostic compares all 324 generated prose passages
and 108 notes with full local PDF extractions, including author abstracts. It
finds no match of at least 21 contiguous normalized tokens. This is not an
originality or plagiarism certificate: extraction defects, short phrases,
translations and other sources are outside its reach.

Python 3.14: 174 repository tests, 173 passes and one unavailable-PowerShell
skip; 11 CLI smoke cases pass. Thirteen experiment-helper tests check immutable
outputs, schema/missingness, reversal/reader separation, hash drift, decoding,
budget sensitivity, separate supplementary results and archive refusal gates.
They validate infrastructure, not semantic ratings or author-paper correctness.
Frontmatter, compilation, public byte receipts and whitespace checks pass.
The [terminal check record](../evals/broad-writing/verification.final.json)
marks only artifact/software completion pass; it does not mark scientific
improvement, perfect protocol compliance or a release as achieved.

Playwright checks the completed HTML at 1440x1000 and 390x844: all 324 displayed
prose strings match the raw files, 216 separate supplementary audit entries are
present, filters/details work, and no page errors, text overflow or column
overlap are observed. The earlier primary-only HTML and its browser receipt
remain archived as snapshots. No new template compilation is claimed.

The archive can verify its public bytes without retrieving papers. Reconstructing
body inputs and a fresh scientific rerun additionally needs the pinned PDFs,
matching Poppler/extraction bytes, private packet reconstruction and an explicit
agent runner. Helpers refuse to overwrite saved artifacts. Model generations
and judgments are not deterministic; archived prompts are not a paid-API runner.

No runtime writing guide, imported resource pin, skill version, installation,
model weights, commit or remote push changes in this experiment round. The
complete multi-stage skill and independent human effectiveness remain unverified.

## Next frontier, not a completed experiment

The broader repeated comparison is complete; repeating easy near-ceiling tasks
alone will not establish progress. Future work should first test the measurement
and explanation failure modes, then freeze a new intervention before fresh papers.

1. Calibrate readers/reviewers with independently labeled negative controls:
   remove an operation-to-consequence relation, change an outcome's measured
   event, or omit a necessary guarantee condition while retaining fluent prose.
   Test detection and justified ties before relying on another large rating run.
2. Use finer-grained, text-located comprehension questions and readers unfamiliar
   with a paper, preferably human/domain reviewers. Separate writer omissions,
   reader-added facts and source-layout uncertainty rather than giving all core
   relationships a coarse maximum score.
3. Study a repair that preserves execution sequence and causal/interpretive
   relations under compression, instead of adding assumption or caveat lists.
   Freeze it and separate read-back from outcome-definition effects with an
   explicit factorial or ablation design and equal revision budgets.
4. Evaluate fresh papers and less-polished drafts after calibration; keep this
   twelve-paper set as development data. Extend to introductions, related work,
   complete Results sections and heterogeneous author priorities before claiming
   a full-system or venue-style improvement. Do not score an author abstract
   with fuller information as an equal-input generated baseline.

These are plans, not results or a release certification. The current evidence
supports a better-documented evaluation system and concrete explanation failures,
not an established gain in writing quality.
