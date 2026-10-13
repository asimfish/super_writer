# ADR-002: Orthogonal Classification and Curated Expansion

## Status

Accepted for local development on 2026-10-12. Extends [ADR-001](adr-001-ai-writing-spec.md).
No release, independent quality improvement or automatic research loop is claimed.

## Problem

Record kind answers what an entry is, but not which reader problem it addresses
or whether it applies to a word, paragraph or whole manuscript. Expansion also
needs a trace from source observation to conditional guidance. More entries alone
are neither broader coverage nor evidence of better writing.

## Alternatives

| Option | Benefit | Tradeoff |
|---|---|---|
| A single tree of dictionary, rules, examples and terminology | Simple menu | Examples duplicate definitions; cross-domain and cross-level guidance has multiple owners |
| Three kinds plus independent topic and level facets | Reuses the canonical catalog and bounded lookup | Requires explicit tagging and reviewed source notes |
| New crawler, database and automatic admission engine | Could gather many candidates | Adds network, storage and semantic-review capabilities not justified here |

## Decision

Keep `writing_rule`, `claim_usage` and `technical_term`. A dictionary is a view
over the latter two, not a second database. Positive/negative examples and their
shared synthetic context remain attached to the same canonical record. A negative
example explains a changed scientific reading, not merely an unfashionable phrase.

Add `topics` for reader-problem categories and `levels` for the writing unit.
Existing domains, sections and intents are preserved; these are independent axes,
not a fixed drafting order. Multiple labels are permitted when genuinely useful.

Schema 2 requires the new facets and `source_notes`, covering exactly the entry's
`source_ids`. A note states a read location and an editorial observation, not a
claim that the source proves the recommendation. Source-free local synthesis is
allowed with empty IDs/notes and must not acquire invented external authority.
Schema 1 stays readable without new fields; facet queries on unsupported catalogs
fail explicitly. The default imported library and its pins remain unchanged.

Candidate observations stay in research notes until admission; the active catalog
contains only inspectable conditional entries. [The learning workflow](../../references/ai-spec-learning.md)
defines source scope, deduplication, counterexamples, exceptions and test separation.
It is an agent/manual process, not a scheduled crawler or model-weight training.

## Verification Boundaries

- Structural checks establish IDs, taxonomy membership, note/reference integrity,
  bounded retrieval, v1 compatibility and fail-closed unsupported filters.
- Synthetic boundary fixtures establish that the authored distinctions survive
  retrieval; they do not establish independent semantic correctness or model behavior.
- Browser checks derive counts and facet intersections from the source catalog.
  Desktop, tablet and mobile layouts must preserve complete records.
- Writing-quality evidence still needs a separately frozen, equal-budget unseen
  test. Papers read for this expansion become development references, not unseen tests.

No modification to frozen argument-transfer guides or failed promotion gates is
authorized by this structural decision. Source-only rendering tools add no runtime
network/model/credential capabilities to the skill.
