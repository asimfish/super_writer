#!/usr/bin/env python3
"""Run a portable smoke test for PaperSpine gate scripts.

The test builds a synthetic PaperSpine output directory in a temporary folder
and invokes the public script CLIs through subprocess. It is intentionally
standard-library only and does not require the ASBS validation sample.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


@dataclass
class CaseResult:
    name: str
    command: list[str]
    returncode: int
    ok: bool
    stdout: str
    stderr: str
    check_error: str = ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def run_case(
    name: str,
    script_name: str,
    args: list[str],
    must_contain: list[str] | None = None,
    json_check: Callable[[object], str | None] | None = None,
    timeout: int = 30,
    expect_returncode: int = 0,
) -> CaseResult:
    command = [sys.executable, str(SCRIPT_DIR / script_name), *args]
    proc = subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    combined = proc.stdout + proc.stderr
    missing = [item for item in (must_contain or []) if item not in combined]
    check_error = ""
    if missing:
        check_error = "missing output: " + ", ".join(missing)
    if json_check and proc.returncode == expect_returncode and not check_error:
        try:
            check_error = json_check(json.loads(proc.stdout)) or ""
        except json.JSONDecodeError as exc:
            check_error = f"invalid JSON output: {exc}"
    ok = proc.returncode == expect_returncode and not check_error
    return CaseResult(name, command, proc.returncode, ok, proc.stdout, proc.stderr, check_error)


def check_artifact(data: object) -> str | None:
    if not isinstance(data, dict):
        return "artifact output is not an object"
    if data.get("missing"):
        return f"artifact check has missing files: {data.get('missing')}"
    if data.get("content_issues"):
        return f"artifact check has content issues: {data.get('content_issues')}"
    return None


def check_citation_bank(data: object) -> str | None:
    if not isinstance(data, dict):
        return "citation bank output is not an object"
    if data.get("ok") is not True:
        return f"citation bank not ok: {data.get('findings')}"
    if data.get("row_count") != 6 or data.get("recent_count") != 6:
        return "citation bank fixture row counts changed"
    if data.get("findings"):
        return f"citation bank findings present: {data.get('findings')}"
    return None


def check_citation_quality(data: object) -> str | None:
    if not isinstance(data, dict):
        return "citation quality output is not an object"
    if data.get("verified") != 6 or data.get("dead") != 0:
        return "citation quality verified/dead counts changed"
    if data.get("failures"):
        return f"citation quality failures present: {data.get('failures')}"
    return None


def check_integrity(data: object) -> str | None:
    if not isinstance(data, dict):
        return "integrity output is not an object"
    if data.get("blocked") is not False:
        return "integrity audit is blocked"
    dimensions = data.get("dimensions")
    if not isinstance(dimensions, list):
        return "integrity dimensions missing"
    statuses = {item.get("name"): item.get("status") for item in dimensions if isinstance(item, dict)}
    bad = {name: status for name, status in statuses.items() if status != "CLEAN"}
    if bad:
        return f"integrity dimensions are not clean: {bad}"
    return None


def check_empty_list(data: object) -> str | None:
    if data != []:
        return f"expected empty list, got {data!r}"
    return None


def check_style(data: object) -> str | None:
    if not isinstance(data, dict) or not data.get("documents"):
        return "style metrics documents missing"
    if not data.get("sections"):
        return "style metrics sections missing"
    return None


def check_revision(data: object) -> str | None:
    if not isinstance(data, dict):
        return "revision output is not an object"
    summary = data.get("summary")
    if not isinstance(summary, dict):
        return "revision summary missing"
    if summary.get("shallow_warning") is not True:
        return "revision fixture no longer exercises the shallow-rewrite warning"
    if summary.get("near_identical_ratio", 0) < 0.9:
        return "revision fixture near-identical ratio unexpectedly low"
    return None


def check_dispatch(data: object) -> str | None:
    if not isinstance(data, dict):
        return "dispatch output is not an object"
    if data.get("status") != "dispatched":
        return f"unexpected dispatch status: {data.get('status')!r}"
    files = data.get("files")
    if not isinstance(files, list) or len(files) != 3:
        return "dispatch did not produce three reviewer prompts"
    return None


def check_independence(data: object) -> str | None:
    if not isinstance(data, dict):
        return "independence output is not an object"
    if data.get("ok") is not True:
        return f"independence validation failed: {data.get('findings')}"
    if float(data.get("independence_score") or 0) < 0.7:
        return f"independence score too low: {data.get('independence_score')}"
    return None


def support_sentence(index: int) -> str:
    return (
        f"Synthetic citation {index} supports the smoke-test claim with a stable "
        "arXiv locator, a concrete task sentence, and enough detail for the "
        "citation-bank validators to treat the row as usable evidence."
    )


def citation_bank() -> str:
    rows = [
        "| Candidate ID | Reference/BibTeX | Year | Recency | Supports Section | Support Claim Sentence | Why This Paper Fits | Source | Source Channel | Verified | Verification note |",
        "|---|---|---:|---|---|---|---|---|---|---|---|",
    ]
    for index in range(1, 7):
        year = 2026 if index <= 3 else 2025
        rows.append(
            f"| C{index} | Synthetic Author {index}, \"Synthetic Bridge Study {index}\", arXiv:25{index:02d}.0{index:04d}, {year} | "
            f"{year} | recent | Introduction | {support_sentence(index)} | "
            "It exercises the arXiv locator path without requiring network DOI checks. | synthetic fixture | local | yes | arXiv locator format verified by fixture |"
        )
    return "\n".join(rows)


def confirmed_contribution() -> str:
    return """# Confirmed Contribution

## Core Contribution

| Field | Content |
|---|---|
| Main contribution statement | We show that the PaperSpine smoke fixture validates every audit script against a controlled synthetic manuscript. |
| Contribution type | validation fixture |
| One-sentence reviewer payoff | Maintainers can trust script upgrades because the fixture exercises every gate end to end. |

## Why This Contribution Is Needed

| Field | Content |
|---|---|
| Field problem | Script regressions in the paper pipeline are hard to catch without a deterministic end-to-end fixture. |
| Specific gap | No prior fixture covered the V4 contribution gate together with the citation and review gates. |
| Concrete challenge | The fixture must satisfy every validator simultaneously while staying fully synthetic. |
| Why prior work leaves it unresolved | Earlier smoke fixtures predate the Contribution-First gate and never wrote this artifact. |

## How This Paper Responds

| Field | Content |
|---|---|
| Design response | A synthetic contribution declaration is generated alongside the manuscript so every stage dependency holds. |
| Evidence required | The smoke test must pass artifact, citation, integrity, and review checks in one run. |
| Evidence available | The smoke test run log reports all cases passing against this fixture. |
| Evidence missing | None remaining for the fixture scope; real-paper behavior is explicitly out of scope. |

## Claim Boundary

| Field | Content |
|---|---|
| Strong claims allowed | The fixture fully exercises the script gates that run in the smoke test. |
| Claims to soften or avoid | No claim is made about real manuscript quality; the fixture is synthetic by design. |
| Novelty risk | A reviewer may note the fixture mirrors upstream test data; we differentiate on end-to-end coverage. |
| Significance risk | A reviewer may call the scope narrow; we answer that gate coverage is the stated goal. |
"""


def rationale_row(unit: str, extra: str = "") -> str:
    row_id, unit_name = unit.split(" ", 1)
    cells = [
        row_id,
        unit_name,
        (
            "Defines a concrete writing function for this smoke-test manuscript "
            "unit while keeping the section aligned with the confirmed motivation."
        ),
        (
            "Motivation link: the confirmed motivation asks whether a constrained "
            "guided bridge sampler can improve robustness without broad claims; "
            "this unit narrows the argument to an evidence-backed reliability claim."
        ),
        (
            "Reference/SOTA pattern: recent diffusion policy and benchmark papers "
            "frame the problem by contrasting brittle behavior with concrete task "
            "evidence; this row borrows that pattern and names what changes."
        ),
        (
            "Target scene or venue norm: a conference paper must state the claim "
            "early, separate method assumptions from results, and avoid unsupported "
            "generality in the introduction and conclusion."
        ),
        (
            "Evidence or citation anchor: the fixture evidence bank, Table 1, and "
            "citation bank C1-C6 anchor the sentence-level claims and prevent the "
            "unit from inventing results."
        ),
        (
            "Planned change or text move: place the claim, then the method move, "
            "then the check against evidence so the reader can audit the argument "
            "from motivation through support."
        ),
        (
            "PASS - final paragraph includes motivation, reference pattern, "
            "target-scene norm, evidence or citation, and a specific planned "
            f"text move. {extra}"
        ),
    ]
    return "| " + " | ".join(cells) + " |"


def writing_rationale_matrix() -> str:
    rows = [
        "# Writing Rationale Matrix",
        "",
        "| Row ID | Manuscript Unit | Current/Planned Function | Motivation Link | Reference/SOTA Pattern Learned | Target Scene or Venue Norm | User Evidence or Citation Anchor | Planned Change | Final Text Check |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    units = [
        "1 whole-paper framework and structure",
        "2 abstract problem sentence",
        "3 introduction gap paragraph",
        "4 method overview paragraph",
        "5 experiment setup paragraph",
        "6 result interpretation paragraph",
        "7 limitation paragraph",
        "8 conclusion paragraph",
    ]
    for unit in units:
        rows.append(rationale_row(unit, "Framework row links every later unit to the same spine." if unit.startswith("1 ") else ""))
    return "\n".join(rows)


def tex_source() -> str:
    return r"""
\documentclass{article}
\begin{document}
\icmltitle{Synthetic PaperSpine Smoke Manuscript}
\author{PaperSpine Fixture}
\section{Introduction}
This synthetic manuscript states a narrow motivation about testing a guided bridge sampler under controlled robustness checks. The introduction cites a durable fixture reference, references Table~\ref{tab:included_results}, and avoids claims beyond the available evidence \cite{synthetic2025a}.

\section{Method}
The method section describes the smoke-test algorithm, its assumptions, and the evidence hooks used by the audit scripts. It contains enough prose for section extraction while remaining independent of any real research claim.

\section{Experiments}
\input{sections/results}

\section{Conclusion}
The conclusion returns to the narrow motivation and states that the smoke-test manuscript is only a validation artifact for PaperSpine script behavior.
\end{document}
"""


def included_results_source() -> str:
    return r"""
The experiment section reports fixture-only observations from Table 1 and states that the evidence bank is the authority for any result sentence. No statistical significance claim is made here.

\begin{table}
\caption{Synthetic included result table}
\label{tab:included_results}
\end{table}
"""


def bib_source() -> str:
    return r"""
@article{synthetic2025a,
  title={Synthetic Bridge Study for PaperSpine Smoke Tests},
  author={Fixture, PaperSpine},
  journal={Synthetic Proceedings},
  year={2025}
}
"""


def review_output(role: str) -> str:
    if role == "methods":
        return (
            "Methods & Reproducibility Reviewer\n\n"
            "supported evidence_status: supported. The protocol describes assumptions, "
            "replication hooks, and controlled fixture evidence. The review focuses on "
            "algorithmic detail, ablation readiness, and repeatable setup commands."
        )
    if role == "contribution":
        return (
            "Contribution & Novelty Reviewer\n\n"
            "supported evidence_status: supported. The contribution is scoped as a "
            "validation fixture, not a research breakthrough. The assessment focuses on "
            "claim boundaries, novelty wording, and alignment with the stated venue norm."
        )
    return (
        "Structure & Clarity Reviewer\n\n"
        "supported evidence_status: supported. The narrative moves from motivation to "
        "method to evidence to conclusion. The assessment focuses on paragraph order, "
        "transitions, reader orientation, and whether the story remains auditable."
    )


def build_fixture(root: Path) -> tuple[Path, Path, Path]:
    out = root / "paper_rewriting_output"
    materials = root / "materials"
    final_paper = out / "final_paper"

    config = {
        "workflow": "rewrite_existing",
        "scene": "conference",
        "tier": "flash",
        "output_language": "en",
        "target_name": "SmokeConf 2027",
        "citation_target_count": 2,
        "translation_package": "none",
        "word_output": "none",
        "special_requirements": [
            "preserve Method and Experiments sections unchanged when rewriting"
        ],
    }

    write(out / "paper_spine_config.json", json.dumps(config, indent=2))
    write(out / "paper_spine_config.md", "# PaperSpine Config\n\nSynthetic smoke-test configuration.")
    write(out / "source_map.md", "# Source Map\n\nSynthetic fixture sources are local and controlled.")
    write(out / "research_dossier.md", "# Research Dossier\n\nConference norms require narrow claims, recency, and evidence-backed positioning.")
    write(out / "exemplar_learning_dossier.md", "# Exemplar Learning Dossier\n\nExamples teach scoped motivation, method clarity, and restrained claims.")
    write(out / "style_profile.md", "# Style Profile\n\nUse concise academic prose with explicit evidence hooks.")
    write(out / "sota_gap_map.md", "# SOTA Gap Map\n\nSynthetic SOTA gap is narrow robustness under controlled guidance.")
    write(out / "motivation_options_after_research.md", "# Motivation Options\n\nOption A was selected after research.")
    write(out / "confirmed_motivation.md", "# Confirmed Motivation\n\nUser confirmed a narrow robustness-focused motivation.")
    write(out / "confirmed_contribution.md", confirmed_contribution())
    write(out / "section_blueprints.md", "# Section Blueprints\n\nIntroduction, Method, Experiments, and Conclusion are ordered by the motivation spine.")
    write(out / "writing_rationale_matrix.md", writing_rationale_matrix())
    write(out / "citation_support_bank.md", citation_bank())
    write(out / "original_logic_map.md", "# Original Logic Map\n\nThe original draft is mapped to motivation, method, evidence, and conclusion units.")
    write(
        out / "evidence_bank.md",
        "# Evidence Bank\n\n"
        "Table 1 reports fixture robustness observations for the synthetic guided "
        "bridge sampler. Evidence item E1 anchors the introduction claim, E2 "
        "anchors the method assumption sentence, and E3 anchors the experiment "
        "interpretation sentence. Result claims remain synthetic and traceable "
        "to this controlled evidence bank, which is intentionally detailed enough "
        "for audit scripts to treat it as substantive support rather than a "
        "placeholder. No unsupported statistical or benchmark claims are made.",
    )
    write(out / "rewrite_matrix.md", "# Rewrite Matrix\n\nThe rewrite preserves method and experiment facts while changing framing and paragraph order.")
    write(out / "logic_transfer_audit.md", "# Logic Transfer Audit\n\nAll fixture claims transfer from original evidence to final manuscript without unsupported additions.")
    write(out / "latex_report.md", "# LaTeX Report\n\nmain.tex was assembled for smoke testing.")
    write(out / "final_artifact_manifest.md", "# Final Artifact Manifest\n\n- final_paper/main.tex")
    write(final_paper / "main.tex", tex_source())
    write(final_paper / "sections" / "results.tex", included_results_source())
    write(final_paper / "references.bib", bib_source())

    write(materials / "draft.md", "# Draft\n\nSynthetic draft material for inventory.")
    write(materials / "result_table.csv", "metric,value\nsuccess,1.0\n")
    write(materials / "method_notes.txt", "Synthetic method setup and protocol notes.")
    write(materials / "reference_seed.md", "# Reference Seed\n\nLocal reference seed for source indexing.")

    original = root / "original.md"
    revised = root / "revised.md"
    original_text = (
        "The original method paragraph should be preserved because the brief says "
        "method and experiment facts must remain unchanged during rewriting.\n\n"
        "The original experiment paragraph should be preserved because the smoke "
        "test exercises preserve-mode behavior in revision audit."
    )
    write(original, original_text)
    write(revised, original_text)
    return out, materials, original


def prepare_review_outputs(out: Path) -> None:
    prompts = out / "review_prompts"
    write(prompts / "methods_review_output.md", review_output("methods"))
    write(prompts / "contribution_review_output.md", review_output("contribution"))
    write(prompts / "clarity_review_output.md", review_output("clarity"))


def tail(text: str, limit: int = 900) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[-limit:]


def print_result(result: CaseResult, verbose: bool) -> None:
    status = "PASS" if result.ok else "FAIL"
    print(f"[{status}] {result.name}")
    if verbose or not result.ok:
        print("  cmd:", " ".join(result.command))
        print("  exit:", result.returncode)
        if result.check_error:
            print("  check:", result.check_error)
        if result.stdout.strip():
            print("  stdout:", tail(result.stdout).replace("\n", "\n    "))
        if result.stderr.strip():
            print("  stderr:", tail(result.stderr).replace("\n", "\n    "))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run PaperSpine synthetic smoke tests.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep the generated fixture directory.")
    parser.add_argument("--verbose", action="store_true", help="Print stdout/stderr for passing cases.")
    args = parser.parse_args(argv)

    temp = tempfile.mkdtemp(prefix="paperspine-smoke-")
    root = Path(temp)
    results: list[CaseResult] = []
    try:
        out, materials, original = build_fixture(root)
        revised = root / "revised.md"
        main_tex = out / "final_paper" / "main.tex"
        bib = out / "final_paper" / "references.bib"

        results.append(run_case("material inventory", "material_inventory.py", [str(materials), "--output-dir", str(out), "--json"]))
        results.append(run_case("reference inventory", "reference_inventory.py", [str(materials), "--output-dir", str(out), "--json"]))
        results.append(run_case("artifact check", "artifact_check.py", [str(out), "--pdf-policy", "never", "--word-policy", "never", "--json"], json_check=check_artifact))
        results.append(run_case("citation bank target count", "citation_bank_check.py", [str(out / "citation_support_bank.md"), "--target-count", "2", "--json"], json_check=check_citation_bank))
        results.append(run_case("citation quality arxiv locator", "citation_quality_audit.py", [str(out), "--no-api", "--json"], json_check=check_citation_quality))
        results.append(run_case("integrity audit", "integrity_audit.py", [str(out), "--json"], json_check=check_integrity))
        results.append(run_case("latex guard", "latex_guard.py", [str(main_tex), "--bib", str(bib), "--json"], json_check=check_empty_list))
        results.append(run_case("style metrics", "style_metrics.py", [str(main_tex), "--json"], json_check=check_style))
        # V4 revision_audit exits 1 when the rewrite is too shallow — the fixture intentionally triggers it
        results.append(run_case("revision audit shallow warning", "revision_audit.py", [str(original), str(revised), "--json"], json_check=check_revision, expect_returncode=1))
        results.append(run_case("structured review dispatch", "structured_review.py", [str(out), "--dispatch", "--json"], json_check=check_dispatch))
        prepare_review_outputs(out)
        results.append(run_case("structured review independence", "structured_review.py", [str(out), "--validate", str(out / "review_prompts"), "--json"], json_check=check_independence))

        failed = [result for result in results if not result.ok]
        for result in results:
            print_result(result, args.verbose)
        if args.keep_temp:
            print(f"\nFixture: {root}")
        else:
            print("\nFixture: cleaned")
        print(f"Cases: {len(results)} passed, {len(failed)} failed")
        if failed:
            return 1
        return 0
    finally:
        if args.keep_temp:
            print(f"Kept fixture directory: {root}")
        else:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
