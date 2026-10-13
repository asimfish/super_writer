"""Check preserved bytes and declared publication boundaries, not writing quality."""

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
    pin_files = ("guide_hashes.json", "source_hashes.json", "initial_input_hashes.json", "initial_hashes.json",
                 "editor_input_hashes.json", "generation_hashes.json", "assessment_input_hashes.json", "reader_hashes.json",
                 "audit_input_hashes.json", "all_raw_hashes.json") if local_inputs else ("all_raw_hashes.json",)
    pins_checked = 0
    for name in pin_files:
        base = ROOT if local_inputs else target
        for path, expected in json.loads((base / name).read_text()).items():
            if hashlib.sha256((base / path).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Frozen artifact changed: {path}")
            pins_checked += 1
    for folder in ("inputs", "sources", "metadata"):
        if (target / folder).exists():
            raise ValueError(f"Private source folder redistributed: {folder}")
    if list(target.rglob("*.pdf")):
        raise ValueError("PDF redistributed")
    if len(json.loads((target / "all_raw_hashes.json").read_text())) != 36:
        raise ValueError("Incomplete raw archive")
    source_pins = json.loads((target / "source_hashes.json").read_text())
    receipts = json.loads((target / "source_receipts.json").read_text())
    if len(receipts) != 6 or {r["id"] for r in receipts} != {f"A{i:02d}" for i in range(1, 7)}:
        raise ValueError("Incomplete source receipts")
    for receipt in receipts:
        for role in ("pdf", "extracted", "body", "recipe"):
            if source_pins.get(receipt["paths"][role]) != receipt["hashes"][role]:
                raise ValueError(f"Source receipt/pin disagreement: {receipt['id']}/{role}")
    result = {"byte_identical_copied_files": len(hashes), "raw_response_files": 36, "pin_entries_checked": pins_checked,
              "all_frozen_local_inputs_unchanged": True if local_inputs else "not checked: omitted", "publisher_body_withheld": True,
              "source_receipt_hash_declarations_match_pins": True}
    print(json.dumps(result))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--local-inputs", action="store_true")
    args = parser.parse_args()
    verify(args.target, args.local_inputs)
