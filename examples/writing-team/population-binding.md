# A Clear Explanation Can Still Misbind a Number

Post-pilot teaching note, not a new blind output or a repaired experiment.
The V-HOP `relaxed` and `meaning` revisions both say:

> Training uses only synthetic data spanning eight grippers and thirteen objects.

The supplied evidence assigns those counts to the **whole dataset**, and separately
excludes D'Claw and pudding_box from training. The coordinator's post-audit visual
check of [PDF page 6, Table II](https://www.roboticsproceedings.org/rss21/p037.pdf)
confirms eight dataset grippers versus seven training grippers. The generated
sentence moves a dataset count onto a training population, undermining the
meaning of unseen-embodiment evaluation. Clear mechanism prose does not excuse it.

A bounded correction, authored after the test:

> Training uses synthetic multi-gripper data, with one gripper and one object
> withheld for generalization evaluation.

This deliberately omits the total count instead of guessing a training count.
If total dataset size is contribution-relevant, state it as dataset coverage in
a separate clause and preserve the split. Do not require both counts in every
abstract. Evidence selection should earn its space.

For each new numerical claim, check quantity, entity, population/split and scope
against its source. Combining two true facts can change what a number modifies.
The existing fidelity channel must fail such a candidate even when all selected
meaning relations and priority criteria pass. The local checker cannot infer
this error from IDs or matching spans; its role is to enforce a supplied failure
judgment, not perform automated scientific entailment.
