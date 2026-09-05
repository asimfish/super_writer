# Raw Protocol

Educational synthetic experiment; no real-world participants or datasets.

- Target: `f(x) = 2*x + sin(4*pi*x)`.
- Training: 40 uniform inputs in `[0,1)`, each followed by uniform noise in `[-0.5,0.5]`.
- Seeds: 11, 22, 33, 44, 55, using `random.Random`.
- Methods: unweighted nearest-neighbor regression with k=1 and k=5; ties use row order.
- Evaluation: 101 midpoint-grid inputs in `(0,1)` and another 101 in `(1,2)`.
- Targets at evaluation: noiseless function values.
- Metric: mean squared error per training seed, then mean and sample SD across seeds.
- Not performed: significance test, real-world benchmark, comparison with parametric
  models, hyperparameter selection, new experiment requested in a reviewer response.
- The setup is a teaching exercise, not a preregistered study.

`experiment.py` is the executable source of truth. `results.csv` contains its
per-seed measurements; `summary.json` records the aggregation and parameters.
