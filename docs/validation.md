# Validation Scope

Super Writer combines an inherited PaperSpine V4 workflow with bounded guards,
portable distribution and public writing examples. Tests establish the specific
behavior below, not research novelty, factual entailment or acceptance gains.

## Reproducible Checks

### Section benchmarks beyond clarity (2026-10-15)

Schema v2 carries contribution-matched criteria, selected existing protocols,
AI rules and language cards through diagnosis, proposal, prose and fresh review.
The [worked comparisons](../examples/writing-team/benchmark.md) cover an abstract,
related work and an experiment passage; only the abstract has a full authored
four-role fixture. None is an independent model trial or a measured quality gain.

- Sixteen new tests cover exact complete resource projection, three section types
  and a table protocol, unknown IDs, wrong section/variant, duplicate or excessive
  selections, missing criterion bases, invalid dimensions, complete assessments,
  exact witnesses, valid alternatives, and unassessed-source stops.
- Selected gaps cannot silently disappear or be replaced in the proposal; every
  proposed criterion needs a located realization or explicit blocked query.
  Review checks all declared criteria, including previously adequate dimensions,
  without receiving earlier assessments or the writer's implementation claims.
- Changed resource content or criteria invalidate old receipts. The standards-only
  label, read-only/offline behavior, mutation isolation and relocated release CLI
  are checked. Local-synthesis entries preserve empty source notes rather than
  receiving invented paper attribution.
- Python 3.14 on macOS runs 331 cases: 330 pass, one PowerShell-unavailable skip.
  All 11 smoke checks, compilation, skill validation and whitespace checks pass.
  The old pilot archive and frozen default guide remain unchanged; library,
  protocol and venue resource hashes retain their previous values.

```bash
python -m unittest discover -s tests -p test_writing_benchmark.py -v
python scripts/writing_loop.py examples/writing-team/benchmark-input.json
```

Three added activation expectations are declared behavior, not measured routing
accuracy. No automatic library expansion, new paper reading, official-format
certification, default quality promotion or model-weight training occurred.
The test suite verifies contracts and authored fixtures, not the insightfulness
of an arbitrary future comparison. Remote CI remains separate commit-bound evidence.

### Optional writing-role handoffs (2026-10-15)

The [role workflow](../references/writing-team.md) and
[source study](research/ideascientist-2026-10-15.md) add an explicit, bounded
revision route, not a new default or a successful writing-quality trial.

| Acceptance scope | Observed local evidence |
|---|---|
| Role contract | 21 focused tests cover the authored sequence, all review return targets, missing evidence, no-change, original retention, exact budget boundary and exhausted budget |
| Input integrity | Changed task/evidence/exemplar/guidance/history invalidates receipts; wrong owners, unknown or duplicate IDs, absent witnesses, duplicate JSON keys and undeclared fields are rejected |
| Acceptance boundaries | Failures, open queries, unassessed applicable references, ties, regressions and unchanged text cannot be accepted as improvements |
| Context and effects | Review input omits diagnosis/proposal/prior review; mutable packet changes do not change the run; offline/read-only behavior and non-dereferenced source paths checked |
| Distribution | Build a real ZIP, extract to a path with spaces, run the installed CLI, match the source packet, append a response without altering input, reject malformed response cleanly |
| Regression | Python 3.14 on macOS: 315 cases, 314 passed, one PowerShell-unavailable skip; all 11 inherited smoke checks pass |
| Static and preservation | New Python compiles; skill validator and whitespace check pass; the AI-spec archive check verifies frozen inputs, 13 completions and derived outputs; default guide and resource corpus hashes remain unchanged |

Reproduce the key checks from the repository root:

```bash
python -m unittest discover -s tests -p test_writing_loop.py -v
python -m unittest discover -s tests
python scripts/smoke_test.py
python evals/ai-spec-pilot/archive.py check
python scripts/writing_loop.py examples/writing-team/input.json
```

The example responses and judgments are authored together, not obtained from
independent model calls. The reviewer comparison is non-blind. Source analysis,
structural tests, and valid handoffs do not establish semantic accuracy, host
isolation or writing gain. Three added activation expectations are declarations,
not executed activation-rate measurements. No new dependencies, provider SDKs,
dataset rows, imported noncommercial code, tags or global installation are added.
Remote CI must be inspected on the pushed commit separately; local macOS tests
alone do not establish Windows or Linux compatibility.

### Opt-in evidence-link mechanism (2026-10-14)

The [candidate procedure](../references/evidence-link-candidate.md) implements
promise-relevant evidence selection, evaluated-object/comparison binding, prose
realization and read-back inside the existing dossier/rationale workflow. It is
explicitly selected, not a default promotion. The last AI-spec trial's 3 / 10 / 11
verdict and failed gate remain unchanged. No new model writing trial is executed.

- Twelve new tests pass: 16 paired development inputs differ in exactly one
  priority, scope or evidence field; baseline/candidate packets share all writer
  fields except guidance; private expectations stay out of input assembly. Hashes,
  malformed/unknown selections, no-op and non-counterfactual changes, offline
  assembly and default-guide preservation are checked. A caller-mutation regression
  first fails, then passes with separate evidence snapshots for each packet.
- The actual release bundle retains the candidate, cases, README and packet tool;
  an extracted, relocated CLI produces the same complete packet and input digest.
  The tool prints JSON only; it does not generate prose, grade semantics or enforce
  filesystem isolation. Guidance exposure is unequal and disclosed. A 120-word
  ceiling has no lower-bound padding requirement.
- Python 3.14 runs 294 tests: 293 pass, one PowerShell-unavailable skip. All 11
  existing CLI smoke checks, Python compilation and whitespace checks pass.
  This is local macOS evidence; remote CI/platform results are checked separately.
- The AI-spec archive check still reproduces all frozen inputs, 13 completions,
  blinding, judgments, recovery and HTML, with all 55 experimental receipts intact.
  The default argument-transfer guide is byte-identical to its frozen baseline;
  library, protocol and venue hashes retain the ADR-001 values. No catalog entries,
  agent defaults, versions, tags, global installs or prior experimental outputs change.

The eight families / 16 probes / seven domain labels describe original synthetic
development fixtures, not a paper corpus or independent samples. Three additional
activation expectations are declarations, not an executed model routing evaluation.
The new guide is locally authored from located failure hypotheses; no upstream
text, dependency or new runtime network/credential/execution capability is imported.
It adds no artifact columns or compulsory full-paper workflow for bounded edits.

Engineering checks pass; writing effectiveness and independent semantic/activation
review remain unverified. A fresh real-paper trial must freeze cases, budgets,
access and promotion criteria before generation. Known development cases and past
votes cannot establish held-out improvement. See the
[reproduction commands and evaluation boundary](../evals/evidence-link/README.md).

### Pilot output-link portability (2026-10-13)

The [first pilot publication CI](https://github.com/asimfish/super_writer/actions/runs/38399574723)
passes Linux 3.10/3.12, macOS 3.12 and document fixtures, but Windows 3.12 fails
`test_exclusive_output_rejects_dangling_symlink`: exclusive text opening follows
the dangling output link instead of rejecting its existing directory entry.
This is separate from the earlier atlas cross-drive defect.

A shared `lstat` preflight now rejects any existing output entry, including a
dangling link, before exclusive opening in the pilot CLI and archive JSON/HTML
writers. Two permissive-opener replay tests first fail, then pass; the original
Windows-capable integration test remains unchanged. Static leaf checks are not
a guarantee against hostile directory replacement or filesystem races.

Locally, all 58 pilot checks pass; the full suite runs 282 tests, with 281 passes
and one PowerShell-unavailable skip. Focused replay also passes on Python 3.9.
All 55 experimental byte receipts, 13 completion strings, derived judgments and
HTML remain unchanged; no writing result or gate is revised. This is macOS
replay evidence, not local Windows execution. Corrective-commit remote CI is
checked separately before delivery.

### Current AI-spec pilot archive (2026-10-13)

The [new writing pilot](ai-spec-pilot-evaluation.md) fails its preference gate:
candidate 3 / baseline 10 / tie 11. The following checks establish engineering
integrity, not a writing-quality gain or runtime promotion.

- Python 3.14: 280 tests, 279 pass and one PowerShell-unavailable skip. The 56
  new pilot checks cover synthetic schema/gate failures, reversal, frozen input
  tampering, completion preservation, witnessed answers and archived results.
- All 11 existing CLI smoke checks pass; Python compilation and diff checks pass.
  Focused synthetic pilot checks also pass under local Python 3.9, outside the
  project's supported Python 3.10+ promise.
- `archive.py check` reproduces 13 completion strings, 12-pair blinding, word
  counts, judgments, 96 audited answers and HTML; experimental byte receipts match.
  All source-catalog hashes and the default argument-transfer guide remain unchanged.
- Chromium 153.0.8010.12 at 1600x1100, 900x1000 and 390x844 verifies every final
  and initial passage, all 60 expandable details, filter/reset paths and three
  local links. No horizontal overflow, section overlap, console errors or remote
  requests; all three screenshots are inspected. See the
  [browser receipt](../evals/ai-spec-pilot/browser-check.json).
- Release packaging succeeds using the existing builder. No dependency install,
  version/tag change, full source-paper redistribution or runtime-guide change.
  Public-source PDFs/extractions stay outside the repo. Six reader-answer cap
  deviations remain visible, with no model-output repair or exclusion.

These are local macOS checks; remote CI/platform outcomes are separate evidence.

### Atlas cross-drive portability (2026-10-13)

The first public CI for `bfc1406` completed with four successful jobs (Linux
Python 3.10/3.12, macOS Python 3.12, and document/template fixtures) but failed
the Windows Python 3.12 job. Two atlas CLI tests could not render into the
system temporary directory: repository and output were on different drives,
which cannot have a relative path. `ntpath.relpath` reproduces that exception.

Owner links now use encoded local file URIs across drives and retain relative
links on one drive. A Windows-path fixture first fails, then passes with the
fix; same-drive and existing deterministic/symlink/drift checks remain covered.
Local Python 3.14 runs 224 tests: 223 pass, 1 PowerShell-unavailable skip;
all 11 atlas tests pass and checked-in HTML/SVG bytes remain unchanged. This is
host-independent Windows path evidence, not a Windows execution claim. The
corrected commit's remote Windows result must be checked separately. No writing
guidance, frozen quality experiment or effectiveness conclusion is changed.

### Selective MARMOT context integration (2026-10-13)

The [pinned source review](research/marmot-ste-integration-2026-10-13.md) reads
all four upstream Markdown files and the MIT license, verifying Git blob IDs
and recording SHA-256 receipts. No upstream rule database or executable resource
is imported. The local catalog is now 0.4 with 68 entries: 19 rules, 15 claim
uses and 34 terms; its 19 primary-source records remain separate from the added
third-party skill-design context.

| Criterion | Executed local evidence |
|---|---|
| Catalog / CLI | 27 tests pass, including new Chinese procedure lookup, full conditional exception/source-pin retrieval, extended definition case and legitimate academic/literal exceptions. New contracts first fail on missing resources/cases, then pass |
| Regression | Python 3.14: 222 tests, 221 passes, 1 PowerShell-unavailable skip; all 11 CLI smoke cases pass. The changed-pin importer rejection remains an expected fixture |
| Distribution | 35 tests pass. The actual bundle retains the guide, review ledger, four-case example and byte-identical MIT notice; a relocated extracted CLI retrieves the canonical procedure-order entry. A red-state test exposed missing-license acceptance; the new preflight rejects that input before build or temporary installation output |
| Atlas / browser | 9 atlas tests pass. Chromium 153.0.8010.12 at 1600x1100, 900x1000 and 390x844 checks 68 records, 8 nodes, 9 edges and 106 local targets per view. Existing 45 desktop facet intersections and search/empty recovery/deep-link journeys pass |
| Visual / offline boundary | No page/control/panel overlap or overflow, SVG label failure, remote request or browser error; all three viewport screenshots are inspected. Mobile diagram scrolling is intentional; the flow remains nonblank at 30,263 nonwhite pixels |
| Preservation | Only `ai.rule.definition` changes among the previous 67 entries; all other 66 entries and all previous 19 source records compare unchanged. Imported library/protocol/venue hashes and the frozen argument-transfer baseline still match |
| Attribution / capabilities | Retained MIT license SHA-256 is `fe29e8048edc1f0ae8123ffc96ba0b3022d1fb2b7aa6995ffa708c539376fd1e`. The reviewed upstream directory has no code/hooks/dependencies; no new runtime network, credential, command-execution or publication capability is added. Hidden-control checks are clean, not a semantic safety proof |
| Activation contract | Four new expectations are self-reviewed; all 23 declarations have unique IDs and valid positive/negative metadata. This is not an executed model activation evaluation or a measured routing rate |
| Documentation / static | Twenty-three Markdown files have 357 valid local targets and 43 fragments; a 30-file configured credential-pattern scan has no matches. Python compile, Node syntax, skill YAML, generated-output drift and diff whitespace checks pass |

The [context-sensitive guide](../references/clarity-context.md) uses existing
bounded edits and read-back, not a new mandatory report or universal grammar
policy. Its four contrasts are authored development fixtures, not blind tests.
Local integration checks pass; release/governance verdict is `CONDITIONAL`
because independent domain/semantic review, model activation, fresh writing
quality tests, Windows, remote CI and a full Forge audit were not executed.
No official dictionary verification, certification, version bump, global install,
commit or push is claimed. Previous milestone receipts below remain historical.

### Grounding and sequential evaluation (2026-10-13)

Specification 0.3 contains 67 original entries: 18 rules, 15 claim-use senses and
34 terms, with nine topics, five levels and seven domains. Seven new primary
sources bring the source count to 19; their actual selected-section scopes and
the MDETR PDF retrieval failure/fallback are disclosed in the
[research ledger](research/ai-spec-expansion-2026-10-13.md).

| Criterion | Executed local evidence |
|---|---|
| Catalog / CLI | 24 tests pass. All 67 exact IDs return complete records; new Chinese aliases and domain/topic/level/kind intersections are exercised, along with the existing schema, budget and offline/read-only contracts |
| Authored boundaries | Fourteen new entry-specific checks retain positive wording, explained errors, legitimate exceptions and source anchors. The task-chain fixture distinguishes full success, mean prefix and conditional survivors. These are synthetic contracts, not an independent semantic-quality evaluation |
| Regression | Python 3.14: 218 tests, 217 passes, 1 PowerShell-unavailable skip. All 11 CLI smoke cases pass. `Import failed: changed pin` remains an expected rejection fixture |
| Atlas / browser | 9 atlas tests pass; Chromium 153.0.8010.12 at 1600x1100, 900x1000 and 390x844 checks 67 records, 8 nodes, 9 edges and 102 local targets per view. All 45 topic/level intersections are checked on desktop |
| Journeys / visuals | Chinese visual-grounding search, complete source-scope display, record expansion and a faithfulness fragment opened through conflicting filters pass on all three views. No page/control/panel overflow or overlap, SVG label failure, remote request or browser error; screenshots are inspected. Mobile diagram scrolling is intentional and checked. The diagram has 30,263 nonwhite pixels |
| Distribution | 34 distribution tests pass, including the actual checkout bundle's new ledger and worked cases. An extracted, relocated CLI retrieves the canonical visual-grounding entry using Chinese domain/topic/level aliases |
| Existing-record fidelity | All previous 53 entries, including 1,171 fields, and all 12 previous source records compare unchanged against the pre-edit snapshot |
| Frozen resources | The three ADR-001 SHA-256 receipts still match; argument-transfer remains byte-identical to its frozen baseline. No experimental guide is promoted |
| Static / documentation | Six Python files compile without bytecode writes; Node syntax, generated-output check, skill YAML and diff whitespace pass. Eighteen Markdown files have 312 valid local targets and 35 fragments; a 23-file configured credential-pattern scan finds no matches, not a full security audit |

The [five new worked cases](../examples/ai-writing-spec/grounding-and-horizon.md)
include two complete question-led Results contrasts. Their facts and arithmetic
are invented; they are not results from CALVIN or the other cited papers. No
fresh blind writing comparison, activation evaluation, independent curator,
Windows execution, remote CI, full Forge governance audit, skill version bump,
global installation, commit or push is performed. Local engineering checks pass;
the broader publication/quality gate remains conditional, not a release verdict.
The earlier measurements below remain historical receipts.

### Classification and curated expansion (2026-10-12)

Schema 2 extends the initial catalog below to 53 records: 15 writing rules,
12 claim uses and 26 terms, tagged across 8 reader-problem topics and 5 writing
levels. Six additional primary sources were read to the exact scopes in the
[research record](research/ai-spec-expansion-2026-10-12.md), not as full-paper audits.
The [curation workflow](../references/ai-spec-learning.md) is manual/agent-driven;
no automatic research job, crawler, training or quality promotion is implemented.

| Criterion | Executed local evidence |
|---|---|
| Catalog / CLI | 21 tests pass. Topic/level/kind intersection, Chinese aliases, all 53 complete records, located source notes, malformed facets/notes, schema-1 readability and unsupported-filter failure are covered |
| Boundary fixtures | Seven curated distinctions survive actual CLI retrieval, including chunk horizon versus feedback, prompting versus updates, hybrid offline/online phases, preference provenance and causal attribution. These are authored synthetic fixtures, not an independent semantic or model-behavior evaluation |
| Atlas | 9 tests pass. Canonical facet options, IDs/deep-link targets, complete note/example preservation, deterministic HTML/SVG and existing path/escaping protections are checked |
| Regression | Python 3.14: 215 tests, 214 passes, 1 PowerShell-unavailable skip. All 11 CLI smoke cases pass. The `Import failed: changed pin` line is an expected importer rejection fixture, not a failed test |
| Browser | Chromium 153.0.8010.12 at 1600x1100, 900x1000 and 390x844: 53 records, 8 nodes, 9 edges, 83 valid local targets per view; complete semantic fields/source notes match canonical data. Forty topic/level intersections are checked on desktop and a representative intersection on each view |
| Layout / journeys | No page overflow, control overlap, panel overlap, escaping SVG labels, remote request or browser error. Chinese search, empty recovery, record expansion, direct fragment opening and bounded diagram scrolling pass; screenshots are inspected and double-column list spacing is corrected |
| Preservation | All three ADR-001 resource SHA-256 receipts still match; the canonical argument-transfer guide remains byte-identical to the frozen baseline. The previously failed continuation gate is not promoted |
| Distribution | The actual checkout bundle includes the learning workflow, classification ADR, research ledger and six-case guide, as well as the existing atlas assets. The relocated extracted CLI retrieves a complete action-chunking record with topic/level filters and source notes |
| Runtime boundary | Lookup remains offline and read-only under the existing no-network/no-process/no-write audit test. Research and rendering tools are separate from runtime guidance |
| Documentation / bounded scan | Fourteen principal Markdown files have 269 valid local targets and 20 fragments; the contributor and library additions are also checked. A 21-file scoped credential-pattern scan has no configured matches, not a full security audit |
| Existing-record fidelity | All 689 pre-existing fields across the original 36 records are checked unchanged; additions are facets/source notes, not silent rewrites of old examples or conditions |

Python compilation without writing bytecode, JavaScript syntax, Markdown targets
and fragments, skill frontmatter, generated-output drift checks and diff whitespace
are checked separately. Catalog integrity and curated contrasts do not establish
independent reader understanding, superiority over original abstracts, conference
compliance or remote CI success. No commit, push, version bump or global install
is performed. The initial milestone's measurements below remain historical receipts.

### Local AI specification and engineering atlas (2026-10-12)

This milestone implements a separate original catalog: 12 writing rules, 6
claim-usage entries and 18 AI technical terms. Each record keeps conditions,
evidence requirements, exceptions, original synthetic positive/negative examples,
an owning playbook and bounded source context. The pinned 130-card library remains
the default. The specification guides an agent; it does not automatically verify
manuscript semantics, certify STE conformity or establish better writing.

| Criterion | Observed local evidence |
| --- | --- |
| Record and retrieval integrity | 15 AI-spec tests pass; all 36 exact records retain complete fields; malformed aliases/statuses/URLs, oversized/corrupt indexes, cross-catalog IDs and insufficient output budgets fail without partial output |
| Atlas contracts | 8 tests pass: deterministic generation, nonwriting drift checks, missing output, actual owner links, full examples/qualifications, HTML escaping, related-card drift and symlink output rejection |
| Regression | Python 3.14: 208 tests, 207 passes and one PowerShell-unavailable skip; all 11 CLI smoke cases pass |
| Static quality | Python compilation, JavaScript syntax, skill frontmatter and diff whitespace checks pass |
| Preservation | The three library/protocol/venue SHA-256 receipts in the ADR still match; canonical argument-transfer guidance remains byte-identical to the frozen baseline |
| Packaging | A regression first exposes missing `BENCHMARK.md`; adding that optional document preserves the existing allowlist. The actual checkout bundle retains the catalog, guide, HTML, SVG and PNG byte-for-byte; its extracted CLI retrieves a complete AI-spec record from a temporary relocated directory |
| Browser journey | Chromium 153.0.8010.12, 1600x1100 and 390x844: 36 records, 8 nodes, 9 edges, 60 valid local links; no page overflow, label escape, panel overlap, remote request or JS error. Chinese search, complete record expansion, empty-filter recovery and mobile diagram scrolling pass |
| Visual evidence | Overview and mobile screenshots inspected; SVG rasterization contains 30,263 nonwhite pixels at 950x335. Mobile retains an intentional horizontally scrollable diagram without page overflow |
| Data boundary | Lookup succeeds with an audit hook forbidding network, child processes and writes. Atlas inputs are bundled public records, not private manuscripts; no model calls, credentials, full paper or STE dictionary imports |
| Activation scope | Two academic terminology cases and one explicit maintenance-domain exclusion added as expectations. Packaging checks their structure; no independent model activation trial is claimed |
| Documentation | Local Markdown destinations/fragments and HTML/SVG owner links checked; CLI examples executed. This does not establish remote-link availability |

Representative repository-root commands (Python >=3.10; this run uses 3.14):

```bash
python -B -m unittest discover -s tests -p test_ai_writing_spec.py -v
python -B -m unittest discover -s tests -p test_writer_atlas.py -v
python -B -m unittest discover -s tests -q
python -B scripts/smoke_test.py
python -B scripts/writing_lookup.py --catalog ai-spec "零样本" --kind technical_term --limit 1 --format ids
python -B tools/render_writer_atlas.py --output-dir docs --check
node --check tools/check_writer_atlas.mjs
```

Browser dependency setup and the explicit rendering command are in the
[design decision](designs/adr-001-ai-writing-spec.md#verification-and-maintenance).
The generated [HTML](writer-atlas.html) opens directly without a server;
[overview PNG](assets/writer-atlas.png) is included in the README. Browser PNGs
are environment-dependent; only generated HTML/SVG are byte-reproducible.

Local engineering criteria pass. No new blind writing comparison, independent
human review, Windows run, remote CI, performance benchmark, installation, version
bump, commit or push occurs. Native tests and synthetic contrasts are not
effectiveness evidence. Existing failed quality gates and experimental snapshots
remain unchanged; the next quality frontier is a frozen comparison on separate
materials measuring faithful terminology and reader-recoverable argument, not
only rule compliance. This standalone repository does not run the separate Forge
catalog audit or claim that the larger skill catalog passes governance.

### Abstract-only transfer confirmation (2026-10-11 to 2026-10-12)

The [six-paper confirmation](abstract-transfer-evaluation.md) completes twelve
pairs with the exact preceding candidate. Preferences are candidate 10 / baseline
6 / tie 8. Both sample strata and four paper strata net favor candidate, with two
unanimous candidate pairs, but one Neural ODE pair unanimously favors baseline.
The predeclared continuation gate fails; no threshold change or runtime promotion.
All 48 source-audit judgments pass fidelity, critical support and reader grounding
equally in both versions, not an advantage in those channels or human validity.

| Gate | Observed local evidence |
| --- | --- |
| Artifact integrity | 36 original responses / 96 byte-identical copied files; 134 frozen/input/raw hash entries checked against the complete local workspace; public checker explicitly omits unavailable source bytes |
| Source boundary | Six bodies reproduce 32 original raw-extraction spans totaling 206,896 bytes with two-LF separators; PDFs, full bodies, metadata and recipes remain local |
| Static checks | Skill frontmatter, new Python compilation, browser JavaScript syntax and diff whitespace checks pass |
| Focused infrastructure | Fourteen new helper tests plus five new archive/link tests pass; duplicate IDs, source/question drift, missing assessments, booleans as scores, fidelity risks, budget violations and missing directories have negative coverage |
| Regression | Python 3.14: 185 tests, 184 passes and one unavailable-PowerShell skip; eleven CLI smoke cases pass; prior control/relation/broad helper suites pass 10 / 10 / 13 tests separately |
| Data safety | No PDF or publisher body distributed; bounded credential-pattern scan and entry-point links are recorded separately; no new dependency, external SDK or paid-API runner |
| User journey | 1440px desktop / 390px mobile, all 36 displayed raw strings and every pair's layout verified; paper/sample filters, details and no-overlap pass; both screenshots inspected |
| Remaining checks | No new Windows or remote CI, official-template compilation, Word-client visual review, human judgments or performance claim |

The helper fixtures test software logic, not fresh writing quality. Archive tests
fail with missing artifacts before copying and pass with the complete archive;
no tests or cases are deleted or skipped to make the result pass. One untouched
FlexGen shared initial is 203 words against a 200-word ceiling; both final versions
are in budget. All other generation/note fields, assessment budgets and literal
witness checks pass. No extra revision, response repair, padding, judge replacement
or favorable-result selection occurs.

SAM uses the allowed arXiv v1 after blocked official access, without verified
final-publication equivalence. DreamBooth/Toolformer supplements and Neural ODE's
absent cited appendices remain unchecked; extraction defects and incidental
excluded-text exposure are disclosed. Writer questions are withheld, while
prompt restrictions are not OS isolation or proof of absent scientific recall.
The default writing guide, imported pins, installation, version and model weights
are unchanged. This is a completed local test/archive, not a release or push.

The first public-link check incorrectly treats eight existing directory links
as missing files. A failing directory fixture reproduces the defect; the corrected
checker distinguishes files/directories and still rejects nonexistent targets.
Only that non-generation helper and its derived copied-file hash are updated in
both local/public copies, with old/new hashes recorded in the
[verification receipt](../evals/abstract-transfer/verification_receipt.json).
All 134 frozen/input/raw entries remain unchanged. The final bounded scan covers
fourteen entry points, 192 file links and eight directory links, and 102 public
archive files including the derived receipt; no credential-pattern match or PDF.
This is not remote-link availability, fragment validation or a security proof.

### Evaluator controls and operative-relation follow-up (2026-10-11)

The [synthetic calibration](evaluator-control-calibration.md) completes twelve
original pairs. All 18 defective-pair preferences favor faithful prose; fine
auditors detect all 18 critical defects with no false flag in 30 faithful/neutral
judgments. Every prespecified admission criterion passes. Coarse fidelity also
detects false metric claims even when readers correctly reject the contradiction;
successful reader recovery is not true writer prose. This is calibration only,
not writing improvement or human validity.

The separately frozen [two-paper follow-up](operative-relation-evaluation.md)
completes twelve pairs and twenty-four final passages. Overall preferences are
candidate 5 / baseline 5 / tie 14; abstract votes are 4 / 0 / 4, but Methods and
Results do not favor the candidate. All 48 body-only audit judgments mark fidelity
pass and the bounded critical objective supported in both conditions. No overall
gain or runtime promotion follows. Same-family recall, purposive sampling,
within-paper contamination and clustered assessments remain limitations.

| Gate | Observed local evidence |
| --- | --- |
| Artifact integrity | Controls: ten unchanged raw files / 45 copied files. Follow-up: 24 raw / 75 copied files and all 58 frozen input/hash entries unchanged |
| Source boundaries | Three N1 and nine N2 original byte spans reproduce the selected bodies exactly; PDF/extraction/body hashes pass; publication body remains local |
| Static metadata/code | Skill frontmatter, Python compilation, browser JavaScript syntax and diff whitespace checks pass |
| Focused infrastructure | Ten control-helper tests, ten follow-up-helper tests and six repository archive tests pass; fixtures are not semantic judgments |
| Regression | Python 3.14: 180 tests, 179 passes and one unavailable-PowerShell skip; all eleven CLI smoke cases pass |
| Data safety | No PDF, full extraction or publisher body in either public archive; bounded secret-pattern scan finds no credential match; no new dependency or paid-model runner |
| User journey | 1440px desktop / 390px mobile, all 24 control and 36 follow-up displayed prose strings match raw text; filters/details/non-overlap pass and screenshots are inspected |
| Compatibility and remaining gaps | No new Windows/remote CI, official-template compilation, Word-client visual check, human review or performance claim; existing portable suite is local evidence only |

Follow-up retains a 181-word baseline Results against a 180-word ceiling and a
20-word candidate reader witness against an 18-word limit. Assessment answer/reason
budgets pass; no raw repair, drop, extra revision or judge replacement occurs.
Controls have no assessment-budget or witness deviation. Helper suites reproduce
infrastructure on temporary fixtures, not fresh model judgments. The original
duplicate-ID test fails before correction and passes afterward; both sets of
archive tests fail while their archive is absent and pass after complete copying.

N2's publisher access is blocked; an allowed author version is used with revision
and publication-equivalence uncertainty retained. Omitted local source bytes are
required for the full original-input check. The public follow-up byte verifier
explicitly does not claim to check those omitted inputs. Existing imported pins,
licenses, capabilities, installation and skill version remain unchanged. This
round is not a commit, GitHub push, remote release or complete writing-quality gate.
The final bounded link check verifies 135 local file destinations in twelve public
entry points, not remote availability or Markdown fragment targets. The secret scan
covers 133 files before the derived receipt is added; it is not a security guarantee.

### Broad revision and prose-only reading (2026-10-11)

The [broader evaluation](broad-writing-evaluation.md) completes twelve papers,
six domains, three samples and three units, with 108 paired units and 216 final
passages. Both conditions receive the same initial draft/notes/body and one
revision with equal budgets. The candidate bundles read-back and measured-event
guidance; their individual effects and the full skill pipeline are not isolated.
Anonymous votes are candidate 12, baseline 20 and tie 184: no overall gain.

Two source-free reader contexts per domain reconstruct final prose; separately
grounded auditors evaluate fidelity and core/scope recovery. Primary core scores
are all maximal, a non-discriminating ceiling rather than quality evidence.
Primary auditors in three domains report excluded-PDF text visibility, so six
fresh text-only auditors assess all 216 passages. Their results remain separate,
not substituted for primary labels or pooled as independent evidence. Both
rounds have one concern per condition, but differ on specific texts. Same-family
model recall, within-domain clustering and human independence remain limitations.

All 432 prose/note fields meet budgets. Twenty-two reader answers and three
reviewer reasons exceed their assessment budgets; one reader witness has a
literal capitalization mismatch. Raw responses are retained without repair.
Source versions, the pre-generation P02-to-P13 download replacement, publication
rights, extraction warnings and supplementary-registration timing are explicit.

Python 3.14: 174 repository tests, 173 passes and one unavailable-PowerShell
skip; 11 CLI smoke cases and thirteen separate experiment-helper tests pass.
Frontmatter, compilation, byte receipts and diff whitespace checks pass.
Playwright checks desktop/mobile rendering, raw-prose identity, both audit rounds,
filters, details and non-overlap. These verify infrastructure, not prose scores.
No runtime-guide, imported-pin, installation, version, model-weight, commit,
remote-push or template-compilation change is claimed for this round.

### Prose read-back revision (2026-10-11)

The [revision pilot](readback-revision-evaluation.md) compares one equal-budget
revision of each shared initial draft, isolating the new argument-guide section.
Two fresh initial writers, four editors, two reversed-order anonymous reviewers
and a separately grounded source auditor use two previously unused documented
paper cases. Two pairs unanimously favor the candidate, one the baseline, two
tie and three disagree. All initial, revised and note budgets pass. The source
auditor flags one passage per condition, including a preferred candidate's
outcome-definition ambiguity. No stable abstract or overall improvement follows.

The guide remains equal to its frozen candidate snapshot. Matrix/build/rewrite
routing is outside this isolated test. After source auditing, Results guidance
and abstract preflight additionally distinguish measured final-stage outcomes
from joint trajectory completion; that post-pilot addition is outside this
pilot. The later broad experiment tests it only in a bundle, without an
isolated-effect or overall-gain result. Source PDFs/bodies are not redistributed.
Raw prose is not repaired.

Python 3.14: 174 tests, 173 passes, one unavailable-PowerShell skip; 11 CLI smoke
cases pass. Frontmatter, archive-helper compilation, local-source and original
output hashes, public copy fidelity, reversed packet order, schema/budget checks
and documentation targets pass. No new runtime capability, imported pin,
installation, version bump, remote push or template compilation is claimed.

### Real-body explanation follow-up (2026-10-10)

The argument-transfer guide adds selected Methods observations and an
operation-to-consequence drafting step. The
[real-body pilot](body-argument-transfer-evaluation.md) compares eight units from
two CoRL papers with two fresh writer contexts per condition. Three pairs
unanimously favor the candidate, one favors the baseline, two tie and two have
reviewer disagreement. All sixteen passages meet frozen budgets; model prose
reviewers and a separate source auditor mark them fidelity-pass. Mixed replicate
outcomes do not establish stable writing improvement.

Post-pilot matrix guidance checks whether compression preserves the actual
operation and whether comparison populations or sampling weights change.
Those additions are not part of the evaluated guide-only intervention. Source
PDFs and body text stay local; repository artifacts preserve untouched outputs
and exact source receipts without redistributing third-party prose.

Python 3.14: 174 tests, 173 passes and one unavailable-PowerShell skip; all 11
CLI smoke cases pass. Frontmatter, frozen receipts, artifact consistency and
whitespace checks pass. No executable runtime, imported pins, installation,
version metadata, template compilation or remote publication changes.

### Argument-transfer follow-up (2026-10-10)

The exemplar agent now hands off located writing choices, reader questions,
applicable author evidence and prose actions instead of bounded paper summaries.
The existing dossier, rationale matrix, build and rewrite routes carry those
choices through to a final-text check. Fixed move counts and rewrite ratios are
not proof of learning; abstract lexical contracts are optional diagnostics, not
an entailment or argument-quality gate.

The [isolated-context pilot](argument-transfer-evaluation.md) generates three
synthetic abstracts and three Results paragraphs per condition, without editing
responses. Two anonymous, reversed-order reviewers give one candidate preference
and eleven ties; there is no unanimous directional preference or established
general improvement. Public raw artifacts preserve disagreements. A separate
worked example uses already-computed regression results and is explicitly a
teaching comparison, not blind evaluation.

Python 3.14: 174 unittest cases, 173 passes and one unavailable-PowerShell skip;
11 CLI smoke cases pass. Skill frontmatter and diff whitespace checks pass.
No runtime capability, imported pin, installation or version metadata changes;
no new template compilation or remote publication is claimed.

### Abstract contract gate (2026-09-20)

Added `tools/check_abstract_contract.py`, a configurable pre-review admission
check for abstract word range, required source-backed anchors, and explicitly
forbidden claim upgrades. The embodied round-2 candidates pass with 157, 153,
and 152 words respectively. This gate checks declared constraints only; it is
not an entailment checker, language-quality score, or acceptance predictor.
The checker normalizes line breaks before phrase matching and has regression
tests for both passing and failing contracts.

### Abstract source-fidelity follow-up (2026-09-18)

The guide now distinguishes heterogeneous baseline training regimes, preserves
supported design rationale without claiming isolated causality, permits both
method-first and gap-first openings, and makes word-budget/source-access
differences explicit in comparisons. Three new synthetic calibration pairs bring
the collection to eleven. Existing integrity tests exercise their schema and
oracle consistency, not model behavior. The real-paper evaluation report records
the OFT baseline-condition error missed by both judges; raw outputs are unchanged.

Verification: Python 3.14 ran 164 unittest cases (163 passed; one unavailable
PowerShell skip) and all 11 CLI smoke cases passed. The frontmatter validator
passed under system Python with PyYAML. Homebrew Python lacked PyYAML for that
validator. The earlier default-Python full-suite failure was reproduced under
Python 3.9.6: distribution tests hit the documented Python >=3.10 requirement.
Switching only the test interpreter to 3.14 resolved it; no distribution code,
dependency pin, global environment or installation was changed. The diagnostic
`Import failed: changed pin` also appears in the passing run and is not itself
evidence of a failed test.

No fresh blinded generation test, publication, installation or version bump was
performed. This is a bounded editorial update, not demonstrated writing-quality
improvement or a release certification.

### Claim-scope alignment (2026-09-14)

The [claim-scope diagnostic](claim-scope-evaluation.md) tests completed-results,
proposal and encoding-only evidence boundaries. Six fresh synthetic abstracts
all parse and meet their budgets. Judges tie the completed case; the other two
cases each have one judge tie and one directional preference. This is diagnostic
evidence only, not a general quality or acceptance result.

### Contribution-priority alignment (2026-09-13)

The [synthetic priority diagnostic](contribution-priority-evaluation.md) accompanies
alignment of conflicting single-contribution/five-sentence instructions with the
abstract guide. Three probes produce six untouched abstracts; both versions follow
explicit priority changes, but both still include a desired unestablished objective
in an evidence-only abstract. No general quality gain is established. The existing
eight calibration pairs remain separate from these three generation probes.
Verification:164 unittest cases,163 pass and one PowerShell skip;11 smoke cases;
compilation, frontmatter and diff checks pass. Guard schemas and runtime behavior
are unchanged; no publication or installation occurred.

### Evidence preservation follow-up (2026-09-13, round 3)

The [two-paper repeated-sample test](embodied-writing-round3.md) compares the
preceding candidate with focused evidence-preservation guidance. Eight raw
generations yield eight abstracts and eight experimental passages; all parse
as JSON and meet word budgets without repairs or retries. Both judges prefer
the new Octo abstracts in both samples. FAST preferences vary, including an
experimental co-contribution omission in the second new sample. This is mixed
evidence, not an overall quality gain. The two additional synthetic calibration
cases bring the collection to eight; a fresh evaluator matches both new oracles.
Those observations do not prove improved arithmetic or uncertainty retention in
generation. Source and packet exposure limits are explicit in the report.

Python 3.14 verification: 163 unittest cases, 162 passed and one unavailable
PowerShell skip; 11 smoke cases; compilation, upstream reproduction, frontmatter
validation and whitespace checks passed. Runtime capabilities, imported pins,
activation description and distribution version are unchanged. No publication,
global installation or remote CI validation was performed.

### Evidence allocation update (2026-09-13)

The writing references now distinguish co-contributions from supporting detail,
scientific claim boundaries from unresolved author queries, and embodied
evaluation units and transfer settings. Results-mapping examples no longer imply
that an ablation isolates causality or that counted FLOPs establish runtime.
No executable capability, imported resource pin, global installation or version
metadata changes. The calibration collection now contains six synthetic cases.

Observed local checks: 163 unittest cases (one PowerShell-unavailable skip),
11 inherited smoke cases, Python compilation, upstream resource reproduction,
skill frontmatter validation and diff whitespace checks passed. A fresh-context
model evaluator, without fixture oracles, matched all six declared calibration
preferences and fidelity labels, including the tie. This is evaluator calibration,
not six independent tests of generation improvements. The fixture tests remain
schema/integrity checks, not semantic scoring.

The preceding two-paper writing pilot is development evidence: its learned-guide
condition lost a co-contribution on one abstract and improved evidence selection
on the other. It did not evaluate this patch. Fresh embodied writing comparisons
are recorded in [the embodied evaluation report](embodied-writing-evaluation.md).
Across three papers, two reversed-order model judges tie all three abstracts,
prefer old experimental prose on two papers, and tie the third. One new response
fails raw JSON parsing; a derived parse preserves its prose. Source auditing also
catches an old numerical author-query error and an unsupported ablation workload
attribution missed by both judges. The update has not demonstrated overall
writing improvement; do not infer superiority from the synthetic cases. Intake
leakage and judge-protocol deviations are disclosed in the report.

### Abstract decision update (2026-09-11)

The local abstract guide and 24 original exemplar notes add contribution-first
selection and separate factual fidelity from argument quality. Three synthetic
calibration cases cover a valid contribution omission, an overstated theoretical
guarantee, and a defensible tie. Their oracles are expectations, not observed
model results. `test_abstract_calibration.py` checks fixture integrity only.
No independent forward-test of this update or acceptance/quality gain is claimed.
Use new held-out topics and hide the oracles when running a model evaluation.
Runtime permissions and executable resources are unchanged; references and
fixtures are local text. Publication and global installation remain separate.

Local verification on 2026-09-11: Python 3.14 ran 163 tests successfully with
one PowerShell-unavailable skip; upstream resource reproduction and diff checks
passed. The skill-creator frontmatter validator passed using the system Python
with its existing PyYAML. The first suite attempt used the system Python below
the distribution's 3.10 minimum and failed version gates; no requirement was
weakened to make it pass. Exemplar links and calibration schema checks do not
establish semantic quality. Release assessment remains CONDITIONAL pending
independent behavioral evaluation; no publication or global install was done.

Run from the source checkout with Python 3.10+. The portable suite uses the
standard library and temporary fixtures; it needs no model or paid API.

| Command | Evidence | Not established |
|---|---|---|
| `python3 -m compileall -q scripts tools tests` | Python syntax compilation | Runtime correctness |
| `python3 scripts/smoke_test.py` | 11 inherited synthetic CLI cases | Every workflow path or writing decision |
| `python3 -m unittest discover -s tests -v` | Distribution, installation, portability, privacy, document preservation, policy wiring and example regressions | Agent-level writing quality |
| `python3 examples/knn-regression/experiment.py` | Recomputed deterministic experimental summary | Real-world generalization or significance |
| `python3 tools/render_examples.py --output-dir build/rendered-examples` | PDF/Word export; text, reference, font and overfull-box checks | Every document client's rendering |
| `python3 tools/check_template_compatibility.py --output-dir build/template-check` | Eight pinned official-template fixtures, including two citation modes and a distinct rebuttal | Complete submission compliance |
| `python3 tools/import_writing_library.py --check` | Reproduce 130 cards, 16 protocols / 30 variants, five tables and licenses from pinned inputs | Citation entailment or completeness of terminology |
| `python3 tools/check_table_templates.py --output-dir build/table-check` | Five generic tables in single-column and two-column full-width layouts; ten synthetic PDF fixtures | Official-format compliance, narrow-column fit or real experimental results |
| `python3 scripts/pdf_layout_check.py paper.pdf --log main.log` | Snapshot hash, physical-page bounds, font embedding and optional log check | Visual quality, anonymity or source-to-PDF build provenance |
| `python3 tools/build_release.py` | Allowlisted ZIP, manifest and archive checksum | That an arbitrary download matches without checking its hash |

The document commands require Pandoc, pdfLaTeX, BibTeX and Poppler. The explicit
template command downloads style archives; the separate importer downloads
pinned public corpus inputs. Template SHA-256 pins, official
links and allowlists are in
[`sources.json`](../tests/fixtures/templates/sources.json). CI runs four portable
platform/Python combinations and a separate Linux document job. Inspect the run
for the commit in question; a badge is not a manuscript audit receipt.

For the Ubuntu document environment, install the explicit dependencies below
after updating the package index. The separate `lmodern` package supplies the
LaTeX font support required by Pandoc; OpenType fonts alone are insufficient.
`texlive-science` supplies the `algorithm` and `algorithmic` packages required
by the unchanged ICML style.
`cm-super` supplies Type 1 fonts for the unchanged ECCV style's T1 encoding.
Its metrics match the original Computer Modern family; see the
[font package description](https://ctan.org/pkg/cm-super).

```bash
sudo apt-get install -y --no-install-recommends pandoc texlive-latex-extra texlive-fonts-recommended texlive-science lmodern cm-super poppler-utils
```

## What the New Examples Test

- **Empirical study:** recompute all 20 measurements, independently aggregate
  means and sample standard deviations, and compare every rounded table result
  with the Markdown, PDF text and Word XML. Direct kNN oracles cover ties,
  extreme neighbor counts and extrapolation behavior.
- **Theory note:** exact-rational finite cases check the stated range bound;
  signed-weight and inaccurate-average counterexamples check its limits. These
  cases do not prove a theorem; the accompanying elementary proof is separate.
- **Reviewer response:** the response explicitly distinguishes completed
  wording changes from an unrun baseline. Export and structural guards run on
  it. There is no automated test proving that arbitrary reviewer responses are
  persuasive or scientifically sufficient.

The three new PDFs have 3, 2 and 1 pages respectively in the published build.
Sources and seeds are public. Data are synthetic; table values are actually
computed, not hand-invented. The earlier `synthetic-study` example remains a
separately labeled, hand-authored arithmetic fixture.

These are AI-assisted worked demonstrations checked against their inputs, not
independent blind evaluations. No private manuscript or third-party full paper
is distributed. PDF previews are generated from the actual documents.

## Official Template Boundary

| Pinned template | Citation mode | Fixture checks |
|---|---|---|
| ICML 2026 | Author-date | Compilation, citations, table/equation references, hidden identity sentinels |
| ICLR 2026 | Author-date | Same bounded checks |
| CVPR 2026 | Numeric | Same bounded checks |
| NeurIPS 2026 main review | Author-date and numeric, separately compiled | Same checks; explicit natbib mode retained |
| ACL style, used by ACL/EMNLP 2026 | Author-date | Package-selected bibliography; separate long/short profiles |
| ECCV 2026 main review | Numeric, LNCS | Unchanged class/style; no CVPR font substitution |
| ECCV 2026 rebuttal | Numeric, two-column | Distinct template; one total page and no external URL in fixture text |
| AAAI 2026 | Not locally verified | Guide-only profile; official kit returned HTTP 403 |

The source tool verifies archive hashes, reads only named style files in a
temporary directory, disables shell escape, and verifies that style bytes remain
unchanged. Regression fixtures reject changed hashes, duplicate/missing members,
symlinks, oversized members and non-flat output filenames. This is not an OS
sandbox; TeX and its packages remain executable dependencies.
MiKTeX builds explicitly disable automatic package installation. Template tests
also invoke the PDF receipt tool; no word bounding box may escape the physical
page and fonts must be embedded. These are not content-margin or readability
proofs. Type 3 and image-only pages require inspection rather than a universal
policy verdict. The file-hash receipt identifies inspected bytes; it does not
retroactively certify other versions.

The Word companions test numeric/author-date recognition and content/font guards.
They are **not official Word submission templates**. Fixtures do not test every
page-limit rule, supplemental/appendix convention, track, camera-ready mode or
disclosure policy. Supply current official requirements for the actual target.
No endorsement by these conferences is implied.

## Policy and Safety Regressions

Section count defaults to an advisory; an explicit positive `max_sections`
enforces a project budget. TeX comments, appendices and bibliography material are
excluded from that count. Citation collection size and recency are suggestions
unless `citation_enforce_heuristics=true`; empty banks and malformed rows still
fail, including records beyond the suggested collection target. This changes
heuristic severity, not evidence requirements.

Natural-expression heuristics are likewise advisory unless
`humanize_enforce_heuristics` is exactly JSON `true`. Matrix structure and required
dimension coverage remain checked. A truthful audit need not invent a
high-severity defect. Ten authored expression cases check declared protected
spans; no automated test here proves arbitrary semantic preservation.

Citation privacy tests intercept network calls: manuscript-support fields cannot
become fallback search queries. Global preference setup cannot rewrite project
config, and Word `--fix-fonts` preserves `word/document.xml` exactly. These are
bounded regressions, not a universal security claim. See [SECURITY.md](../SECURITY.md).

English and Chinese citation verification inspect the first Markdown table in a
support bank. Keep citation records in that table; later tables are not silently
interpreted under its column labels.

## Remaining Limits

- `progress_check.py` primarily inventories stage artifacts. Contribution,
  results-validation and reviewer-audit guards run in the final gate but are not
  independent progress stages. Old PASS files are not content-addressed receipts;
  rerun guards after changes to any checked input.
- LaTeX guards recognize some included labels but do not expand every macro or
  audit all prose in every included file. Compile and inspect the whole document.
- Known bibliography styles are recognized, not every future year or custom
  template. Resolve unknown styles without overriding official requirements.
- DOI/metadata matches do not prove that a source supports a sentence. Citation
  entailment, experimental fairness and numerical interpretation need review.
- Word checks inspect structure, text and fonts. Open the document in the target
  client to review equations, figures, pagination and layout.
- Style and reviewer-independence text heuristics do not establish human
  authorship, detector outcomes, novelty or reviewer agreement.
- `evals/activation.json` defines routing cases; schema validation alone does not
  execute them against an agent. A writing-quality benchmark needs held-out raw
  inputs, blinded scoring, negative cases and reported failures.

The 11 profiles cover eight named venues at specific 2026 stages. Additional
years, camera-ready stages, verified AAAI compilation and independent writing
evaluations remain future work. A test suite does not complete those tasks.

## Local 1.3.0 Release Check

Observed on 2026-09-07, macOS / Python 3.14.3, MiKTeX pdfTeX and Poppler.
This is a local receipt; inspect the exact GitHub commit/tag for remote CI results.

| Check | Observed result |
|---|---|
| Full portable suite | 161 tests: 160 pass, one PowerShell test skipped because the executable is absent locally |
| Inherited smoke suite | 11/11 pass; Python compilation passes |
| Added resource contracts | 15 focused tests pass, including every alias and all 30 variants, complete warnings/checks, small-budget refusal, card availability, paths/hashes, import failure before writes and synthetic fixture scope |
| Distribution | Full manifest equality, deterministic rebuild, installed lookup outside the skill directory with spaces and network audit hooks; missing CC0/MIT notices rejected |
| Upstream reproduction | All nine pins verify; 130 cards, 37 source records, 16 protocols / 30 variants, five adapted tables and licenses reproduce exactly |
| Preservation | All 127 previous cards and all 37 source records are unchanged; precisely three sentence-pattern IDs added |
| Table compilation | Five tables x two layouts, ten one-page PDFs; embedded fonts, text bounds, no overfull boxes or unresolved placeholders |
| Visual inspection | Five distinct table renderings inspected; the ten final previews match the inspected single/full-width renderings byte-for-byte |
| Metadata and docs | Skill validator, CFF 1.2.0 schema/version and YAML checks pass; 201 relative file/image links checked; 14 unique activation expectations |

The table fixtures use arbitrary synthetic numbers solely to test rendering.
The separate protocol-application example uses the existing measured synthetic
regression results. Neither is an answer-withheld writing evaluation. The three
new activation expectations are declared behavior, not measured activation rates.
Existing official-style fixtures remain in the Linux CI job alongside the new
table check; this extension adds no official venue coverage or Word-client visual
certification. Tool-environment dependencies were not installed globally.

## Local 1.2.0 Release Check

Recorded on 2026-09-06. The previous release record below is historical.

| Check | Observed result |
|---|---|
| Full suite, Python 3.10.19 and 3.14.3 on macOS | 144 cases per interpreter: 143 passed, 1 skipped because PowerShell was unavailable |
| Inherited CLI smoke | 11 passed |
| New resources | Exact venue selection, no year fallback, bounded offline lookup, Chinese aliases, whole-card JSON budgets, provenance and license preservation |
| Corpus regeneration | 127 cards and 37 discovery-source records reproduce exactly from pinned inputs |
| Official templates | Eight cases compile, PDF citation modes and document guards pass, official styles unchanged; all nine rendered pages visually inspected |
| Existing worked examples | Three PDFs and Word companions rebuilt successfully; sources remain unchanged |
| Metadata | Skill validator, CFF 1.2.0 schema/version and YAML checks pass; 161 relative file/image links checked |
| Distribution | Real runtime and installed offline lookup/profile commands tested from paths containing spaces; missing corpus licenses block packaging |

The 48 added tests include negative cases for malformed PDF-tool output,
out-of-page text, citation-mode drift, changed download bytes, unreviewed corpus
records, missing notices and inappropriate heuristic blocking. Counts include
some methods with multiple subcases; they are not 144 writing-quality trials.
The old/new heuristic comparison reproduced a real v1.1.0 false rejection.
The Linux template job also exposed a citation-oracle false rejection when
TeX split `background` across lines as `back-` / `ground`. Its captured text is
a regression case; only line-break hyphenation is normalized, and wrong citation
modes still fail. This does not modify the official ACL style or the rendered PDF.
The Linux ECCV build then exposed missing Type 1 font dependencies: extracted
`fi`/`ffi` ligatures became XML-invalid `U+001C`/`U+001E` characters. A disposable
Debian 12 font probe reproduced this with Type 3 output; installing only
`cm-super` and rebuilding the same source produced Type 1 fonts with Unicode
maps and valid bounding-box XML. CI now installs that dependency explicitly.
The strict XML parser, original fixture prose and official styles remain unchanged.

No new model-based blind writing evaluation or Word-client visual certification
was performed. AAAI remains guide-only. Source-only document commands explicitly
disable MiKTeX auto-installation; see the release notes for the early discovery.

## Local 1.1.0 Release Check

Recorded on 2026-09-05 for the release candidate; remote CI is separate evidence
and must match the published commit.

| Check | Observed result |
|---|---|
| Full suite, Python 3.10.19 and 3.14.3, macOS 26.2 | 96 cases on each interpreter: 95 passed, 1 skipped because PowerShell was unavailable |
| Inherited CLI smoke | 11 passed; also repeated from an isolated installed payload |
| Three worked examples | PDF/Word guards pass; all six PDF pages visually inspected |
| Three pinned template fixtures | Compile and guards pass; all three rendered pages inspected; official styles unchanged |
| Metadata and public docs | CFF 1.2.0 schema valid, skill metadata valid, YAML parses, 104 relative file/image links checked |
| Distribution | Archive checksum and per-file manifest verified; installed files match the ZIP in a temporary path containing spaces |

The document environment used Pandoc 3.9.0.1, MiKTeX-pdfTeX 4.10 / BibTeX 4.1
(MiKTeX 22.1), and Poppler 26.03.0. PDF inspection caught an unwanted response
section number and an ICML fixture's visible `AUTHORERR` notice; both were fixed.
A new negative regression rejects that notice even if TeX exits successfully.
This illustrates why compilation alone is not a visual review.

No Word-client visual inspection or new blinded writing-quality evaluation was
performed for this release. Those limits remain explicit rather than being
counted as successful tests.
