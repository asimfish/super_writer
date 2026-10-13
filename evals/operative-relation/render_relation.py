"""Display every saved pair without repairing or selecting model prose."""

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def esc(value):
    return html.escape(str(value), quote=True)


def main():
    summary = read("summary.json")
    mapping = read("mapping.json")
    votes = read("decoded_votes.json")
    audits = read("decoded_audits.json")
    outcomes = {p["id"]: p for p in read("pair_results.json")}
    papers = {p["id"]: p for p in read("papers.json")}
    articles = []
    for m in mapping:
        pid, sample, unit = m["paper"], m["sample"], m["unit"]
        columns = []
        for c in ("baseline", "candidate"):
            prose = read(f"raw/{c}_{pid}_{sample}.json")[unit]
            reader = next((n, m[f"reader_{n}"]["id"]) for n in (1, 2) if m[f"reader_{n}"]["condition"] == c)
            reading = next(r for r in read(f"raw/reader_{pid}_{reader[0]}.json")["readings"] if r["id"] == reader[1])
            detail = "".join(f"<p><strong>{esc(k)}:</strong> {esc(reading[k])}</p>" for k in ("core", "scope", "core_witness", "scope_witness", "unclear"))
            detail += "".join(f'<p><strong>Auditor {a["auditor"]}:</strong> {esc(a["fidelity"])}; '
                f'{esc(a["critical_support"])}; {esc(a["reader_support"])}. {esc(a["reason"])}</p>'
                for a in audits if a["pair"] == m["id"] and a["condition"] == c)
            columns.append(f'<section class="version"><h3>{esc(c.title())}</h3><p class="prose" data-condition="{c}">{esc(prose)}</p>'
                           f'<details><summary>Reader and source audit</summary>{detail}</details></section>')
        preferences = "".join(f'<p><strong>Reviewer {v["reviewer"]}: {esc(v["winner"])}</strong>. {esc(v["reason"])}</p>'
                              for v in votes if v["pair"] == m["id"])
        initial = read(f"raw/initial_{pid}_{sample}.json")[unit]
        objective = read(f"requests/{pid}.json")["questions"][unit]
        articles.append(f'<article id="{esc(m["id"])}" data-paper="{pid}" data-unit="{unit}">'
            f'<h2>{esc(pid)} / Sample {sample} / {esc(unit.title())}</h2><p class="title">{esc(papers[pid]["title"])}</p>'
            f'<p><strong>Frozen objective:</strong> {esc(objective)}</p><p class="outcome">{esc(outcomes[m["id"]]["outcome"])}</p>'
            f'<div class="columns">{"".join(columns)}</div><details><summary>Anonymous preferences</summary>{preferences}</details>'
            f'<details><summary>Shared initial draft</summary><p class="initial-prose">{esc(initial)}</p></details></article>')
    counts = summary["votes"]
    content = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Operative-relation revision comparison</title><style>
*{box-sizing:border-box}body{margin:0;color:#24272b;background:#fff;font:15px/1.55 system-ui,sans-serif;letter-spacing:0}
header,main{max-width:1400px;margin:auto;padding:24px}header{border-bottom:1px solid #cdd2d8}h1{font-size:26px;margin:0 0 10px}
h2{font-size:20px;margin:0 0 6px}h3{font-size:17px;margin:0 0 10px}p{margin:8px 0;overflow-wrap:anywhere}
.title{color:#59616a}.outcome{color:#364659;font-weight:600}.toolbar{display:flex;gap:18px;flex-wrap:wrap;margin-top:18px}
label{display:flex;gap:8px;align-items:center}select{max-width:100%;font:inherit;padding:6px;border:1px solid #aeb6c0;border-radius:4px;background:white}
article{padding:24px 0;border-bottom:1px solid #cdd2d8}.columns{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px;margin-top:20px}
.version{min-width:0}.version:first-child h3{color:#a7394c}.version:last-child h3{color:#246a54}.prose,.initial-prose{font:19px/1.65 Georgia,serif;white-space:pre-wrap}
details{margin-top:16px}summary{cursor:pointer;color:#46505e}details p{font-size:14px}.initial-prose{font-size:18px}a{color:#246b97}
[hidden]{display:none!important}@media(max-width:760px){header,main{padding:18px}.columns{grid-template-columns:minmax(0,1fr);gap:22px}.prose{font-size:18px}h1{font-size:24px}}
</style><header><h1>Operative-relation revision comparison</h1>"""
    content += f'<p>2 papers · 2 samples · 3 units · 12 pairs. Votes: candidate {counts.get("candidate",0)}, baseline {counts.get("baseline",0)}, tie {counts.get("tie",0)}.</p>'
    content += '<p>Targeted same-family model test, not human review or general effectiveness. Source PDFs and publisher prose are not redistributed.</p>'
    content += '<p><a href="README.md">Archive and limitations</a> · <a href="summary.json">All counts and violations</a></p>'
    content += '<div class="toolbar"><label>Paper<select id="paper"><option value="all">All papers</option><option>N1</option><option>N2</option></select></label>'
    content += '<label>Unit<select id="unit"><option value="all">All units</option><option value="abstract">Abstract</option><option value="methods">Methods / Analysis</option><option value="results">Results</option></select></label></div></header>'
    content += '<main>' + "".join(articles) + '</main><script>const paper=document.getElementById("paper"),unit=document.getElementById("unit");'
    content += 'function filter(){document.querySelectorAll("article").forEach(a=>a.hidden=(paper.value!=="all"&&a.dataset.paper!==paper.value)||(unit.value!=="all"&&a.dataset.unit!==unit.value))}paper.addEventListener("change",filter);unit.addEventListener("change",filter);</script></html>'
    with (ROOT / "comparison.html").open("x", encoding="utf-8") as stream:
        stream.write(content)


if __name__ == "__main__":
    main()
