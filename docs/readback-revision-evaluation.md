# Prose read-back revision pilot (2026-10-11)

## Question and intervention

The preceding pilot showed a planning-to-prose gap: correct working notes could
be compressed into method labels or ambiguous comparisons. The new
[argument-guide section](../references/argument-transfer.md#read-back-the-claim-before-checking-the-plan)
asks an editor to reconstruct the claim from prose before consulting the plan,
then check its strongest reasonable interpretation against the evidence and
repair the affected sentence. This is a semantic self-review, not a keyword
gate, trained model, independent reader or proof of comprehension.

The existing matrix, build/rewrite routes and SKILL entry now point to this
check. This experiment isolates the new argument-guide section; those other
workflow changes and a complete manuscript pipeline are not directly tested.
The candidate guide is frozen before reading test bodies. Prior Equivariant
Diffusion Policy/ReMix cases inform the change and remain development data.

## Sources and equal-pass design

- P1: [Behavior Generation with Latent Actions (VQ-BeT)](https://proceedings.mlr.press/v235/lee24y.html), ICML 2024, sections 3-4.
- P2: [Imitation Bootstrapped Reinforcement Learning (IBRL)](https://roboticsproceedings.org/rss20/p056.html), RSS 2024, sections IV-VI and the separately titled limitations passage.

Neither paper appears in the repository's preceding documented cases or
exemplar notes. This does not establish absence from model pretraining. The
initial venue assumption during discovery is corrected from official metadata
before body reading or generation, as recorded in the
[protocol](../evals/readback-revision/PROTOCOL.md). The coordinator sees abstracts
embedded in metadata pages but does not use them to compose the already-frozen
guide. Writers/editors do not receive them or browse. Introductions, summary
conclusions, acknowledgments and references are excluded. The coordinator reads
body material to define extraction boundaries. Poppler 26.03.0 extracts text
without repairing tables, equations or conflicting source labels.

Two fresh initial writers each generate an abstract and Results for both
papers using shared abstract/section guidance. Each corresponding pair of fresh
editors gets the **exact same initial draft, notes and evidence**, with one
revision response and identical final budgets. Initial writers do not use the
argument guide. Baseline editors use its preceding version; candidate editors
use that version plus the new read-back section. Both may use working notes.
This is revision versus revision, not an edited candidate versus an unrevised
baseline. It is also not the original writer revisiting its own hidden thoughts.

All contexts inherit the same model family and do not fork parent history.
Responses are saved unchanged, without selection, post-generation edits,
padding or retries. Abstracts must be 150-200 words, Results 120-180 and internal
notes at most 120. All eight initial units, sixteen revised units and twelve
case-level note passages meet their budgets. Length is not a quality score.

| Paper/sample | Initial abstract/Results | Baseline revision | Candidate revision |
| --- | --- | --- | --- |
| P1/1 | 184 / 135 | 167 / 140 | 178 / 148 |
| P1/2 | 167 / 146 | 173 / 136 | 169 / 137 |
| P2/1 | 176 / 145 | 169 / 140 | 170 / 133 |
| P2/2 | 160 / 124 | 171 / 134 | 165 / 124 |

Two fresh reviewers receive the same bodies and eight anonymous revision pairs,
with A/B order reversed (randomization seed 20261012). Initial drafts, notes,
guides, conditions and prior results are withheld. Contribution, argument,
selection and language use ordinal 1-5 ratings; fidelity is separate. Both
responses are saved before the coordinator decodes the mapping. A separately
grounded auditor checks sixteen anonymous texts against designated PDF body
pages/tables without condition labels or quality judgments.

## Anonymous preferences

| Pair | Reviewer 1 | Reviewer 2 |
| --- | --- | --- |
| P1/1 abstract | Tie | Tie |
| P1/1 Results | Candidate | Candidate |
| P1/2 abstract | Baseline | Baseline |
| P1/2 Results | Baseline | Tie |
| P2/1 abstract | Baseline | Candidate |
| P2/1 Results | Candidate | Candidate |
| P2/2 abstract | Baseline | Candidate |
| P2/2 Results | Tie | Tie |

There are two unanimous candidate preferences, one unanimous baseline
preference, two unanimous ties and three disagreements. Across sixteen votes:
candidate 6, baseline 5, tie 5. These are clustered judgments, not sixteen
independent experiments or a percentage quality improvement. Each editor covers
both papers, repeated revisions share a source and reviewers are same-family
models rather than humans. Do not pool counts with earlier drafting pilots.

### Located improvements

In P1/1 Results, the candidate keeps the aggregate sequence advantage but places
the contrary door-closing result beside the diversity observation. Its phrase
"The aggregate gain does not extend to every sequence" introduces the 6/10
diffusion versus 5/10 VQ-BeT comparison; both closing orders remain observable.
Both reviewers prefer this because diversity and success dominance become
distinct findings, not because another number appears.

In P2/1 Results, the baseline says Square ablations "distinguish this benefit"
immediately after Hang's improvement over cloning. Both reviewers mark that
baseline passage fidelity-concern: it may imply a mechanism explanation for
hardware that was only ablated in simulation. The candidate instead assigns
separate roles: "The ablations support both proposal mechanisms beyond actor
regularization, while Hang documents improvement over the reference policy
within the hardware budget." Both prefer it. This is a repair to the actual
inference, not an appended generic limitation. It remains a local model judgment.

### Failures and disagreement

Both reviewers prefer the baseline P1/2 abstract. It gives residual coding and
continuous refinement a shared purpose in representing alternatives while
preserving control precision. It also explains why all policies use closed-loop
control: receding-horizon execution fails on this robot. The candidate retains
the protocol name and numbers but loses that reason. The new self-review still
does not reliably preserve every consequential relationship in compression.

The IBRL abstracts split reviewers in both samples. Reviewer 1 values the
baseline's explicit function for controlled ablations beyond regularization;
reviewer 2 values the candidate's more explicit hybrid action choice and target
computation. These are substantive tradeoffs, not a consensus abstract gain.
One P1 Results pair also splits baseline/tie. No losing or tied output is repaired
or removed from the archive.

## Source fidelity and remaining limits

Quality reviewers mark every revised passage pass except baseline P2/1 Results,
which both mark concern for the simulation-to-hardware interpretation above.
The separate source auditor marks fourteen revised passages pass and two
concern, with no explicit numerical mismatches or fail labels. Each condition
has seven passes and one concern. It confirms the baseline P2/1 Results ambiguity
and additionally flags **candidate P1/1 Results**, despite both quality reviewers
preferring that passage and marking it fidelity-pass.

The candidate's "Final completion rates on each of four longer sequences"
may imply joint completion of all stages. The source reports end-of-task success,
but Table 6 does not unambiguously define joint all-stage completion; some
later-stage counts even increase. The numerical final-stage ratios support the
reported end-stage comparison, not an inferred trajectory-wide event. The other
drafts' narrower success-count/rate wording receives pass labels, but the source
reporting uncertainty itself remains. This is a consequential ambiguity rather
than an established arithmetic error. The adverse door-closing comparison is
supported; the whole preferred paragraph is **not** thereby cleared of concerns.

Thus one unanimous candidate preference remains source-concerned, while the
P2/1 Results repair is fidelity-pass. Raw preferences and audit disagreement are
preserved without rescoring or editing outputs. No pass certifies all claims.
The existing [Results guidance](../references/results-validation.md#check-what-the-metric-counts)
and abstract preflight now explicitly check the measured event before compressing
its name. This is a **post-pilot addition, not tested by this frozen-guide
experiment**. The later [broad comparison](broad-writing-evaluation.md) evaluates
it in a guidance bundle without establishing an isolated effect or overall gain.

The editors are instructed to put their plans aside, but no mechanism erases
source knowledge from a model's context. Notes and ratings cannot prove that
the requested internal step occurred. Reviewers also see source bodies and may
supply explanations absent from the prose. A fresh prose-only reader task and
human reading would more directly test recoverable understanding. The author
abstracts are not a scored condition; their authors had fuller source context.

## Artifacts and verification

The [archive](../evals/readback-revision/README.md) preserves exact guide snapshots,
initial generations, revisions, judgments, prompts with portable paths,
source receipts and anonymous displayed prose. Third-party PDFs, extracted
bodies, rendered pages and full source-containing review packets stay local,
outside this repository's redistribution/license boundary. Inputs and packets
can be reconstructed from official PDFs and archived extraction recipes after
checking their pins; model generations and preferences are not deterministic.

Python 3.14 runs 174 unittest cases: 173 pass and one unavailable-PowerShell skip.
All 11 CLI smoke cases, frontmatter and whitespace checks pass. Archived helper
compilation, frozen-source/generation hashes, exact public copies, reversed-order
packet consistency and all prose/note budget checks pass. These are software and
artifact checks, not a writing-quality score.

No installation, version bump, model training, commit, push or new official
template compilation occurs. The bounded experiment gives inspectable local
Results improvements and an unresolved outcome-definition concern, not stable
abstract or general writing superiority.

Release assessment: **CONDITIONAL**. PowerShell validation is unavailable; the
complete multi-stage workflow, routing changes and post-pilot outcome-definition
guidance are not behaviorally verified. This is not a release certification.
