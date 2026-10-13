"""Verify public byte receipts without missing third-party source text."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():
    checked = 0
    for name in ("archive_hashes.json", "all_raw_hashes.json", "supplemental/hashes.json"):
        for file, expected in json.loads((ROOT / name).read_text()).items():
            actual = hashlib.sha256((ROOT / file).read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f"Byte receipt mismatch: {file}")
            checked += 1
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    raw = len(list((ROOT / "raw").glob("*.json")))
    secondary = len(list((ROOT / "supplemental").glob("audit_D*.json")))
    if (raw, secondary) != (manifest["raw_files"], manifest["supplementary_raw_files"]):
        raise ValueError("Raw archive count mismatch")
    if any((ROOT / name).exists() for name in ("inputs", "packets")) or list((ROOT / "sources").glob("*.pdf")):
        raise ValueError("Private paper text in public archive")
    print(json.dumps({"byte_receipts_checked": checked, "primary_raw_files": raw,
                      "supplementary_raw_files": secondary, "paper_text_redistributed": False,
                      "scope": "Byte integrity only, not scientific or prose-quality validation."}, indent=2))


if __name__ == "__main__":
    main()
