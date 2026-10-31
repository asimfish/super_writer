"""Render source-calibrated abstract demonstrations; not a quality scorer."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from writing_benchmark import word_count


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render() -> str:
    natural = load(ROOT / "natural_candidates.json")
    prior = {p["id"]: p for p in load(REPO / "evals/abstract-argument/corrections.json")["papers"]}
    previous = {p["id"]: p for p in load(REPO / "evals/abstract-argument/candidates.json")["papers"]}
    authors = {p["id"]: p for p in load(REPO / "evals/abstract-five/results.json")["papers"]}
    sections, links = [], []
    esc = html.escape
    for paper in natural["papers"]:
        ident = esc(paper["id"], quote=True)
        author = authors[paper["id"]]
        old = prior.get(paper["id"], previous[paper["id"]])
        old_en = old.get("replacement", old)["text_en"]
        links.append(f'<a href="#{ident}">{esc(author["short_title"])}</a>')
        cards = []
        for label, kind, prose, english in (
            ("作者摘要 · 中文概述", "author", author["author_summary_zh"], None),
            ("上一轮候选 · 中文译稿", "previous", old.get("replacement", old)["text_zh"], old_en),
            ("本轮 source-calibrated · 中文译稿", "natural", paper["text_zh"], paper["text_en"]),
        ):
            english_block = (f'<details><summary>英文稿 · {word_count(english)} 词</summary>'
                             f'<p lang="en">{esc(english)}</p></details>') if english else ""
            cards.append(f'<article class="card {kind}"><h3>{label}</h3>'
                         f'<p>{esc(prose)}</p>{english_block}</article>')
        shape = (f'<p><strong>原文形状：</strong>{esc(paper["shape"]["opening"])}；'
                 f'{esc(paper["shape"]["progression"])}；'
                 f'{esc(paper["shape"]["abstraction"])}；'
                 f'{esc(paper["shape"]["ending"])}。</p>')
        sections.append(
            f'<section id="{ident}"><header><h2>{esc(author["short_title"])}</h2>'
            f'<a href="{esc(paper["source_url"], quote=True)}" target="_blank" '
            'rel="noopener noreferrer">原文页面</a></header>'
            f'<p class="title" lang="en">{esc(paper["title"])}</p>'
            f'<div class="cards">{"".join(cards)}</div>'
            f'<details class="shape"><summary>为什么这一版更接近原文组织方式</summary>'
            f'{shape}<p><strong>本轮改动：</strong>{esc(paper["changes"])}</p></details></section>')
    return '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><title>摘要自然度校准 | Super Writer</title>
<style>
*{box-sizing:border-box}html{scroll-padding-top:70px}body{margin:0;color:#252a2d;background:#fff;letter-spacing:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}
a{color:#246d73;text-underline-offset:4px}a:focus-visible,summary:focus-visible{outline:2px solid #287c67;outline-offset:4px}
.intro,main,nav>div,footer{max-width:1600px;margin:auto;padding-inline:32px}.intro{padding-block:30px 22px}h1{font-size:27px;line-height:1.4;margin:0 0 12px}.intro p{max-width:1120px;font-size:14px;line-height:1.9;color:#566066;margin:6px 0}
nav{border-block:1px solid #dce3e3;background:#f6f8f8;position:sticky;top:0;z-index:2}nav>div{display:flex;flex-wrap:wrap;gap:12px 28px;padding-block:14px}nav a{text-decoration:none;font-size:14px}
section{padding-block:31px;border-bottom:1px solid #dce3e3}header{display:flex;align-items:baseline;justify-content:space-between;gap:16px}h2{font-size:23px;margin:0}header a{font-size:13px;flex-shrink:0}.title{font-size:14px;line-height:1.7;color:#5c666a;margin:7px 0 22px;overflow-wrap:anywhere}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}.card{min-width:0;border-top:3px solid #22666d;padding-top:13px}.card.previous{border-color:#8b727c}.card.natural{border-color:#337c45}.card h3{font-size:15px;line-height:1.6;margin:0 0 13px;color:#22666d}.card.previous h3{color:#825d6c}.card.natural h3{color:#337c45}.card>p{font-size:16px;line-height:1.95;margin:0;overflow-wrap:anywhere}
details{margin-top:18px}summary{cursor:pointer;color:#526168;font-size:13px;line-height:1.8;width:fit-content}.card details p{font-size:14px;line-height:1.85;overflow-wrap:anywhere}.shape{border-top:1px solid #e8ebeb;padding-top:14px}.shape p{font-size:14px;line-height:1.9;color:#4f595d;max-width:1100px;overflow-wrap:anywhere}footer{padding-block:22px 30px;font-size:12px;line-height:1.9;color:#657076}
@media(max-width:900px){html{scroll-padding-top:15px}nav{position:static}.intro,main,nav>div,footer{padding-inline:20px}h1{font-size:23px}.cards{grid-template-columns:minmax(0,1fr);gap:25px}section{padding-block:25px}h2{font-size:21px}}
@media print{nav{display:none}.intro,main,footer{padding-inline:0}section{break-before:page}section:first-child{break-before:auto}.cards{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.card>p{font-size:10pt;line-height:1.7}details{display:none}}
</style></head><body>
<div class="intro"><h1>五篇摘要：从技术摘要回到作者式表达</h1>
<p>这一页不是把原摘要逐字翻译，也不是盲测。作者栏沿用此前中文概述；上一轮候选保留；绿色栏是在读过官方摘要、对照正文事实后，按原文的信息层级重新组织的版本。</p>
<p>本轮重点不是减少数字，而是恢复自然的摘要节奏：先让读者知道研究问题或能力，再给贡献级方法，随后给同层级的验证，最后用意义、迁移或第二贡献收束。实现细节和逐项结果不再承担主线。</p>
</div><nav><div>''' + "".join(links) + '''</div></nav><main>''' + "".join(sections) + '''</main>
<footer>Super Writer · source-calibrated developmental examples · 不代表原作者认可，不构成写作质量提升证明。原文版权归论文作者及出版方所有。</footer></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = render()
    path = ROOT / "comparison.html"
    if args.check:
        if not path.is_file() or path.read_text(encoding="utf-8") != output:
            parser.exit(1, "Natural comparison HTML is stale\n")
    else:
        path.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
