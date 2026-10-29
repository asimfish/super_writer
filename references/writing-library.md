# Offline Terms and Sentence Patterns

`writing-library.json` is a reproducible, curated subset of Super Library's
CC0 original records. It retains source IDs, qualifications and provenance.
Coverage includes general research writing, world models, reinforcement
learning, embodied AI, robot learning and vision-language-action. It is not
an exhaustive terminology dictionary or an evidence database.

The selection contains 130 cards: 78 sentence patterns and 52 definitions,
terms, usage notes or anti-patterns. All 78 reviewed upstream sentence-pattern
cards are included; not all 274 upstream entries are imported. For section
structures and tables, use [writing protocols](writing-protocols.md) separately.

The original library remains the lookup default. The separate, locally authored
[AI writing specification](ai-writing-spec.md) contains 19 rules, 15 claim-usage entries
and 34 technical terms, plus eight local functional sentence patterns, via explicit
`--catalog ai-spec`, with topic/level facets. The eight patterns extend the 78
upstream wording cards with preceding/following functions and non-transfer bounds;
they do not change the pinned imported records or constitute eight venue templates.
These are conditional
editorial records, not more imported cards or a universal vocabulary whitelist.
They do not change the 130-card count, imported data or reproduction pins.

## Sentence Progression, Not Syntactic Variety

Test the sequence by reading adjacent sentences: what question or unresolved
object does the first leave, and what does the next add? A bottleneck can motivate
an operation; that operation can explain a capability; a comparison can test it;
a boundary can revise the resulting interpretation. These are possible relations,
not a compulsory abstract outline. Independent co-contributions may be parallel
when their relationship and shared purpose are explicit.

If result sentences can be freely permuted with no change in the argument,
inspect whether they are a table inventory. Merge measurements answering the
same question, then give the next sentence a different job. A useful next job
might be testing an alternative explanation or showing transfer, rather than
announcing another task score. Do not merely vary subjects, insert "moreover",
or add "therefore": a connective cannot supply missing scientific support.
The permutation test is an editorial probe, not a mechanical pass/fail rule.

Retrieve conventional wording only after choosing that relationship. The local
`sentence_pattern` cards record a reader question, predecessor, successor and
non-transfer boundary, alongside evidence requirements and original positive and
negative examples. Existing upstream phrase cards remain useful for wording.
Choose a small applicable subset; do not concatenate one sentence per card or
replace precise, familiar technical terms to make the prose look more varied.
Related work needs an axis of comparison; Results needs a question and finding;
neither should inherit an abstract's order just because it uses the same wording.

## Query and Apply

Resolve commands against the skill directory, keeping the paper project as cwd:

```bash
python scripts/writing_lookup.py "distribution shift" --domain reinforcement_learning --kind definition --limit 3
python scripts/writing_lookup.py "result boundary" --section experiments --limit 3
python scripts/writing_lookup.py "显著提升" --kind usage_note --limit 3
python scripts/writing_lookup.py --id general.sentence-pattern.rebuttal-no-evidence.001 --format json
```

1. Choose the section, purpose and scientific domain. Retrieve 3-8 relevant
   cards, not the whole JSON file. Use `--max-chars` to bound context; complete
   cards are retained so warnings are never truncated away.
2. Separate a technical query (for example, offline distribution shift) from a
   rhetorical query (a qualified results comparison). Lexical matching and
   Chinese aliases aid discovery; this is not semantic search or an LLM call.
3. Read each card's meaning, guidance and avoid fields before its examples.
   Resolve ambiguous terms against the manuscript's operational definition.
4. Fill every placeholder only from supplied evidence. Preserve metric direction,
   units, variability, denominators, comparator fairness and untested conditions.
5. Use source links for discovery. Read the actual source to establish support
   before adding a citation; corpus review status is not claim verification.
6. Stop after enough useful cards. A missing hit does not invalidate a term.

No network, model SDK, credentials or companion installation is needed for
lookup. Only the explicitly invoked source-repository maintenance tool
`tools/import_writing_library.py --write` downloads pinned public corpus inputs.
It verifies SHA-256 and never fetches full papers or runs upstream code.

The original corpus records retain [CC0](../DATA_LICENSE). Linked papers and
their metadata do not acquire a new license. See [notices](../THIRD_PARTY_NOTICES.md).
