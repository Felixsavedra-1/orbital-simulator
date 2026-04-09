import math

from constants import G


def calculate_orbital_velocity(radius_m, central_mass_kg, gravitational_constant=G):
    """Calculate orbital velocity in km/s (circular orbit approximation)."""
    if radius_m <= 0:
        raise ValueError("radius_m must be > 0")
    if central_mass_kg <= 0:
        raise ValueError("central_mass_kg must be > 0")
    if gravitational_constant <= 0:
        raise ValueError("gravitational_constant must be > 0")

    velocity_m_per_s = math.sqrt((gravitational_constant * central_mass_kg) / radius_m)
    return velocity_m_per_s / 1000


def meters_to_km(distance_m):
    return distance_m / 1000
