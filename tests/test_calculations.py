import unittest

from calculations import calculate_orbital_velocity
from constants import EARTH_MASS, SUN_MASS
from data import EARTH_ORBITAL_RADIUS


class TestCalculations(unittest.TestCase):
    def test_orbital_velocity_earth_sun(self):
        velocity_km = calculate_orbital_velocity(EARTH_ORBITAL_RADIUS, SUN_MASS)
        self.assertTrue(29.0 <= velocity_km <= 30.5)

    def test_orbital_velocity_moon_earth(self):
        moon_orbital_radius = 3.844e8
        velocity_km = calculate_orbital_velocity(moon_orbital_radius, EARTH_MASS)
        self.assertTrue(0.8 <= velocity_km <= 1.2)

    def test_invalid_orbital_velocity_inputs_raise(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(0, EARTH_MASS)
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(1, 0)


if __name__ == "__main__":
    unittest.main()
