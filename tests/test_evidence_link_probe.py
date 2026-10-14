"""Development packet integrity, not semantic grading or writing-quality gains."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "evals/evidence-link"


def module():
    spec = importlib.util.spec_from_file_location("evidence_link_probe", PACK / "probe.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class EvidenceLinkProbeTests(unittest.TestCase):
    def test_resources_exist(self):
        for path in (PACK / "probe.py", PACK / "cases.json", PACK / "README.md",
                     ROOT / "references/evidence-link-candidate.md"):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file(), f"Missing candidate resource: {path}")

    def test_pairs_change_one_input_and_require_different_editorial_decisions(self):
        probes = module().load_probes()
        self.assertEqual(len(probes), 16)
        self.assertEqual(len({p["id"] for p in probes}), 16)
        families = {}
        for probe in probes:
            families.setdefault(probe["family"], []).append(probe)
            self.assertTrue(probe["oracle"]["required_meanings"])
            self.assertTrue(probe["oracle"]["forbidden_meanings"])
            self.assertLessEqual(set(probe["oracle"]["selected_evidence_ids"]),
                                 set(probe["evidence"]))
        self.assertEqual(len(families), 8)
        for name, pair in families.items():
            with self.subTest(family=name):
                self.assertEqual(len(pair), 2)
                left, right = pair
                changes = sum(left[field] != right[field] for field in ("author_priority", "task"))
                changes += sum(left["evidence"][key] != right["evidence"][key]
                               for key in left["evidence"])
                self.assertEqual(changes, 1)
                self.assertNotEqual(left["oracle"], right["oracle"])
        self.assertGreaterEqual(len({p["domain"] for p in probes}), 5)
        self.assertEqual({p["unit"] for p in probes}, {"abstract", "methods", "results"})

    def test_conditions_share_every_writer_field_except_guidance(self):
        runner = module()
        for probe in runner.load_probes():
            with self.subTest(probe=probe["id"]):
                baseline = runner.build_packet(probe, "baseline")
                candidate = runner.build_packet(probe, "candidate")
                left = dict(baseline["writer_input"])
                right = dict(candidate["writer_input"])
                base_guides = left.pop("guidance")
                candidate_guides = right.pop("guidance")
                self.assertEqual(left, right)
                self.assertEqual(left["contract"]["words"], {"max": 120})
                self.assertEqual(candidate_guides[:-1], base_guides)
                self.assertEqual(candidate_guides[-1]["path"],
                                 "references/evidence-link-candidate.md")
                self.assertNotEqual(baseline["input_sha256"], candidate["input_sha256"])
                for packet in (baseline, candidate):
                    encoded = runner.canonical(packet["writer_input"])
                    self.assertEqual(hashlib.sha256(encoded).hexdigest(), packet["input_sha256"])
                    for guide in packet["writer_input"]["guidance"]:
                        self.assertEqual(guide["sha256"], hashlib.sha256(
                            guide["text"].encode("utf-8")).hexdigest())

    def test_writer_packet_cannot_leak_private_oracle_or_extra_fields(self):
        runner = module()
        probe = runner.load_probes()[0]
        probe["oracle"] = {"reason": "PRIVATE_ORACLE_SENTINEL"}
        probe["unexpected"] = "PRIVATE_EXTRA_SENTINEL"
        for condition in ("baseline", "candidate"):
            packet = runner.build_packet(probe, condition)
            output = json.dumps(packet)
            self.assertNotIn("PRIVATE_", output)
            self.assertNotIn("oracle", packet["writer_input"])
            self.assertEqual(packet["status"], "development_not_quality_evidence")
            self.assertEqual(packet["writer_input"]["evidence"], probe["evidence"])

    def test_bad_counterfactuals_and_unknown_evidence_are_rejected(self):
        runner = module()
        original = json.loads((PACK / "cases.json").read_text(encoding="utf-8"))
        mutations = []
        data = copy.deepcopy(original)
        data["families"][0]["probes"][0]["changes"] = {}
        mutations.append((data, "exactly one"))
        data = copy.deepcopy(original)
        data["families"][0]["probes"][0]["changes"] = {"evidence.UNKNOWN": "Changed"}
        mutations.append((data, "Unknown evidence"))
        data = copy.deepcopy(original)
        data["families"][0]["probes"][0]["changes"] = {"oracle": "Leak"}
        mutations.append((data, "Unknown change"))
        data = copy.deepcopy(original)
        data["families"][0]["probes"][0]["oracle"]["selected_evidence_ids"] = ["UNKNOWN"]
        mutations.append((data, "Unknown selected evidence"))
        data = copy.deepcopy(original)
        data["families"][0]["probes"][1]["id"] = data["families"][0]["probes"][0]["id"]
        mutations.append((data, "Duplicate probe"))
        data = copy.deepcopy(original)
        first = data["families"][0]["probes"][0]
        data["families"][0]["probes"][1]["changes"] = dict(first["changes"])
        mutations.append((data, "values must differ"))
        data = copy.deepcopy(original)
        data["families"][0]["probes"][1]["changes"] = {"task": "A different task"}
        mutations.append((data, "same input"))
        data = copy.deepcopy(original)
        data["families"][0]["probes"][0]["changes"] = {
            "author_priority": data["families"][0]["author_priority"]}
        mutations.append((data, "no-op"))
        for data, reason in mutations:
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                runner.expand_probes(data)

    def test_invalid_condition_never_silently_falls_back(self):
        runner = module()
        with self.assertRaisesRegex(ValueError, "Unknown condition"):
            runner.build_packet(runner.load_probes()[0], "typo")

    def test_packets_do_not_share_mutable_evidence_with_each_other_or_the_probe(self):
        runner = module()
        probe = runner.load_probes()[0]
        original = dict(probe["evidence"])
        baseline = runner.build_packet(probe, "baseline")
        candidate = runner.build_packet(probe, "candidate")
        candidate["writer_input"]["evidence"]["E1"] = "Caller-modified evidence"
        self.assertEqual(baseline["writer_input"]["evidence"], original)
        self.assertEqual(probe["evidence"], original)

    def test_packet_assembly_is_offline_and_does_not_write(self):
        runner = module()
        with patch("socket.socket", side_effect=AssertionError("Network forbidden")), \
                patch.object(Path, "write_text", side_effect=AssertionError("Writes forbidden")), \
                patch.object(Path, "write_bytes", side_effect=AssertionError("Writes forbidden")):
            packet = runner.build_packet(runner.load_probes()[0], "candidate")
        self.assertEqual(packet["writer_input"]["unit"], "abstract")

    def test_cli_is_relocatable_and_only_emits_the_requested_packet(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [sys.executable, str(PACK / "probe.py"), "--id", "E01-diversity",
                 "--condition", "candidate"], cwd=temporary, capture_output=True,
                text=True, encoding="utf-8", timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            packet = json.loads(result.stdout)
            self.assertEqual(packet["probe_id"], "E01-diversity")
            self.assertNotIn("oracle", packet["writer_input"])
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_cli_rejects_unknown_or_ambiguous_selection_without_traceback(self):
        for args in (["--id", "unknown", "--condition", "candidate"],
                     ["--id", "E01-diversity"],
                     ["--list", "--condition", "candidate"],
                     ["--id", "E01-diversity", "--condition", "typo"]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(PACK / "probe.py"), *args],
                                        capture_output=True, text=True, encoding="utf-8", timeout=30)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)

    def test_default_argument_transfer_remains_unchanged(self):
        self.assertEqual((ROOT / "references/argument-transfer.md").read_bytes(),
                         (ROOT / "evals/abstract-transfer/baseline/argument-transfer.md").read_bytes())

    def test_release_bundle_retains_a_self_contained_development_packet_path(self):
        with tempfile.TemporaryDirectory(prefix="evidence link bundle ") as temporary:
            base = Path(temporary)
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools/build_release.py"), "--output-dir", str(base / "release")],
                cwd=temporary, capture_output=True, text=True, encoding="utf-8", timeout=60,
                env={**os.environ, "PYTHONUTF8": "1"},
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            archive, = (base / "release").glob("*.zip")
            with zipfile.ZipFile(archive) as bundle:
                required = {"super-writer/" + path for path in (
                    "evals/evidence-link/probe.py", "evals/evidence-link/cases.json",
                    "evals/evidence-link/README.md", "references/evidence-link-candidate.md")}
                self.assertLessEqual(required, set(bundle.namelist()))
                bundle.extractall(base / "relocated")
            result = subprocess.run(
                [sys.executable, str(base / "relocated/super-writer/evals/evidence-link/probe.py"),
                 "--id", "E06-approximate-implementation", "--condition", "candidate"],
                cwd=temporary, capture_output=True, text=True, encoding="utf-8", timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            packet = json.loads(result.stdout)
            expected = module().build_packet(next(p for p in module().load_probes()
                                                  if p["id"] == packet["probe_id"]), "candidate")
            self.assertEqual(packet, expected)


if __name__ == "__main__":
    unittest.main()
