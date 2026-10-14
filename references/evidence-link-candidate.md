# Evidence-Linked Drafting: Candidate 0.1

**Status: experimental, not promoted.** Use only when the author or an evaluation
explicitly selects this candidate for structural drafting or revision. Do not
apply it to punctuation-only edits, load it for every paragraph, or claim that it
has improved writing. The [latest pilot](../docs/ai-spec-pilot-evaluation.md)
motivates these hypotheses; its failed gate is unchanged.

This is a decision procedure inside the existing
[rationale matrix](writing-rationale-matrix.md) and
[exemplar dossier](exemplar-learning-dossier.md), not another required report.
For a bounded passage, a brief internal note is enough. Keep planning labels and
source-packet queries out of manuscript prose.

## 1. Select the Evidence That Answers This Promise

Start with the author's supported contribution and the passage's job. State the
answer a reader should retain: not "better robots", but, for example, "training
across more scenes improves performance at equal dataset size on these tasks."
If that answer exceeds the evidence, narrow it before allocating words. Author
priority does not make an unmeasured benefit a completed finding.

When several facts compete for space, compare the plausible candidates against
that answer. What does each establish, and what alternative would remain if it
were the only evidence retained? Dataset size establishes scale, not diversity's
utility. A size-matched contrast may address diversity; adding more data does
not separate diversity from quantity. Prefer the evidence that resolves the
active question, not the largest gain or the most detailed table row.

Record the choice and one consequential deferral in the existing evidence and
planned-move cells when a real tradeoff exists. Do not invent competing facts,
alternative explanations or a mandatory ablation. Construction evidence can
support a resource contribution; a derivation can support theory; an adverse
observation can support a diagnosis. If no evidence answers the proposed promise,
narrow the promise, state the supported negative finding, or query the author
outside the manuscript. Adding a caution cannot supply missing support.

Two independently supported promises can need two evidence links. Preserve the
meaning of both when author priorities require them; remove a lower-value detail
before combining results from different comparators into a fictitious single gain.

## 2. Bind the Finding Before Choosing Its Sentence

For the selected evidence, identify the evaluated object, measured event or
quantity, actual comparator, and condition that changes the interpretation.
These are checks on a relationship, not a four-slot sentence template.

Use the evaluated object as the subject where the predicate concerns performance:
policies trained on trajectories succeed; trajectories themselves do not succeed
at the benchmark. A dataset can legitimately have higher coverage, and a metric
can have lower error. Choose by what was evaluated, not a ban on inanimate subjects.

Attach a necessary shared backbone, timing boundary, population or assumption
where the reader interprets that comparison. Do not assert matching when several
factors change together. Prefer the actual joint comparison over an isolated
mechanism claim. If the control is already clear, do not restate it mechanically.

Embedding is not always better: a common protocol can be introduced once before
several results, a complex setup may need its own sentence, and Methods may need
explicit dependency steps. The test is whether the reader can assign the condition
to the right result without breaking the result's explanation, not adjacency at
any cost. Preserve legitimate passive voice and technical terminology.

## 3. Turn the Link Into an Argument

Choose an order that lets the next sentence answer the question raised by the
previous one. Draft from the selected relationship, not by paraphrasing every
evidence item in input order. No universal gap-first or method-first opening is
required.

- **Abstract:** connect the foregrounded addition to its most informative support.
  If space forces a choice, remove a construction tally before dropping the test
  that makes the opening motivation credible. A scale-focused resource abstract
  can reasonably make the opposite allocation.
- **Methods/analysis:** explain the operation and the specific obstacle or
  ambiguity it addresses when that is the passage's job. Defining Pearson
  correlation as linear association does not explain why a complementary ranking
  measure is needed. For a definition-only request, a correct definition is enough.
  Separate an exact derivation, design intent and an observed intervention effect.
- **Results:** say what the comparison answers, place the finding and its necessary
  scope together, then add only an interpretation or next question that advances
  the argument. A null or worse ablation narrows an attribution; it need not become
  a positive mechanism story.

State an interpretation once at the point it earns its place. An already scoped
claim about ranking need not end with another generic denial of universal success.
Keep a further qualification if it rules out a materially different reading, such
as interpreting preserved rankings as accurate absolute rates. Repetition may be
necessary across independently read captions or sections; do not delete it by count.

## 4. Read Back Without the Plan, Then Repair the Smallest Loss

Read only the draft first. What addition, operation or finding does it communicate?
Which evidence answers it, what is being compared, and under which condition?
Then compare this reading with the author's facts and the existing planned move.

For a difficult passage, try a targeted counterfactual: remove the selected support,
or change the actual control. Would the prose still make the same persuasive claim?
If so, check for a missing link or unsupported strength. This is an editorial probe,
not a word-matching test, a quality score or a demand to rewrite every paragraph twice.

Repair the lost relation in its actual sentence. Do not add plan jargon, an invented
mechanism, every available measurement or a boilerplate disclaimer. In a full-paper
task, locate the retained relation and scope in `Final Text Check`; a structural
`PASS` does not prove that a reader understands it.

## Development and Evaluation

[Eight counterfactual families](../evals/evidence-link/README.md) change a priority,
condition, metric, assumption or outcome to require a different decision. They
are original synthetic development inputs, with private editorial expectations;
they are not published science, model outputs or blind quality results. The
packet tool withholds those expectations but does not enforce agent isolation.

Test this candidate separately from the whole AI-spec catalog. Freeze exact inputs,
budgets, model access and promotion criteria before fresh generation. Record the
added guidance exposure, retain all raw drafts and disagreements, and audit factual
scope before comparing writing. These known probes and the earlier pilot cases
cannot be held-out confirmation. See the [evaluation boundary](../evals/evidence-link/README.md#next-quality-test).
