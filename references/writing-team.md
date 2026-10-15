# Bounded Writing Revision Team

Status: opt-in engineering workflow, not a promoted writing-quality improvement.
Use when the author asks for comparative, evidence-backed revision or explicitly
tests this mechanism. Ordinary drafting, punctuation fixes and diagnosis-only
requests do not require this loop. Do not automatically load the experimental
evidence-link guide. Default argument-transfer guidance remains unchanged.

## Four Owners and Two Supporting Functions

| Owner | Question | Handoff | Not its responsibility |
|---|---|---|---|
| [Orchestrator](../agents/writing-orchestrator.md) | What is the next justified action? | Scope, input snapshot, next role, stop/return decision | Writing expert verdicts or changing facts |
| [Gap finder](../agents/writing-gap-finder.md) | How does this section differ from applicable excellent-paper choices and writing standards? | Criterion-level comparisons, strengths, valid alternatives and prioritized gaps | Inventing a scientific gap or treating clarity as the entire quality target |
| [Revision proposer](../agents/revision-proposer.md) | Which concrete edit would resolve that problem? | Operation, expected effect, preconditions, risk, success test | Inventing a new method or experiment |
| [Writer](../agents/revision-writer.md) | How does that operation become clear, accurate prose? | Candidate passage and open author queries | Accepting its own revision |
| [Reviewer](../agents/revision-reviewer.md) | Does the passage itself deliver the intended relation? | Prose-first read-back, three separate judgments, return target | Grading compliance as writing excellence |
| [Exemplar learner](../agents/research-exemplar.md) | Which source choice transfers under our evidence? | Located observation with applicability and non-transfer | Treating generated annotations as paper evidence |

The first four are the requested production/control roles; the last two support
them. Existing citation/integrity reviewers still own their wider manuscript
checks. One agent may execute several roles sequentially, but this is self-review,
not independent multi-agent evidence. Deploy separate contexts only when warranted.

## Retrieve Choices, Not Sentences

Use two retrieval questions: (1) how do papers with the same contribution type
and section function expose the important distinction, and (2) how do papers in
other domains resolve this same reader difficulty? The second question transfers
an editorial operation, not another paper's technical solution or result.

The Svalbard Idea Vault is a discovery source, not a writing-quality label or a
local installed corpus. Follow the [source study](../docs/research/ideascientist-2026-10-15.md)
before using it. A search hit must lead back to the original paper and a bounded
reading. Store the resulting choice in the existing exemplar dossier:

`source + location -> reader problem -> observed choice -> author evidence /
applicability -> planned edit -> non-transfer -> final prose check`.

For related work, establish a comparison axis (task, assumptions, mechanism,
evaluation or scope), inspect the relevant source locations, and distinguish
reported evidence from your interpretation. Record search scope and unresolved
coverage. "Not in these retrieved sources" does not mean "no prior work exists".
A writing gap is not a research gap, and either may require further source reading.

## Executable Handoff Contract

The standard-library helper reads an explicit local JSON run and emits JSON to
stdout. It has no model API, network, credential access or file-writing mode.
Paths in evidence and exemplars are text; the helper never opens them. The host
must perform the actual reading, writing, dispatch and artifact storage.

```bash
python scripts/writing_loop.py examples/writing-team/input.json
python scripts/writing_loop.py RUN.json --response RESPONSE.json
```

Without `--response`, get the next packet and its `input_sha256`. The role returns
`{"role": "...", "input_sha256": "...", "output": {...}}` using that exact
receipt. With `--response`, validate and emit an updated run, without overwriting
the supplied file. The host retains the actual response and saves the new run.
Store a bounded run alongside the existing rationale row when this route is
selected; it is not another mandatory artifact for all papers.

The run has exactly `schema_version` (1), `task`, original `draft`, author
`evidence` (nonempty ID-to-text mapping), `exemplars` (possibly empty),
`max_steps` (4-24), and `events` (initially empty). Each exemplar has `source`,
`location`, `choice`, `applicability`, `non_transfer`. These are observations
already grounded by reading, not a search result's quality score. The orchestrator
chooses a bounded budget; 12 handoffs is a useful starting point, not a quality norm.

### Schema 2: Exemplar and Standards Benchmark

Use v2 for the user's excellent-paper-informed comparison request; v1 remains
readable as the original intrinsic-diagnosis contract. Add `benchmark` to the run
and set `schema_version` to 2. No implicit migration rewrites old events.
Build the target using [section benchmarking](style-learning-workflow.md#section-benchmark-before-revision).

The benchmark has exactly:

- `section`, `contribution`: scope and supported contribution type/priority.
- `protocol`, `variant`: exact bundled section-protocol and variant IDs.
- `ai_spec_ids`, `library_ids`: 0-6 exact IDs each, not entire catalogs.
- `criteria`: 1-12 scoped ID-keyed records with `dimension` (`content`,
  `organization`, `evidence`, `expression`, `clarity`, `format`), `expectation`,
  `applicability`, `resource_ids` and `source_ids`. At least one resource or
  located exemplar must support each criterion. Cover relevant dimensions without
  manufacturing six defects or turning an uninspected format into a pass.

The helper resolves the protocol and cards with the existing lookup APIs and
includes their full checks, conditions, exceptions and source metadata in every
role packet. It does not open manuscript/source paths or fetch papers. Protocol
IDs and complete card bytes enter the input receipt, so a changed selected
resource invalidates old handoffs. Unknown IDs and section mismatches fail closed.
`benchmark_basis` distinguishes `standards_only` from `standards_and_exemplars`;
local norms alone cannot demonstrate learning from a particular excellent paper.

The v2 role outputs extend, not replace, the fields above:

| Role | Additional output |
|---|---|
| Gap finder | `assessments` for every criterion and `selected_criteria` containing only diagnosed gaps |
| Proposer | `criterion_ids` matching selected gaps, addressed concretely in `operation` |
| Writer | `implementations` keyed by every proposed criterion, each with `status` (`realized`/`blocked`), exact `witness`, and `note`; blocked entries require an author query |
| Reviewer | Fresh `assessments` of every criterion, without seeing prior assessments or implementation claims |

Each assessment has `status` (`gap`, `meets`, `valid_alternative`, `not_applicable`,
`not_assessed`), `current`, `difference`, `draft_witness`, `evidence_ids`.
Inapplicable/unassessed criteria use an empty witness and explain the reason.
An omitted idea is witnessed by the existing passage whose selection/organization
should change, not by a quotation invented to fill the schema.
Known gaps or unassessed criteria preclude `no_change` and acceptance; a supported
alternative is allowed. Source needs can stop the gap finder as `needs_sources`.
Checks establish coverage and linkage, not whether judgments are insightful.

See the [clear-but-weaker abstract example](../examples/writing-team/benchmark.md),
including related-work and experiment contrasts. New runs are required after this
guidance update; old raw events are retained rather than silently re-hashed.

Every event is owned by the expected role. Its receipt binds task, original draft,
evidence, exemplars, budget, full event prefix, role context and loaded guidance.
Changed upstream inputs invalidate old receipts. Fork a new run and preserve the
old one rather than relabeling old outputs. Hashes are not signatures or proof
that another agent produced the content.

Reviewer packets omit the diagnosis, proposal and previous review, so the reviewer
must recover meaning from prose. They include the original passage for a subsequent
non-blind editorial comparison (`better`, `tie`, `worse`, `not_assessed`). Other packets contain only stage-relevant
handoffs. This projection cannot erase a host agent's memory or restrict its tools.

## Feedback and Stopping

- Wrong diagnosis: return to `gap_finder`; discard the current plan for dispatch.
- Suitable diagnosis, unsuitable operation: return to `proposer`.
- Suitable plan, poor prose realization: return to `writer`.
- Missing author/source evidence: `needs_evidence`; ask the minimum factual query.
- No useful gap: `no_change`. Unhelpful revision: `keep_original`.
- Reviewer-supported completion: `accepted_revision`.
- Budget reached without acceptance: `budget_exhausted`; keep the original.

Previous events stay inspectable. Every non-acceptance stop returns the original
as `retained_text`, even if a later attempt is fluent; `last_attempt_text` remains
available for inspection. The helper does not patch the manuscript. The host
locates an accepted edit in the rationale matrix's Final Text Check and reports
scope and unresolved limitations to the author.

## Three Feedback Channels, Not One Reward Number

| Channel | Inspect | Common false positive |
|---|---|---|
| Intrinsic writing quality | Contribution recovery, operative connection, evidence selection, organization and compression | Accurate numbers listed without an argument |
| Reference-function transfer | Whether a source's applicable writing choice resolves the same reader problem | Shared vocabulary or identical sentence order |
| Evidence fidelity | Referents, comparisons, conditions, scope, negation and uncertainty against author materials | Plausible scientific prose unsupported by this study |

Each channel records `pass`, `fail` or `not_assessed`, with a reason and exact
prose witness for assessed judgments. Fidelity passes cite author evidence IDs;
reference passes cite located exemplar IDs. With no exemplars, reference transfer
is explicitly unassessed. Alternative sound structures may pass.

Acceptance requires intrinsic/fidelity passes, an applicable reference judgment,
no unresolved writer queries, and a better-than-original comparison with a located
reason. A tie, unassessed comparison or unchanged text cannot be promoted as an
improvement. Deterministic checks verify IDs, witnesses,
ownership and freshness only; semantic judgments remain fallible. Citation-set F1
may diagnose retrieval coverage in a separate study, never rank prose or force
citations into an abstract. Do not sum these channels, reward extra searches, or
claim reinforcement learning took place.

## Development and Evaluation

The [worked example](../examples/writing-team/README.md) and automated transition
tests are authored development material, not independent writing outcomes.
Freeze role cards, reference choices and budgets before a new held-out trial.
Compare default writing, this role loop, and an equal-call-budget unstructured
revision baseline; ablate the proposer or reference channel to identify cause.
Hold out entire papers and their versions, keep author abstracts/reference answers
out of writer packets, and fix denominators including invalid or missing outputs.
Use order-balanced blind judgments with located reasons and a separate fidelity
audit. Log tokens, calls, stops and raw outputs. A failed promotion gate cannot be
overridden by passing these software tests or increasing the resource count.
