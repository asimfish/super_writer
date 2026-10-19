# Explanation-Preserving Compression Pilot

Declared 2026-10-19, before writer generation and judging. This is a small
mechanism probe, not a general-quality benchmark or full multi-role-loop trial.
The failed six-paper compression pilot is development evidence and is not reused
as fresh test data. No human validation or pretraining-unseen claim is made.

## Materials and conditions

Four RSS 2025 papers not previously named in this repository's writing evaluations:
MISO (p004), Doppler Correspondence (p005), Building Rome with Convex Optimization
(p032), V-HOP (p037). Two independent source contexts prepare body-only fact
packets, ordinary shared initial drafts and two explanation questions per paper.
PDF page 1 and author abstracts are withheld from source agents and writers.
The coordinator saw proceedings abstracts during metadata discovery; it does not
author the packets or generated candidates. Source packets are checked before
freezing. The coordinator narrows source-prepared questions to abstract-level
relationships before freezing; it does not add technical facts or optimize drafts.
All treatments receive identical evidence and relation priorities.

Twelve revisions: four papers x three conditions, one generation each:

- `hard`: legacy compression guide at commit 020e17862e00ac9d03afdd05fd3612348ffb46c3;
  no more words than the supplied initial draft, plus a 150-word absolute cap.
- `relaxed`: identical legacy guide and facts, but explicitly allowed to grow
  within the same 150-word absolute cap as `meaning`. This control separates
  budget relaxation from the new editorial guidance.
- `meaning`: frozen explanation-preserving guide; 150-word absolute cap without
  a relative cap. Protect relationships and contribution organization before
  compressing, using the same facts and priorities as both controls.

The relative-budget instruction in each prompt overrides the generic legacy
guide's author-approval language; relaxed growth is explicitly authorized.
No minimum length, fixed sentence count or requirement to use every fact.
Two fresh writer contexts per treatment handle disjoint two-paper blocks. Each
context receives one self-contained JSON prompt only. No retries for prose quality;
retain missing/invalid outputs and budget misses in denominators. Equal numbers of
writer contexts and passages per treatment. Host model/effort inherited, no model
override; token and monetary costs unavailable. Prompts differ in guide length,
so equal call count does not establish token-cost equivalence.

## Evaluation

Two fresh anonymous preference reviewers see each paper's three revisions only,
with randomized labels and reversed labels/order for the second reviewer. They
see neither evidence, plans, conditions, questions nor original abstracts. Each
records rankings with ties and a reason for each pair on overall effectiveness,
explanation, organization and language. These judgments concern prose; source
fidelity is audited separately. Same-model judgments can share biases.

One separate fresh reader receives each revision independently in randomized order,
without the evidence or other versions of that paper in the same case. It answers
two frozen explanation questions and supplies exact prose witnesses, or reports
that the text does not specify the answer. All versions are in one context, so
cross-case inference remains possible; it is not true per-passage isolation.
Two synthetic controls contrast a true label-only summary and an explicit
operation. They calibrate missing-explanation detection, not prose preference.

A separate grounded auditor receives evidence, prose and the actual reader
answers, never treatment identities or preference judgments. It classifies each
answer as `supported`, `missing`, `contradicted` or `reader_added`, with a located
reason. A source-correct guess not entailed by the prose is not recovered meaning.
It separately lists consequential factual errors in each passage. Keep calibration
outcomes and disagreements, including audit mistakes; no adjudication rerun.

## Frozen decision rule

Report raw wins/losses/ties, per-paper disagreements, word counts, answer support,
calibration and fidelity separately. Do not turn twelve passages into a general
win-rate or acceptance claim. The provisional mechanism gate requires:

1. `meaning` beats `relaxed` on at least 6 of 8 overall paper-reviewer judgments,
   with no more than 2 losses.
2. At least 7 of 8 `meaning` explanation answers are audited `supported`, and at
   least 2 more than `relaxed`; otherwise the recovery measure does not establish
   an explanatory benefit even if preferences favor the candidate.
3. Both synthetic controls are classified as expected; all `meaning` outputs
   meet the 150-word cap, with no consequential factual error.

Passing permits a larger preregistered evaluation, not a default-quality claim.
Failure is reported without changing the gate. No selection of the best draft,
retroactive packet repairs, author-original baseline, or extra writer attempts.
Source/preparation errors discovered later are retained and scoped explicitly.

## Reproduction

`pilot.py prepare` freezes protocol, source packets, guides, code and writer
prompts before dispatch. `blind` freezes anonymous packets before reviewer/reader
dispatch. `analyze` derives summaries and HTML from saved outputs. `check` verifies
frozen hashes and recomputes those results; it does not make model calls or assert
that a fallible semantic verdict is correct. `execution.json` records actual agent
IDs/dispatch inputs. Public files contain paraphrased facts and generated prose,
not full source papers or their original abstracts.
