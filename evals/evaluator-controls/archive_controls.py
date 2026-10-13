"""Archive original synthetic controls without modifying saved model answers."""

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
    files = ["PROTOCOL.md", "cases.json", "cases.initial.json", "corrections.json",
             "fixture_review.json", "fixture_review.final.json", "frozen_hashes.json",
             "reader_hashes.json", "audit_input_hashes.json", "mapping.json",
             "summary.json", "decoded_votes.json", "decoded_audits.json", "budgets.json",
             "witnesses.json", "all_raw_hashes.json", "control_eval.py", "test_control_eval.py",
             "render_controls.py", "comparison.html", "archive_controls.py", "execution.json",
             "candidate_hypothesis.md", "hypothesis_hashes.json", "next-writing-protocol.proposed.md",
             "browser_controls.mjs", "browser_verification.json"]
    files.extend(str(p.relative_to(ROOT)) for folder in ("raw", "packets") for p in sorted((ROOT / folder).glob("*.json")))
    missing = [name for name in files if not (ROOT / name).is_file()]
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
    prompts = {name: portable(json.loads((ROOT / name).read_text())) for name in ("tasks.initial.json", "tasks.audit.json")}
    (target / "prompts.portable.json").write_text(json.dumps(prompts, indent=2) + "\n")
    (target / "archive_hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    manifest = {"copied_files": len(files), "raw_response_files": 10,
                "fixture_review_contexts": 2, "anonymous_output_contexts": 10,
                "all_copied_bytes_identical": True,
                "sources": "Original synthetic fictional premises and prose; no publication or private manuscript text.",
                "prompt_transformation": "Workspace string values replaced with {WORKSPACE}; no behavioral text repair.",
                "claim_boundary": "Evaluator calibration only, not improved writing or human independence.",
                "rerun": "Use a new workspace. Helpers do not call a model or overwrite outputs. "
                         "Temporary fixture tests are not fresh model judgments. Results are nondeterministic."}
    (target / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    main(parser.parse_args().target)
