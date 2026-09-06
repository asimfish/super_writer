# Security and Research Data

## Reporting

Do not post private manuscripts, reviewer identities, keys or unpublished results
in public issues. If private vulnerability reporting is available on GitHub's
Security tab, use it. Otherwise contact the maintainer through the contact method
listed on the GitHub profile before sharing a sensitive reproducer. There is no
promised response-time SLA.

## Boundaries

- The host agent and model provider determine manuscript processing. This skill
  does not make the host offline.
- Citation scripts can query Crossref with explicit bibliography metadata, never
  private support fields as fallback queries. Use `--no-api` where supported.
- The source-only template check downloads pinned public archives from
  `media.icml.cc`, `media.neurips.cc` and `codeload.github.com`. No document upload or credentials.
  Digest mismatches fail; only allowlisted styles enter temporary directories.
- Document tools execute document/style code. Demonstration builders disable TeX
  shell escape and restrict TeX file access, but are not an OS sandbox. Use only
  reviewed fixtures and styles; isolate untrusted submissions.
- Demonstration builders detect MiKTeX and pass `--disable-installer` for TeX
  and BibTeX, overriding automatic package installation for those commands.
  Missing dependencies need explicit resolution, not a global-setting change.
- Offline venue/card lookup reads bundled JSON. Protocol lookup reads bounded
  JSON and allowlisted TeX skeletons with digest and symlink checks; it never
  compiles, fills placeholders or writes files. The explicit source-only importer
  accesses pinned public data, audited table source and licenses on
  `raw.githubusercontent.com`, verifies every input before writes, and never
  executes upstream code or fetches linked papers. Only the separately invoked
  source-only table checker compiles its fixed synthetic fixtures.
- PDF inspection uses local Poppler against a size-bounded snapshot with process
  timeouts. It does not execute TeX or upload content; parser vulnerabilities
  still require a maintained toolchain and appropriate process isolation.
- Build/install tools use an allowlist, reject source links and refuse to replace
  existing installations. Preserve local changes before upgrading.
- Offline tests intercept network calls. Passing tests or scanners do not prove
  that arbitrary future inputs are safe.

See [capabilities](skill-card.md) and [validation limits](docs/validation.md).
