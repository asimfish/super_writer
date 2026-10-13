#!/usr/bin/env python3
"""Render a local engineering atlas from the actual writer specification."""

from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import writing_lookup

OWNERS = {
    "materials": "references/build.md",
    "planning": "references/writing-rationale-matrix.md",
    "draft": "references/rewrite.md",
    "readback": "references/argument-transfer.md",
    "guards": "scripts/progress_check.py",
    "spec": "references/ai-writing-spec.json",
    "library": "references/writing-library.json",
    "protocols": "references/writing-protocols.json",
    "quality": "references/blind-evaluation.md",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def link(name: str, base: Path) -> str:
    source = ROOT / name
    if not source.is_file():
        raise ValueError(f"Missing architecture owner: {name}")
    if source.drive.casefold() != base.drive.casefold():
        return esc(source.as_uri())
    return esc(Path(os.path.relpath(source, base)).as_posix())


def diagram(base: Path, resource_label: str) -> str:
    nodes = [
        ("materials", "Author materials", "Facts and boundaries", "build.md"),
        ("planning", "Contribution + plan", "Evidence-linked choices", "writing-rationale-matrix.md"),
        ("draft", "Draft / rewrite", "Agent-generated prose", "build.md / rewrite.md"),
        ("readback", "Semantic read-back", "Recover claim and scope", "argument-transfer.md"),
        ("guards", "Guards / delivery", "Coded constraints only", "progress_check.py"),
    ]
    chunks = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 335" role="img" aria-labelledby="flow-title flow-desc">',
              '<title id="flow-title">Super Writer: evidence, guidance and checks</title>',
              '<desc id="flow-desc">An agent-driven workflow. Guidance feeds planning and drafting; defects return to their owner. Blind quality comparison is separate and optional.</desc>',
              '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>',
              '<style>text{font-family:Arial,sans-serif;fill:#20272c;letter-spacing:0}.node rect{fill:#fff;stroke:#818c94;stroke-width:1.2}.node text{font-size:13px}.file{font-family:monospace;font-size:10px!important;fill:#52636e}.flow{fill:none;stroke:#374850;stroke-width:1.4;marker-end:url(#arrow)}.guide{stroke:#24778c;stroke-dasharray:5 4}.repair{stroke:#a94739}.caption,.node .caption{font-size:11px;fill:#52636e}</style>',
              '<rect x="8" y="100" width="575" height="102" fill="none" stroke="#c5cdd2" stroke-dasharray="3 4"/>',
              '<text x="20" y="96" class="caption">Author evidence and its owning writing stages</text>']
    for number, (ident, title, function, filename) in enumerate(nodes):
        x = 10 + number * 190
        chunks.append(f'<a href="{link(OWNERS[ident], base)}" class="node" data-node="{ident}">'
                      f'<rect x="{x}" y="114" width="170" height="76"/>'
                      f'<text x="{x + 85}" y="139" text-anchor="middle">{esc(title)}</text>'
                      f'<text x="{x + 85}" y="156" text-anchor="middle" class="caption">{esc(function)}</text>'
                      f'<text x="{x + 85}" y="175" text-anchor="middle" class="file">{esc(filename)}</text></a>')
        if number < 4:
            chunks.append(f'<path class="flow" data-edge="{ident}-{nodes[number + 1][0]}" d="M {x + 170} 152 H {x + 190}"/>')
    for ident, x, width, title, filename in (
        ("spec", 170, 320, "Local rules + conditional dictionary", "ai-writing-spec.json"),
        ("library", 565, 365, "Pinned language cards + writing protocols", resource_label),
    ):
        chunks.append(f'<a href="{link(OWNERS[ident], base)}" class="node" data-node="{ident}">'
                      f'<rect x="{x}" y="16" width="{width}" height="50"/>'
                      f'<text x="{x + width / 2}" y="37" text-anchor="middle">{esc(title)}</text>'
                      f'<text x="{x + width / 2}" y="55" text-anchor="middle" class="file">{esc(filename)}</text></a>')
    chunks += [
        '<path class="flow guide" data-edge="spec-planning" d="M 330 66 V 80 H 285 V 114"/>',
        '<path class="flow guide" data-edge="library-draft" d="M 745 66 V 84 H 475 V 114"/>',
        '<path class="flow repair" data-edge="readback-owner" d="M 665 190 V 226 H 315 V 202"/>',
        '<path class="repair" data-edge="guards-owner" d="M 855 190 V 226 H 665" fill="none" stroke-width="1.4"/>',
        '<text x="500" y="242" text-anchor="middle" class="caption">Return a defect to its owning stage, not a new automatic engine</text>',
        f'<a href="{link(OWNERS["quality"], base)}" class="node" data-node="quality"><rect x="515" y="278" width="405" height="42"/><text x="717" y="295" text-anchor="middle">Optional frozen, equal-budget blind comparison</text><text x="717" y="310" text-anchor="middle" class="caption">Development evidence; no automatic default promotion</text></a>',
        '<path class="flow guide" data-edge="draft-quality" d="M 475 190 V 299 H 515"/>',
        '<text x="20" y="289" class="caption">Solid: author workflow. Dashed: guidance / optional evaluation.</text>',
        '<text x="20" y="309" class="caption">Writing and semantic checks are performed by an agent or reader.</text>',
        '</svg>',
    ]
    return "\n".join(chunks)


STYLE = """
*{box-sizing:border-box}html{color-scheme:light}body{margin:0;color:#20272c;background:#fff;font:14px/1.5 Arial,sans-serif;letter-spacing:0}a{color:#176b82;text-decoration-thickness:1px;text-underline-offset:3px}main{max-width:1800px;margin:auto;padding:26px 30px}header{display:flex;gap:24px;justify-content:space-between;align-items:start;border-bottom:2px solid #25343b;padding-bottom:14px}h1{font-size:26px;line-height:1.2;margin:0 0 7px}h2{font-size:17px;line-height:1.35;margin:0 0 15px}h3{font-size:14px;margin:12px 0 4px}p{margin:6px 0 12px}small,.muted{color:#52636e;font-size:12px}code{font:12px/1.45 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}.atlas{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:22px 26px;padding-top:22px}.panel{min-width:0;border-top:1px solid #a5afb6;padding-top:12px}.wide{grid-column:span 6}.narrow{grid-column:span 4}.half{grid-column:span 5}.panel-title{display:flex;gap:10px;align-items:baseline}.letter{font:700 12px ui-monospace,monospace;color:#52636e}.flow-wrap svg{display:block;width:100%;height:auto}.compact-list{display:grid;grid-template-columns:1fr 1fr;gap:6px 34px;margin:0;padding-left:18px;font-size:13px}.compact-list li{padding-left:2px}.scope{border-left:3px solid #24778c;padding-left:12px;margin-top:14px}.good{color:#19644f}.bad{color:#9b3b30}.sentence{font:14px/1.65 ui-monospace,Menlo,monospace;margin:8px 0}.anatomy{display:flex;flex-wrap:wrap;gap:8px 20px;border-top:1px solid #cbd2d7;padding-top:8px;color:#24778c;font-size:12px}table{width:100%;border-collapse:collapse;table-layout:fixed}th,td{border-bottom:1px solid #d8dfe3;padding:7px 9px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{font-size:11px;color:#52636e;font-weight:500}td{font-size:12px}tbody tr:nth-child(2n){background:#f5f7f8}td:first-child{font-weight:600}.dictionary td:first-child{width:22%}.boundary-list{margin:0;padding-left:18px}.boundary-list li{margin:5px 0}.verification{display:grid;grid-template-columns:110px 1fr;gap:8px 12px}.verification strong{font-size:13px}footer{border-top:1px solid #a5afb6;margin-top:22px;padding-top:12px;font-size:12px;color:#52636e}.catalog{margin-top:38px;padding-top:20px;border-top:2px solid #25343b}.search-row{display:grid;grid-template-columns:minmax(220px,1fr) 180px 210px 150px 115px;gap:14px;align-items:end;margin-bottom:18px}label{display:block;font-size:12px;margin-bottom:4px}input,select{width:100%;min-height:36px;background:white;color:#20272c;border:1px solid #a5afb6;border-radius:3px;font:14px Arial,sans-serif;padding:7px 9px}output{font-size:13px;min-height:36px;display:flex;align-items:center}.record{border-top:1px solid #cbd2d7;padding:13px 0}.record[hidden]{display:none}.record summary{cursor:pointer;font-weight:600;overflow-wrap:anywhere}.record-body{max-width:1050px;padding:12px 0 6px 20px}.record-body ul{margin:4px 0 12px;padding-left:20px}.record-meta{font-size:12px;color:#52636e}.record-body blockquote{margin:8px 0;padding-left:14px;border-left:2px solid #b2bdc4}.record-body .counter{border-left-color:#a94739}.empty{padding:18px 0}.top-meta{text-align:right;max-width:430px}.source-list{font-size:12px;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{outline:2px solid #24778c;outline-offset:4px} .formation{border-top:1px solid #a5afb6;margin-top:22px;padding-top:16px}.formation ol{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px 24px;padding-left:20px;margin:0 0 12px}.formation li{font-size:13px}.formation small{display:block}@media(max-width:1000px){.search-row{grid-template-columns:repeat(2,minmax(0,1fr))}.formation ol{grid-template-columns:repeat(2,minmax(0,1fr))}.wide,.narrow,.half{grid-column:span 10}.flow-wrap{overflow-x:auto}.flow-wrap svg{min-width:740px}.top-meta{max-width:300px}}@media(max-width:600px){.formation ol{grid-template-columns:1fr}main{padding:18px 16px}header{display:block}.top-meta{text-align:left;max-width:none;margin-top:12px}.atlas{gap:22px}.compact-list{grid-template-columns:1fr}.search-row{grid-template-columns:1fr;gap:9px}h1{font-size:24px}.verification{grid-template-columns:95px 1fr}.record-body{padding-left:8px}th,td{padding:6px 5px}.dictionary{table-layout:auto}.flow-wrap{padding-bottom:10px}.flow-wrap svg{min-width:740px}}
"""

JS = """
const search = document.querySelector('#search');
const kind = document.querySelector('#kind');
const topic = document.querySelector('#topic');
const level = document.querySelector('#level');
const records = [...document.querySelectorAll('.record')];
function filter() {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  for (const record of records) {
    record.hidden = !(record.dataset.search.includes(query) && (!kind.value || record.dataset.kind === kind.value)
      && (!topic.value || JSON.parse(record.dataset.topics).includes(topic.value))
      && (!level.value || JSON.parse(record.dataset.levels).includes(level.value)));
    if (!record.hidden) visible++;
  }
  document.querySelector('#count').textContent = `${visible} / ${records.length} entries`;
  document.querySelector('#empty').hidden = visible !== 0;
}
search.addEventListener('input', filter);
kind.addEventListener('change', filter);
topic.addEventListener('change', filter);
level.addEventListener('change', filter);
filter();
function revealHash() {
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const record = document.getElementById(id);
  if (!record?.classList.contains('record')) return;
  search.value = kind.value = topic.value = level.value = '';
  filter();
  record.open = true;
  record.scrollIntoView();
}
addEventListener('hashchange', revealHash);
revealHash();
"""


def records_html(spec: dict, base: Path) -> str:
    sources = {s["id"]: s for s in spec["sources"]}
    reverse_aliases: dict[str, list[str]] = {}
    for alias, expanded in spec["aliases"].items():
        for term in expanded:
            reverse_aliases.setdefault(term.casefold(), []).append(alias)
    chunks = []
    for entry in spec["entries"]:
        aliases = [a for term, values in reverse_aliases.items() if term in entry["expression"].casefold() for a in values]
        search = json.dumps(entry, ensure_ascii=False).casefold() + " " + " ".join(aliases)
        chunks.append(f'<details class="record" id="{esc(entry["id"])}" data-id="{esc(entry["id"])}" data-kind="{esc(entry["kind"])}" data-search="{esc(search)}" '
                      f'data-topics="{esc(json.dumps(entry["topics"]))}" data-levels="{esc(json.dumps(entry["levels"]))}">'
                      f'<summary>{esc(entry["expression"])} <span class="record-meta">{esc(entry["id"])} / {esc(entry["status"])}</span></summary><div class="record-body">'
                      f'<p class="record-meta">Part of speech: {esc(entry["part_of_speech"])}. Local editorial status, not global word approval.</p>'
                      f'<p class="record-meta">Topics: {esc(", ".join(entry["topics"]))}. Levels: {esc(", ".join(entry["levels"]))}.</p>'
                      f'<p><strong>Meaning.</strong> {esc(entry["meaning"])}</p><p><strong>Action.</strong> {esc(entry["guidance"])}</p>'
                      f'<p><strong>Avoid.</strong> {esc(entry["avoid"])}</p>')
        for field, label in (("conditions", "Applies when"), ("evidence_required", "Evidence needed"), ("exceptions", "Exceptions")):
            chunks.append(f'<h3>{label}</h3><ul>' + "".join(f'<li>{esc(x)}</li>' for x in entry[field]) + '</ul>')
        chunks.append(f'<h3>Synthetic context</h3><p>{esc(entry["example_context"])}</p>')
        for example in entry["examples"]:
            chunks.append(f'<blockquote class="good">{esc(example)}</blockquote>')
        for example in entry["counter_examples"]:
            chunks.append(f'<blockquote class="counter"><span class="bad">{esc(example["text"])}</span><br><small>{esc(example["why"])}</small></blockquote>')
        chunks.append(f'<p>Owner: <a href="{link(entry["owner"], base)}">{esc(entry["owner"])}</a></p>')
        if entry.get("related_library_ids"):
            chunks.append('<p class="record-meta">Existing language cards: ' + esc(", ".join(entry["related_library_ids"])) + '</p>')
        for source_id in entry["source_ids"]:
            source = sources[source_id]
            chunks.append(f'<p class="source-list">Source context, not manuscript evidence: <a href="{esc(source["url"])}">{esc(source["title"])}</a>. Reading scope: {esc(source["read_scope"])}.</p>')
        for note in entry.get("source_notes", []):
            chunks.append(f'<p class="source-list"><strong>Research anchor ({esc(note["source_id"])}).</strong> {esc(note["location"])}. {esc(note["observation"])}</p>')
        chunks.append('</div></details>')
    return "\n".join(chunks)


def render(base: Path) -> dict[str, str]:
    spec = json.loads(writing_lookup.AI_SPEC.read_text(encoding="utf-8"))
    writing_lookup.validate_ai_spec(spec)
    library = json.loads(writing_lookup.INDEX.read_text(encoding="utf-8"))
    protocols = json.loads((ROOT / OWNERS["protocols"]).read_text(encoding="utf-8"))
    ids = {e["id"] for e in library["entries"]}
    for entry in spec["entries"]:
        if not set(entry.get("related_library_ids", [])) <= ids:
            raise ValueError("Related card is not in the pinned library")
    rules = [e for e in spec["entries"] if e["kind"] == "writing_rule"]
    terms = [e for e in spec["entries"] if e["kind"] != "writing_rule"]
    rule_list = "".join(f'<li><a href="{link(e["owner"], base)}">{esc(e["expression"])}</a></li>' for e in rules)
    selected = {e["id"]: e for e in spec["entries"]}
    operation = selected["ai.rule.operation"]
    preview_ids = ["ai.usage.significant", "ai.usage.faithful", "ai.usage.grounded", "ai.term.zero-shot", "ai.term.visual-grounding", "ai.term.task-chain-success"]
    rows = "".join(f'<tr><td>{esc(selected[i]["expression"])}</td><td>{esc(selected[i]["part_of_speech"])}</td><td>{esc(selected[i]["meaning"])}</td></tr>' for i in preview_ids)
    catalog = records_html(spec, base)
    def options(field: str) -> str:
        return "".join(f'<option value="{esc(value)}">{esc(value.replace("_", " "))}</option>'
                       for value in spec["taxonomy"][field])
    topic_options, level_options = options("topics"), options("levels")
    resource_label = f"{len(library['entries'])} cards; {len(protocols['guides'])} protocols / {sum(len(g['templates']) for g in protocols['guides'])} variants"
    content = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Super Writer | AI Research Writing System</title><style>{STYLE}</style></head>
<body><main><div id="atlas">
<header><div><h1>Super Writer</h1><p>AI research writing system: specification, dictionary and evidence flow</p></div><div class="top-meta"><strong>Local specification {esc(spec["spec_version"])}</strong><p class="muted">{len(rules)} rules / {len(terms)} dictionary entries<br>{len(library["entries"])} pinned language cards / {len(protocols["guides"])} protocols / {sum(len(g["templates"]) for g in protocols["guides"])} variants</p></div></header>
<div class="atlas">
<section class="panel wide"><div class="panel-title"><span class="letter">A</span><h2>Architecture and responsibility</h2></div><div class="flow-wrap">{diagram(base, resource_label)}</div><p class="muted">Core manuscript path. Resource arrows guide an agent; they do not run an autonomous semantic engine. Local links identify the actual owner.</p><p class="muted">Research, citations, document formats, translation and reviewer responses are scoped routes through <a href="{link('SKILL.md', base)}">the single Skill entrypoint</a>, not additional automatic steps.</p></section>
<section class="panel narrow"><div class="panel-title"><span class="letter">B</span><h2>Part 1: writing specification</h2></div><ol class="compact-list">{rule_list}</ol><p class="scope"><strong>Invariant vs editorial choice.</strong> Preserve truth-bearing relationships. Adapt organization to contribution, evidence and reader need; no fixed abstract sentence count.</p></section>
<section class="panel half"><div class="panel-title"><span class="letter">C</span><h2>Anatomy of a supported sentence</h2></div><p class="muted">{esc(operation["example_context"])}</p><p class="sentence bad">{esc(operation["counter_examples"][0]["text"])}</p><p class="sentence good">{esc(operation["examples"][0])}</p><div class="anatomy"><span>Object: scheduler</span><span>Action: requests an observation</span><span>Condition: age exceeds threshold</span></div><p class="muted">{esc(operation["counter_examples"][0]["why"])}</p></section>
<section class="panel half"><div class="panel-title"><span class="letter">D</span><h2>Part 2: conditional dictionary</h2></div><table class="dictionary"><thead><tr><th style="width:22%">Term / claim word</th><th style="width:16%">Part of speech</th><th>Local meaning, not a global approval</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="panel half"><div class="panel-title"><span class="letter">E</span><h2>Technical terminology and boundaries</h2></div><ul class="boundary-list"><li><strong>faithful / grounded:</strong> name the reference: source text, visual target, action state or model process. Unsupported is not automatically false.</li><li><strong>citation recall / precision:</strong> distinguish statement coverage from per-citation relevance; neither certifies answer completeness.</li><li><strong>object hallucination:</strong> declare reference coverage and denominator; unassessed attributes and relations remain outside an object-only check.</li><li><strong>plan / execution / task chain:</strong> distinguish validity, feasibility, full completion, prefix length and conditional survivors.</li><li><strong>action chunk / long-horizon:</strong> prediction length is not feedback cadence or demonstrated task completion.</li><li><strong>No STE transplant:</strong> no universal word whitelist, 20/25-word ceiling, passive-voice ban or technical -ing ban.</li></ul><p class="muted"><a href="{link('examples/ai-writing-spec/grounding-and-horizon.md', base)}">Original same-fact contrasts and question-led Results paragraphs</a><br><a href="{link('references/clarity-context.md', base)}">Context-sensitive clarity: referents, academic exceptions and procedure order</a></p></section>
<section class="panel half"><div class="panel-title"><span class="letter">F</span><h2>Verification and development evidence</h2></div><div class="verification"><strong>Schema / CLI</strong><span>IDs, required fields, complete retrieval and coded guards. Not semantic truth.</span><strong>Prose reading</strong><span>Recover the relationship and scope; verify against author evidence. Label self-review honestly.</span><strong>Blind comparison</strong><span>Frozen guides, separate cases and equal budgets. Keep losses, ties and disagreement; no automatic promotion.</span></div><p class="scope"><a href="{link('docs/designs/adr-001-ai-writing-spec.md', base)}">Design decision and preservation receipts</a><br><a href="{link('UPSTREAM.md', base)}">Source scope and adaptation boundaries</a><br><a href="{link('BENCHMARK.md', base)}">Existing quality-evaluation evidence</a></p></section>
</div><section class="formation"><h2>How the specification is formed</h2><ol><li>Primary-source reading<br><small>Version and actual read scope</small></li><li>Located observation<br><small>Separate source from inference</small></li><li>Conditional entry<br><small>Evidence, contrasts, exceptions</small></li><li>Reviewed admission<br><small>Deduplicate and check contracts</small></li></ol><p class="muted"><a href="{link('references/ai-spec-learning.md', base)}">Curated learning workflow</a> / <a href="{link('docs/research/ai-spec-expansion-2026-10-13.md', base)}">Primary-source research record</a> / <a href="{link('docs/research/marmot-ste-integration-2026-10-13.md', base)}">Selective skill integration and exclusions</a> / <a href="{link('examples/ai-writing-spec/README.md', base)}">Six earlier synthetic cases</a> / <a href="{link('examples/ai-writing-spec/grounding-and-horizon.md', base)}">Five grounding/horizon cases and Results contrasts</a>. Candidate notes are separate from admitted records; writing-quality tests remain separate from contract checks.</p></section><footer>Original specification and synthetic examples. Linked standards and papers retain their rights. No ASD-STE100 conformity, model-weight training or measured writing improvement is claimed.</footer></div>
<section class="catalog"><h2>Complete specification records</h2><div class="search-row"><div><label for="search">Term, rule or ID</label><input id="search" type="search" autocomplete="off"></div><div><label for="kind">Record type</label><select id="kind"><option value="">All records</option><option value="writing_rule">Writing rules</option><option value="claim_usage">Claim usage</option><option value="technical_term">AI terminology</option></select></div><div><label for="topic">Reader problem</label><select id="topic"><option value="">All topics</option>{topic_options}</select></div><div><label for="level">Writing level</label><select id="level"><option value="">All levels</option>{level_options}</select></div><output id="count" aria-live="polite"></output></div>{catalog}<p id="empty" class="empty" hidden>No matching entries.</p></section>
</main><script>{JS}</script></body></html>'''
    return {"writer-atlas.html": content, "assets/writer-flow.svg": diagram(base / "assets", resource_label)}


def require_plain_output(path: Path) -> None:
    for component in (path, *path.parents):
        if component.is_symlink():
            raise ValueError("Generated output must not traverse a symlink")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="Check generated text without writing")
    args = parser.parse_args()
    base = args.output_dir.absolute()
    try:
        require_plain_output(base)
        base = base.resolve()
        outputs = render(base)
        for name in outputs:
            require_plain_output(base / name)
        for name, content in outputs.items():
            path = base / name
            if args.check:
                if not path.is_file() or path.read_bytes() != content.encode("utf-8"):
                    raise ValueError(f"Generated output missing or changed: {name}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content.encode("utf-8"))
        print(f"{'Verified' if args.check else 'Rendered'} {len(outputs)} atlas artifacts")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Atlas failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
