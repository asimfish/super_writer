# From Clear Prose to Exemplar-Informed Writing

These are authored, synthetic teaching contrasts, not real research or new blind
evaluation results. The point is to diagnose quality differences even when the
original text is understandable. No source sentences or scientific results are
copied from exemplar papers. The abstract's S1 is an existing local editorial
observation with abstract-only reading scope, not a new full-paper analysis.
The abstract fixture also teaches a negative lesson: completeness and extra
qualification are not substitutes for selective emphasis.

## Abstract: Explain the Insight, Not Only the Modules

[Runnable v2 input](benchmark-input.json) and [authored response bodies](benchmark-responses.json)
contain six criteria. Three are priority gaps; expression, basic clarity and
format already meet the target. The writer addresses the selected three within a
60-word, no-expansion budget; the reviewer accepts a purpose-led opening as a
valid alternative to a gap-first one.

**Before:** We present PatchMap for indoor robot navigation. PatchMap has a map
cache and an update module. We evaluate it on 120 indoor navigation trials. Mean
map-update time is 12 ms and task success is 81%, compared with 28 ms and 82% for
full rebuilding.

**Rejected over-complete revision:** To avoid rebuilding unchanged map regions,
PatchMap reuses existing cells and updates those touched by new observations during
indoor robot navigation. On 120 matched trials with the same perception backbone,
mean map-update time is 12 ms versus 28 ms for full rebuilding, while observed task
success is 81% versus 82%. The measured computational benefit concerns map updating
rather than end-to-end navigation latency.

This version is accurate, but it grows from 44 to 63 words. The final limitation is
already carried by the precise metric name `map-update time`; the module inventory,
standalone evaluation lead and defensive tail dilute the answer. The benchmark
rejects it before stylistic preference.

**Accepted concise revision:** PatchMap updates only cells touched by new
observations instead of rebuilding the map. On 120 matched indoor trials with the
same perception backbone, it reduces mean map-update time from 28 to 12 ms;
observed task success is 81% versus 82%.

This version is 40 words. It makes the operation, avoided work and matched evidence
recoverable while removing four words from the original. It does not claim
equivalent success or faster end-to-end navigation.

The transfer is a writing choice: make the operation explain the contribution,
then use evidence to evaluate it. The [ResNet abstract note](../../references/abstract-exemplars.md#05-resnet-cvpr-2016)
motivates that choice; it supplies no robotics claims. The local `abstract`
protocol and `ai.rule.operation`/`ai.rule.quantities` supply complementary checks.
The original is not incomprehensible; it leaves the most informative scientific
choice unused. The revision is a teaching candidate, not the uniquely best wording.

```bash
python scripts/writing_loop.py examples/writing-team/benchmark-input.json
python -m unittest discover -s tests -p test_writing_benchmark.py -v
```

The CLI emits the actual selected protocol, complete rule/language cards and
located exemplar observation, not a command to imagine what the library says.

## Related Work: Synthesize Along a Comparison Axis

Synthetic facts: Method A and Method B both rely on a known environment map;
Method C and our method build the map online. C rebuilds it after every
observation; ours updates affected cells. No performance ranking is supplied.

**Before:** A uses a known map. B also uses a known map. C builds a map online.
Our method also builds a map online and updates affected cells.

**Authored revision:** Prior methods either assume a known environment map (A, B)
or build one online (C). Our method shares C's online setting but updates affected
cells instead of rebuilding the map after each observation.

The `related_work` / `taxonomy-first` protocol supplies grouping, shared setting
and differentiating axis. The gain sought is synthesis and precise positioning,
not stronger criticism of prior work. This example is **standards-based**, not
evidence that we read a real related-work exemplar. In a real manuscript, replace
the synthetic source facts with verified passages and preserve their citations.
Without such verification, do not declare a novel research gap or superiority.

## Experiments: Make the Comparison Answer a Question

Use the same synthetic PatchMap evidence above, with Table 1 assumed to contain
those two rows and the stated metrics; no additional measurements are invented.

**Before:** Table 1 reports map-update time. PatchMap takes 12 ms. Full rebuilding
takes 28 ms. Task success is 81% and 82%, respectively.

**Authored revision:** On the same 120 indoor trials and perception backbone,
PatchMap reduces mean map-update time from 28 to 12 ms versus full rebuilding;
observed task success is 81% versus 82% (Table 1).

The `experiments.analysis` / `result-paragraph` protocol changes the paragraph
from cell-by-cell narration into a controlled comparison with a bounded answer.
For a whole experiment section, use `experiments` instead and compare question
coverage, setup, controls, result ordering and analysis. For a table, select its
table protocol and inspect caption, units, aggregation and comparison conditions.
An unmeasured ablation cannot be invented to match an exemplar's experiment layout.

## What Should Remain Different

A theory abstract needs its assumptions and result, not our timing sentence.
Chronology can organize related work when conceptual evolution is the subject.
A setup paragraph may correctly enumerate settings; it need not make every line
an argumentative result. Official format follows a checked venue requirement,
not the appearance of a famous paper. Learning requires selecting which observed
choice fits the author's facts and showing it in the final prose.
