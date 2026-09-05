#!/usr/bin/env python3
"""Inspect a local PDF with Poppler. Mechanical checks, not visual certification.

No TeX execution, network access, package installation or manuscript modification.
Receipts bind the inspected PDF and optional log to SHA-256 hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

MAX_PDF = 50 * 1024 * 1024
MAX_OUTPUT = 16 * 1024 * 1024


def run_tool(args: list[str]) -> str:
    with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
        result = subprocess.run(args, stdout=output, stderr=errors, timeout=45,
                                env={**os.environ, "LC_ALL": "C"}, check=False)
        output.seek(0)
        data = output.read(MAX_OUTPUT + 1)
        errors.seek(0)
        message = errors.read(4096).decode("utf-8", errors="replace")
    if result.returncode or len(data) > MAX_OUTPUT:
        raise ValueError(f"{args[0]} failed or exceeded output limit: {message}")
    return data.decode("utf-8", errors="replace")


def inspect_bbox(xml: str) -> tuple[int, list[str], list[str]]:
    if "<!ENTITY" in xml.upper():
        raise ValueError("Unexpected XML entity declaration")
    root = ET.fromstring(xml)
    pages = root.findall(".//{*}page")
    errors, warnings = [], []
    if not pages:
        errors.append("PDF has no inspectable pages")
    for number, page in enumerate(pages, 1):
        width, height = float(page.attrib["width"]), float(page.attrib["height"])
        if not all(math.isfinite(v) and v > 0 for v in (width, height)):
            raise ValueError("Invalid page dimensions")
        words = page.findall(".//{*}word")
        if not words:
            warnings.append(f"Page {number}: no extractable text; inspect image-only or blank content visually")
        for word in words:
            x0, y0, x1, y1 = (float(word.attrib[k]) for k in ("xMin", "yMin", "xMax", "yMax"))
            if (not all(math.isfinite(v) for v in (x0, y0, x1, y1)) or x0 > x1 or y0 > y1
                    or x0 < -1 or y0 < -1 or x1 > width + 1 or y1 > height + 1):
                errors.append(f"Page {number}: text bounding box outside physical page or invalid")
                break
    return len(pages), errors, warnings


def inspect_fonts(fonts: str) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    lines = fonts.splitlines()
    if len(lines) < 2 or lines[0].split() != ["name", "type", "encoding", "emb", "sub", "uni", "object", "ID"]:
        raise ValueError("Unrecognized pdffonts header; cannot verify font embedding")
    rows = lines[2:]
    for row in rows:
        if not row.strip():
            continue
        match = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", row)
        if not match:
            raise ValueError("Unrecognized pdffonts output; cannot verify font embedding")
        if match.group(1) != "yes":
            errors.append(f"Unembedded font: {row.split()[0]}")
        if "Type 3" in row:
            warnings.append(f"Type 3 font: {row.split()[0]}; check the venue's actual font policy")
    if not rows:
        warnings.append("No fonts listed; inspect rasterized or image-only pages")
    return errors, warnings


def inspect_log(log: str) -> list[str]:
    findings = []
    if re.search(r"(?:Citation .* undefined|Reference .* undefined|There were undefined)", log):
        findings.append("Unresolved citations or references in the supplied log")
    if re.search(r"Overfull \\[hv]box", log):
        findings.append("Overfull box in the supplied log; inspect the actual affected page")
    if re.search(r"(?m)^!|Fatal error occurred", log):
        findings.append("Fatal TeX error in the supplied log")
    return findings


def check(pdf: Path, log: Path | None = None, max_pages: int | None = None) -> dict:
    pdf = pdf.resolve(strict=True)
    with pdf.open("rb") as stream:
        data = stream.read(MAX_PDF + 1)
    if len(data) > MAX_PDF or not data.startswith(b"%PDF-"):
        raise ValueError("Expected a PDF no larger than 50 MiB")
    # Inspect exactly the snapshotted bytes, not a file changing during rendering.
    with tempfile.TemporaryDirectory(prefix="writer-pdf-check-") as temporary:
        snapshot = Path(temporary) / "input.pdf"
        snapshot.write_bytes(data)
        pages, errors, warnings = inspect_bbox(run_tool(["pdftotext", "-bbox", str(snapshot), "-"]))
        font_errors, font_warnings = inspect_fonts(run_tool(["pdffonts", str(snapshot)]))
    errors.extend(font_errors)
    warnings.extend(font_warnings)
    if max_pages is not None and pages > max_pages:
        errors.append(f"Total PDF pages {pages} exceed explicit limit {max_pages}")
    hashes = {"pdf_sha256": hashlib.sha256(data).hexdigest()}
    if log is not None:
        with log.open("rb") as stream:
            log_data = stream.read(MAX_OUTPUT + 1)
        if len(log_data) > MAX_OUTPUT:
            raise ValueError("Log exceeds 16 MiB limit")
        hashes["log_sha256"] = hashlib.sha256(log_data).hexdigest()
        errors.extend(inspect_log(log_data.decode("utf-8", errors="replace")))
        warnings.append("Log is caller-supplied; its hash does not prove it produced this PDF")
    return {"ok": not errors, "scope": "physical-page bounds, font embedding and optional log/total-page checks only",
            "pages": pages, **hashes, "errors": errors, "warnings": warnings,
            "manual_checks": ["Visual layout on every page, figures and equations", "Venue body-page boundary and required sections",
                              "Anonymity including metadata, figures and external links", "Evidence and citation support"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--max-pages", type=int, help="Total PDF pages, not a venue body-only budget")
    args = parser.parse_args()
    if args.max_pages is not None and args.max_pages < 1:
        parser.error("--max-pages must be positive")
    try:
        result = check(args.pdf, args.log, args.max_pages)
    except (OSError, ValueError, KeyError, ET.ParseError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, f"PDF check unavailable: {exc}\n")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
