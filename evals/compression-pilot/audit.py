"""Verify completion provenance, auxiliary limits and the published artifact receipts."""
from collections import Counter
import hashlib
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("compression_pilot_audit", ROOT / "pilot.py")
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


def derive():
    mapping = pilot.read(ROOT / "mapping.json")
    dimensions = Counter()
    limits = []
    for judge in ("J01", "J02"):
        for case in pilot.read(ROOT / "raw" / f"{judge}.json")["cases"]:
            labels = mapping[f'{judge}/{case["id"]}']
            for comparison in case["comparisons"]:
                conditions = [labels[side] for side in comparison["pair"]]
                if "compression" in conditions:
                    control = next(c for c in conditions if c != "compression")
                    for metric in ("choice", "clarity", "economy"):
                        selected = comparison[metric]
                        chosen = "tie" if selected == "tie" else labels[selected]
                        outcome = "tie" if chosen == "tie" else "win" if chosen == "compression" else "loss"
                        dimensions[control, metric, outcome] += 1
                words = pilot.count(comparison["reason"])
                if words > 35:
                    limits.append({"reviewer": judge, "id": case["id"], "field": "reason", "words": words, "limit": 35})
            for side, version in case["versions"].items():
                for answer in version["answers"]:
                    words = pilot.count(answer["answer"])
                    if words > 25:
                        limits.append({"reviewer": judge, "id": case["id"], "side": side,
                                       "field": answer["question_id"], "words": words, "limit": 25})
    for condition in pilot.CONDITIONS:
        for block in (1, 2):
            ident = f"{condition}-{block}"
            for case in pilot.read(ROOT / "raw" / f"{ident}.json")["cases"]:
                words = pilot.count(case["note"])
                if words > 45:
                    limits.append({"writer": ident, "id": case["id"], "field": "note", "words": words, "limit": 45})
    for path in (ROOT / "responses").glob("*.json"):
        import json
        assert json.loads(pilot.read(path)["completion"]) == pilot.read(ROOT / "raw" / path.name)
    return {"dimensions": {c: {m: {o: dimensions[c, m, o] for o in ("win", "loss", "tie")}
                               for m in ("choice", "clarity", "economy")} for c in pilot.CONTROLS},
            "auxiliary_limit_deviations": limits,
            "note": "All deviations retained; reader-answer limits are outside the frozen writer gate."}


def receipts():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ROOT.rglob("*")) if p.is_file()
            and "__pycache__" not in p.parts and p.name != "receipts.json"}


if __name__ == "__main__":
    data = derive()
    if len(sys.argv) == 2 and sys.argv[1] == "check":
        assert pilot.read(ROOT / "audit.json") == data
        assert pilot.read(ROOT / "receipts.json") == receipts()
        print("Raw completions, auxiliary counts and all artifact receipts verified.")
    else:
        pilot.write_new(ROOT / "audit.json", data)
        pilot.write_new(ROOT / "receipts.json", receipts())
        print(f"Captured {len(data['auxiliary_limit_deviations'])} auxiliary limit deviations.")
