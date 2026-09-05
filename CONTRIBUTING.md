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

Preserve legacy artifact names unless a migration is included. Update
`SKILL.md`, `agents/openai.yaml`, `skill-card.md`, and activation cases together
when changing how the skill routes or acts. Record imported work in `UPSTREAM.md`
and retain its license. Do not copy reference papers or images into examples
without permission.

Release ZIPs are produced from an explicit file list rather than the entire
worktree. Build them with `tools/build_release.py`; do not commit generated ZIPs
or private project output. Before a release, run CI, check the release digest,
and bind the GitHub release to its version tag.
