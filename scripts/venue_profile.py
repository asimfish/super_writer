#!/usr/bin/env python3
"""Read an exact, year/track/stage-specific venue profile. Offline; no writes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "references" / "venue-profiles.json"


def select(catalog: dict, *, profile_id: str | None = None, venue: str | None = None,
           year: int | None = None, track: str | None = None, stage: str | None = None) -> list[dict]:
    return [p for p in catalog["profiles"]
            if (profile_id is None or p["id"] == profile_id)
            and (venue is None or p["venue"].casefold() == venue.casefold())
            and (year is None or p["year"] == year)
            and (track is None or p["track"] == track)
            and (stage is None or p["stage"] == stage)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List matching profile IDs, not a selected submission target")
    parser.add_argument("--id")
    parser.add_argument("--venue")
    parser.add_argument("--year", type=int)
    parser.add_argument("--track")
    parser.add_argument("--stage")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()
    if not args.list and not args.id and any(v is None for v in (args.venue, args.year, args.track, args.stage)):
        parser.error("Use --id or all of --venue, --year, --track, --stage; no implicit year/stage fallback")
    try:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        profiles = select(catalog, profile_id=args.id, venue=args.venue, year=args.year,
                          track=args.track, stage=args.stage)
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    if not profiles:
        parser.error("No exact profile. Consult official rules; another year's template is not a substitute.")
    if not args.list and len(profiles) != 1:
        parser.error("Ambiguous target; supply an exact profile ID")
    report = {"checked_on": catalog["checked_on"], "scope": catalog["scope"], "profiles": profiles}
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.list:
        print("\n".join(f"{p['id']}\t{p['status']}" for p in profiles))
    else:
        p = profiles[0]
        print(f"# {p['id']}\n\nChecked: {catalog['checked_on']}\n\n{catalog['scope']}\n")
        print(f"Status: {p['status']}\nBody budget: {p['body_pages']} pages")
        print("Excluded: " + (", ".join(p["excluded_from_body"]) or "nothing; total PDF limit"))
        print("Citation modes: " + (", ".join(p["citation_modes"]) or "not verified"))
        print("Fixture IDs: " + (", ".join(p["template_ids"]) or "none"))
        print("Appendix: " + p["appendix"])
        print("\n" + "\n".join("- " + check for check in p["required_checks"]))
        print("\n" + "\n".join(f"[Official source]({url})" for url in p["official_sources"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
