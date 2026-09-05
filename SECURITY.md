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
  `media.icml.cc` and `codeload.github.com`. No document upload or credentials.
  Digest mismatches fail; only allowlisted styles enter temporary directories.
- Document tools execute document/style code. Demonstration builders disable TeX
  shell escape and restrict TeX file access, but are not an OS sandbox. Use only
  reviewed fixtures and styles; isolate untrusted submissions.
- Build/install tools use an allowlist, reject source links and refuse to replace
  existing installations. Preserve local changes before upgrading.
- Offline tests intercept network calls. Passing tests or scanners do not prove
  that arbitrary future inputs are safe.

See [capabilities](skill-card.md) and [validation limits](docs/validation.md).
