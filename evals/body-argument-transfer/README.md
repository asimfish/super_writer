# Real-body argument-transfer artifacts

Two CoRL 2024 papers (PMLR publication in 2025), two fresh writer contexts per
condition, an abstract and Results passage per paper: sixteen raw passages.
Author abstracts, introductions and conclusion summaries are not writer inputs.
The sources are unexposed to this repository's documented development before
this round, not guaranteed unseen by the underlying model.
Read the [evaluation report](../../docs/body-argument-transfer-evaluation.md)
for observed preferences, disagreements and residual interpretation risks.

## Artifact boundary

The local run is stored in `super_writer_body_eval_20261010`. Repository copies
contain original generated prose, judgment records, guide snapshots and source
receipts. Third-party PDFs, body text, rendered pages and full source-text review
packets are **not** redistributed or relicensed. Source authors retain their
rights. Reports and project-authored artifacts are covered by the repository
license; links are not imports.

| Artifact | Purpose |
| --- | --- |
| `PROTOCOL.md` | Frozen design and disclosed limits |
| `request.json` | Shared task, budgets and output schema |
| `baseline/` | Three guidance snapshots used by both baseline replicates |
| `candidate/argument-transfer.md` | Replacement guide used by both candidate replicates |
| `raw/baseline_1.json`, `raw/baseline_2.json` | Untouched baseline generations, including unscored working notes |
| `raw/candidate_1.json`, `raw/candidate_2.json` | Untouched candidate generations, including unscored working notes |
| `raw/judge_1.json`, `raw/judge_2.json` | Untouched anonymous judgments |
| `raw/source_audit.json` | Separate source-fidelity audit, using reviewer 1's labels |
| `anonymous_pairs.json` | Pairs derived from the original packets, excluding third-party source text |
| `private_mapping.json` | Mapping disclosed only after judgments; reviewer 2's order is reversed |
| `source_receipts.json` | Official source URLs, source PDF and extracted-body hashes |
| `generation_hashes.json` | Guide, request, body and generation hashes |
| `word_counts.json` | Raw budget checks, not prose scores |
| `prepare_inputs.py`, `prepare_review.py` | Local extraction/packet-assembly code; neither generates nor scores prose |
| `prompts.portable.json` | Prompt records with machine-specific root paths replaced; not byte-identical originals |

Snapshots are experimental inputs, not additional installed playbooks. Their
relative links identify original repository resources; the writer prompts allow
only the explicitly supplied files, not following those links. Current skill
guidance may change after evaluation; use the snapshot to identify the tested
condition.

## Source reproduction

The official PDFs are linked and pinned in `source_receipts.json`. In a local
evaluation directory, obtain those exact bytes into `sources/wang25a.pdf` and
`sources/hejna25a.pdf`, verify their SHA-256 hashes, and extract physical pages
2-9 with `pdftotext -layout` into `sources/<paper>.body-candidate.txt`. Then run
`prepare_inputs.py` there and compare the input hashes. Its declared boundaries
exclude the abstract and conclusion summary while preserving limitations.

`prepare_review.py` reads the four untouched generations, uses fixed-seed label
permutations, excludes working notes, and reverses A/B order for reviewer 2.
It writes local review packets containing the reproduced body passages; these
are deliberately outside the redistributed artifact set. Mechanical reproduction
does not guarantee identical model generations or human agreement.

These cases become development data after this round. Do not present them as
unseen in a later iteration or pool their judgments with earlier synthetic tests.
