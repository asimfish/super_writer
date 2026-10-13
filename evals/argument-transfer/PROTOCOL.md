# Argument-transfer development pilot

Frozen before generation on 2026-10-10. Three original synthetic topics test
abstracts (130-180 words) and result passages (90-140 words). Each condition gets
the same request.json, abstract decisions and experimental prose guidance. The
candidate condition additionally gets the new argument-transfer guide. The
baseline references are snapshotted in baseline/ before repository edits.

Two separate writer agents have no inherited conversation context. Each writes
one sample for all three topics; untouched JSON responses go to raw/. No retries,
padding or edits to those responses are part of this evaluation. Word counts are
reported separately; a failure stays in the record.

Two fresh reviewer agents receive only request.json, anonymized paired passages
and the same review rubric, with opposite display order. They do not receive
generation prompts, condition labels, mapping, guide or expected preferences.

Primary question: can the reader recover the contribution and why the evidence
answers it, rather than only recall numbers and components? Reviews report
source fidelity, argument connection, evidence selection, and language, with
located reasons and a preference or tie for each unit. Fidelity failures take
precedence over a fluent presentation. Preserve disagreements.

This is a small same-family model pilot on synthetic development data. It is
neither an evaluation of unseen real papers nor independent human validation.
No overall superiority or stable improvement is inferred from six pairs.
