# Blind Review Round 4

The reusable protocol is documented in
[references/blind-evaluation.md](../references/blind-evaluation.md). A local
review page for the three embodied-robot comparisons is available at:

`/Users/liyufeng/Desktop/research/super_writer_real_abstract_eval_20260914/BLIND_REVIEW.html`

The page shows frozen facts and randomized candidate labels, collects five
dimension scores, a pairwise preference, and a reason, then downloads a JSON
review. The A/B mapping is stored separately in `BLIND_REVIEW_MAPPING.json` and
must remain hidden until review exports are complete.

The page displays completion progress and blocks export until every score,
preference, reason, and reviewer ID is present. The command-line aggregator still
rechecks the export because browser-side checks are usability aids, not trust
boundaries.

After collection, validate and aggregate one or more exports with:

```bash
python3 tools/aggregate_blind_review.py \
  --mapping /path/to/BLIND_REVIEW_MAPPING.json \
  --review /path/to/reviewer-1.json \
  --review /path/to/reviewer-2.json \
  --output blind-review-summary.json
```

The command rejects incomplete scores, duplicate or missing reviewer IDs,
invalid values, missing preferences, and missing reasons before unblinding. It
reports dimension means by version, per-paper score deltas, and pairwise
preferences separately. With multiple reviewers it also reports exact pairwise
preference agreement; this is descriptive agreement, not proof of reviewer
reliability or a substitute for adjudication.

Render the accepted aggregate as a cautious report with:

```bash
python3 tools/render_blind_summary.py blind-review-summary.json \
  --output blind-review-summary.html
```

The report refuses to imply an overall win when there are fewer than two
reviewers, mixed preferences, or unresolved ties.

This page is a review instrument, not a completed independent evaluation. No
human or external reviewer has submitted scores yet. Therefore it can improve
the measurement procedure but cannot by itself establish that the new version
is better.
