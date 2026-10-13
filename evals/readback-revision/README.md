# Prose read-back revision artifacts

This archive compares equal-pass revisions of shared generated drafts, not an
edited candidate against an untouched baseline. See the
[evaluation report](../../docs/readback-revision-evaluation.md) and frozen
[protocol](PROTOCOL.md). Two papers, two initial-draft samples and two units give
eight pairs. Separate model contexts do not establish human independence or
absence from model pretraining.

## What is preserved

- `raw/initial_1.json` and `initial_2.json`: untouched shared draft generations.
- `raw/baseline_*.json` and `candidate_*.json`: one untouched revision per editor.
- `raw/judge_*.json`: two anonymous quality reviews with reversed display order.
- `raw/source_audit.json`: separately grounded source-fidelity findings.
- `baseline/` and `candidate/`: the exact guide snapshots supplied to writers.
  Only the candidate argument guide adds the prose read-back section. Both
  editors use the same abstract and section guides. Initial writers do not use
  either argument guide. Snapshot links are archival, not a standalone skill.
- `request.json`, `source_receipts.json`, `generation_hashes.json`: task, inputs,
  extraction boundaries and exact-byte provenance.
- `anonymous_pairs.json`: exact displayed prose without third-party body text;
  original complete local review-packet hashes are included.
- `private_mapping.json`: disclosed after reviews are saved, not provided to
  reviewers. Reviewer 2 sees reviewer 1's A/B order reversed.
- `word_counts.json`, `initial_word_counts.json`, `note_word_counts.json`: length
  checks, not evidence of writing quality or successful semantic review.
- `prompts.portable.json`: original task prompts with only the evaluation root
  replaced by `<EVAL_ROOT>`, accompanied by hashes of the original prompt files.

Original PDFs, extracted bodies, rendered pages, source-grounding notes and
complete review packets remain local. They are not covered by this repository's
license or redistributed as a corpus. Generated prose and judgments may have
errors; consult the located findings rather than treat a pass as an oracle.

## Reconstruct local inputs and packets

Download the official PDFs identified in `source_receipts.json` to
`sources/lee24y.pdf` and `sources/p056.pdf`. **Verify their SHA-256 values first**;
the extraction helper records values but does not enforce the archived pins.
With Poppler, run:

```bash
mkdir -p inputs
pdftotext -raw -f 3 -l 9 sources/lee24y.pdf sources/lee24y.body-candidate.txt
pdftotext -raw -f 2 -l 10 sources/p056.pdf sources/p056.body-candidate.txt
python3 prepare_inputs.py
python3 prepare_review.py
```

Compare the derived body hashes to the archived receipts before considering
the inputs equivalent. Poppler extraction can vary across versions. These
helpers reproduce task inputs and anonymous packets from archived prose, not
stochastic model generations or judgment outcomes. Do not publish reconstructed
publisher text. Conditions and samples within this pilot are clustered; do not
pool its judgments with earlier guide-only drafting experiments.
