"""Recheck declared byte assembly without normalizing source text."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():
    receipts = []
    for pid in ("N1", "N2"):
        meta = json.loads((ROOT / f"metadata/{pid}.json").read_text())
        raw = (ROOT / f"sources/{pid}.raw.txt").read_bytes()
        body = (ROOT / f"inputs/{pid}.txt").read_bytes()
        segments = meta.get("ordered_segments", meta.get("segments"))
        slices = []
        for expected_order, segment in enumerate(segments, 1):
            if segment["order"] != expected_order:
                raise ValueError(f"Segment order: {pid}")
            start = segment.get("raw_start_byte", segment.get("raw_byte_start"))
            end = segment.get("raw_end_byte", segment.get("raw_byte_end_exclusive"))
            if not 0 <= start < end <= len(raw):
                raise ValueError(f"Byte boundaries: {pid}")
            source = raw[start:end]
            expected_hash = segment.get("segment_sha256", segment.get("sha256"))
            if hashlib.sha256(source).hexdigest() != expected_hash:
                raise ValueError(f"Segment hash: {pid}/{expected_order}")
            body_start = segment.get("body_start_byte", segment.get("body_byte_start"))
            body_end = segment.get("body_end_byte", segment.get("body_byte_end_exclusive"))
            if source != body[body_start:body_end]:
                raise ValueError(f"Body differs from original span: {pid}/{expected_order}")
            slices.append(source)
        separator = b"" if pid == "N1" else b"\n\n"
        if separator.join(slices) != body:
            raise ValueError(f"Unexpected body bytes: {pid}")
        receipts.append({"id": pid, "segments": len(slices), "raw_bytes": len(raw), "body_bytes": len(body),
                         "all_segments_original_bytes": True, "declared_assembly_identical": True})
    with (ROOT / "source_assembly_verification.json").open("x") as stream:
        stream.write(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps(receipts))


if __name__ == "__main__":
    main()
