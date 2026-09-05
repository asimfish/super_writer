---
title: "An Average Is Not a Guarantee: Making Assumptions Visible"
author: "Super Writer worked example"
date: "September 2026"
abstract: |
  A bound on an aggregate is easy to overstate when its assumptions disappear
  between a proof and an abstract. This educational note restates the elementary
  range bound for a convex combination, proves it directly, and gives a signed-
  weight counterexample. Nonnegative weights that sum to one keep a weighted
  average within the range of its inputs. The result does not establish that
  every input is accurate, that the average is unbiased, or that a predictive
  model generalizes. The purpose is to demonstrate assumption-aware theoretical
  writing, not to present a new theorem or a conference submission.
---

# The Writing Problem

The sentence "aggregation guarantees reliable predictions" mixes a mathematical
property with an empirical promise. Even when an aggregate satisfies a range
bound, nothing in that bound establishes that the inputs are close to an
unknown target. The proof and the headline need to answer the same question.

We use a convex combination, a standard object in convex analysis
[@boyd2004], to separate the two statements. The argument below is written
independently for this example. It is elementary and carries no novelty claim.

# Setting and Proposition

Let $y_1,\ldots,y_n$ be real numbers, with finite $n\geq 1$. Let
$w_i\geq 0$ for every $i$, and suppose $\sum_{i=1}^n w_i=1$.
Define the aggregate

$$
\bar y=\sum_{i=1}^n w_i y_i.
$$

**Proposition.** Under these assumptions,

$$
\min_i y_i\;\leq\;\bar y\;\leq\;\max_i y_i.
$$

The statement is deterministic. It does not assume a training distribution,
sampling independence, or a probabilistic model. Conversely, it does not
provide any conclusion about those quantities.

# Proof and Assumption Use

Write $m=\min_i y_i$ and $M=\max_i y_i$. For every index,
$m\leq y_i\leq M$. Since $w_i$ is nonnegative, multiplication preserves
both inequalities: $w_i m\leq w_i y_i\leq w_i M$. Summing over indices
gives

$$
m\sum_i w_i\;\leq\;\sum_i w_i y_i\;\leq\;M\sum_i w_i.
$$

Normalization, $\sum_i w_i=1$, gives the claimed interval. This identifies
where each assumption enters: nonnegativity preserves order, while
normalization returns the bounds to the original scale.

For unnormalized nonnegative weights with positive total $W$, the same
argument applies to $w_i/W$, and hence to $(\sum_i w_i y_i)/W$.
If $W=0$, that expression is undefined. Dropping the denominator is not an
equivalent estimator and does not inherit the same range bound.

# Counterexamples to Broader Claims

Normalization alone is insufficient. Take $(y_1,y_2)=(0,1)$ and
$(w_1,w_2)=(-1,2)$. The weights sum to one, but the aggregate is 2,
outside the input interval $[0,1]$. Negative weights invalidate the order
argument in the proof. A manuscript cannot omit nonnegativity while retaining
the proposition unchanged.

Nor does the range bound imply accuracy. Suppose two predictors both output
100 when the true value is 0. Every convex combination of those outputs
remains 100. The proposition holds exactly, yet the squared error is 10000.
There is no contradiction: containment and accuracy are different properties.

The example also gives no guarantee of unbiasedness. Bias requires a target
and an expectation under a specified distribution, neither of which appears
in the proposition. A paper claiming such a guarantee would need additional
assumptions and a separate argument.

# Verification and Limits

The repository tests finite rational examples using exact arithmetic and
checks the counterexamples numerically. Those tests are useful for catching
transcription mistakes; they do not prove the proposition for all real inputs.
The proof above supplies that argument. This distinction is the theoretical
analogue of separating a measured result from a universal empirical claim.

This note contains no new aggregation method, empirical benchmark, formal
proof-assistant verification, or peer-review outcome. It was authored with AI
assistance as an open writing example. Its scientific scope is the stated
elementary inequality and the demonstrated limits of its interpretation.

# Conclusion

The defensible headline is that nonnegative normalized aggregation preserves
the input range. Reliability, accuracy, and generalization are not consequences
of that statement alone. A theoretical manuscript should keep the assumptions
that make its claim true visible in the abstract, proposition, and interpretation.
