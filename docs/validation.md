# Validation Scope

Super Writer combines an inherited PaperSpine V4 workflow with bounded guards,
portable distribution and public writing examples. Tests establish the specific
behavior below, not research novelty, factual entailment or acceptance gains.

## Reproducible Checks

Run from the source checkout with Python 3.10+. The portable suite uses the
standard library and temporary fixtures; it needs no model or paid API.

| Command | Evidence | Not established |
|---|---|---|
| `python3 -m compileall -q scripts tools tests` | Python syntax compilation | Runtime correctness |
| `python3 scripts/smoke_test.py` | 11 inherited synthetic CLI cases | Every workflow path or writing decision |
| `python3 -m unittest discover -s tests -v` | Distribution, installation, portability, privacy, document preservation, policy wiring and example regressions | Agent-level writing quality |
| `python3 examples/knn-regression/experiment.py` | Recomputed deterministic experimental summary | Real-world generalization or significance |
| `python3 tools/render_examples.py --output-dir build/rendered-examples` | PDF/Word export; text, reference, font and overfull-box checks | Every document client's rendering |
| `python3 tools/check_template_compatibility.py --output-dir build/template-check` | Eight pinned official-template fixtures, including two citation modes and a distinct rebuttal | Complete submission compliance |
| `python3 tools/import_writing_library.py --check` | Reproduce 127 selected cards and data-license bytes from pinned public inputs | Citation entailment or completeness of terminology |
| `python3 scripts/pdf_layout_check.py paper.pdf --log main.log` | Snapshot hash, physical-page bounds, font embedding and optional log check | Visual quality, anonymity or source-to-PDF build provenance |
| `python3 tools/build_release.py` | Allowlisted ZIP, manifest and archive checksum | That an arbitrary download matches without checking its hash |

The document commands require Pandoc, pdfLaTeX, BibTeX and Poppler. The explicit
template command downloads style archives; the separate importer downloads
pinned public corpus inputs. Template SHA-256 pins, official
links and allowlists are in
[`sources.json`](../tests/fixtures/templates/sources.json). CI runs four portable
platform/Python combinations and a separate Linux document job. Inspect the run
for the commit in question; a badge is not a manuscript audit receipt.

For the Ubuntu document environment, install the explicit dependencies below
after updating the package index. The separate `lmodern` package supplies the
LaTeX font support required by Pandoc; OpenType fonts alone are insufficient.
`texlive-science` supplies the `algorithm` and `algorithmic` packages required
by the unchanged ICML style.
`cm-super` supplies Type 1 fonts for the unchanged ECCV style's T1 encoding.
Its metrics match the original Computer Modern family; see the
[font package description](https://ctan.org/pkg/cm-super).

```bash
sudo apt-get install -y --no-install-recommends pandoc texlive-latex-extra texlive-fonts-recommended texlive-science lmodern cm-super poppler-utils
```

## What the New Examples Test

- **Empirical study:** recompute all 20 measurements, independently aggregate
  means and sample standard deviations, and compare every rounded table result
  with the Markdown, PDF text and Word XML. Direct kNN oracles cover ties,
  extreme neighbor counts and extrapolation behavior.
- **Theory note:** exact-rational finite cases check the stated range bound;
  signed-weight and inaccurate-average counterexamples check its limits. These
  cases do not prove a theorem; the accompanying elementary proof is separate.
- **Reviewer response:** the response explicitly distinguishes completed
  wording changes from an unrun baseline. Export and structural guards run on
  it. There is no automated test proving that arbitrary reviewer responses are
  persuasive or scientifically sufficient.

The three new PDFs have 3, 2 and 1 pages respectively in the published build.
Sources and seeds are public. Data are synthetic; table values are actually
computed, not hand-invented. The earlier `synthetic-study` example remains a
separately labeled, hand-authored arithmetic fixture.

These are AI-assisted worked demonstrations checked against their inputs, not
independent blind evaluations. No private manuscript or third-party full paper
is distributed. PDF previews are generated from the actual documents.

## Official Template Boundary

| Pinned template | Citation mode | Fixture checks |
|---|---|---|
| ICML 2026 | Author-date | Compilation, citations, table/equation references, hidden identity sentinels |
| ICLR 2026 | Author-date | Same bounded checks |
| CVPR 2026 | Numeric | Same bounded checks |
| NeurIPS 2026 main review | Author-date and numeric, separately compiled | Same checks; explicit natbib mode retained |
| ACL style, used by ACL/EMNLP 2026 | Author-date | Package-selected bibliography; separate long/short profiles |
| ECCV 2026 main review | Numeric, LNCS | Unchanged class/style; no CVPR font substitution |
| ECCV 2026 rebuttal | Numeric, two-column | Distinct template; one total page and no external URL in fixture text |
| AAAI 2026 | Not locally verified | Guide-only profile; official kit returned HTTP 403 |

The source tool verifies archive hashes, reads only named style files in a
temporary directory, disables shell escape, and verifies that style bytes remain
unchanged. Regression fixtures reject changed hashes, duplicate/missing members,
symlinks, oversized members and non-flat output filenames. This is not an OS
sandbox; TeX and its packages remain executable dependencies.
MiKTeX builds explicitly disable automatic package installation. Template tests
also invoke the PDF receipt tool; no word bounding box may escape the physical
page and fonts must be embedded. These are not content-margin or readability
proofs. Type 3 and image-only pages require inspection rather than a universal
policy verdict. The file-hash receipt identifies inspected bytes; it does not
retroactively certify other versions.

The Word companions test numeric/author-date recognition and content/font guards.
They are **not official Word submission templates**. Fixtures do not test every
page-limit rule, supplemental/appendix convention, track, camera-ready mode or
disclosure policy. Supply current official requirements for the actual target.
No endorsement by these conferences is implied.

## Policy and Safety Regressions

Section count defaults to an advisory; an explicit positive `max_sections`
enforces a project budget. TeX comments, appendices and bibliography material are
excluded from that count. Citation collection size and recency are suggestions
unless `citation_enforce_heuristics=true`; empty banks and malformed rows still
fail, including records beyond the suggested collection target. This changes
heuristic severity, not evidence requirements.

Natural-expression heuristics are likewise advisory unless
`humanize_enforce_heuristics` is exactly JSON `true`. Matrix structure and required
dimension coverage remain checked. A truthful audit need not invent a
high-severity defect. Ten authored expression cases check declared protected
spans; no automated test here proves arbitrary semantic preservation.

Citation privacy tests intercept network calls: manuscript-support fields cannot
become fallback search queries. Global preference setup cannot rewrite project
config, and Word `--fix-fonts` preserves `word/document.xml` exactly. These are
bounded regressions, not a universal security claim. See [SECURITY.md](../SECURITY.md).

English and Chinese citation verification inspect the first Markdown table in a
support bank. Keep citation records in that table; later tables are not silently
interpreted under its column labels.

## Remaining Limits

- `progress_check.py` primarily inventories stage artifacts. Contribution,
  results-validation and reviewer-audit guards run in the final gate but are not
  independent progress stages. Old PASS files are not content-addressed receipts;
  rerun guards after changes to any checked input.
- LaTeX guards recognize some included labels but do not expand every macro or
  audit all prose in every included file. Compile and inspect the whole document.
- Known bibliography styles are recognized, not every future year or custom
  template. Resolve unknown styles without overriding official requirements.
- DOI/metadata matches do not prove that a source supports a sentence. Citation
  entailment, experimental fairness and numerical interpretation need review.
- Word checks inspect structure, text and fonts. Open the document in the target
  client to review equations, figures, pagination and layout.
- Style and reviewer-independence text heuristics do not establish human
  authorship, detector outcomes, novelty or reviewer agreement.
- `evals/activation.json` defines routing cases; schema validation alone does not
  execute them against an agent. A writing-quality benchmark needs held-out raw
  inputs, blinded scoring, negative cases and reported failures.

The 11 profiles cover eight named venues at specific 2026 stages. Additional
years, camera-ready stages, verified AAAI compilation and independent writing
evaluations remain future work. A test suite does not complete those tasks.

## Local 1.2.0 Release Check

Recorded on 2026-09-06. The previous release record below is historical.

| Check | Observed result |
|---|---|
| Full suite, Python 3.10.19 and 3.14.3 on macOS | 144 cases per interpreter: 143 passed, 1 skipped because PowerShell was unavailable |
| Inherited CLI smoke | 11 passed |
| New resources | Exact venue selection, no year fallback, bounded offline lookup, Chinese aliases, whole-card JSON budgets, provenance and license preservation |
| Corpus regeneration | 127 cards and 37 discovery-source records reproduce exactly from pinned inputs |
| Official templates | Eight cases compile, PDF citation modes and document guards pass, official styles unchanged; all nine rendered pages visually inspected |
| Existing worked examples | Three PDFs and Word companions rebuilt successfully; sources remain unchanged |
| Metadata | Skill validator, CFF 1.2.0 schema/version and YAML checks pass; 161 relative file/image links checked |
| Distribution | Real runtime and installed offline lookup/profile commands tested from paths containing spaces; missing corpus licenses block packaging |

The 48 added tests include negative cases for malformed PDF-tool output,
out-of-page text, citation-mode drift, changed download bytes, unreviewed corpus
records, missing notices and inappropriate heuristic blocking. Counts include
some methods with multiple subcases; they are not 144 writing-quality trials.
The old/new heuristic comparison reproduced a real v1.1.0 false rejection.
The Linux template job also exposed a citation-oracle false rejection when
TeX split `background` across lines as `back-` / `ground`. Its captured text is
a regression case; only line-break hyphenation is normalized, and wrong citation
modes still fail. This does not modify the official ACL style or the rendered PDF.
The Linux ECCV build then exposed missing Type 1 font dependencies: extracted
`fi`/`ffi` ligatures became XML-invalid `U+001C`/`U+001E` characters. A disposable
Debian 12 font probe reproduced this with Type 3 output; installing only
`cm-super` and rebuilding the same source produced Type 1 fonts with Unicode
maps and valid bounding-box XML. CI now installs that dependency explicitly.
The strict XML parser, original fixture prose and official styles remain unchanged.

No new model-based blind writing evaluation or Word-client visual certification
was performed. AAAI remains guide-only. Source-only document commands explicitly
disable MiKTeX auto-installation; see the release notes for the early discovery.

## Local 1.1.0 Release Check

Recorded on 2026-09-05 for the release candidate; remote CI is separate evidence
and must match the published commit.

| Check | Observed result |
|---|---|
| Full suite, Python 3.10.19 and 3.14.3, macOS 26.2 | 96 cases on each interpreter: 95 passed, 1 skipped because PowerShell was unavailable |
| Inherited CLI smoke | 11 passed; also repeated from an isolated installed payload |
| Three worked examples | PDF/Word guards pass; all six PDF pages visually inspected |
| Three pinned template fixtures | Compile and guards pass; all three rendered pages inspected; official styles unchanged |
| Metadata and public docs | CFF 1.2.0 schema valid, skill metadata valid, YAML parses, 104 relative file/image links checked |
| Distribution | Archive checksum and per-file manifest verified; installed files match the ZIP in a temporary path containing spaces |

The document environment used Pandoc 3.9.0.1, MiKTeX-pdfTeX 4.10 / BibTeX 4.1
(MiKTeX 22.1), and Poppler 26.03.0. PDF inspection caught an unwanted response
section number and an ICML fixture's visible `AUTHORERR` notice; both were fixed.
A new negative regression rejects that notice even if TeX exits successfully.
This illustrates why compilation alone is not a visual review.

No Word-client visual inspection or new blinded writing-quality evaluation was
performed for this release. Those limits remain explicit rather than being
counted as successful tests.
