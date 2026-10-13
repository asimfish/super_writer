#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAPER_ID = "P08"
SEGMENTS = [
    {
        "section": "Table 1: reflection-token definitions (float before Section 3)",
        "start": "Type Input Output Definitions\n",
        "end": "of retrieved passages prepended to input, or pre-train a retriever and LM jointly, followed by few-\n",
    },
    {
        "section": "3 Self-RAG: Learning to Retrieve, Generate and Critique (3.1-3.3)",
        "start": "3 SELF-RAG: LEARNING TO RETRIEVE, GENERATE AND CRITIQUE\n",
        "end": "4 EXPERIMENTS\n",
    },
    {
        "section": "4 Experiments (4.1-4.3)",
        "start": "4 EXPERIMENTS\n",
        "end": "5 RESULTS AND ANALYSIS\n",
    },
    {
        "section": "5 Results and Analysis (5.1-5.2, complete Table 2 and Figure 3)",
        "start": "5 RESULTS AND ANALYSIS\n",
        "end": "6 CONCLUSION\n",
    },
    {
        "section": "Ethical Concerns: separately located citation limitation",
        "start": "ETHICAL CONCERNS\n",
        "end": "ACKNOWLEDGMENTS\n",
    },
    {
        "section": "A.2: separately located submission-time API limitation",
        "start": "Note that at the time\n",
        "end": "A.3 SELF-RAG TRAINING\n",
    },
]


def main():
    pdf = ROOT / "sources" / (PAPER_ID + ".pdf")
    extracted = ROOT / "sources" / (PAPER_ID + ".extracted.txt")
    output = ROOT / "inputs" / (PAPER_ID + ".txt")
    subprocess.run(["pdftotext", "-raw", str(pdf), str(extracted)], check=True)
    raw = extracted.read_bytes()
    pieces = []
    manifest = []
    previous_end = 0
    for specification in SEGMENTS:
        start_marker = specification["start"].encode("utf-8")
        end_marker = specification["end"].encode("utf-8")
        assert raw.count(start_marker) == 1, specification["start"]
        assert raw.count(end_marker) == 1, specification["end"]
        start = raw.index(start_marker)
        end = raw.index(end_marker, start + len(start_marker))
        assert start >= previous_end and end > start
        pieces.append(raw[start:end])
        manifest.append({
            **specification,
            "start_inclusive": True,
            "end_exclusive": True,
            "pdf_pages": [raw[:start].count(b"\f") + 1, raw[:end - 1].count(b"\f") + 1],
            "byte_range": [start, end],
        })
        previous_end = end
    # Retain source bytes and float order; do not repair formulas, captions, or tables.
    body = b"".join(pieces)
    for required in [b"Table 1:", b"Table 2:", b"Figure 3:", b"Ret-ChatGPT", b"No Critic"]:
        assert required in body, required
    for excluded in [b"ABSTRACT\n", b"1 INTRODUCTION\n", b"2 RELATED WORK\n",
                     b"6 CONCLUSION\n", b"ACKNOWLEDGMENTS\n", b"REFERENCES\n",
                     b"A.3 SELF-RAG TRAINING\n"]:
        assert excluded not in body, excluded
    output.write_bytes(body)
    print(json.dumps({
        "id": PAPER_ID,
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "extracted_sha256": hashlib.sha256(raw).hexdigest(),
        "body_sha256": hashlib.sha256(body).hexdigest(),
        "body_word_count_whitespace": len(body.decode("utf-8").split()),
        "extraction_segments": manifest,
    }, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
