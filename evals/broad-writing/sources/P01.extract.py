#!/usr/bin/env python3
"""Select unchanged byte ranges from P01's Poppler -raw extraction."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "sources/P01.extracted.txt"
OUT = ROOT / "inputs/P01.txt"
SEGMENTS = [
    ("methods", "III. APPROACH\n", "IV. EXPERIMENTS\n"),
    ("experiments", "IV. EXPERIMENTS\n", "V. DISCUSSION\n"),
    ("limitations", "DMD also has several limitations. DMD assumes that the\n",
     "Possible future directions include: learning diffusion mod-\n"),
]

raw = RAW.read_bytes()
parts = []
locations = []
for name, start_string, end_string in SEGMENTS:
    start_marker, end_marker = start_string.encode(), end_string.encode()
    assert raw.count(start_marker) == 1, (name, "nonunique start")
    assert raw.count(end_marker) == 1, (name, "nonunique end")
    start, end = raw.index(start_marker), raw.index(end_marker)
    assert start < end, (name, "reversed boundary")
    parts.append(raw[start:end])
    locations.append({
        "name": name, "start_byte": start, "end_byte_exclusive": end,
        "pdf_pages": [raw[:start].count(b"\f") + 1,
                      raw[:end - 1].count(b"\f") + 1],
        "words": len(raw[start:end].decode("utf-8").split()),
    })
assert all(a["end_byte_exclusive"] <= b["start_byte"]
           for a, b in zip(locations, locations[1:]))
body = b"".join(parts)
OUT.write_bytes(body)
print(json.dumps({
    "body_sha256": hashlib.sha256(body).hexdigest(),
    "extracted_sha256": hashlib.sha256(raw).hexdigest(),
    "word_count": len(body.decode("utf-8").split()),
    "segments": locations,
}, indent=2))
