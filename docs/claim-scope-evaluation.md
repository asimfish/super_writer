# Claim-Scope Evaluation

Date: 2026-09-14. Synthetic forward test of genre and evidence scope, not a real-paper holdout.

The skill now distinguishes completed-results abstracts from proposals: unsupported future work belongs in notes for the former, but may be a clearly labeled objective in the latter. Encoding reuse and downstream policy success are separate claims requiring separate evidence.

Three synthetic cases produced six fresh-context abstracts (120-160 words) with two reversed-order judges. The completed case was tied by both judges. The proposal case and updated encoding case were each tied by one judge; the other preferred the new wording for tighter scope in the proposal and the old wording for a narrower reuse claim. All responses parsed and met budget. This is useful directional evidence, not a general quality improvement claim.

One remaining issue is explicit: both evidence-only versions mention the future objective while labeling it unestablished. Whether that objective belongs in a completed-results abstract remains unresolved. The disagreement and raw prompts/responses are retained locally in [the evaluation directory](/Users/liyufeng/Desktop/research/super_writer_claim_scope_eval_20260914).

Repository verification: 164 unittest cases, 163 passed and one PowerShell-unavailable skip; 11 smoke cases; compilation, frontmatter validation and whitespace checks passed. No installation, commit, push or remote CI run occurred. Release assessment: CONDITIONAL pending real-paper and human evaluation.
