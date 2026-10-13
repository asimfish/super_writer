"""Render only original generated prose and preserved judgments, never source bodies."""

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads((ROOT / path).read_text())


def esc(value):
    return html.escape(str(value), quote=True)


def main(output="comparison.html"):
    summary = read("summary.json")
    pairs = read("pair_results.json")
    votes = read("decoded_votes.json")
    audits = read("decoded_audits.json")
    secondary = read("supplemental/decoded_audits.json") if (ROOT / "supplemental/decoded_audits.json").is_file() else []
    supplementary = {(a["pair"], a["condition"]): a for a in secondary}
    domains = read("domains.json")
    papers = {p[0]: (p[1], d["id"]) for d in domains for p in d["papers"]}
    units = {"abstract": "Abstract", "methods": "Methods / Analysis", "results": "Results"}
    labels = {"baseline": "Baseline", "candidate": "Candidate", "tie": "Tie"}
    cases = {}
    budgets = read("word_counts.json")
    readings = {}
    for domain in domains:
        did = domain["id"]
        for sample in (1, 2, 3):
            for condition in ("initial", "baseline", "candidate"):
                for case in read(f"raw/{condition}_{did}_{sample}.json")["cases"]:
                    cases[case["id"], sample, condition] = case
        for reader in (1, 2):
            for row in read(f"raw/reader_{did}_{reader}.json")["readings"]:
                readings[row["id"]] = row
    sections = []
    for pair in pairs:
        pid, sample, unit = pair["paper"], pair["sample"], pair["unit"]
        concerned = any(f != "pass" for f in pair["fidelity"].values()) or any(
            supplementary.get((pair["id"], c), {}).get("fidelity", "pass") != "pass"
            for c in ("baseline", "candidate"))
        pv = [v for v in votes if v["id"] == pair["id"]]
        columns = []
        for condition in ("baseline", "candidate"):
            text = cases[pid, sample, condition][unit]
            audit = next(a for a in audits if a["pair"] == pair["id"] and a["condition"] == condition)
            reading = readings[audit["id"]]
            budget = next(c for c in budgets if c["paper"] == pid and c["sample"] == sample
                          and c["unit"] == unit and c["condition"] == condition)
            sa = supplementary.get((pair["id"], condition))
            extra = (f'<p class="secondary-audit"><b>Supplementary text-only audit:</b> '
                     f'{esc(sa["fidelity"])}; core {sa["core_recovery"]}/2; '
                     f'scope {sa["scope_recovery"]}/2. {esc(sa["reason"])}</p>') if sa else ""
            source_label = f'Primary: {esc(audit["fidelity"])}'
            if sa:
                source_label += f'; text-only: {esc(sa["fidelity"])}'
            columns.append(
                f'<section class="version"><h3>{labels[condition]} '
                f'<span class="fidelity">{source_label}</span></h3>'
                f'<p class="muted">{budget["words"]} words; '
                f'{"within budget" if budget["budget_pass"] else "OUTSIDE word budget"}</p>'
                f'<p class="prose">{esc(text)}</p>'
                '<details><summary>Reader reconstruction and source audit</summary>'
                f'<p><b>Core:</b> {esc(reading["core_relation"])}</p>'
                f'<p><b>Scope:</b> {esc(reading["scope"])}</p>'
                f'<p><b>Witness:</b> {esc(reading["witness"])}</p>'
                f'<p><b>Unclear:</b> {esc(reading["unclear"])}</p>'
                f'<p><b>Recovery scores:</b> core {audit["core_recovery"]}/2; '
                f'scope {audit["scope_recovery"]}/2.</p>'
                f'<p><b>Primary audit:</b> {esc(audit["reason"])}</p>{extra}</details></section>'
            )
        reviewers = "".join(f'<p><b>Reviewer {v["reviewer"]}: {labels[v["winner"]]}</b> '
                            f'{esc(v["reason"])}</p>' for v in pv)
        sections.append(
            f'<article id="{pair["id"]}" data-paper="{pid}" data-unit="{unit}" data-sample="{sample}" '
            f'data-concern="{str(concerned).lower()}"><h2>{pid} / {units[unit]} / Sample {sample}</h2>'
            f'<p class="title">{esc(papers[pid][0])}</p><div class="columns">{"".join(columns)}</div>'
            f'<details class="judgments"><summary>Anonymous preference reasons</summary>{reviewers}</details>'
            '<details><summary>Shared initial draft</summary>'
            f'<p class="prose">{esc(cases[pid, sample, "initial"][unit])}</p></details></article>'
        )
    rows = []
    for domain in domains:
        result = summary["by_domain"][domain["id"]]
        v = result["votes"]
        sa = result["source_audit"]
        rr = result["reader_recovery"]
        rows.append(f'<tr><th>{esc(domain["domain"])}</th><td>{v.get("candidate",0)}</td>'
                    f'<td>{v.get("baseline",0)}</td><td>{v.get("tie",0)}</td>'
                    f'<td>{sa["candidate"].get("concern",0)} / {sa["candidate"].get("fail",0)}</td>'
                    f'<td>{sa["baseline"].get("concern",0)} / {sa["baseline"].get("fail",0)}</td>'
                    f'<td>{rr["candidate"]["core_recovery"]["mean"]:.2f} / '
                    f'{rr["baseline"]["core_recovery"]["mean"]:.2f}</td></tr>')
    options = ''.join(f'<option value="{pid}">{pid}: {esc(title)}</option>'
                      for pid, (title, _) in papers.items())
    overall = summary["overall"]["votes"]
    page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Super Writer: Broad Writing Comparison</title>
<style>
*{box-sizing:border-box}body{margin:0;color:#24262a;background:#fff;font:15px/1.55 system-ui,sans-serif;letter-spacing:0}
header,main{max-width:1360px;margin:auto;padding:24px 28px}header{border-bottom:1px solid #ddd}h1{font-size:24px;margin:0 0 8px}
h2{font-size:18px;margin:0}h3{font-size:16px;margin:0 0 14px;color:#285c46}h3 .fidelity{font-size:12px;font-weight:500;color:#555;display:block}
p{margin:8px 0}a{color:#245e8f}.title,.muted{color:#64676d}.filters{display:flex;flex-wrap:wrap;gap:14px;align-items:end;padding:18px 0;border-bottom:1px solid #ddd}
label{display:flex;flex-direction:column;gap:4px;min-width:0}select{font:inherit;font-size:14px;padding:7px;max-width:100%;border:1px solid #bbb;border-radius:4px;background:white;color:#222}
.paper-filter{max-width:600px;flex:1 1 320px}.checkbox{flex-direction:row;align-items:center;padding-bottom:6px;gap:6px}
article{padding:28px 0;border-bottom:1px solid #ddd;scroll-margin-top:20px}.columns{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px;margin-top:18px}
.version{min-width:0}.version:first-child h3{color:#943b45}.prose{font:18px/1.75 Georgia,serif;white-space:pre-wrap;overflow-wrap:anywhere}
details{margin-top:16px;font-size:14px;overflow-wrap:anywhere}summary{cursor:pointer;color:#4c525a}details p{margin:10px 0}
.table-wrap{overflow:auto;margin-top:16px}table{border-collapse:collapse;font-size:13px;min-width:790px;width:100%}td,th{text-align:left;padding:9px;border-bottom:1px solid #ddd}thead th{background:#f1f3f4}tbody th{font-weight:500}
[hidden]{display:none!important}@media(max-width:760px){header,main{padding:18px}.columns{grid-template-columns:1fr;gap:22px}.version+.version{border-top:1px solid #ddd;padding-top:18px}.prose{font-size:17px}}
</style></head><body>'''
    page += (
        '<header><h1>Super Writer: Broad Writing Comparison</h1>'
        '<p>12 papers &middot; 6 domains &middot; 3 repetitions &middot; 108 paired units &middot; 2026-10-11</p>'
        f'<p>Anonymous votes: candidate {overall.get("candidate",0)}, baseline {overall.get("baseline",0)}, '
        f'tie {overall.get("tie",0)}. These are clustered model judgments, not quality percentages.</p>'
        '<p class="muted">All raw outputs are unchanged. Source concerns, disagreements and budget failures remain visible. '
        'Sources and author abstracts are not redistributed. Readers/reviewers are same-family models, not humans.</p>'
        '<p>No overall writing gain was demonstrated. The table below reports the primary audit. '
        'A separate, operationally triggered text-only audit does not replace it.</p>'
        '<p><a href="../../docs/broad-writing-evaluation.md">Full report</a> &middot; '
        '<a href="supplemental/summary.json">Separate text-only audit summary</a></p>'
        '<div class="table-wrap"><table><thead><tr><th>Domain</th><th>Candidate votes</th><th>Baseline votes</th>'
        '<th>Ties</th><th>Candidate source concerns / fails</th><th>Baseline source concerns / fails</th>'
        '<th>Reader core recovery mean (0-2), candidate / baseline</th></tr></thead><tbody>'
        + ''.join(rows) + '</tbody></table></div></header><main>'
        '<div class="filters"><label class="paper-filter">Paper<select id="paper"><option value="all">All papers</option>'
        + options + '</select></label><label>Unit<select id="unit"><option value="all">All units</option>'
        '<option value="abstract">Abstract</option><option value="methods">Methods / Analysis</option>'
        '<option value="results">Results</option></select></label><label>Sample<select id="sample">'
        '<option value="all">All samples</option><option>1</option><option>2</option><option>3</option></select></label>'
        '<label class="checkbox"><input type="checkbox" id="concern">Source concerns only</label></div>'
        '<p id="count" class="muted">108 pairs</p>' + ''.join(sections) + '</main>'
        '<script>const ids=["paper","unit","sample","concern"];'
        'function filter(){let n=0;document.querySelectorAll("article").forEach(a=>{'
        'const show=ids.slice(0,3).every(id=>document.getElementById(id).value==="all"||'
        'a.dataset[id]===document.getElementById(id).value)&&(!document.getElementById("concern").checked||'
        'a.dataset.concern==="true");a.hidden=!show;if(show)n++;});'
        'document.getElementById("count").textContent=n+" pairs";}'
        'ids.forEach(id=>document.getElementById(id).addEventListener("change",filter));</script></body></html>'
    )
    target = ROOT / output
    if target.exists():
        raise FileExistsError(target)
    target.write_text(page, encoding="utf-8")
    print(f"Rendered {len(pairs)} pairs, untouched generated prose only: {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="comparison.html")
    main(parser.parse_args().output)
