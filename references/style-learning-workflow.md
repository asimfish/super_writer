# Style Learning Workflow

Use this reference when the user wants the manuscript to imitate excellent papers, a journal, or a conference.

## Goal

For corpus-based manuscript rewriting, convert the selected full texts into a
reusable `style_profile.md` before imitation; use it to guide later revisions.
For a bounded passage or organization-learning request, keep the relevant
observations in the existing plan as described below, without a full profile.

For deep imitation, also read `deep-imitation-protocol.md` after this file.

Use [argument transfer](argument-transfer.md) to turn each useful observation
into a located writing choice and an evidence-conditioned text action. For a
bounded request, analyze only the relevant passages and keep these decisions in
the existing plan. Corpus metrics describe examples; they do not prescribe how
many paragraphs, citations or numbers our argument must contain.

## Section Benchmark Before Revision

When the author wants excellent-paper-informed writing, set a positive quality
target before diagnosing defects. Understandable, grammatical prose can still
choose the wrong information, bury the insight, narrate tables, or summarize
papers without synthesis. The gap finder compares the draft with this target;
it does not merely search for confusion or invent its own ideal paragraph.

Use the existing resources, in this order of purpose (not authority):

1. **Author contribution and section function:** decide what this passage must
   accomplish and what evidence is available. A theory abstract and a dataset
   abstract need different targets.
2. **Located exemplar choices:** choose relevant observations from the existing
   dossier or [abstract notes](abstract-exemplars.md), or read the relevant source
   section when needed. Notes on an abstract cannot establish that paper's
   experiment or related-work style. Prefer complementary examples when the
   choice is contentious; do not require a paper-count quota.
3. **Reusable norms and expression:** select one [section protocol](writing-protocols.md),
   applicable [AI-spec records](ai-writing-spec.md), and optional [language cards](writing-library.md).
   These local syntheses are conditional guidance, not official conference rules.
4. **Format authority:** use supplied requirements and the exact venue/year/track/
   stage guide for mandatory formatting. Do not infer word limits, citation bans
   or caption styles from famous papers. Missing current rules mean unverified
   compliance, not permission to substitute an archived profile.

Cover these dimensions at the requested scope; record why an excluded dimension
is inapplicable or unassessed. They are not six mandatory weaknesses to repair.

| Dimension | Positive target | Difference worth diagnosing |
|---|---|---|
| Content selection | Space goes to the distinctive contribution and consequential evidence | Correct implementation details crowd out the key insight |
| Argument organization | Moves and paragraph roles form an effective progression | A list of accurate statements leaves the argument implicit |
| Evidence presentation | Comparisons, displays and interpretation answer the section's question | Scores are enumerated without showing what they establish |
| Academic expression | Precise disciplinary terms, informative verbs, economical sentence roles | Generic praise or inflated wording replaces scientific specificity |
| Clarity and cohesion | Referents, transitions and information dependencies remain recoverable | The relation must be reconstructed from the author's notes |
| Format and reporting | Applicable structural/reporting requirements are met | Unexplained table conventions, missing units or verified format violations |

The section changes what these dimensions mean:

| Section | Compare with applicable exemplars | Useful local starting point |
|---|---|---|
| Abstract | Contribution emphasis; obstacle/insight/mechanism relation; decisive evidence; information compression; scoped ending | `abstract` with a contribution-matched variant; [abstract decisions](abstract-decisions.md) and selected exemplar notes |
| Related work | Technical grouping; synthesis across sources; fair comparison axes; relationship to our contribution; citation-to-claim scope | `related_work` / `taxonomy-first` or `concept-evolution` |
| Experiments | Questions mapped to controls; setup/result/analysis separation; result ordering; ablation/failure logic; tables, captions and reporting | `experiments` for section structure, `experiments.analysis` for a passage, or one matching table protocol |

Record comparisons in existing dossier/rationale rows:

`criterion -> source/resource location and observed choice -> our current choice
-> consequential difference -> applicability -> edit -> final-text witness`.

Use `gap`, `meets`, `valid_alternative`, `not_applicable` or `not_assessed` rather
than a vague excellent/poor label. A method-first opening, chronological account
of a genuine conceptual evolution, or necessary technical repetition can be a
valid alternative. Different facts may require a different rhetorical choice.
Show what should improve, what already works, and what must not be transferred.

In the explicitly selected [role loop](writing-team.md), use schema v3 to carry
these criteria and selected resources through every handoff. The writer must
locate the implementation of each proposed criterion; the reviewer rechecks the
criteria against the prose without seeing earlier assessments. No clear-text
case should be declared good merely because it is understandable. Before cutting,
identify 1-3 indispensable explanatory relations and any essential co-contribution
in the existing plan. Preserve them in prose, not just keywords or writer notes.
Apply [explanation-preserving compression](compression-first-writing.md); a draft's
current length is not automatically its ideal budget. V1/v2 remain compatible.

For drafting from materials, use the same target and exemplar-informed blueprint
before the first draft. There is no existing-prose gap to invent, and the revision
checker is unnecessary until a passage exists. Learn organization, evidence
allocation and scientific phrasing; write original prose from the author's facts.

## Explain a System or Synthesize a Rule Set

Use this bounded branch when the user supplies a diagram, overview or passage
and asks to learn its organization. Read that material first. Analyze only the
visible structure; a one-page overview does not establish the full specification
or the unseen paper's organization. Keep notes in the existing plan or profile;
do not require a full corpus, new database or all downstream artifacts.

Distinguish the system's workflow from its supporting resources and validation.
A module list answers what exists; a useful explanation also shows what enters,
what each operation changes, where its output goes and why the parts are grouped
that way. Describe real dependencies, not an invented pipeline chosen to fit the
reference. A taxonomy, derivation or parallel interaction may explain the object
better than a sequence.

One useful presentation is a structural map, an annotated unit, conditional
entries, limits and provenance. Choose only what clarifies the requested object;
these are explanation options, not obligatory manuscript sections. Label a
synthetic example as such. Show a positive example and a misleading transfer
when the contrast clarifies applicability, rather than copying source sentences.

For a reusable observation, adapt the existing dossier row with these fields:

| Field | What to record |
|---|---|
| Location and reading scope | Visible panel, sentence or passage; what was not read |
| Function | Reader question answered or dependency made intelligible |
| Applicability | Kind of work and author evidence that permit this choice |
| Text action | Explain, distinguish, reorder or qualify a specific relationship |
| Contrast and exception | A misleading version or a case needing another order |
| Nature and evidence | Source observation, project convention, optional guidance or experimental candidate; actual verification, if any |
| Prose check | What the reader can recover from the final unit without notes |

Group observations by the reader problem or operation they share, not just by
venue, similar words or sentence length. Keep distinct assumptions distinct;
record a non-transfer when our materials cannot support the source's structure.
Repeated observations do not become official requirements, and an instruction
currently used by this project is not thereby a proven quality improvement.

Transfer the explanatory organization, not domain-specific restrictions. A
maintenance manual's sentence budgets or vocabulary approval do not establish
academic-writing limits. Preserve technical definitions, uncertainty, equations
and scope. Claims of improved writing need separate evaluation under
[blind evaluation](blind-evaluation.md); filled entries and guard passes are not
such evidence. This branch does not promote evaluation snapshots to defaults.

## Corpus Selection

Prefer 3-6 full-text papers:

| Corpus Slot | Purpose | Selection Rule |
|---|---|---|
| Same-task exemplar | learn direct argument structure | same task and method family |
| SOTA exemplar | learn current field expectations | recent, strong venue, high-quality writing |
| Prior milestone | learn field lineage | heavily cited or directly built upon |
| Adjacent exemplar | learn alternative framing | nearby task or method |
| Venue exemplar | learn journal/conference voice | same target venue, recent |
| User favorite | honor user's taste | user says "write like this" |

If the user has no corpus, ask for PDFs or extracted text first. Use web search only when the user wants help finding papers or the paper list is incomplete.

## Preparation

1. Extract text from PDFs when needed.
2. Keep each paper in a separate file.
3. Preserve section headings.
4. Run style metrics when possible:

```bash
python scripts/style_metrics.py <corpus-folder> --markdown > paper_rewriting_output/style_metrics.md
```

5. Read `style_metrics.md` before writing qualitative conclusions.

## Style Profile Template

Save as `paper_rewriting_output/style_profile.md`.

```markdown
# Style Profile

## Corpus

| ID | Title | Venue/Year | Role | Why Selected |
|---|---|---|---|---|

## Global Style

- Typical paper arc:
- Reader expertise assumed:
- Claim strength:
- Technical density:
- Citation style:
- Figure/table emphasis:

## Section Profiles

### Abstract

| Dimension | Corpus Consensus | Rule for Our Paper |
|---|---|---|
| Sentence count | | |
| Move sequence | | |
| Numerical specificity | | |
| Opening pattern | | |
| Closing pattern | | |
| Forbidden moves | | |

### Introduction

| Dimension | Corpus Consensus | Rule for Our Paper |
|---|---|---|
| Paragraph count | | |
| Move sequence | | |
| Gap statement style | | |
| Contribution placement | | |
| Citation density | | |
| Final paragraph role | | |

### Methods

| Dimension | Corpus Consensus | Rule for Our Paper |
|---|---|---|
| Procedure depth | | |
| Equation/code detail | | |
| Subsection rhythm | | |
| Rationale placement | | |
| Evaluation setup style | | |

### Results

| Dimension | Corpus Consensus | Rule for Our Paper |
|---|---|---|
| Result ordering | | |
| Figure/table callout style | | |
| Quantitative detail | | |
| Comparison language | | |
| Interpretation depth | | |

### Discussion/Conclusion

| Dimension | Corpus Consensus | Rule for Our Paper |
|---|---|---|
| Opening move | | |
| Summary vs interpretation balance | | |
| Limitation style | | |
| Future work style | | |
| Closing move | | |

## Phrase and Skeleton Bank

Record patterns, not copied prose.

| Function | Source Pattern | Reusable Skeleton | Notes |
|---|---|---|---|
| establish gap | verbatim example for analysis only | `Although [prior capability], [specific gap] remains [unresolved].` | rewrite before use |
| present method | | `We introduce [method], a [descriptor] approach for [task].` | |
| interpret result | | `These results suggest that [mechanism], particularly when [condition].` | |

## Claim Strength Rules

| Claim Type | Allowed Verbs | Avoid |
|---|---|---|
| direct experimental result | | |
| interpretation | | |
| speculation | | |
| limitation | | |

## Terminology and Collocations

| Concept | Preferred Term | Avoid | Evidence |
|---|---|---|---|

## Style Constraints for Rewriting

- Section length targets:
- Paragraph length targets:
- Sentence length targets:
- Citation density target:
- Maximum claim strength:
- Words/phrases to avoid:
- Must-use conventions:

## Section Blueprint Inputs

For each section, list the exact constraints that must be transferred into `section_blueprints.md`:

| Section | Obligatory Moves | Exemplar Closest Match | Paragraph Count Target | Evidence Placement Rule | Opening/Closing Rule |
|---|---|---:|---:|---|---|

Also create a compact transfer table that links the style profile to the writing templates:

| Section | Style Rule | Paragraph Template Row | Result Template Row, If Applicable | Why This Transfers |
|---|---|---|---|---|

## Observed Patterns and Actual Constraints

Identify actual official venue requirements separately from recurring prose
patterns. A choice shared by two papers is an observation, not a mandatory rule.
Record when our contribution or evidence calls for a different choice.
```

## How to Infer Style

Use this order:

1. Hard venue rules: official guidelines and template.
2. Corpus consensus: patterns shared by most exemplar papers.
3. Closest-paper pattern: when only one exemplar matches the user's paper closely.
4. General academic writing norms: only when corpus evidence is absent.

Always state which level supports each rule.

## Anti-Plagiarism Rules

- Verbatim sentences may appear in analysis tables, but not in the user's manuscript.
- Convert source wording into abstract skeletons before reuse.
- Do not reuse rare metaphors, distinctive phrases, or unusual sentence sequences.
- Common academic transitions are acceptable, but still adapt them to the user's content.

## Style Fit Report

After rewriting, produce a short check:

```markdown
## Style Fit Report

| Section | Target Pattern | Applied? | Evidence | Remaining Gap |
|---|---|---|---|---|

## Metrics Drift

| Metric | Corpus Target | Revised Draft | Acceptable? |
|---|---:|---:|---|

## Manual Judgment

- Strongest style match:
- Weakest style match:
- Next revision priority:
```

## Completion Check

The style-learning phase is incomplete if:

- no `style_profile.md` was produced,
- no `style_metrics.md` was produced when analyzable text was available,
- section profiles are generic rather than section-specific,
- no `paragraph_function_templates.md` exists when section rewriting is requested,
- no `result_narrative_templates.md` exists when Results rewriting is requested,
- the profile does not specify how the user's sections should be rebuilt,
- the later rewrite matrix cannot point to concrete rules in the profile.
