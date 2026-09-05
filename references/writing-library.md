# Offline Terms and Sentence Patterns

`writing-library.json` is a reproducible, curated subset of Super Library's
CC0 original records. It retains source IDs, qualifications and provenance.
Coverage includes general research writing, world models, reinforcement
learning, embodied AI, robot learning and vision-language-action. It is not
an exhaustive terminology dictionary or an evidence database.

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
