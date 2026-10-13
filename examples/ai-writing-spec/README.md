# AI Writing Boundaries: Six Synthetic Cases

These are development examples, not real-paper results, blind tests or proof of
improved writing. Definitions and complete conditions/exceptions live in the
[canonical catalog](../../references/ai-writing-spec.json); links below open its
atlas records. All numbers and scenarios are synthetic.

The next [five worked cases and Results paragraphs](grounding-and-horizon.md)
cover grounding, faithfulness, citation measures and sequential task evaluation.
The [four clarity-context cases](clarity-context.md) cover referents, compounds,
procedure order/literals and legitimate academic voice/temporal wording.

## 1. Context Is Not Fine-Tuning

Facts: two labeled examples enter the prompt; parameters do not change.

- Supported: "We provide two labeled in-context examples without updating model parameters."
- Misleading: "We fine-tune the model on two examples."
- Why: the update procedure changes. Legitimate exception: an actual pipeline
  can combine prompting and adapter training; report both.

[Entry: in-context learning](../../docs/writer-atlas.html#ai.term.in-context-learning).

## 2. Prediction Horizon Is Not Feedback Cadence

Facts: six actions are predicted, but a fresh observation affects the command each step.

- Supported: "The policy predicts six-action chunks and recomputes commands from fresh observations at every step."
- Misleading: "The policy runs open-loop for six steps."
- Why: prediction length is mistaken for feedback interval. Legitimate exception:
  fixed high-level targets may coexist with closed-loop low-level tracking.

[Entries: action chunking](../../docs/writer-atlas.html#ai.term.action-chunking),
[open-loop](../../docs/writer-atlas.html#ai.term.open-loop),
[closed-loop](../../docs/writer-atlas.html#ai.term.closed-loop).

## 3. Retrieval Does Not Certify Support

Facts: retrieved passages reach the generator; statement-level support is not tested.

- Supported: "The generator conditions on retrieved passages; statement-level support remains unevaluated."
- Misleading: "All generated statements are grounded because the system uses RAG."
- Why: input availability is not output verification. Legitimate exception:
  a separately conducted support evaluation can justify its own bounded claim.

[Entry: RAG](../../docs/writer-atlas.html#ai.term.retrieval-augmented-generation).

## 4. Prefer an Answer to a Sequence of Scores

Facts: an index changes, weights and queries stay fixed, retrieval identifiers are
logged; there is no answer-correctness measurement.

- Supported: "With model weights and queries fixed, replacing the index changes which documents are retrieved; this experiment tests retrieval responsiveness, not answer correctness."
- Misleading: "The new index improves reasoning and guarantees accurate answers."
- Why: explaining a result cannot invent the implication. Legitimate exception:
  a descriptive dataset report need not pretend to be a controlled mechanism test.

[Entry: result answer](../../docs/writer-atlas.html#ai.rule.result-answer).

## 5. Preference Labels Do Not Define the Optimization Pipeline

Facts: machine-labeled preference pairs train a direct objective; no separate
reward network is fitted.

- Supported: "We optimize a direct preference objective on machine-labeled pairs, without fitting a separate reward network."
- Misleading: "We train a human reward model and optimize it with RL."
- Why: both provenance and optimization stages change. Legitimate exception:
  an implicit reward representation does not imply a separately trained network.

[Entry: preference optimization](../../docs/writer-atlas.html#ai.term.preference-optimization).

## 6. A Hedge Does Not Create Causal Evidence

Facts: a pilot changes caching and other settings together; fewer failures are observed.

- Supported: "The pilot suggests a possible reduction in failures, although the changed settings prevent attribution to caching alone."
- Misleading: "The pilot suggests that caching eliminates control failures."
- Why: `suggests` does not repair elimination or identification overreach.
  Legitimate exception: valid direct evidence should not be weakened by obligatory hedging.

[Entries: suggest](../../docs/writer-atlas.html#ai.usage.suggest),
[causal](../../docs/writer-atlas.html#ai.usage.causal).

Use the [curation workflow](../../references/ai-spec-learning.md) to turn a new
reader confusion into a reviewed candidate, not a blanket ban.
