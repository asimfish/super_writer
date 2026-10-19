"""Load selected existing writing resources and check a section comparison contract."""

from __future__ import annotations

import json
import re

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


def word_count(value: str) -> int:
    """Count stable Latin/number tokens for the bounded English fixtures."""
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?|[\u4e00-\u9fff]", value))


def sentence_count(value: str) -> int:
    # Decimal metrics are not sentence boundaries; this remains a punctuation heuristic.
    prose = re.sub(r"(?<=\d)\.(?=\d)", "", value)
    return max(1, len(re.findall(r"[.!?。！？]+", prose))) if prose.strip() else 0


def string_list(value: object, message: str) -> None:
    require(isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value),
            message)


def ids(values: object, pool: dict) -> None:
    require(isinstance(values, list) and all(isinstance(v, str) for v in values),
            "Expected benchmark IDs")
    require(len(values) == len(set(values)) and set(values) <= set(pool),
            "Duplicate or unknown benchmark ID")


def load_resources(profile: dict, exemplars: dict, *, schema_version: int = 2,
                   evidence: dict | None = None) -> dict:
    fields(profile, "section contribution target_answer priority_criteria protocol variant "
                   "ai_spec_ids library_ids budget criteria"
           + (" relations" if schema_version == 3 else ""))
    for key in ("section", "contribution", "protocol", "variant"):
        nonempty(profile[key])
    nonempty(profile["target_answer"])
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
    ids(profile["priority_criteria"], criteria)
    require(1 <= len(profile["priority_criteria"]) <= 3,
            "Select 1..3 priority criteria for one revision pass")
    budget = profile["budget"]
    fields(budget, "max_words max_delta_words max_sentences max_added_clauses replacement_rule")
    for key in ("max_words", "max_delta_words", "max_sentences", "max_added_clauses"):
        if schema_version == 3 and key == "max_delta_words" and budget[key] is None:
            continue
        require(type(budget[key]) is int and budget[key] >= 0,
                f"{key} must be a non-negative integer")
    require(budget["max_words"] > 0 and budget["max_sentences"] > 0,
            "A writing budget needs positive word and sentence limits")
    nonempty(budget["replacement_rule"])
    if schema_version == 3:
        relations = profile["relations"]
        require(isinstance(relations, dict) and 1 <= len(relations) <= 3,
                "Select 1..3 indispensable meaning relations, not a fact inventory")
        for ident, relation in relations.items():
            nonempty(ident)
            fields(relation, "meaning evidence_ids original_witness")
            nonempty(relation["meaning"])
            ids(relation["evidence_ids"], evidence or {})
            require(bool(relation["evidence_ids"]), "Meaning relations need author evidence")
            require(isinstance(relation["original_witness"], str),
                    "A relation's original_witness must be text or empty for an omission")
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


def assess(values: dict, context: dict, *, reviewer: bool = False) -> None:
    criteria = context["benchmark"]["criteria"]
    require(isinstance(values, dict) and set(values) == set(criteria),
            "Assess every declared criterion exactly once")
    preserve = reviewer and "relations" in context["benchmark"]
    for assessment in values.values():
        fields(assessment, "status current difference draft_witness evidence_ids"
               + (" original_status original_witness" if preserve else ""))
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
        if preserve:
            require(assessment["original_status"] in ASSESSMENTS,
                    "Unknown original comparison assessment")
            original_witness = assessment["original_witness"]
            if assessment["original_status"] in ("not_applicable", "not_assessed"):
                require(original_witness == "", "Unassessed original has no witness")
            else:
                nonempty(original_witness)
                require(original_witness in context["original_draft"],
                        "Original assessment witness is not in the source draft")


def check_relations(values: dict, context: dict, prose: str) -> None:
    require(isinstance(values, dict) and set(values) == set(context["benchmark"]["relations"]),
            "Account for every declared meaning relation exactly once")
    for item in values.values():
        fields(item, "status witness readback")
        require(item["status"] in ("stated", "entailed", "missing"),
                "Unknown meaning-relation status")
        nonempty(item["readback"])
        if item["status"] == "missing":
            require(item["witness"] == "", "A missing relation has no prose witness")
        else:
            nonempty(item["witness"])
            require(item["witness"] in prose, "Relation witness is not in the prose")


def validate_compression(value: dict, context: dict, *, reviewer: bool) -> None:
    fields(value, "status reason original_words revision_words delta_words removed_or_merged added_clauses"
           if reviewer else "original_words revision_words delta_words removed_or_merged added_clauses")
    if reviewer:
        require(value["status"] in ("better", "tie", "worse", "not_assessed"),
                "Unknown compression judgment")
        nonempty(value["reason"])
    for key in ("original_words", "revision_words"):
        require(type(value[key]) is int and value[key] >= 0,
                "Compression counts must be non-negative integers")
    require(type(value["delta_words"]) is int,
            "Compression delta_words must be an integer")
    original = context.get("original_draft", context["draft"])
    revision = context["draft"] if reviewer else context.get("candidate_text", "")
    if not revision:
        revision = context["draft"]
    expected_original = word_count(original)
    expected_revision = word_count(revision)
    require(value["original_words"] == expected_original,
            "Compression original_words does not match the source draft")
    require(value["revision_words"] == expected_revision,
            "Compression revision_words does not match the candidate draft")
    require(value["delta_words"] == expected_revision - expected_original,
            "Compression delta_words does not match the candidate draft")
    string_list(value["removed_or_merged"], "removed_or_merged must be a list of nonempty strings")
    string_list(value["added_clauses"], "added_clauses must be a list of nonempty strings")
    budget = context["benchmark"]["budget"]
    require(expected_revision <= budget["max_words"],
            "Revision exceeds the section word budget")
    if budget["max_delta_words"] is not None:
        require(expected_revision - expected_original <= budget["max_delta_words"],
                "Revision exceeds the allowed change in word count")
    require(len(value["added_clauses"]) <= budget["max_added_clauses"],
            "Revision adds more clauses than the edit budget allows")
    if expected_revision < expected_original:
        require(value["removed_or_merged"],
                "A shorter revision must name what it removed or merged")
    elif expected_revision > expected_original:
        require(value["removed_or_merged"] or value["added_clauses"],
                "An expanded revision must account for its editorial change")


def validate_handoff(role: str, output: dict, context: dict) -> None:
    criteria = context["benchmark"]["criteria"]
    meaning_contract = "relations" in context["benchmark"]
    if meaning_contract and role in ("writer", "reviewer"):
        check_relations(output["relation_checks"], context,
                        output["text"] if role == "writer" else context["draft"])
    if role in ("gap_finder", "reviewer"):
        assess(output["assessments"], context, reviewer=role == "reviewer")
        statuses = {row["status"] for row in output["assessments"].values()}
        if role == "gap_finder":
            ids(output["selected_criteria"], criteria)
            ids(output["deferred_criteria"], criteria)
            if output["status"] == "no_change":
                require(not statuses & {"gap", "not_assessed"},
                        "no_change requires no unresolved or unassessed criteria")
                require(not output["selected_criteria"] and not output["deferred_criteria"],
                        "A no_change diagnosis cannot select or defer edits")
            for ident in output["selected_criteria"]:
                require(output["assessments"][ident]["status"] == "gap",
                        "Only a diagnosed gap can be selected for revision")
            gap_ids = {ident for ident, row in output["assessments"].items()
                       if row["status"] == "gap"}
            require(set(output["selected_criteria"]) <= set(context["benchmark"]["priority_criteria"]),
                    "Only priority criteria can drive this revision pass")
            require(set(output["selected_criteria"]) | set(output["deferred_criteria"]) == gap_ids,
                    "Every diagnosed gap must be selected or explicitly deferred")
            require(not set(output["selected_criteria"]) & set(output["deferred_criteria"]),
                    "A criterion cannot be selected and deferred")
            if output["status"] == "actionable":
                require(bool(output["selected_criteria"]), "Select an actionable comparison gap")
            else:
                require(not output["selected_criteria"], "A stopped diagnosis cannot select edits")
        elif output["decision"] == "accept":
            if meaning_contract:
                require(all(item["status"] != "missing"
                            for item in output["relation_checks"].values()),
                        "Missing meaning relations block acceptance")
                for row in output["assessments"].values():
                    require(row["status"] != "not_assessed",
                            "Unassessed candidate criteria block v3 acceptance")
                    if row["status"] == "gap":
                        require(row["original_status"] == "gap",
                                "A newly introduced gap cannot be deferred")
                    if row["original_status"] in ("meets", "valid_alternative"):
                        require(row["status"] in ("meets", "valid_alternative"),
                                "A previously satisfied criterion cannot regress")
            priority_statuses = {output["assessments"][ident]["status"]
                                 for ident in context["benchmark"]["priority_criteria"]}
            require(not priority_statuses & {"gap", "not_assessed"},
                    "Unresolved or unassessed priority criteria block acceptance")
            validate_compression(output["compression"], context, reviewer=True)
            require(output["compression"]["status"] in ("better", "tie"),
                    "Acceptance cannot ignore a compression regression")
    elif role == "proposer":
        ids(output["criterion_ids"], criteria)
        require(set(output["criterion_ids"]) == set(context["gap"]["selected_criteria"]),
                "Proposal must address the selected criteria without substituting gaps")
        plan = output["compression_plan"]
        fields(plan, "keep remove_or_merge add_only_if")
        for key in plan:
            string_list(plan[key], f"compression_plan.{key} must be a list of nonempty strings")
        require(len(plan["add_only_if"]) <= context["benchmark"]["budget"]["max_added_clauses"],
                "Compression plan exceeds the edit budget")
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
        compression = output["compression"]
        writer_context = dict(context, candidate_text=output["text"])
        validate_compression(compression, writer_context, reviewer=False)
        require(sentence_count(output["text"]) <= context["benchmark"]["budget"]["max_sentences"],
                "Revision exceeds the section sentence budget")
