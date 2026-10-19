"""Freeze a small guide ablation and reproduce saved model judgments (no API calls)."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import itertools
import json
from pathlib import Path
import random
import re
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CONDITIONS = ("hard", "relaxed", "meaning")
LEGACY = "020e17862e00ac9d03afdd05fd3612348ffb46c3"
DIMENSIONS = ("overall", "explanation", "organization", "language")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def count(prose):
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", prose))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    papers = sum((read(ROOT / f"materials-{i}.json")["papers"] for i in (1, 2)), [])
    assert [p["paper_id"] for p in papers] == [f"N{i:02}" for i in range(1, 5)]
    for paper in papers:
        evidence = {row["id"] for row in paper["evidence"]}
        assert len(evidence) == len(paper["evidence"])
        assert 90 <= count(paper["initial_draft"]) <= 110
        assert len(paper["questions"]) == len(paper["relations"]) == 2
        for row in paper["questions"] + paper["relations"]:
            assert row["evidence_ids"] and set(row["evidence_ids"]) <= evidence
        for row in paper["relations"]:
            assert not row["original_witness"] or row["original_witness"] in paper["initial_draft"]
    new(ROOT / "materials.json", {"papers": papers})
    guide_path = "references/compression-first-writing.md"
    legacy = subprocess.check_output(["git", "show", f"{LEGACY}:{guide_path}"], cwd=REPO, text=True)
    new(ROOT / "guides.json", {"legacy_commit": LEGACY, "legacy": legacy,
                              "meaning": (REPO / guide_path).read_text(encoding="utf-8"),
                              "common": (REPO / "references/abstract-decisions.md").read_text(encoding="utf-8")})
    guides = read(ROOT / "guides.json")
    for block, indices in ((1, (0, 2)), (2, (1, 3))):
        for condition in CONDITIONS:
            ident = f"{condition}-{block}"
            cases = [{key: papers[i][key] for key in
                      ("paper_id", "title", "contribution", "evidence", "initial_draft", "relations")}
                     for i in indices]
            for case in cases:
                case["max_words"] = min(150, count(case["initial_draft"])) if condition == "hard" else 150
            instruction = (
                "Revise each initial draft once into an effective academic abstract using only its evidence. "
                "Preserve technical referents, consequential scope and author contribution priorities. "
                "Apply the attached editorial guidance. Do not pad to a minimum or use every fact. "
                "The budget below is author-authorized for this experiment and overrides any generic "
                "instruction in a guide to seek permission for expansion. Return your actual first "
                "result even if it misses a constraint; no retries. Return JSON {writer_id,cases}: "
                "each case has {id,text,note}, id is paper_id; note <=40 words stays outside prose. "
                "No file reads beyond this packet, web searches or agents. "
            )
            instruction += ("Do not exceed the initial draft's word count or 150 words. " if condition == "hard"
                            else "Growth beyond the initial draft is explicitly permitted up to 150 words. ")
            new(ROOT / "prompts" / f"{ident}.json", {
                "writer_id": ident, "instruction": instruction, "cases": cases,
                "count_rule": "ASCII alphanumerics, with one internal hyphen/apostrophe, count as one token; [A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?",
                "guides": [guides["common"], guides["meaning" if condition == "meaning" else "legacy"]]})
    paths = ["PROTOCOL.md", "pilot.py", "materials-1.json", "materials-2.json", "materials.json", "guides.json"]
    paths += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "prompts").glob("*.json"))]
    new(ROOT / "freeze.json", {"date": "2026-10-19", "seed": 20261019,
                               "inputs": {name: sha(ROOT / name) for name in paths}})


def verify_freeze():
    for name, expected in read(ROOT / "freeze.json")["inputs"].items():
        if sha(ROOT / name) != expected:
            raise ValueError(f"Frozen input changed: {name}")


def revisions():
    verify_freeze()
    outputs = {}
    for block in (1, 2):
        for condition in CONDITIONS:
            ident = f"{condition}-{block}"
            prompt = read(ROOT / "prompts" / f"{ident}.json")
            response = read(ROOT / "raw" / f"{ident}.json")
            assert response["writer_id"] == ident
            expected = {p["paper_id"] for p in prompt["cases"]}
            assert {c["id"] for c in response["cases"]} == expected
            assert len(response["cases"]) == len(expected)
            for case in response["cases"]:
                assert set(case) == {"id", "text", "note"} and case["text"].strip()
                outputs[(case["id"], condition)] = case
    return outputs


def blind():
    outputs = revisions()
    papers = read(ROOT / "materials.json")["papers"]
    rng = random.Random(20261019)
    mapping = {}
    for judge in ("J01", "J02"):
        cases = []
        for paper in (papers if judge == "J01" else papers[::-1]):
            ident = paper["paper_id"]
            if judge == "J01":
                order = list(CONDITIONS)
                rng.shuffle(order)
            else:
                order = list(mapping["J01"][ident].values())[::-1]
            mapped = dict(zip("ABC", order))
            mapping.setdefault(judge, {})[ident] = mapped
            cases.append({"id": ident, "versions": {label: outputs[(ident, condition)]["text"]
                                                      for label, condition in mapped.items()}})
        new(ROOT / "blind" / f"{judge}.json", {
            "reviewer_id": judge,
            "instruction": "Compare the three anonymous academic abstracts for each paper using prose alone. Do not infer source correctness from fluency. No evidence, original abstract or condition identities are supplied. For each unordered pair A/B, A/C, B/C, judge overall effectiveness, explanation, organization and language as left/right/tie, with one located decisive reason. Do not reward length or checklist completeness. Return JSON {reviewer_id,cases:[{id,pairs:[{left,right,overall,explanation,organization,language,reason}]}]}. No searches, other file reads, agents or editing.",
            "cases": cases})
    reader_cases = []
    for index, ((ident, condition), output) in enumerate(outputs.items()):
        rid = f"T{index + 1:02}"
        paper = next(p for p in papers if p["paper_id"] == ident)
        mapping.setdefault("reader", {})[rid] = {"paper": ident, "condition": condition}
        reader_cases.append({"id": rid, "text": output["text"], "questions": [
            {"id": q["id"], "question": q["question"]} for q in paper["questions"]]})
    for ident, text in (("K01", "PatchMap uses a cache and an updater for indoor navigation. Mean map-update time falls from 28 to 12 ms."),
                        ("K02", "PatchMap keeps unchanged cells and updates only cells touched by new observations, instead of rebuilding the entire map.")):
        mapping["reader"][ident] = {"paper": "synthetic", "condition": ident}
        reader_cases.append({"id": ident, "text": text,
                             "questions": [{"id": "Q1", "question": "Which map cells are recomputed and what work is avoided?"}]})
    rng.shuffle(reader_cases)
    new(ROOT / "blind" / "R01.json", {
        "reader_id": "R01", "instruction": "Answer each question from that case's prose alone, not other cases or your background knowledge. If the relation is not stated or necessarily entailed, answer 'not specified' with empty witness. Return JSON {reader_id,cases:[{id,answers:[{id,answer,witness}]}]}; each answer <=35 words, witness an exact prose span. No source searches, other file reads or agents.",
        "cases": reader_cases})
    new(ROOT / "blind" / "mapping.json", mapping)
    new(ROOT / "blind-freeze.json", {str(p.relative_to(ROOT)): sha(p)
                                      for p in sorted((ROOT / "blind").glob("*.json"))})


def audit_packet():
    outputs = revisions()
    mapping = read(ROOT / "blind" / "mapping.json")["reader"]
    reader = read(ROOT / "raw" / "R01.json")
    papers = {p["paper_id"]: p for p in read(ROOT / "materials.json")["papers"]}
    cases = []
    for row in read(ROOT / "blind" / "R01.json")["cases"]:
        ident = row["id"]
        source = mapping[ident]
        if source["paper"] == "synthetic":
            facts = [{"id": "E1", "statement": "PatchMap preserves unchanged cells and updates newly observed cells rather than rebuilding the map; reported map-update time is 28 versus 12 ms.", "location": "Authored control, not a real study"}]
            questions = [{"id": "Q1", "answer": "Only newly observed cells are updated, avoiding full map rebuilding."}]
        else:
            paper = papers[source["paper"]]
            facts, questions = paper["evidence"], paper["questions"]
        cases.append({"id": ident, "text": row["text"], "evidence": facts,
                      "questions": questions,
                      "reader_answers": next(c["answers"] for c in reader["cases"] if c["id"] == ident)})
    new(ROOT / "blind" / "A01.json", {"auditor_id": "A01", "instruction":
        "Audit actual reader answers against BOTH the supplied prose and source evidence. supported means the required relationship is recoverable from prose and the answer faithful to evidence. missing means the needed relation is absent even if the reader correctly says not specified. reader_added means the reader supplied source-correct specificity not stated/necessarily entailed by prose. contradicted means the text/answer conflicts with evidence. Do not credit a source-aware guess. For each answer return id,status (supported/missing/contradicted/reader_added),reason,witness (exact prose span, empty allowed). Separately flag consequential factual errors in each prose, not missing optional details. Return JSON {auditor_id,cases:[{id,answers:[...],factual_errors:[{claim,evidence_ids,reason}]}]}. No condition identities/preferences supplied; no other files, searches or agents.",
        "cases": cases})
    new(ROOT / "audit-freeze.json", {"blind/A01.json": sha(ROOT / "blind/A01.json")})


def analyze():
    outputs = revisions()
    papers = {p["paper_id"]: p for p in read(ROOT / "materials.json")["papers"]}
    mapping = read(ROOT / "blind/mapping.json")
    rows, comparisons = [], {c: {d: Counter() for d in DIMENSIONS} for c in ("hard", "relaxed")}
    for judge in ("J01", "J02"):
        result = read(ROOT / "raw" / f"{judge}.json")
        assert result["reviewer_id"] == judge
        assert len(result["cases"]) == 4 and {c["id"] for c in result["cases"]} == set(papers)
        for case in result["cases"]:
            assert {tuple(sorted((p["left"], p["right"]))) for p in case["pairs"]} == set(itertools.combinations("ABC", 2))
            assert len(case["pairs"]) == 3
            for pair in case["pairs"]:
                left, right = (mapping[judge][case["id"]][pair[k]] for k in ("left", "right"))
                row = {"reviewer": judge, "paper": case["id"], "left": left, "right": right, "reason": pair["reason"]}
                for dimension in DIMENSIONS:
                    assert pair[dimension] in ("left", "right", "tie")
                    winner = pair[dimension] if pair[dimension] == "tie" else (left if pair[dimension] == "left" else right)
                    row[dimension] = winner
                    if "meaning" in (left, right):
                        control = right if left == "meaning" else left
                        comparisons[control][dimension]["tie" if winner == "tie" else "win" if winner == "meaning" else "loss"] += 1
                rows.append(row)
    reader_cases = {c["id"]: c for c in read(ROOT / "blind/R01.json")["cases"]}
    reader = read(ROOT / "raw/R01.json")
    assert reader["reader_id"] == "R01" and len(reader["cases"]) == len(reader_cases)
    assert {c["id"] for c in reader["cases"]} == set(reader_cases)
    audit = read(ROOT / "raw/A01.json")
    assert audit["auditor_id"] == "A01" and len(audit["cases"]) == len(reader_cases)
    assert {c["id"] for c in audit["cases"]} == set(reader_cases)
    recovery, errors, calibration, deviations = {c: Counter() for c in CONDITIONS}, [], {}, []
    for case in audit["cases"]:
        ident = case["id"]
        expected_ids = {q["id"] for q in reader_cases[ident]["questions"]}
        answers = next(c["answers"] for c in reader["cases"] if c["id"] == ident)
        assert {a["id"] for a in answers} == expected_ids and len(answers) == len(expected_ids)
        assert {a["id"] for a in case["answers"]} == expected_ids and len(case["answers"]) == len(expected_ids)
        condition = mapping["reader"][ident]["condition"]
        for answer in answers:
            assert not answer["witness"] or answer["witness"] in reader_cases[ident]["text"]
            if count(answer["answer"]) > 35:
                deviations.append(f"{ident}/{answer['id']}: reader answer >35 words")
        for answer in case["answers"]:
            assert answer["status"] in ("supported", "missing", "contradicted", "reader_added")
            assert answer["reason"].strip()
            assert not answer["witness"] or answer["witness"] in reader_cases[ident]["text"]
            if condition in CONDITIONS:
                recovery[condition][answer["status"]] += 1
            else:
                calibration[ident] = answer["status"]
        if case["factual_errors"]:
            errors.append({"case": ident, "condition": condition, "errors": case["factual_errors"]})
    words = []
    for (ident, condition), output in outputs.items():
        limit = min(150, count(papers[ident]["initial_draft"])) if condition == "hard" else 150
        words.append({"paper": ident, "condition": condition, "words": count(output["text"]), "max_words": limit,
                      "compliant": count(output["text"]) <= limit})
        if count(output["note"]) > 40:
            deviations.append(f"{ident}/{condition}: writer note >40 words")
    overall = comparisons["relaxed"]["overall"]
    gate = {"preference": overall["win"] >= 6 and overall["loss"] <= 2,
            "recovery": recovery["meaning"]["supported"] >= 7 and recovery["meaning"]["supported"] >= recovery["relaxed"]["supported"] + 2,
            "calibration": calibration == {"K01": "missing", "K02": "supported"},
            "budget": all(w["compliant"] for w in words if w["condition"] == "meaning"),
            "fidelity": not any(e["condition"] == "meaning" for e in errors)}
    return {"gate": {**gate, "passed": all(gate.values())}, "comparisons": comparisons,
            "recovery": recovery, "calibration": calibration, "factual_errors": errors,
            "words": words, "pairs": rows, "auxiliary_deviations": deviations}


def render():
    outputs = revisions()
    sections = []
    for paper in read(ROOT / "materials.json")["papers"]:
        columns = [("Initial draft", paper["initial_draft"])] + [(c, outputs[(paper["paper_id"], c)]["text"]) for c in CONDITIONS]
        sections.append("<section><h2>" + html.escape(paper["title"]) + "</h2><div class='columns'>" +
                        "".join(f"<article><h3>{html.escape(label)} <small>{count(text)} words</small></h3><p>{html.escape(text)}</p></article>" for label, text in columns) + "</div></section>")
    return """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Explanation pilot comparison</title><style>
*{box-sizing:border-box}body{margin:0;color:#24262b;background:#fff;font:16px/1.65 system-ui,sans-serif}header{padding:24px 28px;border-bottom:1px solid #b9bec3;background:#eef4f0}h1{font-size:26px;margin:0}header p{margin:6px 0}a{color:#176746}section{padding:24px 28px;border-bottom:1px solid #b9bec3}h2{font-size:20px;line-height:1.4;margin:0 0 18px}.columns{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}article{min-width:0;border-top:3px solid #267654}article:first-child{border-color:#697078}h3{font-size:16px;margin:10px 0 12px}small{display:block;color:#616972;font-size:13px;font-weight:400}p{overflow-wrap:anywhere;margin:0} @media(max-width:1100px){.columns{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){header,section{padding:18px}.columns{grid-template-columns:minmax(0,1fr);gap:24px}h1{font-size:23px}}
</style><header><h1>Explanation-preserving compression</h1><p>Four-paper guide ablation · generated revisions, not author abstracts</p><p><a href="README.md">Methods, outcomes and limits</a></p></header><main>""" + "".join(sections) + "</main></html>\n"


def check():
    verify_freeze()
    for filename in ("blind-freeze.json", "audit-freeze.json", "receipts.json"):
        for name, expected in read(ROOT / filename).items():
            assert sha(ROOT / name) == expected, f"Archived artifact changed: {name}"
    for path in (ROOT / "responses").glob("*.json"):
        response = read(path)
        assert json.loads(response["completion"]) == read(ROOT / "raw" / path.name)
    assert analyze() == read(ROOT / "summary.json")
    assert render() == (ROOT / "comparison.html").read_text(encoding="utf-8")
    return {"status": "pass", "scope": "Archive integrity and recomputation, not semantic certification"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "blind", "audit", "analyze", "check", "seal"))
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "blind":
        blind()
    elif args.command == "audit":
        audit_packet()
    elif args.command == "analyze":
        new(ROOT / "summary.json", analyze())
        with (ROOT / "comparison.html").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(render())
    elif args.command == "seal":
        new(ROOT / "receipts.json", {str(p.relative_to(ROOT)): sha(p) for p in sorted(ROOT.rglob("*"))
                                     if p.is_file() and p.name != "receipts.json" and "__pycache__" not in p.parts})
    else:
        print(json.dumps(check(), indent=2))
