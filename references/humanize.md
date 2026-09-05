# Humanize Stage

This file is the canonical stage playbook for the paper-spine orchestrator.

## Purpose

Improve natural academic expression while preserving evidence and meaning.
Start with [academic-expression.md](academic-expression.md). D1-D5 describe
local surface heuristics, not measured detector risk or authorship evidence.

## Important Disclaimers

- Do **not** promise that a manuscript will pass any specific AIGC detector.
- Do **not** output a fabricated "AI rate" or percentage.
- Platform references are risk mappings, not descriptions of internal algorithms.

## Optional Legacy Platform Notes

Only when a user explicitly asks about a named platform, consult the legacy notes:
- CNKI → `references/platform-cnki.md`
- Weipu → `references/platform-weipu.md`
- Unknown / general → `references/platform-general.md`

These map platform-level risk dimensions to the machine-checkable metrics
that `humanize_check.py` measures (D1–D5).

## Tier-Based Audit Coverage

| Tier | Required audit coverage | Other dimensions |
|------|----------|----------|
| `light` | D1, D4 | D2, D3, D5 |
| `medium` | D1, D2, D3, D4 | D5 |
| `heavy` | D1–D5 | (none) |
| `none` | (structural only) | D1–D5 |

## Required Output: humanize_matrix.md

| Row ID | Manuscript Unit | AI Pattern Found | Detection Dim | Severity | Applied Change | Expected Effect | Teaching Note |
|---|---|---|---|---|---|---|---|

## Verification

```bash
python scripts/humanize_check.py paper_rewriting_output --markdown --write
```

Produces `humanize_report.md` with local D1-D5 measurements. Matrix structure and
configured audit coverage remain required. Style measurements are advisory by
default; only explicit JSON `humanize_enforce_heuristics: true` opts into legacy
threshold blocking. Never change facts or terms to satisfy a frequency target.
It is valid to record no high-severity findings or to leave a passage unchanged.

## Three-Round Revision Loop

At most 3 scoped rounds. Fix actual fidelity/clarity defects and audit structure.
Inspect heuristic findings in context; do not force them to PASS by introducing
synonyms, unsupported detail, artificial sentence variation or hidden limitations.

## Target-Journal Style Conformity (optional deeper method)

Local style diagnostics (D1-D5) and matching the *target
journal's* voice is a separate axis. When the deep-read journal corpus and
`journal-style-analysis.md` (JS templates) are available, apply the CASPArS
context-sensitive calibration in `references/round2-journal-revision.md`
(R1 Recalibration → R2 Replacement → R3 Redevelopment). Learn rhetorical moves
and terminology usage, not target word frequencies or claim-strength quotas.
Build its Style Conformity Checklist. Record the analysis in
`restructuring_notes.md`. This complements, and does not replace, the humanize
metrics above.

## Humanize Threshold Overrides

Individual detection thresholds can be overridden via `paper_spine_config.json`
under the `humanize_thresholds` key.  This allows gradual calibration from real
platform back-tests without modifying the script source.

These thresholds control **local risk scanning** only — they do not represent
any vendor's internal algorithm and do not guarantee a platform pass.

Example:

```json
{
  "humanize_tier": "medium",
  "humanize_thresholds": {
    "sentence_length_cv_warning": 0.30,
    "max_connector_density": 7
  }
}
```

Invalid keys, non-numeric values, or negative values produce a warning in the
report and are ignored (the built-in default is used instead).

## Calibration

When real platform detection scores are available, read
`references/humanize-calibration.md` and record runs in
`humanize_calibration/platform_runs.md`. Do not change thresholds from a single
result.
