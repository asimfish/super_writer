# Evaluator control archive

Twelve original synthetic cases, 24 short passages, 24 preferences, 24 readings,
48 coarse and 48 fine judgments. The frozen admission gate passes; **this is
evaluator calibration, not improved writing or a real-paper benchmark**.

[Report](../../docs/evaluator-control-calibration.md) |
[All controls side by side](comparison.html) |
[Exact criteria/results](summary.json)

## Artifacts

- `cases.json`, `PROTOCOL.md`: final fictional source/variant/oracle fixture and prespecified protocol.
- `cases.initial.json`, `fixture_review.json`, `corrections.json`, `fixture_review.final.json`: initial independent review, pre-assessment corrections and different final review.
- `packets/`, `mapping.json`: anonymous source/reader/audit packets and their mapping, revealed after assessment.
- `raw/`, `all_raw_hashes.json`: ten unchanged model-response files and SHA-256 receipts.
- `decoded_votes.json`, `decoded_audits.json`, `summary.json`: all decisions, reasons, coarse/fine channels and every admission criterion.
- `budgets.json`, `witnesses.json`: complete assessment word and literal-witness diagnostics.
- `frozen_hashes.json`, `reader_hashes.json`, `audit_input_hashes.json`: original input and source-free-reader byte pins.
- `execution.json`, `MANIFEST.json`, `archive_hashes.json`: completion, scope and byte-identical public-copy receipts.
- `prompts.portable.json`: exact messages with local workspace string values replaced by `{WORKSPACE}` only.
- `candidate_hypothesis.md`, `next-writing-protocol.proposed.md`, `hypothesis_hashes.json`: separately frozen next-step proposal, not a tested or installed writing guide.
- `control_eval.py`, `test_control_eval.py`, `render_controls.py`, `browser_controls.mjs`: infrastructure, temporary-fixture tests and display checks.

## Checks and rerunning

From the repository root:

```bash
python3 -m unittest discover -s evals/evaluator-controls -p 'test_*.py' -v
python3 -m unittest discover -s tests -p test_evaluator_controls.py -v
```

These tests need Python 3.10+ and no model, network or third-party publication.
They check infrastructure and integrity, not human semantic ratings. Scientific
claims in the supplied premises are explicitly fictional. Original oracles are
editorial expectations, not automatically established true by the tests.

For a new behavioral rerun, create a new workspace and reproduce the anonymous
packets using `control_eval.py prepare`, dispatch the portable initial messages,
then prepare/dispatch audits and analyze only after all responses are saved.
Do not execute phase commands into this completed archive: writes refuse to
overwrite. An explicit agent runner is required; no hidden API or model invocation
exists in these helpers. Preserve the final independently reviewed fixture, input
pins, reason budgets and raw deviations. Model judgments are nondeterministic.

The source fixture and prose are original synthetic material. No publisher text,
private paper or third-party skill is imported. Assessor inputs withhold oracles
and counterpart texts as declared, but do not cryptographically isolate the
filesystem or erase model recall. Do not pool judgments into independent trials,
treat full reader recovery as prose truth, or publish a writing-gain claim from
passing these deliberately constructed controls.
