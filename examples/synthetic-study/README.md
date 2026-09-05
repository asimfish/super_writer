# Synthetic Study / 合成示例

All counts in `materials/results.csv` were invented for this tutorial. They are
not observations from a real experiment. The task is to compare writing claims
against explicit evidence, not to establish a research finding.

| File | Role |
|---|---|
| `materials/method.md` | Synthetic protocol and known limitations |
| `materials/results.csv` | Fixed counts for reproducible arithmetic |
| `draft.md` | An intentionally over-strong sentence to revise |
| `evidence-to-claim.md` | A worked mapping with allowed and unsupported statements |
| `manuscript.tex` | A bounded result excerpt in a standalone LaTeX document |
| `manuscript.pdf` | Compiled one-page example with resolved table reference |
| `manuscript.docx` | Pandoc conversion checked by the Word guard |
| `preview.png` | First-page preview rendered from the PDF |

Try a bounded exercise:

```text
使用 $super-writer，根据 examples/synthetic-study/materials/ 的合成数据，
审计 draft.md 的声明并改写这一段。不要运行完整写作流程；不要检索文献或补充实验。
标明哪些结论受支持，哪些不能写，并保留“合成教学数据”的说明。
```

For an independent exercise, give the agent only the task, `draft.md`, and
`materials/`; do not provide the worked answer. For a full-writing trial, use real
author-approved materials and reference sources instead of treating this small
example as a completed pipeline.

Check the public TeX without external dependencies:

```bash
python3 scripts/latex_guard.py examples/synthetic-study/manuscript.tex --markdown
```

Optional compilation from this example directory: `pdflatex -no-shell-escape
-interaction=nonstopmode -halt-on-error manuscript.tex`.
