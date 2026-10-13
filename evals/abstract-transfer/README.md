# Abstract Transfer Evidence Archive

Six papers, two samples, twelve pairs and twenty-four final abstracts. This is
an abstract-only confirmation of the exact preceding operative-relation candidate,
not a new rule, author-original comparison, leaderboard or human study.

**Votes: candidate 10 / baseline 6 / tie 8. The frozen continuation gate fails.**
A06_s2 unanimously favors baseline. Two pairs favor candidate unanimously, one
ties unanimously, and eight disagree. Both sample strata and four paper strata
net favor candidate, but do not discard the counterexample or relax the gate.
The canonical writing guide is unchanged.

- [All pairs side by side](comparison.html)
- [Full report and failure analysis](../../docs/abstract-transfer-evaluation.md)
- [Frozen protocol](PROTOCOL.md), [summary](summary.json), [pair results](pair_results.json)
- [Untouched response hashes](all_raw_hashes.json), [copied-byte hashes](archive_hashes.json)
- [Source receipts](source_receipts.json), [execution and exposure](execution.json)
- [Portable prompts](prompts.portable.json), [publication boundary](MANIFEST.json)
- [Final software checks and infrastructure correction](verification_receipt.json)

All forty-eight source-audit labels mark fidelity pass, critical support supported
and reader support text-grounded equally in both versions. This is no fidelity
or reader-grounding improvement; the channels again reach a ceiling. See the
saved anonymous preferences for differences in argumentative organization.

## Contents and Integrity

Thirty-six original response files are preserved: six initial, twelve editor,
six preference, six reader and six source-auditor responses. Each writing response
contains two paper cases. Ninety-six files are copied byte-identically from the
local run; public derived receipts and this README are outside that copy count.
The local full-input check verifies 134 hash entries, including private source
inputs. Public source receipt declarations agree with the frozen source pins,
but public verification cannot inspect the intentionally omitted source bytes.

Source and guide identity are frozen before writing; all assessment responses
are collected before unblinding. Expected critical answers are not given to
writers or assessors. No retry, raw correction, padding, judge replacement or
case exclusion occurs. The 203-word A05 shared initial exceeds its ceiling by
three words; all final abstracts, other prose/note fields, assessment budgets
and literal witness checks pass. All exceptions remain in the archive.

Thirty-nine fresh same-family contexts inherit the model without overrides or
parent conversation forks. Source preparation uses three grouped contexts;
writing uses eighteen, assessment eighteen. They are not thirty-nine independent
human observations. Readers may see another replicate of a paper, and source
auditors see counterpart texts without supplied condition labels. Prompt limits
are not filesystem quarantine or proof of absent scientific recall.

## Sources and Publication Boundary

Cases are VoxPoser, SAM, DreamBooth, Toolformer, FlexGen and Neural ODE, with
registry and exact source choices in [papers.json](papers.json). DPO and MAE
are excluded before preparation because they are already developed exemplars.
SAM uses the explicitly allowed arXiv v1 after blocked official access, with
final-version equivalence unverified. Neural ODE's assigned official file lacks
cited appendices and has extraction defects. DreamBooth and Toolformer supplements
are not independently inspected. Incidental preparer/coordinator excluded-text
exposure, unrepaired equations/tables and other version limits remain disclosed.

The selected inputs contain 32 original byte spans totaling 206,896 bytes. PDF,
raw extraction, selected publisher body, complete metadata and extraction recipes
remain local; they are not redistributed or relicensed. Saved prose is generated
research reconstruction, not the authors' original abstracts or our new findings.

## Verification and Reruns

From the repository root, using the supported Python environment:

```bash
python3 evals/abstract-transfer/verify_abstract_artifacts.py evals/abstract-transfer
python3 -m unittest discover -s evals/abstract-transfer -p 'test_abstract_eval.py'
python3 -m unittest tests.test_abstract_transfer_archive
python3 evals/abstract-transfer/verify_public.py .
```

The helper suite uses synthetic temporary fixtures; it verifies logic, not fresh
model judgments. Original full-input verification is available only from the local
experiment workspace with its omitted inputs and `--local-inputs`. Do not claim
that public-only checking proves publisher-source fidelity.

Helpers invoke no model. A genuine rerun needs an explicit agent runner and
independently checked sources, new immutable output paths and version/hash receipts.
Portable prompts replace the old workspace string with `{WORKSPACE}`. Copied
historical helpers and guide snapshots retain original paths/relative references;
they are not a standalone installed skill. Do not execute phase writes in this
frozen archive or silently replace source revisions to make old hashes pass.

Playwright verifies all 36 displayed prose strings, every pair's layout, paper/sample
filters and details at 1440px/390px. Screenshots are inspected locally and not
included as publisher imagery. These are rendering checks, not human writing review.
No model weights, installed skill, imported pin, skill version, commit or push changes.
