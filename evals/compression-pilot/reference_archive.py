"""Recompute saved exploratory author-reference judgments without publishing originals."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("compression_pilot_reference", ROOT / "pilot.py")
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


def analyze():
    manifest = pilot.read(ROOT / "reference-manifest.json")
    outputs = pilot.generations()
    for source in manifest["sources"]:
        prose = outputs[f'{source["id"]}-abstract', "compression"]["text"]
        assert hashlib.sha256(prose.encode()).hexdigest() == source["candidate_sha256"]
        assert pilot.count(prose) == source["candidate_words"]
    dimensions = ("choice", "focus", "organization", "economy", "language")
    counts = {name: Counter() for name in dimensions}
    normalized = []
    for judge in ("A01", "A02"):
        data = pilot.read(ROOT / "raw" / f"{judge}.json")
        assert data["reviewer_id"] == judge
        assert len(data["cases"]) == 6
        assert {c["id"] for c in data["cases"]} == {f"R{i:02}" for i in range(1, 7)}
        for case in data["cases"]:
            labels = manifest["mapping"][f'{judge}/{case["id"]}']
            outcomes = {}
            for dimension in dimensions:
                assert case[dimension] in ("A", "B", "tie")
                choice = case[dimension]
                chosen = "tie" if choice == "tie" else labels[choice]
                counts[dimension][chosen] += 1
                outcomes[dimension] = chosen
            assert case["reason"]
            normalized.append({"reviewer": judge, "id": case["id"], **outcomes,
                "reason": case["reason"],
                "improve_compression": case["improve_A"] if labels["A"] == "compression" else case["improve_B"]})
    return {"scope": "Exploratory comparison; unequal materials and lengths; originals remain private",
            "papers": 6, "reviewers": 2,
            "votes": {name: {side: counts[name][side] for side in ("compression", "author", "tie")}
                      for name in dimensions}, "normalized": normalized}


if __name__ == "__main__":
    result = analyze()
    if len(sys.argv) == 2 and sys.argv[1] == "check":
        assert pilot.read(ROOT / "reference-summary.json") == result
        print("Saved reference judgments and candidate receipts reproduce exactly.")
    else:
        pilot.write_new(ROOT / "reference-summary.json", result)
        print(json.dumps(result["votes"], indent=2))
