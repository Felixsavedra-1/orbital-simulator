import math
import unittest

from constants import G, SUN_MASS
from data import EARTH_ORBITAL_RADIUS
from propagator import propagate_two_body


def _circular_initial_state(r):
    v = math.sqrt(G * SUN_MASS / r)
    return r, 0.0, 0.0, v


class TestPropagateTwoBody(unittest.TestCase):
    def test_circular_orbit_radius_conservation(self):
        # Earth around Sun for 365 days (dt=86400 s): final radius within 0.1% of initial.
        r0, y0, vx0, vy0 = _circular_initial_state(EARTH_ORBITAL_RADIUS)
        traj = propagate_two_body(r0, y0, vx0, vy0, SUN_MASS, 86400.0, 365)
        r_final = math.sqrt(traj[-1][1] ** 2 + traj[-1][2] ** 2)
        self.assertAlmostEqual(r_final / EARTH_ORBITAL_RADIUS, 1.0, delta=0.001)

    def test_output_length_is_n_steps_plus_one(self):
        r0, y0, vx0, vy0 = _circular_initial_state(EARTH_ORBITAL_RADIUS)
        traj = propagate_two_body(r0, y0, vx0, vy0, SUN_MASS, 86400.0, 10)
        self.assertEqual(len(traj), 11)

    def test_entry_format_is_five_tuple(self):
        r0, y0, vx0, vy0 = _circular_initial_state(EARTH_ORBITAL_RADIUS)
        traj = propagate_two_body(r0, y0, vx0, vy0, SUN_MASS, 86400.0, 2)
        for entry in traj:
            self.assertIsInstance(entry, tuple)
            self.assertEqual(len(entry), 5)

    def test_t0_is_zero_and_initial_state_preserved(self):
        r0, y0, vx0, vy0 = _circular_initial_state(EARTH_ORBITAL_RADIUS)
        traj = propagate_two_body(r0, y0, vx0, vy0, SUN_MASS, 86400.0, 3)
        self.assertEqual(traj[0], (0.0, r0, y0, vx0, vy0))
        self.assertAlmostEqual(traj[1][0], 86400.0, places=0)

    def test_zero_n_steps_raises(self):
        r0, y0, vx0, vy0 = _circular_initial_state(EARTH_ORBITAL_RADIUS)
        with self.assertRaises(ValueError):
            propagate_two_body(r0, y0, vx0, vy0, SUN_MASS, 86400.0, 0)

    def test_negative_dt_raises(self):
        r0, y0, vx0, vy0 = _circular_initial_state(EARTH_ORBITAL_RADIUS)
        with self.assertRaises(ValueError):
            propagate_two_body(r0, y0, vx0, vy0, SUN_MASS, -86400.0, 1)

    def test_zero_mass_raises(self):
        r0, y0, vx0, vy0 = _circular_initial_state(EARTH_ORBITAL_RADIUS)
        with self.assertRaises(ValueError):
            propagate_two_body(r0, y0, vx0, vy0, 0.0, 86400.0, 1)


if __name__ == "__main__":
    unittest.main()
