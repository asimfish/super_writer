#!/usr/bin/env python3
"""Explicitly refresh reviewed writing data and tables from pinned upstream bytes.

Source-only maintenance tool. Never executes upstream code or fetches papers.
The installed lookup is offline. Generated records retain upstream IDs unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "5a5c55c0e553fc11c6b2886a5fa1a3f6094108a7"
BASE = f"https://raw.githubusercontent.com/asimfish/super_library/{COMMIT}/"
PINS = {
    "skills/super-library/references/index.json": "721e48a4ae4a9b401b1e9346b12c764bd02863f3bf4782c7bc1249871693469d",
    "library/compact_ids.json": "f04c60c98709db37de08f2a20f1b284ec5a70fd3c68dd4159ed3da32dea74862",
    "DATA_LICENSE": "858aa43d09445eb1ae9b8aaede251569d3431d5e2bf40410794913b1a0f19648",
    "LICENSE": "9e53589d75a510a23d6f238d68b23072bdb906a3e0365e48188edff24ccc12c5",
    "templates/tables/main_results.tex": "e52794d8871d0b5e09852445028e06b3e0f447bf45047dc0742406fcdc066c57",
    "templates/tables/ablation.tex": "25139df9bc9716fcda03d8bd2633b7b9cd6a6134b6412d50897755f33180b228",
    "templates/tables/generalization.tex": "2244faa3cbbf7e0f03bc479ab3911caa99e4062f54871f2437ed0bf08ed02193",
    "templates/tables/efficiency.tex": "8051b01c5c65e3d17591fe5e66ba4f429fa977aa544cc9d08b7b2ce48396077f",
    "templates/tables/sensitivity.tex": "2f76bf8fdbf6c45c99dd8a43be49d76ba288834a437ef1448fe2f6fa2954c2a8",
}


def fetch(path: str) -> bytes:
    with urllib.request.urlopen(BASE + path, timeout=45) as response:
        data = response.read(2 * 1024 * 1024 + 1)
    if hashlib.sha256(data).hexdigest() != PINS[path]:
        raise ValueError(f"Upstream digest mismatch: {path}; audit the change before updating")
    return data


def curate(index: dict, compact: list[str]) -> dict:
    wanted = set(compact)
    entries = [entry for entry in index["entries"]
               if (entry["id"] in wanted or entry["id"].startswith(("general.", "vla."))
                   or entry["kind"] == "sentence_pattern")
               and entry["provenance"]["type"] != "attested_collocation"
               and entry["quality"]["status"] in {"reviewed", "source_checked"}]
    entries.sort(key=lambda entry: entry["id"])
    source_ids = {sid for entry in entries for sid in entry["source_ids"]}
    sources = [{key: source[key] for key in ("id", "title", "url", "year", "venue") if key in source}
               for source in index["sources"] if source["id"] in source_ids]
    if source_ids != {source["id"] for source in sources}:
        raise ValueError("Selected cards have unresolved source IDs")
    if len(entries) != len({entry["id"] for entry in entries}):
        raise ValueError("Duplicate selected card ID")
    return {"schema_version": 1, "license": "CC0-1.0 (original records only)",
            "upstream": {"repository": "https://github.com/asimfish/super_library", "commit": COMMIT,
                         "input_sha256": PINS, "selection": "reviewed/source_checked compact IDs plus general.*, vla.*, and all sentence_pattern cards, excluding attested collocations"},
            "scope": "Language discovery, not evidence for manuscript claims; linked works retain their own rights.",
            "taxonomy": index["taxonomy"], "aliases": index["aliases"], "entries": entries,
            "sources": sorted(sources, key=lambda source: source["id"])}


def adapt_table(data: bytes) -> bytes:
    text = data.decode("utf-8")
    headers = {
        "Data / pretraining": r"\shortstack{Data /\\pretraining}",
        "Compute / interaction": r"\shortstack{Compute /\\interaction}",
        "Change from full model": r"\shortstack{Change from\\full model}",
        "Evaluation condition": r"\shortstack{Evaluation\\condition}",
        "Gap from reference": r"\shortstack{Gap from\\reference}",
        "Training / interaction cost": r"\shortstack{Training /\\interaction cost}",
        r"Throughput (SL_UNIT) $\uparrow$": r"\shortstack{Throughput\\(SL_UNIT) $\uparrow$}",
        r"Peak memory (GB) $\downarrow$": r"\shortstack{Peak memory\\(GB) $\downarrow$}",
    }
    for old, new in headers.items():
        text = text.replace(old, new)
    text = text.replace("\\vspace{2pt}\n", "")
    prefix = ("% Adapted from Super Library (MIT); see LICENSE in this directory.\n"
              "% Generic table skeleton, not an official venue template.\n"
              "% Replace SL_* from verified author data before compiling; never invent values.\n"
              "% Wrap headers and remove manual vertical spacing; official styles take precedence.\n")
    return ("\n".join(line.rstrip() for line in (prefix + text).splitlines()) + "\n").encode("utf-8")


def curate_protocols(index: dict, cards: dict, tables: dict[str, bytes]) -> dict:
    guides = [g for g in index["writing_guides"]["guides"] if g["id"] != "review"]
    if len(guides) != 16 or len({g["id"] for g in guides}) != 16:
        raise ValueError("Protocol inventory changed; review the selection")
    if sum(len(g["templates"]) for g in guides) != 30:
        raise ValueError("Protocol variants changed; review before importing")
    selected_tables = []
    for template in index["table_templates"]["templates"]:
        filename = template["file"]
        if not re.fullmatch(r"[a-z_]+\.tex", filename):
            raise ValueError("Only flat table filenames may be imported")
        source = "templates/tables/" + filename
        if source not in PINS or filename not in tables:
            raise ValueError("Unpinned table template")
        selected_tables.append({**template, "sha256": hashlib.sha256(tables[filename]).hexdigest(),
                                "upstream_path": source, "upstream_sha256": PINS[source],
                                "license": "MIT", "adaptation": "Wrapped long headers; removed manual vertical spacing."})
    if len(selected_tables) != 5 or len({t["file"] for t in selected_tables}) != 5:
        raise ValueError("Table inventory changed; review before importing")
    return {"schema_version": 1, "license": "CC0-1.0 (original protocol records); MIT (table source)",
            "scope": "Evidence-conditioned writing structures, not official venue rules or evidence for claims.",
            "upstream": {"repository": "https://github.com/asimfish/super_library", "commit": COMMIT,
                         "input_sha256": PINS, "selection": "All writer-facing protocols; review excluded."},
            "available_card_ids": [entry["id"] for entry in cards["entries"]],
            "guides": guides, "tables": selected_tables}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Replace owned generated writing resources and licenses")
    mode.add_argument("--check", action="store_true", help="Download pins and verify reproducible output without writing")
    args = parser.parse_args()
    try:
        # Verify every input before changing any owned output.
        inputs = {path: fetch(path) for path in PINS}
        index = json.loads(inputs["skills/super-library/references/index.json"])
        cards = curate(index, json.loads(inputs["library/compact_ids.json"]))
        tables = {Path(path).name: adapt_table(data) for path, data in inputs.items() if path.endswith(".tex")}
        protocols = curate_protocols(index, cards, tables)
        outputs = {ROOT / "references" / "writing-library.json":
                   (json.dumps(cards, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
                   ROOT / "references" / "writing-protocols.json":
                   (json.dumps(protocols, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
                   ROOT / "DATA_LICENSE": inputs["DATA_LICENSE"],
                   ROOT / "references" / "table-templates" / "LICENSE": inputs["LICENSE"]}
        outputs.update({ROOT / "references" / "table-templates" / name: data for name, data in tables.items()})
        for path, data in outputs.items():
            if args.write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            elif path.read_bytes() != data:
                raise ValueError(f"Generated data drift: {path.name}")
        print(f"{'Wrote' if args.write else 'Verified'} {len(cards['entries'])} cards, "
              f"{len(cards['sources'])} discovery sources, {len(protocols['guides'])} protocols, "
              f"30 variants and {len(tables)} tables")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Import failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
