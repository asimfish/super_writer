"""Test the bounded archive reader without network or a TeX installation."""

from __future__ import annotations

import hashlib
import io
from pathlib import Path
import stat
import sys
import unittest
import warnings
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_template_compatibility import MAX_STYLE, check_pdf_text, style_files


class TemplateSourceTests(unittest.TestCase):
    def test_expected_rendered_content_accepts_small_caps_extraction(self) -> None:
        check_pdf_text("fixture", "S UPER W RITER T EMPLATE 0.1083 0.0851 Hastie", "Pages: 1")

    def test_visible_template_error_fails_even_after_successful_compilation(self) -> None:
        with self.assertRaisesRegex(ValueError, "unexpected rendered marker"):
            check_pdf_text("icml2026", "Super Writer Template 0.1083 0.0851 Hastie AUTHORERR: Missing author", "")

    def test_identity_and_unresolved_markers_in_text_or_metadata_fail(self) -> None:
        valid = "Super Writer Template 0.1083 0.0851 Hastie"
        for marker in ("IdentitySentinel", "AffiliationSentinel", "identity@example.invalid", "[?]", "??"):
            for text, metadata in ((valid + marker, ""), (valid, marker)):
                with self.subTest(marker=marker, metadata=bool(metadata)):
                    with self.assertRaisesRegex(ValueError, "unexpected rendered marker"):
                        check_pdf_text("fixture", text, metadata)

    def archive(self, entries: list[tuple[str | zipfile.ZipInfo, bytes]]) -> tuple[bytes, dict]:
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                for name, data in entries:
                    archive.writestr(name, data)
        data = stream.getvalue()
        return data, {"id": "fixture", "sha256": hashlib.sha256(data).hexdigest(),
                      "archive_prefix": "upstream/", "files": ["example.sty"]}

    def test_only_named_styles_are_read_and_unrelated_members_are_ignored(self) -> None:
        data, spec = self.archive([("upstream/example.sty", b"style"), ("../private", b"ignored")])
        self.assertEqual(style_files(data, spec), {"example.sty": b"style"})

    def test_changed_remote_bytes_fail_the_pin(self) -> None:
        data, spec = self.archive([("upstream/example.sty", b"style")])
        spec["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            style_files(data, spec)

    def test_missing_member_is_not_silently_accepted(self) -> None:
        data, spec = self.archive([])
        with self.assertRaisesRegex(ValueError, "Missing or duplicate"):
            style_files(data, spec)

    def test_duplicate_style_member_is_rejected(self) -> None:
        data, spec = self.archive([("upstream/example.sty", b"one"), ("upstream/example.sty", b"two")])
        with self.assertRaisesRegex(ValueError, "Missing or duplicate"):
            style_files(data, spec)

    def test_symlink_style_is_rejected(self) -> None:
        entry = zipfile.ZipInfo("upstream/example.sty")
        entry.create_system = 3
        entry.external_attr = (stat.S_IFLNK | 0o777) << 16
        data, spec = self.archive([(entry, b"../../outside")])
        with self.assertRaisesRegex(ValueError, "Invalid style"):
            style_files(data, spec)

    def test_oversized_uncompressed_member_is_rejected(self) -> None:
        data, spec = self.archive([("upstream/example.sty", b"x" * (MAX_STYLE + 1))])
        with self.assertRaisesRegex(ValueError, "Invalid style"):
            style_files(data, spec)

    def test_output_filename_cannot_escape_work_directory(self) -> None:
        data, spec = self.archive([])
        spec["files"] = ["../example.sty"]
        with self.assertRaisesRegex(ValueError, "flat style"):
            style_files(data, spec)


if __name__ == "__main__":
    unittest.main()
