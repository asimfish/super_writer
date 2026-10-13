#!/usr/bin/env python3
"""Check a generated abstract against a small, source-backed contract."""

import argparse
import json
import re
import sys
from pathlib import Path


def word_count(text):
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def check(text, contract):
    errors = []
    count = word_count(text)
    lower = re.sub(r"\s+", " ", text.lower()).strip()
    minimum = contract.get("min_words", 0)
    maximum = contract.get("max_words", 10**9)
    if count < minimum or count > maximum:
        errors.append(f"word_count={count} outside [{minimum}, {maximum}]")
    for phrase in contract.get("required", []):
        if phrase.lower() not in lower:
            errors.append(f"missing required phrase: {phrase}")
    for phrase in contract.get("forbidden", []):
        if phrase.lower() in lower:
            errors.append(f"forbidden phrase: {phrase}")
    return {"ok": not errors, "word_count": count, "errors": errors}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--abstract", required=True, type=Path)
    args = parser.parse_args()
    result = check(args.abstract.read_text(), json.loads(args.contract.read_text()))
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
