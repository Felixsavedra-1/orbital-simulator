# Orbital Simulation

Physics-based orbital mechanics engine for all 8 planets — with a live 3D animation driven by the same data.

## Visualization

```bash
open solar_system.html        # macOS
xdg-open solar_system.html   # Linux
```

Or double-click `solar_system.html` in Finder.

The animation is powered entirely by this project's data: JPL Horizons semi-major axes from `data.py`, orbital speeds computed from Kepler's third law in `calculations.py`. No separate dataset — same numbers, rendered in 3D.

| Control | Action |
|---|---|
| Drag | Orbit camera |
| Scroll | Zoom |
| Right-drag | Pan |
| Speed slider | 0× pause → 6× fast-forward |

Requires internet (Three.js via CDN). No Python or build step needed.

---

## Report Engine

```bash
python3 main.py                                           # full report, text
python3 main.py --section planets                         # one section
python3 main.py --format json --output report.json        # machine-readable
python3 main.py --format csv  --output report.csv
```

| Flag | Options |
|---|---|
| `--section` | `all` · `planets` · `earth` · `concepts` · `mars-base` |
| `--format` | `text` · `json` · `csv` |
| `--output` | file path — omit to print to stdout |

---

## Physics

Circular orbit approximation throughout.

| Quantity | Formula | Unit |
|---|---|---|
| Orbital velocity | `v = √(GM / r)` | km/s |
| Orbital period | `T = 2π √(r³ / GM)` | hours |
| Escape velocity | `v_esc = √(2GM / r)` | km/s |

*G* = 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² (CODATA 2018)

---

## Data Sources

| Quantity | Source |
|---|---|
| Gravitational constant *G* | CODATA 2018 |
| Astronomical unit | IAU 2012 Resolution B2 |
| Solar mass | IAU 2015 Resolution B3 |
| Earth mass, radius, ISS altitude | NASA fact sheets (2024) |
| Planetary semi-major axes | JPL Horizons, epoch J2000.0 |
| Moon orbital radius | NASA Moon fact sheet (2024) |

---

## Assumptions

- Circular orbits — eccentricity and perturbations ignored
- Moon radius is the semi-major axis; actual range 356,500–406,700 km (e ≈ 0.0549)
- ISS altitude is a 2024-Q1 mean; decays ~2 km/year without reboosts
- Earth-Mars midpoint is a perihelion/aphelion heuristic, not a true conjunction distance
- Mars base parameters are intentionally TBD

---

## Tests

```bash
python3 -m unittest discover -s tests     # all 48 tests
python3 -m unittest tests.test_calculations
```

Covers: physics functions · invalid input rejection · data integrity · JSON schema contract · CSV format · record counts · full pipeline · CLI routing.

---

## Structure

```
calculations.py     orbital velocity, period, escape velocity
constants.py        G, AU, solar/Earth mass, Moon/ISS data
data.py             planet and orbit datasets (JPL J2000.0)
report.py           record builder + text / JSON / CSV renderers
main.py             CLI entrypoint
solar_system.html   3D animation (Three.js, CDN)
tests/              48 tests across 4 modules
```
