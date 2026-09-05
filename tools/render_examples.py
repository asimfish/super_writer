#!/usr/bin/env python3
"""Build the public worked examples with Pandoc, TeX and Poppler; no network."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {"knn-regression": "manuscript", "theory-note": "manuscript", "review-response": "response"}


def command(args: list[str], cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=120,
                            env={**os.environ, "openin_any": "p", "openout_any": "p"})
    if result.returncode:
        raise RuntimeError(f"{args[0]} exited {result.returncode}:\n{result.stdout[-4000:]}\n{result.stderr[-2000:]}")
    return result.stdout


def render(name: str, output: Path) -> dict:
    stem = SAMPLES[name]
    source = ROOT / "examples" / name
    with tempfile.TemporaryDirectory(prefix="writer-render-") as temporary:
        work = Path(temporary)
        shutil.copyfile(source / f"{stem}.md", work / f"{stem}.md")
        bibliography = source / "references.bib"
        bib_args = []
        if bibliography.exists():
            shutil.copyfile(bibliography, work / "references.bib")
            bib_args = ["--bibliography=references.bib"]
        numbering = [] if name == "review-response" else ["--number-sections"]
        command([
            "pandoc", f"{stem}.md", "--standalone", *numbering, "--natbib", *bib_args,
            "-V", "documentclass=article", "-V", "papersize=letter", "-V", "fontsize=10pt",
            "-V", "geometry=margin=23mm", "-V", "biblio-style=plainnat",
            "-o", f"{stem}.tex",
        ], work)
        latex = ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"]
        command(latex, work)
        if bib_args:
            command(["bibtex", stem], work)
        command(latex, work)
        command(latex, work)
        log = (work / f"{stem}.log").read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?:Citation .* undefined|Reference .* undefined|There were undefined|Overfull \\[hv]box)", log):
            raise RuntimeError(f"{name}: unresolved references or overfull boxes; inspect the TeX output")
        command(["pdftotext", "-layout", f"{stem}.pdf", f"{stem}.txt"], work)
        text = (work / f"{stem}.txt").read_text(encoding="utf-8")
        if len(text.strip()) < 500 or "[?]" in text or "??" in text:
            raise RuntimeError(f"{name}: blank or unresolved PDF text")
        info = command(["pdfinfo", f"{stem}.pdf"], work)
        pages = int(re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE).group(1))
        command(["pdftoppm", "-f", "1", "-singlefile", "-scale-to", "1600", "-png", f"{stem}.pdf", "preview"], work)
        command(["pandoc", f"{stem}.md", "--standalone", "--citeproc", *bib_args, "-o", f"{stem}.docx"], work)
        command([sys.executable, str(ROOT / "scripts" / "word_guard.py"), f"{stem}.docx",
                 "--tex", f"{stem}.tex", "--fix-fonts"], work)
        command([sys.executable, str(ROOT / "scripts" / "word_guard.py"), f"{stem}.docx",
                 "--tex", f"{stem}.tex", "--json"], work)
        command([sys.executable, str(ROOT / "scripts" / "latex_guard.py"), f"{stem}.tex", "--json"], work)
        output.mkdir(parents=True, exist_ok=True)
        for filename in (f"{stem}.tex", f"{stem}.pdf", f"{stem}.docx", f"{stem}.txt", "preview.png"):
            shutil.copyfile(work / filename, output / filename)
        if bibliography.exists() and output.resolve() != source.resolve():
            shutil.copyfile(bibliography, output / "references.bib")
    return {"example": name, "pages": pages, "pdf_text_characters": len(text),
            "latex_guard": "pass", "word_guard": "pass", "unresolved_references": False,
            "overfull_boxes": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="Explicit output root; use examples to refresh the public artifacts")
    parser.add_argument("--example", choices=tuple(SAMPLES), action="append")
    args = parser.parse_args()
    missing = [name for name in ("pandoc", "pdflatex", "bibtex", "pdftotext", "pdftoppm", "pdfinfo")
               if not shutil.which(name)]
    if missing:
        parser.error("Required tools missing: " + ", ".join(missing))
    try:
        results = [render(name, args.output_dir / name) for name in (args.example or SAMPLES)]
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Example render failed: {exc}\n")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
