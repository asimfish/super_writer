"""Extract unchanged body and explicitly relevant supplementary sections."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
raw = (ROOT / "sources/P13.extracted.txt").read_bytes()
pdf = (ROOT / "sources/P13.pdf").read_bytes()
boundaries = [
    ("Complete hardware, ACT method, experiments and ablations (Sections III-VI)",
     "III. ALOHA: A LOW-COST OPEN-SOURCE HARDWARE\n", "VII. LIMITATIONS AND CONCLUSION\n"),
    ("Complete related supplementary C-F, including detailed architecture, settings, user study and limitations; displaced architecture diagram and hyperparameter tables IV-VIII",
     "C. Detailed Architecture Diagram\n", None),
]
segments, parts = [], []
for order, (label, start_text, end_text) in enumerate(boundaries, 1):
    start = start_text.encode()
    assert raw.count(start) == 1
    first = raw.index(start)
    if end_text:
        end = end_text.encode()
        assert raw.count(end) == 1
        last = raw.index(end)
    else:
        last = len(raw)
    assert first < last
    parts.append(raw[first:last])
    segments.append({"order": order, "label": label, "start_string": start_text,
                     "end_string": end_text, "end_mode": "exclusive_boundary" if end_text else "end_of_file",
                     "pdf_pages": [raw[:first].count(b"\f") + 1,
                                   raw[:last - 1].count(b"\f") + 1],
                     "raw_utf8_byte_range": [first, last], "word_count": len(raw[first:last].split())})
body = b"".join(parts)
(ROOT / "inputs/P13.txt").write_bytes(body)
meta = {
    "id": "P13", "title": "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware",
    "domain": "robotics", "venue": "Proceedings of Robotics: Science and Systems XIX", "year": 2023,
    "metadata_url": "https://www.roboticsproceedings.org/rss19/p016.html",
    "pdf_url": "https://www.roboticsproceedings.org/rss19/p016.pdf",
    "pdf_sha256": hashlib.sha256(pdf).hexdigest(),
    "extracted_sha256": hashlib.sha256(raw).hexdigest(),
    "body_sha256": hashlib.sha256(body).hexdigest(),
    "pages": {"pdf_total": 19, "numbering": "1-based physical PDF pages", "selected_segments": segments},
    "ordered_extraction_segments": segments,
    "extraction_command": "pdftotext -raw sources/P13.pdf sources/P13.extracted.txt",
    "selection_command": "python3 sources/P13.extract.py",
    "extractor": "Poppler pdftotext 26.03.0",
    "source_version": {"kind": "official_proceedings_pdf", "fallback_used": False, "retrieved_date": "2026-10-11"},
    "download_attempts": [{"attempt": 1, "max_time_seconds": 80, "automatic_retries": 0,
                            "bytes": len(pdf), "curl_exit_code": 0, "result": "complete official PDF"}],
    "prior_family_overlap": "Related action-chunking concept in writing-library.json; exact paper/title not found in pre-generation repository search. Model-pretraining exposure unknown.",
    "identity_verification": "Official RSS proceedings landing page title, BibTeX year/DOI 10.15607/RSS.2023.XIX.016, and PDF first page.",
    "body_word_count": len(body.decode().split()),
    "source_warnings": ["Replacement for P02 download failure, selected before any generation.",
                        "Table III and adjacent prose say three remaining real tasks but display/name four; original source wording and rows retained.",
                        "Stage success ratios are not inferred to be joint trajectory-completion probabilities; tables contain later-stage counts larger than earlier ones.",
                        "Simulation uses three seeds and 50 trials each; hardware uses one seed and 25 trials. Ablation evidence must not silently establish hardware causality."],
    "extraction_warnings": ["Raw line-wrap hyphens, glyphs, equations, form feeds and flattened tables remain unchanged.",
                            "pdfinfo reports Bad annotation destination; text extraction succeeds. PDF plots remain graphical source, not reconstructed from flattened labels.",
                            "Related supplementary C-F and displaced final figures/tables are explicitly included; unrelated appendices A-B, abstract, Introduction, Related Work, and summary conclusion are excluded."],
    "limitations_locator": {"section": "Appendix F", "pdf_page": raw[:raw.index(b'F. Limitations\n')].count(b'\f') + 1},
}
(ROOT / "metadata/P13.json").write_text(json.dumps(meta, indent=2, ensure_ascii=True) + "\n")
print(json.dumps({"words": meta["body_word_count"], "segments": segments}, indent=2))
