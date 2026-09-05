# Provenance

Super Writer is an adapted derivative of PaperSpine, extracted from the
Super Skill Team collection into a separately maintained public repository.
Standalone versions start at 1.0.0; this does not rename the upstream V4 release.

| Source | Revision / Path | Relationship |
|---|---|---|
| [asimfish/super_skill_team](https://github.com/asimfish/super_skill_team) | `2da7bebf8e84c7eb1065b4c61669650e336e9620`, `skills/paper/paper-spine/` | Exact extraction baseline, including local guard fixes and smoke regression |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | `d4529208cda72aa075767611b0265b95b709b550` | Upstream V4 methodology, playbooks, role cards, and script foundations; MIT |
| [c-narcissus/paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) | `77557418b4ca8c24fa8961206bf9b8f7f6d030e1` | Presentation reference for bilingual documentation, workflow explanation, examples, and release ZIPs only |

Reviewed on 2026-09-05. The applicable upstream license was read at
[this pinned revision](https://github.com/WUBING2023/PaperSpine/blob/d4529208cda72aa075767611b0265b95b709b550/LICENSE).
Its original copyright and MIT permission text are retained in [LICENSE](LICENSE).
Super Skill Team local adaptations are included under the maintainer's authority.

No code, skill instructions, screenshots, example papers, diagrams, or ZIP contents
were copied from the figure-studio reference. Our documentation and synthetic
examples were written for this repository. There is no endorsement implied by
either reference project.

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

## Maintenance

This repository is the owner of the standalone `super-writer` distribution.
The monorepo `paper-spine` entry remains a historical/compatible predecessor;
installing both can create overlapping routing and is unnecessary.

Review upstream changes as explicit patches with provenance, license, and test
evidence. Do not automatically overwrite this derivative from upstream HEAD.
