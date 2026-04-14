# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the full report (default: text format, all sections)
python3 main.py

# Run a specific section: all | planets | earth | concepts | mars-base
python3 main.py --section planets

# Output formats: text | json | csv
python3 main.py --section earth --format json

# Export to file
python3 main.py --format csv --output report.csv

# Run all tests
python3 -m unittest discover -s tests

# Run a single test module
python3 -m unittest tests.test_calculations
python3 -m unittest tests.test_data
python3 -m unittest tests.test_main
python3 -m unittest tests.test_report
```

No build step required — pure Python 3 standard library, no external dependencies.

## Architecture

The project is a deterministic orbital mechanics reporting engine with a strict layered structure:

```
main.py         CLI entrypoint — parses args, routes to render_report()
report.py       Orchestration layer — renderers (text/JSON/CSV) and collect_records()
data.py         Orbital datasets — planets, Earth orbits, concept stations
calculations.py Core physics — calculate_orbital_velocity(), meters_to_km()
constants.py    Physical constants — G, AU, SUN_MASS, EARTH_MASS, ISS_ALTITUDE, etc.
```

**Data flow:** `main.py` → `render_report(section, format)` → renderer (`render_text` / `render_json` / `render_csv`) → `collect_records(section)` → section builders in `report.py` that call `calculate_orbital_velocity()` using data from `data.py` and constants from `constants.py`.

**`MetricRecord` dataclass** (defined in `report.py`) is the universal currency between data collection and rendering. Fields: `section`, `label`, `value` (formatted string), `value_num` (float for machine use), `unit`, `note`.

**Record counts are load-bearing** — `test_report.py` asserts exact totals (21 records: 8 planets, 3 earth, 2 concepts, 8 mars-base). Adding or removing records requires updating those assertions.

**Physics:** All orbital velocities use the circular orbit approximation v = sqrt(GM/r). `calculate_orbital_velocity()` takes radius in meters and central mass in kg, returns km/s. It raises `ValueError` for non-physical inputs (zero or negative radius/mass).

**JSON output** includes a `report_schema_version` field (`"1.0.0"` in `report.py`) and an `assumptions` list. Treat these as a contract — changing them is a breaking change.

**Earth-Mars midpoint** in `data.py` is a lower-bound approximation using perihelion + aphelion averages to account for eccentricity, not a true semi-major axis midpoint.
