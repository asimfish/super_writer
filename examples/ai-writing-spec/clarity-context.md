# Clarity Without a Controlled-Language Transplant

All facts and passages below are original synthetic examples. They demonstrate
editorial decisions, not a measured writing gain, an official STE rule lookup or
domain-specialist verification. Read the [context guide](../../references/clarity-context.md)
for conditions and legitimate exceptions. No command below is executed.

## 1. Name the Update Target

Facts: a teacher supplies pseudo-labels to a student; teacher parameters are
fixed and only student parameters change.

- Ambiguous: "The teacher supplies pseudo-labels to the student, and it is updated."
- Precise: "The teacher supplies pseudo-labels to the student; only the student is updated."
- Why: `it` admits two different targets. The passive clause is useful because
  the student is the comparison focus; changing the voice is not the main repair.
- Exception: an unambiguous pronoun can remain; if the materials do not say
  which parameters change, the editor must not infer the target.

[Definition and referents](../../docs/writer-atlas.html#ai.rule.definition).

## 2. Unpack a Relation, Retain a Standard Term

Facts: the study evaluates a policy in environments whose dynamics change over
time. Environment change is not a modifier of the evaluation policy. Its model
type is explicitly defined as a vision-language-action model.

- Ambiguous: "We use time-varying environment policy evaluation."
- Precise: "We evaluate the policy in time-varying environments. The policy uses the defined vision-language-action model."
- Why: unpacking the noun group exposes which entity varies. Replacing the model
  type with `simple visual model` would erase a supplied technical distinction.
- Exception: a conventional compound with a clear definition can remain; there
  is no universal three-word noun limit for academic prose.

[Definition](../../docs/writer-atlas.html#ai.rule.definition) /
[term consistency](../../docs/writer-atlas.html#ai.rule.term-consistency).

## 3. Preserve Preconditions and the Action Target

Facts: verify a checkpoint checksum before removing only intermediate shards.
Keep the final archive. The literal error code for a failed check is
`CHECKPOINT_MISMATCH`; the interface is not being changed.

- Wrong sequence: "Remove all shards and then verify the checkpoint checksum."
- Precise: "After verifying the checkpoint checksum, remove only the intermediate shards; retain the final archive. If verification fails, report `CHECKPOINT_MISMATCH`."
- Why: the first version changes both order and target. Renaming the literal
  error to `BAD_CHECKPOINT` would also change the interface rather than its prose.
- Exception: the safeguard is supplied here, not invented by the editor. A
  declared simultaneous operation may stay simultaneous; editing instructions
  does not authorize running them.

[Procedure order](../../docs/writer-atlas.html#ai.rule.procedure-order).

## 4. A Known Actor Does Not Make Passive Voice Wrong

Facts: a declared script normalizes trajectories before training. The paragraph
focuses on the dataset transformation. During evaluation, a stated buffer has
been accumulating observations since rollout start.

- Faithful wording: "The trajectories are normalized by the declared script before training. The buffer has been accumulating observations since the rollout began."
- Meaning-changing simplification: "We normalize trajectories during training. The buffer stores one observation."
- Why: the actor is known, yet passive voice preserves the transformation focus.
  Simplifying tense and phrasing changes timing and accumulation, not just style.
- Exception: active wording such as "The script normalizes trajectories before
  training" is also valid. No change is required solely because a sentence is
  passive or uses a perfect/progressive construction.

[Evidence relationships](../../docs/writer-atlas.html#ai.rule.evidence) /
[qualification](../../docs/writer-atlas.html#ai.rule.qualification).

Use local entry IDs for editorial explanations when useful, not unverified
standard rule numbers. A successful retrieval or preservation check is not
certification, independent review or proof that a model now writes better.
