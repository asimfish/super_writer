# Intake Stage

This file is the configuration playbook for the super-writer orchestrator.

## Purpose

Collect workflow options and write validated configuration before any substantive work.

## Required Output

- `paper_rewriting_output/paper_spine_config.json`
- `paper_rewriting_output/paper_spine_config.md`

## Config Fields

| Field | Allowed Values | Default |
|---|---|---|
| `workflow` | `rewrite_existing`, `build_from_materials` | — |
| `scene` | `journal`, `conference`, `report_review`, `competition` | — |
| `tier` | `flash`, `pro` | `flash` |
| `output_language` | `en`, `zh` | `en` for journal/conference; `zh` for Chinese requests |
| `target_name` | free text | — |
| `materials_dir` | path or empty | — |
| `draft_path` | path or empty | — |
| `user_motivation` | free text or empty | — |
| `official_urls` | list | `[]` |
| `special_requirements` | list | `[]` |
| `word_output` | `none`, `docx` | `docx` |
| `translation_package` | `none`, `zh` | `none` |
| `reference_mode` | `local_first`, `specified_paths`, `web` | `local_first` |
| `reference_paths` | list of local paths | `["."]` |
| `citation_target_count` | integer | `20` |
| `humanize_tier` | `none`, `light`, `medium`, `heavy` | `medium` |

## UI

- The supported interactive path is the bundled terminal wizard (`intake_wizard.py`).
- Resolve the installed path from `SKILL.md`, then read `interactive-intake.md`.
- Use the wizard in an accessible terminal or `--no-interactive` for supplied choices.
- Use concise structured/chat questions when interactive stdin is unavailable.
- Do not require a host-specific slash command, external window, or elevated permissions.
- Never require the user to hand-write JSON.

## Scripts

```bash
python scripts/intake_wizard.py --output-dir paper_rewriting_output
```

Resolve the script path against the skill, with the paper project as the working
directory. Keep the output directory and legacy config filenames unchanged.
Never rerun the wizard over an existing config just to resume a project.
