# Evaluator discrimination calibration (2026-10-11)

## Result and scope

The prespecified admission gate passes on **12 original synthetic cases**,
not real-paper generations. Nine pairs introduce a known consequential defect;
three are neutral controls. Two anonymous reviewers prefer the faithful text
in all 18 defective-pair judgments. The identical control receives both ties;
the paraphrase and legitimate-omission cases allow either justified preference
or a tie. A supported stylistic difference is not scored as a factual error.

Two fine auditors identify missing or contradicted critical support in all
18 defective-text judgments and falsely flag none of 30 faithful/neutral-text
judgments. Fidelity labels meet every prespecified allowed-label threshold.
These are eighteen clustered model judgments on nine constructed defects,
not eighteen independent trials, human validity or evidence of better writing.

[View all original controls and judgments](../evals/evaluator-controls/comparison.html)
or inspect the [archive](../evals/evaluator-controls/README.md) and
[full admission criteria](../evals/evaluator-controls/summary.json).

## Why this calibration was needed

The [preceding twelve-paper test](broad-writing-evaluation.md) produced 184 ties
in 216 preferences, with maximal primary core-recovery scores for every final
paragraph. That could reflect polished drafts, a strong baseline, subtle changes
or inadequate measurement. More high scores alone cannot resolve the issue.
This exercise asks whether known defects and valid alternatives can be separated,
not whether the writer has learned excellent papers' style.

| Constructed group | Cases | What changes |
| --- | ---: | --- |
| Missing relationship | 3 | Facts remain true, but execution schedule, allocation relation or fixed-evidence control disappears |
| Changed metric/resource event | 3 | Correct counts/timings/allocations are attached to a false completion, request or total-memory claim |
| Necessary guarantee condition | 3 | Initialization/exchangeability/exact-gradient premises are omitted or a proof is transferred to an uncovered implementation |
| Neutral alternatives | 3 | Byte-identical prose, supported paraphrase, legitimate omission of irrelevant implementation metadata |

All 24 passages are original fictional prose, roughly 75-100 words. No publisher
abstract, private manuscript or real scientific experiment is imported. Synthetic
theorem premises are explicitly supplied fictional facts, not claimed mathematical
discoveries. This is a deliberately constructed diagnostic, not representative
sampling of subtle real-paper failures or training new model weights.

## Oracle review, freezing and blinding

An independent fixture reviewer found two substantive problems before assessment:
C05's valid text unnecessarily asserted that other-device experiments did not
exist; C07's missing initialization also made a general invariant contradicted
by a provided counterexample. Those are corrected before behavioral testing.
C11's editorial rationale also replaces an inaccurate tradeoff label with
comparison. Initial cases, initial review and exact
[corrections](../evals/evaluator-controls/corrections.json) remain archived.
A different fresh reviewer validates all twelve final cases. Neither oracle
review is counted as an anonymous behavioral judgment.

Protocol, final source/variant/oracle fixture, reviewer/reader packets and mappings
are frozen before anonymous testing. Two fresh preference contexts see all twelve
pairs with exactly reversed A/B order, without category, oracle or variant-role
labels. Four fresh source-free readers each receive six individual paragraphs
and generic unit questions. They never see both counterparts of a case, source
evidence or the case-specific critical question. Balanced assignment gives each
reader three texts of each variant role. Every text is read once.

After reading, two coarse and two different fine auditor contexts each inspect
all 24 anonymous paragraphs and the same readers' reconstructions against the
same fictional evidence. Coarse auditors use the earlier 0-2 central-relation
and consequential-scope recovery rubric, selecting the paragraph's function
rather than requiring an exhaustive fact inventory. Fine auditors additionally
receive a pre-frozen case-specific critical question, without an expected answer,
and classify actual prose support as supported, missing, contradicted or uncertain.
The more specific question is an intentional measurement change, not a clean
causal isolation of prompt format, length or assessor variation.

Ten fresh anonymous contexts produce 24 preferences, 24 readings, 48 coarse and
48 fine audit judgments. Two fixture-review contexts bring the total to twelve.
All inherit the same model family without override or parent-history fork.
Input restrictions do not isolate the filesystem or erase prior model knowledge.
Every planned response is saved before decoding, with no semantic response repair,
quality retry, winner selection or post-result threshold adjustment.

## What the two rubrics actually show

| Defect group | Coarse target recovery below maximum | Fine missing/contradicted support |
| --- | ---: | ---: |
| Relationship | 6 / 6 | 6 / 6 |
| Metric/resource event | 2 / 6 | 6 / 6 |
| Guarantee condition | 6 / 6 | 6 / 6 |

**The metric row does not mean coarse auditors missed four false claims.** Both
coarse auditors separately mark all three defective metric passages fidelity-fail.
For C05 timing and C06 memory, prose-only readers correctly reject the false
opening claim using the paragraph's own numbers. Coarse auditors consequently
award maximum reader recovery while retaining the writer's fidelity failure.
The fine rubric calls critical prose support contradicted and the successful
reader reconstruction text-grounded. These are different objects of judgment.

C04 instead misleads its reader into treating final-state attainment as
uninterrupted trajectory completion, despite resets. Its reader recovery is
inadequate as well as its writing claim being false. The two channels must remain
separate: a reader can understand a contradiction without repairing the writer,
and can guess a correct source fact without recovering missing explanation.

Thus this calibration establishes operational discrimination on known controls,
not that a finer rubric is generally superior or that the preceding real-paper
ceiling was caused by score insensitivity. The real-paper drafts and strong
baseline can genuinely be close. A more useful next test can record claim
support, reader-added information and prose preference separately.

## Admission and limitations

The predeclared gate requires at least five of six allowed preference choices,
defect detections and defective fidelity labels in **each** defect category;
at most one false flag and at least five correct faithful fidelity labels per
category; at most one false flag and at least eleven correct faithful fidelity
labels among twelve neutral judgments; and two ties on identical prose. Every
criterion passes. Uncertain support is not credited as defect detection.

The gate permits a separately frozen fresh-paper comparison. It is not a
threshold for publishing a quality-gain claim, successful abstract style learning,
human comprehension or a complete skill release. Only three cases per defect
type are covered; corrupted metrics are often explicitly contradicted by numbers
in the paragraph and are easier than subtle omission or ambiguous measurement.
Different question specificity and different assessors both contribute to any
rubric difference. No independence, statistical significance or population effect
is claimed. Neither prior pilot votes nor different audit channels are pooled.

All reader answers/witnesses and reviewer/auditor reasons meet their frozen word
budgets; every nonempty witness is a literal substring and within eighteen words.
No raw schema failure or repaired behavioral response occurs. One coarse auditor
reports initial tool-output truncation resolved by smaller source reads, not a
new judgment or quality retry. All ten raw JSON files retain byte receipts.

## Changes and verification

The existing [blind-evaluation guide](../references/blind-evaluation.md) now
explicitly calibrates sensitivity and false flags, freezes a consequential
unit question and distinguishes text support from a reader's correct guess or
rejection of a false statement. This is evaluation guidance, not an automatic
entailment tool or a model update. A narrow operation-preservation hypothesis
and its subsequent proposed writing design are frozen separately, not promoted
as measured writing improvement merely because this gate passed.

Ten helper tests exercise immutable writes, malformed/duplicate IDs, balanced
reversal and reader separation, unblinding/missingness, drift, false flags and
uncertain-label handling on temporary fixtures. The initial duplicate-expected-ID
test fails before the parser correction and passes afterward. Three repository
tests check archive integrity and the valid neutral-control distinction; they
initially fail while the archive is absent and pass after complete archival.
These are infrastructure assertions, not semantic re-evaluation of the model.

Playwright verifies desktop/mobile display, exact identity of all 24 displayed
variant strings, category filtering, expandable judgments and non-overlap. The
archive contains original synthetic evidence and anonymous packets, so no
third-party paper retrieval is needed to reconstruct this calibration. A fresh
model rerun still needs an explicit agent runner and will not be deterministic.
No paid-API call runner, new dependency, installation, version bump or remote
publication is introduced.

The subsequent local gate runs 180 repository tests (179 pass, one unavailable
PowerShell skip), eleven CLI smoke cases, compilation/frontmatter and byte checks.
The separately frozen [real-paper follow-up](operative-relation-evaluation.md)
reports mixed results rather than treating this calibration pass as a writing gain.
