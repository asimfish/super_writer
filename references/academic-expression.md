# Academic Expression: Direct, Precise, Faithful

Use for English or Chinese academic editing, including abstracts and responses.
This is not a casual-writing style transplant or an AI-detector evasion method.
The author's evidence and requested edit scope take priority over stylistic taste.
Method attribution and adaptation boundaries are in [UPSTREAM.md](../UPSTREAM.md).

## Select the Contract

Separate **mode**, **scope**, and **intensity**. "Less defensive" is an intensity
request, not permission to restructure the paper or strengthen the evidence.

| Contract | Allowed output |
|---|---|
| Diagnose only | Up to five located findings, their consequence, and a proposed action; no unsolicited replacement draft |
| In-place edit | Preserve sentence order, all information and technical notation; change wording locally |
| Bounded rewrite | Rewrite only the named unit; remove empty sentences only if no factual or logical function is lost |
| Structural revision | Reorder or rebuild only within the explicitly approved scope; record an information-transfer map |

Default to a bounded edit of the supplied passage, in its existing academic
register. Produce one recommended version, not a menu of increasingly assertive
alternatives. For an audit-only request, do not rewrite.

## Pass 1: Preserve Meaning

Before editing, identify protected relationships, not just a bag of tokens:

- Number, entity, unit, denominator, comparison direction and aggregation level.
- Negation, quantifiers, conditions, population, time period and evaluation split.
- Observed association versus intervention, conjecture versus proof, and the
  source of uncertainty. "May", "under assumption A" and confidence intervals
  can carry indispensable information.
- Technical definitions, metric names, equations, citekeys, quotations, commands
  and API identifiers. Repetition of a defined term is often correct.
- Completed versus proposed work, responsibility, and whether evidence is
  supplied, absent, inaccessible or contradictory.

Check input-to-output for omissions and output-to-input for unsupported additions.
The same numbers attached to different models are a failed rewrite. Do not
invent an implementation, mechanism or concrete example to make an abstract
statement sound more natural. Keep a source gap visible or narrow a claim with
the author's agreement; never silently erase an important unsupported claim.

## Pass 2: Remove Empty Framing

Classify a suspect phrase before changing it: redundant preamble, useful
contrast, necessary scope, methodological limit, evidential qualification, or
genuine correction/apology. Remove only framing that adds no information.

- Lead with the supported finding or argument. Make scope precise rather than
  adding a chain of "may perhaps potentially" qualifiers.
- A limitation may be stated once where it belongs, but must also remain beside
  a claim when readers would otherwise misunderstand that claim. Never move a
  necessary qualification out of an abstract just to sound confident.
- Preserve required Limitations, ethics and disclosure sections. Never ban the
  word "limitation" or optimize simulated reviewer scores by concealing gaps.
- Keep useful contrast and statistically justified "significant". There is no
  universal banned-word list, synonym quota, sentence-length target or rule that
  all paragraphs need different syntax.
- In rebuttals, answer the concern and point to evidence. Acknowledge real
  errors plainly; do not add ritual apologies or invent completed revisions.
- Chinese output should remain natural scholarly Chinese. Preserve technical
  terms; remove empty progress rhetoric only when its factual content survives.

Stop after a faithful first pass and, if useful, one light residual pass. Roll
back a candidate that loses evidence or changes scope; do not keep rewriting to
force a heuristic score down. Retain the last evidence-valid version.

## Vocabulary Support

Use [writing-library.md](writing-library.md) for bounded offline lookup. Query the
technical concept and rhetorical purpose separately. A sentence card's example
is a scaffold, not a claim to paste or a source supporting the paper's results.
For AI claim verbs, learning regimes or measurement units, use the separate
[AI writing specification](ai-writing-spec.md). Read its meaning, conditions,
exceptions and evidence requirements together; do not replace words using only
a dictionary label. Its synthetic contrasts are not manuscript evidence.

For ambiguous referents, noun groups or research-artifact procedures, use
[context-sensitive clarity](clarity-context.md). Select by text function; keep
academic voice/tense choices, literal strings and supplied action dependencies.
This is a selective method adaptation, not a controlled-language compliance pass.

## Reporting

For a short edit, deliver the revised passage and only a material fidelity note
when needed. For a full configured style stage, keep `humanize_matrix.md` and
its legacy columns for compatibility. Record "no change" when appropriate;
do not invent high-severity defects. D1-D5 are local heuristics, advisory by
default, and cannot establish authorship, detector risk or scholarly quality.

See [worked boundary cases](../examples/academic-style/README.md). These are
authored demonstrations, not independent model evaluations.
