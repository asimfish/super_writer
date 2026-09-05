"""Exercise public commands from outside the installed skill directory."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PortableUsageTests(unittest.TestCase):
    def run_script(self, name: str, args: list[str], cwd: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name), *args],
            cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=30,
            env={**os.environ, "PYTHONUTF8": "1", "PAPERSPINE_CONFIG_HOME": str(cwd / "prefs")},
        )

    def test_public_clis_work_without_the_repository_as_cwd(self) -> None:
        with tempfile.TemporaryDirectory(prefix="writer cli ") as directory:
            cwd = Path(directory)
            for script in sorted((ROOT / "scripts").glob("*.py")):
                if script.name.startswith("_"):
                    continue
                with self.subTest(script=script.name):
                    result = self.run_script(script.name, ["--help"], cwd)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(list(cwd.iterdir()), [])

    def test_explicit_config_does_not_imply_author_confirmation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="writer project ") as directory:
            cwd = Path(directory)
            out = cwd / "paper_rewriting_output"
            result = self.run_script("intake_wizard.py", [
                "--no-interactive", "--workflow", "rewrite_existing", "--scene", "conference",
                "--tier", "flash", "--output-language", "en", "--ui-language", "zh",
                "--draft-path", "draft with spaces.tex", "--target-name", "Example venue",
                "--reference-path", "local references", "--humanize-tier", "none",
                "--word-output", "none", "--output-dir", str(out),
            ], cwd)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            config = json.loads((out / "paper_spine_config.json").read_text(encoding="utf-8"))
            self.assertEqual(config["draft_path"], "draft with spaces.tex")
            self.assertEqual(config["reference_paths"], ["local references"])
            self.assertEqual(config["target_name"], "Example venue")
            self.assertFalse((out / "confirmed_motivation.md").exists())
            self.assertFalse((cwd / "prefs").exists())
            progress = self.run_script("progress_check.py", [str(out), "--json"], cwd)
            self.assertEqual(progress.returncode, 0, progress.stderr)
            status = json.loads(progress.stdout)
            self.assertFalse(status["is_complete"])
            self.assertEqual(status["next_stage"], "research")
            missing = self.run_script("contribution_check.py", [str(out), "--json"], cwd)
            self.assertNotEqual(missing.returncode, 0)

    def test_public_example_has_no_structural_findings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_script("latex_guard.py", [
                str(ROOT / "examples" / "synthetic-study" / "manuscript.tex"), "--json",
            ], Path(directory))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout), [])

    def test_latex_guard_rejects_missing_title_and_unknown_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path(directory)
            tex = cwd / "broken.tex"
            tex.write_text(
                "\\documentclass{article}\n\\begin{document}\n"
                "Missing result: \\ref{tab:absent}.\n\\end{document}\n", encoding="utf-8",
            )
            result = self.run_script("latex_guard.py", [str(tex), "--json"], cwd)
            self.assertNotEqual(result.returncode, 0)
            findings = json.loads(result.stdout)
            self.assertTrue(any(finding["check"] == "title" for finding in findings))
            self.assertTrue(any("absent" in finding["message"] for finding in findings))

    @unittest.skipIf(os.name == "nt" or not shutil.which("bash"), "POSIX launcher only")
    def test_shell_wrapper_requires_interactive_input(self) -> None:
        result = subprocess.run(
            ["bash", str(ROOT / "scripts" / "launch_paperspine_ui.sh")],
            input="", capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("--no-interactive", result.stderr)

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell unavailable")
    def test_powershell_wrapper_requires_interactive_input(self) -> None:
        result = subprocess.run(
            ["pwsh", "-NoProfile", "-NonInteractive", "-File",
             str(ROOT / "scripts" / "launch_paperspine_ui.ps1")],
            input="", capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--no-interactive", result.stderr)


if __name__ == "__main__":
    unittest.main()
