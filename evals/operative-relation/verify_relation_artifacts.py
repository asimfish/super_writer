"""Check byte preservation and intentional publication boundaries, not quality."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def verify(target, local_inputs=False):
    hashes = json.loads((target / "archive_hashes.json").read_text())
    for name, expected in hashes.items():
        for base in ((ROOT, target) if local_inputs else (target,)):
            if hashlib.sha256((base / name).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Archived bytes changed: {base / name}")
    pin_files = ("guide_hashes.json", "source_hashes.json", "initial_hashes.json", "generation_hashes.json",
                 "reader_hashes.json", "initial_input_hashes.json", "editor_input_hashes.json",
                 "assessment_input_hashes.json", "audit_input_hashes.json", "all_raw_hashes.json") if local_inputs else ("all_raw_hashes.json",)
    for name in pin_files:
        base = ROOT if local_inputs else target
        pins = json.loads((base / name).read_text())
        for path, expected in pins.items():
            if hashlib.sha256((base / path).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Frozen local artifact changed: {path}")
    for folder in ("inputs", "sources", "metadata"):
        if (target / folder).exists():
            raise ValueError(f"Private source folder redistributed: {folder}")
    if list(target.rglob("*.pdf")):
        raise ValueError("PDF redistributed")
    if len(json.loads((target / "all_raw_hashes.json").read_text())) != 24:
        raise ValueError("Incomplete raw archive")
    print(json.dumps({"byte_identical_copied_files": len(hashes), "raw_response_files": 24,
                      "all_frozen_local_inputs_unchanged": True if local_inputs else "not checked: omitted",
                      "publisher_body_withheld": True}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--local-inputs", action="store_true")
    args = parser.parse_args()
    verify(args.target, args.local_inputs)
