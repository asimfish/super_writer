"""Reproduce blinding, witnessed recovery checks and public pilot artifacts."""

import argparse
from collections import Counter
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("pilot_harness", ROOT / "pilot.py")
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)
RECOVERY = {"recovered", "partial", "missing", "contradicted", "reader_added", "source_uncertain"}


def read(path):
    return pilot._load_json(path)


def write_new(path, value):
    pilot.require_new_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def verify_freeze(root=ROOT):
    freeze = read(root / "freeze.json")
    for name, receipt in freeze["inputs"].items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != receipt["sha256"]:
            raise ValueError(f"Frozen input changed: {name}")
    return freeze


def artifact_receipts(root=ROOT):
    names = ["freeze.json", "execution.json", "materials.json", "questions.json",
             "questions.private.json", "mapping.json", "summary.json", "word_counts.json",
             "normalized_reviews.json", "comparison.html"]
    names.extend(str(p.relative_to(root)).replace("\\", "/") for folder in
                 ("guides", "prompts", "responses", "raw", "blind")
                 for p in sorted((root / folder).iterdir()) if p.is_file())
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in sorted(names)}


def blind_data(root=ROOT):
    freeze = verify_freeze(root)
    writers = {}
    for entry in freeze["writers"]:
        data = read(root / "raw" / f'{entry["id"]}_final.json')
        pilot.validate_writer(data)
        if data["writer_id"] != entry["id"] or data["replicate"] != entry["replicate"]:
            raise ValueError("Writer identity differs from freeze")
        for case in data["cases"]:
            writers[case["id"], entry["replicate"], entry["condition"]] = case
    rng = random.Random(freeze["seed"])
    pairs, mapping = [], {}
    for identifier, meta in sorted(pilot.PAIR_META.items()):
        sides = ["baseline", "candidate"]
        if rng.choice([False, True]):
            sides.reverse()
        mapping[identifier] = dict(zip(("A", "B"), sides))
        pairs.append({"id": identifier, **meta, **{
            side: writers[meta["paper"], meta["sample"], condition][meta["unit"]]
            for side, condition in mapping[identifier].items()}})
    canonical = {"pairs": pairs}
    reversed_packet = {"pairs": [{**p, "A": p["B"], "B": p["A"]} for p in reversed(pairs)]}
    return canonical, reversed_packet, mapping


def question_keys(packet, questions):
    return {(p["id"], side, q["id"]) for p in packet["pairs"]
            for side in ("A", "B") for q in questions["questions"][p["paper"]][p["unit"]]}


def complete(rows, expected, fields, label):
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError(f"{label}: expected object list")
    try:
        keys = [tuple(row[field] for field in fields) for row in rows]
        if len(set(keys)) != len(keys) or set(keys) != expected:
            raise ValueError(f"{label}: duplicate, missing or unexpected identities")
    except (KeyError, TypeError) as exc:
        raise ValueError(f"{label}: malformed identity") from exc


def validate_reader(data, packet, questions):
    if data.get("reader_id") not in ("T01", "T02"):
        raise ValueError("Unexpected reader ID")
    rows = data.get("answers")
    complete(rows, question_keys(packet, questions), ("id", "side", "question_id"), "reader")
    passages = {(p["id"], s): p[s] for p in packet["pairs"] for s in ("A", "B")}
    witness_checks = []
    for row in rows:
        if row.get("status") not in ("recoverable", "partial", "unrecoverable"):
            raise ValueError("Invalid reader status")
        if not isinstance(row.get("answer"), str) or not row["answer"].strip():
            raise ValueError("Missing reader answer")
        witnesses = row.get("witnesses")
        if not isinstance(witnesses, list) or len(witnesses) > 3 or any(
                not isinstance(w, str) or not w.strip() for w in witnesses):
            raise ValueError("Invalid reader witness list")
        witness_checks.append({"reader_id": data["reader_id"], **{k: row[k] for k in
                               ("id", "side", "question_id")},
                               "exact": all(w in passages[row["id"], row["side"]] for w in witnesses),
                               "empty": not witnesses, "answer_words": pilot.count_words(row["answer"])})
    return witness_checks


def validate_audit(data, packet, questions, readers, materials):
    if data.get("auditor_id") != "F01":
        raise ValueError("Unexpected auditor ID")
    expected_passages = {(p["id"], s) for p in packet["pairs"] for s in ("A", "B")}
    complete(data.get("passages"), expected_passages, ("id", "side"), "audit passages")
    expected_recovery = {(r, *k) for r in ("T01", "T02") for k in question_keys(packet, questions)}
    complete(data.get("recovery"), expected_recovery,
             ("reader_id", "id", "side", "question_id"), "audit recovery")
    prose = {(p["id"], s): p[s] for p in packet["pairs"] for s in ("A", "B")}
    facts = {p["id"]: {f["id"] for f in p["facts"]} for p in materials["papers"]}
    paper_for = {p["id"]: p["paper"] for p in packet["pairs"]}
    witness_checks = {tuple(row[k] for k in ("reader_id", "id", "side", "question_id")): row
                      for reader in readers for row in validate_reader(reader, packet, questions)}
    audit_disagreements = []
    for row in data["passages"]:
        if row.get("status") not in ("pass", "concern", "source_uncertain") or type(row.get("consequential")) is not bool:
            raise ValueError("Invalid passage audit state")
        issues = row.get("issues")
        if not isinstance(issues, list) or (row["status"] == "pass" and (issues or row["consequential"])):
            raise ValueError("Inconsistent passage audit issues")
        if row["status"] == "concern" and not issues:
            raise ValueError("Concern without located issue")
        for issue in issues:
            if not isinstance(issue.get("witness"), str) or not issue["witness"] or issue["witness"] not in prose[row["id"], row["side"]]:
                raise ValueError("Audit issue witness is not an exact passage substring")
            if not isinstance(issue.get("fact_ids"), list) or not issue["fact_ids"] or not set(issue["fact_ids"]) <= facts[paper_for[row["id"]]]:
                raise ValueError("Audit issue has invalid fact anchor")
            if not isinstance(issue.get("reason"), str) or not issue["reason"].strip():
                raise ValueError("Audit issue lacks reason")
    for row in data["recovery"]:
        if row.get("status") not in RECOVERY or type(row.get("witness_supported")) is not bool:
            raise ValueError("Invalid audited recovery state")
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            raise ValueError("Recovery audit lacks reason")
        key = tuple(row[k] for k in ("reader_id", "id", "side", "question_id"))
        if row["witness_supported"] and not witness_checks[key]["exact"]:
            audit_disagreements.append({"reader_id": key[0], "id": key[1], "side": key[2],
                                        "question_id": key[3], "problem": "Auditor accepted a nonexact reader witness"})
    return audit_disagreements


def normalize_review(data):
    if data["reviewer_id"] != "J02":
        return data
    return {**data, "pairs": [{**row, "A": row["B"], "B": row["A"],
                               "preferred": {"A": "B", "B": "A", "tie": "tie"}[row["preferred"]]}
                              for row in data["pairs"]]}


def analyze(root=ROOT):
    packet, reverse, mapping = blind_data(root)
    for name, expected in (("reader.json", packet), ("J01.json", packet), ("J02.json", reverse)):
        if read(root / "blind" / name) != expected:
            raise ValueError(f"Anonymous packet differs from frozen mapping: {name}")
    if read(root / "mapping.json") != mapping:
        raise ValueError("Mapping differs from deterministic frozen seed")
    meta = pilot.validate_pairs(packet)
    reviews = []
    for rid in ("J01", "J02"):
        review = read(root / "raw" / f"{rid}.json")
        if review["reviewer_id"] != rid:
            raise ValueError("Reviewer file/identity mismatch")
        pilot.validate_review(review)
        reviews.append(normalize_review(review))
    readers = [read(root / "raw" / f"{rid}.json") for rid in ("T01", "T02")]
    if [r["reader_id"] for r in readers] != ["T01", "T02"]:
        raise ValueError("Reader file/identity mismatch")
    questions = read(root / "questions.private.json")
    checks = [c for reader in readers for c in validate_reader(reader, packet, questions)]
    audit = read(root / "raw" / "F01.json")
    disagreements = validate_audit(audit, packet, questions, readers, read(root / "materials.json"))
    failures = [row for row in audit["passages"] if row["consequential"] and mapping[row["id"]][row["side"]] == "candidate"]
    diagnostics = []
    for entry in read(root / "freeze.json")["writers"]:
        for phase in ("initial", "final"):
            data = read(root / "raw" / f'{entry["id"]}_{phase}.json')
            response = read(root / "responses" / f'{entry["id"]}_{phase}.json')
            if json.loads(response["completion"]) != data:
                raise ValueError("Decoded writer differs from original completion")
            if data["writer_id"] != entry["id"] or data["replicate"] != entry["replicate"]:
                raise ValueError("Initial/final writer identity differs from freeze")
            diagnostics.append({"condition": entry["condition"], **pilot.validate_writer(data, phase)})
    for rid in ("J01", "J02", "T01", "T02", "F01"):
        if json.loads(read(root / "responses" / f"{rid}.json")["completion"]) != read(root / "raw" / f"{rid}.json"):
            raise ValueError("Decoded assessment differs from original completion")
    violations = [v for d in diagnostics for v in d["budget_violations"]]
    summary = pilot.summarize(reviews, mapping, meta, violations, failures)
    summary["ordinal_scores"] = {}
    for unit in ("all", *pilot.UNITS):
        summary["ordinal_scores"][unit] = {}
        for condition in pilot.CONDITIONS:
            scores = [row[side] for review in reviews for row in review["pairs"]
                      for side in ("A", "B") if mapping[row["id"]][side] == condition
                      and (unit == "all" or meta[row["id"]]["unit"] == unit)]
            summary["ordinal_scores"][unit][condition] = {
                dimension: {"n": len(scores), "mean": sum(s[dimension] for s in scores) / len(scores)}
                for dimension in pilot.DIMENSIONS}
    summary["recovery"] = {}
    for condition in pilot.CONDITIONS:
        rows = [r for r in audit["recovery"] if mapping[r["id"]][r["side"]] == condition]
        summary["recovery"][condition] = {"all": dict(Counter(r["status"] for r in rows)),
            "by_unit": {u: dict(Counter(r["status"] for r in rows if meta[r["id"]]["unit"] == u)) for u in pilot.UNITS}}
    summary["passage_fidelity"] = {c: dict(Counter(r["status"] for r in audit["passages"]
        if mapping[r["id"]][r["side"]] == c)) for c in pilot.CONDITIONS}
    summary["witness_checks"] = {"records": len(checks), "nonexact": [c for c in checks if not c["exact"]],
                                 "audit_disagreements": disagreements,
                                 "reader_answer_over_budget": [c for c in checks if c["answer_words"] > 45]}
    summary["scope"] = "Two development papers; inherited-model packet-grounded pilot; correlated judgments, no runtime promotion or author-abstract superiority claim."
    return summary, diagnostics, reviews


def render(root=ROOT):
    summary, diagnostics, reviews = analyze(root)
    packet = read(root / "blind" / "reader.json")
    mapping = read(root / "mapping.json")
    audit = read(root / "raw" / "F01.json")
    readers = [read(root / "raw" / f"{r}.json") for r in ("T01", "T02")]
    questions = read(root / "questions.json")["questions"]
    esc = lambda value: html.escape(str(value), quote=True)
    articles = []
    for p in packet["pairs"]:
        cols = []
        for condition in pilot.CONDITIONS:
            side = next(s for s in ("A", "B") if mapping[p["id"]][s] == condition)
            fidelity = next(a for a in audit["passages"] if a["id"] == p["id"] and a["side"] == side)
            recoveries = [r for r in audit["recovery"] if r["id"] == p["id"] and r["side"] == side]
            initial = next(d for d in diagnostics if d["condition"] == condition and d["replicate"] == p["sample"] and d["phase"] == "initial")
            original = next(c for c in read(root / "raw" / f'{initial["writer_id"]}_initial.json')["cases"] if c["id"] == p["paper"])[p["unit"]]
            detail = ""
            for r in recoveries:
                answer = next(a for reader in readers if reader["reader_id"] == r["reader_id"]
                              for a in reader["answers"] if all(a[k] == r[k] for k in ("id", "side", "question_id")))
                question = next(q["question"] for q in questions[p["paper"]][p["unit"]] if q["id"] == r["question_id"])
                witnesses = "".join(f'<p><b>Witness:</b> {esc(w)}</p>' for w in answer["witnesses"])
                detail += f'<p><b>{esc(r["reader_id"])} / {esc(r["question_id"])}:</b> {esc(question)}</p><p>{esc(answer["answer"])}</p>{witnesses}<p><b>Audited answer: {esc(r["status"])}</b>. {esc(r["reason"])}</p>'
            detail += "".join(f'<p><b>Fidelity issue:</b> {esc(i["witness"])}. {esc(i["reason"])}</p>' for i in fidelity["issues"])
            cols.append(f'<section><h3>{condition.title()}</h3><p class="muted">{pilot.count_words(p[side])} words / fidelity: {esc(fidelity["status"])}</p><p class="prose" data-side="{condition}">{esc(p[side])}</p><details><summary>Recovery and fidelity</summary>{detail}</details><details><summary>Initial draft</summary><p class="initial">{esc(original)}</p></details></section>')
        reasons = "".join(f'<p><b>{r["reviewer_id"]}: {esc("tie" if row["preferred"] == "tie" else mapping[p["id"]][row["preferred"]])}</b>. {esc(row["reason"])}</p>' for r in reviews for row in r["pairs"] if row["id"] == p["id"])
        outcome = summary["pairs"][p["id"]]["outcome"]
        articles.append(f'<article id="{p["id"]}" data-paper="{p["paper"]}" data-unit="{p["unit"]}" data-sample="{p["sample"]}"><h2>{p["paper"]} / {p["unit"].title()} / Sample {p["sample"]}</h2><p class="muted">Pair outcome: {esc(outcome)}</p><div class="columns">{"".join(cols)}</div><details><summary>Anonymous preferences (J02 reasons use reversed A/B labels)</summary>{reasons}</details></article>')
    counts = summary["overall"]["votes"]
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Super Writer: AI-spec pilot</title><style>
*{box-sizing:border-box}body{margin:0;background:white;color:#24262a;font:15px/1.55 system-ui,sans-serif;letter-spacing:0}header,main{max-width:1400px;margin:auto;padding:24px}header,article{border-bottom:1px solid #ced3d7}h1{font-size:26px;margin:0 0 10px}h2{font-size:20px;margin:0 0 14px}h3{font-size:17px;margin:0}p{margin:10px 0;overflow-wrap:anywhere}a{color:#176688}.muted{color:#59616a}.toolbar{display:flex;flex-wrap:wrap;gap:16px;margin-top:16px}label{display:flex;align-items:center;gap:8px}select{font:inherit;padding:6px;border:1px solid #aeb5bc;border-radius:4px;background:white;max-width:100%}article{padding:24px 0}.columns{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px}section{min-width:0}section:first-child h3{color:#9e3346}section:last-child h3{color:#24634b}.prose,.initial{font:18px/1.65 Georgia,serif;white-space:pre-wrap}details{margin-top:16px}summary{cursor:pointer}[hidden]{display:none!important}@media(max-width:760px){header,main{padding:18px}.columns{grid-template-columns:minmax(0,1fr);gap:24px}h1{font-size:24px}}
</style></head><body><header><h1>Super Writer: AI-spec pilot</h1>''' + f'<p>DROID + SIMPLER / 12 pairs / 24 final passages. Votes: candidate {counts["candidate"]}, baseline {counts["baseline"]}, tie {counts["tie"]}.</p><p class="muted">Same-model development pilot. No original-author abstract comparison or general quality claim.</p><p><a href="README.md">Evidence</a> / <a href="summary.json">Complete results</a> / <a href="materials.json">Located source facts</a></p>' + '''<div class="toolbar"><label>Paper<select id="paper"><option value="all">All</option><option>R01</option><option>R02</option></select></label><label>Unit<select id="unit"><option value="all">All</option><option value="abstract">Abstract</option><option value="methods">Methods</option><option value="results">Results</option></select></label><label>Sample<select id="sample"><option value="all">All</option><option>1</option><option>2</option></select></label></div></header><main>''' + "".join(articles) + '''</main><script>const filters=['paper','unit','sample'].map(id=>document.getElementById(id));function filter(){document.querySelectorAll('article').forEach(a=>a.hidden=filters.some(f=>f.value!=='all'&&f.value!==a.dataset[f.id]))}filters.forEach(f=>f.addEventListener('change',filter));</script></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("blind", "check", "analyze", "render", "receipts"))
    args = parser.parse_args()
    if args.action == "blind":
        packet, reverse, mapping = blind_data()
        for name, data in (("reader", packet), ("J01", packet), ("J02", reverse)):
            write_new(ROOT / "blind" / f"{name}.json", data)
        write_new(ROOT / "mapping.json", mapping)
    else:
        summary, diagnostics, reviews = analyze()
        if args.action == "analyze":
            for name, data in (("summary", summary), ("word_counts", diagnostics), ("normalized_reviews", reviews)):
                write_new(ROOT / f"{name}.json", data)
        elif args.action == "render":
            pilot.require_new_output(ROOT / "comparison.html")
            with (ROOT / "comparison.html").open("x", encoding="utf-8") as stream:
                stream.write(render())
        elif args.action == "receipts":
            write_new(ROOT / "receipts.json", artifact_receipts())
        else:
            if read(ROOT / "summary.json") != summary or read(ROOT / "word_counts.json") != diagnostics or read(ROOT / "normalized_reviews.json") != reviews:
                raise ValueError("Saved derived results differ from raw evidence")
            if (ROOT / "comparison.html").read_text(encoding="utf-8") != render():
                raise ValueError("Comparison differs from raw evidence")
            if read(ROOT / "receipts.json") != artifact_receipts():
                raise ValueError("Published experiment bytes differ from receipts")
            print("Frozen inputs, 13 completions, blinding, judgments, recovery and rendering verified.")


if __name__ == "__main__":
    main()
