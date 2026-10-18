"""Build bounded pilot packets and reproduce the analysis of saved completions."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import random
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CONDITIONS = ("prior", "compression", "editorial")
CONTROLS = ("prior", "editorial", "initial")
UNITS = ("abstract", "results")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def count(text):
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def receipt(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    materials = {"papers": sum((read(ROOT / f"materials-{block}.json")["papers"]
                               for block in (1, 2)), [])}
    assert len(materials["papers"]) == 6
    assert {p["id"] for p in materials["papers"]} == {f"R{i:02}" for i in range(1, 7)}
    for paper in materials["papers"]:
        assert 7 <= len(paper["facts"]) <= 9
        assert len({f["id"] for f in paper["facts"]}) == len(paper["facts"])
        for unit in UNITS:
            assert len(paper["units"][unit]["questions"]) == 2
            assert 40 <= count(paper["units"][unit]["draft"]) <= (160 if unit == "abstract" else 130)
    write_new(ROOT / "materials.json", materials)
    common_paths = ("references/abstract-decisions.md", "references/argument-transfer.md")
    sys.path.insert(0, str(REPO / "scripts"))
    import writing_guide
    protocols = writing_guide.load_index()
    ai_spec = read(REPO / "references/ai-writing-spec.json")
    exemplar_text = (REPO / "references/abstract-exemplars.md").read_text(encoding="utf-8")
    exemplar_blocks = exemplar_text.split("\n## ")
    resources = {"abstract_protocol": writing_guide.report_for(protocols, "abstract", "empirical-method"),
                 "results_protocol": writing_guide.report_for(protocols, "experiments.analysis", "result-paragraph"),
                 "ai_rules": [e for e in ai_spec["entries"] if e["id"] in ("ai.rule.operation", "ai.rule.quantities")],
                 "exemplar_scope": "Existing local editorial abstract notes, not new source reading or Results exemplars",
                 "exemplar_notes": [b for b in exemplar_blocks if b.startswith(("05. ResNet", "14. Many Faces"))]}
    roles = ("agents/writing-gap-finder.md", "agents/revision-proposer.md",
             "agents/revision-writer.md", "agents/revision-reviewer.md")
    guides = {}
    for condition, commit in (("prior", "3f9d99c"), ("compression", "870a205")):
        paths = (*common_paths, *roles)
        if condition == "compression":
            paths += ("references/compression-first-writing.md",)
        guides[condition] = [{"path": path, "commit": commit, "text": subprocess.check_output(
            ["git", "show", f"{commit}:{path}"], cwd=REPO, text=True)} for path in paths]
    for block in (1, 2):
        papers = read(ROOT / f"materials-{block}.json")["papers"]
        cases = []
        for paper in papers:
            for unit in UNITS:
                cases.append({"id": f'{paper["id"]}-{unit}', "paper": paper["id"],
                              "unit": unit, "source": paper["source"],
                              "contribution": paper["contribution"], "facts": paper["facts"],
                              "draft": paper["units"][unit]["draft"],
                              "questions": paper["units"][unit]["questions"],
                              "max_words": 160 if unit == "abstract" else 130})
        for condition in CONDITIONS:
            ident = f"{condition}-{block}"
            instruction = ("Revise each supplied passage once for clear, precise academic writing. "
                           "Preserve the contribution, numerical referents and necessary conditions. "
                           "Use only supplied facts. Do not pad to a minimum. Answer the reader "
                           "questions in the prose. Return JSON with writer_id and cases: each case "
                           "has id, text, note. Notes stay outside manuscript prose. Return your "
                           "actual result even if it misses the budget. Do not read other inputs, "
                           "author abstracts or repository guides. No web searches or agents.")
            if condition == "editorial":
                instruction += " Improve clarity, concision and cohesion using ordinary editorial judgment."
            elif condition == "compression":
                instruction += (" Apply the attached guidance. First choose a target reader answer "
                                "and at most three priority gaps. Delete or merge before adding; "
                                "the revision must use no more words than its supplied draft. "
                                "In note state the target answer, removal/merge and necessary addition.")
            else:
                instruction += (" Apply the attached guidance. Diagnose the passage against its "
                                "section function, propose the applicable repair, realize it, "
                                "then read it back once. In note state the diagnosed gap and repair.")
            packet = {"writer_id": ident, "instruction": instruction,
                      "counting_rule": "ASCII alphanumeric tokens joined by hyphens/apostrophes",
                      "cases": cases, "guides": guides.get(condition, []),
                      "writing_resources": resources if condition != "editorial" else {}}
            write_new(ROOT / "prompts" / f"{ident}.json", packet)
    names = ["PROTOCOL.md", "materials.json", "materials-1.json", "materials-2.json", "pilot.py", "source-receipts.json"]
    names += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "prompts").glob("*.json"))]
    write_new(ROOT / "freeze.json", {"date": "2026-10-18", "seed": 20261018,
                                    "conditions": list(CONDITIONS), "inputs": {
                                        name: receipt(ROOT / name) for name in names}})


def verify_freeze():
    frozen = read(ROOT / "freeze.json")
    for name, sha in frozen["inputs"].items():
        if receipt(ROOT / name) != sha:
            raise ValueError(f"Frozen input changed: {name}")
    return frozen


def generations():
    verify_freeze()
    result = {}
    for condition in CONDITIONS:
        for block in (1, 2):
            ident = f"{condition}-{block}"
            packet = read(ROOT / "prompts" / f"{ident}.json")
            data = read(ROOT / "raw" / f"{ident}.json")
            assert data["writer_id"] == ident
            expected = {row["id"] for row in packet["cases"]}
            assert len(data["cases"]) == len(expected)
            assert {row["id"] for row in data["cases"]} == expected
            for row in data["cases"]:
                assert isinstance(row["text"], str) and row["text"].strip()
                result[row["id"], condition] = row
    for paper in read(ROOT / "materials.json")["papers"]:
        for unit in UNITS:
            ident = f'{paper["id"]}-{unit}'
            result[ident, "initial"] = {"id": ident, "text": paper["units"][unit]["draft"],
                                        "note": "Shared initial draft"}
    return result


def blind():
    outputs = generations()
    papers = read(ROOT / "materials.json")["papers"]
    rng = random.Random(20261018)
    mapping = {}
    packets = {"J01": [], "J02": []}
    for paper in papers:
        for unit in UNITS:
            ident = f'{paper["id"]}-{unit}'
            order = [*CONDITIONS, "initial"]
            rng.shuffle(order)
            for judge in ("J01", "J02"):
                if judge == "J02":
                    order = list(reversed(order))
                labels = dict(zip(("A", "B", "C", "D"), order))
                mapping[judge, ident] = labels
                packets[judge].append({"id": ident, "unit": unit,
                    "contribution": paper["contribution"], "facts": paper["facts"],
                    "questions": paper["units"][unit]["questions"],
                    "versions": {side: outputs[ident, condition]["text"]
                                 for side, condition in labels.items()}})
    for judge, cases in packets.items():
        if judge == "J02":
            cases.reverse()
        write_new(ROOT / "blind" / f"{judge}.json", {"reviewer_id": judge, "cases": cases})
    write_new(ROOT / "mapping.json", {f"{judge}/{ident}": labels
                                     for (judge, ident), labels in mapping.items()})


def analyze():
    outputs = generations()
    materials = read(ROOT / "materials.json")["papers"]
    mapping = read(ROOT / "mapping.json")
    metadata = {f'{paper["id"]}-{unit}': (paper, unit)
                for paper in materials for unit in UNITS}
    lengths, violations = [], []
    for (ident, condition), row in outputs.items():
        paper, unit = metadata[ident]
        original = count(paper["units"][unit]["draft"])
        words = count(row["text"])
        ceiling = min(original, 160 if unit == "abstract" else 130) if condition == "compression" else (160 if unit == "abstract" else 130)
        lengths.append({"id": ident, "condition": condition, "original_words": original,
                        "words": words, "delta_words": words - original, "ceiling": ceiling})
        if words > ceiling:
            violations.append(lengths[-1])
    votes = Counter()
    unit_votes = {unit: Counter() for unit in UNITS}
    recovered = Counter()
    concerns = []
    normalized = []
    for judge in ("J01", "J02"):
        review = read(ROOT / "raw" / f"{judge}.json")
        assert review["reviewer_id"] == judge
        assert len(review["cases"]) == len(metadata)
        assert {row["id"] for row in review["cases"]} == set(metadata)
        for row in review["cases"]:
            ident = row["id"]
            labels = mapping[f"{judge}/{ident}"]
            paper, unit = metadata[ident]
            assert len(row["comparisons"]) == 6
            seen = set()
            for comparison in row["comparisons"]:
                left, right = comparison["pair"]
                assert {left, right} <= set(labels) and left != right
                assert comparison["choice"] in (left, right, "tie")
                seen.add(frozenset((left, right)))
                if "compression" not in (labels[left], labels[right]):
                    continue
                other = next(c for c in (labels[left], labels[right]) if c != "compression")
                chosen = "tie" if comparison["choice"] == "tie" else labels[comparison["choice"]]
                outcome = "win" if chosen == "compression" else "tie" if chosen == "tie" else "loss"
                votes[other, outcome] += 1
                unit_votes[unit][other, outcome] += 1
                normalized.append({"reviewer": judge, "id": ident, "control": other,
                                   "outcome": outcome, "reason": comparison["reason"]})
            assert len(seen) == 6
            assert set(row["versions"]) == set(labels)
            for side, assessment in row["versions"].items():
                condition = labels[side]
                prose = outputs[ident, condition]["text"]
                assert len(assessment["answers"]) == 2
                assert {a["question_id"] for a in assessment["answers"]} == {"Q1", "Q2"}
                for answer in assessment["answers"]:
                    assert answer["status"] in ("recovered", "partial", "missing", "contradicted")
                    assert answer["witness"] == "" or answer["witness"] in prose
                    assert answer["status"] not in ("recovered", "partial") or answer["witness"]
                    recovered[condition, answer["status"]] += 1
                assert assessment["fidelity"] in ("pass", "concern")
                assert type(assessment["consequential"]) is bool
                assert isinstance(assessment["issues"], list)
                if assessment["fidelity"] == "pass":
                    assert not assessment["issues"] and not assessment["consequential"]
                if assessment["fidelity"] == "concern":
                    assert assessment["issues"]
                    for issue in assessment["issues"]:
                        assert issue["witness"] in prose and issue["witness"]
                        assert issue["fact_ids"] and set(issue["fact_ids"]) <= {f["id"] for f in paper["facts"]}
                    concerns.append({"reviewer": judge, "id": ident, "condition": condition,
                                     "consequential": assessment["consequential"],
                                     "issues": assessment["issues"]})
    gate = (all(votes[control, "win"] > votes[control, "loss"] for control in ("prior", "editorial"))
            and all(unit_votes["abstract"][control, "win"] > unit_votes["abstract"][control, "loss"]
                    for control in ("prior", "editorial"))
            and votes["initial", "win"] >= votes["initial", "loss"]
            and unit_votes["abstract"]["initial", "win"] >= unit_votes["abstract"]["initial", "loss"]
            and not any(r["condition"] == "compression" for r in violations)
            and not any(c["condition"] == "compression" and c["consequential"] for c in concerns)
            and all(recovered["compression", "recovered"] >= recovered[c, "recovered"]
                    for c in ("prior", "editorial")))
    return {"papers": 6, "units": 12, "passages": 36, "judged_versions_including_initial": 48, "reviewers": 2,
            "votes": {c: {s: votes[c, s] for s in ("win", "loss", "tie")}
                      for c in CONTROLS},
            "unit_votes": {u: {c: {s: unit_votes[u][c, s] for s in ("win", "loss", "tie")}
                                 for c in CONTROLS} for u in UNITS},
            "recovery": {c: {s: recovered[c, s] for s in ("recovered", "partial", "missing", "contradicted")}
                         for c in (*CONDITIONS, "initial")},
            "mean_words": {u: {c: sum(r["words"] for r in lengths if r["condition"] == c and metadata[r["id"]][1] == u) / 6
                               for c in (*CONDITIONS, "initial")} for u in UNITS},
            "lengths": lengths,
            "budget_violations": violations, "fidelity_concerns": concerns,
            "normalized_preferences": normalized, "gate_pass": gate}


def render(summary):
    outputs = generations()
    papers = read(ROOT / "materials.json")["papers"]
    articles = []
    for paper in papers:
        for unit in UNITS:
            ident = f'{paper["id"]}-{unit}'
            columns = []
            for condition, label in (("initial", "Initial draft"), ("prior", "Previous guidance"),
                                     ("compression", "Compression first"), ("editorial", "Ordinary revision")):
                row = outputs[ident, condition]
                columns.append(f'<section><h3>{label} <small>{count(row["text"])} words</small></h3>'
                               f'<p class="prose">{html.escape(row["text"])}</p></section>')
            reasons = [r for r in summary["normalized_preferences"] if r["id"] == ident]
            reason_html = ''.join(f'<p>{html.escape(r["reviewer"] + " vs " + r["control"] + ": " + r["outcome"] + ". " + r["reason"])}</p>' for r in reasons)
            articles.append(f'<article id="{ident}" data-unit="{unit}" data-paper="{paper["id"]}"><h2>{html.escape(paper["name"])} / {unit}</h2>'
                            f'<a href="{html.escape(paper["source"])}">Primary paper</a>'
                            f'<div class="columns">{"".join(columns)}</div>'
                            f'<details><summary>Shared initial draft and reviewer reasons</summary>'
                            f'<p>{html.escape(paper["units"][unit]["draft"])}</p>{reason_html}</details></article>')
    compact = html.escape(json.dumps({k: summary[k] for k in ("votes", "unit_votes", "recovery", "gate_pass")}, indent=2))
    result_rows = ''.join(f'<tr><td>Compression vs {control}</td><td>{scores["win"]}</td>'
                          f'<td>{scores["loss"]}</td><td>{scores["tie"]}</td></tr>'
                          for control, scores in summary["votes"].items())
    paper_options = ''.join(f'<option value="{p["id"]}">{html.escape(p["name"])}</option>' for p in papers)
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Compression-first writing pilot</title><style>'
            'body{font:16px/1.65 system-ui;margin:0;color:#1c2525;background:#fff}main{max-width:1680px;margin:auto;padding:24px}'
            'h1{font-size:26px}h2{font-size:20px}h3{font-size:16px}small{font-weight:400;color:#586665}'
            '.columns{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}.prose{font-family:Georgia,serif}'
            'section{min-width:0}article{border-top:1px solid #cfd8d7;padding:20px 0;overflow-wrap:anywhere}'
            'pre{white-space:pre-wrap;font-size:13px}select{font:inherit;padding:6px}a{color:#18705e}'
            'table{border-collapse:collapse;margin:16px 0}th,td{text-align:left;padding:6px 18px 6px 0;border-bottom:1px solid #cfd8d7}'
            '@media(max-width:900px){.columns{grid-template-columns:1fr}main{padding:16px}}</style><main>'
            '<h1>Compression-first writing pilot</h1><p>6 RSS 2025 papers · 12 units · 36 revisions · 2 anonymous reviewers.</p>'
            '<p>Same initial drafts and body-grounded evidence. This measures a guidance bundle; effective length constraints differ.</p>'
            f'<p>Frozen pilot gate: {"PASS" if summary["gate_pass"] else "FAIL"}</p>'
            f'<table><thead><tr><th>Comparison</th><th>Wins</th><th>Losses</th><th>Ties</th></tr></thead><tbody>{result_rows}</tbody></table>'
            f'<details><summary>Recomputed results</summary><pre>{compact}</pre></details>'
            '<label>Section <select id="unit"><option value="all">All</option><option value="abstract">Abstract</option>'
            '<option value="results">Results</option></select></label> '
            f'<label>Paper <select id="paper"><option value="all">All</option>{paper_options}</select></label>' + ''.join(articles) +
            '</main><script>function filter(){const u=document.getElementById("unit").value,p=document.getElementById("paper").value;'
            'document.querySelectorAll("article").forEach(a=>a.hidden=(u!=="all"&&a.dataset.unit!==u)||(p!=="all"&&a.dataset.paper!==p))}'
            'document.getElementById("unit").onchange=filter;document.getElementById("paper").onchange=filter;</script></html>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "blind", "analyze", "check"))
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "blind":
        blind()
    elif args.command == "analyze":
        summary = analyze()
        write_new(ROOT / "summary.json", summary)
        with (ROOT / "comparison.html").open("x", encoding="utf-8") as stream:
            stream.write(render(summary))
        print(json.dumps({k: summary[k] for k in ("votes", "unit_votes", "recovery", "gate_pass")}, indent=2))
    else:
        assert read(ROOT / "summary.json") == analyze()
        assert (ROOT / "comparison.html").read_text(encoding="utf-8") == render(analyze())
        print("Frozen inputs, saved results and rendered passages reproduce exactly.")


if __name__ == "__main__":
    main()
