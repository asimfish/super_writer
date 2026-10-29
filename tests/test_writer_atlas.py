"""Engineering atlas generation contracts; not an editorial-quality oracle."""

from __future__ import annotations

import copy
from html.parser import HTMLParser
import json
from pathlib import Path, PureWindowsPath
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import render_writer_atlas as atlas


def cli(output: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-B", str(ROOT / "tools/render_writer_atlas.py"),
                           "--output-dir", str(output), *flags],
                          cwd=tempfile.gettempdir(), capture_output=True, text=True, timeout=30)


class Elements(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.elements: list[tuple[str, dict]] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data: str) -> None:
        self.text.append(data)


class AtlasTests(unittest.TestCase):
    def test_cross_drive_owner_links_use_encoded_file_uris(self) -> None:
        class ExistingWindowsPath(PureWindowsPath):
            def is_file(self) -> bool:
                return True

        with patch.object(atlas, "ROOT", ExistingWindowsPath("D:/Writer Repo")):
            actual = atlas.link("references/build.md", PureWindowsPath("C:/Temp/atlas"))
        self.assertEqual(actual, "file:///D:/Writer%20Repo/references/build.md")

    def test_same_drive_owner_links_remain_relative(self) -> None:
        with patch.object(atlas.os.path, "relpath", return_value="../references/build.md"):
            self.assertEqual(atlas.link("references/build.md", ROOT / "docs"), "../references/build.md")

    def test_deterministic_render_and_nonwriting_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp).resolve() / "atlas"
            result = cli(output)
            self.assertEqual(result.returncode, 0, result.stderr)
            snapshots = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in output.rglob("*") if p.is_file()}
            self.assertEqual(cli(output, "--check").returncode, 0)
            self.assertEqual({p: (p.read_bytes(), p.stat().st_mtime_ns) for p in snapshots}, snapshots)
            first = atlas.render(output)
            self.assertEqual(first, atlas.render(output))

    def test_missing_check_does_not_create_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp).resolve() / "missing"
            result = cli(output, "--check")
            self.assertEqual(result.returncode, 1)
            self.assertFalse(output.exists())

    def test_drift_fails_without_repairing_the_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp).resolve() / "atlas"
            result = cli(output)
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output / "writer-atlas.html"
            html.write_text("changed output", encoding="utf-8")
            self.assertEqual(cli(output, "--check").returncode, 1)
            self.assertEqual(html.read_text(), "changed output")

    def test_svg_has_actual_owner_links_and_separate_flow_roles(self) -> None:
        svg = ET.fromstring(atlas.render(ROOT / "docs")["assets/writer-flow.svg"])
        nodes = [e for e in svg.iter() if "data-node" in e.attrib]
        edges = [e for e in svg.iter() if "data-edge" in e.attrib]
        self.assertEqual(len(nodes), 8)
        self.assertEqual(len(edges), 9)
        for node in nodes:
            self.assertTrue((ROOT / "docs/assets" / node.attrib["href"]).is_file())
        classes = {e.attrib["data-edge"]: e.attrib["class"].split() for e in edges}
        self.assertIn("guide", classes["spec-planning"])
        self.assertIn("repair", classes["readback-owner"])
        self.assertIn("guide", classes["draft-quality"])

    def test_all_records_keep_full_conditions_exceptions_and_contrasts(self) -> None:
        html = atlas.render(ROOT / "docs")["writer-atlas.html"]
        parsed = Elements()
        parsed.feed(html)
        records = [a for tag, a in parsed.elements if tag == "details" and a.get("class") == "record"]
        spec = json.loads(atlas.writing_lookup.AI_SPEC.read_text(encoding="utf-8"))
        self.assertEqual({r["data-id"] for r in records}, {e["id"] for e in spec["entries"]})
        by_id = {r["data-id"]: r for r in records}
        text = "\n".join(parsed.text)
        for entry in spec["entries"]:
            self.assertEqual(by_id[entry["id"]]["id"], entry["id"])
            self.assertEqual(json.loads(by_id[entry["id"]]["data-topics"]), entry["topics"])
            self.assertEqual(json.loads(by_id[entry["id"]]["data-levels"]), entry["levels"])
            for field in ("meaning", "guidance", "avoid", "example_context"):
                self.assertIn(entry[field], text)
            for field in ("conditions", "exceptions", "evidence_required", "examples"):
                for value in entry[field]:
                    self.assertIn(value, text)
            for example in entry["counter_examples"]:
                self.assertIn(example["text"], text)
                self.assertIn(example["why"], text)
            for note in entry["source_notes"]:
                self.assertIn(note["location"], text)
                self.assertIn(note["observation"], text)
            for value in entry.get("discourse", {}).values():
                self.assertIn(value, text)

    def test_filter_options_are_derived_from_canonical_facets(self) -> None:
        html = atlas.render(ROOT / "docs")["writer-atlas.html"]
        spec = json.loads(atlas.writing_lookup.AI_SPEC.read_text())
        for field in ("topics", "levels", "kinds"):
            for value in spec["taxonomy"][field]:
                self.assertIn(f'<option value="{value}">', html)

    def test_dictionary_data_is_escaped_not_executed(self) -> None:
        spec = json.loads(atlas.writing_lookup.AI_SPEC.read_text(encoding="utf-8"))
        spec = copy.deepcopy(spec)
        payload = '<img src="https://example.com/secret" onerror="alert(1)"> & <script>bad()</script>'
        spec["entries"][0]["guidance"] = payload
        html = atlas.records_html(spec, ROOT / "docs")
        parsed = Elements()
        parsed.feed(html)
        self.assertFalse(any(tag in {"img", "script"} for tag, _ in parsed.elements))
        self.assertFalse(any("onerror" in attrs for _, attrs in parsed.elements))
        self.assertIn(payload, "".join(parsed.text))

    def test_related_card_drift_is_rejected(self) -> None:
        spec = json.loads(atlas.writing_lookup.AI_SPEC.read_text(encoding="utf-8"))
        spec["entries"][0]["related_library_ids"] = ["missing.card"]
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "spec.json"
            source.write_text(json.dumps(spec), encoding="utf-8")
            with patch.object(atlas.writing_lookup, "AI_SPEC", source):
                with self.assertRaisesRegex(ValueError, "Related card"):
                    atlas.render(ROOT / "docs")

    @unittest.skipIf(sys.platform == "win32", "Creating symlinks requires Windows privileges")
    def test_symlink_output_or_parent_fails_before_any_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            actual = base / "actual"
            actual.mkdir()
            alias = base / "alias"
            alias.symlink_to(actual, target_is_directory=True)
            self.assertEqual(cli(alias).returncode, 1)
            self.assertEqual(list(actual.iterdir()), [])
            output = base / "atlas"
            output.mkdir()
            (output / "assets").symlink_to(actual, target_is_directory=True)
            self.assertEqual(cli(output).returncode, 1)
            self.assertFalse((output / "writer-atlas.html").exists())
            self.assertEqual(list(actual.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
