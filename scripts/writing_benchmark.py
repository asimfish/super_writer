"""Load selected existing writing resources and check a section comparison contract."""

from __future__ import annotations

import json

import writing_guide
import writing_lookup

DIMENSIONS = {"content", "organization", "evidence", "expression", "clarity", "format"}
ASSESSMENTS = {"gap", "meets", "valid_alternative", "not_applicable", "not_assessed"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def fields(value: object, expected: str) -> None:
    require(isinstance(value, dict) and set(value) == set(expected.split()),
            f"Expected benchmark fields: {expected}")


def nonempty(value: object) -> None:
    require(isinstance(value, str) and bool(value.strip()), "Expected nonempty benchmark text")


def ids(values: object, pool: dict) -> None:
    require(isinstance(values, list) and all(isinstance(v, str) for v in values),
            "Expected benchmark IDs")
    require(len(values) == len(set(values)) and set(values) <= set(pool),
            "Duplicate or unknown benchmark ID")


def load_resources(profile: dict, exemplars: dict) -> dict:
    fields(profile, "section contribution protocol variant ai_spec_ids library_ids criteria")
    for key in ("section", "contribution", "protocol", "variant"):
        nonempty(profile[key])
    protocol = writing_guide.report_for(writing_guide.load_index(), profile["protocol"], profile["variant"])
    require(protocol["guide"]["section"] == profile["section"], "Protocol does not match section")
    require(protocol["guide"]["id"] == profile["protocol"], "Use the canonical protocol ID")
    resources = {profile["protocol"]: protocol}
    for name, filename in (("ai_spec_ids", "ai-writing-spec.json"), ("library_ids", "writing-library.json")):
        selected = profile[name]
        require(isinstance(selected, list) and len(selected) <= 6,
                "Select at most six cards per catalog")
        if not selected:
            continue
        catalog = json.loads(writing_guide.read_bounded(writing_guide.REFERENCES / filename, 2 * 1024 * 1024))
        if name == "ai_spec_ids":
            writing_lookup.validate_ai_spec(catalog)
        inventory = {entry["id"]: entry for entry in catalog["entries"]}
        ids(selected, inventory)
        for ident in selected:
            # Keep the complete entry, source notes and exceptions, not just a phrase.
            resources[ident] = json.loads(writing_lookup.render(catalog, [inventory[ident]], "json"))
    criteria = profile["criteria"]
    require(isinstance(criteria, dict) and 1 <= len(criteria) <= 12,
            "Use 1..12 scoped comparison criteria")
    for ident, criterion in criteria.items():
        nonempty(ident)
        fields(criterion, "dimension expectation applicability resource_ids source_ids")
        require(isinstance(criterion["dimension"], str) and criterion["dimension"] in DIMENSIONS,
                "Unknown comparison dimension")
        nonempty(criterion["expectation"])
        nonempty(criterion["applicability"])
        ids(criterion["resource_ids"], resources)
        ids(criterion["source_ids"], exemplars)
        require(bool(criterion["resource_ids"] or criterion["source_ids"]),
                "A comparison criterion needs a resource or located exemplar")
    return resources


def assess(values: dict, context: dict) -> None:
    criteria = context["benchmark"]["criteria"]
    require(isinstance(values, dict) and set(values) == set(criteria),
            "Assess every declared criterion exactly once")
    for assessment in values.values():
        fields(assessment, "status current difference draft_witness evidence_ids")
        require(isinstance(assessment["status"], str) and assessment["status"] in ASSESSMENTS,
                "Unknown comparison assessment")
        nonempty(assessment["current"])
        nonempty(assessment["difference"])
        ids(assessment["evidence_ids"], context["evidence"])
        witness = assessment["draft_witness"]
        if assessment["status"] in ("not_applicable", "not_assessed"):
            require(witness == "", "Unassessed/inapplicable criteria have no draft witness")
        else:
            nonempty(witness)
            require(witness in context["draft"], "Comparison witness is not in the draft")


def validate_handoff(role: str, output: dict, context: dict) -> None:
    criteria = context["benchmark"]["criteria"]
    if role in ("gap_finder", "reviewer"):
        assess(output["assessments"], context)
        statuses = {row["status"] for row in output["assessments"].values()}
        if role == "gap_finder":
            ids(output["selected_criteria"], criteria)
            for ident in output["selected_criteria"]:
                require(output["assessments"][ident]["status"] == "gap",
                        "Only a diagnosed gap can be selected for revision")
            if output["status"] == "actionable":
                require(bool(output["selected_criteria"]), "Select an actionable comparison gap")
            else:
                require(not output["selected_criteria"], "A stopped diagnosis cannot select edits")
            if output["status"] == "no_change":
                require(not statuses & {"gap", "not_assessed"},
                        "Unresolved or unassessed criteria cannot establish no_change")
        elif output["decision"] == "accept":
            require(not statuses & {"gap", "not_assessed"},
                    "Unresolved or unassessed criteria block acceptance")
    elif role == "proposer":
        ids(output["criterion_ids"], criteria)
        require(set(output["criterion_ids"]) == set(context["gap"]["selected_criteria"]),
                "Proposal must address the selected criteria without substituting gaps")
    else:
        implementations = output["implementations"]
        require(isinstance(implementations, dict)
                and set(implementations) == set(context["proposal"]["criterion_ids"]),
                "Writer must account for every proposed criterion")
        for item in implementations.values():
            fields(item, "status witness note")
            require(item["status"] in ("realized", "blocked"), "Unknown implementation status")
            nonempty(item["note"])
            if item["status"] == "realized":
                nonempty(item["witness"])
                require(item["witness"] in output["text"], "Implementation witness is not in the revision")
            else:
                require(item["witness"] == "" and bool(output["open_queries"]),
                        "Blocked implementations need an explicit author query")
