"""Archive original generations and evidence receipts, not publisher body text."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


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
    files = ["PROTOCOL.md", "papers.json", "guide_hashes.json", "source_hashes.json", "initial_hashes.json",
             "generation_hashes.json", "reader_hashes.json", "initial_input_hashes.json", "editor_input_hashes.json",
             "assessment_input_hashes.json", "audit_input_hashes.json", "mapping.json", "word_counts.json",
             "summary.json", "decoded_votes.json", "decoded_audits.json", "pair_results.json", "all_raw_hashes.json",
             "assessment_budgets.json", "witnesses.json", "relation_eval.py", "test_relation_eval.py",
             "render_relation.py", "browser_relation.mjs", "archive_relation.py", "verify_relation_artifacts.py", "comparison.html",
             "execution.json", "browser_verification.json", "verify_sources.py", "source_assembly_verification.json"]
    files.extend(str(p.relative_to(ROOT)) for folder in ("raw", "requests", "anchors", "packets", "baseline", "candidate", "shared")
                 for p in sorted((ROOT / folder).glob("*")) if p.is_file())
    missing = [f for f in files if not (ROOT / f).is_file()]
    if missing:
        raise ValueError(f"Incomplete archive: {missing}")
    target.mkdir(parents=True)
    hashes = {}
    for name in files:
        dest = target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
        hashes[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if hashlib.sha256(dest.read_bytes()).hexdigest() != hashes[name]:
            raise ValueError(f"Archive mismatch: {name}")
    receipts = []
    for pid in ("N1", "N2"):
        meta = json.loads((ROOT / f"metadata/{pid}.json").read_text())
        keys = ("id", "title", "venue", "year", "conference_event_year", "metadata_url", "pdf_url", "downloaded_pdf_url",
                "source_version", "source_version_limitations", "fallback", "hashes", "source_paths", "paths",
                "extraction_command", "extraction_version", "source_warnings", "encoding_warnings", "download_warnings",
                "warnings", "permission_version_limitations", "permission_limitations", "excluded_source_exposure")
        receipts.append(portable({k: meta[k] for k in keys if k in meta}))
    (target / "source_receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
    prompts = {phase: portable(json.loads((ROOT / f"tasks.{phase}.json").read_text()))
               for phase in ("initial", "editors", "assessments", "audits")}
    (target / "prompts.portable.json").write_text(json.dumps(prompts, indent=2) + "\n")
    (target / "archive_hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    manifest = {"copied_files": len(files), "raw_response_files": 24,
                "source_preparation_contexts": 2, "writing_contexts": 12, "assessment_contexts": 12,
                "all_copied_bytes_identical": True,
                "withheld": "PDFs, full extraction, selected publisher body, full metadata/boundary recipes and image renders remain local.",
                "prompt_transformation": "Workspace string values replaced with {WORKSPACE}; no saved response changed.",
                "receipt_transformation": "Selected structured source metadata, version warnings and SHA-256; no source body excerpt.",
                "rerun": "Helpers make no model calls. Fresh runs need an explicit agent runner and independently reviewed source packets, "
                         "then new byte receipts. Original hash analysis requires the local omitted inputs. New source versions cannot silently replace them.",
                "claim_boundary": "Small targeted same-family experiment, not human review, general writing gain or new research."}
    (target / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    main(parser.parse_args().target)
