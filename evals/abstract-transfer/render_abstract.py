"""Render every saved abstract verbatim, including unsuccessful cases."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def esc(value):
    return html.escape(str(value), quote=True)


def prose(condition, m):
    return next(r["abstract"] for r in read(f"raw/{condition}_{m['group']}_{m['sample']}.json")["cases"] if r["id"] == m["paper"])


def main():
    summary = read("summary.json")
    votes, audits = read("decoded_votes.json"), read("decoded_audits.json")
    outcomes = {r["id"]: r["outcome"] for r in read("pair_results.json")}
    papers = {p["id"]: p for p in read("papers.json")}
    articles = []
    for m in read("mapping.json"):
        cols = []
        for condition in ("baseline", "candidate"):
            n = next(n for n in (1, 2) if m[f"reader_{n}"]["condition"] == condition)
            reading = next(r for r in read(f"raw/reader_{m['group']}_{n}.json")["readings"] if r["id"] == m[f"reader_{n}"]["id"])
            detail = "".join(f"<p><strong>{esc(k)}:</strong> {esc(reading[k])}</p>" for k in ("core", "scope", "core_witness", "scope_witness", "unclear"))
            detail += "".join(f'<p><strong>Audit {a["auditor"]}: {esc(a["fidelity"])}, {esc(a["critical_support"])}, {esc(a["reader_support"])}</strong>. {esc(a["reason"])}</p>' for a in audits if a["pair"] == m["id"] and a["condition"] == condition)
            cols.append(f'<section class="version"><h3>{condition.title()}</h3><p class="prose">{esc(prose(condition,m))}</p><details><summary>Reader / source audit</summary>{detail}</details></section>')
        preferences = "".join(f'<p><strong>Reviewer {v["reviewer"]}: {esc(v["winner"])}</strong>. {esc(v["reason"])}</p>' for v in votes if v["pair"] == m["id"])
        question = read(f"anchors/{m['paper']}.json")["critical_question"]
        articles.append(f'<article id="{m["id"]}" data-paper="{m["paper"]}" data-sample="{m["sample"]}"><h2>{m["paper"]} / Sample {m["sample"]}</h2><p class="title">{esc(papers[m["paper"]]["title"])}</p><p class="outcome">{esc(outcomes[m["id"]])}</p><div class="columns">{"".join(cols)}</div><details><summary>Anonymous preferences</summary>{preferences}</details><details><summary>Shared initial draft</summary><p class="initial-prose">{esc(prose("initial",m))}</p></details><details><summary>Frozen audit question</summary><p>{esc(question)}</p></details></article>')
    counts = summary["votes"]
    options = "".join(f'<option>{pid}</option>' for pid in papers)
    content = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Abstract transfer comparison</title><style>
*{box-sizing:border-box}body{margin:0;background:#fff;color:#24272b;font:15px/1.55 system-ui,sans-serif;letter-spacing:0}
header,main{max-width:1400px;margin:auto;padding:24px}header,article{border-bottom:1px solid #cdd2d8}h1{font-size:26px;margin:0 0 10px}h2{font-size:20px;margin:0 0 6px}h3{font-size:17px;margin:0 0 10px}p{margin:8px 0;overflow-wrap:anywhere}.title{color:#59616a}.outcome{font-weight:600;color:#364659}.toolbar{display:flex;gap:18px;flex-wrap:wrap;margin-top:18px}label{display:flex;gap:8px;align-items:center}select{max-width:100%;font:inherit;padding:6px;border:1px solid #aeb6c0;border-radius:4px;background:white}article{padding:24px 0}.columns{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px;margin-top:20px}.version{min-width:0}.version:first-child h3{color:#a7394c}.version:last-child h3{color:#246a54}.prose,.initial-prose{font:19px/1.65 Georgia,serif;white-space:pre-wrap}details{margin-top:16px}summary{cursor:pointer;color:#46505e}details p{font-size:14px}.initial-prose{font-size:18px}a{color:#246b97}[hidden]{display:none!important}@media(max-width:760px){header,main{padding:18px}.columns{grid-template-columns:minmax(0,1fr);gap:22px}.prose{font-size:18px}h1{font-size:24px}}
</style><header><h1>Abstract transfer comparison</h1>'''
    content += f'<p>6 papers / 2 samples / 12 pairs. Votes: candidate {counts.get("candidate",0)}, baseline {counts.get("baseline",0)}, tie {counts.get("tie",0)}.</p><p><a href="README.md">Evidence and limitations</a> / <a href="summary.json">Complete results</a></p>'
    content += f'<div class="toolbar"><label>Paper<select id="paper"><option value="all">All</option>{options}</select></label><label>Sample<select id="sample"><option value="all">All</option><option>1</option><option>2</option></select></label></div></header><main>{"".join(articles)}</main>'
    content += '''<script>const paper=document.getElementById('paper'),sample=document.getElementById('sample');function filter(){document.querySelectorAll('article').forEach(a=>a.hidden=(paper.value!=='all'&&paper.value!==a.dataset.paper)||(sample.value!=='all'&&sample.value!==a.dataset.sample))}paper.addEventListener('change',filter);sample.addEventListener('change',filter);</script></html>'''
    with (ROOT / "comparison.html").open("x", encoding="utf-8") as stream:
        stream.write(content)


if __name__ == "__main__":
    main()
