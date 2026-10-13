"""Display all original synthetic controls and preserved anonymous judgments."""

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def esc(value):
    return html.escape(str(value), quote=True)


def main():
    cases = read("cases.json")["cases"]
    summary = read("summary.json")
    votes = read("decoded_votes.json")
    audits = read("decoded_audits.json")
    mapping = read("mapping.json")["texts"]
    readings = {r["id"]: r for n in range(1, 5) for r in read(f"raw/reader_{n}.json")["readings"]}
    body = []
    for case in cases:
        columns = []
        for variant in ("v1", "v2"):
            key = next(m for m in mapping if m["case"] == case["id"] and m["variant"] == variant)
            reading = readings[key["id"]]
            records = [a for a in audits if a["id"] == key["id"]]
            reasons = "".join(f'<p><b>{esc(a["phase"])} auditor {a["auditor"]}:</b> '
                f'{esc(a["fidelity"])}; {esc(a.get("critical_support", "core " + str(a.get("core_recovery")) + ", scope " + str(a.get("scope_recovery"))))}. '
                f'{esc(a["reason"])}</p>' for a in records)
            columns.append(f'<section class="version"><h3>Variant {variant[-1]}</h3>'
                f'<p class="muted">Editorial expectation: {esc(case["oracle"]["support"][variant])}</p>'
                f'<p class="prose">{esc(case["variants"][variant])}</p>'
                '<details><summary>Reader and both source-audit rubrics</summary>'
                f'<p><b>Core:</b> {esc(reading["core"])}</p><p><b>Scope:</b> {esc(reading["scope"])}</p>'
                f'<p><b>Core witness:</b> {esc(reading["core_witness"])}</p>'
                f'<p><b>Scope witness:</b> {esc(reading["scope_witness"])}</p>'
                f'<p><b>Unclear:</b> {esc(reading["unclear"])}</p>{reasons}</details></section>')
        reviews = "".join(f'<p><b>Reviewer {v["reviewer"]}: {esc(v["winner"])}</b> {esc(v["reason"])}</p>'
                          for v in votes if v["case"] == case["id"])
        body.append(f'<article id="{case["id"]}" data-category="{case["category"].split("_")[0]}">'
                    f'<h2>{case["id"]}: {esc(case["category"])} / {esc(case["unit"])}</h2>'
                    f'<p><b>Critical question:</b> {esc(case["question"])}</p>'
                    f'<div class="columns">{"".join(columns)}</div>'
                    f'<details><summary>Anonymous preferences</summary>{reviews}</details>'
                    '<details><summary>Supplied fictional evidence and editorial expectation</summary>'
                    f'<p>{esc(case["evidence"])}</p><p><b>Relation:</b> {esc(case["relation"])}</p>'
                    f'<p><b>Oracle:</b> {esc(case["oracle"]["reason"])}</p></details></article>')
    criteria = "".join(f'<tr><td>{esc(c["name"])}</td><td>{c["observed"]}/{c["total"]}</td>'
                       f'<td>{"pass" if c["pass"] else "FAIL"}</td></tr>' for c in summary["admission"]["criteria"])
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Super Writer: Evaluator Controls</title>
<style>*{box-sizing:border-box}body{margin:0;color:#25272b;background:white;font:15px/1.55 system-ui,sans-serif;letter-spacing:0}
header,main{max-width:1360px;margin:auto;padding:24px 28px}header{border-bottom:1px solid #ddd}h1{font-size:24px;margin:0 0 8px}
h2{font-size:18px;margin:0}h3{font-size:16px;margin:0;color:#285c46}p{margin:8px 0}.muted{color:#62676c}a{color:#245e8f}
article{padding:28px 0;border-bottom:1px solid #ddd;scroll-margin-top:20px}.columns{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px;margin-top:18px}
.version{min-width:0}.version:first-child h3{color:#943b45}.prose{font:18px/1.75 Georgia,serif;white-space:pre-wrap;overflow-wrap:anywhere}
details{margin-top:16px;overflow-wrap:anywhere;font-size:14px}summary{cursor:pointer;color:#4c525a}table{border-collapse:collapse;font-size:13px;width:100%;margin:14px 0}
td,th{text-align:left;padding:7px;border-bottom:1px solid #ddd}label{display:flex;align-items:center;gap:12px;padding:16px 0}select{font:inherit;padding:6px;border:1px solid #aaa;border-radius:4px;background:white}
[hidden]{display:none!important}@media(max-width:760px){header,main{padding:18px}.columns{grid-template-columns:1fr;gap:22px}.version+.version{border-top:1px solid #ddd;padding-top:18px}.prose{font-size:17px}}
</style></head><body>'''
    page += ('<header><h1>Super Writer: Evaluator Controls</h1><p>12 synthetic cases; 24 passages; 2026-10-11</p>'
             f'<p>Prespecified admission: <b>{"PASS" if summary["admission"]["pass"] else "STOP"}</b>. '
             'Calibration of constructed controls is not improved writing, a real-paper benchmark or human validation.</p>'
             '<p>All judgments and editorial expectations remain visible. No raw answer was repaired.</p>'
             '<p><a href="../../docs/evaluator-control-calibration.md">Full report</a> &middot; <a href="summary.json">Raw summary</a></p>'
             f'<details><summary>Every admission criterion</summary><table><thead><tr><th>Criterion</th><th>Observed</th><th>Result</th></tr></thead><tbody>{criteria}</tbody></table></details>'
             '</header><main><label>Category<select id="category"><option value="all">All</option><option value="relation">Relation</option>'
             '<option value="metric">Metric</option><option value="condition">Condition</option><option value="neutral">Neutral</option></select></label>'
             '<p id="count" class="muted">12 cases</p>' + ''.join(body) + '</main>'
             '<script>document.getElementById("category").addEventListener("change",e=>{let n=0;document.querySelectorAll("article").forEach(a=>{'
             'const show=e.target.value==="all"||a.dataset.category===e.target.value;a.hidden=!show;if(show)n++;});document.getElementById("count").textContent=n+" cases";});</script></body></html>')
    with (ROOT / "comparison.html").open("x", encoding="utf-8") as stream:
        stream.write(page)
    print("Rendered all 12 synthetic cases without changing raw text")


if __name__ == "__main__":
    main()
