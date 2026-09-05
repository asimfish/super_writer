# Update Super Writer

Use this playbook only when the user asks to inspect or update the skill itself.
Do not start a manuscript workflow or update any installation just because the
skill is loaded.

1. Read `VERSION` next to `SKILL.md` and identify the actual installation path.
2. Compare against releases at `https://github.com/asimfish/super_writer/releases`.
   Report the current and available versions. A network failure is not evidence
   that the installation is current.
3. For a Git checkout, inspect its remote and worktree first. When update is
   requested and the tree is clean, fetch and inspect the selected version's diff
   before fast-forwarding. Preserve local edits and avoid force/reset operations.
4. For a copied or ZIP installation, download the selected release to a separate
   temporary directory and verify the published SHA-256 digest. Review changes
   and retain a recoverable copy before replacing the installation.
5. Run `scripts/smoke_test.py` from the updated skill. Do not touch paper project
   outputs or global UI preferences as part of a skill update.

The standalone installer rejects existing destinations. It deliberately does not
offer an overwrite switch. Follow the release review procedure for upgrades.

Upstream PaperSpine is a separate project. See `UPSTREAM.md`; integrating new
upstream changes requires a reviewed patch, not replacing this repository with
the upstream tree.
