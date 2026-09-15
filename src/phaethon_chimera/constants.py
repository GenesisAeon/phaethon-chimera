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
# HONESTY NOTE (2026-09-15, ecosystem-wide Gamma-circularity review):
# unlike GAMMA_AMAZON/GAMMA_AMOC (each a documented rescaling of a real,
# cited domain ratio via a shared sigma=2.2 -- itself a separate honesty
# finding, see those packages' own constants.py), GAMMA_PHAETHON has NO
# cited physical derivation, no eta input, and no reference paper. Its
# own original comment described it only as a "target: between Amazon
# and AMOC" -- i.e. a value chosen to occupy a plausible slot in the
# shared cross-package Gamma ordering, not derived from any measured or
# modelled property of asteroid 3200 Phaethon. This value is presented
# in README.md/destiny_predictions.py as DESTINY+ Prediction #1 (with an
# uncertainty band, "falsifiable" against the 2029 flyby) -- see
# destiny_predictions.py for the corresponding fix. See
# D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md for the full
# finding.
GAMMA_PHAETHON: float = 0.165
GAMMA_SANDPILE: float = 0.296

# Phaethon orbital parameters (3200 Phaethon, JPL Horizons)
PHAETHON_PERIOD_DAYS: float = 523.5           # ~1.434 yr
PHAETHON_PERIOD_YEARS: float = PHAETHON_PERIOD_DAYS / 365.25
PHAETHON_PERIHELION_AU: float = 0.1397        # Extremely close to Sun
PHAETHON_APHELION_AU: float = 2.403
PHAETHON_ECCENTRICITY: float = 0.8898
PHAETHON_INCLINATION_DEG: float = 22.26
# CORRECTED (2026-09-15, DESTINY+ predictions audit): the real Hanus et al.
# 2016 (A&A 592, A34) result is an effective DIAMETER of 5.1+/-0.2 km from
# thermophysical modelling of infrared data -- NOT an occultation
# measurement, and NOT a radius of 2.78 km. Radius = diameter/2 = 2.55 km.
# See destiny_predictions.py Prediction #26 for the corresponding fix and
# D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md for the finding.
PHAETHON_RADIUS_KM: float = 2.55             # Mean radius (Hanus et al. 2016, A&A 592 A34)

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
# CORRECTED (2026-09-15, DESTINY+ predictions audit): JAXA's own current
# schedule (see https://en.wikipedia.org/wiki/DESTINY%2B, launch-vehicle
# change from Epsilon S to H3) delayed launch to JFY2028 and the Phaethon
# flyby to JFY2030 -- this was 2029 in an earlier mission plan. See
# destiny_predictions.py Prediction #46 and README.md/.zenodo.json (all
# updated) for the corresponding fixes, and FOLLOWUP_TICKETS.md for the
# full finding.
DESTINY_FLYBY_YEAR: int = 2030

# Package metadata
PACKAGE_NUMBER: int = 35
ZENODO_DOI: str = "10.5281/zenodo.20807497"
