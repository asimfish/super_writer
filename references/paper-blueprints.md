# Contribution-Specific Blueprints

These are adaptable argument designs, not official section templates or claims
that one outline wins acceptance. Combine the closest design with the exact
[venue profile](venue-profiles.json), supplied evidence and author decisions.
Use existing contribution, writing-rationale and results-validation artifacts;
do not introduce another mandatory planning document.

| Contribution | Argument order to consider | Evidence obligations | Common failure |
|---|---|---|---|
| Method / algorithm | Problem and restrictive assumption; design insight; mechanism; controlled evaluation; boundary | Closest comparable methods, implementation detail, fair budgets, appropriate ablations, negative cases | A component list described as novelty; gains with unmatched resources |
| Theory | Precise problem; assumptions; formal result; interpretation; proof; boundary or counterexample | Quantifiers, dependencies, proof of the actual statement, relation to prior bounds | Turning a range bound into an accuracy or convergence claim |
| Dataset / benchmark | Missing evaluation capability; construction; governance; protocol; diagnostic results; limitations | Rights/consent as applicable, split design, leakage audit, annotator process, baselines, intended use | Dataset size alone treated as contribution; test data used for selection |
| Systems / efficiency | Workload and constraint; bottleneck; system design; end-to-end measurement; trade-offs | Hardware, precision, batch size, timing boundary, throughput/latency distinction, quality-cost comparison | Unmatched hardware; inference-only timing presented as end-to-end speedup |
| Negative result / replication | Testable expectation; faithful setup; observed result; uncertainty; competing explanations; scoped implication | Baseline reproduction fidelity, failed and successful controls, power/variability, missing conditions | "No significant difference" called equivalence; a failed run called impossibility |
| Survey / position | Bounded question; selection basis; organizing axes; synthesis; disagreements; supported agenda | Search/selection scope, balanced coverage, traceable comparisons; arguments distinguished from observations | Author-by-author summaries; a position claim presented as consensus |

## Writing Units

- **Title:** name the object or contribution; do not advertise superiority that
  the evidence does not establish.
- **Abstract:** problem and scope, insight or result, method where relevant,
  strongest verified evidence, and the boundary needed to interpret it. Theory
  abstracts need a precise result, not invented experimental numbers.
- **Introduction:** explain why the concrete gap matters, why the closest work
  does not settle it, and how this paper's design/result addresses it. Contribution
  bullets should make distinct, verifiable promises.
- **Related work:** compare families along technical axes. Preserve foundational
  work where it supplies the formulation; a recency target cannot exclude it.
- **Method:** define objects before operations, match equations to prose, expose
  assumptions and implementation choices. Do not merge conceptual motivation
  with claims of experimental verification.
- **Results:** question, protocol, finding, evidence pointer, interpretation and
  exception. Describe what a table establishes, not every cell in prose.
- **Conclusion / limitations:** state the supported outcome and remaining
  boundary. Do not add new experiments, universal claims or perfunctory caveats.

## Venue Calibration

Treat these as editorial starting points, then learn from relevant accepted
papers and the venue's current review criteria:

- ICML/ICLR/NeurIPS: expose assumptions, comparison conditions and the technical
  contribution early. NeurIPS contribution types need different evidence;
  a negative-results or theory paper is not a generic method paper in disguise.
- CVPR/ECCV: make the visual task and evaluation protocol inspectable; captions
  identify what panels measure and the relevant failure boundary. ECCV main and
  rebuttal layouts are different.
- ACL/EMNLP: make language/task, data selection, evaluation and responsible-NLP
  implications explicit. A four-page short paper needs a narrower complete claim.
- AAAI: use the actual main-track instructions and author kit before formatting;
  do not infer main-track constraints from a symposium using the same style.

Allocate space to evidence that carries the contribution. Page allocations and
section counts are planning choices, not universal gates. Cut redundancy before
moving essential proof, experimental protocol or adverse results out of sight.
