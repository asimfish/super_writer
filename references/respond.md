# Review Response Workflow

Use this stage when the user has reviewer comments and needs a revision
response package.  Do **not** create a separate skill — this is routed from
the main `paper-spine` orchestrator.

## Output Directory

```
paper_rewriting_output/review_response/
```

## Inputs

- Reviewer comments file or user-pasted text
- Original manuscript: `final_paper/main.tex`
- Supporting artifacts: `writing_rationale_matrix.md`, `evidence_bank.md`,
  `claim_register.md` (read when available)

## Comment Extraction

If reviewer comments are not already numbered, extract and assign IDs:

- `R1.C1`, `R1.C2`, `R2.C1`, etc.  (`R` = Reviewer, `C` = Comment)
- Present the extracted list to the user for confirmation before proceeding.

## Required Outputs

### 1. `reviewer_comments_extracted.md`

Numbered list of every reviewer comment with stable Comment IDs.

### 2. `response_matrix.md`

| Comment ID | Reviewer | Original Comment | Issue Type | Required Action | Manuscript Change | Evidence / Source | Response Draft | Status |
|---|---|---|---|---|---|---|---|---|

- **Comment ID**: `R1.C1`, etc.
- **Issue Type**: `major` / `minor` / `clarification` / `format`
- **Status**: `draft` / `final` / `needs-author`

### 3. `response_letter.md`

Point-by-point response letter addressed to the editor/reviewers.  Each
comment ID must appear.  Polite, specific, and locatable in the manuscript.

### 4. `revision_change_log.md`

Summary of every revision made, with manuscript line/section references.

### 5. Revised manuscript

Either `revised_manuscript.md` or a note that changes have been applied to
`final_paper/main.tex`.

## Rules

- Every reviewer comment must receive an individual response.  No omissions.
- Responses must be polite, specific, and traceable to a manuscript change.
- Do **not** fabricate new experiments, data, statistics, author info, or
  reviewer comments.
- When user data is needed, use explicit placeholders:
  `[NEEDS USER DATA: <description>]`
  `[AUTHOR CONFIRMATION REQUIRED: <description>]`
- If a comment cannot be adopted, explain why and offer an alternative.
- All changes must be traceable to the original manuscript, `evidence_bank`,
  `claim_register`, or explicit user supplements.
- Do **not** silently pass unresolved comments to appear complete.

## Rebuttal Escalation (Optional)

This stage produces a journal-style revision response (response letter +
revised manuscript). For conference rebuttals — strict character limits,
text-only replies, multiple reviewers with scores, follow-up rounds — escalate
to the companion `rebuttal` skill instead of stretching this playbook:

- Route there when the user mentions OpenReview/CMT/HotCRP, a character/word
  cap, reviewer scores to move, or a second rebuttal round.
- Reuse this stage's artifacts as its inputs: `reviewer_comments_extracted.md`
  seeds its comment parsing, and `response_matrix.md` rows map to its coverage
  ledger; `evidence_bank.md` / `claim_register.md` remain the only permitted
  evidence sources.
- Its outputs live beside this stage's, under
  `paper_rewriting_output/review_response/rebuttal/`.

The no-fabrication rule carries over unchanged: no invented experiments, no
promised results that cannot be delivered. If the `rebuttal` skill is not
installed, stay in this playbook and note the venue's limits manually.

## Verification

```bash
python scripts/respond_check.py paper_rewriting_output/review_response --markdown --write
```

Produces `review_response/respond_check.md`.  Fix all FAIL findings before
delivery.
