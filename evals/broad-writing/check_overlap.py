"""Publication diagnostic, not a writing-quality score or plagiarism certificate."""

import collections
import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WINDOW = 21


def tokens(text):
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text.lower())


def main(mode="prose"):
    domains = json.loads((ROOT / "domains.json").read_text())
    records = []
    for domain in domains:
        for pid, _, _ in domain["papers"]:
            source = tokens((ROOT / "sources" / f"{pid}.extracted.txt").read_text())
            index = collections.defaultdict(list)
            for pos in range(len(source) - WINDOW + 1):
                index[tuple(source[pos:pos + WINDOW])].append(pos)
            for condition in ("initial", "baseline", "candidate"):
                for sample in (1, 2, 3):
                    raw = json.loads((ROOT / "raw" / f"{condition}_{domain['id']}_{sample}.json").read_text())
                    case = next(c for c in raw["cases"] if c["id"] == pid)
                    for unit in (("notes",) if mode == "notes" else ("abstract", "methods", "results")):
                        text = tokens(case[unit])
                        longest, generated_offset, source_offset = 0, None, None
                        for pos in range(len(text) - WINDOW + 1):
                            for srcpos in index.get(tuple(text[pos:pos + WINDOW]), []):
                                length = WINDOW
                                while pos + length < len(text) and srcpos + length < len(source) and text[pos + length] == source[srcpos + length]:
                                    length += 1
                                if length > longest:
                                    longest, generated_offset, source_offset = length, pos, srcpos
                        records.append({"paper": pid, "condition": condition, "sample": sample,
                                        "unit": unit, "long_match_words": longest,
                                        "generated_token_offset": generated_offset,
                                        "source_token_offset": source_offset})
    output = {"window": WINDOW, "passages": len(records), "records": records,
              "flagged": [r for r in records if r["long_match_words"] >= WINDOW],
              "scope": "Lowercased English/numeric token matches against each full saved PDF extraction, "
                       "including author abstract; no source text is exported. Raw extraction defects "
                       "can hide matches; shorter phrases, translated overlap and other sources are "
                       "not assessed. Flags require contextual review, not automatic prose rescoring."}
    target = ROOT / ("overlap_notes_diagnostics.json" if mode == "notes" else "overlap_diagnostics.json")
    if target.exists():
        raise FileExistsError(target)
    target.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"passages": len(records), "flagged": output["flagged"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prose", "notes"), nargs="?", default="prose")
    main(parser.parse_args().mode)
