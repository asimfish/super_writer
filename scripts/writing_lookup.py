#!/usr/bin/env python3
"""Bounded offline lookup of academic terms and sentence patterns, not evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

INDEX = Path(__file__).resolve().parents[1] / "references" / "writing-library.json"
STOPWORDS = {"a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "with", "our", "we"}


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[^\W_]+(?:[-'][^\W_]+)*", text.casefold())) - STOPWORDS


def search(index: dict, query: str, filters: dict[str, str], entry_id: str | None = None) -> list[dict]:
    resolved = {}
    for field, value in filters.items():
        aliases = index["taxonomy"].get("filter_aliases", {}).get(field, {})
        value = aliases.get(value, value)
        if value not in index["taxonomy"][{"domain": "domains", "section": "sections", "intent": "intents", "kind": "kinds"}[field]]:
            raise ValueError(f"Unknown {field}: {value}")
        resolved[field] = value
    expanded = query.casefold()
    for alias, values in index["aliases"].items():
        if alias.casefold() in query.casefold():
            expanded += " " + " ".join(values)
    terms = tokens(expanded)
    ranked = []
    for entry in index["entries"]:
        if entry_id is not None and entry["id"] != entry_id:
            continue
        if any(value not in (entry["kind"],) if field == "kind" else value not in entry[field + "s"]
               for field, value in resolved.items()):
            continue
        score = 0
        for field, weight in (("expression", 6), ("meaning", 3), ("guidance", 2), ("tags", 3), ("examples", 1)):
            value = entry.get(field, "")
            text = " ".join(value) if isinstance(value, list) else value
            score += weight * len(terms & tokens(text))
        if entry_id is not None or score > 0:
            ranked.append((score, entry["id"], entry))
    return [entry for _, _, entry in sorted(ranked, key=lambda row: (-row[0], row[1]))]


def render(index: dict, entries: list[dict], output_format: str) -> str:
    if output_format == "ids":
        return "\n".join(entry["id"] for entry in entries)
    ids = {sid for entry in entries for sid in entry["source_ids"]}
    sources = [s for s in index["sources"] if s["id"] in ids]
    if output_format == "json":
        return json.dumps({"scope": index["scope"], "upstream_commit": index["upstream"]["commit"],
                           "entries": entries, "discovery_sources": sources}, ensure_ascii=False, indent=2)
    chunks = [index["scope"]]
    for entry in entries:
        chunks.append(f"## {entry['id']}\n\n{entry['expression']}\n\nMeaning: {entry['meaning']}\n\n"
                      f"Use: {entry['guidance']}\n\nAvoid: {entry['avoid']}\n\n"
                      + "\n".join("- " + example for example in entry["examples"]))
    if sources:
        chunks.append("Discovery only; verify support before citing:\n" + "\n".join(
            f"- {source['id']}: [{source['title']}]({source['url']})" for source in sources))
    return "\n\n".join(chunks)


def bounded_render(index: dict, entries: list[dict], limit: int, max_chars: int, output_format: str) -> str:
    selected = []
    for entry in entries[:limit]:
        candidate = render(index, selected + [entry], output_format)
        if len(candidate) + 1 > max_chars:
            break  # Never truncate a card's qualifications or emit malformed JSON.
        selected.append(entry)
    if not selected:
        raise ValueError("No complete matching card fits; increase --max-chars or narrow the query")
    return render(index, selected, output_format)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--id")
    for field in ("domain", "section", "intent", "kind"):
        parser.add_argument("--" + field)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--format", choices=("markdown", "json", "ids"), default="markdown")
    args = parser.parse_args()
    if not 1 <= args.limit <= 20 or not 512 <= args.max_chars <= 50000:
        parser.error("--limit must be 1..20 and --max-chars 512..50000")
    if len(args.query) > 256 or (not args.query.strip() and not args.id):
        parser.error("Supply --id or a query of 1..256 characters; do not pass an entire manuscript")
    try:
        with INDEX.open("rb") as stream:
            raw = stream.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise ValueError("Bundled index exceeds 2 MiB")
        index = json.loads(raw)
        filters = {field: getattr(args, field) for field in ("domain", "section", "intent", "kind") if getattr(args, field)}
        entries = search(index, args.query, filters, args.id)
        if not entries:
            raise ValueError("No matching cards in this curated subset; this is not evidence that a term is invalid")
        print(bounded_render(index, entries, args.limit, args.max_chars, args.format))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"Lookup failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
