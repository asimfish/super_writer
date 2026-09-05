# 使用方式 / Usage

## 已有初稿 / Rewrite

```text
使用 $super-writer 处理 draft.tex。目标会议及其格式要求在 venue.md，
参考文献在 references/，实验结果在 results/。先检查已有输出，梳理论文贡献、
证据和限制，向我呈现动机方案；确认后再写逐段计划并改写。
```

```text
Use $super-writer to revise draft.tex using venue.md, references/, and results/.
Inspect existing outputs, establish the contribution and evidence boundary,
and present motivation options before planning and rewriting the manuscript.
```

## 从材料写作 / Build

```text
使用 $super-writer 从 materials/ 的方法笔记、CSV 和图表构建英文期刊论文。
缺少的实验要标出，不要补造数值。先产出素材清单、贡献边界和动机方案。
```

Start with `workflow=build_from_materials`. Inventory contents before interpreting
results. Distinguish author's experimental evidence from literature examples.

## 中断后继续 / Resume

```text
使用 $super-writer 继续当前项目。读取 paper_rewriting_output/，
从第一个未完成且前置条件有效的阶段继续，保留已经确认的动机和特殊要求。
```

The config and outputs are the checkpoint. A file's existence is not a current
audit result; rerun the relevant guards when their input has changed.

## 单独审计 / Audit Only

```text
使用 $super-writer，只检查 manuscript.tex 和 references.bib 的引用、标签和占位符，
输出问题位置与建议，不修改论文，也不启动完整写作流程。
```

From the repository root, a direct read-only command is:

```bash
python3 scripts/latex_guard.py /path/to/manuscript.tex --bib /path/to/references.bib --markdown
```

Commands in this document use repository-relative script paths. When installed,
resolve the script under the installed skill and keep the user's project as cwd.

## 翻译、投稿与回复 / Requested Extensions

```text
使用 $super-writer 为已有英文稿生成完整中文翻译和 paper.zh.docx。
保留表格、图注、引用、公式和数值，给出翻译覆盖检查。
```

```text
Use $super-writer to prepare a cover letter and highlights using the journal's
supplied requirements. Preserve the manuscript's actual contribution and claims.
Prepare files for my review; do not submit them.
```

```text
使用 $super-writer 将 review_comments.md 映射到论文修改与逐条回复。
每项标明已改内容、证据和稿件位置；无法支持的意见说明原因。
```

## 可重复的配置 / Explicit Configuration

Run this from the paper project, replacing the skill path:

```bash
python3 /path/to/super-writer/scripts/intake_wizard.py --no-interactive \
  --workflow rewrite_existing --scene conference --tier flash \
  --output-language en --ui-language zh --draft-path draft.tex \
  --target-name "My target conference" --reference-path references \
  --humanize-tier none --word-output docx --output-dir paper_rewriting_output
```

This creates configuration only, not a manuscript or an approved motivation.
Keep existing configs when resuming. Use `--classic-input` in a real terminal for
the interactive version. Use `--word-output none` only when Word is not wanted.

## ZIP 使用 / ZIP Use

Download the release ZIP and matching `.sha256` file from the same release.
On Linux use `sha256sum -c FILE.sha256`; on macOS use
`shasum -a 256 -c FILE.sha256`. On Windows use `Get-FileHash FILE.zip -Algorithm SHA256`
and compare its hash with the checksum file. Extract to a fresh directory.
The `super-writer/` root contains `SKILL.md` and the required resources.

Text-only hosts cannot run Python, compile TeX, or produce a verified Word file.
In those environments, use the instructions as a guide and identify unexecuted
checks rather than calling the workflow complete.
