"""Physical and orbital constants for Phaethon-Chimera (Package 35)."""

from __future__ import annotations

import math

# Golden ratio and derived values
PHI: float = (1 + math.sqrt(5)) / 2           # 1.6180339887...
PHI_CUBEROOT: float = PHI ** (1 / 3)           # 1.17398499...
SIGMA_PHI: float = 1 / 16                      # Frame Principle constant

# CREP benchmark values (from entropy atlas)
GAMMA_AMAZON: float = 0.116
GAMMA_AMOC: float = 0.251
GAMMA_PHAETHON: float = 0.165   # P35 target: between Amazon and AMOC
GAMMA_SANDPILE: float = 0.296

# Phaethon orbital parameters (3200 Phaethon, JPL Horizons)
PHAETHON_PERIOD_DAYS: float = 523.5           # ~1.434 yr
PHAETHON_PERIOD_YEARS: float = PHAETHON_PERIOD_DAYS / 365.25
PHAETHON_PERIHELION_AU: float = 0.1397        # Extremely close to Sun
PHAETHON_APHELION_AU: float = 2.403
PHAETHON_ECCENTRICITY: float = 0.8898
PHAETHON_INCLINATION_DEG: float = 22.26
PHAETHON_RADIUS_KM: float = 2.78             # Mean radius (Hanus et al.)

# UTAC default parameters for Phaethon
UTAC_R_PHAETHON: float = 0.18    # Growth rate (moderate)
UTAC_K_PHAETHON: float = 1.0     # Carrying capacity (normalised)
UTAC_SIGMA: float = 2.2          # Steepness (from CREP beta-bridge)
UTAC_GAMMA: float = GAMMA_PHAETHON  # CREP coupling

# Frustrated-system forcing amplitude
FORCING_AMPLITUDE: float = 0.08   # A in A·cos(ω_p·t)

# SOC power-law exponent prediction
SOC_TAU_EXPONENT: float = 1.3    # Dust avalanche size distribution τ

# Chimera state predictions
CHIMERA_R_PERIHELION: float = 0.50  # Order parameter at perihelion
CHIMERA_ALTITUDE_KM: float = 2.3    # Transition altitude from surface

# Emission probability per orbit
EMISSION_PROBABILITY: float = 0.23

# DESTINY+ mission timeline
DESTINY_FLYBY_YEAR: int = 2029

# Package metadata
PACKAGE_NUMBER: int = 35
ZENODO_DOI: str = "10.5281/zenodo.17472834"
