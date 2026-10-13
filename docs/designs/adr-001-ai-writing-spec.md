# ADR-001: A Local AI Writing Specification Beside the Pinned Library

## Status

Accepted for this local implementation on 2026-10-12. Not a release, installation,
model-training change or demonstrated writing-quality improvement.

## Context

The existing skill has workflow playbooks, 130 pinned language cards, 16 protocols
with 30 variants, and separate semantic/quality checks. Users need a more explicit
specification of writing decisions and AI terminology, with positive/negative
examples and a diagram exposing how the parts connect.

Karpathy's linked post motivates outputs suited to understanding and oversight;
the illustrated STE structure suggests a rule/dictionary/terminology distinction.
Neither supplies an authoritative AI-paper vocabulary. The screenshot is not the
standard, and the official FAQ contradicts its approximately/about treatment.
The domain-specific restrictions and copyright cannot be carried over wholesale.

## Requirements

- Preserve the pinned library/protocol/venue files and default CLI behavior.
- Make local rules and technical senses conditional, source-located and inspectable.
- Include evidence requirements, legitimate exceptions and explained counterexamples.
- Keep fact invariants distinct from editorial preferences and effectiveness claims.
- Reuse the existing retrieval and writing owners; add no model, network or credential access.
- Draw the actual data/guidance flow, including feedback and limitations of checks.

## Alternatives

| Option | Benefit | Cost or risk |
|---|---|---|
| Merge all rules into the imported library JSON | One apparent corpus | Breaks exact upstream reproduction and confuses original guidance with imported CC0 data |
| Separate original catalog through the existing CLI | Preserves provenance, bounded output and familiar selection | Requires explicit catalog selection and a small record validator |
| Build a new orchestrator and automatic semantic linter | Could later automate more decisions | Requires capabilities and semantic oracles not currently implemented; a rule list cannot justify it |

## Decision

Choose the separate catalog. `references/ai-writing-spec.json` is canonical for
the original records; `writing_lookup.py --catalog ai-spec` validates and retrieves
them. The no-flag default remains the existing library. Owning playbooks retain
their workflow responsibilities. The specification is guidance consumed by the
writing agent, not executable upstream instructions or an automatic rewrite engine.

The dictionary permits explicit multiple senses instead of a universal one-word,
one-meaning policy. Defined manuscript terms and author evidence govern selection.
Part-of-speech labels aid disambiguation; they do not license global grammar bans.
Current invariants restate existing fidelity boundaries; editorial examples are
original local synthesis. Experimental guide snapshots stay outside defaults.

## Interfaces and Dependency Direction

```text
local specification JSON -> existing bounded lookup -> agent's scoped decision
author facts -> contribution/rationale -> draft -> prose read-back -> guards/delivery
language cards/protocols -> supported choices in rationale/draft
read-back/source defects -> owning draft or evidence stage
frozen candidate + separate cases -> existing blind evaluation -> evidence report
```

An arrow denotes a declared input or workflow relationship, not an implemented
automatic scheduler. Guards check their actual coded constraints, not all semantic
claims. Blind evaluation is a separate development workflow, not a required gate
for every user paragraph or automatic permission to upgrade defaults.

`tools/render_writer_atlas.py` reads this specification and current resource data,
validates owner/reference targets, and generates the atlas HTML and flow SVG.
The HTML exposes full records and exact source metadata, with local search only.
The overview PNG is rendered from this HTML using the separately invoked browser
check. No unpublished manuscript enters the atlas and it makes no remote requests.

## Verification and Maintenance

```bash
python -m unittest discover -s tests -p 'test_ai_writing_spec.py' -v
python tools/render_writer_atlas.py --output-dir docs
python tools/render_writer_atlas.py --output-dir docs --check
python -m unittest discover -s tests -p 'test_writer_atlas.py' -v
python -m unittest discover -s tests -q
```

Schema tests reject duplicate IDs, incomplete examples, invalid local statuses,
broken source references and unsafe owner paths. CLI tests preserve complete
records and legacy behavior. Browser verification checks visual bounds, readable
SVG labels, local links, dictionary selection, no remote requests and JS errors.
These prove engineering properties only, not that writers use the guidance well.

The source-only browser check requires an existing `playwright-core` installation
and Chromium; it does not install or download them. Supply their locations via
`PLAYWRIGHT_MODULE` and `CHROMIUM_PATH` when they are not locally discoverable:

```bash
node tools/check_writer_atlas.mjs --html docs/writer-atlas.html \
  --output-dir /absolute/non-symlink/check-directory \
  --overview-png docs/assets/writer-atlas.png
```

Output paths and their parents must not be symlinks (on macOS, `/tmp` is typically
a symlink; use its canonical location). The browser checks 1600px desktop and
390px mobile viewports. Mobile preserves diagram label sizes inside a horizontal
scroll region; the page itself must not overflow. HTML/SVG reproducibility is
checked byte-for-byte; PNG pixels depend on the supplied browser and fonts.

Future additions need an owning reference, synthetic context, a useful positive
example, a scientifically misleading counterexample, and a genuine exception.
Broader paper-quality evaluation must freeze a candidate and distinguish factual
accuracy, comprehension and writing preference. No global installation or push
is performed by these tools. Rendering dependencies are not runtime dependencies.

## Initial Preservation Receipts

SHA-256 values recorded before implementation; none of these files is edited:

```text
e59830a029dfe4259868335f3a0c6a6048b5dcb3a6ff767cdbe3578612287fe2  references/writing-library.json
1b8439458a039ad96ea6149b479d1fe2dfa9358477007ef93df5d3f700839a96  references/writing-protocols.json
6bf44127560ca0ffcca515f673a210bc2a01bb82635bf5f95c990a05d7ff4316  references/venue-profiles.json
```
