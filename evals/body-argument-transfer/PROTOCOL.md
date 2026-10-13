# Real-body argument-transfer pilot

Frozen before generation on 2026-10-10. Two papers not previously used in this
repository's exemplar notes or development reports are selected from CoRL 2024,
published in PMLR 270 in 2025: Equivariant Diffusion Policy and ReMix. This means
unexposed to this skill's documented development, not unseen by model pretraining.

The shared inputs are mechanically extracted Background/Methods, Experiments
and limitations passages from official PDFs. Page 1, Introduction, the conclusion
summary, author abstracts, acknowledgments and references are excluded. Text
extraction is not repaired; tables and mathematical notation retain extraction
artifacts. The coordinator reads body material to define the extraction and
checks reading scope, but does not write or select the candidate responses.

Baseline: the current abstract-decisions.md, writing-protocols.md and
argument-transfer.md, snapshotted before this turn's edits. Candidate: identical
abstract and section guidance, with only the argument-transfer guide replaced
by its new version. The new portion uses DPO and PagedAttention Methods to
explain how to turn an operative relationship into concise prose. No test paper
is used to write the new guide. The candidate snapshot is frozen before reading
the two test papers' body passages.

Four fresh writer contexts, without parent history: two replicates per condition.
Each reads the same two bodies and produces an abstract (150-200 words), a Results
paragraph (120-180 words) and brief working notes per case. Notes may be used in
both conditions; they are not scored. Writers must not browse, read author
abstracts or other agents' outputs, or deliberately reproduce remembered author
wording. Pretraining recall cannot be ruled out by these instructions.

Save exactly one untouched generation per context. No response edits, selection,
padding or retries. Failures and budget violations stay in the record.
Word counts use the repository abstract checker's word-token rule, including
hyphenated/apostrophe words as one token; this is a mechanical budget check,
not a language-quality score.

Two fresh reviewers get the same bodies and eight anonymous A/B pairs (two
papers, two replicates, two units). Their display order is reversed, and they
receive no condition labels, guides, notes, prior conclusions or expected
preference. They assess fidelity, contribution, argument, selection and language,
with a located preference or tie. Treat one poor or strong sentence as local
evidence, not a general win. A separate fresh source auditor can inspect the
designated body pages/tables to check claims missed by prose reviewers.

Unblind only after both reviewers save responses. Report repeated samples and
disagreements separately; this is a small same-family model pilot, not a human
study, no-leakage guarantee, representative benchmark, full-workflow evaluation
or evidence of conference acceptance. These papers become development data
after this round. Full third-party body text/PDFs remain local; repository
reports may include original generated prose, receipts and source locations.
