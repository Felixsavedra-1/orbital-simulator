G = 6.67430e-11          # m^3 kg^-1 s^-2, CODATA 2018
AU = 149_597_870_700.0   # meters, IAU 2012 Resolution B2

SUN_MASS = 1.98892e30    # kg, IAU 2015 Resolution B3
EARTH_MASS = 5.9722e24   # kg, NASA Earth fact sheet (2024)

# Semi-major axis of lunar orbit; actual range 356,500–406,700 km (e ≈ 0.0549)
MOON_ORBITAL_RADIUS = 384_400_000.0  # m, NASA Moon fact sheet (2024)

EARTH_RADIUS = 6_371_000.0  # m, volumetric mean, NASA Earth fact sheet (2024)
ISS_ALTITUDE = 408_000.0    # m, approximate mean as of 2024-Q1; decays ~2 km/year

DATA_VALIDATION_DATE = "2025-01-01"  # last verified against NASA/JPL/CODATA/IAU sources; update manually when re-verified

# Orbital eccentricities at epoch J2000.0, from JPL Horizons
EARTH_ECCENTRICITY = 0.0167086   # NASA Earth fact sheet (2024)
MARS_ECCENTRICITY  = 0.0934      # NASA Mars fact sheet (2024)

STANDARD_GRAVITY = 9.80665  # m/s², exact by BIPM/IAU definition; used in Tsiolkovsky Isp conversion
