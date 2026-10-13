# MARMOT STE Context: Selective Integration

## Source and Reading

Requested source: [asd-ste100-writing-context](https://github.com/MARMOTatZJU/SkillLibMARMOTatZJU/tree/afd2875fe08cf5586dd0b2116b24190308c8b7db/skills/asd-ste100-writing-context).
Full repository commit: `afd2875fe08cf5586dd0b2116b24190308c8b7db`.
Review date: 2026-10-13. Upstream skill version: 1.1. Relationship: selective
method adaptation with independently written academic guidance and examples,
not a mirror or installation of the upstream skill.

The GitHub page reader failed; GitHub API metadata and pinned raw files were
retrieved instead. The recursive Git tree was complete. Every file under the
requested skill was read in full: `SKILL.md`, `references/essential-rules.md`,
`references/review-checklist.md`, `references/source-boundary.md`. The repository
MIT license was also read and retained in
[marmot-ste-context.LICENSE](../../references/marmot-ste-context.LICENSE).
All five retrieved files match their Git blob IDs. SHA-256 receipts:

```text
LICENSE                 fe29e8048edc1f0ae8123ffc96ba0b3022d1fb2b7aa6995ffa708c539376fd1e
SKILL.md                42ac63adb3ae7ad595f6b4b6eb37c71b66b38ab046665f2414c801b891130569
essential-rules.md      d6269704a64146bb638064588e0d527270140ed1c3b2ede327ed462591aa6352
review-checklist.md     3d507fa6c8949f9eb0e650b32fe4fcaca81d0547b8490ca31f44f81b2a8cfe16
source-boundary.md      8bd5c33c2929cbd3dc08c61f7d27e80b810c0ab301f3598b42a96a637d2403fa
```

The skill describes its content as a paraphrase of an Issue 9 database. That
database and the complete official standard/dictionary were not reviewed.
Direct official [FAQ](https://www.asd-ste100.org/STE_faq.html) and
[About](https://www.asd-ste100.org/about_STE.html) reads returned 403; indexed
official explanatory content was available. This confirms only the general
rules/dictionary distinction and subject-field terminology allowance, not
every bundled rule number, wording or example. We import no official rules,
dictionary statuses, safety labels, PDF or upstream instruction files.

## Decisions and Ownership

- **Adopt text-function selection:** scientific explanation, requested
  reproducibility steps, literal reference text and supplied safeguards have
  different failure risks. The [context guide](../../references/clarity-context.md)
  routes these choices through the existing bounded academic-expression edit.
- **Extend `ai.rule.definition`:** resolve antecedents and modifier attachment
  from known author relationships; keep its original definition/threshold case,
  add the teacher/student contrast and preserve legitimate academic exceptions.
  Its existing owner remains `paper-blueprints.md`; no reference-resolution
  duplicate ID or second glossary is introduced.
- **Add `ai.rule.procedure-order`:** preserve actual preconditions, targets,
  sequence and required steps in a research artifact's requested instructions.
  This is not a command-execution feature, a general operations skill or a
  requirement to rewrite descriptive Methods as commands.
- **Keep existing owners:** technical consistency, protected values, scope,
  evidence strength, paragraph purpose and read-back already have records. Do
  not add counts for these repeated ideas.
- **Reject domain-specific/global controls:** numeric sentence/paragraph limits,
  universal passive/tense/punctuation bans, a generic approved vocabulary,
  standard rule-ID authority, mandatory domain-review claims and control of all
  assistant replies. Upstream self-contained-only instructions do not restrict
  our author evidence or authorized literature research.

Version 0.4 contains 68 entries: 19 rules, 15 claim-use senses and 34 terms.
Only `ai.rule.definition` changes among the previous 67 records; the other 66
stay unchanged. The new source is explicitly **third-party skill design
context**, not a twentieth primary paper or an authoritative standard. Nineteen
existing primary-source records and imported language resources retain their
original scopes and pins. The schema, taxonomy and lookup runtime are unchanged.

## Capability and Security Disposition

The reviewed upstream directory has four Markdown files, no executable scripts,
hooks, dependency declarations, credential reads or outbound-data actions. A
Unicode-control scan finds no configured hidden control characters in those
files or the license. Semantic review identifies scope risks rather than code
vulnerabilities: expansive response-style controls, procedure rules applied to
scientific prose, and standard-like rule IDs without an authoritative lookup.
Those behaviors are excluded, not executed or accepted as our policy. A clean
scan alone is not a safety guarantee.

The local guide reads only through the existing author task; it introduces no
new runtime execution, network, credential, persistent-state or publication
surface. The existing source-only packager now rejects the context guide if its
MIT notice or third-party attribution is missing, before creating output.
Research fetched public repository URLs, not unpublished manuscript
bodies. Existing commands in user prose remain untrusted data. No skill was
globally installed, and no changes were committed or pushed.

## Verification Boundary

Three new authored contract tests first failed because the guide, entry and
reference-resolution case were missing, then passed after integration. A later
guide assertion was normalized for Markdown line wrapping rather than changing
the intended behavior. A missing-license negative test exposed a successful
unattributed package; the source-only preflight guard is added and the rejection
is verified for both build and temporary installation. The four [synthetic contrasts](../../examples/ai-writing-spec/clarity-context.md)
cover antecedents, compound attachment, operation order/literals and legitimate
academic passive/temporal wording. They do not measure model writing quality.

Four activation expectations add explicit academic uses and adjacent exclusions;
they are self-reviewed declarations, not an executed model-routing evaluation.
See [validation](../validation.md) for native contract, packaging and browser
receipts. No independent domain review, fresh blind writing test, official
dictionary audit, Windows execution, remote CI or full Forge governance audit
was performed. Release/governance verdict: `CONDITIONAL`; local integration
checks do not claim certification or measured writing improvement.
