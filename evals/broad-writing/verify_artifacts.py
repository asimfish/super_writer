"""Integrity checks and observational diagnostics; no repairs or prose rescoring."""

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def words(text):
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def main():
    counts = {"hashes": 0, "reversed_pairs": 0, "counterpart_separation": 0,
              "raw_outputs": 0, "reader_reconstructions": 0}
    for file in ("frozen_hashes.json", "source_hashes.json", "initial_hashes.json", "generation_hashes.json", "reader_hashes.json"):
        for name, sha in read(file).items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha, name
            counts["hashes"] += 1
    mapping = read("private_mapping.json")
    rmap = read("private_reader_mapping.json")
    reader_diagnostics, response_budgets = [], []
    for domain in read("domains.json"):
        did = domain["id"]
        ids = [p[0] for p in domain["papers"]]
        originals = {}
        for condition in ("initial", "baseline", "candidate"):
            for sample in (1, 2, 3):
                cases = read(f"raw/{condition}_{did}_{sample}.json")["cases"]
                assert len(cases) == 2 and {c["id"] for c in cases} == set(ids)
                originals[condition, sample] = {c["id"]: c for c in cases}
                counts["raw_outputs"] += 1
        one, two = (read(f"packets/review_{did}_{r}.json") for r in (1, 2))
        assert len(one) == len(two) == 18
        for a, b in zip(one, two, strict=True):
            assert a["id"] == b["id"] and a["A"] == b["B"] and a["B"] == b["A"]
            item = next(m for m in mapping if m["id"] == a["id"])
            for label in ("A", "B"):
                c = item["reviewer_1"][label]
                assert a[label] == originals[c, item["sample"]][item["paper"]][item["unit"]]
            readers = [r for r in rmap if r["pair"] == a["id"]]
            assert len(readers) == 2 and {r["reader"] for r in readers} == {1, 2}
            assert {r["condition"] for r in readers} == {"baseline", "candidate"}
            counts["reversed_pairs"] += 1
            counts["counterpart_separation"] += 1
        for reviewer in (1, 2):
            rows = read(f"raw/review_{did}_{reviewer}.json")["reviews"]
            for row in rows:
                n = words(row["reason"])
                response_budgets.append({"id": row["id"], "domain": did, "phase": "review",
                                         "replicate": reviewer, "words": n, "budget_pass": n <= 65})
            counts["raw_outputs"] += 1
        for reader in (1, 2):
            packet = read(f"packets/reader_{did}_{reader}.json")
            assigned = [r for r in rmap if r["domain"] == did and r["reader"] == reader]
            assert len(packet) == len(assigned) == 18
            assert sum(r["condition"] == "candidate" for r in assigned) == 9
            rows = read(f"raw/reader_{did}_{reader}.json")["readings"]
            assert len(rows) == 18 and {r["id"] for r in rows} == {p["id"] for p in packet}
            for row in rows:
                p = next(p for p in packet if p["id"] == row["id"])
                m = next(m for m in assigned if m["id"] == row["id"])
                assert p["text"] == originals[m["condition"], m["sample"]][m["paper"]][m["unit"]]
                witness = row["witness"].strip()
                n = sum(words(row[k]) for k in ("core_relation", "scope", "witness", "unclear"))
                reader_diagnostics.append({"id": row["id"], "words": n, "budget_pass": n <= 90,
                                           "witness_words": words(witness),
                                           "witness_budget_pass": words(witness) <= 15,
                                           "witness_literal_substring": bool(witness) and witness in p["text"]})
                counts["reader_reconstructions"] += 1
            counts["raw_outputs"] += 1
        rows = read(f"raw/audit_{did}.json")["audits"]
        for row in rows:
            n = words(row["reason"])
            response_budgets.append({"id": row["id"], "domain": did, "phase": "audit",
                                     "words": n, "budget_pass": n <= 90})
        counts["raw_outputs"] += 1
    assert counts["raw_outputs"] == 84 and counts["reader_reconstructions"] == 216
    raw_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted((ROOT / "raw").glob("*.json"))}
    assert len(raw_hashes) == 84
    for name, value in (("all_raw_hashes.json", raw_hashes),
                        ("reader_diagnostics.json", reader_diagnostics),
                        ("assessment_word_counts.json", response_budgets),
                        ("verification.json", {"checks": counts,
                            "reader_budget_violations": sum(not r["budget_pass"] for r in reader_diagnostics),
                            "reader_witness_violations": sum(not r["witness_budget_pass"] or not r["witness_literal_substring"]
                                                             for r in reader_diagnostics),
                            "assessment_budget_violations": sum(not r["budget_pass"] for r in response_budgets),
                            "prose_repaired": False})):
        path = ROOT / name
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite verification: {path}")
        path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps(read("verification.json"), indent=2))


if __name__ == "__main__":
    main()
