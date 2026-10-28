"""Render the existing five-paper Chinese comparison as standalone offline HTML."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def render(data: dict) -> str:
    escape = html.escape
    links, sections = [], []
    for index, paper in enumerate(data["papers"], 1):
        ident = escape(paper["id"], quote=True)
        name = escape(paper["short_title"])
        links.append(f'<a href="#{ident}"><span>{index:02}</span> {name}</a>')
        columns = []
        for label, words, prose, kind in (
            ("作者摘要 · 中文概述", paper["author_word_count"], paper["author_summary_zh"], "author"),
            ("Super Writer · 中文译稿", paper["ours_word_count"], paper["ours_zh"], "writer"),
        ):
            columns.append(
                f'<article class="version {kind}" aria-label="{name} {label}">'
                f'<div class="version-heading"><h3>{label}</h3>'
                f'<span class="word-count">英文 {words} 词</span></div>'
                f'<p class="abstract">{escape(prose)}</p></article>'
            )
        observations = "".join(
            f'<div><dt>{label}</dt><dd>{escape(paper["comparison"][key])}</dd></div>'
            for key, label in (("retained", "保留内容"), ("improved", "解释变化"),
                               ("omitted_or_risk", "遗漏与风险"))
        )
        sections.append(
            f'<section class="paper" id="{ident}" aria-labelledby="title-{ident}">'
            f'<header class="paper-heading"><div class="paper-title">'
            f'<span class="paper-number">{index:02}</span><h2 id="title-{ident}">{name}</h2>'
            f'</div><a class="source" href="{escape(paper["source_url"], quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">论文原文 ↗</a></header>'
            f'<p class="full-title" lang="en">{escape(paper["title"])}</p>'
            f'<p class="venue">{escape(paper["venue"])}</p>'
            f'<div class="comparison">{"".join(columns)}</div>'
            f'<details><summary>差异与取舍</summary><dl>{observations}</dl></details>'
            '</section>'
        )
    return """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>五篇论文摘要 · 中文对照 | Super Writer</title>
<style>
:root { color-scheme: light; --ink: #25272b; --muted: #62666d; --line: #dfe2e5;
  --author: #25686b; --writer: #8f4658; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 90px; }
body { margin: 0; background: #fff; color: var(--ink); letter-spacing: 0;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; }
a { color: #205d68; text-underline-offset: 4px; }
a:focus-visible, summary:focus-visible { outline: 2px solid #236b9a; outline-offset: 5px; }
.page-heading, main, .footer-inner, .nav-inner { max-width: 1460px; margin: 0 auto; }
.page-heading { padding: 32px 36px 25px; }
.eyebrow { font-size: 12px; color: var(--muted); margin: 0 0 9px; }
h1 { font-size: 27px; line-height: 1.4; font-weight: 650; margin: 0 0 12px; }
.context { color: #51575d; font-size: 14px; line-height: 1.85; margin: 0; max-width: 1040px; }
.context + .context { margin-top: 4px; }
nav { position: sticky; top: 0; z-index: 2; border-block: 1px solid var(--line); background: #f7f9fa; }
.nav-inner { display: flex; flex-wrap: wrap; gap: 8px 28px; padding: 15px 36px; }
nav a { text-decoration: none; font-size: 14px; line-height: 1.7; font-weight: 550; }
nav a:hover { text-decoration: underline; }
nav span { color: #747a83; font-size: 12px; margin-right: 5px; font-variant-numeric: tabular-nums; }
main { padding: 0 36px; }
.paper { padding: 30px 0 28px; border-bottom: 1px solid var(--line); scroll-margin-top: 0; }
.paper-heading { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
.paper-title { display: flex; align-items: baseline; gap: 12px; min-width: 0; }
.paper-number { color: #858a90; font-size: 13px; font-variant-numeric: tabular-nums; }
h2 { font-size: 23px; line-height: 1.4; margin: 0; overflow-wrap: anywhere; }
.source { font-size: 13px; flex-shrink: 0; }
.full-title { font-size: 14px; line-height: 1.65; margin: 8px 0 3px; overflow-wrap: anywhere; }
.venue { font-size: 12px; color: var(--muted); margin: 0 0 21px; }
.comparison { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; }
.version { min-width: 0; border-top: 3px solid var(--author); padding-top: 13px; }
.writer { border-color: var(--writer); }
.version-heading { display: flex; align-items: baseline; justify-content: space-between;
  gap: 8px 15px; flex-wrap: wrap; margin-bottom: 13px; }
h3 { font-size: 15px; line-height: 1.6; margin: 0; color: var(--author); }
.writer h3 { color: var(--writer); }
.word-count { font-size: 12px; line-height: 1.6; color: var(--muted); white-space: nowrap;
  font-variant-numeric: tabular-nums; }
.abstract { margin: 0; font-size: 17px; line-height: 1.95; text-align: left; overflow-wrap: anywhere; }
details { margin-top: 23px; padding-top: 15px; border-top: 1px solid #e9ebed; }
summary { width: fit-content; cursor: pointer; font-size: 14px; line-height: 1.8; color: #505860; }
summary:hover { color: var(--ink); }
dl { margin: 16px 0 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
dt { font-size: 13px; font-weight: 600; margin-bottom: 6px; }
dd { font-size: 14px; color: #565e65; line-height: 1.85; margin: 0; overflow-wrap: anywhere; }
footer { background: #f7f9fa; }
.footer-inner { padding: 23px 36px 30px; font-size: 12px; line-height: 1.9; color: var(--muted); }
.footer-inner p { margin: 0 0 6px; }
@media (max-width: 760px) {
  html { scroll-padding-top: 15px; }
  .page-heading { padding: 23px 20px 20px; }
  h1 { font-size: 23px; }
  nav { position: static; }
  .nav-inner { padding: 12px 20px; gap: 8px 19px; }
  main { padding: 0 20px; }
  .paper { padding: 25px 0; }
  h2 { font-size: 21px; }
  .comparison { grid-template-columns: minmax(0, 1fr); gap: 25px; }
  .abstract { font-size: 16px; line-height: 1.95; }
  dl { grid-template-columns: minmax(0, 1fr); gap: 17px; }
  .footer-inner { padding: 20px; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
@media print {
  html { scroll-behavior: auto; }
  nav, .source { display: none; }
  .page-heading, main, .footer-inner { padding-inline: 0; }
  .paper { break-before: page; }
  .paper:first-child { break-before: auto; }
  .comparison { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }
  .abstract { font-size: 11pt; line-height: 1.7; }
  details { display: none; }
  .version-heading, .paper-heading { break-after: avoid; }
}
</style>
</head>
<body>
<header class="page-heading">
<p class="eyebrow">SUPER WRITER · 2026-10-27 · 5 篇论文</p>
<h1>五篇论文摘要 · 中文对照</h1>
<p class="context">左栏为作者摘要的中文概述，并非原摘要全文译文；右栏为前轮独立英文稿的中文翻译。写作者仅接收正文证据包，未提供作者摘要。</p>
<p class="context">英文词数沿用前轮记录，不是本页中文长度。本页呈现已有结果与取舍，不代表新版本优于原论文。</p>
</header>
<nav aria-label="论文目录"><div class="nav-inner">""" + "".join(links) + """</div></nav>
<main>""" + "".join(sections) + """</main>
<footer><div class="footer-inner">
<p>作者摘要、独立生成稿的来源与接触范围不同；此对照不是受控盲评。差异说明沿用前轮分析，未新增独立评审或事实认证。</p>
<a href="README.md">测试说明</a> · <a href="results.json">完整数据</a> · <a href="receipts.json">来源记录</a>
</div></footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the generated HTML differs")
    args = parser.parse_args()
    data = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    expected = render(data)
    output = ROOT / "comparison.html"
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != expected:
            parser.exit(1, "comparison.html is out of date; run render.py\n")
        print("comparison.html matches results.json")
    else:
        output.write_text(expected, encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
