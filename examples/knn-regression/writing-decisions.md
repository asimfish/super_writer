# Evidence and Writing Decisions

This is a worked answer. Withhold it, the manuscript, and the response example
when running a fresh writing exercise.

| Manuscript unit | Evidence | Writing decision | Boundary |
|---|---|---|---|
| Abstract | Four aggregate errors in `materials/summary.json` | Report both domains, not just the favorable one | No significance or universal robustness claim |
| Introduction | One fixed protocol with two estimators | Frame an evaluation question, not a new algorithm | No novelty claim for nearest-neighbor regression |
| Background | Hastie et al., 2009 | Cite only the conventional estimator background | The book does not substantiate our measured errors |
| Protocol | `experiment.py` and raw protocol | Name draw order, seed unit, noise, grid, and metric | Grid points are not independent training runs |
| Results | Means and sample SD from five seeds | Keep the reversed extrapolation ranking | SD is not a confidence interval |
| Interpretation | Sorted distances for queries beyond all training inputs | Derive constant extrapolation predictions | This does not determine the ranking for every signal |
| Limitations | Methods and settings actually executed | Name missing baselines and scope | Do not turn proposed experiments into completed results |

## Before and After

Before: "Five-neighbor regression significantly outperforms one-neighbor
regression and is robust to distribution shift."

After: "On the in-domain grid, five-neighbor regression reduces mean MSE from
0.1083 to 0.0851 across five fixed training seeds. On the extrapolation grid,
mean MSE increases from 2.6891 to 3.7012; the in-domain advantage does not
extend to this tested setting."

The revision corrects scope and reports the adverse result. It does not claim
that a particular sentence pattern, word frequency, or AI-detector score makes
the text suitable for a top conference.
