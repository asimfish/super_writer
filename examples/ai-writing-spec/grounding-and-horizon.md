# Grounding, Faithfulness and Task Chains

All scenarios, scores and paragraphs below are original synthetic examples,
not CALVIN results or results from any cited paper. They demonstrate bounded
editorial choices, not model-weight training or a measured quality gain.
The [catalog](../../references/ai-writing-spec.json) supplies complete conditions,
exceptions and source locations. These examples extend the
[six earlier cases](README.md), not a new mandatory paragraph template.

## 1. One Word, Different Targets

Facts: a date is independently verified outside the supplied passage but is not
in that passage. Readers find a generated rationale convincing. No check of the
model's prediction process is conducted.

Misleading:

> The answer is unfaithful and therefore false; the convincing rationale faithfully explains the model's decision.

Supported:

> The date is externally verified but unsupported by the supplied passage. Reader approval establishes the rationale's plausibility, not its fidelity to the model's prediction process.

The revision gives each judgment a referent. Source support, world truth and
process faithfulness are not interchangeable. External verification is a fact
of this toy scenario, not a license to assume unsupported claims are true.

[Faithful](../../docs/writer-atlas.html#ai.usage.faithful) /
[evaluated construct](../../docs/writer-atlas.html#ai.rule.evaluation-target).

## 2. High Precision Can Still Leave a Question Unanswered

Facts: a response states ten atomic facts; eight are reference-supported.
Required-topic coverage is not evaluated. A separate answer has four statements:
three have citations jointly supporting their full content, and one is uncited.
For one supported statement, two passages each independently suffice.

Misleading:

> The first answer is 80% complete. The second has perfect citation recall because its three cited statements are supported, but its duplicate supporting citation is incorrect.

Supported:

> Eight of ten extracted facts in the first response are reference-supported; completeness remains unmeasured. Under the stated ALCE-style segmentation, the second answer has citation recall of three out of four statements. Its two individually sufficient citations can both receive precision credit.

Do not combine these separate toy answers into a single score or call a single
response's supported fraction a reproduced corpus-level FActScore. Citation
precision is not a smallest-set requirement, and joint passage support is valid
under the declared protocol. These metrics do not by themselves establish
fluency, answer completeness or all forms of factual correctness.

[Factual precision](../../docs/writer-atlas.html#ai.term.factual-precision) /
[citation recall](../../docs/writer-atlas.html#ai.term.citation-recall) /
[citation precision](../../docs/writer-atlas.html#ai.term.citation-precision).

## 3. Visual Input Is Not Verified Visual Support

Facts: images enter a caption model. Reference captions omit a mug, but they are
not exhaustive object inventories. Only object mentions are checked in the
available hallucination evaluation; attributes and relations are unassessed.

Misleading:

> The captions are visually grounded and hallucination-free. The missing mug mention proves that no mug is present.

Supported:

> Image conditioning supplies visual input but does not itself verify each generated statement. Because the reference captions are incomplete, their omission of a mug does not establish its absence. The object-only check leaves attribute and relation errors unassessed.

The paragraph separates input, reference coverage and error scope, rather than
putting all three under a reassuring adjective. A complete annotation for a
particular object could justify a stronger absence judgment; the toy reference
does not provide one.

[Grounded](../../docs/writer-atlas.html#ai.usage.grounded) /
[evidence modality](../../docs/writer-atlas.html#ai.rule.evidence-modality) /
[object hallucination](../../docs/writer-atlas.html#ai.term.object-hallucination).

## 4. A Planning Score Does Not Diagnose Execution Failure

Facts: the same ten instructions are evaluated. Nine plans pass the declared
validity check; six full instructions finish on the robot. Stage-specific logs
and controlled component interventions are not available.

Score logbook:

> Plan validity is 90%. Execution success is 60%. There are four execution failures. The planner causes the failures.

Question-led Results paragraph:

> Do valid plans suffice for physical completion? On the same ten instructions, nine plans pass the validity check, whereas six instructions finish on the robot. The two measures therefore assess different requirements, and planning validity alone does not establish end-to-end completion. Without stage-specific logs or controlled interventions, this result does not attribute the execution failures to the planner, skill selection or low-level control.

The question organizes the comparison; the comparison supports a narrow answer;
the closing sentence states the unresolved diagnostic question. It is not merely
a list of scores with a stronger final adjective. The observed counts are not
by themselves a statistically established population gap or a causal effect.

[Result answer](../../docs/writer-atlas.html#ai.rule.result-answer) /
[failure localization](../../docs/writer-atlas.html#ai.rule.failure-localization) /
[robotic affordance](../../docs/writer-atlas.html#ai.term.robotic-affordance).

## 5. Three Chain Summaries, Three Questions

Facts: twelve chains each contain four dependent subgoals, with no intermediate
resets. A chain stops at first failure. Counts completing at least one, two,
three and four consecutive subgoals are **12, 9, 6, 3**.

| Summary | Calculation | Question answered |
| --- | --- | --- |
| Full-chain success | 3/12 = 25% | How many initial chains finish every subgoal? |
| Mean successful-prefix length | 30/12 = 2.5 | How far does a chain progress on average? |
| Last-stage conditional success | 3/6 = 50% | Of the chains reaching the last subgoal, how many finish it? |

The prefix mean is `(12 + 9 + 6 + 3) / 12`; adding survival counts counts each
chain once for every successful prefix step. These are correlated stages within
chains, not four independent task samples. The final conditional rate measures
survivors in carried-over states, not isolated last-task success.

Score logbook:

> The system scores 100%, 75%, 50% and 25%, with a mean of 62.5%. Last-task success is 50%, demonstrating strong long-horizon control.

Question-led Results paragraph:

> How much of the task sequence survives state carryover? In twelve four-subgoal chains without intermediate resets, all chains complete the first subgoal, but only three finish the full sequence. The mean successful-prefix length is 2.5 subgoals. These summaries distinguish partial progress from complete execution; the final-stage conditional success of 50% applies only to the six chains that reach that stage. The evaluation characterizes this chain protocol, not an unrestricted long-horizon capability.

The first sentence defines the reader's question, the next selects the
consequential contrast, and the rest explains the scope rather than inventing
why chains fail. Reporting an action prediction length would not answer this
question. A descriptive report can omit the explicit question sentence when its
heading and surrounding text already make the comparison purpose clear.

[Task-chain success](../../docs/writer-atlas.html#ai.term.task-chain-success) /
[long-horizon](../../docs/writer-atlas.html#ai.term.long-horizon) /
[paragraph function](../../docs/writer-atlas.html#ai.rule.paragraph-function).
