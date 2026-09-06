#!/usr/bin/env python3
"""Compile five audited generic tables in two layouts using synthetic render data.

Offline, source-only fixtures. No manuscript input or automatic TeX installation.
Requires an existing TeX/Poppler toolchain; this is not an OS sandbox.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from render_examples import command

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from writing_guide import load_index, table_resource

LAYOUTS = ("single-column", "two-column-wide")


def fixture(latex: str, layout: str) -> str:
    if layout not in LAYOUTS:
        raise ValueError("Unknown fixture layout")
    # Fixed synthetic values exercise typesetting only, never manuscript results.
    values = {
        "SL_CAPTION": "Synthetic comparison", "SL_PROTOCOL": "a synthetic protocol",
        "SL_LABEL": "fixture", "SL_AGGREGATE": "synthetic means", "SL_N": "3",
        "SL_RUN_UNIT": "synthetic trials", "SL_UNCERTAINTY": "synthetic standard deviations",
        "SL_METHOD": "Fixture C", "SL_BASELINE": "Fixture A", "SL_BASELINE_A": "Fixture A",
        "SL_BASELINE_B": "Fixture B", "SL_METRIC": "Score", "SL_QUALITY": "Score",
        "SL_METRIC_A": "Score", "SL_METRIC_B": "Error", "SL_METRIC_C": "Rate",
        "SL_COMPONENT_A": "Part A", "SL_COMPONENT_B": "Part B", "SL_DESIGN_CHOICES": "two components",
        "SL_HARDWARE": "synthetic hardware", "SL_PRECISION": "FP32", "SL_BATCH": "1",
        "SL_INPUT": "a fixed input", "SL_MEASUREMENT_PROTOCOL": "a synthetic measurement protocol",
        "SL_SHIFT_AXIS": "synthetic scene shifts", "SL_HELD_OUT_UNIT": "Each synthetic scene",
        "SL_SHIFT_A": "Shift A", "SL_SHIFT_B": "Shift B", "SL_LEVEL_A": "Low", "SL_LEVEL_B": "High",
        "SL_PARAMETER": "Width", "SL_SELECTION_SET": "a synthetic validation set",
        "SL_MATCHED_CONFIGURATION": "a fixed synthetic configuration", "SL_RESOURCE": "Cost",
        "SL_UNIT": "items", "SL_NOTE": "Fixture note",
    }
    numeric_tokens = ("SL_BUDGET_A", "SL_BUDGET_B", "SL_BUDGET_OURS", "SL_COST", "SL_DATA_A",
                      "SL_DATA_B", "SL_DATA_OURS", "SL_DELTA", "SL_GAP", "SL_RESULT", "SL_VALUE",
                      "SL_VALUE_A", "SL_VALUE_B", "SL_VALUE_C", "SL_VALUE_D")
    values.update({token: "0.50" for token in numeric_tokens})
    unknown = set(re.findall(r"SL_[A-Z_]+", latex)) - values.keys()
    if unknown:
        raise ValueError("Unknown fixture placeholders: " + ", ".join(sorted(unknown)))
    latex = re.sub(r"SL_[A-Z_]+", lambda match: values[match[0]], latex)
    latex = latex.replace(r"\caption{", r"\caption{SYNTHETIC RENDER FIXTURE (not measured results). ", 1)
    if layout == "two-column-wide":
        latex = latex.replace(r"\begin{table}", r"\begin{table*}").replace(r"\end{table}", r"\end{table*}")
    options = "10pt,letterpaper" + (",twocolumn" if layout == "two-column-wide" else "")
    return (f"\\documentclass[{options}]{{article}}\n"
            "\\usepackage[margin=23mm]{geometry}\n\\usepackage{booktabs}\n"
            "\\begin{document}\n" + latex + "\n\\end{document}\n")


def verify(template: dict, layout: str, output: Path | None) -> dict:
    resource = table_resource(template)
    source = fixture(resource["latex"], layout)
    with tempfile.TemporaryDirectory(prefix="writer-table-") as temporary:
        work = Path(temporary)
        (work / "main.tex").write_text(source, encoding="utf-8")
        args = ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        command(args, work)
        command(args, work)
        log = (work / "main.log").read_text(encoding="utf-8", errors="replace")
        if re.search(r"Overfull \\[hv]box|There were undefined|(?:Citation|Reference) .* undefined", log):
            raise ValueError(f"{template['id']}/{layout}: overflow or unresolved reference\n{log[-5000:]}")
        command(["pdftotext", "-layout", "main.pdf", "main.txt"], work)
        text = (work / "main.txt").read_text(encoding="utf-8")
        if "SYNTHETIC RENDER FIXTURE" not in text or "0.50" not in text or "SL_" in text or "??" in text:
            raise ValueError("Missing fixture content or unresolved placeholder")
        layout_report = json.loads(command([sys.executable, str(ROOT / "scripts/pdf_layout_check.py"),
                                            "main.pdf", "--log", "main.log", "--max-pages", "1"], work))
        if output:
            output.mkdir(parents=True, exist_ok=True)
            command(["pdftoppm", "-f", "1", "-singlefile", "-scale-to", "1400", "-png", "main.pdf", "preview"], work)
            for filename in ("main.tex", "main.pdf", "main.txt", "preview.png"):
                shutil.copyfile(work / filename, output / filename)
        return {"table": template["id"], "layout": layout, "sha256": template["sha256"],
                "synthetic_data_only": True, "overfull_boxes": False, "pdf_layout": layout_report}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    missing = [name for name in ("pdflatex", "pdftotext", "pdffonts", "pdfinfo", "pdftoppm") if not shutil.which(name)]
    if missing:
        parser.error("Required tools missing: " + ", ".join(missing))
    results = []
    try:
        for template in load_index()["tables"]:
            for layout in LAYOUTS:
                name = template["id"] + "-" + layout
                results.append(verify(template, layout, args.output_dir / name if args.output_dir else None))
                print("PASS " + name, file=sys.stderr)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Table check failed: {exc}\n")
    report = json.dumps({"scope": "Synthetic generic-table fixtures, not official venue compliance", "results": results}, indent=2) + "\n"
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "report.json").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
