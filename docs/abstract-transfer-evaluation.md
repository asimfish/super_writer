# Abstract-Only Transfer Confirmation

Protocol frozen on 2026-10-11; local run completed on 2026-10-12.

## Result and Decision

Six papers, two initial samples per paper and one revision per condition produce
12 pairs and 24 final abstracts. Anonymous preferences are **candidate 10,
baseline 6, tie 8**. Both sample strata and four paper strata favor the candidate
on net. Two pairs unanimously favor the candidate, one the baseline, one ties,
and eight disagree.

**The frozen continuation criterion fails.** Neural ODE sample 2 unanimously
favors baseline, violating the predeclared no-unanimous-baseline requirement.
Do not remove that pair, lower the threshold or call the candidate generally
better. The same append-only candidate remains an experimental snapshot;
the canonical argument-transfer guide is unchanged. There is directional
preference evidence worth studying, not an admitted default writing rule.

[All 12 pairs side by side](../evals/abstract-transfer/comparison.html) /
[raw outputs and receipts](../evals/abstract-transfer/README.md) /
[complete summary](../evals/abstract-transfer/summary.json).

## What Was Frozen

The candidate is byte-identical to the preceding
[operative-relation pilot](operative-relation-evaluation.md), whose abstract
preferences were 4 / 0 / 4 despite no overall gain. It asks editors to protect
the operative relationship and necessary conditions during compression.
There is no new candidate rule, model training or post-selection retuning.
Baseline and candidate share four guides and the exact initial abstract,
working notes and selected body. Each receives one revision, 150-200 English
words and notes no longer than 100 words. No quality retries or raw repair.

Source preparers freeze one abstract-level critical question before generation.
**Writers and editors never receive that question.** Anonymous preference
reviewers also do not receive it. Source-free readers answer generic contribution
and scope questions; source auditors later receive the frozen question and
locator, but no expected answer. Legitimate abstract-level alternatives are
allowed; optional omissions are not automatically false science.

Six initial, twelve editor, six reviewer, six reader and six auditor contexts,
plus three source-preparation contexts, total 39 fresh inherited same-family
contexts with `fork_context=false` and no model override. All are closed.
Two reviewers per group see exactly reversed A/B labels. Each reader sees four
texts balanced by condition, never both counterparts of one paper/sample.
All 18 assessment responses are saved before the first decode.

The [protocol](../evals/abstract-transfer/PROTOCOL.md) freezes the continuation
criteria, requested budgets and exceptions before preparation. Groups, paper
replicates and same-family judges are clustered, not independent humans.

## Cases and Source Versions

| ID | Function | Primary metadata | Actual input limitation |
| --- | --- | --- | --- |
| A01 | Robot planning | [VoxPoser, CoRL 2023](https://proceedings.mlr.press/v229/huang23b.html) | Assigned 23-page PMLR PDF, no numbered revision asserted |
| A02 | Optimization | [SAM, author metadata](https://research.google/pubs/sharpness-aware-minimization-for-efficiently-improving-generalization/) | OpenReview access blocked; allowed [arXiv v1](https://arxiv.org/pdf/2010.01412v1) is a 2020 preprint, not verified equivalent to final ICLR 2021 |
| A03 | Image personalization | [DreamBooth, CVPR 2023](https://openaccess.thecvf.com/content/CVPR2023/html/Ruiz_DreamBooth_Fine_Tuning_Text-to-Image_Diffusion_Models_for_Subject-Driven_Generation_CVPR_2023_paper.html) | CVF accepted-paper version; separately linked supplement and IEEE-version equivalence not checked |
| A04 | Tool learning | [Toolformer, NeurIPS 2023](https://proceedings.neurips.cc/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html) | Main proceedings PDF; separately linked supplementary experiments not independently checked |
| A05 | Inference systems | [FlexGen, ICML 2023](https://proceedings.mlr.press/v202/sheng23a.html) | 23-page official PDF including Appendix A; dummy-weight speed and real-weight quality evidence remain distinct |
| A06 | Continuous models | [Neural ODE, NeurIPS 2018](https://proceedings.neurips.cc/paper/2018/hash/69386f6bb1dfed68692a24c8686939b9-Abstract.html) | Complete assigned 13-page file lacks cited appendices A-F; raw extraction contains 626 replacement characters |

DPO and MAE are excluded before source preparation because existing exemplar
guidance already develops them. A bounded exact-title search has no matches for
the six selected titles in previous eval/docs/references metadata. It does not
exclude abbreviations, concept/family overlap, other repository paths or model
pretraining. These are new evaluation inputs, not model-unseen papers.

Selected bodies retain 32 original extraction spans, 206,896 bytes, with exact
two-LF separators. Methods, analysis, experiments, relevant limits and available
necessary proofs are retained; A06 has declared essential Introduction definitions.
Original abstracts, contribution previews, conclusions and references are not
writer inputs. No equation, table, glyph or whitespace repair is made.
Bitmap plots are not independently inspected; no unprinted point values are inferred.

Preparers record incidental excluded-text exposure, including A01/A02 metadata
abstracts and A06's truncated HTML abstract; A03/A04 display no abstract or
conclusion prose. The coordinator sees discovery abstracts and a Neural ODE review
search excerpt, neither supplied as an assessment target. There is no perfect
coordinator/preparer isolation claim. Candidate identity is frozen beforehand;
writing and assessment contexts remain prompt-restricted, not OS-quarantined.
Full details, source versions, warnings and hashes are in
[source receipts](../evals/abstract-transfer/source_receipts.json) and
[execution disclosure](../evals/abstract-transfer/execution.json).

## All-Paper and Sample Results

| Paper | Candidate votes | Baseline votes | Ties |
| --- | ---: | ---: | ---: |
| VoxPoser | 3 | 1 | 0 |
| SAM | 1 | 1 | 2 |
| DreamBooth | 2 | 1 | 1 |
| Toolformer | 2 | 0 | 2 |
| FlexGen | 2 | 1 | 1 |
| Neural ODE | 0 | 2 | 2 |
| Total | 10 | 6 | 8 |

Sample 1 is 4 candidate / 2 baseline / 6 tie; sample 2 is 6 / 4 / 2.
Unanimous candidate pairs are A01_s2 and A03_s2. A06_s2 unanimously favors
baseline; A06_s1 unanimously ties. All other pairs disagree, including opposite
preferences on A01_s1 and A05_s2. Preserve both independent reasons rather than
resolving them by a third selected judge.

All 48 source-audit judgments mark fidelity pass, critical support supported
and reader support text-grounded, equally in both conditions. Preference
reviewers also mark all 48 version judgments fidelity pass. **There is no
audited fidelity, critical-support or reader-grounding improvement.** These
channels again hit a ceiling; synthetic calibration did not guarantee that
real-paper variants would discriminate. Argument and language ratings remain
ordinal descriptive judgments, not calibrated quality scores.

## What the Examples Teach

**VoxPoser A01_s2, unanimous candidate:** both reviewers favor explaining what
voxel values do and how scoring a trajectory combines targets and constraints,
not merely naming composed maps. They also credit a preserved exploration-prior
co-contribution and qualified evidence. A01_s1 disagrees: one reviewer prefers
baseline's more explicit local waypoint perturbations, the other candidate's
disturbance/replanning explanation. This is not a universal candidate win.

**DreamBooth A03_s2, unanimous candidate:** the reviewers credit an explicit
few-reference-view problem and a reason for using DINO to distinguish subjects
within a class. The gain is connecting an evaluation choice to the contribution,
not adding the largest metric inventory. A03_s1 instead gives baseline/tie.

**Neural ODE A06_s2, unanimous baseline:** the two abstracts retain the same
scientific contributions, decisive numbers and numerical limitations. Baseline
puts MNIST evidence next to continuous-depth training, density experiments next
to trace-based flows, and spiral prediction next to the latent model. Candidate
introduces flow and latent mechanisms, then returns to MNIST. Both reviewers
identify that displaced evidence as a weaker argumentative progression.

The observed structures are:

```text
Baseline:  dynamics/adjoint -> MNIST -> trace/flows -> density -> latent -> spirals -> numerical limit
Candidate: dynamics/adjoint -> trace/flows -> density -> latent -> MNIST -> spirals -> numerical limit
```

This is an analyst inference from the saved texts and independent reasons,
not a new writing rule proven by this test: preserving each local operation
does not ensure that each co-contribution stays coupled to its own evidence.
Future development should test global contribution/evidence ordering, not assume
that more procedural explanation always improves an abstract. Those cases are
now development material; a new hypothesis needs genuinely new evaluation inputs.

**SAM and FlexGen show limits of a single preferred order.** SAM sample 2 gives
tie/baseline: one reviewer finds candidate more enumerative despite correct extra
results. FlexGen sample 2 splits baseline/candidate on whether compression should
precede the measured throughput or follow it next to the cause. Both preserve
dummy-weight versus real-weight distinctions and the idealized weight-I/O scope.
No after-the-fact rationale changes any recorded vote.

## Gate, Exceptions and Next Frontier

Six of seven continuation conditions pass: both samples net candidate, at least
four papers net candidate, at least two unanimous candidate pairs, no candidate
fidelity fail, no new candidate concern and all candidate budgets respected.
The no-unanimous-baseline criterion fails. It is a conservative operational
next-stage decision, not a hypothesis test or confidence interval. Keep it failed.
Even passing would not automatically promote runtime guidance or prove human gain.

One FlexGen shared initial abstract has 203 words against the 200-word limit.
Both final conditions use that same untouched initial and are within budget.
All other 71 prose/note fields pass; all assessment budgets and literal witness
checks pass. No sample is dropped or padded. Source receipt-assembly errors are
recovered before generation; some later read-display truncations require rereads,
not new writing attempts. These operational problems remain disclosed.

These are generated reconstructions of published research, not author abstracts
or our new findings. No author-original comparator, independent human panel,
population significance, venue acceptance effect, full-skill pipeline test,
source-version equivalence or model-unseen generalization is established.
The fixed budget is a controlled writing budget, not every venue's submission rule.
No previous round's preference counts are pooled.

Next frontier: develop a separately frozen hypothesis about maintaining
contribution/evidence coupling in multi-contribution abstracts, then evaluate it
on different papers with calibrated judgments and human checks. Do not retest
these six as fresh data or infer improvement from the all-pass support labels.

## Verification Boundary

The archive preserves 36 original response files and copied bytes. Publisher
PDFs, raw/selected bodies, full metadata and extraction recipes remain local;
they are not relicensed. Public checks verify archived responses and declared
hash consistency; omitted original-input verification requires the local workspace.
See [validation scope](validation.md) for completed software, browser and safety
checks. No commit, push, installation, skill version or imported pin changes.
