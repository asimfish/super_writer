"""Bounded local entry-point links and credential-pattern scan, not a security proof."""

import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def main(repo):
    entries = ["README.md", "README.en.md", "BENCHMARK.md", "UPSTREAM.md", "docs/validation.md",
               "docs/broad-writing-evaluation.md", "docs/evaluator-control-calibration.md",
               "docs/operative-relation-evaluation.md", "docs/abstract-transfer-evaluation.md",
               "evals/broad-writing/README.md", "evals/evaluator-controls/README.md",
               "evals/operative-relation/README.md", "evals/abstract-transfer/README.md", "examples/README.md"]
    checked = 0
    files_checked, directories_checked = 0, 0
    missing = []
    for name in entries:
        path = repo / name
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", path.read_text()):
            target = target.strip().strip("<>")
            url = urlsplit(target)
            if url.scheme or not url.path:
                continue
            checked += 1
            destination = path.parent / unquote(url.path)
            if destination.is_file():
                files_checked += 1
            elif destination.is_dir():
                directories_checked += 1
            else:
                missing.append({"entry": name, "target": target})
    archive = repo / "evals/abstract-transfer"
    patterns = re.compile(rb"(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|ct-[a-f0-9]{32}|-----BEGIN(?: RSA| EC| OPENSSH)? PRIVATE KEY-----)")
    files = [p for p in archive.rglob("*") if p.is_file()]
    hits = [str(p.relative_to(repo)) for p in files if patterns.search(p.read_bytes())]
    pdfs = [str(p.relative_to(repo)) for p in files if p.suffix.lower() == ".pdf"]
    result = {"entry_points": len(entries), "local_destinations_checked": checked,
              "local_file_destinations": files_checked, "local_directory_destinations": directories_checked, "missing": missing,
              "archive_files_scanned": len(files), "credential_pattern_matches": hits, "pdfs": pdfs,
              "scope": "Local file/directory links only; no remote availability or Markdown fragment check. Patterns are not a semantic security guarantee."}
    print(json.dumps(result, indent=2))
    if missing or hits or pdfs:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path)
    main(parser.parse_args().repo)
