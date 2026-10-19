#!/usr/bin/env python3
"""Check bounded writing handoffs and emit the next role packet; never call a model."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import writing_benchmark

ROOT = Path(__file__).resolve().parents[1]
ROLE_FILES = {
    "gap_finder": "agents/writing-gap-finder.md",
    "proposer": "agents/revision-proposer.md",
    "writer": "agents/revision-writer.md",
    "reviewer": "agents/revision-reviewer.md",
}
DIMENSIONS = ("intrinsic", "reference_function", "fidelity")


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def fields(value: object, names: str) -> None:
    require(isinstance(value, dict) and set(value) == set(names.split()),
            f"Expected exactly these fields: {names}")


def text(value: object) -> None:
    require(isinstance(value, str) and bool(value.strip()), "Expected nonempty text")


def ids(value: object, pool: dict) -> None:
    require(isinstance(value, list) and all(isinstance(x, str) for x in value),
            "Expected a list of IDs")
    require(len(value) == len(set(value)) and set(value) <= set(pool),
            "Duplicate or unknown evidence/exemplar ID")


def validate_input(run: dict) -> None:
    require(isinstance(run, dict), "Run must be a JSON object")
    version = run.get("schema_version")
    fields(run, "schema_version task draft evidence exemplars max_steps events"
           + (" benchmark" if version in (2, 3) else ""))
    require(type(version) is int and version in (1, 2, 3),
            "Unsupported schema_version")
    text(run["task"])
    text(run["draft"])
    require(isinstance(run["evidence"], dict) and bool(run["evidence"]),
            "Supply author evidence; do not infer it from exemplars")
    for key, value in run["evidence"].items():
        text(key)
        text(value)
    require(isinstance(run["exemplars"], dict), "exemplars must be a mapping")
    for key, record in run["exemplars"].items():
        text(key)
        fields(record, "source location choice applicability non_transfer")
        for value in record.values():
            text(value)
    require(type(run["max_steps"]) is int and 4 <= run["max_steps"] <= 24,
            "max_steps must be an integer from 4 to 24")
    require(isinstance(run["events"], list) and len(run["events"]) <= run["max_steps"],
            "events must be a list within the step budget")


def validate_output(role: str, out: dict, context: dict) -> None:
    extensions = {"gap_finder": " assessments selected_criteria deferred_criteria",
                  "proposer": " criterion_ids compression_plan",
                  "writer": " implementations compression", "reviewer": " assessments compression"}
    extension = extensions[role] if "benchmark" in context else ""
    if "relations" in context.get("benchmark", {}) and role in ("writer", "reviewer"):
        extension += " relation_checks"
    if role == "gap_finder":
        fields(out, "status diagnosis draft_witness reader_question evidence_ids source_ids" + extension)
        require(out["status"] in ("actionable", "no_change", "needs_evidence", "needs_sources"),
                "Unknown gap status")
        for key in ("diagnosis", "reader_question", "draft_witness"):
            text(out[key])
        require(out["draft_witness"] in context["draft"], "Gap witness is not in the current draft")
    elif role == "proposer":
        fields(out, "status operation expected_effect risk success_test evidence_ids source_ids" + extension)
        require(out["status"] in ("revise", "needs_evidence"), "Unknown proposal status")
        for key in ("operation", "expected_effect", "risk", "success_test"):
            text(out[key])
    elif role == "writer":
        fields(out, "text evidence_ids open_queries" + extension)
        text(out["text"])
        require(isinstance(out["open_queries"], list), "open_queries must be a list")
        for query in out["open_queries"]:
            text(query)
    else:
        fields(out, "decision comparison reason readback judgments" + extension)
        require(out["decision"] in ("accept", "return_gap_finder", "return_proposer",
                                    "return_writer", "needs_evidence", "keep_original"),
                "Unknown review decision")
        require(out["comparison"] in ("better", "tie", "worse", "not_assessed"),
                "Unknown comparison judgment")
        text(out["reason"])
        text(out["readback"])
        fields(out["judgments"], " ".join(DIMENSIONS))
        for dimension, judgment in out["judgments"].items():
            fields(judgment, "status reason witness evidence_ids source_ids")
            require(judgment["status"] in ("pass", "fail", "not_assessed"),
                    "Unknown judgment status")
            text(judgment["reason"])
            ids(judgment["evidence_ids"], context["evidence"])
            ids(judgment["source_ids"], context["exemplars"])
            if judgment["status"] == "not_assessed":
                require(judgment["witness"] == "", "An unassessed dimension has no witness")
            else:
                text(judgment["witness"])
                require(judgment["witness"] in context["draft"],
                        "Review witness is not in the current draft")
            if dimension == "fidelity" and judgment["status"] == "pass":
                require(bool(judgment["evidence_ids"]), "Fidelity needs author evidence IDs")
            if dimension == "reference_function" and judgment["status"] == "pass":
                require(bool(judgment["source_ids"]), "Reference alignment needs located exemplars")
        if out["decision"] == "accept":
            require(out["comparison"] == "better", "Acceptance needs a comparative improvement judgment")
            require(context["draft"] != context["original_draft"],
                    "Unchanged text is not an improved revision")
            judgments = out["judgments"]
            require(all(judgments[k]["status"] == "pass" for k in ("intrinsic", "fidelity")),
                    "Acceptance requires intrinsic and fidelity judgments")
            expected = "pass" if context["exemplars"] else "not_assessed"
            require(judgments["reference_function"]["status"] == expected,
                    "Reference judgment must reflect the supplied reference context")
            require(not context["open_queries"], "Resolve open writer queries before acceptance")
        if extension:
            writing_benchmark.validate_handoff(role, out, context)
        return
    ids(out["evidence_ids"], context["evidence"])
    if "source_ids" in out:
        ids(out["source_ids"], context["exemplars"])
    if role == "writer" or out.get("status") in ("actionable", "revise"):
        require(bool(out["evidence_ids"]), "An actionable handoff needs author evidence IDs")
    if extension:
        writing_benchmark.validate_handoff(role, out, context)


def instructions(role: str) -> list[dict]:
    paths = (ROLE_FILES[role], "references/writing-team.md", "references/argument-transfer.md",
             "references/compression-first-writing.md")
    return [{"path": path, "text": (ROOT / path).read_text(encoding="utf-8")}
            for path in paths]


def inspect_run(run: dict) -> dict:
    """Replay handoffs. A hash links inputs, not authorship or semantic truth."""
    validate_input(run)
    resources = (writing_benchmark.load_resources(run["benchmark"], run["exemplars"],
                  schema_version=run["schema_version"], evidence=run["evidence"])
                 if run["schema_version"] in (2, 3) else None)
    if run["schema_version"] == 3:
        for relation in run["benchmark"]["relations"].values():
            require(not relation["original_witness"] or relation["original_witness"] in run["draft"],
                    "Relation original_witness is not in the source draft")
    initial = {key: value for key, value in run.items() if key != "events"}
    role, status = "gap_finder", "ready"
    draft, gap, proposal, feedback, queries = run["draft"], None, None, None, []
    packet = None
    for step in range(len(run["events"]) + 1):
        if status != "ready":
            require(step == len(run["events"]), "Events appended after a terminal decision")
            break
        if step == run["max_steps"]:
            status = "budget_exhausted"
            break
        context = {"task": run["task"], "draft": draft,
                   "evidence": run["evidence"], "exemplars": run["exemplars"]}
        if resources is not None:
            context.update(benchmark=run["benchmark"], writing_resources=resources)
            # A returned writer must not ratchet the relative budget from its last attempt.
            context["original_draft"] = run["draft"]
            context["benchmark_basis"] = ("standards_and_exemplars" if run["exemplars"] else "standards_only")
        if role == "reviewer":
            # Read-back is independent of the proposed explanation, not of host memory.
            context["open_queries"] = queries
            context["original_draft"] = run["draft"]
        else:
            context["feedback"] = feedback
            if role in ("proposer", "writer"):
                context["gap"] = gap
            if role == "writer":
                context["proposal"] = proposal
        guidance = instructions(role)
        if resources is not None:
            paths = ["references/style-learning-workflow.md"]
            if run["benchmark"]["section"] == "abstract":
                paths.append("references/abstract-decisions.md")
            guidance.extend({"path": path, "text": (ROOT / path).read_text(encoding="utf-8")}
                            for path in paths)
        packet = {"role": role, "step": step, "run_input_sha256": digest(initial),
                  "history_sha256": digest(run["events"][:step]),
                  "input": context, "guidance": guidance}
        packet_hash = digest(packet)
        if step == len(run["events"]):
            return {"status": status, "steps_used": step, "packet": copy.deepcopy(packet),
                    "input_sha256": packet_hash,
                    "limit": "Structural handoff checks, not semantic certification or isolation"}
        event = run["events"][step]
        fields(event, "role input_sha256 output")
        require(event["role"] == role, f"Step {step}: expected owner {role}")
        require(event["input_sha256"] == packet_hash, f"Step {step}: stale or mismatched input")
        out = event["output"]
        validate_output(role, out, context)
        if role == "gap_finder":
            gap, proposal = out, None
            if out["status"] == "actionable":
                role = "proposer"
            else:
                status = out["status"]
        elif role == "proposer":
            proposal = out
            if out["status"] == "revise":
                role = "writer"
            else:
                status = "needs_evidence"
        elif role == "writer":
            draft, queries = out["text"], out["open_queries"]
            role = "reviewer"
        else:
            decision = out["decision"]
            if decision.startswith("return_"):
                role, feedback = decision.removeprefix("return_"), out
                if role == "gap_finder":
                    gap, proposal = None, None
                elif role == "proposer":
                    proposal = None
            else:
                status = "accepted_revision" if decision == "accept" else decision
    return {"status": status, "steps_used": len(run["events"]),
            "retained_text": draft if status == "accepted_revision" else run["draft"],
            "last_attempt_text": draft,
            "last_output": copy.deepcopy(run["events"][-1]["output"]) if run["events"] else None,
            "limit": "Acceptance records supplied judgments, not proven quality improvement"}


def append_response(run: dict, response: dict) -> dict:
    state = inspect_run(run)
    require(state["status"] == "ready", "Cannot append to a terminal run")
    fields(response, "role input_sha256 output")
    result = copy.deepcopy(run)
    result["events"].append(response)
    inspect_run(result)
    return result


def unique_object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="Explicit local JSON run")
    parser.add_argument("--response", type=Path, help="Validate and append one response; emit updated run")
    args = parser.parse_args()
    try:
        run = json.loads(args.run.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        if args.response:
            response = json.loads(args.response.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
            result = append_response(run, response)
        else:
            result = inspect_run(run)
        print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
