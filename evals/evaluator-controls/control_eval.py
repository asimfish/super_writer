"""Prepare and analyze immutable synthetic evaluator controls, never model calls."""

import argparse
import collections
import hashlib
import json
import random
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUPPORT = {"supported", "missing", "contradicted", "uncertain"}
FIDELITY = {"pass", "concern", "fail"}
GENERIC = {
    "methods": ["How does computation proceed, and why does that operation permit the stated consequence?",
                "What conditions bound the main claim, and what remains unestablished?"],
    "results": ["What finding supports the conclusion, and against which comparator?",
                "What exactly was measured, and which conditions limit the inference?"],
    "abstract": ["What does the work establish, and what relation explains its contribution?",
                 "Which empirical or theoretical boundaries are explicit?"]}


def read(name):
    return json.loads((ROOT / name).read_text())


def write(name, value):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def words(text):
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def exact(rows, ids):
    if len(set(ids)) != len(ids) or len(rows) != len(ids) or {r["id"] for r in rows} != set(ids):
        raise ValueError("Incomplete or duplicate response IDs")
    return {r["id"]: r for r in rows}


def valid_score(value):
    return type(value) is int and 0 <= value <= 2


def prepare():
    cases = read("cases.json")["cases"]
    review = exact(read("fixture_review.final.json")["cases"], [c["id"] for c in cases])
    if len(cases) != 12 or any(review[c["id"]]["valid"] is not True for c in cases):
        raise ValueError("Fixture not independently validated")
    rng = random.Random(20261014)
    ordered = list(cases)
    rng.shuffle(ordered)
    maps, reviewers = [], {1: [], 2: []}
    for n, case in enumerate(ordered, 1):
        variants = ["v1", "v2"]
        rng.shuffle(variants)
        key = {"id": f"Q{n:02d}", "case": case["id"],
               "reviewer_1": dict(zip(("A", "B"), variants)),
               "reviewer_2": dict(zip(("A", "B"), variants[::-1]))}
        maps.append(key)
        for reviewer in (1, 2):
            reviewers[reviewer].append({"id": key["id"], "unit": case["unit"],
                "evidence": case["evidence"], **{label: case["variants"][variant]
                    for label, variant in key[f"reviewer_{reviewer}"].items()}})
    texts, readers = [], {i: [] for i in range(1, 5)}
    n = 0
    for group in range(2):
        for index, case in enumerate(ordered[group * 6:(group + 1) * 6]):
            first = "v1" if index % 2 == 0 else "v2"
            for offset, variant in enumerate((first, "v2" if first == "v1" else "v1")):
                n += 1
                reader = group * 2 + offset + 1
                key = {"id": f"T{n:03d}", "case": case["id"], "variant": variant, "reader": reader}
                texts.append(key)
                readers[reader].append({"id": key["id"], "unit": case["unit"],
                                       "questions": GENERIC[case["unit"]], "text": case["variants"][variant]})
    for reader in readers.values():
        rng.shuffle(reader)
    for number, rows in reviewers.items():
        write(f"packets/review_{number}.json", rows)
    for number, rows in readers.items():
        write(f"packets/reader_{number}.json", rows)
    write("mapping.json", {"pairs": maps, "texts": texts})
    tasks = []
    for number in (1, 2):
        tasks.append({"phase": "review", "number": number, "output": f"raw/review_{number}.json",
            "message": f"Independently review the anonymous prose pairs in {ROOT}/packets/review_{number}.json. "
            "Use only supplied fictional evidence, not actual scientific claims. No browsing, other files, history or agents. "
            "Assess stand-alone contribution/operation clarity and evidence calibration, not length or labels. "
            "Fidelity pass: supported claims; concern: consequential ambiguous/missing claim condition; fail: materially false attribution/event. "
            "A missing explanation can weaken writing without being false. Legitimate alternative phrasing or omitted nonessential detail is not automatically defective. "
            "Return exactly one response, no quality retry or raw repair, via apply_patch to "
            f"{ROOT}/raw/review_{number}.json with schema "
            '{"reviews":[{"id":"pair id","preferred":"A|B|Tie","fidelity":{"A":"pass|concern|fail","B":"pass|concern|fail"},'
            '"reason":"<=110 words with decisive evidence/text witnesses"}]}. Cover all 12 pairs. Final only path and operational problems.'})
    for number in range(1, 5):
        tasks.append({"phase": "reader", "number": number, "output": f"raw/reader_{number}.json",
            "message": f"Read only {ROOT}/packets/reader_{number}.json. Treat each paragraph as standalone fictional research prose. "
            "No browsing, source evidence, other files, history or agents. Answer the two questions using only what the paragraph states or necessarily entails. "
            "Do not use scientific familiarity to complete missing operations or conditions; explicitly say not recoverable when absent. "
            "Supply a literal text witness for each answer (<=18 words) or empty witness when absent. "
            "At most 140 words per text across answers, witnesses and unclear. Save exactly one untouched JSON response via apply_patch to "
            f"{ROOT}/raw/reader_{number}.json with schema "
            '{"readings":[{"id":"text id","core":"answer to question 1","scope":"answer to question 2",'
            '"core_witness":"literal substring or empty","scope_witness":"literal substring or empty","unclear":"specific missing relation or none"}]}. '
            'Cover all six texts. Final only path and operational problems.'})
    write("tasks.initial.json", tasks)
    frozen = ["cases.json", "PROTOCOL.md", "fixture_review.final.json", "control_eval.py", "tasks.initial.json", "mapping.json"]
    frozen.extend(str(p.relative_to(ROOT)) for p in sorted((ROOT / "packets").glob("*.json")))
    write("frozen_hashes.json", {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in frozen})


def prepare_audits():
    mapping = read("mapping.json")["texts"]
    cases = {c["id"]: c for c in read("cases.json")["cases"]}
    readings = {}
    for number in range(1, 5):
        readings.update(exact(read(f"raw/reader_{number}.json")["readings"],
                              [m["id"] for m in mapping if m["reader"] == number]))
    common = [{"id": m["id"], "unit": cases[m["case"]]["unit"],
               "evidence": cases[m["case"]]["evidence"],
               "text": cases[m["case"]]["variants"][m["variant"]], "reading": readings[m["id"]]}
              for m in mapping]
    tasks = []
    for phase in ("coarse", "fine"):
        packet = [{**row, **({"critical_question": cases[m["case"]]["question"]} if phase == "fine" else {})}
                  for row, m in zip(common, mapping, strict=True)]
        write(f"packets/{phase}.json", packet)
        for number in (1, 2):
            rubric = ("Score reader central-relation and consequential-scope recovery 0 absent/wrong, 1 partial, 2 recoverable, source-supported and text-supported. "
                      "Judge the paragraph's selected function, not a mandatory fact inventory. Do not credit remembered/missing facts as prose recovery. "
                      'Schema {"audits":[{"id":"text id","fidelity":"pass|concern|fail","core_recovery":0,"scope_recovery":0,"reason":"<=110 words, located evidence/prose/reading"}]}.'
                      if phase == "coarse" else
                      "For each critical question, classify the support IN THE PROSE as supported (explicit or necessarily entailed), missing (requires absent information), "
                      "contradicted (text answers it incompatibly with evidence), or uncertain (source/prose insufficient to decide). Source knowledge cannot fill prose gaps. "
                      "A correct source fact supplied by a reader is inferred rather than text-grounded when the prose lacks it. Legitimate omissions outside the requested relation are not errors. "
                      'Schema {"audits":[{"id":"text id","fidelity":"pass|concern|fail","critical_support":"supported|missing|contradicted|uncertain",'
                      '"reader_support":"text_grounded|inferred|wrong|unanswered|ambiguous","reason":"<=110 words, locate critical prose witness or absence and supporting evidence"}]}.' )
            tasks.append({"phase": phase, "number": number, "output": f"raw/{phase}_{number}.json",
                "message": f"Independently audit all 24 anonymous prose/reader entries in {ROOT}/packets/{phase}.json using only those fictional premises. "
                "No browsing, oracles, mappings, guides, other outputs, history or agents. Fidelity pass means supported claims; concern means consequential ambiguous scope/missing claim condition; "
                "fail means materially false event/attribution. Missing explanation is not automatically false science. " + rubric +
                f" Save exactly one untouched response via apply_patch to {ROOT}/raw/{phase}_{number}.json. No repair or quality retry. Final only path and operational problems."})
    write("tasks.audit.json", tasks)
    write("reader_hashes.json", {f"raw/reader_{n}.json": hashlib.sha256((ROOT / f"raw/reader_{n}.json").read_bytes()).hexdigest()
                                 for n in range(1, 5)})
    write("audit_input_hashes.json", {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                    for name in ("packets/coarse.json", "packets/fine.json", "tasks.audit.json")})


def analyze():
    files = [f"raw/{p}_{n}.json" for p, numbers in (("review", (1, 2)), ("reader", range(1, 5)),
                                                  ("coarse", (1, 2)), ("fine", (1, 2))) for n in numbers]
    missing = [p for p in files if not (ROOT / p).is_file()]
    if missing:
        raise ValueError(f"Incomplete assessment, no unblinding: {missing}")
    for name in ("frozen_hashes.json", "reader_hashes.json", "audit_input_hashes.json"):
        for file, expected in read(name).items():
            if hashlib.sha256((ROOT / file).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Frozen input/raw drift: {file}")
    mapping = read("mapping.json")
    cases = {c["id"]: c for c in read("cases.json")["cases"]}
    votes, audits, budgets, witnesses = [], [], [], []
    for n in (1, 2):
        rows = exact(read(f"raw/review_{n}.json")["reviews"], [m["id"] for m in mapping["pairs"]])
        for m in mapping["pairs"]:
            r = rows[m["id"]]
            if r["preferred"] not in ("A", "B", "Tie") or set(r["fidelity"]) != {"A", "B"} or not set(r["fidelity"].values()) <= FIDELITY:
                raise ValueError(f"Invalid preference: {r}")
            key = m[f"reviewer_{n}"]
            winner = "tie" if r["preferred"] == "Tie" else key[r["preferred"]]
            votes.append({"case": m["case"], "reviewer": n, "winner": winner,
                          "correct": winner in cases[m["case"]]["oracle"]["preferred"],
                          "fidelity": {key[k]: v for k, v in r["fidelity"].items()}, "reason": r["reason"]})
            budgets.append({"phase": "review", "id": m["id"], "replicate": n, "words": words(r["reason"]), "limit": 110})
    for n in range(1, 5):
        selected = [m for m in mapping["texts"] if m["reader"] == n]
        rows = exact(read(f"raw/reader_{n}.json")["readings"], [m["id"] for m in selected])
        for m in selected:
            r = rows[m["id"]]
            text = cases[m["case"]]["variants"][m["variant"]]
            for k in ("core", "scope", "core_witness", "scope_witness", "unclear"):
                if not isinstance(r[k], str):
                    raise ValueError(f"Invalid reading: {r}")
            budgets.append({"phase": "reader", "id": m["id"], "words": sum(words(r[k]) for k in
                           ("core", "scope", "core_witness", "scope_witness", "unclear")), "limit": 140})
            for k in ("core_witness", "scope_witness"):
                witnesses.append({"id": m["id"], "field": k, "literal_or_empty": not r[k] or r[k] in text,
                                  "within_budget": words(r[k]) <= 18})
    for phase in ("coarse", "fine"):
        for n in (1, 2):
            rows = exact(read(f"raw/{phase}_{n}.json")["audits"], [m["id"] for m in mapping["texts"]])
            for m in mapping["texts"]:
                r = rows[m["id"]]
                if r["fidelity"] not in FIDELITY:
                    raise ValueError(f"Invalid fidelity: {r}")
                if phase == "coarse" and any(not valid_score(r[k]) for k in ("core_recovery", "scope_recovery")):
                    raise ValueError(f"Invalid coarse score: {r}")
                if phase == "fine" and (r["critical_support"] not in SUPPORT or r["reader_support"] not in
                                        {"text_grounded", "inferred", "wrong", "unanswered", "ambiguous"}):
                    raise ValueError(f"Invalid fine status: {r}")
                case = cases[m["case"]]
                expected = case["oracle"]["support"][m["variant"]]
                target_score = "core_recovery" if case["category"] == "relation" else "scope_recovery"
                detected = r["critical_support"] in {"missing", "contradicted"} if phase == "fine" else r[target_score] < 2
                audits.append({**m, **r, "phase": phase, "auditor": n, "category": case["category"],
                               "expected_support": expected, "flagged": detected,
                               "fidelity_correct": r["fidelity"] in case["oracle"]["fidelity"][m["variant"]]})
                budgets.append({"phase": phase, "id": m["id"], "replicate": n, "words": words(r["reason"]), "limit": 110})
    criteria = []
    for category in ("relation", "metric", "condition"):
        ids = {c["id"] for c in cases.values() if c["category"] == category}
        correct = sum(v["correct"] for v in votes if v["case"] in ids)
        criteria.append({"name": f"preference_{category}", "observed": correct, "total": 6, "required_minimum": 5, "pass": correct >= 5})
        group = [a for a in audits if a["phase"] == "fine" and a["category"] == category]
        bad = [a for a in group if a["expected_support"] != "supported"]
        good = [a for a in group if a["expected_support"] == "supported"]
        for name, value, minimum in (("detect", sum(a["flagged"] for a in bad), 5),
                                     ("fidelity", sum(a["fidelity_correct"] for a in bad), 5)):
            criteria.append({"name": f"fine_{name}_{category}", "observed": value, "total": 6, "required_minimum": minimum, "pass": value >= minimum})
        false = sum(a["flagged"] for a in good)
        criteria.append({"name": f"fine_false_flags_{category}", "observed": false, "total": 6, "required_maximum": 1, "pass": false <= 1})
        correct_good = sum(a["fidelity_correct"] for a in good)
        criteria.append({"name": f"fine_faithful_fidelity_{category}", "observed": correct_good, "total": 6, "required_minimum": 5, "pass": correct_good >= 5})
    identical = {c["id"] for c in cases.values() if c["category"] == "neutral_identical"}
    ties = sum(v["winner"] == "tie" for v in votes if v["case"] in identical)
    criteria.append({"name": "identical_ties", "observed": ties, "total": 2, "required_minimum": 2, "pass": ties == 2})
    neutral = [a for a in audits if a["phase"] == "fine" and a["category"].startswith("neutral")]
    false = sum(a["flagged"] for a in neutral)
    criteria.append({"name": "fine_false_flags_neutral", "observed": false, "total": 12, "required_maximum": 1, "pass": false <= 1})
    correct_neutral = sum(a["fidelity_correct"] for a in neutral)
    criteria.append({"name": "fine_neutral_fidelity", "observed": correct_neutral, "total": 12, "required_minimum": 11, "pass": correct_neutral >= 11})
    summaries = {phase: {category: {
        "defective_flagged": sum(a["flagged"] for a in audits if a["phase"] == phase and a["category"] == category and a["expected_support"] != "supported"),
        "defective_total": sum(1 for a in audits if a["phase"] == phase and a["category"] == category and a["expected_support"] != "supported"),
        "faithful_flagged": sum(a["flagged"] for a in audits if a["phase"] == phase and a["category"] == category and a["expected_support"] == "supported"),
        "faithful_total": sum(1 for a in audits if a["phase"] == phase and a["category"] == category and a["expected_support"] == "supported")}
        for category in ("relation", "metric", "condition", "neutral_identical", "neutral_paraphrase", "neutral_omission")}
        for phase in ("coarse", "fine")}
    result = {"completed": {"cases": 12, "texts": 24, "preference_votes": len(votes), "reader_reconstructions": 24,
                             "coarse_judgments": 48, "fine_judgments": 48},
              "admission": {"pass": all(c["pass"] for c in criteria), "criteria": criteria},
              "by_rubric": summaries, "budget_violations": [b for b in budgets if b["words"] > b["limit"]],
              "witness_violations": [w for w in witnesses if not w["literal_or_empty"] or not w["within_budget"]],
              "interpretation": "Original synthetic calibration only. Not improved writing, human validity, independent trials or a fine-rubric causal effect."}
    write("decoded_votes.json", votes)
    write("decoded_audits.json", audits)
    write("summary.json", result)
    write("budgets.json", budgets)
    write("witnesses.json", witnesses)
    write("all_raw_hashes.json", {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "audits", "analyze"))
    phase = parser.parse_args().phase
    {"prepare": prepare, "audits": prepare_audits, "analyze": analyze}[phase]()
