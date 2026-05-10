import csv
import io
import json
import unittest

from report import REPORT_SCHEMA_VERSION, _format_period, collect_records, render_report


class TestReportContracts(unittest.TestCase):
    def test_all_section_record_counts_and_order(self):
        # planets: 8 velocity + 8 period = 16
        # earth:   2 velocity + 2 period + 1 distance + 1 escape velocity = 6
        # concepts: 2
        # mars-base: 8
        # transfers: 2 transfers × 3 records (departure, arrival, total) = 6
        # total: 38
        records = collect_records("all")
        sections = [record.section for record in records]

        self.assertEqual(len(records), 38)
        self.assertEqual(sections.count("planets"), 16)
        self.assertEqual(sections.count("earth"), 6)
        self.assertEqual(sections.count("concepts"), 2)
        self.assertEqual(sections.count("mars-base"), 8)
        self.assertEqual(sections.count("transfers"), 6)
        self.assertEqual(records[0].label, "Mercury orbital velocity")
        self.assertEqual(records[-1].label, "Earth-Mars total Δv")

    def test_json_contract_shape_and_types(self):
        payload = json.loads(render_report("earth", "json"))
        self.assertEqual(payload["section"], "earth")
        self.assertEqual(payload["report_schema_version"], REPORT_SCHEMA_VERSION)
        self.assertIn("generated_at_utc", payload)
        self.assertIsInstance(payload["records"], list)
        self.assertEqual(len(payload["records"]), 6)

        required_fields = {"section", "label", "value", "value_num", "unit", "note"}
        for record in payload["records"]:
            self.assertEqual(set(record.keys()), required_fields)
            self.assertIsInstance(record["section"], str)
            self.assertIsInstance(record["label"], str)
            self.assertIsInstance(record["value"], str)
            self.assertTrue(
                isinstance(record["value_num"], (int, float)) or record["value_num"] is None
            )
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
        self.assertEqual(len(payload["records"]), 38)
        self.assertIn("data_sources", payload)
        self.assertIn("assumptions", payload)


class TestFormatPeriod(unittest.TestCase):
    def test_minutes_branch(self):
        value, unit = _format_period(0.5)  # 30 minutes
        self.assertEqual(value, "30")
        self.assertEqual(unit, "minutes")

    def test_exactly_one_hour(self):
        value, unit = _format_period(1.0)
        self.assertEqual(value, "1.0")
        self.assertEqual(unit, "hours")

    def test_exactly_two_days(self):
        value, unit = _format_period(48.0)
        self.assertEqual(value, "2.0")
        self.assertEqual(unit, "Earth days")

    def test_exactly_730_days(self):
        value, unit = _format_period(730 * 24)  # 730 / 365.25 ≈ 2.0 years
        self.assertEqual(value, "2.0")
        self.assertEqual(unit, "Earth years")

    def test_multi_year(self):
        value, unit = _format_period(164.8 * 365.25 * 24)  # Neptune ~164.8 years
        self.assertAlmostEqual(float(value), 164.8, delta=0.2)
        self.assertEqual(unit, "Earth years")

    def test_below_years_threshold_is_days(self):
        # 729.9 days is just under the 2-year threshold
        value, unit = _format_period(729.9 * 24)
        self.assertEqual(unit, "Earth days")

    def test_at_years_threshold_is_years(self):
        # 730.5 days is just over the 730-day threshold (_YEARS_THRESHOLD_DAYS = 730.0)
        value, unit = _format_period(730.5 * 24)
        self.assertEqual(unit, "Earth years")


if __name__ == "__main__":
    unittest.main()
