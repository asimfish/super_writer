# AI Writing Specification: Curated Expansion, 2026-10-12

## Gap and Review Status

The initial 36 records separated rules, claim words and terminology, but did not
support reader-problem or writing-level selection. This round adds orthogonal
facets and 17 entries: 3 organizational/support rules, 6 conditional claim uses,
and 8 technical terms. Total: 53 records, not 53 writing templates.

Reviewer: the implementing agent, performing editorial self-review. No independent
reviewer or new blind writing-quality experiment has been run. The six sources
below were read only to the stated scope; all examples are original and synthetic.
These works are development references and cannot be counted as unseen tests.

## Sources and Admission Decisions

| Primary source | Actual scope read | Observation and local use | Admitted IDs |
|---|---|---|---|
| [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist), live page read October 12 | Claims, limitations, assumptions, reproducibility, experimental settings, variability and compute questions | Reporting questions motivate local scope guards, not a fixed vocabulary or year-specific certification | `ai.usage.suggest`, `.state-of-the-art`, `.scalable`, `.novel` |
| [GPT-3 v4](https://arxiv.org/abs/2005.14165v4) | Abstract only | Prompt demonstrations and weight optimization must not be conflated | `ai.term.in-context-learning` |
| [RAG v4](https://arxiv.org/html/2005.11401v4) | Abstract, Introduction, Section 2, Sections 4.4-4.5 including index hot-swapping | Connected retrieval/generation operations and question-led result subsections motivate local editorial choices; external memory updates are distinct from weight updates | `ai.rule.paragraph-function`, `.result-answer`, `.citation-support`; `ai.usage.enable`; `ai.term.retrieval-augmented-generation` |
| [Offline RL tutorial v3](https://arxiv.org/abs/2005.01643v3) | Abstract only | Previously collected data and new online interaction are phase-sensitive distinctions | `ai.term.offline-reinforcement-learning` |
| [ACT v1](https://arxiv.org/html/2304.13705v1) | Section IV opening, IV-A, Algorithms 1-2 | Demonstration targets, chunk prediction, fresh observations and low-level tracking are separate parts of the control description | `ai.term.imitation-learning`, `.action-chunking`, `.open-loop`, `.closed-loop` |
| [DPO v3](https://arxiv.org/html/2305.18290v3) | Abstract and Section 4, equations 4-7 and pipeline | A direct preference objective is distinct from fitting a separate reward model and then running RL; assumptions still matter | `ai.term.preference-optimization` |

`ai.usage.causal` is explicitly source-free local synthesis about identification
and claim scope, not a new instruction attributed to the checklist. Entries with
source links retain per-record location and observation; links do not certify the
entry or support user-project results. Existing 36 records gain facets and honest
context notes, without silently changing their original wording.

## Deferred or Rejected

- Universal sentence counts, mandatory paragraph move order, passive-voice bans
  and global word approval remain rejected: research prose needs legitimate exceptions.
- A general causal-inference taxonomy is deferred until relevant primary methods
  are read; the conditional word-use guard is not a causal-estimation manual.
- `grounded`, `faithful` and `hallucination` evaluation glossaries need dedicated
  primary evaluation definitions before admission. RAG presence alone is not that audit.
- Reasoning traces, multimodal grounding and long-horizon manipulation terminology
  are next coverage candidates, not implemented entries or scheduled research jobs.
- No paper-specific result, figure, passage or third-party dictionary is copied.
  No universal writing improvement is inferred from exemplar organization.

## Follow-Through

The [curation workflow](../../references/ai-spec-learning.md) defines the next round.
The [classification ADR](../designs/adr-002-classification-and-curation.md) records
the schema and compatibility decision. Actual executed checks belong in
[validation](../validation.md), not in a prospective success statement here.
