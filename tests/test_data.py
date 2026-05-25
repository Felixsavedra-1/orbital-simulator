import unittest

from constants import AU, EARTH_MASS, EARTH_RADIUS, ISS_ALTITUDE, MOON_ORBITAL_RADIUS, SUN_MASS
from data import (
    CONCEPT_STATIONS,
    EARTH_MARS_MIN_SEPARATION_LOWER_BOUND,
    EARTH_ORBITAL_RADIUS,
    EARTH_ORBITS,
    ISS_TO_MOON_DISTANCE,
    MARS_ORBITAL_RADIUS,
    PLANETS,
    TRANSFER_ORBITS,
)


class TestData(unittest.TestCase):
    def test_planets_count_and_central_mass(self):
        self.assertEqual(len(PLANETS), 8)
        for body in PLANETS:
            self.assertEqual(body.central_mass_kg, SUN_MASS)

    def test_earth_orbits_entries(self):
        self.assertEqual(len(EARTH_ORBITS), 2)

        moon = EARTH_ORBITS[0]
        iss = EARTH_ORBITS[1]

        self.assertEqual(moon.name, "Moon")
        self.assertEqual(moon.orbital_radius_m, MOON_ORBITAL_RADIUS)
        self.assertEqual(moon.central_mass_kg, EARTH_MASS)

        self.assertEqual(iss.name, "ISS")
        self.assertEqual(iss.orbital_radius_m, EARTH_RADIUS + ISS_ALTITUDE)
        self.assertEqual(iss.central_mass_kg, EARTH_MASS)

    def test_iss_to_moon_distance(self):
        expected = MOON_ORBITAL_RADIUS - (EARTH_RADIUS + ISS_ALTITUDE)
        self.assertEqual(ISS_TO_MOON_DISTANCE, expected)
        self.assertGreater(ISS_TO_MOON_DISTANCE, 0)

    def test_concept_stations_midpoints(self):
        self.assertEqual(len(CONCEPT_STATIONS), 2)

        earth_moon = CONCEPT_STATIONS[0]
        self.assertEqual(earth_moon.name, "Earth-Moon midpoint")
        self.assertEqual(earth_moon.distance_m, MOON_ORBITAL_RADIUS / 2)

        earth_mars = CONCEPT_STATIONS[1]
        self.assertEqual(earth_mars.name, "Earth-Mars midpoint")
        self.assertIn("lower-bound Earth-Mars separation", earth_mars.note)
        self.assertEqual(earth_mars.distance_m, EARTH_MARS_MIN_SEPARATION_LOWER_BOUND / 2)
        self.assertGreater(earth_mars.distance_m, 0)

    def test_earth_planet_distance_close_to_one_au(self):
        earth = next(p for p in PLANETS if p.name == "Earth")
        self.assertEqual(earth.central_mass_kg, SUN_MASS)
        self.assertAlmostEqual(earth.orbital_radius_m / AU, 1.0, places=3)

    def test_earth_and_mars_orbital_radii_named_correctly(self):
        earth = next(p for p in PLANETS if p.name == "Earth")
        mars = next(p for p in PLANETS if p.name == "Mars")
        self.assertEqual(EARTH_ORBITAL_RADIUS, earth.orbital_radius_m)
        self.assertEqual(MARS_ORBITAL_RADIUS, mars.orbital_radius_m)

    def test_transfer_orbits_structure(self):
        self.assertEqual(len(TRANSFER_ORBITS), 2)
        for t in TRANSFER_ORBITS:
            self.assertIsInstance(t.name, str)
            self.assertGreater(t.r1_m, 0)
            self.assertGreater(t.r2_m, 0)
            self.assertGreater(t.central_mass_kg, 0)
            self.assertGreater(t.r2_m, t.r1_m)

        leo_moon = TRANSFER_ORBITS[0]
        self.assertEqual(leo_moon.name, "LEO-Moon")
        self.assertEqual(leo_moon.central_mass_kg, EARTH_MASS)

        earth_mars = TRANSFER_ORBITS[1]
        self.assertEqual(earth_mars.name, "Earth-Mars")
        self.assertEqual(earth_mars.central_mass_kg, SUN_MASS)


if __name__ == "__main__":
    unittest.main()
