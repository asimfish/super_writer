# Review instructions (path-independent record)

Each fresh reviewer reads only its anonymous review packet. It must not read
other outputs or files, browse, search, inspect parent context or infer version
identities. The packet contains the author's facts and priorities, word budgets
and six A/B pairs; it does not contain guides or an expected preference.

For each pair:

1. Assess source fidelity as pass, concern or fail, with a located reason.
2. Rate contribution clarity, argument connection (why this design or evidence
   answers the question), evidence selection (not merely quantity) and language
   quality on a 1-5 ordinal scale. A 1 means a serious deficiency, 3 adequate
   and coherent, and 5 clear specific reasoning with well-chosen evidence.
3. Prefer A, B or Tie with a decisive located reason. Ordering or length alone
   is insufficient. Allow defensible allocations and do not expect a particular
   preference. Fidelity defects take precedence over fluent phrasing. Do not
   reward generic caution, penalize every omission or demand every number.
4. Write one untouched JSON judgment covering all six pairs. Do not revise it
   after writing or change repository files.

The records use this schema:

```json
{
  "reviews": [{
    "case": "C1",
    "unit": "abstract",
    "fidelity": {
      "A": {"status": "pass", "reason": "located explanation"},
      "B": {"status": "pass", "reason": "located explanation"}
    },
    "ratings": {
      "A": {"contribution": 3, "argument": 3, "selection": 3, "language": 3},
      "B": {"contribution": 3, "argument": 3, "selection": 3, "language": 3}
    },
    "preferred": "Tie",
    "reason": "decisive located comparison"
  }]
}
```

This is a path-independent restatement, not a byte-for-byte prompt transcript.
