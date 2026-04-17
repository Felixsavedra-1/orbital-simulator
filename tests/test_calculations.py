import math
import unittest

from calculations import (
    calculate_escape_velocity,
    calculate_orbital_period,
    calculate_orbital_velocity,
    meters_to_km,
)
from constants import EARTH_MASS, EARTH_RADIUS, G, SUN_MASS
from data import EARTH_ORBITAL_RADIUS, MOON_ORBITAL_RADIUS


class TestOrbitalVelocity(unittest.TestCase):
    def test_earth_around_sun(self):
        # ~29.78 km/s (NASA fact sheet)
        velocity_km = calculate_orbital_velocity(EARTH_ORBITAL_RADIUS, SUN_MASS)
        self.assertAlmostEqual(velocity_km, 29.78, places=1)

    def test_moon_around_earth(self):
        # ~1.022 km/s (NASA Moon fact sheet)
        velocity_km = calculate_orbital_velocity(MOON_ORBITAL_RADIUS, EARTH_MASS)
        self.assertAlmostEqual(velocity_km, 1.022, places=2)

    def test_custom_gravitational_constant(self):
        v1 = calculate_orbital_velocity(EARTH_ORBITAL_RADIUS, SUN_MASS, G)
        v2 = calculate_orbital_velocity(EARTH_ORBITAL_RADIUS, SUN_MASS, G * 2)
        self.assertAlmostEqual(v2 / v1, math.sqrt(2), places=5)

    def test_zero_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(0, EARTH_MASS)

    def test_negative_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(-1e8, EARTH_MASS)

    def test_zero_mass_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(MOON_ORBITAL_RADIUS, 0)

    def test_negative_mass_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(MOON_ORBITAL_RADIUS, -1e24)


class TestOrbitalPeriod(unittest.TestCase):
    def test_earth_around_sun(self):
        # ~8,766 hours (365.25 Earth days)
        period_hours = calculate_orbital_period(EARTH_ORBITAL_RADIUS, SUN_MASS)
        self.assertAlmostEqual(period_hours, 8766, delta=50)

    def test_moon_around_earth(self):
        # ~655 hours (27.3 Earth days)
        period_hours = calculate_orbital_period(MOON_ORBITAL_RADIUS, EARTH_MASS)
        self.assertAlmostEqual(period_hours, 655, delta=10)

    def test_zero_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_period(0, EARTH_MASS)

    def test_negative_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_period(-1e11, EARTH_MASS)

    def test_zero_mass_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_period(MOON_ORBITAL_RADIUS, 0)

    def test_negative_mass_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_period(MOON_ORBITAL_RADIUS, -1e24)


class TestEscapeVelocity(unittest.TestCase):
    def test_earth_surface(self):
        # ~11.186 km/s (NASA Earth fact sheet)
        v_esc = calculate_escape_velocity(EARTH_RADIUS, EARTH_MASS)
        self.assertAlmostEqual(v_esc, 11.19, places=1)

    def test_equals_sqrt2_times_orbital_velocity(self):
        v_orb = calculate_orbital_velocity(MOON_ORBITAL_RADIUS, EARTH_MASS)
        v_esc = calculate_escape_velocity(MOON_ORBITAL_RADIUS, EARTH_MASS)
        self.assertAlmostEqual(v_esc / v_orb, math.sqrt(2), places=5)

    def test_zero_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_escape_velocity(0, EARTH_MASS)

    def test_negative_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_escape_velocity(-1e8, EARTH_MASS)

    def test_zero_mass_raises(self):
        with self.assertRaises(ValueError):
            calculate_escape_velocity(EARTH_RADIUS, 0)

    def test_negative_mass_raises(self):
        with self.assertRaises(ValueError):
            calculate_escape_velocity(EARTH_RADIUS, -1e24)


class TestMetersToKm(unittest.TestCase):
    def test_basic(self):
        self.assertAlmostEqual(meters_to_km(1000.0), 1.0)

    def test_fractional(self):
        self.assertAlmostEqual(meters_to_km(500.0), 0.5)

    def test_zero(self):
        self.assertEqual(meters_to_km(0.0), 0.0)


if __name__ == "__main__":
    unittest.main()
