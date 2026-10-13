# Argument-transfer pilot artifacts

Original synthetic development material, collected on 2026-10-10. Read the
[evaluation report](../../docs/argument-transfer-evaluation.md) before interpreting
scores. This is a six-pair, same-family model pilot, not a human evaluation or a
test of unseen real papers. One candidate preference and eleven ties do not
establish general improvement.

## Files

| File | Role |
| --- | --- |
| `PROTOCOL.md` | Protocol frozen before generation |
| `request.json` | Same author priorities, facts, budgets and schema for both writers |
| `baseline/abstract-decisions.md` | Baseline abstract guidance snapshot |
| `baseline/writing-protocols.md` | Baseline section guidance snapshot |
| `candidate-guide.md` | Additional guidance actually used by the candidate writer |
| `raw/writer_1.json` | Untouched baseline generation |
| `raw/writer_2.json` | Untouched candidate generation |
| `review_packet_1.json`, `review_packet_2.json` | Anonymous inputs, with reversed A/B order |
| `raw/judge_1.json`, `raw/judge_2.json` | Untouched judgments in the corresponding packet's labels |
| `private_mapping.json` | Post-review disclosed mapping: writer index 0 baseline, 1 candidate; arrays map A/B for reviewer 1 and reverse for reviewer 2 |
| `generation_hashes.json` | SHA-256 receipts for the request and untouched generations |
| `prepare_review.py` | Local packet-assembly script used before review; not a writing or scoring engine |
| `REVIEW-RUBRIC.md` | Review instructions, restated without machine-specific file paths |

`private_mapping.json` retains its original pre-review filename; it is disclosed
here for audit, not secret. The raw responses are copied byte-for-byte, with no
word padding, parsing repairs or post-review rewriting. The linked guidance
inside snapshots may reference their original repository-relative locations;
only the explicitly supplied guide text was part of each writer's instruction.

The source facts and generated passages are original project-owned synthetic
material under the repository's MIT license. Guide snapshots preserve existing
source-attribution boundaries. These cases are development data after this
evaluation and must not be presented as unseen in a later iteration.
