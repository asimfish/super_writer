import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ID = "P10"
metadata_path = ROOT / "metadata" / f"{ID}.json"
metadata = json.loads(metadata_path.read_bytes())
anchors = json.loads((ROOT / "anchors" / f"{ID}.json").read_bytes())
for unit in ("abstract", "methods", "results"):
    assert len(anchors[unit]) == 2
    assert {anchor["role"] for anchor in anchors[unit]} == {"core", "scope"}
pdf = ROOT / metadata["pdf_path"]
assert hashlib.sha256(pdf.read_bytes()).hexdigest() == metadata["pdf_sha256"]
subprocess.run(["pdftotext", "-raw", str(pdf), str(ROOT / metadata["extracted_path"])], check=True)
assert hashlib.sha256((ROOT / metadata["extracted_path"]).read_bytes()).hexdigest() == metadata["extracted_sha256"]

parts = []
body_offset = 0
for order, segment in enumerate(metadata["ordered_extraction_segments"], 1):
    assert segment["order"] == order
    raw = (ROOT / segment["source_text_path"]).read_bytes()
    start, end = segment["start"].encode(), segment["end"].encode()
    assert raw.count(start) == raw.count(end) == 1
    first, last = raw.index(start), raw.index(end)
    assert first < last
    assert [raw[:first].count(b"\f") + 1, raw[:last - 1].count(b"\f") + 1] == segment["pdf_pages"]
    part = raw[first:last]
    segment["source_byte_range"] = [first, last]
    segment["body_byte_range"] = [body_offset, body_offset + len(part)]
    segment["word_count"] = len(part.decode("utf-8").split())
    parts.append(part)
    body_offset += len(part)
body = b"".join(parts)
(ROOT / metadata["body_path"]).write_bytes(body)
metadata["body_sha256"] = hashlib.sha256(body).hexdigest()
metadata["body_word_count"] = len(body.decode("utf-8").split())
metadata["status"] = "source_preparation_complete"
metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
print(f"{ID}: {metadata['body_word_count']} words; sha256={metadata['body_sha256']}")
