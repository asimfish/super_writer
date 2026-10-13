# Embodied Writing Follow-up: Round 3

Date: 2026-09-13. This experiment tests a local candidate, not a released model
or demonstrated general writing improvement. No model weights are trained.

## Change and Split

The [preceding three-paper comparison](embodied-writing-evaluation.md) did not
show an overall improvement. Its OpenVLA, VLFM and RDT-1B examples, together with
the earlier DRIFT/DDAT pilot, are development material for this follow-up.
Changes preserve supplied uncertainty when interpreting close comparisons,
replace redundant table narration with a decision-relevant contrast, avoid
repeated generic disclaimers, and require numerical author queries and sample
counts to respect arithmetic and experimental scope. Two original synthetic
calibration cases cover uncertainty retention and ablation-count attribution.

The new explicit-prompt test papers are
[Octo, RSS 2024](https://www.roboticsproceedings.org/rss20/p090.pdf) and
[FAST, RSS 2025](https://www.roboticsproceedings.org/rss21/p012.pdf).
The experimental targets are Octo's six-domain finetuning table and FAST's
action-token compression table with reconstruction and deployment context.
These papers are new to this test sequence, not proven absent from the model's
pretraining or the skill's full library.

Baseline is the preceding round's uncommitted candidate, not repository HEAD.
Both conditions load `SKILL.md` and the same three writing references. The only
new-condition resource changes are in `abstract-decisions.md` and
`writing-protocols.md`. Thirteen SHA-256 snapshots freeze protocol, eight resource
files, two fact packets and two official PDFs before generation. This evaluates
the selected writing path, not complete skill activation or document production.

## Execution

Two fresh-context generations per paper per condition produce eight abstracts
(150-190 words) and eight experimental passages (180-240 words), each with
separate author notes. All eight raw responses parse as requested JSON; all
sixteen passages meet whitespace-count budgets. No retries, prose edits, or
format repairs were used. Same inherited model/reasoning configuration, without
overrides or fixed seeds; exact backend revision is not recorded by the harness.

Two fresh-context model judges receive anonymously labeled old/new pairs.
Replicate 1 is paired with 1, and 2 with 2; order is reversed for the second
judge. Manuscript preferences and factual objections are separate from note
defects. Rankings use reasons and ties, not uncalibrated numerical quality scores.
Author originals are not ranked this round because previous unequal-context
comparisons were not valid quality controls. Eight paired section comparisons
remain clustered in two papers; judges do not add independent paper samples.

## Observed Results

Each cell lists judge 1 / judge 2's preference for the same paired samples.

| Paper and replicate | Abstract | Experimental passage |
|---|---|---|
| Octo 1 | New / New | Tie / New |
| Octo 2 | New / New | Tie / Tie |
| FAST 1 | Old / Tie | New / New |
| FAST 2 | Tie / Tie | Old / Old |

There is a repeatable preference for the new Octo abstracts in these two samples,
not a general improvement result. They recover the substantive zero-shot
comparison and its unequal training budgets instead of using that space for
generic caution or omitting the result. Experimental preferences are less stable.
The first new FAST passage retains the reusable tokenizer's separate held-out
compression result and distinguishes it from policy-training overlap. Its second
sample omits that contribution and spends the space on implementation and
inference-component details; both judges prefer the old second sample. The
contribution-retention problem therefore remains unresolved. Neither more exact
numbers nor an accurate author note restores a missing manuscript contribution.

Both judges identify no material unsupported or contradicted manuscript claims
against the supplied packets; this is not an exhaustive source audit. Coordinator
checks confirm the displayed table values, units, compression ratios, inference
scope and Octo row arithmetic. All Octo notes preserve the table-average ambiguity,
but those means were explicitly included in both packets: this does not test
whether the new guide independently improves arithmetic. One old note treats
approximately five hours versus less than five hours as needing clarification;
both judges correctly observe that these descriptions need not conflict.

No author comparison, quality percentage, pooled win rate, or statistical
significance claim is made. Retain this candidate for further development rather
than presenting it as a generally validated upgrade. Future tests need new
papers, explicit author contribution priorities, repeated samples and human
judgments. Do not revise these frozen samples or rerun them as fresh evidence.

## Source and Test Limits

The Octo extractor read physical pages 3-6, which accidentally excluded Table I.
The coordinator added page 7's table and caption after visually checking the PDF.
Its printed averages are retained alongside the arithmetic means of its printed
domain values; an unspecified aggregation convention is not silently corrected.
FAST's official PDF has no extractable text layer. OCR corrupted several table
values; both extractor and coordinator checked Table I's rendered image. Raw OCR
and source PDFs are retained locally rather than distributed with this repository.

Extractors did not receive writing guides or original abstracts. However, body
pages included result discussion and FAST's conclusion, and search metadata
exposed the coordinator to the FAST abstract. This is not a no-leakage claim.
Packets provide a subset of the paper: for example, FAST's release is absent
from its packet, so release omission cannot be attributed to the writer. Exact
confidence-interval endpoints were not read from charts. Thus these two papers
do not directly test retention of supplied numerical intervals in experimental
prose; that decision currently has only synthetic evaluator-calibration evidence.

A fresh-context evaluator, with fixture oracles hidden, matched both new cases'
declared preferences and fidelity labels. This tests evaluator discrimination,
not generation improvement or independent human agreement. The eight public
fixtures are calibration examples, never a fresh held-out benchmark.

## Engineering Verification

Python 3.14 ran 163 unittest cases: 162 passed and one PowerShell-unavailable
case skipped. Eleven inherited smoke cases, Python compilation, skill frontmatter
validation, pinned resource reproduction and diff whitespace checks passed.
Runtime scripts, capabilities, activation description, dependencies, imported
pins and licenses are unchanged. No global installation, version bump, Git
commit, push or remote CI run was performed. Cross-platform/document rendering
was not rerun for this text-only change. Linked papers retain their own rights;
only original guidance, synthetic examples and evaluation summaries enter the repo.
