# Section, Paragraph and Table Protocols

Read one protocol for the current writing unit, not the entire JSON index.
These are original writing structures from Super Library, not quotations from
accepted papers, official author kits, or evidence of acceptance gains.

## Select a Resource

Resolve these script paths against the installed skill directory:

```bash
python scripts/writing_guide.py --list
python scripts/writing_guide.py introduction --variant theory-analysis
python scripts/writing_guide.py "实验分析" --variant result-paragraph --format json
python scripts/writing_guide.py "效率表" --format json
```

Exact protocol IDs and English/Chinese aliases select one record. Unknown or
ambiguous selectors fail instead of falling back. `--variant` selects one
structure without dropping inputs, checks, domain overlays or warnings.
The default output budget is 16,000 characters including the final newline;
`--max-chars` accepts 512..50,000. If a complete record cannot fit, no partial
output is returned. Choose one variant or explicitly increase the budget.

## Apply to Actual Material

1. Select the contribution-specific whole-paper [blueprint](paper-blueprints.md)
   only when the request is whole-paper design. A bounded section request does
   not authorize a full workflow.
2. Select the section protocol and a variant appropriate to the supplied work.
   Check each move against evidence: present, missing or not applicable. Reuse
   the existing rationale matrix/section plan rather than creating another gate.
3. Interpret `required: true` as a check when applicable, not an obligation to
   invent a paragraph, novelty claim, experiment, weakness or mitigation. Ask
   the minimum necessary question or narrow the draft when essential input is
   missing. Do not invent empirical results for a theory-only paper.
4. Draft using verified author material. Keep numbers, units, denominators,
   conditions, uncertainty, negation and unrun-work status unchanged. A rebuttal
   need not concede an unsupported criticism or invent a manuscript location.
5. Retrieve a few related [language cards](writing-library.md) if useful.
   `available_card_ids` are bundled; `unbundled_card_ids` are catalog pointers
   only. In particular, an excluded attested phrase is not silently imported.
6. Run the selected protocol's verification and the existing stage guards.
   Check current official venue/year/track/stage rules separately. Neither the
   protocol nor its retrieval tests attest to the quality of a drafted paper.

## Inventory: 16 Protocols, 30 Variants

| Protocol ID | Structural variants | Scope |
|---|---|---|
| `abstract` | 3 | Empirical method, resource/benchmark, theory |
| `introduction` | 3 | Technique, new setting/resource, theory/analysis |
| `experiments` | 3 | Empirical, real robot, theory plus empirical |
| `experiments.analysis` | 3 | Result, ablation, failure paragraph |
| `experiments.table.common` | 1 | Caption and comparison contract |
| `experiments.table.main_results` | 1 | Method-by-task comparison |
| `experiments.table.ablation` | 1 | Component matrix |
| `experiments.table.generalization` | 1 | Explicit train/test shift |
| `experiments.table.efficiency` | 1 | Deployment profile |
| `experiments.table.sensitivity` | 1 | Parameter sweep |
| `related_work` | 2 | Taxonomy-first, concept evolution |
| `method` | 2 | Model/objective/procedure, algorithmic |
| `limitations` | 2 | Empirical boundary, assumptions/resources |
| `conclusion` | 2 | Empirical closure, theory/resource closure |
| `rebuttal` | 2 | Clarification, established limitation |
| `translation` | 2 | Technical prose, definitions/literature |

Experiments include domain overlays for RL, world models, embodied AI and VLA.
The upstream peer-review protocol is excluded; producing a referee report is
not the writer's role. These counts do not add to the number of venue formats.

## Five LaTeX Table Skeletons

| Asset | Evidence needed before filling |
|---|---|
| [Main results](table-templates/main_results.tex) | Comparable data/pretraining, compute/interaction budgets, metrics and uncertainty |
| [Ablation](table-templates/ablation.tex) | Matched controls, component interactions, measured deltas |
| [Generalization](table-templates/generalization.tex) | Held-out axis, model-selection separation, reference/shift conditions |
| [Efficiency](table-templates/efficiency.tex) | Hardware, precision, batch, warm-up, end-to-end measurement scope |
| [Sensitivity](table-templates/sensitivity.tex) | Tested range, fixed factors, selection rule and validation split |

The associated protocol returns the complete TeX skeleton, required `booktabs`
package, license and hashes. It reads files only; it neither writes a table nor
compiles TeX. Edit a project copy, never the installed resource. Replace every
`SL_*` using verified inputs, including metric names/directions and captions;
the raw placeholders intentionally are not a ready-to-compile result table.
Do not fill missing values with zeros or infer significance from bold cells.

Long headers are wrapped and manual vertical spacing removed. Retain the
official venue's fonts, margins and float rules. The fixtures test an article
with 23 mm margins in single-column and two-column full-width `table*` layouts,
not a narrow column or arbitrary long content. Compile the actual paper and
inspect every page after filling cells; do not shrink a table to hide overflow.

Provenance: [pinned upstream](../UPSTREAM.md#writing-resource-extension-2026-09-07),
[CC0 protocol data](../DATA_LICENSE), [MIT table license](table-templates/LICENSE).
Maintenance reproduces both JSON files, all five tables and licenses via
`tools/import_writing_library.py --check`; no runtime network or model is used.
See the [worked protocol application](../examples/protocol-application/README.md).
