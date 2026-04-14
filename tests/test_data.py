import unittest

from constants import AU, EARTH_MASS, EARTH_RADIUS, ISS_ALTITUDE, MOON_ORBITAL_RADIUS, SUN_MASS
from data import (
    CONCEPT_STATIONS,
    EARTH_MARS_MIN_SEPARATION_LOWER_BOUND,
    EARTH_ORBITS,
    ISS_TO_MOON_DISTANCE,
    PLANETS,
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
        earth = PLANETS[2]
        self.assertEqual(earth.name, "Earth")
        self.assertEqual(earth.central_mass_kg, SUN_MASS)
        self.assertAlmostEqual(earth.orbital_radius_m / AU, 1.0, places=3)


if __name__ == "__main__":
    unittest.main()
