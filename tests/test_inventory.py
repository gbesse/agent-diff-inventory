import subprocess
import tempfile
import unittest
from pathlib import Path

from inventory import compare, snapshot


class InventoryTests(unittest.TestCase):
    def test_tracks_script_edits_and_untracked_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "one.py").write_text("before")
            (root / "gone.txt").write_text("removed")
            before = snapshot(root)
            (root / "one.py").write_text("after")
            (root / "gone.txt").unlink()
            (root / "new.txt").write_text("new")
            result = compare(before, snapshot(root))
            self.assertEqual(result["modified"], ["one.py"])
            self.assertEqual(result["deleted"], ["gone.txt"])
            self.assertEqual(result["added"], ["new.txt"])


if __name__ == "__main__":
    unittest.main()
