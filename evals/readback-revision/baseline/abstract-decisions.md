# Abstract Decisions: Contribution Before Structure

Use for drafting, structurally revising, or comparing abstracts. For punctuation
or in-place editing, respect that narrower contract; do not rebuild the argument.
This is an editorial decision aid, not a validated predictor of acceptance.

## Decide What the Reader Must Retain

Use the existing contribution record and author priorities. Identify the central
addition, the evidence supporting it, and the condition that changes its meaning.
Keep this compact in the existing plan; do not require another artifact or a new
approval gate. If two materially different contribution priorities remain
unresolved, ask one focused question or label a provisional choice.

Select the [protocol](writing-protocols.md) only after this decision. A paper
with experiments need not have an empirical-method-centered abstract. A theory
plus diagnostic paper may need its theorem and counterexample more than a list
of candidate-generation modules. Do not automatically prioritize theory either:
the supported contribution and author's intent determine the allocation.

Before compressing, distinguish the main contribution, any co-contribution
essential to the paper's promise, and supporting details. A dominant result
does not automatically replace another contribution: faster updates and fewer
expert corrections, for example, answer different questions. After drafting,
check what the reader can still recover. If a co-contribution disappeared, trade
off a lower-value mechanism detail or per-task tally before dropping it. This
is not a requirement to mention every result or invent equal author priorities.
Preserve comparison scope when joining results measured against different baselines.
When baselines use different training regimes, retain that distinction: pretrained
models fine-tuned with default recipes and policies trained from scratch are not
all fine-tuned baselines. Attach each comparison to its actual group, metric,
and setting; a shared task does not imply a shared training budget or protocol.
Use the [contribution priority check](contribution.md#contribution-priorities-and-compression)
in the existing plan: check retained meaning against author priorities, not
keyword presence. A paper's contribution may be a reusable resource as well as
a method; conversely, not every resource or secondary result deserves abstract space.

## Choose Information by Function

| Contribution | Information that often carries the argument | Common loss |
| --- | --- | --- |
| Method | Specific obstacle, insight, mechanism, relevant comparison | Modules replace the reason the approach works |
| Theory | Objects, quantifiers, assumptions, result and implication | A conditional or necessary result becomes universal or sufficient |
| Theory plus implementation | Formal scheme, approximations, what is empirically observed | Implementation silently inherits the entire theorem |
| Diagnosis | Existing interpretation, discriminating test, finding, revised understanding | A negative result is disguised as improved performance |
| System | Workload bottleneck, design response, end-to-end tradeoff | Throughput is presented as latency or comparison conditions disappear |
| Dataset or tool | Missing capability, construction, evidence of utility, access scope | Size and feature count replace usefulness |

There is no mandatory opening, sentence count, numeric result, or future-work
ending. A result can precede mechanism when that improves understanding. Include
design lists when they express tested findings or explain interacting decisions;
omit inventories that crowd out the main contribution. A bound or diagnostic
observation may be the strongest evidence, not a benchmark percentage.

Keep comparison budgets and consequential assumptions beside their claims.
Distinguish observed improvement, statistically significant improvement,
equivalence, and certification. A failed certificate alone does not prove an
unsafe population rate. An empirical safety observation is not a guarantee.
Necessary qualifications should clarify an assertion, not accumulate as a
generic disclaimer paragraph. Preserve adverse evidence when omission would
misrepresent the overall result.

Scope the positive claim itself: a result on the tested tasks need not end with
an additional denial of universal superiority. Keep a limitation when removing
it would change the reader's interpretation, not merely to signal caution.
Compression should trade low-value detail for the paper's distinctive insight
and decisive evidence, rather than trade evidence for generic safety language.

Separate claim boundaries from unresolved reporting work. A simulator-only
result, conditional guarantee, or materially mixed outcome qualifies the claim
in the manuscript. A missing table unit or unavailable uncertainty definition
belongs in a separate author query unless that absence itself is the scientific
finding. Meanwhile use a supported descriptive claim, omit an uninterpretable
number, or mark the draft provisional; never silently guess or claim readiness.
Do not spend the abstract explaining that a source packet lacks information.

Do not upgrade descriptive source framing into stronger labels merely because
they sound academic. Claims such as general-purpose, reliable, robust, unified,
or state of the art need explicit scope and evidence. When a source says it
evaluates or studies a capability, retain that evidential verb unless the
supplied evidence supports the stronger claim.

Preserve the argument while compressing: the concrete problem, why the design
addresses it, and what the evidence establishes. These are information functions,
not a required sentence order; a method-first opening can be as effective as a
gap-first opening. Do not invent a literature gap to complete a template.
Remove repeated module names before losing a supported design rationale. Keep
that rationale distinct from a demonstrated benefit: using a pretrained model
to exploit prior semantic knowledge does not itself establish improved transfer.
Prefer the actual measured quantity (`action-generation throughput`, not
end-to-end latency or unspecified `efficiency`) and preserve absolute versus
relative gains. Conventional technical terms can repeat; do not replace them
with broader synonyms for variety. Hyphenation alone is not a quality gain.
An ending should add a supported finding or implication, not repeat the method
inventory or append an unsupported claim of a unified framework.

An author-prioritized but unestablished contribution is not automatically an
abstract promise. For an evidence-only research abstract, keep the supported
contribution in prose and put the missing claim and needed evidence in author
notes; labeling a wish as future work does not make it responsive to that task.
For a proposal or an explicit request for future directions, planned objectives
can belong in the abstract, clearly separated from completed findings. Resolve
the requested genre before allocating space, not by adding more caveats.

## Compare Good Drafts, Not Only Correct Drafts

First check source fidelity. Then compare drafts from the same evidence and
author priorities using located reasons rather than a single quality percentage:

- **Contribution retention:** Can a reader state the distinctive addition,
  rather than merely name the task and modules?
- **Argument connection:** Does the insight explain the design and does the
  chosen evidence answer the central promise?
- **Evidence selection:** Is the result decision-relevant, with its comparison
  scope intact, rather than simply the largest available number?
- **Compression:** Which important information is missing, and what took its
  place? Do not penalize every omission or reward maximal density.
- **Reader understanding:** Can the target reader reconstruct the contribution,
  reason for the approach, and evidential boundary without inventing links?

Treat grammatical, accurate text as eligible, not automatically excellent.
Allow ties and explain different valid allocations. Distinguish research
strength from how faithfully and effectively an abstract communicates it.
Neither paper fame nor a model judge's confidence establishes prose quality.

For a measured comparison, freeze inputs and priorities before generation,
retain raw drafts, anonymize versions, and record judge disagreements. Do not
equate a shorter draft with better compression: record the agreed word-count
rule, check the generation budget, and report violations without padding or
silently editing raw outputs. Treat a published abstract with a different length
or richer source access as an editorial reference, not a controlled A/B baseline.
Do not retroactively change criteria to favor a version. Calibrate evaluators on
factually valid but contribution-weak variants as well as factual errors; use
held-out topics to assess transfer. Same-family model judging is not human
validation. See [calibration fixtures](../evals/abstract-quality/README.md).

## Learn from Exemplars Selectively

Read a few contribution-matched [exemplar notes](abstract-exemplars.md), not the
entire collection for each draft. Notes are independent editorial analyses of
public abstracts, not copied templates or evidence supporting the user's paper.
Learn the function of a choice, including when not to make it; never transplant
claims, superiority language, or data from a reference into a new manuscript.
