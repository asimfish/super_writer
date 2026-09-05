"""Offline CLI contract tests; run with Python >= 3.10 and unittest discovery.

Tests use synthetic release metadata and unmodified copies of the real runtime.
They do not import the distribution implementation or its allowlist. All outputs,
HOME, fault injection, and runtime smoke fixtures stay in temporary directories.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile


REPOSITORY = Path(__file__).resolve().parents[1]
ARCHIVE_NAME = "super_writer-v1.0.0-skill.zip"

# Python audit hooks enforce offline execution, including smoke-test subprocesses.
AUDIT_HOOK = '''
import functools
import os
import sys

def audit(event, args):
    if event in {"socket.connect", "socket.connect_ex", "socket.getaddrinfo",
                 "socket.gethostbyname", "socket.sendto", "socket.bind"}:
        raise RuntimeError("Network access is forbidden in distribution tests")
    if os.environ.get("DISTRIBUTION_NO_PROCESS") and event in {
            "subprocess.Popen", "os.system", "os.exec", "os.posix_spawn"}:
        raise RuntimeError("Distribution tools must not execute other programs")
    failure = os.environ.get("DISTRIBUTION_FAIL_PATH")
    if failure:
        target = args[1] if event == "os.link" else args[0] if event == "open" else None
        if isinstance(target, (str, bytes)) and os.fsdecode(target) == failure:
            raise OSError("injected publication failure")

sys.addaudithook(audit)

# Inject only OS metadata; the real build/install CLI and identity checks run.
scenario = os.environ.get("DISTRIBUTION_METADATA_FAULT")
if scenario:
    original_stat = os.stat
    original_lstat = os.lstat
    original_fstat = os.fstat
    source = original_stat(os.environ["DISTRIBUTION_METADATA_PATH"])
    handle_samples = 0

    class Metadata:
        def __init__(self, actual, **changes):
            self.actual = actual
            self.__dict__.update(changes)

        def __getattr__(self, name):
            return getattr(self.actual, name)

    def fstat(fd):
        global handle_samples
        actual = original_fstat(fd)
        if not os.path.samestat(source, actual):
            return actual
        handle_samples += 1
        if scenario == "stable-ctime":
            # Windows 3.12 fstat ctime can differ from pathname creation time.
            return Metadata(actual, st_ctime_ns=source.st_ctime_ns + 1_000_000_000)
        if scenario.startswith("cross:"):
            field = scenario.split(":", 1)[1]
            return Metadata(actual, **{field: getattr(actual, field) + 1})
        if scenario.startswith("handle:") and handle_samples >= 2:
            field = scenario.split(":", 1)[1]
            return Metadata(actual, **{field: getattr(actual, field) + 1})
        if scenario == "opened-identity":
            return Metadata(actual, st_ino=actual.st_ino + 1)
        return actual

    def path_metadata(actual):
        if handle_samples < 2 or not os.path.samestat(source, actual):
            return actual
        if scenario.startswith("path:"):
            field = scenario.split(":", 1)[1]
            return Metadata(actual, **{field: getattr(actual, field) + 1})
        if scenario == "current-identity":
            return Metadata(actual, st_ino=actual.st_ino + 1)
        return actual

    def stat_path(*args, **kwargs):
        return path_metadata(original_stat(*args, **kwargs))

    def lstat_path(*args, **kwargs):
        return path_metadata(original_lstat(*args, **kwargs))

    os.fstat = fstat
    # Python 3.10 pathlib stores these as class attributes: avoid method binding.
    os.stat = functools.partial(stat_path)
    os.lstat = functools.partial(lstat_path)
'''


class DistributionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="super writer distribution ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / "source checkout"
        self.repo.mkdir()
        self.cwd = self.base / "unrelated working directory"
        self.cwd.mkdir()
        self.home = self.base / "isolated home"
        self.home.mkdir()
        hook_dir = self.base / "offline harness"
        hook_dir.mkdir()
        (hook_dir / "sitecustomize.py").write_text(AUDIT_HOOK, encoding="utf-8")
        self.environment = {
            **os.environ,
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "TMPDIR": str(self.base),
            "TEMP": str(self.base),
            "TMP": str(self.base),
            "PYTHONPATH": str(hook_dir),
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUTF8": "1",
        }
        self.metadata = {
            "SKILL.md": "---\nname: super-writer\ndescription: Synthetic packaging fixture.\n---\n",
            "PATTERNS.md": "# Synthetic patterns\n",
            "LICENSE": "Synthetic test metadata, not a release license.\n",
            "DATA_LICENSE": (REPOSITORY / "DATA_LICENSE").read_text(encoding="utf-8"),
            "THIRD_PARTY_NOTICES.md": (REPOSITORY / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8"),
            "VERSION": "1.0.0\n",
            "UPSTREAM.md": "# Synthetic provenance\n",
            "skill-card.md": "# Synthetic capability card\n",
            "evals/activation.json": json.dumps({
                "skill": "super-writer",
                "activation_cases": [
                    {"id": "explicit", "prompt": "Use $super-writer to revise my paper.",
                     "should_activate": True},
                    {"id": "materials", "prompt": "Write a report from my research materials.",
                     "should_activate": True},
                    {"id": "exclusion", "prompt": "Do not use super-writer; fix punctuation only.",
                     "should_activate": False},
                    {"id": "neighbor", "prompt": "Write marketing copy.", "should_activate": False},
                ],
            }) + "\n",
            "README.md": "# Distribution test\n\n[Contribute](CONTRIBUTING.md)\n",
            "README.en.md": "# Distribution test in English\n\n[Contribute](CONTRIBUTING.md)\n",
            "CONTRIBUTING.md": "# Synthetic contribution guide\n",
            "docs/release notes.md": "# Public release notes\n",
            "examples/minimal/input.json": '{"synthetic": true}\n',
        }
        for name, content in self.metadata.items():
            self.write(name, content)
        for name in ("agents", "scripts", "references"):
            shutil.copytree(REPOSITORY / name, self.repo / name, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
        (self.repo / "tools").mkdir()
        for name in ("build_release.py", "install_skill.py"):
            shutil.copyfile(REPOSITORY / "tools" / name, self.repo / "tools" / name)

    def write(self, name: str, content: str) -> Path:
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_cli(self, script: Path, *args: object, success: bool = True,
                environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        env = {**self.environment, **(environment or {})}
        if script.parent.name == "tools":
            env["DISTRIBUTION_NO_PROCESS"] = "1"
        result = subprocess.run(
            [sys.executable, "-B", str(script), *(str(arg) for arg in args)],
            cwd=self.cwd, env=env, capture_output=True, text=True, timeout=120,
            check=False,
        )
        details = f"{script.name}: exit={result.returncode}\n{result.stdout}\n{result.stderr}"
        if success:
            self.assertEqual(result.returncode, 0, details)
        else:
            self.assertNotEqual(result.returncode, 0, details)
        return result

    def build(self, output: Path | None = None, **kwargs: object) -> Path:
        output = output or self.base / "release output"
        self.run_cli(self.repo / "tools/build_release.py", "--output-dir", output, **kwargs)
        return output / ARCHIVE_NAME

    def install(self, destination: Path | None = None, **kwargs: object) -> Path:
        destination = destination or self.base / "skill host with spaces" / "super-writer"
        self.run_cli(self.repo / "tools/install_skill.py", "--destination", destination, **kwargs)
        return destination

    def archive_payload(self, archive: Path) -> dict[str, bytes]:
        with zipfile.ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
            names = bundle.namelist()
            self.assertEqual(len(names), len(set(names)), "Duplicate ZIP entries")
            result = {}
            for entry in bundle.infolist():
                path = PurePosixPath(entry.filename)
                self.assertFalse(path.is_absolute())
                self.assertNotIn("..", path.parts)
                self.assertEqual(path.parts[0], "super-writer")
                self.assertGreater(len(path.parts), 1)
                self.assertNotIn("\\", entry.filename)
                self.assertTrue(stat.S_ISREG(entry.external_attr >> 16))
                result[PurePosixPath(*path.parts[1:]).as_posix()] = bundle.read(entry)
            return result

    def assert_manifest(self, payload: dict[str, bytes]) -> None:
        entries = {}
        for line in payload["MANIFEST.sha256"].decode("utf-8").splitlines():
            digest, name = line.split("  ", 1)
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
            self.assertNotIn(name, entries)
            entries[name] = digest
        self.assertEqual(set(entries), set(payload) - {"MANIFEST.sha256"})
        for name, digest in entries.items():
            self.assertEqual(digest, hashlib.sha256(payload[name]).hexdigest(), name)

    def assert_rejected_source(self) -> None:
        archive = self.build(success=False)
        destination = self.install(success=False)
        self.assertFalse(archive.parent.exists())
        self.assertFalse(destination.parent.exists())

    def assert_metadata_rejected(self, scenario: str, phase: str) -> None:
        source = self.repo / "SKILL.md"
        original = source.read_bytes()
        environment = {
            "DISTRIBUTION_METADATA_FAULT": scenario,
            "DISTRIBUTION_METADATA_PATH": str(source),
        }
        output = self.base / "rejected release"
        destination = self.base / "rejected install" / "super-writer"
        for script, flag, target in (
            ("build_release.py", "--output-dir", output),
            ("install_skill.py", "--destination", destination),
        ):
            with self.subTest(tool=script):
                result = self.run_cli(self.repo / "tools" / script, flag, target,
                                      success=False, environment=environment)
                self.assertIn(f"Source changed while {phase}: SKILL.md", result.stderr)
                self.assertFalse(output.exists())
                self.assertFalse(destination.parent.exists())
                self.assertEqual(source.read_bytes(), original)

    def test_zip_contents_digests_and_real_runtime_smoke(self) -> None:
        archive = self.build()
        self.assertEqual(archive.name, ARCHIVE_NAME)
        payload = self.archive_payload(archive)
        self.assert_manifest(payload)
        self.assertLessEqual(set(self.metadata), set(payload))
        for name, data in payload.items():
            if name != "MANIFEST.sha256":
                self.assertEqual(data, (self.repo / name).read_bytes(), name)
        digest, filename = archive.with_suffix(".zip.sha256").read_text(encoding="ascii").strip().split("  ")
        self.assertEqual(filename, ARCHIVE_NAME)
        self.assertEqual(digest, hashlib.sha256(archive.read_bytes()).hexdigest())
        extracted = self.base / "complete extraction with spaces"
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(extracted)
        self.assertEqual([path.name for path in extracted.iterdir()], ["super-writer"])
        result = self.run_cli(extracted / "super-writer/scripts/smoke_test.py")
        self.assertIn("Cases: 11 passed, 0 failed", result.stdout)
        self.assertEqual(result.stdout.count("[PASS]"), 11)

    def test_double_build_is_reproducible_across_metadata_and_environment(self) -> None:
        first = self.build(self.base / "first release", environment={"TZ": "UTC", "PYTHONHASHSEED": "1"})
        for path in self.repo.rglob("*"):
            if path.is_file():
                os.utime(path, (1893456000, 1893456000))
                path.chmod(0o700)
        second = self.build(self.base / "second release",
                            environment={"TZ": "Asia/Shanghai", "PYTHONHASHSEED": "321"})
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(first.with_suffix(".zip.sha256").read_bytes(),
                         second.with_suffix(".zip.sha256").read_bytes())
        original = first.read_bytes()
        self.build(first.parent)
        self.assertEqual(first.read_bytes(), original)

    def test_stable_cross_api_ctime_difference_preserves_build_and_install(self) -> None:
        baseline = self.build(self.base / "baseline release")
        environment = {
            "DISTRIBUTION_METADATA_FAULT": "stable-ctime",
            "DISTRIBUTION_METADATA_PATH": str(self.repo / "SKILL.md"),
        }
        injected = self.build(self.base / "different ctime release", environment=environment)
        self.assertEqual(baseline.read_bytes(), injected.read_bytes())
        destination = self.install(environment=environment)
        installed = {path.relative_to(destination).as_posix(): path.read_bytes()
                     for path in destination.rglob("*") if path.is_file()}
        self.assertEqual(installed, self.archive_payload(baseline))
        self.assert_manifest(installed)

    def test_handle_metadata_changes_during_read_are_rejected(self) -> None:
        for field in ("st_size", "st_mtime_ns", "st_ctime_ns"):
            with self.subTest(field=field):
                self.assert_metadata_rejected(f"handle:{field}", "reading")

    def test_path_metadata_changes_during_read_are_rejected(self) -> None:
        for field in ("st_size", "st_mtime_ns", "st_ctime_ns"):
            with self.subTest(field=field):
                self.assert_metadata_rejected(f"path:{field}", "reading")

    def test_stable_cross_api_size_and_mtime_differences_are_rejected(self) -> None:
        for field in ("st_size", "st_mtime_ns"):
            with self.subTest(field=field):
                self.assert_metadata_rejected(f"cross:{field}", "reading")

    def test_source_identity_change_while_opening_is_rejected(self) -> None:
        self.assert_metadata_rejected("opened-identity", "opening")

    def test_source_identity_change_after_read_is_rejected(self) -> None:
        self.assert_metadata_rejected("current-identity", "reading")

    def test_current_checkout_keeps_linked_docs_examples_and_activation_contract(self) -> None:
        output = self.base / "actual checkout release"
        self.run_cli(REPOSITORY / "tools/build_release.py", "--output-dir", output)
        version = (REPOSITORY / "VERSION").read_text(encoding="utf-8").strip()
        payload = self.archive_payload(output / f"super_writer-v{version}-skill.zip")
        self.assert_manifest(payload)
        for name in ("CONTRIBUTING.md", "README.md", "README.en.md", "docs/validation.md",
                     "DATA_LICENSE", "THIRD_PARTY_NOTICES.md", "references/writing-library.json",
                     "references/venue-profiles.json", "examples/academic-style/cases.json",
                     "docs/usage.md", "examples/synthetic-study/manuscript.tex",
                     "examples/synthetic-study/materials/results.csv"):
            self.assertEqual(payload[name], (REPOSITORY / name).read_bytes(), name)
        self.assertIn("name: super-writer", payload["SKILL.md"].decode("utf-8").splitlines())
        self.assertIn(b"CONTRIBUTING.md", payload["README.md"])
        activation = json.loads(payload["evals/activation.json"])
        self.assertEqual(activation["skill"], "super-writer")
        self.assertGreaterEqual(sum(case["should_activate"] is True
                                    for case in activation["activation_cases"]), 2)
        self.assertGreaterEqual(sum(case["should_activate"] is False
                                    for case in activation["activation_cases"]), 2)

    def test_default_output_is_dist_in_working_directory(self) -> None:
        self.run_cli(self.repo / "tools/build_release.py")
        self.assertTrue((self.cwd / "dist" / ARCHIVE_NAME).is_file())
        self.assertFalse((self.repo / "dist").exists())

    def test_installed_payload_matches_release_and_cli_runs_with_spaces(self) -> None:
        payload = self.archive_payload(self.build())
        destination = self.install()
        installed = {path.relative_to(destination).as_posix(): path.read_bytes()
                     for path in destination.rglob("*") if path.is_file()}
        self.assertEqual(installed, payload)
        self.assert_manifest(installed)
        result = self.run_cli(destination / "scripts/material_inventory.py", "--help")
        self.assertIn("usage:", result.stdout.lower())
        result = self.run_cli(destination / "scripts/writing_lookup.py", "显著提升", "--kind", "usage_note", "--limit", "1", "--format", "ids")
        self.assertEqual(result.stdout.strip(), "general.usage-note.significant.001")
        result = self.run_cli(destination / "scripts/venue_profile.py", "--id", "eccv-2026-main-rebuttal", "--format", "json")
        self.assertEqual(json.loads(result.stdout)["profiles"][0]["body_pages"], 1)
        result = self.run_cli(destination / "scripts/smoke_test.py")
        self.assertIn("Cases: 11 passed, 0 failed", result.stdout)
        self.assertEqual(result.stdout.count("[PASS]"), 11)
        self.assertEqual([path.name for path in destination.parent.iterdir()], ["super-writer"])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_explicit_destination_and_discoverable_basename_are_required(self) -> None:
        script = self.repo / "tools/install_skill.py"
        result = self.run_cli(script, success=False)
        self.assertIn("--destination", result.stderr)
        for name in ("super_writer", "paper-spine", "arbitrary", ""):
            with self.subTest(name=name):
                self.run_cli(script, "--destination", name, success=False)
        self.run_cli(script, "--destination", self.base / "super-writer", "--force", success=False)
        self.assertEqual(list(self.cwd.iterdir()), [])
        self.assertEqual(list(self.home.iterdir()), [])
        self.assertFalse((self.base / "super-writer").exists())

    def test_relative_and_tilde_destinations_are_explicitly_supported(self) -> None:
        self.run_cli(self.repo / "tools/install_skill.py", "--destination", "relative host/super-writer")
        self.assertTrue((self.cwd / "relative host/super-writer/SKILL.md").is_file())
        self.run_cli(self.repo / "tools/install_skill.py", "--destination", "~/temporary skills/super-writer")
        self.assertTrue((self.home / "temporary skills/super-writer/SKILL.md").is_file())

    def test_existing_empty_directory_is_not_replaced(self) -> None:
        destination = self.base / "existing host/super-writer"
        destination.mkdir(parents=True)
        before = destination.stat()
        self.install(destination, success=False)
        self.assertTrue(os.path.samestat(before, destination.stat()))
        self.assertEqual(list(destination.iterdir()), [])

    def test_existing_install_and_existing_file_are_unchanged(self) -> None:
        destination = self.install()
        marker = destination / "user-owned.txt"
        marker.write_text("preserve me", encoding="utf-8")
        before = {path.relative_to(destination): path.read_bytes()
                  for path in destination.rglob("*") if path.is_file()}
        self.install(destination, success=False)
        after = {path.relative_to(destination): path.read_bytes()
                 for path in destination.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        target_file = self.base / "super-writer"
        target_file.write_bytes(b"existing file")
        self.install(target_file, success=False)
        self.assertEqual(target_file.read_bytes(), b"existing file")

    def test_existing_and_dangling_target_symlinks_are_not_followed(self) -> None:
        for dangling in (False, True):
            with self.subTest(dangling=dangling):
                parent = self.base / f"linked host {dangling}"
                parent.mkdir()
                outside = self.base / f"outside target {dangling}"
                if not dangling:
                    outside.mkdir()
                    (outside / "preserve.txt").write_bytes(b"existing")
                target = parent / "super-writer"
                target.symlink_to(outside, target_is_directory=True)
                original_link = target.readlink()
                original_identity = target.lstat()
                self.install(target, success=False)
                self.assertTrue(target.is_symlink())
                self.assertEqual(target.readlink(), original_link)
                self.assertTrue(os.path.samestat(original_identity, target.lstat()))
                if dangling:
                    self.assertFalse(outside.exists())
                else:
                    self.assertEqual((outside / "preserve.txt").read_bytes(), b"existing")
                    self.assertEqual(len(list(outside.iterdir())), 1)

    def test_private_environment_and_generated_files_are_excluded(self) -> None:
        forbidden = (
            "private_notes.txt", "credentials.json", ".env", ".git/config",
            ".venv/pyvenv.cfg", "paper_rewriting_output/final_paper/main.tex",
            "private/manuscript.md", "tests/private_fixture.txt", "tools/local_notes.txt",
            "scripts/__pycache__/module.cpython-310.pyc", "scripts/cache.pyc",
            "scripts/stale.pyo", "references/.env.local", "docs/.git/config",
            "docs/venv/bin/python", "docs/env/passwords.txt", "docs/private/notes.md",
            "docs/custom environment/pyvenv.cfg", "docs/custom environment/bin/python",
            "examples/paper_rewriting_output/final_paper/main.tex",
            "examples/.venv/pyvenv.cfg", "examples/secrets/api.txt",
            "references/client.key", "references/client.pem",
        )
        for name in forbidden:
            self.write(name, "PRIVATE-TEST-SENTINEL\n")
        self.write("docs/public.txt", "public")
        payload = self.archive_payload(self.build())
        self.assertEqual(payload["docs/public.txt"], b"public")
        self.assertTrue(set(forbidden).isdisjoint(payload))
        self.assertFalse(any(b"PRIVATE-TEST-SENTINEL" in data for data in payload.values()))
        destination = self.install()
        for name in forbidden:
            self.assertFalse((destination / name).exists(), name)
        self.assertFalse((destination / "tools").exists())
        self.assertFalse((destination / "tests").exists())
        self.assert_manifest(payload)

    def test_optional_documentation_can_be_absent(self) -> None:
        for name in ("README.md", "README.en.md", "CONTRIBUTING.md"):
            (self.repo / name).unlink()
        for name in ("docs", "examples"):
            shutil.rmtree(self.repo / name)
        payload = self.archive_payload(self.build())
        self.assertIn("SKILL.md", payload)
        self.assertIn("evals/activation.json", payload)
        self.assertNotIn("README.md", payload)
        self.assert_manifest(payload)
        self.install()

    def test_readme_requires_its_contributing_companion(self) -> None:
        (self.repo / "CONTRIBUTING.md").unlink()
        self.assert_rejected_source()

    def test_corpus_requires_data_license_and_third_party_notices(self) -> None:
        for name in ("DATA_LICENSE", "THIRD_PARTY_NOTICES.md"):
            with self.subTest(name=name):
                path = self.repo / name
                data = path.read_bytes()
                path.unlink()
                try:
                    self.assert_rejected_source()
                finally:
                    path.write_bytes(data)

    def test_missing_required_source_fails_without_creating_output(self) -> None:
        for name in ("SKILL.md", "LICENSE", "VERSION", "UPSTREAM.md", "skill-card.md",
                     "agents/openai.yaml", "scripts/smoke_test.py", "evals/activation.json"):
            with self.subTest(name=name):
                path = self.repo / name
                data = path.read_bytes()
                path.unlink()
                try:
                    self.assert_rejected_source()
                finally:
                    path.write_bytes(data)

    def test_invalid_version_cannot_escape_or_name_a_release(self) -> None:
        for version in ("", "../escape", "1.0.0\n../escape", "1.0", "v1.0.0", "01.0.0"):
            with self.subTest(version=version):
                self.write("VERSION", version)
                self.assert_rejected_source()

    def test_wrong_allowlisted_source_types_are_rejected(self) -> None:
        path = self.repo / "LICENSE"
        path.unlink()
        path.mkdir()
        self.assert_rejected_source()

    def test_source_file_symlinks_inside_outside_and_dangling_are_rejected(self) -> None:
        outside = self.base / "outside secret.txt"
        outside.write_bytes(b"outside private data")
        for target in (self.repo / "PATTERNS.md", outside, self.base / "missing"):
            with self.subTest(target=target):
                link = self.repo / "references/linked.md"
                link.symlink_to(target)
                try:
                    self.assert_rejected_source()
                finally:
                    link.unlink()
        self.assertEqual(outside.read_bytes(), b"outside private data")

    def test_source_directory_and_root_file_symlinks_are_rejected(self) -> None:
        outside = self.base / "outside documents"
        outside.mkdir()
        (outside / "private.txt").write_bytes(b"outside")
        link = self.repo / "docs/linked directory"
        link.symlink_to(outside, target_is_directory=True)
        self.assert_rejected_source()
        link.unlink()
        (self.repo / "LICENSE").unlink()
        (self.repo / "LICENSE").symlink_to(outside / "private.txt")
        self.assert_rejected_source()
        self.assertEqual((outside / "private.txt").read_bytes(), b"outside")

    def test_outside_hard_link_is_rejected(self) -> None:
        outside = self.base / "hard link secret.txt"
        outside.write_bytes(b"outside")
        os.link(outside, self.repo / "references/hard_link.txt")
        self.assert_rejected_source()
        self.assertEqual(outside.read_bytes(), b"outside")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO test requires POSIX")
    def test_special_source_file_is_rejected_without_hanging(self) -> None:
        os.mkfifo(self.repo / "references/pipe")
        self.assert_rejected_source()

    @unittest.skipIf(os.name == "nt", "Windows disallows these filenames at creation")
    def test_unsafe_manifest_or_archive_names_are_rejected(self) -> None:
        for name in ("docs/line\nbreak.md", "docs/back\\slash.md", "docs/stream:private.md"):
            with self.subTest(name=name):
                path = self.write(name, "unsafe name")
                try:
                    self.assert_rejected_source()
                finally:
                    path.unlink()

    def test_install_publication_failure_rolls_back_only_new_entries(self) -> None:
        parent = self.base / "shared skill host"
        parent.mkdir()
        sentinel = parent / "keep existing directory"
        sentinel.mkdir()
        (sentinel / "user.txt").write_bytes(b"untouched")
        destination = parent / "super-writer"
        result = self.run_cli(
            self.repo / "tools/install_skill.py", "--destination", destination, success=False,
            environment={"DISTRIBUTION_FAIL_PATH": str(destination / "references/citation.md")},
        )
        self.assertIn("injected publication failure", result.stderr)
        self.assertFalse(os.path.lexists(destination))
        self.assertEqual(list(parent.iterdir()), [sentinel])
        self.assertEqual((sentinel / "user.txt").read_bytes(), b"untouched")

    def test_two_installers_do_not_replace_each_other(self) -> None:
        (self.repo / "SKILL.md").write_bytes(self.metadata["SKILL.md"].replace("\n", "\r\n").encode("utf-8"))
        destination = self.base / "concurrent host/super-writer"
        command = [sys.executable, "-B", str(self.repo / "tools/install_skill.py"),
                   "--destination", str(destination)]
        processes = []
        try:
            for _ in range(2):
                processes.append(subprocess.Popen(
                    command, cwd=self.cwd,
                    env={**self.environment, "DISTRIBUTION_NO_PROCESS": "1"},
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                ))
            outputs = [process.communicate(timeout=120) for process in processes]
            self.assertEqual(sorted(process.returncode for process in processes), [0, 1], outputs)
            installed = {path.relative_to(destination).as_posix(): path.read_bytes()
                         for path in destination.rglob("*") if path.is_file()}
            self.assert_manifest(installed)
            self.assertEqual(installed["SKILL.md"], (self.repo / "SKILL.md").read_bytes())
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                process.communicate()

    def test_release_output_cannot_pollute_distributed_sources(self) -> None:
        output = self.repo / "docs/release artifacts"
        self.build(output, success=False)
        self.assertFalse(output.exists())

    def test_release_output_symlink_is_not_followed(self) -> None:
        output = self.base / "release output"
        output.mkdir()
        outside = self.base / "preserve archive.txt"
        outside.write_bytes(b"untouched")
        archive = output / ARCHIVE_NAME
        archive.symlink_to(outside)
        self.build(output, success=False)
        self.assertTrue(archive.is_symlink())
        self.assertEqual(outside.read_bytes(), b"untouched")
        self.assertEqual(list(output.iterdir()), [archive])


if __name__ == "__main__":
    unittest.main()
