# Five-Paper Argument-Driven Development Follow-up

[中文三栏对照：作者概述／上一版／本轮候选](comparison.html)

This is a developmental response to the user's critique of the previous five
abstracts: repeated task numbers, flat sentence sequences and insufficient use
of familiar functional expressions. It is **not a new blind test**, an equal-budget
A/B experiment or a measured writing-quality improvement.

## Preserved and New Material

- `../abstract-five/` remains unchanged, including the old Chinese passages.
- `baseline.json` preserves the actual old English writer outputs and their
  self-reported counts. A common deterministic recount gives 149/212/160/149/149
  words for P01-P05, not the earlier displayed 145/209/147/141/143. The old page
  is not silently corrected; the new page labels its recount explicitly.
- `evidence.json` preserves the same body-derived facts and source locations,
  including unresolved reporting ambiguities. Public paper facts are not a
  license to invent missing literature gaps or average incompatible outcomes.
- `candidates.json` contains new English drafts, Chinese translations, selected
  evidence roles, sentence progression and actual functional-card IDs.
- `audit.json` records a separate context's source/translation reading, not a
  human quality score or blind preference vote. Reported flags remain visible.
- `corrections.json` preserves a host-authored factual correction to P02 separately
  from its raw generation. The page labels the corrected version and retains the
  raw English/Chinese inside its evidence notes. `correction-audit.json` rechecks
  only those changes, not the entire experiment or its writing quality.
- `receipts.json` records source/input hashes, writer identity and access limits.
  `render.py --check` verifies that the committed HTML matches its data.

Guide/catalog hashes record the generation state; they do not freeze the live
guides against future improvements. This demonstration does not archive a full
model environment or promise deterministic regeneration. Historical prose/data
are preserved separately from mutable runtime guidance.

The previous `factual_audit: pass` labels were authored labels, not a completed
independent certification. This follow-up does not reuse them as validation.
The author's Chinese column remains a summary, **not a full literal translation**.
Read the linked paper for the complete original English abstract. CoRL 2024
papers appeared in PMLR volume 270 in 2025; publication and conference years differ.

The independent audit found a real source conflict: Sparsh's prose and packet
characterization of I-JEPA on textiles contradict Table 10. The raw draft inherited
it. The displayed correction removes that task ranking in both languages instead
of guessing which source component should be rewritten, and uses an approximate
pretraining count rather than false precision. The raw issue is not relabeled
as a pass. Four other drafts had no issue found in the claims checked, which
does not certify every source fact or prove better writing.

## Generation Contract

One fresh-context writer receives the same three body-only evidence packets,
the revised argument/abstract guides and a small selected subset of the new
functional patterns. It is instructed not to read full author abstracts or
previous drafts and uses one authored candidate per paper, at most 200 English
words, without a lower length target. No provider setting or model override is
made. The host has read the author abstracts; source-derived rhetorical notes
may also be visible in selected cards. Tools are not sandbox-isolated. These
conditions cannot establish absence of indirect source influence or model
pretraining familiarity. The five cases are development data now.

The intervention selects facts by reader question, not by coverage: explain the
main operation, retain essential complementary contributions, choose a decisive
comparison, and make the next sentence answer or revise the previous one.
No universal one-number limit or compulsory five-sentence outline is applied.
Important contrary results remain; protocol inventories and generic caveats do
not automatically deserve abstract space. Open source ambiguities belong in
notes, with only a supported claim used in the prose.

## What This Can Establish

The displayed passages and selection notes let a reader inspect whether the
proposed edit actually changes information allocation and sentence relationships.
Catalog, source-binding, translation and browser checks cover their stated
boundaries only. They do not establish human preference, causal effectiveness
of a guide or reliable transfer to unseen papers. No new win rate is reported.
Older frozen evaluation outputs and failed quality gates remain unchanged.

Host editorial self-review still finds room to improve: the EquiBot draft retains
several adjacent evaluation statements, Sparsh spends substantial space on the
training/probing recipe, and PoliFormer's memory caveat interrupts the transition
to BoxNav. These are specific remaining organization questions, not automatic
failure labels or independent reviewer votes. The new process is not yet evidence
that every generated paragraph has learned the exemplar's writing decisions.

```bash
python3.14 evals/abstract-argument/render.py
python3.14 evals/abstract-argument/render.py --check
python3.14 -m unittest discover -s tests -p 'test_abstract_argument.py'
# Optional, with Playwright and a local browser installed:
python evals/abstract-argument/check_browser.py /absolute/output/directory --chrome /path/to/chrome
```

All source-located annotations, generated prose and editorial notes are separate
from the paper authors' statements; no original English abstracts or PDFs are
bundled. Linked works retain their rights.

## Local Verification

- Python 3.14: 382 unit/contract/regression tests, 381 passed and one skipped
  because PowerShell is unavailable locally. No skip is a writing-quality vote.
- Smoke suite: 11 checks. Release build and extracted lookup retain the new cards.
- Comparison HTML: 1440, 960, 390 and 320 pixel widths, five anchors, collapsed
  evidence/English toggles, no overflow, browser errors or remote requests.
- Architecture atlas: 1600, 900 and 390 pixel widths; 76 full records, functional
  filters and source/discourse boundaries verified; overview PNG refreshed.
- Earlier frozen experiment checks and the unchanged default guide are retained.
- Source audit: 38 checked claims, one substantive raw source conflict recorded;
  two host factual corrections separately rechecked, not a blind preference trial.

These are local checks. Remote CI and writing effectiveness require their own
evidence and are not inferred from this list.
