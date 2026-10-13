# Embodied Writing Round 4

Date: 2026-09-18. Corrected classification on 2026-10-10: this was a local
development exercise with self-audit, not an independent blind test.

## Change under test

The abstract workflow now requires an evidence preflight before prose. It freezes
the metric, unit, evaluation setting, baseline training protocol, evidence verb,
allowed claim strength, design rationale, and word budget. It also permits either
method-first or gap-first organization and prevents design intent from becoming
an isolated causal claim.

## Development procedure

The writer packet contained three embodied-robot fact summaries for Diffusion
Policy, OpenVLA-OFT, and pi0. It did not contain published wording, source links,
candidate labels, or round-1 judge decisions. However, the coordinating agent had
seen the prior abstracts and findings and wrote both candidates and the scorecard
in the same conversation. It later edited the candidates to satisfy the word
budget. Those conditions do not meet the separate-context, untouched-output
protocol. The previous claim of blind validation was unsupported.

## Result

The edited candidates measured 157, 153, and 152 words respectively and later
passed lexical contract checks. These checks do not establish semantic fidelity
or successful argument transfer. The OFT candidate explicitly separates pi0/RDT-1B default
fine-tuning from Diffusion Policy/ACT training from scratch, which was the main
source-fidelity failure found after round 1. The pi0 candidate avoids universal
reliability/generalization claims, and the Diffusion Policy candidate separates
planned dissemination from evaluated results.

The complete packet and edited development candidates are in the local evaluation
directory `/Users/liyufeng/Desktop/research/super_writer_real_abstract_eval_20260918/`.
The local scorecard records a retrospective round-1 comparison, not a randomized
human or model preference result. No independent writing-quality gain is
established by this exercise. Raw history is not repaired or relabeled as a fresh
generation trial.

## Verification

- Abstract calibration tests: 4 passed.
- CLI smoke suite: 11 passed.
- Full Python 3.14 suite after the rule update: 164 tests, 163 passed and one
  PowerShell-unavailable skip.
- Skill frontmatter validation: passed with a Python environment containing
  PyYAML.
- `git diff --check`: passed.
