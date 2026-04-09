import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class TestMainCLI(unittest.TestCase):
    def _run_main_with_args(self, args):
        output = io.StringIO()
        with patch("sys.argv", ["main.py", *args]):
            with redirect_stdout(output):
                main.main()
        return output.getvalue()

    def test_planets_section_only(self):
        output = self._run_main_with_args(["--section", "planets"])
        self.assertIn("--PLANET ORBITAL VELOCITY DATA--", output)
        self.assertNotIn("--EARTH ORBITAL SYSTEMS--", output)

    def test_earth_section_only(self):
        output = self._run_main_with_args(["--section", "earth"])
        self.assertIn("--EARTH ORBITAL SYSTEMS--", output)
        self.assertNotIn("--CONCEPT STATIONS--", output)

    def test_all_sections(self):
        output = self._run_main_with_args([])
        self.assertIn("--PLANET ORBITAL VELOCITY DATA--", output)
        self.assertIn("--EARTH ORBITAL SYSTEMS--", output)
        self.assertIn("--CONCEPT STATIONS--", output)
        self.assertIn("--MARS BASE CONCEPT--", output)

    def test_json_format(self):
        output = self._run_main_with_args(["--format", "json", "--section", "planets"])
        self.assertIn('"section": "planets"', output)
        self.assertIn('"report_schema_version": "1.0.0"', output)
        self.assertIn('"records"', output)
        self.assertIn("Mercury orbital velocity", output)

    def test_csv_format(self):
        output = self._run_main_with_args(["--format", "csv", "--section", "earth"])
        self.assertIn("section,label,value,value_num,unit,note", output)
        self.assertIn("earth,Moon orbital velocity", output)

    def test_output_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "report.json")
            output = self._run_main_with_args(
                ["--format", "json", "--section", "planets", "--output", output_path]
            )
            self.assertIn(f"Report written to {output_path}", output)
            with open(output_path, "r", encoding="utf-8") as report_file:
                content = report_file.read()
            self.assertIn('"section": "planets"', content)


if __name__ == "__main__":
    unittest.main()
