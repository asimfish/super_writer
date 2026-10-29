# AI Research Writing Specification

Use when AI research prose needs a precise claim verb, technical term, reporting
unit or explanation of a system's operation. This is an original local editorial
specification, not ASD-STE100, an official conference standard or a word whitelist.
Version 0.5 contains 19 writing rules, 15 claim-usage entries, 34 technical
entries and eight functional sentence patterns. Canonical records are in
[ai-writing-spec.json](ai-writing-spec.json).
The existing 130 imported language cards and their pins remain separate.

## Classification Model

The four kinds answer **what the entry is**. Nine topics answer **which reader
problem it addresses**, and five levels answer **where the decision operates**.
Domains, manuscript sections and local intents remain independent filters.

| Kind | Responsibility | Not its responsibility |
|---|---|---|
| `writing_rule` | Truth-preserving constraints or conditional organization decisions | A universal paragraph formula |
| `claim_usage` | Meaning and evidential strength of a word in context | A global approved/banned vocabulary |
| `technical_term` | Operational meaning, boundaries and confusable concepts | Authority over a manuscript's explicit definition |
| `sentence_pattern` | Conventional wording with a reader question, preceding/following functions and evidence boundaries | A sentence to paste without planning the argument |

The dictionary is a view over claim uses and technical terms, not a duplicate
database. Positive/negative examples belong to each entry: same synthetic facts,
different readings, an explained error and a legitimate exception. They are not
an independent pool of sentence templates to paste into papers.

Topics: `argument_structure`, `claim_strength`, `learning_regimes`,
`evaluation_protocol`, `statistics`, `embodied_control`, `systems_measurement`,
`citation_support`, `grounding_faithfulness`. Levels: `word`, `sentence`, `paragraph`, `section`, `document`.
Multi-label selection is allowed; labels do not prescribe a drafting sequence.
The seven domains include `multimodal`, currently supported by vision-language
cases, not a claim of full audio/video coverage.

Schema 2 adds these facets and per-source read locations/observations. The CLI
continues to read schema 1; facet filters unsupported by a catalog fail explicitly.
The source note is inspectable provenance, not proof that its editorial advice
works. See the [classification decision](../docs/designs/adr-002-classification-and-curation.md).

## Part 1: Writing Decisions

Rules have stable IDs, an owning playbook, conditions, evidence requirements,
exceptions and original synthetic positive/negative examples. They consolidate
existing guidance; a new catalog does not establish a writing-quality gain.

| ID suffix | Decision | Local status |
|---|---|---|
| `evidence` | Preserve quantity-entity-condition relationships | Invariant within factual edits |
| `evidence-role` | Keep exemplar style separate from manuscript evidence | Invariant |
| `scope` | Keep conditions that change a claim's interpretation | Invariant |
| `operation` | Explain the operation connecting components when names are insufficient | Editorial choice |
| `definition` | Make objects and symbols recoverable | Editorial choice |
| `contrast` | Explain what the comparator distinguishes | Editorial choice |
| `quantities` | Preserve measurement and aggregation units | Invariant |
| `uncertainty` | Keep consequential uncertainty and its definition | Invariant |
| `co-contributions` | Retain confirmed, author-prioritized promises | Invariant within the agreed scope |
| `term-consistency` | Use a stable term for a stable defined object | Editorial choice |
| `qualification` | Remove empty framing, not scientific qualifications | Editorial choice |
| `readback` | Read the actual prose before consulting its plan | Semantic self-review |
| `paragraph-function` | Organize around a local reader question | Editorial choice, not a move quota |
| `result-answer` | Connect results to the question the design can answer | Editorial choice, not invented causality |
| `citation-support` | Check support for each substantive attached claim | Invariant, not a citation quota |
| `evaluation-target` | Name the evaluated construct, reference and unit | Editorial choice, not metric interchangeability |
| `evidence-modality` | Distinguish unsupported, contradicted and unassessed | Editorial choice, conditional on reference coverage |
| `failure-localization` | Separate planning, feasibility and execution | Editorial choice, not causal diagnosis from score gaps |
| `procedure-order` | Preserve preconditions, action order and targets in research-artifact instructions | Invariant within executable instructions, not a grammar rule for all Methods |

An invariant constrains truth-preserving edits, not all possible manuscript
outlines. Editorial entries apply when their reader problem exists. Do not force
every paragraph through the same move sequence. Missing evidence prompts a scoped
question or a narrower claim, not an invented explanation.

## Part 2: Conditional Dictionary

Every dictionary entry identifies its local meaning and part of speech, the
evidence needed for its use, and cases where a tempting substitution changes the
claim. None is globally "approved" or "banned".

- Claim words: `evaluate`, `demonstrate`, `prove`, `significant`, `robust`, `efficient`,
  `suggest`, `enable`, `state-of-the-art`, `scalable`, `novel`, `causal`,
  `grounded`, `faithful`, `hallucination-free`.
- Learning regimes: `zero-shot`, `few-shot`, `fine-tuning`, `pretraining`,
  `inference`, `test-time adaptation`.
- Evaluation boundaries: `out-of-distribution`, `generalization`, `held-out`,
  `data leakage`.
- Embodied/RL reporting units: `success rate`, `demonstration`, `trajectory`, `episode`.
- Systems and uncertainty: `latency`, `throughput`, `end-to-end`, `uncertainty`.
- Further learning distinctions: `in-context learning`, `retrieval-augmented
  generation`, `offline reinforcement learning`, `imitation learning`,
  `preference optimization`.
- Control semantics: `action chunking`, `open-loop control`, `closed-loop control`.
- Support metrics: `factual precision`, `citation recall`, `citation precision`.
- Visual targets: `object hallucination`, `visual grounding`.
- Sequential embodiment: `robotic affordance`, `task-chain success`, `long-horizon`.

The manuscript's explicit operational definition takes precedence over an
oversimplified generic gloss. For example, end-to-end learning and end-to-end
timing are distinct senses; a frozen base model can still undergo adapter
fine-tuning; unlabeled test-time adaptation still uses target information.
An unfamiliar term is not invalid because it is absent from this initial set.

## Query and Apply

Resolve commands against the skill directory, keeping the paper project as cwd:

```bash
python scripts/writing_lookup.py --catalog ai-spec --id ai.rule.operation
python scripts/writing_lookup.py --catalog ai-spec "零样本" --kind technical_term --limit 1
python scripts/writing_lookup.py --catalog ai-spec --id ai.usage.significant --format json
python scripts/writing_lookup.py --catalog ai-spec "动作分块" --topic embodied_control --level word --kind technical_term --limit 1
python scripts/writing_lookup.py --catalog ai-spec --id ai.rule.result-answer --level paragraph
python scripts/writing_lookup.py --catalog ai-spec "视觉定位" --domain multimodal --topic grounding_faithfulness --level word --kind technical_term --limit 1
python scripts/writing_lookup.py --catalog ai-spec --id ai.term.task-chain-success --format json
python scripts/writing_lookup.py --catalog ai-spec "复现步骤" --topic evaluation_protocol --level sentence --kind writing_rule --limit 1
python scripts/writing_lookup.py --catalog ai-spec "数字堆积" --kind sentence_pattern --section abstract --limit 1
python scripts/writing_lookup.py --catalog ai-spec --id ai.pattern.operation-effect
python scripts/writing_lookup.py --id general.usage-note.significant.001 --format json
```

The last command still queries the original library. Catalog selection is
explicit: unknown catalogs, cross-catalog IDs and unknown filters fail rather
than silently falling back. Queries remain bounded to 256 characters. Complete
entries, including conditions, examples, exceptions and source context, must fit
the output budget; otherwise the command fails with no partial prose or JSON.
`--format ids` returns identifiers only, not sufficient guidance for application.

1. Select a relevant rule, dictionary sense or functional pattern, not all 76 records.
2. Compare its conditions and evidence needs with this paper's actual materials.
3. Use its owning playbook and existing rationale row to plan the text action.
4. Write from author evidence. Synthetic examples are contrasts, not paste-ready
   claims or actual experiments; numerical examples must not enter the manuscript.
5. Read back the final relation and scope, then run applicable existing guards.

The CLI validates the catalog structure and performs offline retrieval. It does
not inspect manuscripts, judge causality or enforce semantic rules automatically.
It makes no network/model calls, reads no credentials and writes no files.

## Continuous Expansion

Use the [curated learning cycle](ai-spec-learning.md): concrete gap, primary-source
reading, located observation, bounded local inference, deduplication, original
contrast pair, legitimate exception, structural checks, and separate quality tests.
Candidates stay outside the active catalog until reviewed. This is a declared
agent/manual workflow, not an automatic crawler or research schedule.

The [October 13 research record](../docs/research/ai-spec-expansion-2026-10-13.md)
lists seven newly read primary sources, scope limits, 14 admitted entries and
deferred gaps; the [previous round](../docs/research/ai-spec-expansion-2026-10-12.md)
remains historical evidence. The [six earlier cases](../examples/ai-writing-spec/README.md)
and [five new cases with Results paragraphs](../examples/ai-writing-spec/grounding-and-horizon.md)
show why these boundaries matter. None is an unseen-paper or measured-improvement claim.

The subsequent [MARMOT integration record](../docs/research/marmot-ste-integration-2026-10-13.md)
adds one rule and amends `definition`, with no new schema or runtime. Its source
is third-party design context, not an authoritative STE standard or another
primary paper. Use [context-sensitive clarity](clarity-context.md) only for
relevant ambiguity or procedure risks; its [four original cases](../examples/ai-writing-spec/clarity-context.md)
preserve legitimate academic exceptions. There are 19 primary-source records
and one skill-design record in that historical round; do not sum them as 20 papers reviewed in full.

## Functional Patterns: Select, Then Phrase

The eight `ai.pattern.*` records are local editorial extensions, not modifications
of the imported library. They cover bottleneck/choice, operation/effect,
complementary contributions, question/answer Results, distinct evidence roles,
scoped transfer, family-level contrast and interpretation-changing boundaries.
Each includes `discourse.question`, `predecessor`, `successor` and `non_transfer`.
The lookup and existing `ai_spec_ids` role-packet selection preserve these fields
with the conditions, evidence requirements and source observations.

Use [evidence selection](abstract-decisions.md#select-an-answer-not-a-fact-inventory)
and [sentence progression](writing-library.md#sentence-progression-not-syntactic-variety)
first. Select one applicable relationship, not a sequence of eight mandatory moves.
The [curation record](../docs/research/argument-selection-2026-10-29.md) distinguishes
source observations from original templates and synthetic examples. The total is
now 21 primary-source records and one third-party skill-design record, with actual
read scopes; neither this count nor the eight cards measures learning quality.

## Domain Adaptation and Verification

Borrow the separation of writing rules, dictionary senses, technical terminology,
examples and boundaries from controlled-language design. Do not transplant the
maintenance domain's grammar or numeric limits. Academic passive voice, formulas,
precise compound terms and `-ing` technical names remain legitimate. There is no
20/25-word ceiling, six-sentence paragraph ceiling or global synonym ban here.

Keep three checks distinct:

- **Catalog/guard checks:** record integrity, IDs, bounded retrieval and existing
  artifact/fact constraints; not proof of prose meaning or research correctness.
- **Semantic checks:** final-prose reading and source audit; state who performed
  them and whether independent readers were actually used.
- **Quality evaluation:** equal-budget anonymous comparison with failures and
  disagreements retained; not implied by either preceding check.

Adding this catalog does not promote the experimental operative-relation guide
or its failed continuation gate. A later quality claim needs a separately frozen
test, including terminology misuse, legitimate exceptions and reader understanding.

The [architecture atlas](../docs/writer-atlas.html) maps these responsibilities to
real files. [Design decision](../docs/designs/adr-001-ai-writing-spec.md) records why
the catalog is separate, and [provenance](../UPSTREAM.md#ai-writing-specification-2026-10-12)
records the sources and reading limits. No third-party dictionary or paper prose
is redistributed. Linked papers give terminology context, not manuscript evidence.
