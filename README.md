# Orbital Simulation Report Engine

A deterministic orbital mechanics reporting tool for technical review, academic submission, and institutional analysis workflows.

## What It Produces
- Orbital velocity and period for Mercury through Neptune
- Earth orbital system metrics for Moon and ISS (velocity, period, and separation distance)
- Concept station distances for Earth-Moon and Earth-Mars midpoints
- Mars base concept fields for planning discussions

## Physics Reference

All calculations use the circular orbit approximation. For a body of mass *M* with an orbiting body at radius *r*:

| Quantity | Formula |
|---|---|
| Orbital velocity | `v = sqrt(GM / r)` → km/s |
| Orbital period (Kepler's third law) | `T = 2π * sqrt(r³ / GM)` → hours |
| Escape velocity | `v_esc = sqrt(2GM / r)` → km/s |

Where *G* = 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² (CODATA 2018).

## Data Sources

| Constant | Value | Source |
|---|---|---|
| *G* | 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² | CODATA 2018 |
| AU | 149,597,870,700 m (exact) | IAU 2012 Resolution B2 |
| Solar mass | 1.98892 × 10³⁰ kg | IAU 2015 Resolution B3 |
| Earth mass | 5.9722 × 10²⁴ kg | NASA Earth fact sheet (2024) |
| Planetary semi-major axes | — | JPL Horizons, epoch J2000.0 |
| Moon distance | 384,400,000 m | NASA Moon fact sheet (2024) |
| Earth radius | 6,371,000 m | NASA Earth fact sheet (2024) |
| ISS altitude | 408,000 m | NASA (~2024-Q1 mean) |

## Assumptions and Limitations
- All orbits are modeled as circular; eccentricity and perturbations are ignored.
- Moon orbital radius is the semi-major axis. Actual range: 356,500–406,700 km (e ≈ 0.0549).
- ISS altitude is an approximate mean as of 2024-Q1. The orbit decays ~2 km/year without reboosts.
- Earth-Mars midpoint uses a perihelion/aphelion lower-bound separation — a heuristic, not an actual conjunction distance.
- Mars base section is conceptual and intentionally marked as `TBD` for undecided parameters.
- No uncertainty propagation or confidence intervals.

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

Run all tests:
```bash
python3 -m unittest discover -s tests
```

Run a single suite:
```bash
python3 -m unittest tests.test_calculations
```

Test coverage areas:
- Physics calculations: orbital velocity, orbital period, escape velocity, invalid input rejection
- Source data integrity and derived-distance consistency
- Report record counts, JSON schema contract, CSV format contract
- Full pipeline integration (`all` section, JSON format)
- CLI section routing and output format behavior

## Project Structure
- `main.py`: CLI entrypoint and output routing
- `constants.py`: Physical constants and reference values with source citations
- `data.py`: Orbital datasets as typed NamedTuples (`OrbitalBody`, `ConceptStation`)
- `calculations.py`: Core formulas — orbital velocity, period, and escape velocity
- `report.py`: Record construction and output renderers (`text/json/csv`)
- `tests/`: Four test modules covering calculations, data, report contracts, and CLI
