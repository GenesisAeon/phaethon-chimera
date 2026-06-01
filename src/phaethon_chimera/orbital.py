"""Phaethon Keplerian orbital mechanics."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from phaethon_chimera.constants import (
    PHAETHON_APHELION_AU,
    PHAETHON_ECCENTRICITY,
    PHAETHON_INCLINATION_DEG,
    PHAETHON_PERIOD_DAYS,
    PHAETHON_PERIHELION_AU,
)


@dataclass
class OrbitalState:
    """Snapshot of Phaethon's position in its orbit."""

    time_days: float
    true_anomaly_rad: float
    radius_au: float
    is_perihelion: bool = False
    solar_flux_relative: float = 1.0  # relative to 1 AU


@dataclass
class PhaethonOrbit:
    """
    Keplerian orbit of 3200 Phaethon (JPL Horizons elements).

    Computes true anomaly, heliocentric distance, and solar flux
    as a function of time. Perihelion passages are tagged as
    phase events — they trigger dust emission in FrustratedUTAC.
    """

    period_days: float = PHAETHON_PERIOD_DAYS
    perihelion_au: float = PHAETHON_PERIHELION_AU
    aphelion_au: float = PHAETHON_APHELION_AU
    eccentricity: float = PHAETHON_ECCENTRICITY
    inclination_deg: float = PHAETHON_INCLINATION_DEG

    _semi_major_au: float = field(init=False)
    _angular_freq_rad_per_day: float = field(init=False)

    def __post_init__(self) -> None:
        self._semi_major_au = (self.perihelion_au + self.aphelion_au) / 2
        self._angular_freq_rad_per_day = 2 * math.pi / self.period_days

    def mean_anomaly(self, t: float) -> float:
        """Mean anomaly M(t) in radians."""
        return self._angular_freq_rad_per_day * t % (2 * math.pi)

    def eccentric_anomaly(self, M: float, tol: float = 1e-10) -> float:
        """Eccentric anomaly E via Newton-Raphson (Kepler's equation)."""
        e = self.eccentricity
        E = M if e < 0.8 else math.pi
        for _ in range(50):
            dE = (M - E + e * math.sin(E)) / (1 - e * math.cos(E))
            E += dE
            if abs(dE) < tol:
                break
        return E

    def true_anomaly(self, t: float) -> float:
        """True anomaly ν(t) in radians."""
        M = self.mean_anomaly(t)
        E = self.eccentric_anomaly(M)
        e = self.eccentricity
        nu = 2 * math.atan2(
            math.sqrt(1 + e) * math.sin(E / 2),
            math.sqrt(1 - e) * math.cos(E / 2),
        )
        return nu % (2 * math.pi)

    def radius(self, t: float) -> float:
        """Heliocentric distance r(t) in AU."""
        nu = self.true_anomaly(t)
        e = self.eccentricity
        a = self._semi_major_au
        return a * (1 - e**2) / (1 + e * math.cos(nu))

    def solar_flux_relative(self, t: float) -> float:
        """Solar flux relative to 1 AU (∝ 1/r²)."""
        r = self.radius(t)
        return 1 / r**2

    def is_near_perihelion(self, t: float, window_days: float = 5.0) -> bool:
        """True if within window_days of a perihelion passage."""
        M = self.mean_anomaly(t)
        return M < self._angular_freq_rad_per_day * window_days or M > (
            2 * math.pi - self._angular_freq_rad_per_day * window_days
        )

    def state_at(self, t: float) -> OrbitalState:
        nu = self.true_anomaly(t)
        r = self.radius(t)
        return OrbitalState(
            time_days=t,
            true_anomaly_rad=nu,
            radius_au=r,
            is_perihelion=self.is_near_perihelion(t),
            solar_flux_relative=1 / r**2,
        )

    def perihelion_times(self, n_orbits: int) -> list[float]:
        """Times (days) of perihelion passages over n_orbits."""
        return [i * self.period_days for i in range(n_orbits + 1)]
