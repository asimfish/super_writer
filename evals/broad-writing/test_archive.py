import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import archive


class ArchiveTests(unittest.TestCase):
    def test_missing_inputs_leave_no_partial_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "output"
            with patch.object(archive, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "Incomplete archive inputs"):
                    archive.main(target)
            self.assertFalse(target.exists())

    def test_existing_archive_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(FileExistsError, "Archive already exists"):
                archive.main(Path(temp))


if __name__ == "__main__":
    unittest.main()
