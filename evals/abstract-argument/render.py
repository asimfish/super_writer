"""Render developmental author/prior/new comparisons; not a quality scorer."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "scripts"))
from writing_benchmark import word_count


def corrected(paper: dict, repair: dict | None) -> dict:
    if repair is None:
        return paper
    if any(paper[key] != repair["original"][key] for key in ("text_en", "text_zh")):
        raise ValueError("Correction no longer matches its raw candidate")
    return {**paper, **repair["replacement"]}


def render(candidates: dict, baseline: dict, authors: dict, audit: dict | None = None,
           corrections: dict | None = None, correction_audit: dict | None = None) -> str:
    esc = html.escape
    old = {p["id"]: p for p in baseline["papers"]}
    source = {p["id"]: p for p in authors["papers"]}
    reviews = {p["id"]: p for p in (audit or {}).get("papers", [])}
    repairs = {p["id"]: p for p in (corrections or {}).get("papers", [])}
    rechecks = {p["id"]: p for p in (correction_audit or {}).get("papers", [])}
    links, sections = [], []
    for raw in candidates["papers"]:
        repair = repairs.get(raw["id"])
        paper = corrected(raw, repair)
        ident = esc(paper["id"], quote=True)
        previous, author = old[paper["id"]], source[paper["id"]]
        name = esc(author["short_title"])
        links.append(f'<a href="#{ident}">{name}</a>')
        columns = []
        for label, kind, zh, en in (
            ("作者摘要 · 中文概述", "author", author["author_summary_zh"], None),
            ("上一版 · 原样保留", "previous", author["ours_zh"], previous["text_en"]),
            ("本轮候选 · 审读后修正" if repair else "本轮候选 · 中文译稿",
             "candidate", paper["text_zh"], paper["text_en"]),
        ):
            english = (f'<details class="english"><summary>英文稿 · {word_count(en)} 词</summary>'
                       f'<p lang="en">{esc(en)}</p></details>') if en else ""
            columns.append(f'<article class="version {kind}"><h3>{label}</h3>'
                           f'<p class="abstract">{esc(zh)}</p>{english}</article>')
        progression = "".join(f'<li>{esc(s)}</li>' for s in paper["progression_zh"])
        selection = "".join(
            f'<li><strong>{esc(s["question_zh"])}</strong> '
            f'{esc(s["reason_zh"])} <small>{esc(", ".join(s["evidence_ids"]))}</small></li>'
            for s in paper["selection"])
        notes = "".join(f'<li>{esc(s)}</li>' for s in paper["author_notes_zh"])
        review = reviews.get(paper["id"])
        review_html = (f'<p class="review">首轮候选的独立上下文审读：{esc(review["summary_zh"])}</p>'
                       if review else '<p class="review">独立审读尚未记录；不作事实或质量通过声明。</p>')
        correction_html = (f'<p class="review"><strong>本栏已作事实修正：</strong>{esc(repair["reason_zh"])}</p>'
                           '<details><summary>保留的首轮候选（修正前）</summary>'
                           f'<p>{esc(raw["text_zh"])}</p><p lang="en">{esc(raw["text_en"])}</p></details>'
                           if repair else "")
        if repair and paper["id"] in rechecks:
            correction_html += ('<p class="review">仅两处事实修正的单独复核：'
                                + esc(rechecks[paper["id"]]["summary_zh"]) + '</p>')
        sections.append(
            f'<section id="{ident}" class="paper"><header><h2>{name}</h2>'
            f'<a href="{esc(author["source_url"], quote=True)}" target="_blank" '
            'rel="noopener noreferrer">论文原文</a></header>'
            f'<p class="title" lang="en">{esc(author["title"])}</p>'
            '<p class="meta">CoRL 2024 · PMLR 270（2025 年出版）</p>'
            f'<div class="comparison">{"".join(columns)}</div>'
            '<details class="decisions"><summary>论证与证据取舍</summary>'
            f'<p><strong>主线：</strong>{esc(paper["thesis_zh"])}</p>'
            f'<ol>{progression}</ol><h4>证据分工</h4><ul>{selection}</ul>'
            f'<h4>保留的边界与待核验事项</h4><ul>{notes}</ul>'
            f'<p class="meta">使用的功能卡：{esc(", ".join(paper["pattern_ids"]))}</p>'
            f'{review_html}{correction_html}</details></section>'
        )
    return '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>五篇摘要 · 论证组织对照 | Super Writer</title>
<style>
*{box-sizing:border-box}html{scroll-padding-top:75px;color-scheme:light}
body{margin:0;color:#252a2d;background:white;letter-spacing:0;
font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}
a{color:#22666d;text-underline-offset:4px}a:focus-visible,summary:focus-visible{outline:2px solid #287c67;outline-offset:4px}
.heading,main,.nav-inner,footer{max-width:1640px;margin:auto;padding-inline:32px}
.heading{padding-block:30px 22px}h1{font-size:26px;line-height:1.4;margin:0 0 12px}
.context{font-size:14px;line-height:1.85;color:#565e63;max-width:1100px;margin:5px 0}
nav{position:sticky;top:0;z-index:2;background:#f6f8f8;border-block:1px solid #dce2e2}
.nav-inner{display:flex;flex-wrap:wrap;gap:12px 28px;padding-block:14px}nav a{font-size:14px;text-decoration:none}
.paper{padding-block:30px;border-bottom:1px solid #dce2e2}header{display:flex;align-items:baseline;justify-content:space-between;gap:16px}
h2{font-size:23px;margin:0;overflow-wrap:anywhere}header a{font-size:13px;flex-shrink:0}
.title{font-size:14px;line-height:1.7;margin:8px 0 3px;overflow-wrap:anywhere}.meta{font-size:12px;line-height:1.8;color:#687076;overflow-wrap:anywhere}
.comparison{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:22px}
.version{min-width:0;border-top:3px solid #22666d;padding-top:13px}.previous{border-color:#8b727c}.candidate{border-color:#337c45}
h3{font-size:15px;line-height:1.6;margin:0 0 14px;color:#22666d}.previous h3{color:#825d6c}.candidate h3{color:#337c45}
.abstract{font-size:16px;line-height:1.95;margin:0;overflow-wrap:anywhere}
details{margin-top:19px}summary{font-size:13px;line-height:1.8;cursor:pointer;width:fit-content;color:#536269}
.english p{font-size:14px;line-height:1.8;overflow-wrap:anywhere}.decisions{border-top:1px solid #e7eaea;padding-top:14px}
.decisions p,.decisions li{font-size:14px;line-height:1.9;overflow-wrap:anywhere}.decisions li{margin-bottom:8px}.decisions small{color:#70787b}
h4{font-size:14px;margin:18px 0 8px}.review{border-left:2px solid #89979b;padding-left:12px}footer{padding-block:22px 30px;font-size:12px;line-height:1.9;color:#647076}
@media(max-width:880px){html{scroll-padding-top:15px}nav{position:static}.heading,main,.nav-inner,footer{padding-inline:20px}
h1{font-size:23px}.comparison{grid-template-columns:minmax(0,1fr);gap:26px}.paper{padding-block:25px}h2{font-size:21px}}
@media print{nav{display:none}.heading,main,footer{padding-inline:0}.paper{break-before:page}.paper:first-child{break-before:auto}
.comparison{grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.abstract{font-size:10pt;line-height:1.7}details{display:none}}
</style></head><body>
<div class="heading"><h1>五篇摘要：从证据清单到论证主线</h1>
<p class="context">同一组论文与正文证据。作者栏沿用此前的中文概述，不是摘要逐字全译；上一版中文与英文稿均原样保留。本轮为读过这些论文后的开发性改写，不是新盲测，也不是等预算 A/B 实验。</p>
<p class="context">英文词数按统一规则重新统计，可能与旧页面的自报数不同。程序检查只能验证资源和产物，不证明文章更好；旧稿中的事实“通过”标签不作为本轮的独立认证。</p>
<p class="context">Sparsh 一栏为审读后事实修正稿；正文与表格冲突的判断已删除，首轮稿及发现问题的审读记录未覆盖。</p>
</div><nav aria-label="论文"><div class="nav-inner">''' + "".join(links) + '''</div></nav>
<main>''' + "".join(sections) + '''</main>
<footer>2026-10-29 · Super Writer · 开发性候选；质量尚未经过未见论文上的独立盲评。论文版权属于原作者，中文概述、生成稿与编辑分析不代表作者认可。页面可离线阅读。</footer>
</body></html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    load = lambda path: json.loads(path.read_text(encoding="utf-8"))
    audit_path = ROOT / "audit.json"
    correction_path = ROOT / "corrections.json"
    recheck_path = ROOT / "correction-audit.json"
    output = render(load(ROOT / "candidates.json"), load(ROOT / "baseline.json"),
                    load(ROOT.parent / "abstract-five/results.json"),
                    load(audit_path) if audit_path.exists() else None,
                    load(correction_path) if correction_path.exists() else None,
                    load(recheck_path) if recheck_path.exists() else None)
    path = ROOT / "comparison.html"
    if args.check:
        if not path.is_file() or path.read_text(encoding="utf-8") != output:
            parser.exit(1, "Comparison HTML is stale\n")
    else:
        path.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
