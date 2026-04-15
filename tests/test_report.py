import csv
import io
import json
import unittest

from report import REPORT_SCHEMA_VERSION, collect_records, render_report


class TestReportContracts(unittest.TestCase):
    def test_all_section_record_counts_and_order(self):
        # planets: 8 velocity + 8 period = 16
        # earth:   2 velocity + 2 period + 1 distance = 5
        # concepts: 2
        # mars-base: 8
        # total: 31
        records = collect_records("all")
        sections = [record.section for record in records]

        self.assertEqual(len(records), 31)
        self.assertEqual(sections.count("planets"), 16)
        self.assertEqual(sections.count("earth"), 5)
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
        self.assertEqual(len(payload["records"]), 5)

        required_fields = {"section", "label", "value", "value_num", "unit", "note"}
        for record in payload["records"]:
            self.assertEqual(set(record.keys()), required_fields)
            self.assertIsInstance(record["section"], str)
            self.assertIsInstance(record["label"], str)
            self.assertIsInstance(record["value"], str)
            self.assertIn(type(record["value_num"]), (int, float, type(None)))
            self.assertIsInstance(record["unit"], str)
            self.assertIsInstance(record["note"], str)

    def test_json_contains_data_sources(self):
        payload = json.loads(render_report("planets", "json"))
        self.assertIn("data_sources", payload)
        sources = payload["data_sources"]
        self.assertIn("gravitational_constant", sources)
        self.assertIn("planetary_semi_major_axes", sources)
        self.assertIn("data_validation_date", sources)

    def test_json_contains_assumptions(self):
        payload = json.loads(render_report("planets", "json"))
        self.assertIn("assumptions", payload)
        self.assertIsInstance(payload["assumptions"], list)
        self.assertGreater(len(payload["assumptions"]), 0)

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

    def test_csv_none_exported_as_empty_field(self):
        csv_text = render_report("mars-base", "csv")
        reader = csv.DictReader(io.StringIO(csv_text))
        rows = list(reader)
        for row in rows:
            self.assertNotEqual(
                row["value_num"], "None",
                "value_num None must export as empty string, not the string 'None'",
            )

    def test_invalid_section_raises_value_error(self):
        with self.assertRaises(ValueError):
            collect_records("asteroids")

        with self.assertRaises(ValueError):
            render_report("asteroids", "text")

    def test_invalid_output_format_raises_value_error(self):
        with self.assertRaises(ValueError):
            render_report("planets", "yaml")

    def test_full_pipeline_produces_valid_json(self):
        raw = render_report("all", "json")
        payload = json.loads(raw)
        self.assertEqual(payload["report_schema_version"], REPORT_SCHEMA_VERSION)
        self.assertEqual(payload["section"], "all")
        self.assertEqual(len(payload["records"]), 31)
        self.assertIn("data_sources", payload)
        self.assertIn("assumptions", payload)


if __name__ == "__main__":
    unittest.main()
