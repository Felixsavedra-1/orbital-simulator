# Orbital Simulation Report Engine

This project provides a deterministic orbital mechanics reporting tool for technical review, academic submission, and institutional analysis workflows.

## What It Produces
- Planet orbital velocity estimates for Mercury through Neptune
- Earth orbital system metrics for Moon and ISS
- Concept station distances for Earth-Moon and Earth-Mars midpoints
- Mars base concept fields for planning discussions

## Institutional Readiness Upgrades
- Structured output model with `text`, `json`, and `csv` report formats
- Optional file export with stable output contracts for downstream systems
- Versioned JSON schema contract via `report_schema_version` (currently `1.0.0`)
- Machine-readable numeric field (`value_num`) included alongside display strings
- Input validation in core physics functions (rejects non-physical values)
- Expanded unit test coverage across calculations, data integrity, and CLI behavior
- Explicit assumptions and model limitations for auditability

## Methodology
- Orbital speed formula: `v = sqrt(GM/r)`
- Model type: circular orbit approximation
- Units: SI inputs, output velocity in `km/s`
- Data basis:
  - IAU astronomical unit definition
  - NASA fact-sheet values for body mass/radius and Moon distance
  - JPL approximate planetary semi-major axes (AU)

## CLI Usage
Run full text report:
```bash
python3 main.py
```

Run one section:
```bash
python3 main.py --section planets
```

Export machine-readable report:
```bash
python3 main.py --section earth --format json --output earth_report.json
python3 main.py --section all --format csv --output full_report.csv
```

Arguments:
- `--section`: `all`, `planets`, `earth`, `concepts`, `mars-base`
- `--format`: `text`, `json`, `csv`
- `--output`: optional file path; if omitted, output is printed to stdout

## Reproducibility and QA
Run tests:
```bash
python3 -m unittest discover -s tests
```

Current coverage areas:
- Physics calculation sanity and invalid input rejection
- Source data integrity and derived-distance consistency
- CLI section routing and output format behavior

## Limitations
- Circular orbits are an approximation and ignore eccentricity and perturbations.
- No uncertainty propagation, confidence intervals, or stochastic modeling yet.
- Mars base section is conceptual and intentionally marked as `TBD` for undecided parameters.

## Project Structure
- `main.py`: CLI entrypoint and output routing
- `constants.py`: Physical constants and reference values
- `data.py`: Orbital datasets and derived distances
- `calculations.py`: Core formulas and unit conversions
- `report.py`: Record construction and output renderers (`text/json/csv`)
- `tests/test_calculations.py`: Calculation tests
- `tests/test_data.py`: Data consistency tests
- `tests/test_main.py`: CLI and output format tests
