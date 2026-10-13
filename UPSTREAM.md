# Provenance

Super Writer is an adapted derivative of PaperSpine, extracted from the
Super Skill Team collection into a separately maintained public repository.
Standalone versions start at 1.0.0; this does not rename the upstream V4 release.

| Source | Revision / Path | Relationship |
|---|---|---|
| [asimfish/super_skill_team](https://github.com/asimfish/super_skill_team) | `2da7bebf8e84c7eb1065b4c61669650e336e9620`, `skills/paper/paper-spine/` | Exact extraction baseline, including local guard fixes and smoke regression |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | `d4529208cda72aa075767611b0265b95b709b550` | Upstream V4 methodology, playbooks, role cards, and script foundations; MIT |
| [c-narcissus/paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) | `77557418b4ca8c24fa8961206bf9b8f7f6d030e1` | Presentation reference for bilingual documentation, workflow explanation, examples, and release ZIPs only |
| [asimfish/super_translate](https://github.com/asimfish/super_translate) | `32cdaedf59b62ab05bedf3faef6c07cec872402b` | High-level README organization: artifacts, reproduction and verification boundaries; no imported content |
| [wanshuiyin/auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/auto-claude-code-research-in-sleep) | `e59008d7a42eea50a2797e55dd0d85bbbf6572f5` | High-level README organization: gallery, workflow and contribution routes; no imported content |

Baseline reviewed on 2026-09-05. The applicable upstream license was read at
[this pinned revision](https://github.com/WUBING2023/PaperSpine/blob/d4529208cda72aa075767611b0265b95b709b550/LICENSE).
Its original copyright and MIT permission text are retained in [LICENSE](LICENSE).
Super Skill Team local adaptations are included under the maintainer's authority.

No code, skill instructions, screenshots, example papers, diagrams, or ZIP contents
were copied from the figure-studio reference. Our documentation and synthetic
examples were written for this repository. There is no endorsement implied by
either reference project.

The additional README references were studied for organization only. No code,
prose, logos, screenshots, papers, performance claims or dependencies were copied.
Their licenses do not become this project's license through inspiration.

Official template sources and exact revisions/digests are recorded in
`tests/fixtures/templates/sources.json` in the source repository. Upstream styles
are downloaded into temporary directories for explicit compatibility checks,
not vendored or relicensed. Fixture prose, the minimal numeric CSL and example
manuscripts were independently written here.

## Selective Integration Audit: 2026-09-06

| Project / exact audited commit | Accepted integration | Deliberately excluded |
|---|---|---|
| [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra/tree/798f03a14ce582607ba2742d025691f226470641) | High-level dependency preflight, actual-PDF inspection, evidence-constrained revision and bounded stopping; independently implemented here | No code or paper-excerpt prompts copied. No ban on limitations, review-score acceptance surrogate, agent-cache scanning, API-key discovery or generic PDF builder presented as official |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine/tree/1fe46f0e76aab800db381b0a0c392cebe14d86bf) | Compared with the existing `d4529208...` baseline: no changed files in `src/skill/`. Retain contribution/rationale/evidence design; extend locally with contribution-specific blueprints | No claim of a new V5 runtime import. Do not restore universal numeric citations, hard citation quotas, elevated wizard launch or deletion of misplaced outputs |
| [shuorenhua](https://github.com/MrGeDiao/shuorenhua/tree/d2d0ce27da295581c3cf87a30ab65deb7d0ddfb8) | MIT method adaptation: mode/scope separation, protected semantic relationships, fidelity pass before residual prose pass | No casual-register transplant, mechanical word ban or silent removal of scholarly source gaps |
| [anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing/tree/d25ea080e1252ac2258cccc09519d138e4d2da63) | MIT method adaptation: classify caveats, lead with supported statements and preserve necessary precision | No removal of genuine uncertainty, real limitations, useful contrast or warranted acknowledgment of errors |
| [super_library](https://github.com/asimfish/super_library/tree/5a5c55c0e553fc11c6b2886a5fa1a3f6094108a7) | 127 CC0 original cards and 37 discovery-source metadata records; retain IDs, constraints and provenance; original offline lookup implementation | No upstream executable code, full papers, attested-collocation records, private data or claim of citation entailment |

PaperOrchestra's root license includes an additional notice about prompts
excerpted from its paper. We do not treat MIT as permission to republish those
excerpts, and import none. Its limitation-suppression rule conflicts with
research integrity and required ACL/EMNLP sections, so it is rejected.

Super Library distinguishes MIT software from CC0 original corpus records.
`tools/import_writing_library.py` verifies pinned index, selection-list and
data-license digests. `references/writing-library.json` records the exact inputs
and selection policy. `--check` reproduces the generated files without changes.
See [DATA_LICENSE](DATA_LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Writing Resource Extension: 2026-09-07

Rechecked Super Library at the same pinned `5a5c55c0e553fc11c6b2886a5fa1a3f6094108a7`
revision. v1.2 selected 127 cards; v1.3 adds three original related-work patterns
(embodied systems, RL regimes, and world-model generation/control), reaching
130 cards including all 78 reviewed sentence patterns. The 37 discovery-source
records are unchanged. This is not a claim of 130 conference templates.

Added all 16 writer-facing protocols and their 30 variants without rewriting
their data fields. Excluded the peer-review protocol and its two variants,
attested phrases and the upstream orchestration/task routes. Related IDs outside
the card selection remain explicit unbundled pointers. Required moves are
conditioned locally on present, missing or inapplicable author evidence.

Adapted five MIT TeX table skeletons with wrapped long headers and no manual
vertical spacing. The full table license is retained separately from CC0 data.
The importer pins all nine input files, verifies every input before writing,
and records both upstream and adapted table hashes. The offline protocol CLI
is independently implemented here; lookup never compiles or fills table cells.
The source-only renderer uses labeled synthetic fixtures in two layouts, not
real experimental findings or new official-venue compatibility claims.

These are selective integrations into one academic-writing skill, not five
bundled orchestrators. No companion is silently installed and none of these
projects is claimed to endorse Super Writer.

## Standalone Changes

- Publish as repository `super_writer` with discoverable skill ID `super-writer`.
- Make the entrypoint and intake/update guidance independent of monorepo paths
  and absent helper skills; keep all stage playbooks and 25 Python scripts.
- Preserve `paper_rewriting_output/`, `paper_spine_config.json`, Python helper
  module names, and legacy `PAPERSPINE_CONFIG_HOME` preferences for compatibility.
- Add bilingual onboarding, capability disclosure, activation examples, public
  synthetic materials, reproducible packaging, installation tests, and CI.
- Run the intake wrappers in the current terminal with literal arguments.
- Restrict citation API inputs to explicit bibliography fields, isolate global
  preference setup from project configuration, and keep font repair from
  changing document body content.
- Retain script-level `PaperSpine` names where changing them would obscure
  provenance or affect existing integrations.
- Recognize checked conference citation styles, make generic editorial budgets
  advisory unless explicitly enforced, and check all candidate citation rows.
- Add reproducible empirical, theoretical and response examples, real document
  builds, pinned template fixtures and open-source contribution metadata.

## Maintenance

### System organization presentation (2026-10-12)

The user supplied an image titled "Simplified Technical English: overview",
showing document structure, annotated sentences, verb forms, dictionary entries,
limits and history. Reviewed image SHA-256:
`ce0bdd73d436f7a4b63349be7f49484a7f6963dce89bfe15c0037952e5e2d07e`.
Its publication revision, author and redistribution license are not established;
there is no applicable upstream Git commit. Only its high-level explanatory
organization informs the original [system guide](docs/system-organization.md)
and bounded style-learning guidance. The image, layout artwork, sentences and
dictionary entries are not copied into the repository. No conformity to
ASD-STE100 or verification of its current rules is claimed, and its domain-specific
language limits are not adopted for papers.

This is an explanation of existing responsibilities and conditional learning,
not a new skill, model-training pipeline, rule database or measured writing gain.
Runtime scripts, schemas, dependencies, resource counts, imported pins and
licenses are unchanged. Experimental writing guides remain snapshots unless
separately evaluated and adopted; this documentation does not promote them.

### Abstract editorial synthesis (2026-09-11)

The abstract decision guide, exemplar notes, and synthetic calibration fixtures
are independent editorial synthesis, not imported paper text or executable
upstream code. The 24 publication titles, years, and direct source URLs are
listed in [abstract-exemplars.md](references/abstract-exemplars.md). Sources were
read on 2026-09-10; no upstream Git commit applies to these publication pages.
No full abstracts, figures, private manuscripts, or private evaluation outputs
are bundled. Linked publications retain their own copyright and licenses;
public availability is not treated as permission to relicense their content.
The repository license covers the original notes/fixtures, not the linked works.
The pinned Super Library protocol JSON and reproduction contract are unchanged.
These editorial hypotheses do not establish a measured effectiveness gain.

### Evidence-allocation refinement (2026-09-13)

Original guidance and synthetic calibration cases refine co-contribution
retention, author-query separation, and embodied evaluation units. The motivating
local pilot studied [DRIFT](https://www.roboticsproceedings.org/rss21/p159.pdf)
and [DDAT](https://www.roboticsproceedings.org/rss21/p078.pdf), reviewed on
2026-09-13; publication PDFs have no applicable upstream Git commit.
They are development cases, not fresh held-out evidence for this refinement.
No publication prose, figures, PDFs, private research, or raw author comparators
are imported. These are independently written editorial decisions and synthetic
examples; linked papers retain their copyright. Executable capabilities, imported
protocol pins, licenses, and the standalone skill owner are unchanged.

### Evidence preservation follow-up (2026-09-13)

The preceding embodied comparison is now development evidence for a focused
follow-up: preserve decision-relevant uncertainty, avoid redundant table narration,
verify numerical author queries, and scope sample counts to their experiments.
Sources and observed failures are recorded in
[the evaluation report](docs/embodied-writing-evaluation.md). These guidance
changes and two additional synthetic cases are original synthesis, not copied
publication prose. Runtime capabilities, upstream pins and licenses are unchanged.
No model-weight training, global installation or release is implied.

### Contribution-priority alignment (2026-09-13)

Original synthesis reconciles inherited single-contribution/five-sentence
instructions with the abstract decision guide. Existing contribution and rationale
artifacts now carry author-prioritized co-contributions and a retained-meaning
check, without new schema requirements. The accompanying three synthetic
counterfactual probes contain no publication text or real experimental claims.
The preceding FAST omission is development motivation, not proof of the cause.
No new capabilities, dependencies, imported licenses or upstream pins are added.

This repository is the owner of the standalone `super-writer` distribution.
The monorepo `paper-spine` entry remains a historical/compatible predecessor;
installing both can create overlapping routing and is unnecessary.

Review upstream changes as explicit patches with provenance, license, and test
evidence. Do not automatically overwrite this derivative from upstream HEAD.
# Argument Transfer Follow-up (2026-10-10)

The local argument-transfer guide and regression worked comparison are original
editorial synthesis. Three author abstracts were read to locate writing choices:
[DPO](https://arxiv.org/abs/2305.18290),
[PagedAttention](https://arxiv.org/abs/2309.06180), and
[Mirage](https://proceedings.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html).
Reading scope is abstract only; no full paper, source prose, executable code,
official template or experimental data is imported from these works. The linked
papers retain their rights. Source ideas guide rhetorical choices, not evidence
for a user manuscript. Existing imported corpus pins and notices are unchanged.

### Methods-to-explanation refinement (2026-10-10)

The subsequent guide revision additionally studies
[DPO section 4, equations 4-7](https://arxiv.org/pdf/2305.18290) and
[PagedAttention sections 4.1-4.3](https://arxiv.org/pdf/2309.06180).
These are selected Methods passages, not a full-paper correctness review.
Original editorial observations explain how an operation permits a consequence
and how a walk-through connects components. No source prose, figures, code or
PDFs are redistributed, and no source mechanism becomes a user-paper result.
The preceding abstract-only observations retain their narrower reading scope.

The subsequent body-only pilot studies
[Equivariant Diffusion Policy](https://proceedings.mlr.press/v270/wang25a.html)
and [ReMix](https://proceedings.mlr.press/v270/hejna25a.html) for evaluation,
not to compose the tested candidate guide. Exact official-PDF and extracted-body
SHA-256 receipts are in `evals/body-argument-transfer/source_receipts.json`.
After generation and quality judgments, their abstracts are read as editorial
references only. Full PDFs, body passages, rendered pages and author abstracts
remain outside the redistributed artifacts. Original generated outputs and
judgments are retained without repairs. Neither publication is a future unseen
case after this round; separate contexts do not exclude model pretraining recall.

### Prose read-back refinement (2026-10-11)

The new final-prose read-back check is original local guidance, motivated by
compression and comparison ambiguities in the preceding development cases.
It does not import a third-party skill, model, sentence library or executable
resource. The existing argument guide, rationale matrix and build/rewrite routes
remain the owners; no additional mandatory artifact or runtime capability is
introduced. Frozen-guide revision testing and source receipts are recorded
separately from this design claim.

The revision pilot uses
[Behavior Generation with Latent Actions](https://proceedings.mlr.press/v235/lee24y.html)
(ICML 2024) and
[Imitation Bootstrapped Reinforcement Learning](https://roboticsproceedings.org/rss20/p056.html)
(RSS 2024). The candidate argument guide is frozen before reading these test
bodies. The coordinator sees abstracts embedded in official metadata during
source discovery, but writers/editors receive only declared Methods/Experiments
and a separately extracted limitation passage. Exact official-PDF and body
hashes plus section boundaries are in
`evals/readback-revision/source_receipts.json`; Poppler 26.03.0 performs the
unrepaired extraction. PDFs, extracted publisher prose, source-grounding notes
and rendered pages are not redistributed or relicensed. Original generated
drafts, equal-pass revisions and judgments are evaluation artifacts, not a new
third-party template or language corpus. These papers are development data
after this round; context isolation does not rule out pretraining exposure.

### Broad revision evaluation archive (2026-10-11)

The [twelve-paper evaluation](docs/broad-writing-evaluation.md) adds original
generated prose, editorial anchors, anonymous judgments and infrastructure
receipts, not another imported skill, official format, sentence corpus, model or
runtime capability. Exact publication/version URLs and PDF/extracted-body hashes
are in `evals/broad-writing/source_receipts.json`. Reading spans declared complete
relevant Methods/Analysis and Experiments plus located limitations/supplements;
author abstracts and Introductions are excluded from writer/editor inputs.
Discoverers may see metadata abstracts. No linked publication is relicensed.

P02 ScrewMimic was unavailable after bounded download attempts; P13 ALOHA/ACT
replaces it before generation, not based on prose quality. P10 is explicitly
pinned to arXiv v1 after publisher download failure. Official ICLR proceedings
replace blocked OpenReview PDFs for P03/P08/P11; P11 download-finalization and
P13 extraction warnings remain in receipts. FlashAttention-2 family overlap and
related action-chunking concept exposure are disclosed. These twelve papers
become development cases after the round; model-pretraining exposure is unknown.

PDFs, full extracted publication prose, selected bodies, rendered pages and
source-containing packets remain outside the archive. The 72 anchors are
original editorial grounding aids, not quotations or mandatory author wording.
All 84 primary and six supplementary raw response files are copied unchanged.
Supplementary auditing does not replace the primary judges' concerns or permit
favorable label selection. A limited 21-token overlap diagnostic is not an
originality certificate. Existing imported pins, licenses, installed owner and
skill version remain unchanged; this round is not a commit or remote release.

### Evaluator controls (2026-10-11)

The [calibration archive](docs/evaluator-control-calibration.md) contains original
fictional evidence, prose, editorial labels and anonymous judgments, not excerpts
from papers, an imported skill or new scientific results. Two independent fixture
reviews precede assessment; their corrections are retained. All ten behavioral
responses are byte-preserved. No third-party license or corpus is added.

The existing blind-evaluation reference now separates consequential prose support,
source fidelity and reader-added information, with frozen sensitivity and false-flag
criteria. Passing synthetic calibration is not empirical writing improvement or
validation by independent humans. A narrow compression hypothesis remains a local
candidate, not automatically promoted to runtime guidance. Existing ownership,
imported pins, licenses, capabilities, installation and version remain unchanged.

### Operative-relation follow-up (2026-10-11)

The [two-paper follow-up](docs/operative-relation-evaluation.md) adds original
generated prose, six pre-generation editorial objectives, anonymous assessments
and byte receipts, not another imported skill, template or sentence corpus.
N1 uses the official PMLR PDF of Rudin et al.'s CoRL 2021 / PMLR 2022 paper.
N2 uses an explicitly authorized CMU author-hosted manuscript of Conformal
Prediction Beyond Exchangeability after blocked publisher access; its exact
revision and journal-version equivalence remain unverified. Actual version URLs,
hashes, source/encoding warnings and preparer exposure are preserved in
`evals/operative-relation/source_receipts.json`.

Selected inputs retain complete relevant main-body methods, theory, experiments
and proofs, with declared essential N2 Introduction definitions. They exclude
author abstracts and summary targets. Preparers encounter metadata abstracts and
section boundaries but no writing guides or prior outputs; writers/editors and
auditors receive only declared selected body evidence. No pretraining isolation
or source-version equivalence is implied. These papers become development cases.

All 24 raw responses and 75 copied files remain byte-identical. PDFs, full
extraction, selected publisher body, full metadata/boundary recipes and image
renders remain local and are not relicensed. The narrow candidate is an original
append-only hypothesis, not a promoted runtime rule: overall preferences remain
5 / 5 / 14 despite a local abstract signal. No imported pin, license, installed
owner, skill version, model weights or external publication changes.

### Abstract-only transfer confirmation (2026-10-11 to 2026-10-12)

The [six-paper confirmation](docs/abstract-transfer-evaluation.md) adds original
generated abstracts, anonymous judgments and receipts, not another imported skill,
template or sentence corpus. The candidate and baseline argument guides remain
byte-identical to the preceding pilot, and canonical writing guidance is unchanged.
VoxPoser, DreamBooth, Toolformer, FlexGen and Neural ODE use their assigned official
files. SAM uses the explicitly allowed arXiv v1 after ordinary OpenReview access
is blocked; final-publication equivalence is unverified. Missing supplements,
Neural ODE extraction defects, source versions and incidental excluded-text exposure
remain in [structured receipts](evals/abstract-transfer/source_receipts.json).

Writers never receive the independently frozen critical questions or author
abstract targets. Public artifacts preserve 36 response files and 96 copied files
byte-identically; PDF, raw/selected body, full metadata and extraction recipes stay
local and are not relicensed. The source/body assembly has 32 original byte spans.
The papers are now development cases, not fresh inputs for another tuned trial.

Preferences are 10 candidate / 6 baseline / 8 tie, but a unanimous baseline case
fails the frozen continuation gate. All factual/support labels pass equally;
no human gain, author-abstract equivalence or default promotion is established.
No imported pin, license, installation, version, model-weight or remote publication
changes occur. Existing unrelated working-tree changes are preserved.

### AI writing specification (2026-10-12)

The original [AI writing specification](references/ai-writing-spec.md) and
[engineering atlas](docs/writer-atlas.html) adapt the high-level distinction
between rules, dictionary senses, technical terminology, annotated contrasts
and inspectable boundaries. They are an independent MIT editorial synthesis,
not a copied STE dictionary, paper corpus, official conference standard or
ASD-STE100-compliant implementation. All examples are original and synthetic.
The separate 130-card CC0 library and protocol reproduction pins are unchanged.

The supplied [Karpathy post](https://x.com/karpathy/status/2105819303471976479),
dated 2026-10-02, was read in full through the
[FxTwitter public JSON mirror](https://api.fxtwitter.com/karpathy/status/2105819303471976479)
after direct X access returned HTTP 403; returned author and exact post ID were
checked. This is mirror retrieval, not direct verification of the live X page.
The post motivates understandable outputs and oversight, including controlled
writing, diagrams and HTML. It does not define an AI research standard or prove
that our implementation improves writing. Neither the post's full prose nor its
image is redistributed.

Primary public STE material reviewed: [About STE](https://www.asd-ste100.org/about_STE.html),
[official FAQ](https://www.asd-ste100.org/STE_faq.html) and
[download/copyright guidance](https://www.asd-ste100.org/STE_downloads.html).
Reading scope is those explanatory pages, some via indexed search content after
direct access failures; not the complete standard or its controlled dictionary.
The public About page identifies Issue 9 (January 2025). The FAQ distinguishes
general dictionary words from subject-field technical nouns/verbs and explains
the maintenance domain. Its treatment of `about` and `approximately` contradicts
the supplied screenshot: the image is not an authoritative rule source.
We do not copy its vocabulary or impose its numerical sentence limits, passive
restriction or `-ing` restrictions on research prose. Linked materials retain
their rights; no permission to redistribute the standard is inferred.

The initial six primary terminology-context references and actual reading limits are recorded
in [the catalog sources](references/ai-writing-spec.json): CLIP, LoRA, RLiable,
DomainBed and Tent abstracts, and scikit-learn's data-leakage/preprocessing guidance.
These support context-aware local distinctions, not universal definitions or the
user paper's empirical results. No source prose, PDF, table, code or dictionary
is imported. Web pages have URLs, review dates and read scopes, not invented
Git commits. No remote runtime requests, credentials, model training, global
installation, skill version bump, commit or publication is introduced.

The subsequent schema-2 expansion adds six primary references: the official
[NeurIPS checklist](https://neurips.cc/public/guides/PaperChecklist),
[GPT-3 v4 abstract](https://arxiv.org/abs/2005.14165v4),
[RAG v4 selected sections](https://arxiv.org/html/2005.11401v4),
[offline RL v3 abstract](https://arxiv.org/abs/2005.01643v3),
[ACT v1 Section IV/IV-A and algorithms](https://arxiv.org/html/2304.13705v1), and
[DPO v3 abstract and Section 4](https://arxiv.org/html/2305.18290v3).
The [research record](docs/research/ai-spec-expansion-2026-10-12.md) states actual
read scopes, editorial inferences, admitted IDs and deferred gaps. The live
checklist is not a pinned conference-year profile or certification. No full-paper
review is implied, and source observations are not authority for our synthetic
examples or user results. Original guidance is MIT synthesis; linked publications
retain their rights. No paper text, images, PDFs or dictionary is redistributed.

At the October 12 milestone the catalog has 53 records: 15 writing rules, 12 claim uses and 26 terms.
Eight topic facets and five writing levels do not alter the three canonical kinds.
Per-record source notes distinguish located context from local inference.
[Curated admission](references/ai-spec-learning.md) is a manual/agent workflow,
not a network-enabled runtime, scheduled crawler or automatic promotion engine.
New sources are development references, not unseen quality-test cases.

### Grounding and sequential evaluation (2026-10-13)

Seven primary references are added: [FActScore](https://aclanthology.org/2023.emnlp-main.741/),
[ALCE](https://aclanthology.org/2023.emnlp-main.398/),
[object hallucination](https://aclanthology.org/D18-1437/),
[explanation faithfulness](https://aclanthology.org/2020.acl-main.386/),
[CALVIN v2](https://arxiv.org/html/2112.03227v2),
[SayCan v2](https://arxiv.org/html/2204.01691v2), and
[MDETR v2 abstract](https://arxiv.org/abs/2104.12763v2).
The [research ledger](docs/research/ai-spec-expansion-2026-10-13.md) records selected
sections, the MDETR PDF retrieval failure/author-page fallback, local inferences,
deduplication and reviewer independence. No complete-paper or code audit is implied.

Fourteen original entries bring the catalog to 67 records: 18 rules, 15 claim
uses and 34 terms, with nine topics and five writing levels. Existing records
and pinned imported resources are preserved. The seven-domain taxonomy adds a
multimodal route currently represented only by vision-language examples.
The [worked cases](examples/ai-writing-spec/grounding-and-horizon.md) use invented
facts, including task-chain arithmetic; none reproduces a paper's experiment.
Original editorial synthesis is MIT; linked works retain their rights. No paper
prose, figure, PDF, code, official vocabulary or standard is redistributed.
These are development sources, not fresh held-out quality tests or evidence of
improved model generation. Runtime remains offline and read-only; no automated
crawler, model training, global install or publication is introduced.

## MARMOT STE Context Integration (2026-10-13)

Source: [MARMOTatZJU/SkillLibMARMOTatZJU, asd-ste100-writing-context](https://github.com/MARMOTatZJU/SkillLibMARMOTatZJU/tree/afd2875fe08cf5586dd0b2116b24190308c8b7db/skills/asd-ste100-writing-context),
commit `afd2875fe08cf5586dd0b2116b24190308c8b7db`, upstream skill 1.1.
All four bundled Markdown files and repository MIT license were read; retrieved
bytes match the Git tree blob IDs. The [review record](docs/research/marmot-ste-integration-2026-10-13.md)
contains hashes, scopes, ownership, security disposition and excluded controls.
The [MIT notice](references/marmot-ste-context.LICENSE) is retained unchanged.

This is a selective method adaptation: classify the passage's function, resolve
technical referents, and preserve preconditions/action order. The independently
written [academic clarity guide](references/clarity-context.md) and
[four contrasts](examples/ai-writing-spec/clarity-context.md) use original facts.
One rule is added, and the existing definition rule is extended rather than
duplicated. The local catalog now has 68 entries; the additional source record is
third-party skill context, separate from its 19 primary research/guidance sources.

Excluded: upstream Markdown instructions and compact rule database, official
dictionary statuses/rule-ID authority, maintenance sentence/paragraph ceilings,
universal voice/tense restrictions, response-wide style control and a restriction
to upstream-only resources. No complete official standard/dictionary was checked;
the source's underlying database was not provided. Its MIT license does not grant
rights to external standard content. No compliance, human domain-review result,
model training or writing-quality gain is inferred. No executable upstream code,
dependency, hook, secret read, autonomous network action, global installation,
commit or publication is introduced.
