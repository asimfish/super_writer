# Compression-first revision pilot

Frozen before revision generation on 2026-10-18. This is a local pilot, with
six RSS 2025 papers and two units per paper: Abstract and Results. Papers were
absent from the repository's earlier evaluation materials at selection time.
This does not exclude model pretraining exposure.

All writers receive the same body-grounded editorial facts, an initial readable
draft, two reader questions and a 160-word ceiling for Abstract or 130 for Results.
Author abstracts and first PDF pages are withheld from writer inputs. Source
preparers inspect pages 2-10, subject to the actual paper length. Their original
paraphrases are published; full source PDFs and OCR extractions stay outside Git.
Numbers and uncertain OCR are checked against rendered source pages as needed.

Three conditions each revise every unit once in fresh inherited-model contexts:

- prior: selected relevant guidance and role cards from commit 3f9d99c;
- compression: the same guidance plus the compression-first changes at 870a205,
  including no increase over the initial draft's word count;
- editorial: ordinary academic revision with an explicit clarity and concision
  request, the same facts and absolute ceiling, without the system's role cards.

Both system conditions also receive the same complete selected Abstract and
Results protocols, operation/quantity AI-spec records, and existing ResNet and
Many Faces abstract-only editorial notes. These are bundled local observations;
no new reading of those exemplar papers or Results-style transfer is claimed.

Two writer blocks contain three disjoint papers each, making six writer contexts.
Each returns one actual revision per unit and brief private edit notes. No retry
is allowed for prose quality or budget violations. Malformed transport/JSON may
be repaired without changing prose, with the repair retained in the execution log.
This tests the revision guidance bundle, not independent execution of the full
four-role handoff loop. The relative length constraint is part of the treatment;
the three conditions do not have identical effective word budgets.

Two new reviewers receive anonymized four-way passages and common evidence;
the fourth version is the shared initial draft. This directly tests whether a
rewrite improves on the already-readable original.
The second receives reversed unit order and a different label permutation.
Each compares all six pairs on overall writing, clarity and economy, with an
exact witness and reason. Shorter text is not automatically preferred. Reviewers
also answer the two reader questions using prose witnesses, and audit factual
claims separately against the common evidence. Reviews must flag unsupported
causality, altered measurement objects, numerical errors, lost essential
qualifications and loss of an author's central contribution.

The primary comparison is compression versus prior on Abstract. Secondary
comparisons cover Results and compression versus ordinary editorial revision.
Report all votes, ties, reviewer disagreement, lengths, missing outputs, budget
violations and source-fidelity concerns. Count papers and passages separately;
correlated votes are not independent samples. No quality score is formed by
adding rubric scores or word savings.

The candidate passes this pilot only if it has positive net preference against
both controls overall and on Abstract, no consequential candidate factual
failure, no reduction in fully recovered reader answers, and no candidate word
budget violation. It must also have no negative net preference versus the shared
initial draft overall or on Abstract. A failed component fails the gate. Passing is evidence for
this small pilot, not a general promotion or proof of excellent-paper imitation.
All inputs and guidance are checksummed before generation; all initial outputs,
review outputs and mappings are retained unchanged. No tuning or runtime-guide
editing occurs after generation starts.

Question recovery is assessed by the two evidence-aware reviewers using exact
prose witnesses. It is not a separate prose-only reader experiment. A recovery
judgment can still be influenced by source knowledge. The reviewers receive no
condition identities, revision prompts, word counts, edit notes or expected gate.
