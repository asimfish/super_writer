#!/usr/bin/env python3
"""Bounded offline lookup of academic terms and sentence patterns, not evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit

INDEX = Path(__file__).resolve().parents[1] / "references" / "writing-library.json"
AI_SPEC = INDEX.with_name("ai-writing-spec.json")
STOPWORDS = {"a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "with", "our", "we"}
FILTER_FIELDS = {"domain": "domains", "section": "sections", "intent": "intents",
                 "kind": "kinds", "topic": "topics", "level": "levels"}


def validate_ai_spec(index: dict) -> None:
    """Validate local guidance records, not the scientific truth of their prose."""
    def strings(value: object, field: str, allow_empty: bool = False) -> None:
        if (not isinstance(value, list) or (not value and not allow_empty)
                or any(not isinstance(x, str) or not x.strip() for x in value)):
            raise ValueError(f"Invalid string list: {field}")

    def unique_ids(records: object, field: str) -> set[str]:
        if (not isinstance(records, list) or not records
                or any(not isinstance(r, dict) or not isinstance(r.get("id"), str)
                       or not r["id"].strip() for r in records)):
            raise ValueError(f"Invalid records: {field}")
        ids = [r["id"] for r in records]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate ID: {field}")
        return set(ids)

    if (not isinstance(index, dict) or index.get("catalog") != "ai-spec"
            or index.get("schema_version") not in ("1", "2")):
        raise ValueError("Unsupported AI specification schema")
    for field in ("spec_version", "scope", "license", "reviewed_on"):
        if not isinstance(index.get(field), str) or not index[field].strip():
            raise ValueError(f"Missing AI specification field: {field}")
    taxonomy = index.get("taxonomy")
    if not isinstance(taxonomy, dict):
        raise ValueError("Missing AI specification taxonomy")
    facets = ("topics", "levels") if index["schema_version"] == "2" else ()
    for field in ("domains", "sections", "intents", "kinds", *facets):
        strings(taxonomy.get(field), field)
        if len(taxonomy[field]) != len(set(taxonomy[field])):
            raise ValueError(f"Duplicate taxonomy value: {field}")
    filter_aliases = taxonomy.get("filter_aliases", {})
    if not isinstance(filter_aliases, dict):
        raise ValueError("Invalid filter aliases")
    filter_fields = {k: v for k, v in FILTER_FIELDS.items() if v in taxonomy}
    for field, values in filter_aliases.items():
        if field not in filter_fields or not isinstance(values, dict):
            raise ValueError("Invalid filter alias field")
        for alias, value in values.items():
            if (not isinstance(alias, str) or not alias.strip() or not isinstance(value, str)
                    or value not in taxonomy[filter_fields[field]]):
                raise ValueError("Invalid filter alias destination")
    aliases = index.get("aliases")
    if not isinstance(aliases, dict):
        raise ValueError("Invalid aliases")
    for key, values in aliases.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Invalid alias")
        strings(values, "alias expansions")
    source_ids = unique_ids(index.get("sources"), "sources")
    for source in index["sources"]:
        for field in ("title", "url", "read_scope", "reviewed_on"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                raise ValueError(f"Missing source field: {field}")
        url = source["url"]
        parsed = urlsplit(url)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
                or parsed.password is not None or any(c.isspace() for c in url)):
            raise ValueError("Source must be a valid HTTPS URL without credentials")
    unique_ids(index.get("entries"), "entries")
    root = INDEX.parent.parent
    for entry in index["entries"]:
        if (not entry["id"].startswith("ai.") or entry.get("kind") not in taxonomy["kinds"]
                or not isinstance(entry.get("status"), str)
                or entry["status"] not in {"invariant", "conditional", "editorial"}):
            raise ValueError(f"Invalid AI entry identity or status: {entry['id']}")
        for field in ("expression", "part_of_speech", "meaning", "guidance", "avoid", "example_context", "owner"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f"Missing entry field: {field}")
        for field in ("domains", "sections", "intents", "conditions", "exceptions", "evidence_required", "examples", *facets):
            strings(entry.get(field), field)
            if field in {"domains", "sections", "intents", *facets} and not set(entry[field]) <= set(taxonomy[field]):
                raise ValueError(f"Unknown taxonomy value: {field}")
        strings(entry.get("source_ids"), "source_ids", allow_empty=True)
        if not set(entry["source_ids"]) <= source_ids:
            raise ValueError("Unknown source ID")
        if facets:
            notes = entry.get("source_notes")
            if (not isinstance(notes, list) or any(not isinstance(n, dict)
                    or any(not isinstance(n.get(k), str) or not n[k].strip()
                           for k in ("source_id", "location", "observation")) for n in notes)):
                raise ValueError("Source notes need an ID, read location and observation")
            note_ids = [n["source_id"] for n in notes]
            if len(note_ids) != len(set(note_ids)) or set(note_ids) != set(entry["source_ids"]):
                raise ValueError("Source notes must cover exactly the entry's source IDs")
        strings(entry.get("related_library_ids", []), "related_library_ids", allow_empty=True)
        examples = entry.get("counter_examples")
        if (not isinstance(examples, list) or not examples
                or any(not isinstance(x, dict) or any(not isinstance(x.get(k), str)
                       or not x[k].strip() for k in ("text", "why")) for x in examples)):
            raise ValueError("Counter-example needs text and reason")
        owner = PurePosixPath(entry["owner"])
        if (owner.is_absolute() or ".." in owner.parts or "\\" in entry["owner"]
                or not owner.parts or owner.parts[0] != "references"
                or not (root / owner).is_file() or not (root / owner).resolve().is_relative_to(root.resolve())):
            raise ValueError("Invalid owner reference")


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[^\W_]+(?:[-'][^\W_]+)*", text.casefold())) - STOPWORDS


def search(index: dict, query: str, filters: dict[str, str], entry_id: str | None = None) -> list[dict]:
    resolved = {}
    for field, value in filters.items():
        taxonomy_field = FILTER_FIELDS.get(field)
        if taxonomy_field not in index["taxonomy"]:
            raise ValueError(f"Filter not supported by this catalog: {field}")
        aliases = index["taxonomy"].get("filter_aliases", {}).get(field, {})
        value = aliases.get(value, value)
        if value not in index["taxonomy"][taxonomy_field]:
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
        if any(value not in (entry["kind"],) if field == "kind" else value not in entry[FILTER_FIELDS[field]]
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
    if index.get("catalog") == "ai-spec":
        if output_format == "json":
            return json.dumps({"catalog": "ai-spec", "spec_version": index["spec_version"],
                               "scope": index["scope"], "entries": entries,
                               "terminology_context_sources": sources}, ensure_ascii=False, indent=2)
        chunks = [index["scope"]]
        for entry in entries:
            lines = [f"## {entry['id']}: {entry['expression']}",
                     f"Kind: {entry['kind']}; local status: {entry['status']}; part of speech: {entry['part_of_speech']}",
                     f"Meaning: {entry['meaning']}", f"Action: {entry['guidance']}", f"Avoid: {entry['avoid']}"]
            if "topics" in entry:
                lines.append("Topics: " + ", ".join(entry["topics"]) + "; levels: " + ", ".join(entry["levels"]))
            for field, label in (("conditions", "Applies when"), ("exceptions", "Exceptions"),
                                 ("evidence_required", "Evidence needed")):
                lines.append(label + ":\n" + "\n".join("- " + x for x in entry[field]))
            lines.append("Synthetic example context: " + entry["example_context"])
            lines.append("Supported wording:\n" + "\n".join("- " + x for x in entry["examples"]))
            lines.append("Misleading transfer:\n" + "\n".join(
                f"- {x['text']}\n  Why: {x['why']}" for x in entry["counter_examples"]))
            lines.append("Owner: " + entry["owner"])
            for note in entry.get("source_notes", []):
                lines.append(f"Research anchor ({note['source_id']}): {note['location']}. {note['observation']}")
            if entry.get("related_library_ids"):
                lines.append("Related original cards: " + ", ".join(entry["related_library_ids"]))
            chunks.append("\n\n".join(lines))
        if sources:
            chunks.append("Terminology context, not manuscript evidence:\n" + "\n".join(
                f"- {s['id']}: [{s['title']}]({s['url']}); read scope: {s['read_scope']}" for s in sources))
        return "\n\n".join(chunks)
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
    parser.add_argument("--catalog", choices=("library", "ai-spec"), default="library")
    for field in FILTER_FIELDS:
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
        path = AI_SPEC if args.catalog == "ai-spec" else INDEX
        if args.catalog == "ai-spec" and path.is_symlink():
            raise ValueError("AI specification must not be a symlink")
        with path.open("rb") as stream:
            raw = stream.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise ValueError("Bundled index exceeds 2 MiB")
        index = json.loads(raw)
        if args.catalog == "ai-spec":
            validate_ai_spec(index)
        filters = {field: getattr(args, field) for field in FILTER_FIELDS if getattr(args, field)}
        entries = search(index, args.query, filters, args.id)
        if not entries:
            raise ValueError("No matching cards in this curated subset; this is not evidence that a term is invalid")
        print(bounded_render(index, entries, args.limit, args.max_chars, args.format))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"Lookup failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
