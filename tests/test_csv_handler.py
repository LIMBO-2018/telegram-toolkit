import csv
import tempfile
import unittest
from pathlib import Path

from telegram_toolkit.utils.csv_handler import load_members_from_csv, merge_csv_files


class TestCsvHandler(unittest.TestCase):
    def _write(self, text):
        handle = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8", newline="")
        handle.write(text)
        handle.close()
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def test_load_valid_rows(self):
        path = self._write(
            "id,access_hash,username,name,group\n"
            "123,456,alice,Alice,Test\n"
        )
        rows = load_members_from_csv(path)
        self.assertEqual(rows[0]["id"], 123)
        self.assertEqual(rows[0]["access_hash"], 456)

    def test_invalid_rows_are_skipped(self):
        path = self._write(
            "id,access_hash,username,name,group\n"
            "bad,456,bob,Bob,Test\n"
            "123,789,alice,Alice,Test\n"
        )
        rows = load_members_from_csv(path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], 123)

    def test_merge_deduplicates_ids(self):
        first = self._write(
            "id,access_hash,username,name,group\n"
            "123,456,alice,Alice,Test\n"
        )
        second = self._write(
            "id,access_hash,username,name,group\n"
            "123,456,alice,Alice,Test\n"
            "456,789,bob,Bob,Test\n"
        )
        output = tempfile.NamedTemporaryFile(suffix=".csv", delete=False).name
        self.addCleanup(lambda: Path(output).unlink(missing_ok=True))
        self.assertTrue(merge_csv_files(first, second, output))
        with open(output, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
