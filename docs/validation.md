# Validation Scope

The standalone release retains the PaperSpine V4 guard foundation with targeted
privacy and data-preservation fixes, plus portable distribution, onboarding, and
installation. The repository does not
claim measured acceptance-rate gains, detector bypass, or autonomous scientific
verification.

## Reproducible Checks

| Command | Evidence |
|---|---|
| `python3 -m compileall -q scripts tools tests` | Python syntax/import compilation |
| `python3 scripts/smoke_test.py` | 11 inherited synthetic CLI cases across inventories, artifact/citation/integrity guards, LaTeX, style, revision, and review dispatch/independence |
| `python3 -m unittest discover -s tests -v` | Distribution/install behavior, package integrity, portability, citation privacy, preference isolation, and document-preservation regressions |
| `python3 scripts/latex_guard.py examples/synthetic-study/manuscript.tex --markdown` | The public standalone TeX example passes structural guard checks |
| `python3 tools/build_release.py` | Versioned ZIP and checksum built from intended source files |

CI in `.github/workflows/ci.yml` runs the declared checks on its platform matrix.
Results are bound to each CI commit; a CI badge is not evidence that an arbitrary
manuscript was reviewed. Optional Pandoc/TeX tools are not needed for the portable
guard tests.

The release-safety regressions use intercepted network calls and temporary
project/document fixtures. They check that citation queries cannot fall back to
manuscript-support fields, global preference setup cannot rewrite project config,
and `--fix-fonts` preserves `word/document.xml` exactly. These are bounded regression
checks, not a claim that arbitrary files or future changes are secure.

## Known Limits in the Inherited Engine

- `progress_check.py` primarily inventories stage artifacts. Contribution,
  results-validation, and reviewer-audit guards also run in the final gate, but
  are not independent progress stages. The entrypoint requires checking
  contribution before planning and results mapping before assembly.
- Old PASS reports are not content-addressed audit receipts. Rerun checks after
  modifying a manuscript, config, evidence bank, or other checked input.
- The synthetic smoke suite does not exercise every final-audit path, Word/PDF
  rendering, live citation API, or actual agent writing decision. Its fixture
  is not a complete publishable paper.
- `latex_guard.py` recognizes labels from included TeX files but does not expand
  all commands or fully audit every included file's prose/citations. Compilation
  and a document-level review remain necessary.
- Numeric-citation and section-economy checks encode inherited conventions.
  Author-year venues and complex templates may require a scoped guard adaptation.
  Preserve official venue requirements and record unresolved compatibility.
- DOI and bibliography matching establish metadata plausibility, not whether
  the cited paper entails a manuscript sentence.
- Word checks inspect document structure, text, and fonts. They do not replace
  opening the rendered document to inspect equations, figures, pagination, and
  layout. PDF generation is conditional on a TeX environment.
- Style metrics and independent-review text checks are heuristic. They do not
  establish human authorship, research novelty, or reviewer agreement.

## Evaluation Integrity

`evals/activation.json` records routing expectations, including explicit use and
explicit exclusion. Schema checks only validate that fixture; agent-level routing
requires a behavioral evaluation. Independent exercises should receive raw
materials and a realistic request, without the expected answer or prior diagnosis.

The example study is hand-authored synthetic data with documented arithmetic.
It supports a bounded demonstration of evidence-to-claim mapping. No SafeLab or
SafeTransport manuscript, private result, or other real project data is distributed.
