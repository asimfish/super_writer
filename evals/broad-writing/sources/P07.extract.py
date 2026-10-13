#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAPER_ID = "P07"
SEGMENTS = [
    {
        "section": "2 Multi-Document Question Answering (opening)",
        "start": "2 Multi-Document Question Answering\n",
        "end": "1\nnelsonliu.me/papers/lost-in-the-middle.\n",
    },
    {
        "section": "2 Multi-Document Question Answering (continuation and 2.1-2.3)",
        "start": "analyze model performance on multi-document\nquestionanswering,",
        "end": "3 How Well Can Language Models\nRetrieve From Input Contexts?\n",
    },
    {
        "section": "3 How Well Can Language Models Retrieve From Input Contexts?",
        "start": "3 How Well Can Language Models\nRetrieve From Input Contexts?\n",
        "end": "4 Why Are Language Models Not\nRobust to Changes in the Position of\nRelevant Information?\n",
    },
    {
        "section": "4 Why Are Language Models Not Robust to Changes in the Position of Relevant Information?",
        "start": "4 Why Are Language Models Not\nRobust to Changes in the Position of\nRelevant Information?\n",
        "end": "5 Is More Context Is Always Better?\nA Case Study With Open-Domain QA\n",
    },
    {
        "section": "5 Is More Context Is Always Better? A Case Study With Open-Domain QA",
        "start": "5 Is More Context Is Always Better?\nA Case Study With Open-Domain QA\n",
        "end": "6 Related Work\n",
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
    # Byte slices only: no whitespace cleanup, OCR, reordering, or inserted labels.
    body = b"".join(pieces)
    assert b"Table 1:" in body
    for excluded in [b"1 Introduction\n", b"6 Related Work\n", b"7 Conclusion\n",
                     b"Acknowledgments\n", b"References\n", b"nelsonliu.me/papers/lost-in-the-middle."]:
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
