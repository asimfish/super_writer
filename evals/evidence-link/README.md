# Evidence-Link Mechanism Development

**Implemented candidate; no new model trial executed.** The latest real-paper
pilot remains candidate 3 / baseline 10 / tie 11, with its failed gate and default
guide unchanged. This directory develops a smaller selection-and-realization
mechanism, not a larger dictionary or a replacement quality claim.

[Candidate procedure](../../references/evidence-link-candidate.md) ·
[Failure evidence](../../docs/ai-spec-pilot-evaluation.md) ·
[Original synthetic cases and private expectations](cases.json)

## What Changes

The existing dossier teaches what an exemplar does; the rationale matrix records
why a unit should be written. The candidate makes an intervening choice explicit:
which of the available facts actually answers the promise being foregrounded?
It then binds the evaluated object, comparator and necessary condition before
realizing that relationship in prose. Read-back checks the relationship, not
keyword presence. Use existing cells or a brief internal note, not another
mandatory artifact or approval step.

The candidate is opt-in. The main `argument-transfer.md`, catalog entries, agent
defaults, schema and previous experiments are not replaced. No model weights,
external service, scheduled research job or automatic semantic linter is added.

## Worked Decisions

All facts below are invented development facts, not measurements from DROID,
SIMPLER or a new experiment. The snippets are authored illustrations, not sampled
model outputs or independently judged better drafts.

### Evidence Selection

E01 has three true facts: 12000 released demonstrations; a 32%-to-61% co-training
gain that changes amount and coverage; and a size-matched scene comparison.
If the promise is diversity at equal size, selecting only the largest gain leaves
the question unanswered. A possible result sentence is:

> At equal dataset size and training steps, policies trained across 12 scenes
> achieve 58% success on the held-out scene tasks, compared with 41% for policies
> trained across three scenes using the same backbone.

For a scale-and-construction priority, the release and collection protocol can
instead lead. An empirical ablation is not a prerequisite for describing a
resource. This is a priority-dependent decision, not a rule to always prefer E2.

### Conditions and Evaluated Objects

E02 does not call the training images the successful objects. With a shared
backbone, one possible sentence is:

> With a shared backbone, equal dataset sizes and the same training steps, the
> broad-data classifier achieves 63% recognition accuracy versus 49% for the narrow-data
> classifier on the held-out images.

When backbones differ, the numbers stay unchanged, but an appropriate claim is
about the two classifier configurations, not an isolated data-composition effect.
A common setup paragraph can still introduce controls before several results;
embedding every control in every sentence is not the objective.

### Interpretation, Not Another Disclaimer

E04 preserves policy ordering while overestimating every physical rate. For a
ranking question, the ordering agreement earns the conclusion. For an absolute-rate
question, the overestimates become the central finding. One generic closing line
about "not generalizing universally" cannot substitute for that distinction.

### Definition Versus Explanation

E05's definition-only request needs the meaning of Pearson correlation. Its
rationale request needs the relationship that motivates a second measure:

> A monotone nonlinear mapping can preserve policy order without preserving a
> linear relationship between success rates, so policy-order agreement complements
> Pearson correlation by answering a different evaluation question.

The second sentence is useful because of the requested question and supplied
relationship, not because a longer Methods paragraph is inherently better.

## Counterfactual Coverage

There are **eight families / 16 probes / seven domain labels**, covering Abstract,
Methods and Results. Each family has two inputs that differ in exactly one priority,
task scope or evidence field, with a corresponding different editorial expectation:

- E01: diversity's usefulness versus resource scale, with identical facts.
- E02: shared versus changed backbone, with identical accuracies.
- E03: answer accuracy versus calibration error, with identical training scope.
- E04: ranking agreement versus absolute-rate estimation, with identical measurements.
- E05: a metric definition versus its complementary-design rationale.
- E06: exact versus approximate density access, with the same conditional theorem.
- E07: removal worsens versus improves performance, with the same full-system gain.
- E08: two supported additions versus an unmeasured second benefit.

These domain labels describe fixture coverage, not papers, independent samples or
measured transfer. The expectations are locally authored editorial oracles; they
need independent semantic review before being used as evaluation ground truth.

## Reproduce the Writer Inputs

From the repository root, with Python 3.10+:

```bash
python evals/evidence-link/probe.py --list
python evals/evidence-link/probe.py --id E01-diversity --condition baseline
python evals/evidence-link/probe.py --id E01-diversity --condition candidate
python -m unittest discover -s tests -p 'test_evidence_link_probe.py' -v
```

The tool prints one JSON packet and does not call a model, search, write files or
grade prose. Paths resolve from its own checkout, including in an extracted skill.
Baseline and candidate receive the same complete evidence, priorities, 120-word
passage ceiling and output contract, with no padding to a minimum. Both receive the three current common guides;
candidate alone receives the complete new guide. Guidance exposure is therefore
**unequal**; neither equal context length nor an isolated decision effect is claimed.
The `input_sha256` covers canonical UTF-8 `writer_input`, with complete guide hashes.

Only `writer_input` is intended for the writer. The packet assembler uses a field
whitelist, excludes all private oracles and avoids revealing which facts an oracle
selected. This is prompt assembly, not an OS sandbox: a local agent with repository
access can still read `cases.json`. Use a separately scoped context and record its
actual access if conducting a trial. The hashes are reproducibility aids, not an
external preregistration or proof of isolation.

Tests check paired-input differences, packet equivalence, expectation exclusion,
hashes, bad selection failures, independent evidence snapshots, offline/read-only assembly, relocatability and
default-guide preservation. They do not test that a model chooses the right evidence
or that anyone prefers its prose. No trial responses, reviewer votes or scores are
manufactured in this directory.

## Next Quality Test

First review these meanings and legitimate exceptions, then execute development
probes to find failures. Their outputs must be kept as development evidence, not
counted as held-out confirmation. Do not repeatedly tune against reviewers and
present the final retry as an original result.

For a writing-quality claim, assemble **fresh real-paper body packets** outside
all prior pilot/development cases, with contribution-matched Abstract, Methods
and Results and broader domain coverage. Freeze exact candidate/common inputs,
author priorities, one draft/one revision budgets, model settings when available,
source access, judge reversal, fidelity checks and promotion criteria before
generation. Use a matched-context editorial control if attributing an effect to
the decision mechanism rather than added guidance exposure; otherwise disclose
that confound and evaluate only the bundle.

Retain all original completions, budget deviations, disagreements, negative
findings and located reviewer reasons. Collect prose-only understanding before
showing plans. Audit the actual measured objects and control scope separately
from preference. Evaluate losses of co-contributions, lawful standalone setup
and approximate implementations as well as positive cases. Keep human review
and author-abstract comparison separate from same-family model judgments.

No new promotion gate is preregistered here: actual fresh cases, access constraints
and evaluator calibration must be fixed first. Do not reuse the last pilot's failed
gate as an adjustable target, pool old votes, or promote this candidate on schema
tests or authored examples. Default guidance remains unchanged until an appropriate
new frozen trial supports the claimed improvement.
