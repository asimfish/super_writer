#!/usr/bin/env python3
"""Validate and aggregate randomized blind abstract review exports."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

DIMENSIONS = ("contribution", "rationale", "precision", "evidence", "language")
VERSIONS = {"old", "new"}


def load(path):
    return json.loads(Path(path).read_text())


def validate_review(review, mapping):
    errors = []
    if not str(review.get("reviewer_id", "")).strip():
        errors.append("missing reviewer_id")
    for case_id in sorted(set(review.get("cases", {})) - set(mapping)):
        errors.append(f"unexpected case: {case_id}")
    for case_id, versions in mapping.items():
        if set(versions) != {"A", "B"} or set(versions.values()) != VERSIONS:
            errors.append(f"invalid mapping: {case_id}")
        case = review.get("cases", {}).get(case_id)
        if not isinstance(case, dict):
            errors.append(f"missing case: {case_id}")
            continue
        for label in ("A", "B"):
            scores = case.get(label)
            if not isinstance(scores, dict):
                errors.append(f"missing candidate: {case_id}/{label}")
                continue
            for dimension in DIMENSIONS:
                value = scores.get(dimension)
                if str(value) not in {"1", "2", "3", "4", "5"}:
                    errors.append(f"invalid score: {case_id}/{label}/{dimension}")
        if case.get("preferred") not in {"A", "B", "Tie"}:
            errors.append(f"invalid preference: {case_id}")
        if not str(case.get("reason", "")).strip():
            errors.append(f"missing reason: {case_id}")
    return errors


def aggregate(reviews, mapping):
    totals = {version: {dimension: [] for dimension in DIMENSIONS} for version in ("old", "new")}
    preferences = Counter()
    reasons = []
    per_case = {}
    for review in reviews:
        for case_id, labels in mapping.items():
            case = review["cases"][case_id]
            per_case.setdefault(case_id, {"old": {d: [] for d in DIMENSIONS}, "new": {d: [] for d in DIMENSIONS}, "preferences": Counter()})
            for label, version in labels.items():
                for dimension in DIMENSIONS:
                    value = int(case[label][dimension])
                    totals[version][dimension].append(value)
                    per_case[case_id][version][dimension].append(value)
            preference = case["preferred"]
            preferences["tie" if preference == "Tie" else labels[preference]] += 1
            per_case[case_id]["preferences"]["tie" if preference == "Tie" else labels[preference]] += 1
            reasons.append({"case": case_id, "preference": preference, "text": case["reason"]})
    means = {
        version: {
            dimension: round(sum(values) / len(values), 3) if values else None
            for dimension, values in dimensions.items()
        }
        for version, dimensions in totals.items()
    }
    case_summary = {}
    for case_id, values in per_case.items():
        case_summary[case_id] = {
            "scores": {
                version: {dimension: round(sum(scores) / len(scores), 3) for dimension, scores in dims.items()}
                for version, dims in (("old", values["old"]), ("new", values["new"]))
            },
            "delta_new_minus_old": {
                dimension: round(
                    sum(values["new"][dimension]) / len(values["new"][dimension]) -
                    sum(values["old"][dimension]) / len(values["old"][dimension]), 3
                )
                for dimension in DIMENSIONS
            },
            "preferences": dict(values["preferences"]),
        }
    return {"reviewers": len(reviews), "scores": means, "preferences": dict(preferences), "per_case": case_summary, "reasons": reasons}


def preference_agreement(reviews, mapping):
    """Return exact agreement over non-tied version preferences."""
    if len(reviews) < 2:
        return None
    pairs = agreements = 0
    for case_id, labels in mapping.items():
        resolved = []
        for review in reviews:
            preference = review["cases"][case_id]["preferred"]
            if preference != "Tie":
                resolved.append(labels[preference])
        for left in range(len(resolved)):
            for right in range(left + 1, len(resolved)):
                pairs += 1
                agreements += resolved[left] == resolved[right]
    return {"pairs": pairs, "agreements": agreements,
            "exact_agreement": round(agreements / pairs, 3) if pairs else None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--review", required=True, type=Path, action="append")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    mapping = load(args.mapping)
    reviews = [load(path) for path in args.review]
    reviewer_ids = [str(review.get("reviewer_id", "")).strip() for review in reviews]
    if len(reviewer_ids) != len(set(reviewer_ids)):
        parser.error("review validation failed:\nduplicate reviewer_id")
    errors = [f"{path}: {error}" for path, review in zip(args.review, reviews)
              for error in validate_review(review, mapping)]
    if errors:
        parser.error("review validation failed:\n" + "\n".join(errors))
    result = aggregate(reviews, mapping)
    result["preference_agreement"] = preference_agreement(reviews, mapping)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
