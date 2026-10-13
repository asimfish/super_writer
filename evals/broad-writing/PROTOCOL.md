# Broad writing revision experiment

Frozen design, 2026-10-11, before test-body preparation or prose generation.

## Sampling and scope

Twelve purposively selected papers, two in each domain: robotics (Diffusion
Meets DAgger; ScrewMimic), efficient inference (FlashAttention-2; Speculative
Decoding), adaptation/training (DoRA; GaLore), language evaluation/retrieval
(Lost in the Middle; Self-RAG), vision/graphics (ConvNeXt; 3D Gaussian Splatting),
and uncertainty/theory (Conformal Risk Control; Adaptive Conformal Inference).
Verify titles/venues/official primary PDFs and prior documented exposure before
generation. If an input is unavailable or unsuitable, record the exclusion
and replace within domain before generating any prose, never by output quality.
FlashAttention-2 has family overlap with the previously studied FlashAttention;
do not call family-overlap cases fully held out. This is a broad curated sample,
not representative random sampling or unseen model-pretraining data.

Use complete relevant main-body Methods/Analysis and Experiments, with separately
located limitations where available; exclude abstracts, Introduction, summary
conclusions, acknowledgments, references and unrelated appendices. Preserve
unrepaired extraction, tables and mixed/adverse findings. Do not choose passages
to induce a desired win. Record PDF and input SHA-256, section boundaries,
page range and Poppler version. Metadata may expose author abstracts to source
preparers/coordinator; never use them as writer inputs or generated targets.

## Conditions and generation

Three fresh-context initial generations per paper. Batch only the two papers
within one domain per context and disclose that clustering. Each produces an
English abstract (150-200 words), one Methods/Analysis explanation (110-160),
and one Results interpretation (120-180), plus at most 120 words of notes per
paper. For empirical diagnostics, Methods explains the evaluation design;
for theoretical papers, explain a supported operation/guarantee and interpret
an informative worked example. No fabricated experiments or mandatory mechanism.

Each identical initial draft/notes/body goes to two fresh editor contexts, each
with exactly one revision response and the same budgets. Baseline uses the
pre-read-back argument guide plus pre-outcome-definition abstract preflight and
Results guidance. Candidate uses current counterparts, including prose read-back
and measured-outcome-definition guidance. Shared abstract and section guides
are identical. Freeze all snapshots before source preparation. This tests a
bounded guidance bundle, not separate effects, model training or full pipeline.

Eighteen initial contexts and thirty-six editor contexts produce 108 initial
and 216 final passages, yielding 108 paired units. All raw responses stay
untouched. No selection, padding, repairs or quality retries. Missing tasks,
schema errors, budget violations and operational interruptions are recorded,
not silently dropped. Task infrastructure may be repaired without rewriting
saved prose. Model family is inherited; no override, hidden SDK/API or paid
external evaluator. No global installation, publication or commit is implied.

## Three complementary outcomes

1. Preference: two fresh reviewers per domain see identical body evidence and
   anonymous pairs with reversed A/B order. No initial drafts, guides, notes,
   version labels or prior results. Judge source fidelity separately from
   contribution, argument, selection and language (1-5 ordinal), with a located
   A/B/Tie reason. Preserve disagreements and source-concerned preferences.
2. Prose-only understanding: two fresh reader contexts per domain see anonymous
   individual texts, generic questions appropriate to the unit, and no source,
   title metadata, anchors, guide, paired counterpart for the same unit/sample,
   or scores. Reconstruct contribution/operation/comparison and scope from text
   with a short located witness; say not recoverable when absent. Randomization
   balances conditions across readers. Readers can encounter other replicates
   of the paper; disclose within-domain context contamination. Model recall is
   not erased, so this is not a literal knowledge-free human experiment.
3. Source/understanding audit: independently source-grounded assessors inspect
   all final anonymous texts and reader reconstructions against actual source
   tables/conditions. No condition labels or preferences. Record fidelity
   pass/concern/fail, central-relation recovery and consequential scope recovery
   (0 absent/wrong, 1 partial, 2 recoverable). Score selected text functions, not
   mandatory inclusion of every available source fact. Distinguish missing text,
   reader inference and unsupported writer claims. Two short evidence anchors
   per unit are frozen by source preparers before generation; they aid grounding
   but do not mandate an exemplar's wording, result inventory or template.

## Analysis and stopping

Do not unblind until every planned preference response is saved or its failure
recorded. Report counts by paper, domain, unit and replicate; original source
concerns, budget/schema failures and missingness remain visible. Preference
votes and ordinal means are descriptive, not percentage quality gains. Average
signed preference (candidate +1, baseline -1, tie 0) within each paper before
summary; any bootstrap resamples papers within domain with a frozen seed and
reports conditional uncertainty only, not population significance. Report
understanding and fidelity separately; a stylistic win with a source concern is
not an unqualified improvement. Do not pool prior pilots. No after-the-fact
change to guide/anchors is credited to this test.

Complete generation, two reviews, readers and audit for all eligible papers.
Do not stop early for favorable outcomes. If a repeated operational blocker
prevents a phase, retain partial artifacts, exact planned/completed counts and
the named blocker without claiming the full experiment finished. Source PDFs,
body text, rendered pages and source-containing packets stay local; public
artifacts contain original generated prose, anonymous reader/reviewer/audit
responses, exact receipts, frozen guides and extraction recipes only.
