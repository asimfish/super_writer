"""Byte-preserved prior candidate and current baseline, before new source reading."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path("/Users/liyufeng/Code/super_writer")

def main():
    paths = {"baseline/argument-transfer.md": REPO / "references/argument-transfer.md",
             "candidate/argument-transfer.md": REPO / "evals/operative-relation/candidate/argument-transfer.md"}
    paths.update({f"shared/{name}.md": REPO / f"references/{name}.md" for name in
                  ("abstract-decisions", "abstract-preflight", "writing-protocols", "results-validation")})
    if paths["baseline/argument-transfer.md"].read_bytes() != (REPO / "evals/operative-relation/baseline/argument-transfer.md").read_bytes():
        raise ValueError("Canonical baseline drift; do not silently change the intervention")
    pins = {}
    for name, source in paths.items():
        dest = ROOT / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("xb") as stream:
            stream.write(source.read_bytes())
        pins[name] = hashlib.sha256(dest.read_bytes()).hexdigest()
    for name in ("PROTOCOL.md", "papers.json", "selection.json", "freeze_guides.py"):
        pins[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    with (ROOT / "guide_hashes.json").open("x") as stream:
        stream.write(json.dumps(pins, indent=2) + "\n")
    print(json.dumps({"frozen_entries": len(pins), "previous_candidate_identical": True}))

if __name__ == "__main__":
    main()
