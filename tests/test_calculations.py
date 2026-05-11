import math
import unittest

from calculations import (
    calculate_escape_velocity,
    calculate_hohmann_delta_v,
    calculate_mass_ratio,
    calculate_orbital_period,
    calculate_orbital_velocity,
    calculate_vis_viva_velocity,
    meters_to_km,
)
from constants import EARTH_MASS, EARTH_RADIUS, G, STANDARD_GRAVITY, SUN_MASS
from data import EARTH_ORBITAL_RADIUS, MARS_ORBITAL_RADIUS, MOON_ORBITAL_RADIUS


class TestOrbitalVelocity(unittest.TestCase):
    def test_earth_around_sun(self):
        # Circular-orbit formula gives ~29.79 km/s; NASA observed mean is 29.78 km/s.
        # places=2 validates formula precision; elliptical deviation is documented.
        velocity_km = calculate_orbital_velocity(EARTH_ORBITAL_RADIUS, SUN_MASS)
        self.assertAlmostEqual(velocity_km, 29.79, places=2)

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

    def test_nan_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(float("nan"), EARTH_MASS)

    def test_inf_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(float("inf"), EARTH_MASS)

    def test_nan_mass_raises(self):
        with self.assertRaises(ValueError):
            calculate_orbital_velocity(MOON_ORBITAL_RADIUS, float("nan"))


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


class TestVisVivaVelocity(unittest.TestCase):
    def test_circular_orbit_matches_orbital_velocity(self):
        r = EARTH_RADIUS + 408_000.0
        self.assertAlmostEqual(
            calculate_vis_viva_velocity(r, r, EARTH_MASS),
            calculate_orbital_velocity(r, EARTH_MASS),
            places=8,
        )

    def test_known_elliptical_value(self):
        # r=2Re, a=3Re: v = sqrt(GM * (1/Re - 1/(3Re))) = sqrt(GM * 2/(3Re)) ≈ 6.46 km/s
        v = calculate_vis_viva_velocity(2.0 * EARTH_RADIUS, 3.0 * EARTH_RADIUS, EARTH_MASS)
        self.assertAlmostEqual(v, 6.46, places=1)

    def test_zero_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_vis_viva_velocity(0.0, EARTH_RADIUS * 3, EARTH_MASS)

    def test_negative_radius_raises(self):
        with self.assertRaises(ValueError):
            calculate_vis_viva_velocity(-1e7, EARTH_RADIUS * 3, EARTH_MASS)

    def test_zero_semi_major_axis_raises(self):
        with self.assertRaises(ValueError):
            calculate_vis_viva_velocity(EARTH_RADIUS, 0.0, EARTH_MASS)

    def test_negative_semi_major_axis_raises(self):
        with self.assertRaises(ValueError):
            calculate_vis_viva_velocity(EARTH_RADIUS, -1e7, EARTH_MASS)

    def test_unphysical_discriminant_raises(self):
        # r=3Re, a=Re: 2/(3Re) - 1/Re = -1/(3Re) < 0
        with self.assertRaises(ValueError):
            calculate_vis_viva_velocity(3.0 * EARTH_RADIUS, EARTH_RADIUS, EARTH_MASS)


class TestHohmannDeltaV(unittest.TestCase):
    def test_earth_to_mars_departure(self):
        dv1, _ = calculate_hohmann_delta_v(EARTH_ORBITAL_RADIUS, MARS_ORBITAL_RADIUS, SUN_MASS)
        self.assertAlmostEqual(dv1, 2.9, delta=0.1)

    def test_earth_to_mars_arrival(self):
        _, dv2 = calculate_hohmann_delta_v(EARTH_ORBITAL_RADIUS, MARS_ORBITAL_RADIUS, SUN_MASS)
        self.assertAlmostEqual(dv2, 2.6, delta=0.1)

    def test_ascending_transfer_both_positive(self):
        dv1, dv2 = calculate_hohmann_delta_v(EARTH_ORBITAL_RADIUS, MARS_ORBITAL_RADIUS, SUN_MASS)
        self.assertGreater(dv1, 0.0)
        self.assertGreater(dv2, 0.0)

    def test_equal_radii_zero_delta_v(self):
        dv1, dv2 = calculate_hohmann_delta_v(EARTH_ORBITAL_RADIUS, EARTH_ORBITAL_RADIUS, SUN_MASS)
        self.assertAlmostEqual(dv1, 0.0, places=8)
        self.assertAlmostEqual(dv2, 0.0, places=8)

    def test_returns_two_floats(self):
        result = calculate_hohmann_delta_v(EARTH_ORBITAL_RADIUS, MARS_ORBITAL_RADIUS, SUN_MASS)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)

    def test_zero_r1_raises(self):
        with self.assertRaises(ValueError):
            calculate_hohmann_delta_v(0.0, MARS_ORBITAL_RADIUS, SUN_MASS)

    def test_zero_r2_raises(self):
        with self.assertRaises(ValueError):
            calculate_hohmann_delta_v(EARTH_ORBITAL_RADIUS, 0.0, SUN_MASS)

    def test_descending_transfer_both_negative(self):
        # Mars → Earth is a descending transfer; both burns are decelerations
        dv1, dv2 = calculate_hohmann_delta_v(MARS_ORBITAL_RADIUS, EARTH_ORBITAL_RADIUS, SUN_MASS)
        self.assertLess(dv1, 0.0)
        self.assertLess(dv2, 0.0)


class TestMassRatio(unittest.TestCase):
    def test_known_value(self):
        # dv=9000 m/s, Isp=311s → exp(9000 / (311 * 9.80665))
        ratio = calculate_mass_ratio(9000.0, 311.0)
        self.assertAlmostEqual(ratio, math.exp(9000.0 / (311.0 * STANDARD_GRAVITY)), places=5)
        self.assertAlmostEqual(ratio, 19.12, delta=0.1)

    def test_zero_delta_v_returns_one(self):
        self.assertAlmostEqual(calculate_mass_ratio(0.0, 311.0), 1.0, places=10)

    def test_ratio_always_at_least_one(self):
        self.assertGreaterEqual(calculate_mass_ratio(1000.0, 450.0), 1.0)

    def test_negative_delta_v_raises(self):
        with self.assertRaises(ValueError):
            calculate_mass_ratio(-100.0, 311.0)

    def test_zero_isp_raises(self):
        with self.assertRaises(ValueError):
            calculate_mass_ratio(9000.0, 0.0)

    def test_negative_isp_raises(self):
        with self.assertRaises(ValueError):
            calculate_mass_ratio(9000.0, -311.0)


if __name__ == "__main__":
    unittest.main()
