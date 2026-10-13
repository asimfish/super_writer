# Real Embodied Abstract Evaluation

Date: 2026-09-14. Three real RSS papers were used as source baselines:
[Diffusion Policy](https://roboticsproceedings.org/rss19/p026.html),
[OpenVLA-OFT](https://www.roboticsproceedings.org/rss21/p017.html), and
[pi0](https://www.roboticsproceedings.org/rss21/p010.html). Original abstracts
were read from official proceedings pages and are not copied into the repository.

Writers received fact summaries, not original wording. Six fresh-context writers
produced one 150-190 word abstract per condition; two fresh-context judges
compared old/new against the source baseline with reversed display order.

| Paper | Judge 1 | Judge 2 |
|---|---|---|
| Diffusion Policy | Old | New |
| OpenVLA-OFT | New | New |
| pi0 | New | Old |

OpenVLA-OFT is the strongest positive signal: both judges found the new version
preserved the recipe, exact LIBERO improvement, throughput distinction, real-robot
scope and baseline conditions more clearly. This records their preference, not
a clean factual verdict; see the source-audit correction below.
Diffusion Policy and pi0 expose the
remaining risk: new can omit a source-supported dissemination detail or add
labels such as reliable or unified that exceed the supplied evidence. One new
Diffusion Policy abstract also failed the mechanical length requirement at 126
words. The raw response is retained and was not repaired.

All six responses parsed as JSON; five met the word budget. Source abstracts have
unequal length and are editorial comparators, not causal controls. Three papers
and one sample per condition cannot establish a stable win rate. Model judging is
not human validation. The new evidential-verb rule was added after this generation
and was not applied retroactively.

Repository checks: diff whitespace and skill validation passed; the preceding
full suite passed with 164 tests, 163 passing and one PowerShell-unavailable skip,
plus 11 smoke tests. Release assessment: CONDITIONAL. No commit, push,
installation or version bump was performed.

## Source-Audit Correction (2026-09-18)

Rechecking the linked official OFT abstract identifies a missed factual boundary:
pi0 and RDT-1B are fine-tuned with their default recipes, while Diffusion Policy
and ACT are trained from scratch. Both generated versions group these baselines
under their stated fine-tuning setups. Neither version preserves the distinction
adequately. The two judge preferences above remain the historical observations,
but cannot establish faithful baseline-condition reporting or overall superiority.
The raw generations are not rewritten to remove this failure. The point at which
the distinction was lost (fact summarization or generation) has not been isolated.

The follow-up guide now preserves heterogeneous training regimes and design
rationales without upgrading intended benefits into measured causes. Three new
synthetic calibration pairs cover this attribution error, rationale loss, and a
valid opening-order tie. These are development fixtures, not a new held-out
generation experiment. Writing-quality improvement remains unestablished.
