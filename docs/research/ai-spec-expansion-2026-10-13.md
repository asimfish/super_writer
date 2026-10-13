# AI Specification Expansion: 2026-10-13

## Scope and Evidence

This round addresses the [previously deferred gaps](ai-spec-expansion-2026-10-12.md):
multimodal support, source versus process faithfulness, and sequential embodied
evaluation. It admits 14 original entries: three rules, three claim-use senses
and eight terms. Version 0.3 has 67 entries, nine topics, five levels and seven
domains. Seven new primary-source records bring the source count to 19.

These are manually curated research references, not new unseen quality-test
papers. Reading a definition, passing retrieval contracts and writing a worked
example do not establish a writing-quality improvement. No cited prose, PDF,
figure, implementation or object synonym list is redistributed.

## Actual Reading

| Primary source | Read location | Bounded observation |
| --- | --- | --- |
| [FActScore, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.741/) | Abstract/introduction; PDF Section 3.1, printed page 12078 | Atomic support is reference-relative; aggregation conditions on responses and assumes a suitable reference. |
| [ALCE, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.398/) | Abstract; PDF Sections 3.1-3.4, especially 3.3, printed pages 6468-6469 | Correctness, fluency and citation quality are separate; joint support and individually sufficient citations are allowed. |
| [Object Hallucination, EMNLP 2018](https://aclanthology.org/D18-1437/) | Abstract/introduction; PDF Section 2.1, printed pages 4037-4038 | CHAIR has object-instance and sentence-level denominators, bounded vocabulary and reference coverage. |
| [Explanation faithfulness, ACL 2020](https://aclanthology.org/2020.acl-main.386/) | PDF abstract/introduction, Section 2, Section 5 | Plausible explanations and explanations reflecting prediction processes are different targets. This is an opinion paper. |
| [CALVIN v2](https://arxiv.org/html/2112.03227v2) | Abstract; Section III-C challenge, training/test conditions and evaluation metrics | Single-goal and state-carrying sequential rollouts are distinct protocols. |
| [SayCan v2](https://arxiv.org/html/2204.01691v2) | Section 3 and Algorithm 1; Section 5 setup/metric definitions | Language usefulness, state-conditioned skill value, valid plans and physical completion have different roles. |
| [MDETR v2](https://arxiv.org/abs/2104.12763v2) | Abstract only; [author project](https://ashkamath.github.io/mdetr/) summary and text-conditioned box-evaluation description | Language-to-region targets operationalize localization; visual conditioning is not automatically verified alignment. |

The published MDETR CVF PDF body could not be retrieved in this session. The
pinned abstract and author page are an explicit fallback, not a body-review
substitute. ALCE Appendix E, complete FActScore estimators, later CALVIN release
code and full experiment/theorem audits were not reviewed. ACT Section IV-A and
Algorithms 1-2 were read in the previous round and reused only for the
prediction-versus-execution distinction.

## Editorial Inferences

Source observations are kept separate from local design choices:

- FActScore puts the construct and its assumptions before estimation. We use
  this to ask what a score measures before interpreting it, not to prescribe
  the paper's section order to every manuscript.
- ALCE separates evaluation targets, making it possible to discuss when a
  seemingly good metric still leaves the reader's question unanswered.
- The object-hallucination introduction poses questions about error behavior
  and evaluation coverage. We transfer that question-led explanatory function,
  not its wording, findings or a fixed question count.
- CALVIN declares rollout conditions; SayCan distinguishes selection and
  completion. We use those distinctions to write an answer about task progress
  or failure stages rather than a sequence of percentages.

The [worked paragraphs](../../examples/ai-writing-spec/grounding-and-horizon.md)
use only invented facts. Their editorial organization is a local inference,
not an empirical demonstration that the source style improves our generation.

## Classification and Deduplication

`grounding_faithfulness` is a ninth topic because the shared question is the
relation between an output and its reference: text, visual targets, action state
or model process. `citation_support` alone does not cover these referents.
`multimodal` is a seventh domain, currently represented by vision-language
examples; it does not claim audio, video or all-modalities coverage. Existing
facets intersect these additions without a new schema or retrieval engine.

| Admitted IDs | Existing owner boundary |
| --- | --- |
| `ai.rule.evaluation-target`, `ai.rule.evidence-modality`, `ai.rule.failure-localization` | `results-validation.md`: construct, reference and stage interpretation; quantities still belong to the existing reporting rule. |
| `ai.usage.grounded`, `ai.usage.faithful`, `ai.usage.hallucination-free` | `academic-expression.md`: conditional senses, not universal approved/banned words. |
| `ai.term.factual-precision`, `ai.term.object-hallucination`, `ai.term.visual-grounding` | `results-validation.md`: operational targets and coverage. |
| `ai.term.citation-recall`, `ai.term.citation-precision` | `citation.md`: metric semantics; the existing citation-support rule still owns locating claim support. |
| `ai.term.robotic-affordance`, `ai.term.task-chain-success`, `ai.term.long-horizon` | `writing-protocols.md`: state, sequence and horizon definitions; existing action-chunking and feedback terms stay separate. |

All previous 53 records are unchanged in this round. Source-consistency is a
sense of `faithful`, not an additional near-duplicate term. No new generic
atomic-support rule is added: the existing citation-support rule already owns
that decision. The 130 pinned library cards, 16 protocol guides / 30 variants, venue profiles and
frozen argument-transfer guide are not expanded by these additions.

## Review and Next Frontier

The authoring agent performed source-located self-review and deduplication;
there was no independent curator. Per-entry source notes disclose the actual
location and inference. Exceptions retain complete-reference negative evidence,
joint citation support, bounded zero-error observations, valid interventions
and domain-specific horizons rather than blanket prohibitions.

Engineering receipts belong in [validation](../validation.md). No fresh blind
generation/review, activation evaluation, Windows run, remote CI, global skill
installation, GitHub commit or push is claimed for this curation round.

Still deferred: relation/attribute hallucination beyond the object-only case,
video/audio grounding, adversarial or conflicting reference support,
cross-agent faithfulness, real trajectory failure adjudication and an
independent curator review. These require their own located sources and cases,
not retroactive expansion of the reviewed read scopes.
