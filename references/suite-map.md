# Suite Map

PaperSpine is a single orchestrator skill. Each stage reads its playbook from
`references/*.md`:

| Stage Playbook | Responsibility |
|---|---|
| `references/intake.md` | collect configuration |
| `references/research.md` | index local references, research target scene, and learn examples |
| `references/citation.md` | build citation support candidates |
| `references/rewrite.md` | rewrite an existing draft |
| `references/build.md` | build from a materials folder |
| `references/humanize.md` | reduce AI detection patterns via tiered stylistic constraints |
| `references/latex.md` | assemble and guard LaTeX |
| `references/translate.md` | produce complete translation_zh/ with row-by-row translation |
| `references/audit.md` | check completeness, integrity audit, structured review, and translation coverage |
| `references/update.md` | check and update local PaperSpine installs |
| `references/submission.md` | submission materials package |

> Historical worker skills (`paper-spine-ui`, `paper-spine-intake`, etc.) were
> removed in architecture convergence Stage 2b.  All stage logic now lives in
> `references/*.md` playbooks.

## Companion Skill Escalations

Sibling skills (installed alongside `paper-spine` in the suite) that specific
stages may escalate to. All are optional and additive — see the owning playbook
for routing and fallback rules:

| Companion skill | Owning playbook | Stage |
|---|---|---|
| `result-to-claim` | `references/contribution.md` | contribution evidence gate |
| `ablation-planner` | `references/contribution.md` | contribution evidence gate |
| `paper-figure` | `references/build.md` / `references/latex.md` | figure production |
| `paper-illustration` | `references/build.md` / `references/latex.md` | figure production |
| `ensemble-reviewer` | `references/audit.md` | final audit ensemble review |
| `rebuttal` | `references/respond.md` | conference rebuttal |

## Supplementary Deep-Revision Methods

These are detailed, optional sub-methods invoked from a stage playbook above, not
separate stages. Use them when the inputs they need (e.g. a deep-read journal
corpus) are available:

| Method | Invoked from | What it adds |
|---|---|---|
| `references/round1-literature-revision.md` | `rewrite.md` | motivation-thread extraction, move-guided section rewrite, numerical + cross-section audit |
| `references/round2-journal-revision.md` | `humanize.md` | CASPArS "Three R's" corpus-based style calibration + Style Conformity Checklist |
| `references/round3-latex-polish.md` | `latex.md` | template-first Markdown→LaTeX conversion + native-English polishing |
| `references/round4-template-integration.md` | `latex.md` | journal-template integration, compile-and-fix, content-integrity verification |
