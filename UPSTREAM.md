# Provenance

Super Writer is an adapted derivative of PaperSpine, extracted from the
Super Skill Team collection into a separately maintained public repository.
Standalone versions start at 1.0.0; this does not rename the upstream V4 release.

| Source | Revision / Path | Relationship |
|---|---|---|
| [asimfish/super_skill_team](https://github.com/asimfish/super_skill_team) | `2da7bebf8e84c7eb1065b4c61669650e336e9620`, `skills/paper/paper-spine/` | Exact extraction baseline, including local guard fixes and smoke regression |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | `d4529208cda72aa075767611b0265b95b709b550` | Upstream V4 methodology, playbooks, role cards, and script foundations; MIT |
| [c-narcissus/paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) | `77557418b4ca8c24fa8961206bf9b8f7f6d030e1` | Presentation reference for bilingual documentation, workflow explanation, examples, and release ZIPs only |
| [asimfish/super_translate](https://github.com/asimfish/super_translate) | `32cdaedf59b62ab05bedf3faef6c07cec872402b` | High-level README organization: artifacts, reproduction and verification boundaries; no imported content |
| [wanshuiyin/auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/auto-claude-code-research-in-sleep) | `e59008d7a42eea50a2797e55dd0d85bbbf6572f5` | High-level README organization: gallery, workflow and contribution routes; no imported content |

Baseline reviewed on 2026-09-05. The applicable upstream license was read at
[this pinned revision](https://github.com/WUBING2023/PaperSpine/blob/d4529208cda72aa075767611b0265b95b709b550/LICENSE).
Its original copyright and MIT permission text are retained in [LICENSE](LICENSE).
Super Skill Team local adaptations are included under the maintainer's authority.

No code, skill instructions, screenshots, example papers, diagrams, or ZIP contents
were copied from the figure-studio reference. Our documentation and synthetic
examples were written for this repository. There is no endorsement implied by
either reference project.

The additional README references were studied for organization only. No code,
prose, logos, screenshots, papers, performance claims or dependencies were copied.
Their licenses do not become this project's license through inspiration.

Official template sources and exact revisions/digests are recorded in
`tests/fixtures/templates/sources.json` in the source repository. Upstream styles
are downloaded into temporary directories for explicit compatibility checks,
not vendored or relicensed. Fixture prose, the minimal numeric CSL and example
manuscripts were independently written here.

## Selective Integration Audit: 2026-09-06

| Project / exact audited commit | Accepted integration | Deliberately excluded |
|---|---|---|
| [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra/tree/798f03a14ce582607ba2742d025691f226470641) | High-level dependency preflight, actual-PDF inspection, evidence-constrained revision and bounded stopping; independently implemented here | No code or paper-excerpt prompts copied. No ban on limitations, review-score acceptance surrogate, agent-cache scanning, API-key discovery or generic PDF builder presented as official |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine/tree/1fe46f0e76aab800db381b0a0c392cebe14d86bf) | Compared with the existing `d4529208...` baseline: no changed files in `src/skill/`. Retain contribution/rationale/evidence design; extend locally with contribution-specific blueprints | No claim of a new V5 runtime import. Do not restore universal numeric citations, hard citation quotas, elevated wizard launch or deletion of misplaced outputs |
| [shuorenhua](https://github.com/MrGeDiao/shuorenhua/tree/d2d0ce27da295581c3cf87a30ab65deb7d0ddfb8) | MIT method adaptation: mode/scope separation, protected semantic relationships, fidelity pass before residual prose pass | No casual-register transplant, mechanical word ban or silent removal of scholarly source gaps |
| [anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing/tree/d25ea080e1252ac2258cccc09519d138e4d2da63) | MIT method adaptation: classify caveats, lead with supported statements and preserve necessary precision | No removal of genuine uncertainty, real limitations, useful contrast or warranted acknowledgment of errors |
| [super_library](https://github.com/asimfish/super_library/tree/5a5c55c0e553fc11c6b2886a5fa1a3f6094108a7) | 127 CC0 original cards and 37 discovery-source metadata records; retain IDs, constraints and provenance; original offline lookup implementation | No upstream executable code, full papers, attested-collocation records, private data or claim of citation entailment |

PaperOrchestra's root license includes an additional notice about prompts
excerpted from its paper. We do not treat MIT as permission to republish those
excerpts, and import none. Its limitation-suppression rule conflicts with
research integrity and required ACL/EMNLP sections, so it is rejected.

Super Library distinguishes MIT software from CC0 original corpus records.
`tools/import_writing_library.py` verifies pinned index, selection-list and
data-license digests. `references/writing-library.json` records the exact inputs
and selection policy. `--check` reproduces the generated files without changes.
See [DATA_LICENSE](DATA_LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

These are selective integrations into one academic-writing skill, not five
bundled orchestrators. No companion is silently installed and none of these
projects is claimed to endorse Super Writer.

## Standalone Changes

- Publish as repository `super_writer` with discoverable skill ID `super-writer`.
- Make the entrypoint and intake/update guidance independent of monorepo paths
  and absent helper skills; keep all stage playbooks and 25 Python scripts.
- Preserve `paper_rewriting_output/`, `paper_spine_config.json`, Python helper
  module names, and legacy `PAPERSPINE_CONFIG_HOME` preferences for compatibility.
- Add bilingual onboarding, capability disclosure, activation examples, public
  synthetic materials, reproducible packaging, installation tests, and CI.
- Run the intake wrappers in the current terminal with literal arguments.
- Restrict citation API inputs to explicit bibliography fields, isolate global
  preference setup from project configuration, and keep font repair from
  changing document body content.
- Retain script-level `PaperSpine` names where changing them would obscure
  provenance or affect existing integrations.
- Recognize checked conference citation styles, make generic editorial budgets
  advisory unless explicitly enforced, and check all candidate citation rows.
- Add reproducible empirical, theoretical and response examples, real document
  builds, pinned template fixtures and open-source contribution metadata.

## Maintenance

This repository is the owner of the standalone `super-writer` distribution.
The monorepo `paper-spine` entry remains a historical/compatible predecessor;
installing both can create overlapping routing and is unnecessary.

Review upstream changes as explicit patches with provenance, license, and test
evidence. Do not automatically overwrite this derivative from upstream HEAD.
