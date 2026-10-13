"""Publish generated prose and receipts, never source bodies or PDFs."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent


def portable(value):
    if isinstance(value, str):
        return value.replace(str(ROOT), "{WORKSPACE}")
    if isinstance(value, list):
        return [portable(v) for v in value]
    if isinstance(value, dict):
        return {k: portable(v) for k, v in value.items()}
    return value


def main(target):
    if target.exists():
        raise FileExistsError(target)
    files = ["PROTOCOL.md", "papers.json", "selection.json", "freeze_guides.py", "guide_hashes.json", "source_hashes.json",
             "initial_input_hashes.json", "initial_hashes.json", "editor_input_hashes.json", "generation_hashes.json",
             "assessment_input_hashes.json", "reader_hashes.json", "audit_input_hashes.json", "mapping.json", "word_counts.json",
             "summary.json", "decoded_votes.json", "decoded_audits.json", "pair_results.json", "all_raw_hashes.json",
             "assessment_budgets.json", "witnesses.json", "abstract_eval.py", "test_abstract_eval.py", "render_abstract.py",
             "browser_abstract.mjs", "archive_abstract.py", "verify_abstract_artifacts.py", "comparison.html",
             "execution.json", "browser_verification.json", "source_assembly_verification.json", "verify_public.py"]
    files += [str(p.relative_to(ROOT)) for folder in ("raw", "anchors", "packets", "baseline", "candidate", "shared")
              for p in sorted((ROOT / folder).glob("*")) if p.is_file()]
    missing = [f for f in files if not (ROOT / f).is_file()]
    if missing:
        raise ValueError(f"Incomplete archive: {missing}")
    raw_count = len(list((ROOT / "raw").glob("*.json")))
    if raw_count != 36:
        raise ValueError("Exactly 36 raw responses required")
    target.mkdir(parents=True)
    hashes = {}
    for name in files:
        dest = target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
        hashes[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if hashlib.sha256(dest.read_bytes()).hexdigest() != hashes[name]:
            raise ValueError(f"Archive mismatch: {name}")
    keys = ("id", "title", "venue", "year", "metadata_url", "source_url", "source_version", "fallback", "permission_limitations",
            "paths", "hashes", "extraction_command", "extraction_version", "warnings", "excluded_source_exposure", "operational_problems", "blocker")
    receipts = []
    for p in json.loads((ROOT / "papers.json").read_text()):
        meta = json.loads((ROOT / f"metadata/{p['id']}.json").read_text())
        receipts.append(portable({k: meta[k] for k in keys if k in meta}))
    derived = {"source_receipts.json": receipts,
               "prompts.portable.json": {phase: portable(json.loads((ROOT / f"tasks.{phase}.json").read_text())) for phase in ("initial", "editors", "assessments", "audits")},
               "archive_hashes.json": hashes,
               "MANIFEST.json": {"copied_files": len(files), "raw_response_files": 36, "source_preparation_contexts": 3,
                   "writing_contexts": 18, "assessment_contexts": 18, "all_copied_bytes_identical": True,
                   "withheld": "PDFs, full extraction, selected publisher body, full metadata and extraction recipes remain local.",
                   "prompt_transformation": "Workspace string values replaced with {WORKSPACE}; no saved response changed.",
                   "receipt_transformation": "Selected structured metadata/version warnings and hashes; source spans omitted.",
                   "rerun": "Helpers invoke no model. Fresh runs require a runner, declared source versions and independently checked body packets. Original source hash analysis requires omitted local inputs.",
                   "claim_boundary": "Purposive same-family abstract transfer confirmation, not human review, statistical significance or runtime promotion."}}
    for name, obj in derived.items():
        with (target / name).open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps(derived["MANIFEST.json"], indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    main(parser.parse_args().target)
