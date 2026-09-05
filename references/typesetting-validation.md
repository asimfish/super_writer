# Typesetting and Controlled Revision

## Before Assembly

Select an exact profile with `scripts/venue_profile.py --id ...`. The catalog
records 2026 snapshots, not future rules. Unknown years, stages or tracks require
official-source research; do not silently fall back to the nearest template.
AAAI is currently guide-only because its official kit download was blocked.

Keep original official `.sty`, `.bst` and `.cls` files unchanged. Use the
venue's actual title, anonymity and citation mechanisms. A generic article or
ReportLab approximation is a draft format, never an official template.
Word is an editable companion by default, not a certified submission format;
ICML and NeurIPS require their LaTeX workflow. Do not transfer the companion's
Times font repair to an ECCV LNCS PDF.

Probe tools with `command -v pdflatex bibtex kpsewhich pandoc pdftotext pdffonts`.
Use `kpsewhich package.sty` for packages named by the chosen template. Report
missing dependencies and proposed installation; do not install global packages
or remove required typography to get a successful build. Do not inspect agent
caches, chat logs or API-key stores to fill manuscript gaps.

## Compile and Inspect

Compile the trusted project in its designated output directory, disable shell
escape, and rerun the required bibliography/reference passes. TeX and PDF tools
are executable parsers: disabling shell escape is not an OS sandbox for
untrusted sources. Do not compile retrieved arbitrary TeX without inspection.

```bash
python scripts/pdf_layout_check.py final_paper/main.pdf --log final_paper/main.log
```

The JSON receipt checks physical-page text bounds, font embedding and explicit
log errors, and hashes the bytes inspected. Image-only pages and Type 3 fonts
are inspection warnings, not blanket rejection rules. `--max-pages` means
**total PDF pages**; use it for ECCV's one-page rebuttal, not for an eight-page
body plus unlimited references. A caller-supplied log hash does not prove the
log produced the PDF. The controlled template test does establish its build
sequence, but still does not certify arbitrary papers.

Visually inspect every page at readable scale. Check title and author mode,
column flow, equation overflow, caption placement, labels, table legibility,
figure resolution, font consistency and stranded floats. Inspect charts against
their data. A first-page preview does not establish whole-document quality.
Verify anonymity in metadata, raster figures, acknowledgments and links, not
only visible author text. Preserve attribution required by licenses; resolve
anonymity conflicts instead of silently deleting legal notices.

## Layout Changes Must Preserve Content

Prefer float placement, line breaks and concise equivalent prose over font or
margin changes. Use the template's table/figure conventions; do not impose a
universal aspect-ratio rule or require every visual to be a raster image.
Never delete a limitation, failed baseline or citation to improve a layout score.

For each substantive revision, keep a task-scoped snapshot and record:

| Candidate | Input hash / scope | Intended improvement | Evidence-preservation result | Build / visual result | Decision |
|---|---|---|---|---|---|
| revision ID | Current source version, changed units | Concrete defect | Claim, number-entity, condition, citation checks | Current reports, affected pages | Keep or reject with reason |

Accept only changes that preserve the evidence contract and improve an observed
defect. A simulated review score cannot override an integrity failure. Stop when
the defect is resolved, after at most three scoped rounds, or when further
changes require missing evidence or author decisions. Restore only this task's
candidate snapshot, never use a destructive repository reset.

Rerun relevant guards after changes, inspect affected pages and update the
`main.pdf` / `paper.pdf` alias. Old receipts are evidence of old files, not new
ones. Report mechanical checks, visual inspection and scientific review as
separate outcomes.
