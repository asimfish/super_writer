"""Strict, post-assessment analysis of frozen raw responses."""

import collections
import hashlib
import json
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCORES = ("contribution", "argument", "selection", "language")
FIDELITY = {"pass", "concern", "fail"}
FAILURES = {"none", "writer_error", "text_missing", "text_ambiguous", "reader_inference", "reader_error"}


def read(path):
    return json.loads((ROOT / path).read_text())


def exact_rows(path, field, ids, *, root=None):
    rows = read(path)[field] if root is None else json.loads((root / path).read_text())[field]
    if len(rows) != len(ids) or {row["id"] for row in rows} != set(ids):
        raise ValueError(f"Incomplete/duplicate IDs: {path}")
    return {row["id"]: row for row in rows}


def valid_score(value, maximum):
    return type(value) is int and 0 <= value <= maximum


def bootstrap_papers(paper_scores, domains, seed=20261013, draws=10000):
    rng = random.Random(seed)
    samples = []
    for _ in range(draws):
        selected = [paper_scores[rng.choice([p[0] for p in domain["papers"]])]
                    for domain in domains for _ in domain["papers"]]
        samples.append(statistics.mean(selected))
    samples.sort()
    return {"draws": draws, "seed": seed, "interval": [samples[249], samples[9749]],
            "interpretation": "Conditional paper-cluster descriptive interval only; "
            "two purposively selected papers/domain, not population significance."}


def summarize(votes, audits):
    return {
        "votes": dict(collections.Counter(v["winner"] for v in votes)),
        "source_audit": {c: dict(collections.Counter(a["fidelity"] for a in audits
                                                    if a["condition"] == c))
                         for c in ("baseline", "candidate")},
        "reader_recovery": {
            c: {k: {"mean": statistics.mean(a[k] for a in audits if a["condition"] == c),
                    "counts": dict(collections.Counter(a[k] for a in audits if a["condition"] == c))}
                for k in ("core_recovery", "scope_recovery")}
            for c in ("baseline", "candidate")},
        "reviewer_scores": {
            c: {k: statistics.mean(v[c][k] for v in votes) for k in SCORES}
            for c in ("baseline", "candidate")},
        "reviewer_fidelity": {
            c: dict(collections.Counter(v[c]["fidelity"] for v in votes))
            for c in ("baseline", "candidate")},
        "failure_types": {
            c: dict(collections.Counter(f for a in audits if a["condition"] == c
                                        for f in a["failure_types"]))
            for c in ("baseline", "candidate")},
    }


def main():
    # Complete-review gate precedes reading any label mappings or preferences.
    domains = read("domains.json")
    paths = [f"raw/review_{d['id']}_{r}.json" for d in domains for r in (1, 2)]
    paths += [f"raw/reader_{d['id']}_{r}.json" for d in domains for r in (1, 2)]
    paths += [f"raw/audit_{d['id']}.json" for d in domains]
    missing = [p for p in paths if not (ROOT / p).is_file()]
    if missing:
        raise ValueError(f"Assessment incomplete, no unblinding: {missing}")
    for file, expected in {**read("frozen_hashes.json"), **read("source_hashes.json")}.items():
        if hashlib.sha256((ROOT / file).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Frozen guide/protocol drift: {file}")
    for file, expected in read("generation_hashes.json").items():
        if hashlib.sha256((ROOT / file).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Raw generation drift: {file}")
    for file, expected in read("initial_hashes.json").items():
        if hashlib.sha256((ROOT / file).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Shared initial draft drift: {file}")
    mapping = read("private_mapping.json")
    reader_mapping = read("private_reader_mapping.json")
    votes, audit_rows, pair_rows = [], [], []
    for domain in domains:
        did = domain["id"]
        pairs = [m for m in mapping if m["domain"] == did]
        readers = [m for m in reader_mapping if m["domain"] == did]
        by_reviewer = {}
        for reviewer in (1, 2):
            rows = exact_rows(f"raw/review_{did}_{reviewer}.json", "reviews", [m["id"] for m in pairs])
            by_reviewer[reviewer] = rows
            for pair in pairs:
                row = rows[pair["id"]]
                if row["winner"] not in ("A", "B", "Tie") or not isinstance(row["reason"], str):
                    raise ValueError(f"Invalid review: {row}")
                decoded = {}
                for label in ("A", "B"):
                    ratings = row[label]
                    if ratings["fidelity"] not in FIDELITY:
                        raise ValueError(f"Invalid fidelity: {row}")
                    if any(not valid_score(ratings[k], 5) or ratings[k] == 0 for k in SCORES):
                        raise ValueError(f"Invalid ordinal score: {row}")
                    decoded[pair[f"reviewer_{reviewer}"][label]] = ratings
                winner = "tie" if row["winner"] == "Tie" else pair[f"reviewer_{reviewer}"][row["winner"]]
                votes.append({"id": pair["id"], "paper": pair["paper"], "domain": did,
                              "sample": pair["sample"], "unit": pair["unit"], "reviewer": reviewer,
                              "winner": winner, **decoded, "reason": row["reason"]})
        audited = exact_rows(f"raw/audit_{did}.json", "audits", [r["id"] for r in readers])
        for reader in (1, 2):
            ids = [r["id"] for r in readers if r["reader"] == reader]
            readings = exact_rows(f"raw/reader_{did}_{reader}.json", "readings", ids)
            for row in readings.values():
                if any(not isinstance(row[k], str) for k in ("core_relation", "scope", "witness", "unclear")):
                    raise ValueError(f"Invalid reader schema: {row}")
        for key in readers:
            row = audited[key["id"]]
            if row["fidelity"] not in FIDELITY or any(not valid_score(row[k], 2) for k in
                                                       ("core_recovery", "scope_recovery")):
                raise ValueError(f"Invalid audit: {row}")
            if not isinstance(row["failure_types"], list) or not set(row["failure_types"]) <= FAILURES:
                raise ValueError(f"Invalid failure types: {row}")
            if not row["failure_types"] or ("none" in row["failure_types"] and len(row["failure_types"]) != 1):
                raise ValueError(f"Inconsistent failure types: {row}")
            audit_rows.append({**key, **row})
        for pair in pairs:
            pv = [v for v in votes if v["id"] == pair["id"]]
            winners = [v["winner"] for v in pv]
            outcome = f"unanimous_{winners[0]}" if len(set(winners)) == 1 else "disagreement"
            pa = {a["condition"]: a for a in audit_rows if a["pair"] == pair["id"]}
            pair_rows.append({"id": pair["id"], "paper": pair["paper"], "domain": did,
                              "sample": pair["sample"], "unit": pair["unit"],
                              "winners": winners, "outcome": outcome,
                              "fidelity": {c: a["fidelity"] for c, a in pa.items()},
                              "core_delta": pa["candidate"]["core_recovery"] - pa["baseline"]["core_recovery"],
                              "scope_delta": pa["candidate"]["scope_recovery"] - pa["baseline"]["scope_recovery"]})
    if len(votes) != 216 or len(audit_rows) != 216 or len(pair_rows) != 108:
        raise ValueError("Full planned count mismatch")
    paper_scores = {pid: statistics.mean({"candidate": 1, "baseline": -1, "tie": 0}[v["winner"]]
                                          for v in votes if v["paper"] == pid)
                    for domain in domains for pid, _, _ in domain["papers"]}
    counts = read("word_counts.json")
    in_budget = {f"{c['paper']}_s{c['sample']}_{c['unit']}" for c in counts
                 if c["condition"] != "initial" and c["unit"] != "notes"}
    for c in counts:
        if c["condition"] != "initial" and c["unit"] != "notes" and not c["budget_pass"]:
            in_budget.discard(f"{c['paper']}_s{c['sample']}_{c['unit']}")
    output = {
        "completed": {"papers": 12, "domains": 6, "initial_passages": 108,
                      "final_passages": 216, "pairs": 108, "preference_votes": 216,
                      "reader_reconstructions": 216, "source_audits": 216},
        "overall": summarize(votes, audit_rows),
        "pair_outcomes": dict(collections.Counter(p["outcome"] for p in pair_rows)),
        "paper_signed_preferences": paper_scores,
        "mean_paper_signed_preference": statistics.mean(paper_scores.values()),
        "conditional_bootstrap": bootstrap_papers(paper_scores, domains),
        "by_domain": {d["id"]: summarize([v for v in votes if v["domain"] == d["id"]],
                                          [a for a in audit_rows if a["domain"] == d["id"]]) for d in domains},
        "by_paper": {pid: summarize([v for v in votes if v["paper"] == pid],
                                    [a for a in audit_rows if a["paper"] == pid]) for pid in paper_scores},
        "by_unit": {unit: summarize([v for v in votes if v["unit"] == unit],
                                    [a for a in audit_rows if a["unit"] == unit])
                    for unit in ("abstract", "methods", "results")},
        "by_sample": {sample: summarize([v for v in votes if v["sample"] == sample],
                                        [a for a in audit_rows if a["sample"] == sample]) for sample in (1, 2, 3)},
        "budget_violations": [c for c in counts if not c["budget_pass"]],
        "word_summary": {condition: {unit: {
            "mean": statistics.mean(c["words"] for c in counts if c["condition"] == condition and c["unit"] == unit),
            "minimum": min(c["words"] for c in counts if c["condition"] == condition and c["unit"] == unit),
            "maximum": max(c["words"] for c in counts if c["condition"] == condition and c["unit"] == unit)}
            for unit in ("abstract", "methods", "results", "notes")}
            for condition in ("initial", "baseline", "candidate")},
        "budget_sensitivity": {"eligible_pairs": len(in_budget),
                               "votes": dict(collections.Counter(v["winner"] for v in votes
                                                                   if v["id"] in in_budget))},
        "source_concerned_unanimous_preferences": [p for p in pair_rows
             if p["outcome"] in ("unanimous_candidate", "unanimous_baseline")
             and p["fidelity"][p["outcome"].removeprefix("unanimous_")] != "pass"],
    }
    for name, value in (("summary.json", output), ("decoded_votes.json", votes),
                        ("decoded_audits.json", audit_rows), ("pair_results.json", pair_rows)):
        path = ROOT / name
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite analysis: {path}")
        path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps({"completed": output["completed"], "overall": output["overall"],
                      "pair_outcomes": output["pair_outcomes"],
                      "mean_paper_signed_preference": output["mean_paper_signed_preference"],
                      "conditional_bootstrap": output["conditional_bootstrap"],
                      "budget_violations": len(output["budget_violations"])}, indent=2))


if __name__ == "__main__":
    main()
