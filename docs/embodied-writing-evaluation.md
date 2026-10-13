# Embodied Writing Evaluation: 2026-09-13

This is a small exploratory comparison of frozen old/new writing references,
not a trained model, a full-workflow evaluation, or evidence of acceptance gains.

## Design

Development used the preceding DRIFT/DDAT writing pilot. This round used three
different papers: [OpenVLA (CoRL 2024)](https://proceedings.mlr.press/v270/kim25c.html),
[VLFM (ICRA 2024)](https://naoki.io/portfolio/vlfm.html), and
[RDT-1B (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/file/49f80e4d2471ad4f2edf4f5f1ab62339-Paper-Conference.pdf).
VLFM uses its version-1 author manuscript, not a verified final proceedings PDF.
The selected experiment targets were parameter-efficient adaptation, value-map
update ablation, and seven-task real-robot comparison, respectively.

The baseline is commit `ff429efcf9ecb90df2ccbed857a7de446d520b64`.
Both conditions load `SKILL.md`, `abstract-decisions.md`, `writing-protocols.md`,
and `results-validation.md`; other resources are not loaded. The new condition
adds contribution-retention, author-query separation and embodied evidence-unit
guidance. Six fresh-context writers receive the same fact packet per paper,
without original abstracts or experimental prose. Each produces one abstract
(150-190 words), one experimental passage (180-240), and separate author notes.
No resampling or prose correction is used. All writers and judges inherit the
same model configuration; no model/reasoning override or fixed seed is supplied.

Two fresh-context model judges receive anonymous candidates in reversed display
orders. Manuscript preferences and factual objections are separated from author
note errors. Original author passages are editorial calibration, not equivalent
controls: they differ in length and rely on surrounding sections. Their rankings
must not be interpreted as beating the original papers.

## Observed Preferences

Both judges produced the same old/new manuscript rankings, even with reversed
candidate order. These are six section comparisons, not twelve independent tests.

| Paper | Abstract | Experimental passage |
|---|---|---|
| OpenVLA | Tie | Old preferred |
| VLFM | Tie | Old preferred |
| RDT-1B | Tie | Tie |

The update did not demonstrate an overall prose improvement. In OpenVLA, the new
abstract recovers new-task adaptation while the old one better covers quantized
inference. The new experimental passage drops available standard errors; both
judges prefer the old passage's retained uncertainty and explicit rank comparison.
VLFM's new abstract adds hardware scope but retains generic disclaimers, so the
intended separation of reporting queries from prose is not reliable. Both VLFM
experimental passages remain close to a table inventory. RDT-1B's new passage
has a more concrete terminal-execution failure, without a consistent preference.

Model preferences are not a factual acceptance gate. Both judges reward VLFM's
old passage for listing 1000/2000/2195 episodes, but those counts describe the
general validation workloads; the packet does not establish their reuse for
every ablation. Its assertion that these comparisons cover those counts is
unverified. The new passage avoids that assertion and asks about matched episodes
in author notes. Retain the raw preference and this coordinator correction.
One judge also flags the old RDT abstract's all-task comparator wording because
ACT has no instruction-following rows; the other does not. They disagree about
whether its task-count author query is warranted. The seven-task count includes
two separately named water-instruction tasks, not an invented extra skill.

Both judges rank generated passages above author comparators. This is not reported
as a quality win: packet coverage, context, length and shared-model style bias
make that comparison unsuitable. For example, the OpenVLA author's 10-15-hour
single-A100 and 8x compute statement is present in the source paragraph but
absent from the packet. Its absence is not evidence of an author hallucination.

## Integrity and Failures

- Fifteen SHA-256 snapshots cover the protocol, eight resource files, three fact
  packets and three PDFs. Inputs remained unchanged during generation and judging.
- All twelve generated passages meet the requested whitespace word counts.
- Five of six raw responses parse as JSON. The new VLFM response has one stray
  U+8C80 character between a closing quote and comma. A derived parse removes
  that character without changing prose; the raw format failure remains recorded.
- An old OpenVLA author note incorrectly alleges an aggregate discrepancy.
  Weighting the four condition scores by 10, 5, 12 and 6 trials yields 68.1818%
  and 68.1879% for the two LoRA ranks, both rounding to the reported 68.2%.
  This is a faulty query, not an incorrect number in the generated manuscript.

## Limits

All three material extractors encountered abstract or discussion text, despite
the planned body-only intake. Writer prompts excluded original prose, but this
does not eliminate upstream fact-selection leakage. These papers were separate
from the preceding pilot, not proven absent from model pretraining or the skill's
entire resource collection. Packets are a bounded subset, not complete papers;
missing packet support alone does not establish that an author claim is false.

The protocol requested dimension scores from 0-4; the actual judge prompts
requested ranked tiers and qualitative fidelity reasons instead. No numeric
dimension scores are reported or reconstructed. Same-family judges are not
independent human validation; reversing order does not remove shared-model bias.
Three papers with one sample per condition cannot establish a stable win rate.
These examples become development material for any subsequent revision.

The next revision should test whether preserving available uncertainty and
selecting one decisive contrast helps more than additional cautionary prose.
Numeric author queries need calculation checks before reaching the user. Use
new embodied papers and repeated generations, followed by human blind review;
do not tune on these outputs and reuse them as fresh held-out evidence. This
patch remains an experimental candidate, not a demonstrated quality upgrade.

Full source PDFs and original passages are not redistributed in this repository.
Local artifacts retain frozen inputs, raw generations, prompts, assignments,
blind mappings, author extraction details and source-audit calculations.
