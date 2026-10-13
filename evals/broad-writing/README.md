# Broad writing revision archive

Twelve real papers, six domains, three samples per paper and three units produce
108 initial and 216 final passages: 108 equal-pass baseline/candidate pairs.
Two reversed-order anonymous reviewers give candidate 12, baseline 20 and tie
184 votes. **No overall writing improvement is demonstrated.** All 108 pairs,
including losses and disagreements, are retained.

[Complete report](../../docs/broad-writing-evaluation.md) |
[Side-by-side HTML](comparison-complete.html) |
[Primary summary](summary.json) |
[Separate text-only audit summary](supplemental/summary.json)

## What is archived

| Artifact | Purpose |
| --- | --- |
| `PROTOCOL.md`, `request.json`, `frozen_hashes.json` | Frozen primary design, budgets and guide identities |
| `domains.json`, `domains.initial.json`, `replacements.json`, `exclusions/P02.json` | Effective registry and the pre-generation ScrewMimic-to-P13 availability replacement |
| `source_receipts.json`, `source_hashes.json`, `metadata/`, `sources/*.extract.*` | Exact source versions, hashes, warnings and original extraction recipes |
| `anchors/`, `baseline/`, `candidate/` | Original editorial grounding anchors and frozen guidance |
| `raw/` | 84 untouched initial/editor/reviewer/reader/primary-audit response files |
| `supplemental/` | Separately registered protocol, six untouched text-only audit responses, hashes and comparisons |
| `private_mapping.json`, `private_reader_mapping.json` | Anonymous assignments; private during judging, decoded for public inspection afterward |
| `summary.json`, `pair_results.json`, `decoded_votes.json`, `decoded_audits.json` | Primary descriptive outcomes, complete reasons and fidelity/recovery judgments |
| `word_counts.json`, `reader_diagnostics.json`, `assessment_word_counts.json` | Writer budgets and retained assessment deviations |
| `execution.started.json`, `execution.completed.json`, `execution.supplemental.json` | Primary and supplementary context completion and operational reports |
| `prompts.portable.json` | Exact messages except absolute workspace paths become `{WORKSPACE}`; the original superseded P02 prompt plan is also preserved |
| `comparison-complete.html`, `browser_verification.complete.json` | Current comparison with both audit rounds and desktop/mobile checks |
| `comparison.html`, `browser_verification.json` | Earlier primary-only display and browser-verification snapshot |
| `MANIFEST.json`, `archive_hashes.json`, `all_raw_hashes.json` | Explicit distribution boundary and byte-identity receipts |
| `verification.final.json` | Coordinator-recorded terminal checks, scoped to artifacts/software, not writing superiority or a release |

Primary auditors D2/D4/D6 reported accidental excluded-PDF text visibility.
The supplementary round restricts all six fresh auditors' provided inputs to
locked bodies and anchors. Its 216 judgments **do not replace or pool with**
primary labels. Same-family models, purposive sampling, cross-replicate context,
reader/reviewer budget deviations and the primary understanding ceiling are
disclosed in the report. A pass is not an entailment or human-quality certificate.

## Verification and reconstruction

From the repository root, with Python 3.10+:

```bash
python3 evals/broad-writing/check_archive.py
python3 -m unittest discover -s evals/broad-writing -p 'test_*.py' -v
```

The first checks public byte receipts only. The thirteen fixture tests exercise
infrastructure with temporary synthetic data, not fresh scientific generations.
Both commands work without third-party source PDFs or a model/API.

To reconstruct a scientific rerun, use a **new workspace**. Retrieve each exact
PDF/version from its receipt, reproduce the `pdftotext -raw` command with matching
Poppler, then run the saved extraction recipe and check `source_hashes.json`.
Body text, PDFs, full extractions, rendered pages and source-containing packets
are intentionally not redistributed. Current helpers do not supply a model
runner; dispatch the portable prompts explicitly, respecting their frozen
budgets and fresh-context boundaries. Source updates or extraction-version
changes can invalidate pins. Generations and judgments are not deterministic.

`experiment.py`, `analyze.py`, `verify_artifacts.py`, `compare_audits.py`,
`render_comparison.py` and `archive.py` refuse to overwrite saved artifacts.
Do not run phase commands directly into this completed archive. Display changes
can use a new renderer `--output` filename; browser checks accept an HTML filename
and a distinct JSON receipt filename and require Playwright/Chromium already
available. No dependency installation or paid model call is automatic.

Generated passages describe published work for evaluation; they are not endorsed
author abstracts or new research results. Editorial judgments/anchors are
original model outputs, not publisher text. The repository license does not
relicense linked papers. A local 21-token overlap diagnostic found no long exact
match in prose or notes but does not certify originality. This round changes no
runtime guide, skill version, installed skill, commit or remote publication.
