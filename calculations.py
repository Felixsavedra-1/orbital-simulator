import math

from constants import G

_M_PER_KM = 1000.0
_S_PER_HOUR = 3600.0


def _validate_inputs(radius_m: float, central_mass_kg: float, gravitational_constant: float) -> None:
    if not math.isfinite(radius_m) or radius_m <= 0:
        raise ValueError("radius_m must be a finite positive number")
    if not math.isfinite(central_mass_kg) or central_mass_kg <= 0:
        raise ValueError("central_mass_kg must be a finite positive number")
    if not math.isfinite(gravitational_constant) or gravitational_constant <= 0:
        raise ValueError("gravitational_constant must be a finite positive number")


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
    return velocity_m_per_s / _M_PER_KM


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
    return period_s / _S_PER_HOUR


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
    return velocity_m_per_s / _M_PER_KM


def meters_to_km(distance_m: float) -> float:
    return distance_m / _M_PER_KM
