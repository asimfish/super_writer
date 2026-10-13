# Operative-relation evaluation archive

Two real papers, two initial samples each, three units and one revision per
condition: twelve paired units, twenty-four final passages. Votes are candidate
5 / baseline 5 / tie 14. **No overall gain and no runtime promotion.** Abstract
preferences are 4 / 0 / 4; Methods and Results retain unfavorable outcomes.

[Full report and limitations](../../docs/operative-relation-evaluation.md) |
[All pairs side by side](comparison.html) |
[All counts and violations](summary.json)

## Preserved artifacts

- `raw/`, `all_raw_hashes.json`: all 24 untouched writer, reviewer, reader and audit responses.
- `PROTOCOL.md`, `baseline/`, `candidate/`, `shared/`: pre-body protocol and guide snapshots; candidate changes only an appended compression hypothesis.
- `papers.json`, `source_receipts.json`, `source_hashes.json`, `source_assembly_verification.json`: identities, actual versions, source exposure, warnings and byte provenance.
- `anchors/`, `requests/`: original unit objectives fixed before generation and supplied equally, not gold author wording.
- `packets/`, `mapping.json`, `prompts.portable.json`: anonymous packets, revealed mappings and exact prompts with only workspace values replaced.
- `decoded_votes.json`, `decoded_audits.json`, `pair_results.json`: all preferences, disagreements and independent fidelity/support channels.
- `word_counts.json`, `assessment_budgets.json`, `witnesses.json`: complete diagnostics, including a 181-word baseline Results and a 20-word candidate reader witness.
- `*_hashes.json`, `execution.json`, `MANIFEST.json`: freezes, context counts and byte-identical copying receipts.
- `verification_receipt.json`: later local verification evidence; separate from the 75 unchanged copied artifacts.
- `relation_eval.py`, `test_relation_eval.py`, `render_relation.py`, `browser_relation.mjs`: preparation/analysis, temporary-fixture tests and rendering checks.

N1 is CoRL 2021 / PMLR 2022; N2 is an Annals of Statistics journal article using
an authorized author-hosted manuscript after blocked publisher access. N2's
exact revision and equivalence to the published version are unverified. Model
pretraining and related-family exposure are unknown/not excluded. All contexts
are same-family model contexts, not independent humans; input restrictions are
not filesystem isolation. Do not pool votes across rounds or units into a
general effectiveness, acceptance or training claim.

## Reproducible checks

From the repository root, with Python 3.10+:

```bash
python3 -m unittest discover -s evals/operative-relation -p 'test_*.py' -v
python3 -m unittest discover -s tests -p test_relation_archive.py -v
python3 evals/operative-relation/verify_relation_artifacts.py evals/operative-relation
```

These need no network or model and check infrastructure/archived bytes, not
semantic quality. `verify_sources.py` and full frozen-input analysis require the
omitted original local metadata and source bytes; the public checker explicitly
does not attest those omitted inputs. PDFs, complete extraction, selected
publication body, full metadata/boundary recipes and image renders are not
redistributed or relicensed. Public anonymous packets contain generated prose,
not publisher body evidence.

For a fresh behavioral run, use a new workspace, an explicit agent runner,
independently reviewed source packets and new byte receipts. Phase helpers do
not invoke a model and refuse to overwrite saved artifacts. The portable
messages alone cannot recreate withheld source bodies or guarantee the same
responses. Do not replace old sources with changed downloads while retaining
their old SHA-256, or reclassify these development cases as new held-out papers.

All raw deviations remain: one generation word overage, one witness overage,
six pair-level disagreements and the unfavorable Methods/Results preferences.
No extra revision, prose repair, quality retry or favorable label substitution
was used. Passing synthetic evaluator calibration does not prove this writer
learned excellent papers' style.
