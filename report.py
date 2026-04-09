import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from io import StringIO

from calculations import calculate_orbital_velocity, meters_to_km
from data import CONCEPT_STATIONS, EARTH_ORBITS, ISS_TO_MOON_DISTANCE, PLANETS

LABEL_WIDTH = 36
VALUE_WIDTH = 14
REPORT_TITLE = "PLANET ORBITAL SIMULATION & SPACE EXPLORATION GUIDE"
REPORT_SCHEMA_VERSION = "1.0.0"
SECTION_ORDER = ["planets", "earth", "concepts", "mars-base"]
VALID_SECTIONS = ["all", *SECTION_ORDER]
VALID_OUTPUT_FORMATS = ["text", "json", "csv"]
SECTION_TITLES = {
    "planets": "PLANET ORBITAL VELOCITY DATA",
    "earth": "EARTH ORBITAL SYSTEMS",
    "concepts": "CONCEPT STATIONS",
    "mars-base": "MARS BASE CONCEPT",
}


@dataclass
class MetricRecord:
    section: str
    label: str
    value: str
    value_num: float | None = None
    unit: str = ""
    note: str = ""


def _planet_velocity_records():
    records = []
    for name, orbital_radius, central_mass in PLANETS:
        velocity_km = calculate_orbital_velocity(orbital_radius, central_mass)
        records.append(
            MetricRecord(
                section="planets",
                label=f"{name} orbital velocity",
                value=f"{velocity_km:.2f}",
                value_num=round(velocity_km, 2),
                unit="km/s",
            )
        )
    return records


def _earth_orbit_records():
    records = []
    for name, orbital_radius, central_mass, kind in EARTH_ORBITS:
        velocity_km = calculate_orbital_velocity(orbital_radius, central_mass)
        records.append(
            MetricRecord(
                section="earth",
                label=f"{name} orbital velocity",
                value=f"{velocity_km:.2f}",
                value_num=round(velocity_km, 2),
                unit="km/s",
                note=kind,
            )
        )

    iss_to_moon_km = meters_to_km(ISS_TO_MOON_DISTANCE)
    records.append(
        MetricRecord(
            section="earth",
            label="ISS distance from Moon",
            value=f"{iss_to_moon_km:.0f}",
            value_num=round(iss_to_moon_km, 0),
            unit="km",
        )
    )
    return records


def _concept_station_records():
    records = []
    for name, midpoint_distance, note in CONCEPT_STATIONS:
        midpoint_km = meters_to_km(midpoint_distance)
        records.append(
            MetricRecord(
                section="concepts",
                label=f"Concept station {name}",
                value=f"{midpoint_km:.0f}",
                value_num=round(midpoint_km, 0),
                unit="km",
                note=note,
            )
        )
    return records


def _mars_base_records():
    return [
        MetricRecord("mars-base", "Location", "TBD"),
        MetricRecord("mars-base", "Primary habitation", "TBD", note="Target crew habitat sizing"),
        MetricRecord("mars-base", "Core systems", "Habitat, life support, power, landing pad"),
        MetricRecord("mars-base", "Life support", "Radiation shielding, water extraction, O2 generation"),
        MetricRecord("mars-base", "Power profile", "Nuclear primary, solar secondary, battery reserve"),
        MetricRecord("mars-base", "Safety controls", "Pressure auto-seal, dust airlocks, evacuation protocols"),
        MetricRecord("mars-base", "Crew capacity", "TBD"),
        MetricRecord("mars-base", "Mission duration", "TBD"),
    ]


def collect_records(section):
    _validate_section(section)
    by_section = {
        "planets": _planet_velocity_records,
        "earth": _earth_orbit_records,
        "concepts": _concept_station_records,
        "mars-base": _mars_base_records,
    }
    if section == "all":
        records = []
        for section_name in SECTION_ORDER:
            records.extend(by_section[section_name]())
        return records
    return by_section[section]()


def _format_text_metric(record):
    label_text = f"{record.label}:".ljust(LABEL_WIDTH)
    value_text = f"{record.value:>{VALUE_WIDTH}}"
    unit_text = f" {record.unit}" if record.unit else ""
    note_text = f" ({record.note})" if record.note else ""
    return f"{label_text}{value_text}{unit_text}{note_text}"


def render_text(section):
    records = collect_records(section)
    lines = [f"--{REPORT_TITLE}--", "Project Summary: orbital data and conceptual mission planning"]
    active_sections = SECTION_ORDER if section == "all" else [section]

    for section_name in active_sections:
        lines.append(f"--{SECTION_TITLES[section_name]}--")
        for record in records:
            if record.section == section_name:
                lines.append(_format_text_metric(record))
    return "\n".join(lines)


def render_json(section):
    records = [asdict(record) for record in collect_records(section)]
    payload = {
        "report_title": REPORT_TITLE,
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "section": section,
        "assumption": "Circular orbit approximation v = sqrt(GM/r)",
        "records": records,
    }
    return json.dumps(payload, indent=2)


def render_csv(section):
    records = collect_records(section)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["section", "label", "value", "value_num", "unit", "note"])
    for record in records:
        writer.writerow(
            [record.section, record.label, record.value, record.value_num, record.unit, record.note]
        )
    return output.getvalue().rstrip("\n")


def render_report(section, output_format):
    _validate_section(section)
    _validate_output_format(output_format)

    renderers = {
        "text": render_text,
        "json": render_json,
        "csv": render_csv,
    }
    return renderers[output_format](section)


def _validate_section(section):
    if section not in VALID_SECTIONS:
        valid_sections = ", ".join(VALID_SECTIONS)
        raise ValueError(f"Unsupported section '{section}'. Valid options: {valid_sections}")


def _validate_output_format(output_format):
    if output_format not in VALID_OUTPUT_FORMATS:
        valid_formats = ", ".join(VALID_OUTPUT_FORMATS)
        raise ValueError(f"Unsupported output format '{output_format}'. Valid options: {valid_formats}")
