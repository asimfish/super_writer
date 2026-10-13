"""Offline validation and summaries for this pilot, never model execution.

Schema errors raise ValueError. validate_writer returns word counts and located
final budget deviations without changing raw passages. validate_pairs returns
pair-ID metadata for summarize; validate_review checks one complete judgment.
Summaries consume only supplied pilot reviews and final budget/audit records.
CLI validation success is not a passing writing gate or runtime promotion.
"""

import argparse
import json
from pathlib import Path
import re


UNITS = ("abstract", "methods", "results")
PAPERS = ("R01", "R02")
SAMPLES = (1, 2)
BUDGETS = {"abstract": [150, 190], "methods": [110, 150], "results": [120, 160]}
NOTE_MAX_WORDS = 60
DIMENSIONS = ("contribution", "rationale", "precision", "evidence", "language")
CONDITIONS = ("baseline", "candidate")
WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:[-'\u2019][A-Za-z0-9]+)*")
PAIR_META = {
    f"{paper}_s{sample}_{unit}": {"paper": paper, "sample": sample, "unit": unit}
    for paper in PAPERS for sample in SAMPLES for unit in UNITS
}


def _object(value, label, required, optional=()):
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected an object")
    missing = set(required) - set(value)
    unexpected = set(value) - set(required) - set(optional)
    if missing or unexpected:
        raise ValueError(f"{label}: missing fields {sorted(missing, key=str)!r}; "
                         f"unexpected fields {sorted(unexpected, key=str)!r}")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected a nonempty string")


def _sample(value, label):
    if type(value) is not int or value not in SAMPLES:
        raise ValueError(f"{label}: expected integer 1 or 2")


def _ids(actual, expected, label):
    for identifier in actual:
        _text(identifier, f"{label} ID")
    if len(actual) != len(set(actual)):
        raise ValueError(f"{label}: duplicate IDs")
    missing = set(expected) - set(actual)
    unexpected = set(actual) - set(expected)
    if missing or unexpected:
        raise ValueError(f"{label}: missing IDs {sorted(missing)!r}; "
                         f"unexpected IDs {sorted(unexpected)!r}")


def count_words(text):
    """Count exactly the protocol's ASCII/alphanumeric word tokens."""
    if not isinstance(text, str):
        raise ValueError("word count: expected a string")
    return len(WORD_PATTERN.findall(text))


def validate_writer(data, phase="final"):
    """Reject structural errors; return diagnostics, not rewritten writer text."""
    if phase not in ("initial", "final"):
        raise ValueError("phase: expected initial or final")
    _object(data, "writer", ("writer_id", "replicate", "cases"))
    _text(data["writer_id"], "writer_id")
    _sample(data["replicate"], "replicate")
    if not isinstance(data["cases"], list):
        raise ValueError("cases: expected a list")
    for case in data["cases"]:
        required = ("id", *UNITS, "notes") if phase == "final" else ("id", *UNITS)
        optional = () if phase == "final" else ("notes",)
        _object(case, "case", required, optional)
    _ids([case["id"] for case in data["cases"]], PAPERS, "papers")

    counts = {}
    violations = []
    for case in data["cases"]:
        paper = case["id"]
        counts[paper] = {}
        for unit in UNITS:
            _text(case[unit], f"{paper}/{unit}")
            counts[paper][unit] = count_words(case[unit])
        if "notes" in case:
            _object(case["notes"], f"{paper}/notes", UNITS)
            counts[paper]["notes"] = {}
            for unit in UNITS:
                _text(case["notes"][unit], f"{paper}/notes/{unit}")
                counts[paper]["notes"][unit] = count_words(case["notes"][unit])

        if phase == "final":
            fields = [(unit, counts[paper][unit], *BUDGETS[unit]) for unit in UNITS]
            fields.extend((f"notes.{unit}", counts[paper]["notes"][unit], 0, NOTE_MAX_WORDS)
                          for unit in UNITS)
            for field, length, low, high in fields:
                if not low <= length <= high:
                    violations.append({
                        "writer_id": data["writer_id"], "paper": paper,
                        "sample": data["replicate"], "unit": field.split(".")[-1],
                        "field": field, "phase": phase, "words": length,
                        "min": low, "max": high,
                    })
    return {"writer_id": data["writer_id"], "replicate": data["replicate"],
            "phase": phase, "word_counts": counts, "budget_violations": violations}


def _validate_pair_meta(pair_meta):
    if not isinstance(pair_meta, dict):
        raise ValueError("pair_meta: expected a pair-ID keyed object")
    _ids(list(pair_meta), PAIR_META, "pair metadata")
    for identifier, meta in pair_meta.items():
        _object(meta, identifier, ("paper", "sample", "unit"), ("id", "A", "B"))
        _text(meta["paper"], f"{identifier}/paper")
        _text(meta["unit"], f"{identifier}/unit")
        _sample(meta["sample"], f"{identifier}/sample")
        expected = PAIR_META[identifier]
        if any(meta[field] != expected[field] for field in expected):
            raise ValueError(f"{identifier}: metadata does not match its pilot ID")
        if "id" in meta and meta["id"] != identifier:
            raise ValueError(f"{identifier}: conflicting metadata ID")
        if "A" in meta or "B" in meta:
            for side in ("A", "B"):
                _text(meta.get(side), f"{identifier}/{side}")


def validate_pairs(data):
    """Validate the full 12-pair anonymous packet and return text-free metadata."""
    _object(data, "packet", ("pairs",))
    if not isinstance(data["pairs"], list):
        raise ValueError("packet pairs: expected a list")
    for pair in data["pairs"]:
        _object(pair, "packet pair", ("id", "paper", "sample", "unit", "A", "B"))
    _ids([pair["id"] for pair in data["pairs"]], PAIR_META, "packet pairs")
    full_meta = {pair["id"]: pair for pair in data["pairs"]}
    _validate_pair_meta(full_meta)
    return {identifier: {field: full_meta[identifier][field]
                         for field in ("paper", "sample", "unit")}
            for identifier in PAIR_META}


def validate_mapping(mapping, pair_ids=None):
    """Require complete pilot IDs and an A/B bijection to the two conditions."""
    if not isinstance(mapping, dict):
        raise ValueError("mapping: expected an object")
    if pair_ids is not None:
        _ids(list(pair_ids), PAIR_META, "expected pairs")
    _ids(list(mapping), PAIR_META, "mapping")
    for identifier, sides in mapping.items():
        _object(sides, f"mapping/{identifier}", ("A", "B"))
        if not ((sides["A"] == "baseline" and sides["B"] == "candidate") or
                (sides["A"] == "candidate" and sides["B"] == "baseline")):
            raise ValueError(f"mapping/{identifier}: A/B must map to baseline/candidate")


def validate_review(data, pair_ids=None):
    """Require all pilot IDs and exact integer scores, not booleans or floats."""
    if pair_ids is not None:
        _ids(list(pair_ids), PAIR_META, "expected pairs")
    _object(data, "review", ("reviewer_id", "pairs"))
    _text(data["reviewer_id"], "reviewer_id")
    if not isinstance(data["pairs"], list):
        raise ValueError("review pairs: expected a list")
    for pair in data["pairs"]:
        _object(pair, "review pair", ("id", "preferred", "A", "B", "reason"))
    _ids([pair["id"] for pair in data["pairs"]], PAIR_META, "review pairs")
    for pair in data["pairs"]:
        identifier = pair["id"]
        if pair["preferred"] not in ("A", "B", "tie"):
            raise ValueError(f"{identifier}/preferred: expected A, B or tie")
        _text(pair["reason"], f"{identifier}/reason")
        for side in ("A", "B"):
            _object(pair[side], f"{identifier}/{side}", DIMENSIONS)
            for dimension in DIMENSIONS:
                score = pair[side][dimension]
                if type(score) is not int or not 1 <= score <= 5:
                    raise ValueError(f"{identifier}/{side}/{dimension}: "
                                     "expected integer score 1..5")


def _bucket():
    return {"votes": {"baseline": 0, "candidate": 0, "tie": 0},
            "candidate_minus_baseline": 0,
            "unanimous": {"baseline": [], "candidate": [], "tie": []},
            "disagreements": []}


def _records(value, label):
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{label}: expected a list")
    return list(value)


def summarize(reviews, mapping, pair_meta, budget_violations=None,
              consequential_candidate_failures=None):
    """Summarize exactly two complete reviewers of this pilot, with no pooling.

    pair_meta is pair-ID keyed, as returned by validate_pairs. Budget records
    supplied here must be final deviations from either condition; source-audit
    failures are supplied independently. Empty lists mean no reported failures,
    not that this function independently checked fidelity or all final writers.
    """
    _validate_pair_meta(pair_meta)
    validate_mapping(mapping, pair_meta)
    if not isinstance(reviews, (list, tuple)) or len(reviews) != 2:
        raise ValueError("reviews: exactly two unique reviewer IDs are required")
    for review in reviews:
        validate_review(review, pair_meta)
    reviewer_ids = [review["reviewer_id"] for review in reviews]
    if len({identifier.strip() for identifier in reviewer_ids}) != 2:
        raise ValueError("reviews: exactly two unique reviewer IDs are required")
    budget_violations = _records(budget_violations, "budget_violations")
    failures = _records(consequential_candidate_failures, "consequential_candidate_failures")
    judgments = {review["reviewer_id"]: {pair["id"]: pair for pair in review["pairs"]}
                 for review in reviews}
    reviewer_ids = sorted(reviewer_ids)
    overall = _bucket()
    per_unit = {unit: _bucket() for unit in UNITS}
    per_paper = {paper: _bucket() for paper in PAPERS}
    pairs = {}

    for identifier in PAIR_META:
        meta = pair_meta[identifier]
        preferences = {}
        for reviewer_id in reviewer_ids:
            preferred = judgments[reviewer_id][identifier]["preferred"]
            preferences[reviewer_id] = ("tie" if preferred == "tie"
                                        else mapping[identifier][preferred])
        votes = {condition: list(preferences.values()).count(condition)
                 for condition in (*CONDITIONS, "tie")}
        outcomes = set(preferences.values())
        outcome = next(iter(outcomes)) if len(outcomes) == 1 else "disagreement"
        pairs[identifier] = {"paper": meta["paper"], "sample": meta["sample"],
                             "unit": meta["unit"], "votes": votes,
                             "preferences": preferences, "outcome": outcome}
        for bucket in (overall, per_unit[meta["unit"]], per_paper[meta["paper"]]):
            for condition, count in votes.items():
                bucket["votes"][condition] += count
            bucket["candidate_minus_baseline"] += votes["candidate"] - votes["baseline"]
            if outcome == "disagreement":
                bucket["disagreements"].append(identifier)
            else:
                bucket["unanimous"][outcome].append(identifier)

    unanimous_candidate = overall["unanimous"]["candidate"]
    supporting_papers = {pair_meta[identifier]["paper"] for identifier in unanimous_candidate}
    criteria = {
        "abstract_net_positive": per_unit["abstract"]["candidate_minus_baseline"] > 0,
        "methods_net_positive": per_unit["methods"]["candidate_minus_baseline"] > 0,
        "unanimous_candidate_across_papers": (len(unanimous_candidate) >= 2 and
                                               len(supporting_papers) >= 2),
        "no_consequential_candidate_failures": not failures,
        "no_final_budget_deviations": not budget_violations,
    }
    blockers = {
        "abstract_net_positive": "Abstract candidate-minus-baseline votes must be > 0.",
        "methods_net_positive": "Methods candidate-minus-baseline votes must be > 0.",
        "unanimous_candidate_across_papers":
            "At least two unanimous candidate pairs across at least two papers are required.",
        "no_consequential_candidate_failures":
            "Consequential candidate failures block the gate.",
        "no_final_budget_deviations":
            "Final budget deviations in either condition block the gate, including notes.",
    }
    passed = all(criteria.values())
    reasons = [blockers[key] for key, satisfied in criteria.items() if not satisfied]
    if passed:
        reasons = ["Criteria met: further validation only, never automatic runtime promotion."]
    return {
        "scope": "ai-spec-pilot-only", "reviewer_ids": reviewer_ids, "pair_count": len(pairs),
        "overall": overall, "per_unit": per_unit, "per_paper": per_paper, "pairs": pairs,
        "budget_violations": budget_violations, "consequential_candidate_failures": failures,
        "gate": {"passed": passed, "criteria": criteria, "reasons": reasons,
                 "automatic_runtime_promotion": False},
        "limits": [
            "Only this two-paper, two-replicate, three-unit pilot is summarized; no other studies are pooled.",
            "The 24 reviewer votes are correlated judgments, not 24 independent experiments.",
            "Scores are ordinal schema-checked ratings; they do not determine this preference gate.",
            "Budget and consequential failure records are supplied externally; absence is not an independent audit.",
            "Passing supports further validation only, not human validity, conference acceptance, general writing improvement or runtime promotion.",
        ],
    }


def _json_object(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"JSON: duplicate object key {key!r}")
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError(f"JSON: nonfinite number {value!r} is not allowed")


def _load_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=_json_object, parse_constant=_nonfinite)


def require_new_output(path):
    # Windows exclusive open can follow a dangling link; inspect the entry itself.
    try:
        Path(path).lstat()
    except FileNotFoundError:
        return
    raise FileExistsError(f"Output entry already exists: {path}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline AI-spec pilot validation and summary.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--writer", type=Path)
    mode.add_argument("--reviews", nargs="+", type=Path)
    parser.add_argument("--phase", choices=("initial", "final"), default=None)
    parser.add_argument("--mapping", type=Path)
    parser.add_argument("--pairs", type=Path)
    parser.add_argument("--budget-violations", type=Path)
    parser.add_argument("--consequential-candidate-failures", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.writer:
        if any((args.mapping, args.pairs, args.budget_violations,
                args.consequential_candidate_failures)):
            parser.error("review, mapping, pair and audit inputs cannot accompany --writer")
    else:
        if not args.mapping or not args.pairs:
            parser.error("--reviews requires --mapping and --pairs")
        if args.phase is not None:
            parser.error("--phase applies only to --writer")

    try:
        if args.writer:
            result = validate_writer(_load_json(args.writer), args.phase or "final")
        else:
            result = summarize(
                [_load_json(path) for path in args.reviews], _load_json(args.mapping),
                validate_pairs(_load_json(args.pairs)),
                budget_violations=(_load_json(args.budget_violations)
                                   if args.budget_violations else None),
                consequential_candidate_failures=(_load_json(args.consequential_candidate_failures)
                                                  if args.consequential_candidate_failures else None),
            )
        rendered = json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
        if args.output:
            require_new_output(args.output)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(rendered)
        else:
            print(rendered, end="")
    except (OSError, ValueError, RecursionError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
