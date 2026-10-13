# Contributing

Report issues with a minimal shareable input, exact command, Python/platform
version, expected behavior, and observed output. Use synthetic or public data;
do not attach private manuscripts, credentials, reviewer identities, or unreleased
experiment artifacts.

For a change, keep edits scoped and explain the user-facing behavior. Add a
regression when modifying guards, path handling, schemas, or packaging. Run:

```bash
python3 -m compileall -q scripts tools tests
python3 scripts/smoke_test.py
python3 -m unittest discover -s tests -v
python3 tools/build_release.py
```

The guards use the Python standard library. A new dependency needs a concrete
reason, install instructions, license review, and CI coverage.

## Writing Examples and Templates

Start with a realistic input and an observable invariant: preserved numbers,
explicit assumptions, a correct citation style or an honest response to an unrun
experiment. Do not optimize for test count or attractive prose alone. Store raw
materials separately from worked answers. State whether data are invented counts,
measured synthetic outputs or licensed observations. Worked answers are not blind
evaluations.

Extended checks require Pandoc, TeX and Poppler:

```bash
python3 tools/render_examples.py --output-dir build/rendered-examples
python3 tools/check_template_compatibility.py --output-dir build/template-check
python3 tools/check_table_templates.py --output-dir build/table-check
```

The second command accesses pinned public archives. Record the official guide,
year/track, immutable revision or digest, file allowlist and upstream terms. Do
not vendor templates without permission or change official styles to satisfy a
guard. Inspect every published PDF page and preview; keep README claims aligned.
Use [SECURITY.md](SECURITY.md) for sensitive issues.

Venue additions must identify year, track and stage in `references/venue-profiles.json`.
Distinguish guide-only entries from compiled fixtures; never count a shared style
as independent coverage. Check actual citation modes, reference exclusions and
mandatory sections against primary sources, not last year's assumptions.

Language-card updates use `python3 tools/import_writing_library.py --check` to
verify reproducibility, or `--write` after reviewing pinned upstream changes.
Review the corpus-specific license, source links and qualifications. Never
import papers, unreviewed entries, agent-cache scanners or copied paper prompts.
The importer also reproduces the writer-facing protocols and five adapted TeX
tables. Ship `DATA_LICENSE`, `THIRD_PARTY_NOTICES.md` and the table directory's
MIT `LICENSE`; release building rejects missing notices. Keep required-move
checks complete in every CLI output. Do not mix protocol, variant, sentence-card
and official-format counts or treat synthetic render values as writing examples.

## Local AI Specification Additions

The original [AI specification](references/ai-writing-spec.md) is separate from
the imported, pinned corpus. Follow the [curation workflow](references/ai-spec-learning.md)
and use the [current research record](docs/research/ai-spec-expansion-2026-10-13.md)
as an evidence format, not a fixed entry quota.

Identify the concrete reader confusion and check existing owners first. Record
primary URL/version, actual read scope, located observation and local inference.
Keep conditions, evidence needs, a shared synthetic context, explained negative
wording and a legitimate exception with the canonical record. Declare self-review
as such; do not imply an independent review that did not occur. Assign kind,
topic and writing level separately, without creating a second dictionary database.

Candidate hypotheses remain in research notes until reviewed. Schema/CLI/atlas
checks establish engineering properties; quality claims need a separate frozen
comparison. Newly studied papers are development references, not unseen tests.
Do not use the upstream importer to overwrite the original catalog or promote
experimental drafting defaults after a failed quality gate.

```bash
python3 -B -m unittest discover -s tests -p test_ai_writing_spec.py -v
python3 -B tools/render_writer_atlas.py --output-dir docs
python3 -B tools/render_writer_atlas.py --output-dir docs --check
python3 -B -m unittest discover -s tests -p test_writer_atlas.py -v
```

Regenerate and inspect the PNG with the explicit browser command in
[ADR-001](docs/designs/adr-001-ai-writing-spec.md#verification-and-maintenance).
Keep counts, source notes, examples and distribution checks synchronized.
The workflow does not schedule research or add runtime network access.

Preserve legacy artifact names unless a migration is included. Update
`SKILL.md`, `agents/openai.yaml`, `skill-card.md`, and activation cases together
when changing how the skill routes or acts. Record imported work in `UPSTREAM.md`
and retain its license. Do not copy reference papers or images into examples
without permission.

Release ZIPs are produced from an explicit file list rather than the entire
worktree. Build them with `tools/build_release.py`; do not commit generated ZIPs
or private project output. Before a release, run CI, check the release digest,
and bind the GitHub release to its version tag.
