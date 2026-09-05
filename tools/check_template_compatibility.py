#!/usr/bin/env python3
"""Explicitly download pinned public styles and compile original test fixtures.

Requires Pandoc, TeX and Poppler. Never sends manuscripts or credentials. Only
allowlisted style files enter a disposable directory; shell escape is disabled.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

from render_examples import command

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "templates"
MAX_DOWNLOAD = 8 * 1024 * 1024
MAX_STYLE = 1024 * 1024


def style_files(data: bytes, spec: dict) -> dict[str, bytes]:
    if hashlib.sha256(data).hexdigest() != spec["sha256"]:
        raise ValueError(f"{spec['id']}: archive SHA-256 mismatch; review upstream before updating the pin")
    result = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for name in spec["files"]:
            if not re.fullmatch(r"[A-Za-z0-9_.-]+\.(?:sty|bst)", name):
                raise ValueError("Only flat style filenames may be written")
            member = spec["archive_prefix"] + name
            matches = [entry for entry in archive.infolist() if entry.filename == member]
            if len(matches) != 1:
                raise ValueError(f"Missing or duplicate style member: {member}")
            entry = matches[0]
            if entry.file_size > MAX_STYLE or stat.S_ISLNK(entry.external_attr >> 16) or entry.is_dir():
                raise ValueError(f"Invalid style member: {member}")
            result[name] = archive.read(entry)
    return result


def check_pdf_text(template: str, pdf_text: str, pdf_info: str) -> None:
    compact_text = re.sub(r"\s+", "", pdf_text).casefold()
    compact_all = re.sub(r"\s+", "", pdf_text + pdf_info).casefold()
    for marker in ("IdentitySentinel", "AffiliationSentinel", "identity@example.invalid",
                   "AUTHORERR", "[?]", "??"):
        if marker.casefold() in compact_all:
            raise ValueError(f"{template}: unexpected rendered marker {marker}")
    for marker in ("Super Writer Template", "0.1083", "0.0851", "Hastie"):
        if re.sub(r"\s+", "", marker).casefold() not in compact_text:
            raise ValueError(f"{template}: expected PDF content missing: {marker}")


def verify(spec: dict, output: Path | None) -> dict:
    with urllib.request.urlopen(spec["url"], timeout=45) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("Template archive exceeds the download limit")
    styles = style_files(data, spec)
    with tempfile.TemporaryDirectory(prefix="writer-template-") as temporary:
        work = Path(temporary)
        for name, contents in styles.items():
            (work / name).write_bytes(contents)
        wrapper = (FIXTURES / f"{spec['id']}.tex").read_text(encoding="utf-8")
        body = (FIXTURES / "body.tex").read_text(encoding="utf-8")
        # Assemble this fixed fixture, not a general-purpose TeX include parser.
        (work / "main.tex").write_text(wrapper.replace(r"\input{body}", body), encoding="utf-8")
        shutil.copyfile(ROOT / "examples" / "knn-regression" / "references.bib", work / "references.bib")
        latex = ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        command(latex, work)
        command(["bibtex", "main"], work)
        command(latex, work)
        command(latex, work)
        log = (work / "main.log").read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?:Citation .* undefined|Reference .* undefined|There were undefined|Overfull \\[hv]box)", log):
            raise ValueError(f"{spec['id']}: unresolved references or overfull boxes")
        command(["pdftotext", "-layout", "main.pdf", "main.txt"], work)
        pdf_text = (work / "main.txt").read_text(encoding="utf-8")
        pdf_info = command(["pdfinfo", "main.pdf"], work)
        check_pdf_text(spec["id"], pdf_text, pdf_info)
        command([sys.executable, str(ROOT / "scripts" / "latex_guard.py"), "main.tex",
                 "--bib", "references.bib", "--json"], work)
        (work / "body.tex").write_text(body, encoding="utf-8")
        csl_args = []
        if spec["citation_mode"] == "numeric":
            shutil.copyfile(FIXTURES / "numeric.csl", work / "numeric.csl")
            csl_args = ["--csl=numeric.csl"]
        command(["pandoc", "body.tex", "--standalone", "--citeproc", "--bibliography=references.bib",
                 "--metadata=title:Super Writer Template Compatibility Fixture", *csl_args, "-o", "main.docx"], work)
        command([sys.executable, str(ROOT / "scripts" / "word_guard.py"), "main.docx", "--tex", "main.tex", "--fix-fonts"], work)
        command([sys.executable, str(ROOT / "scripts" / "word_guard.py"), "main.docx", "--tex", "main.tex", "--json"], work)
        unchanged = all((work / name).read_bytes() == contents for name, contents in styles.items())
        if not unchanged:
            raise ValueError("An official style changed during validation")
        pages = int(re.search(r"^Pages:\s+(\d+)", pdf_info, re.MULTILINE).group(1))
        if output is not None:
            output.mkdir(parents=True, exist_ok=True)
            command(["pdftoppm", "-f", "1", "-singlefile", "-scale-to", "1400", "-png", "main.pdf", "preview"], work)
            for filename in ("main.tex", "main.pdf", "main.txt", "main.docx", "references.bib", "preview.png"):
                shutil.copyfile(work / filename, output / filename)
    return {"template": spec["id"], "archive_sha256": spec["sha256"], "pages": pages,
            "official_styles_unchanged": unchanged, "citation_mode": spec["citation_mode"],
            "latex_guard": "pass", "word_guard": "pass", "identity_sentinels_hidden": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Optional explicit location for fixture artifacts and report")
    parser.add_argument("--template", action="append", choices=("icml2026", "iclr2026", "cvpr2026"))
    args = parser.parse_args()
    missing = [name for name in ("pandoc", "pdflatex", "bibtex", "pdftotext", "pdfinfo", "pdftoppm")
               if not shutil.which(name)]
    if missing:
        parser.error("Required tools missing: " + ", ".join(missing))
    specs = json.loads((FIXTURES / "sources.json").read_text(encoding="utf-8"))["templates"]
    results = []
    try:
        for spec in specs:
            if args.template and spec["id"] not in args.template:
                continue
            results.append(verify(spec, args.output_dir / spec["id"] if args.output_dir else None))
            print(f"PASS {spec['id']}", file=sys.stderr)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Template check failed: {exc}\n")
    report = json.dumps({"scope": "bounded fixtures, not full venue compliance", "results": results}, indent=2) + "\n"
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "report.json").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
