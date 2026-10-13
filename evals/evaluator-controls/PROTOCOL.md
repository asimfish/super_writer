# Evaluator discrimination calibration

Design registered before anonymous behavioral assessment, 2026-10-11.
Cases and their original editorial oracles are independently reviewed for
logical validity before the final input freeze. Pre-freeze corrections, if any,
are recorded; no behavioral response is repaired or retried for quality.

## Question and material

The preceding twelve-paper revision experiment had 184 ties in 216 votes and
maximal core recovery in every primary audit. Determine whether assessors can
distinguish known, consequential text defects from legitimate variation before
claiming another writing-quality gain. No paper or model-weight training occurs.

Twelve original synthetic cases, three each: a missing operation/control
relationship with otherwise true facts; a changed metric/resource event despite
correct numbers; an omitted necessary guarantee condition or misplaced proof;
and neutral controls. Neutral cases are byte-identical text, meaning-preserving
paraphrase and legitimate omission of nonessential implementation metadata.
Only the identical control requires a tie; a justified stylistic preference
between equivalent texts is not a false factual judgment.

There are 24 short standalone passages, approximately 75-100 words each, with
both variants and source premises fixed. These are deliberately constructed
diagnostics, not author prose, new science, fresh writing generations or a
representative sample of subtle real-paper defects. Synthetic theoretical
premises are supplied facts for this exercise, not claimed new mathematical
results. No source links, publication text or private manuscripts are needed.

## Blinding and outputs

One independent fixture-oracle reviewer can read the complete fixture before
freezing. It is not counted as an anonymous behavioral assessor. Two fresh
preference contexts then see the twelve source-grounded pairs with exactly
reversed A/B order, no categories, oracles, variant names or prior outcomes.
Each returns a preference, separate fidelity labels and one located reason.

Four fresh prose-only reader contexts each see six individual anonymous texts
and generic unit-appropriate questions, without source, case-specific critical
questions, categories, oracles, paired counterparts or other answers. Two contexts
cover each six-case group with opposite variants, randomized balanced assignment.
Do not reconstruct omitted facts from memory. Quote text witnesses or record
that a requested relation/condition is not stated. All 24 texts are read once.

After readers finish, two fresh coarse auditors and two different fresh fine
auditors inspect all 24 anonymous texts, supplied evidence and reader answers.
Coarse auditors use the preceding 0-2 core/scope definitions and judge selected
paragraph function, not a mandatory fact inventory. Fine auditors additionally
receive the frozen case-specific critical question, but not its expected answer;
classify its support in the prose as supported/missing/contradicted/uncertain.
Both conditions have the same source evidence, texts and reader answers.
The question specificity is an intentional measurement difference, not a
clean causal decomposition of prompt length, format or assessor variation.

All contexts inherit the same model family without override or forked history.
Only supplied input access is restricted, not the filesystem or model memory.
Assessors save one raw JSON file, without repairs, padding or favorable retries.
Preference/coarse/fine reasons have at most 110 words per text/pair; readers have
at most 140 words per text across answers/witnesses, with each witness at most
18 words. Budget deviations, schema failures and missingness remain visible.

Ten anonymous output contexts yield 24 preference votes, 24 reader reconstructions,
48 coarse and 48 fine judgments. Finish every planned response before decoding
oracles/condition maps. Preserve invalid or missing responses; do not silently
drop them or relax admission gates. A helper/infrastructure bug may be fixed
with recorded regression evidence, never by editing raw semantic responses.

## Prespecified analysis and admission decision

Report every case, raw decision, fidelity label, reader witness, budget deviation
and assessor disagreement. Counts are descriptive on three controls per defect
type, not statistical significance or an effectiveness leaderboard. Do not pool
with real-paper preferences. Do not pick the favorable rubric after seeing data.

The fine rubric is eligible for a new writing experiment only if all hold:

1. Preference reviewers select the oracle-allowed variant on at least five of
   six votes in EACH of relation, metric and condition groups; the identical
   control receives both ties. Paraphrase/legitimate-omission preferences have
   no directional correctness oracle.
2. Fine auditors identify missing/contradicted critical support on at least five
   of six defective-text judgments in EACH group. Uncertain is not detection.
3. Fine auditors falsely flag at most one of six faithful texts in EACH defect
   group, and at most one of twelve neutral-text judgments. This prevents an
   always-critical assessor from passing sensitivity alone. Their fidelity
   labels must also match the allowed faithful labels on at least five of six
   judgments per defect group and eleven of twelve neutral judgments.
4. Fine fidelity judgments match allowed source labels on at least five of six
   defective-text judgments in EACH group. Missing explanation with otherwise
   true facts must not be automatically relabeled as false science.

Record coarse discrimination under the corresponding target (core <2 for
relation, scope <2 for metric/condition), but do not require the fine rubric to
win or combine both into a favorable score. Any admission failure stops the
fresh-paper quality experiment for this round; keep the full calibration archive
and diagnose measurement before testing another writing intervention. Passing
permits a separate frozen writing test; it does not itself prove better writing.

Potential subsequent repair is narrow: preserve an operation-to-consequence
relation and its indispensable condition in the actual claim-bearing sentence,
rather than substituting an assumption list. Freeze that guidance before any
fresh-paper body reading or writing, use equal revision budgets, independent
anonymous preference/source checks and disclose that the previous twelve papers
are development cases. The subsequent protocol, if entered, is a separate file.
