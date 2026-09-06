#!/usr/bin/env python3
"""Read one complete evidence-conditioned writing protocol offline; never draft or compile."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REFERENCES = Path(__file__).resolve().parents[1] / "references"
TABLE_FILES = {"main_results.tex", "ablation.tex", "generalization.tex", "efficiency.tex", "sensitivity.tex"}
APPLICATION_CONTRACT = [
    "Check each move against author-supplied evidence: present, missing, or not applicable. "
    "Required means inspect when applicable, not invent a paragraph, experiment, weakness, or result.",
    "For missing essential evidence, ask the minimum question or narrow the draft; keep placeholders explicit. "
    "Do not silently fill inputs from the example structure or assume an experiment was run.",
    "Choose one suitable variant and adapt its order to the contribution. These are not mandatory paragraph counts. "
    "A theory paper need not invent empirical evidence; a rebuttal need not concede an unsupported criticism.",
    "Preserve verified numbers, units, denominators, conditions, uncertainty, negation, and claim scope. "
    "Check citation support and manuscript locations separately.",
    "Table cells remain placeholders until verified. Check the current official venue style separately; "
    "these generic structures do not establish compliance, scientific quality, or acceptance.",
    "Available card IDs can be queried with writing_lookup.py --id. Unbundled IDs are external catalog "
    "pointers only; do not invent their content or fetch them implicitly.",
]


def read_bounded(path: Path, maximum: int) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Expected a regular bundled file: {path.name}")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    if len(raw) > maximum:
        raise ValueError(f"Bundled resource exceeds size limit: {path.name}")
    return raw


def load_index(references: Path = REFERENCES) -> dict:
    index = json.loads(read_bounded(references / "writing-protocols.json", 2 * 1024 * 1024))
    if index["schema_version"] != 1 or not isinstance(index["guides"], list):
        raise ValueError("Unsupported protocol index")
    ids = [guide["id"] for guide in index["guides"]]
    if len(ids) != len(set(ids)) or "review" in ids:
        raise ValueError("Invalid writer protocol inventory")
    return index


def table_resource(template: dict, references: Path = REFERENCES) -> dict:
    filename = template["file"]
    if filename not in TABLE_FILES:
        raise ValueError("Table filename is not allowlisted")
    directory = references / "table-templates"
    if directory.is_symlink():
        raise ValueError("Table directory must not be a symlink")
    raw = read_bounded(directory / filename, 64 * 1024)
    if hashlib.sha256(raw).hexdigest() != template["sha256"]:
        raise ValueError(f"Table digest mismatch: {filename}")
    return {**template, "latex": raw.decode("utf-8")}


def report_for(index: dict, selector: str | None, variant: str | None,
               references: Path = REFERENCES) -> dict:
    base = {"scope": index["scope"], "upstream_commit": index["upstream"]["commit"]}
    tables = {table["guide_id"]: table for table in index["tables"]}
    if selector is None:
        return {**base, "guides": [
            {"id": g["id"], "label": g["label"], "variants": [t["id"] for t in g["templates"]],
             "table_file": tables[g["id"]]["file"] if g["id"] in tables else None}
            for g in index["guides"]]}
    matches = [g for g in index["guides"] if selector.casefold() in
               {name.casefold() for name in (g["id"], *g["aliases"])}]
    if len(matches) != 1:
        raise ValueError("Unknown or ambiguous writer protocol; use --list (peer review is out of scope)")
    guide = dict(matches[0])
    if variant is not None:
        guide["templates"] = [t for t in guide["templates"] if t["id"] == variant]
        if len(guide["templates"]) != 1:
            raise ValueError("Unknown variant for this protocol; use --list")
    available = set(index["available_card_ids"])
    related = guide["related_entry_ids"]
    return {**base, "application_contract": APPLICATION_CONTRACT, "guide": guide,
            "available_card_ids": [entry for entry in related if entry in available],
            "unbundled_card_ids": [entry for entry in related if entry not in available],
            "table": table_resource(tables[guide["id"]], references) if guide["id"] in tables else None}


def render(report: dict, output_format: str) -> str:
    if output_format == "json":
        return json.dumps(report, ensure_ascii=False, indent=2)
    chunks = [report["scope"], "Upstream: " + report["upstream_commit"]]
    if "guides" in report:
        for guide in report["guides"]:
            chunks.append(f"- {guide['id']}: {guide['label']}\n  Variants: " + ", ".join(guide["variants"])
                          + (f"\n  Table: {guide['table_file']}" if guide["table_file"] else ""))
        return "\n\n".join(chunks)
    guide = report["guide"]

    def bullets(title: str, values: list[str]) -> None:
        chunks.append("## " + title + "\n\n" + "\n".join("- " + value for value in values))

    bullets("Application Contract", report["application_contract"])
    chunks.append(f"# {guide['label']}\n\n{guide['purpose']}\n\nUse when: {guide['use_when']}")
    bullets("Inputs", guide["inputs"])
    for move in guide["moves"]:
        status = "check when applicable" if move["required"] else "optional"
        bullets(f"{move['label']} ({status})", move["checks"])
    for template in guide["templates"]:
        chunks.append(f"## Variant: {template['id']} ({template['name']})\n\nWhen: {template['when']}\n\n"
                      + "\n".join(f"{number}. {step}" for number, step in enumerate(template["sequence"], 1)))
    for overlay in guide.get("domain_overlays", []):
        bullets("Domain: " + overlay["label"], overlay["checks"])
    bullets("Avoid", guide["avoid"])
    bullets("Verification", guide["verification"])
    bullets("Available Card IDs", report["available_card_ids"])
    bullets("Unbundled Card IDs (pointers only)", report["unbundled_card_ids"])
    if report["table"]:
        table = report["table"]
        chunks.append(f"## Table: {table['file']}\n\nLicense: {table['license']}; requires: "
                      + ", ".join(table["requires"]) + f"\n\n{table['adaptation']}\n\n```latex\n{table['latex']}```")
    return "\n\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selector", nargs="?", help="One protocol ID or exact English/Chinese alias")
    parser.add_argument("--list", action="store_true", help="List protocol IDs and variants, not full contents")
    parser.add_argument("--variant", help="Select one structure; all evidence checks remain included")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--max-chars", type=int, default=16000)
    args = parser.parse_args()
    if (args.list and (args.selector is not None or args.variant is not None)) or (not args.list and args.selector is None):
        parser.error("Supply one selector or --list, not both; --variant requires a selector")
    if args.selector is not None and not 1 <= len(args.selector.strip()) <= 256:
        parser.error("A selector must contain 1..256 characters, not an entire manuscript")
    if not 512 <= args.max_chars <= 50000:
        parser.error("--max-chars must be 512..50000")
    try:
        report = report_for(load_index(), args.selector.strip() if args.selector is not None else None, args.variant)
        output = render(report, args.format)
        if len(output) + 1 > args.max_chars:
            raise ValueError("No complete protocol fits; increase --max-chars or choose one --variant. "
                             "Evidence checks are never truncated.")
        print(output)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Protocol lookup failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
