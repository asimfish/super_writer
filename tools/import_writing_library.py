#!/usr/bin/env python3
"""Explicitly refresh a bounded CC0 card subset from a SHA-256-pinned upstream.

Source-only maintenance tool. Never executes upstream code or fetches papers.
The installed lookup is offline. Generated records retain upstream IDs unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "5a5c55c0e553fc11c6b2886a5fa1a3f6094108a7"
BASE = f"https://raw.githubusercontent.com/asimfish/super_library/{COMMIT}/"
PINS = {
    "skills/super-library/references/index.json": "721e48a4ae4a9b401b1e9346b12c764bd02863f3bf4782c7bc1249871693469d",
    "library/compact_ids.json": "f04c60c98709db37de08f2a20f1b284ec5a70fd3c68dd4159ed3da32dea74862",
    "DATA_LICENSE": "858aa43d09445eb1ae9b8aaede251569d3431d5e2bf40410794913b1a0f19648",
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
               if (entry["id"] in wanted or entry["id"].startswith(("general.", "vla.")))
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
                         "input_sha256": PINS, "selection": "reviewed/source_checked compact IDs plus general.* and vla.*, excluding attested collocations"},
            "scope": "Language discovery, not evidence for manuscript claims; linked works retain their own rights.",
            "taxonomy": index["taxonomy"], "aliases": index["aliases"], "entries": entries,
            "sources": sorted(sources, key=lambda source: source["id"])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Replace the owned generated corpus and its data license")
    mode.add_argument("--check", action="store_true", help="Download pins and verify reproducible output without writing")
    args = parser.parse_args()
    try:
        index = json.loads(fetch("skills/super-library/references/index.json"))
        cards = curate(index, json.loads(fetch("library/compact_ids.json")))
        outputs = {ROOT / "references" / "writing-library.json":
                   (json.dumps(cards, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
                   ROOT / "DATA_LICENSE": fetch("DATA_LICENSE")}
        for path, data in outputs.items():
            if args.write:
                path.write_bytes(data)
            elif path.read_bytes() != data:
                raise ValueError(f"Generated data drift: {path.name}")
        print(f"{'Wrote' if args.write else 'Verified'} {len(cards['entries'])} cards and {len(cards['sources'])} discovery sources")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Import failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
