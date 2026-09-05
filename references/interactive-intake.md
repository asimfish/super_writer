# Interactive Intake

Resolve `scripts/intake_wizard.py` relative to the loaded `SKILL.md`; do not assume
an installation directory. Keep the current directory in the user's paper project
so material discovery and relative paths refer to that project.

## Choose the Available Interface

- In an accessible terminal, run the wizard with `--classic-input`. The bundled
  `.sh` (macOS/Linux) and `.ps1` (PowerShell) launchers run in the current terminal.
- In a tool without interactive stdin, collect material missing choices using the
  host's question interface. Run `--no-interactive` with the supplied choices.
- For an existing config, preserve it and use `progress_check.py` to resume.
  A request for an explanation or audit does not trigger a new intake.

Example from a user terminal, after resolving the installation:

```bash
python /path/to/super-writer/scripts/intake_wizard.py --classic-input \
  --output-dir paper_rewriting_output
```

Example for an already specified task:

```bash
python /path/to/super-writer/scripts/intake_wizard.py --no-interactive \
  --workflow rewrite_existing --scene conference --tier flash \
  --output-language en --ui-language zh --draft-path draft.tex \
  --target-name "Author-specified venue" --reference-path references \
  --humanize-tier none --word-output docx \
  --output-dir paper_rewriting_output
```

On Windows, `python` can be replaced by `py -3` in direct commands. The wrapper
requires `python` on PATH. Do not change PowerShell policy or request privilege
escalation to make a wrapper work; use the direct Python command instead.

## Configuration Choices

Collect workflow, scene, tier, manuscript language, target name, and draft or
materials path. Also record reference paths, official URLs, special requirements,
citation target, Word preference, translation preference, and style tier when
provided. See `intake.md` for allowed values. Use defaults only for unspecified
non-material settings and show the resulting config to the user.

The wizard may infer local source paths and a provisional motivation. This is
configuration, not author confirmation: the research and motivation stages still
need an evidence-grounded proposal and the user's decision.

The legacy `PAPERSPINE_CONFIG_HOME` override and `~/.paperspine/config.json`
store UI preferences. Use `--setup-global` only when the user requests changing
these preferences. Ordinary project configuration does not require global setup.
