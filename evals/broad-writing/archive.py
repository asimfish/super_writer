"""Copy only redistributable experiment artifacts, retaining raw byte identity."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main(target):
    if target.exists():
        raise FileExistsError(f"Archive already exists: {target}")
    files = ["PROTOCOL.md", "domains.json", "domains.initial.json", "replacements.json", "request.json", "frozen_hashes.json",
             "source_receipts.json", "source_hashes.json", "word_counts.json",
             "initial_hashes.json", "generation_hashes.json", "reader_hashes.json", "private_mapping.json",
             "private_reader_mapping.json", "summary.json", "decoded_votes.json",
             "decoded_audits.json", "pair_results.json", "experiment.py", "analyze.py",
             "prepare_receipts.py", "verify_artifacts.py", "verification.json",
             "all_raw_hashes.json", "reader_diagnostics.json", "assessment_word_counts.json",
             "test_experiment.py", "test_analysis.py", "render_comparison.py", "comparison.html",
             "browser_smoke.mjs", "browser_verification.json", "check_overlap.py", "overlap_diagnostics.json",
             "overlap_notes_diagnostics.json", "execution.started.json", "execution.completed.json",
             "prepare_text_only.py", "compare_audits.py", "execution.supplemental.json",
             "archive.py", "test_archive.py", "comparison-complete.html",
             "browser_verification.complete.json", "check_archive.py"]
    for folder in ("raw", "metadata", "anchors", "baseline", "candidate", "exclusions"):
        files.extend(str(p.relative_to(ROOT)) for p in sorted((ROOT / folder).glob("*")) if p.is_file())
    files.extend(str(p.relative_to(ROOT)) for p in sorted((ROOT / "sources").glob("*.extract.*")))
    files.extend(str(p.relative_to(ROOT)) for p in sorted((ROOT / "sources").glob("*.finalize-download.*")))
    files.extend(str(p.relative_to(ROOT)) for p in sorted((ROOT / "supplemental").glob("*"))
                 if p.is_file() and p.name != "prompts.json")
    missing = [name for name in files if not (ROOT / name).is_file()]
    if missing:
        raise ValueError(f"Incomplete archive inputs: {missing}")
    target.mkdir(parents=True)
    public_hashes = {}
    for name in files:
        source, dest = ROOT / name, target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        if hashlib.sha256(dest.read_bytes()).hexdigest() != sha:
            raise ValueError(f"Archive mismatch: {name}")
        public_hashes[name] = sha
    prompts = {p.name: json.loads(p.read_text().replace(str(ROOT), "{WORKSPACE}"))
               for p in sorted(ROOT.glob("prompts.*.json"))}
    prompts["prompts.text_only_audit.json"] = json.loads(
        (ROOT / "supplemental/prompts.json").read_text().replace(str(ROOT), "{WORKSPACE}"))
    (target / "prompts.portable.json").write_text(json.dumps(prompts, indent=2, ensure_ascii=True) + "\n")
    (target / "archive_hashes.json").write_text(json.dumps(public_hashes, indent=2) + "\n")
    manifest = {"raw_files": len(list((target / "raw").glob("*.json"))),
                "supplementary_raw_files": len(list((target / "supplemental").glob("audit_D*.json"))),
                "source_preparation_contexts": 6,
                "primary_output_contexts": 84,
                "supplementary_output_contexts": 6,
                "total_contexts": 96,
                "copied_files": len(files), "all_copied_bytes_identical": True,
                "prompt_path_transformation_only": "absolute local workspace to {WORKSPACE}",
                "excluded": ["third-party PDFs", "full extracted paper text", "body inputs",
                             "rendered pages", "source-containing review/audit packets"],
                "license_boundary": "Repository license does not relicense cited papers. "
                "Raw generated prose and original editorial judgments are model outputs, "
                "not endorsed author abstracts or human review.",
                "rerun": "Not a self-contained paper-text redistribution or model call runner. "
                "Retrieve the exact source versions, reproduce the saved extraction recipes, "
                "verify source_hashes, and reconstruct private packets in a fresh workspace. "
                "Use prompts.portable.json with an explicit inherited-model agent runner; "
                "helpers refuse to overwrite existing artifacts. Source text and extraction "
                "bytes may differ across Poppler versions and PDF updates."}
    (target / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    main(parser.parse_args().target)
