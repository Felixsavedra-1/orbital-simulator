from typing import NamedTuple

from constants import AU, EARTH_MASS, EARTH_RADIUS, ISS_ALTITUDE, MOON_ORBITAL_RADIUS, SUN_MASS


class OrbitalBody(NamedTuple):
    name: str
    orbital_radius_m: float
    central_mass_kg: float
    body_type: str = ""


class ConceptStation(NamedTuple):
    name: str
    distance_m: float
    note: str = ""


# Semi-major axes (AU) from JPL Horizons, epoch J2000.0
PLANET_SEMIMAJOR_AXIS_AU = [
    ("Mercury", 0.38709927),
    ("Venus",   0.72333566),
    ("Earth",   1.00000261),
    ("Mars",    1.52371034),
    ("Jupiter", 5.20288700),
    ("Saturn",  9.53667594),
    ("Uranus",  19.18916464),
    ("Neptune", 30.06992276),
]

PLANETS = [OrbitalBody(name, axis_au * AU, SUN_MASS) for name, axis_au in PLANET_SEMIMAJOR_AXIS_AU]

EARTH_ORBITS = [
    OrbitalBody("Moon", MOON_ORBITAL_RADIUS, EARTH_MASS, "Natural satellite"),
    OrbitalBody("ISS", EARTH_RADIUS + ISS_ALTITUDE, EARTH_MASS, "Space station"),
]

ISS_TO_MOON_DISTANCE = MOON_ORBITAL_RADIUS - (EARTH_RADIUS + ISS_ALTITUDE)

EARTH_ORBITAL_RADIUS = PLANETS[2].orbital_radius_m
MARS_ORBITAL_RADIUS = PLANETS[3].orbital_radius_m

# Lower-bound separation: Mars at perihelion (e=0.0934), Earth at aphelion (e=0.0167086).
# A coplanar heuristic — not actual minimum conjunction distance.
EARTH_MARS_MIN_SEPARATION_LOWER_BOUND = max(
    0.0,
    MARS_ORBITAL_RADIUS * (1 - 0.0934) - EARTH_ORBITAL_RADIUS * (1 + 0.0167086),
)

CONCEPT_STATIONS = [
    ConceptStation(
        "Earth-Moon midpoint",
        MOON_ORBITAL_RADIUS / 2,
        "Based on average Earth-Moon distance",
    ),
    ConceptStation(
        "Earth-Mars midpoint",
        EARTH_MARS_MIN_SEPARATION_LOWER_BOUND / 2,
        "Based on perihelion/aphelion lower-bound Earth-Mars separation",
    ),
]
