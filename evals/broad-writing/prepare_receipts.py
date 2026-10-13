"""Validate preparers' original metadata and freeze source hashes before writing."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
domains = json.loads((ROOT / "domains.json").read_text())
receipts, hashes = [], {}
for domain in domains:
    for pid, title, discovery_url in domain["papers"]:
        meta = json.loads((ROOT / "metadata" / f"{pid}.json").read_text())
        if meta["id"] != pid or meta["title"].casefold() != title.casefold():
            raise ValueError(f"Paper identity mismatch: {pid}")
        for key, file in (("pdf_sha256", f"sources/{pid}.pdf"),
                          ("body_sha256", f"inputs/{pid}.txt")):
            actual = hashlib.sha256((ROOT / file).read_bytes()).hexdigest()
            if actual != meta[key]:
                raise ValueError(f"Source mismatch: {pid}, {key}")
            hashes[file] = actual
        for file in (f"metadata/{pid}.json", f"anchors/{pid}.json", f"sources/{pid}.extracted.txt"):
            hashes[file] = hashlib.sha256((ROOT / file).read_bytes()).hexdigest()
        if hashes[f"sources/{pid}.extracted.txt"] != meta["extracted_sha256"]:
            raise ValueError(f"Raw extraction mismatch: {pid}")
        if "supplement" in meta:
            for key, field in (("pdf_sha256", "pdf_path"), ("extracted_sha256", "extracted_path")):
                file = meta["supplement"][field]
                actual = hashlib.sha256((ROOT / file).read_bytes()).hexdigest()
                if actual != meta["supplement"][key]:
                    raise ValueError(f"Supplement mismatch: {pid}, {key}")
                hashes[file] = actual
        anchor = json.loads((ROOT / "anchors" / f"{pid}.json").read_text())
        units = anchor.get("units", anchor)
        for unit in ("abstract", "methods", "results"):
            if len(units[unit]) != 2 or {a["role"] for a in units[unit]} != {"core", "scope"}:
                raise ValueError(f"Anchor counts/roles: {pid}, {unit}")
            if any(not all(a.get(k) for k in ("reader_question", "expected_relation", "source_locator"))
                   for a in units[unit]):
                raise ValueError(f"Anchor grounding missing: {pid}, {unit}")
        recipes = sorted((ROOT / "sources").glob(f"{pid}.extract.*"))
        if len(recipes) != 1:
            raise ValueError(f"Extraction recipe missing/ambiguous: {pid}")
        for recipe in recipes:
            hashes[str(recipe.relative_to(ROOT))] = hashlib.sha256(recipe.read_bytes()).hexdigest()
        receipts.append({"id": pid, "domain_id": domain["id"], "domain": domain["domain"],
                         "title": title, "discovery_url": discovery_url,
                         "original_metadata": meta,
                         "extraction_recipe": str(recipes[0].relative_to(ROOT)),
                         "body_words_whitespace": len((ROOT / "inputs" / f"{pid}.txt").read_text().split()),
                         "documented_exposure": {
                             "searched": "super_writer references, docs, evals, examples before archiving this round",
                             "exact_title_or_registered_alias_hit": False,
                             "prior_family_hit": "references/abstract-exemplars.md:168 FlashAttention (NeurIPS 2022)"
                             if pid == "P03" else "references/writing-library.json:6092 Reinforcement Learning with Action Chunking (NeurIPS 2025), related concept"
                             if pid == "P13" else None,
                             "model_pretraining_exposure": "unknown, not claimed unseen"}})
for name, value in (("source_receipts.json", receipts), ("source_hashes.json", hashes)):
    path = ROOT / name
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite source freeze: {path}")
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"Frozen {len(receipts)} papers; {len(hashes)} source/anchor/recipe hashes")
