"""Keep primary and text-only audit labels separate; no favorable substitution."""

import collections
import hashlib
import json
import statistics
from pathlib import Path

import analyze
from experiment import words


ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def audit_summary(rows):
    return {c: {"fidelity": dict(collections.Counter(r["fidelity"] for r in rows if r["condition"] == c)),
                "core_recovery": {"mean": statistics.mean(r["core_recovery"] for r in rows if r["condition"] == c),
                                  "counts": dict(collections.Counter(r["core_recovery"] for r in rows if r["condition"] == c))},
                "scope_recovery": {"mean": statistics.mean(r["scope_recovery"] for r in rows if r["condition"] == c),
                                   "counts": dict(collections.Counter(r["scope_recovery"] for r in rows if r["condition"] == c))}}
            for c in ("baseline", "candidate")}


def main():
    domains = read("domains.json")
    files = [f"supplemental/audit_{d['id']}.json" for d in domains]
    if any(not (ROOT / f).is_file() for f in files):
        raise ValueError("Supplementary audit incomplete")
    primary = {a["id"]: a for a in read("decoded_audits.json")}
    mapping = read("private_reader_mapping.json")
    secondary, differences = [], []
    budgets = []
    for domain in domains:
        did = domain["id"]
        expected = [m for m in mapping if m["domain"] == did]
        rows = analyze.exact_rows(f"supplemental/audit_{did}.json", "audits", [m["id"] for m in expected], root=ROOT)
        for key in expected:
            r = rows[key["id"]]
            if r["fidelity"] not in analyze.FIDELITY or any(not analyze.valid_score(r[k], 2) for k in
                                                             ("core_recovery", "scope_recovery")):
                raise ValueError(f"Invalid supplementary audit: {r}")
            if not r["failure_types"] or not set(r["failure_types"]) <= analyze.FAILURES:
                raise ValueError(f"Invalid supplementary failure types: {r}")
            if "none" in r["failure_types"] and len(r["failure_types"]) != 1:
                raise ValueError(f"Inconsistent supplementary failure types: {r}")
            entry = {**key, **r}
            secondary.append(entry)
            old = primary[key["id"]]
            changed = [k for k in ("fidelity", "core_recovery", "scope_recovery", "failure_types")
                       if old[k] != entry[k]]
            if changed:
                differences.append({"id": key["id"], "pair": key["pair"], "domain": did,
                                    "condition": key["condition"], "changed_fields": changed,
                                    "primary": old, "text_only": entry})
            n = words(r["reason"])
            budgets.append({"id": key["id"], "words": n, "budget_pass": n <= 90})
    assert len(secondary) == len(primary) == 216
    output = {"primary_count": 216, "text_only_count": 216,
              "primary": audit_summary(list(primary.values())), "text_only": audit_summary(secondary),
              "agreement": {k: sum(primary[r["id"]][k] == r[k] for r in secondary)
                            for k in ("fidelity", "core_recovery", "scope_recovery")},
              "differences": differences,
              "by_domain": {d["id"]: audit_summary([r for r in secondary if r["domain"] == d["id"]]) for d in domains},
              "by_unit": {u: audit_summary([r for r in secondary if r["unit"] == u])
                          for u in ("abstract", "methods", "results")},
              "budget_violations": [r for r in budgets if not r["budget_pass"]],
              "interpretation": "Separate supplementary source-access robustness pass, not a replacement or pooled independent evidence. "
                                "Variation can reflect assessor variation and lack of layout, not only primary exposure."}
    for name, value in (("supplemental/summary.json", output), ("supplemental/decoded_audits.json", secondary),
                        ("supplemental/word_counts.json", budgets),
                        ("supplemental/hashes.json", {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files})):
        path = ROOT / name
        if path.exists():
            raise FileExistsError(path)
        path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps({k: output[k] for k in ("primary_count", "text_only_count", "text_only", "agreement")}, indent=2))


if __name__ == "__main__":
    main()
