import csv
import io
import json
import unittest

from report import REPORT_SCHEMA_VERSION, collect_records, render_report


class TestReportContracts(unittest.TestCase):
    def test_all_section_record_counts_and_order(self):
        records = collect_records("all")
        sections = [record.section for record in records]

        self.assertEqual(len(records), 21)
        self.assertEqual(sections.count("planets"), 8)
        self.assertEqual(sections.count("earth"), 3)
        self.assertEqual(sections.count("concepts"), 2)
        self.assertEqual(sections.count("mars-base"), 8)
        self.assertEqual(records[0].label, "Mercury orbital velocity")
        self.assertEqual(records[-1].label, "Mission duration")

    def test_json_contract_shape_and_types(self):
        payload = json.loads(render_report("earth", "json"))
        self.assertEqual(payload["section"], "earth")
        self.assertEqual(payload["report_schema_version"], REPORT_SCHEMA_VERSION)
        self.assertIn("generated_at_utc", payload)
        self.assertIsInstance(payload["records"], list)
        self.assertEqual(len(payload["records"]), 3)

        required_fields = {"section", "label", "value", "value_num", "unit", "note"}
        for record in payload["records"]:
            self.assertEqual(set(record.keys()), required_fields)
            self.assertIsInstance(record["section"], str)
            self.assertIsInstance(record["label"], str)
            self.assertIsInstance(record["value"], str)
            self.assertIn(type(record["value_num"]), (int, float, type(None)))
            self.assertIsInstance(record["unit"], str)
            self.assertIsInstance(record["note"], str)

    def test_csv_contract_shape(self):
        csv_text = render_report("concepts", "csv")
        reader = csv.DictReader(io.StringIO(csv_text))
        rows = list(reader)

        self.assertEqual(
            reader.fieldnames, ["section", "label", "value", "value_num", "unit", "note"]
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["section"], "concepts")
        self.assertTrue(rows[0]["label"].startswith("Concept station"))

    def test_invalid_section_raises_value_error(self):
        with self.assertRaises(ValueError):
            collect_records("asteroids")

        with self.assertRaises(ValueError):
            render_report("asteroids", "text")

    def test_invalid_output_format_raises_value_error(self):
        with self.assertRaises(ValueError):
            render_report("planets", "yaml")


if __name__ == "__main__":
    unittest.main()
