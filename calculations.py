import math

from constants import G


def _validate_inputs(radius_m: float, central_mass_kg: float, gravitational_constant: float) -> None:
    if radius_m <= 0:
        raise ValueError("radius_m must be > 0")
    if central_mass_kg <= 0:
        raise ValueError("central_mass_kg must be > 0")
    if gravitational_constant <= 0:
        raise ValueError("gravitational_constant must be > 0")


def calculate_orbital_velocity(
    radius_m: float,
    central_mass_kg: float,
    gravitational_constant: float = G,
) -> float:
    """Return circular orbital velocity in km/s.  v = sqrt(GM / r)

    Raises:
        ValueError: If any argument is <= 0.
    """
    _validate_inputs(radius_m, central_mass_kg, gravitational_constant)
    velocity_m_per_s = math.sqrt((gravitational_constant * central_mass_kg) / radius_m)
    return velocity_m_per_s / 1000


def calculate_orbital_period(
    radius_m: float,
    central_mass_kg: float,
    gravitational_constant: float = G,
) -> float:
    """Return orbital period in hours using Kepler's third law.  T = 2π * sqrt(r³ / GM)

    Raises:
        ValueError: If any argument is <= 0.
    """
    _validate_inputs(radius_m, central_mass_kg, gravitational_constant)
    period_s = 2 * math.pi * math.sqrt(radius_m**3 / (gravitational_constant * central_mass_kg))
    return period_s / 3600


def calculate_escape_velocity(
    radius_m: float,
    central_mass_kg: float,
    gravitational_constant: float = G,
) -> float:
    """Return escape velocity in km/s.  v_esc = sqrt(2GM / r)

    Raises:
        ValueError: If any argument is <= 0.
    """
    _validate_inputs(radius_m, central_mass_kg, gravitational_constant)
    velocity_m_per_s = math.sqrt((2 * gravitational_constant * central_mass_kg) / radius_m)
    return velocity_m_per_s / 1000


def meters_to_km(distance_m: float) -> float:
    return distance_m / 1000
