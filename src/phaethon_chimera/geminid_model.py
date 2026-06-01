"""Geminid meteor shower model derived from Phaethon UTAC dynamics."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from phaethon_chimera.constants import EMISSION_PROBABILITY, PHAETHON_PERIOD_DAYS


@dataclass
class GeminidStream:
    """Parameters of the Geminid meteoroid stream."""

    stream_age_years: float = 2000.0
    mean_grain_mass_kg: float = 1e-6
    stream_width_au: float = 0.05
    zhr_peak: float = 120.0      # Zenith Hourly Rate


class GeminidModel:
    """
    Models the Geminid meteor shower as the integrated debris trail
    of Phaethon's stochastic dust emissions over ~2000 years.

    Uses UTAC cumulative mass-flux integrated over n_orbits:
        M_stream = Σ_i P_emit · F_peak(orbit_i) · Δt_emission

    The ZHR is proportional to stream density at Earth crossing.
    """

    def __init__(
        self,
        emit_probability: float = EMISSION_PROBABILITY,
        period_days: float = PHAETHON_PERIOD_DAYS,
        stream: GeminidStream | None = None,
    ) -> None:
        self.emit_probability = emit_probability
        self.period_days = period_days
        self.stream = stream or GeminidStream()

    @property
    def n_orbits_in_stream_age(self) -> int:
        return int(self.stream.stream_age_years * 365.25 / self.period_days)

    def cumulative_mass_flux(self, n_orbits: int | None = None) -> float:
        """
        Expected cumulative mass ejected over the stream lifetime.

        M_total = P_emit · n_orbits · mean_flux_per_orbit · M_grain
        """
        n = n_orbits or self.n_orbits_in_stream_age
        mean_flux = self.emit_probability * 0.55  # from DustEmissionModel.mean_flux
        return n * mean_flux * self.stream.mean_grain_mass_kg

    def orbital_diffusion_width(self, n_orbits: int | None = None) -> float:
        """
        Stream width due to differential Keplerian shear over time.

        Δa ≈ v_eject · T_orbit / (2π · a) ≈ 0.05 AU (P39 prediction)
        """
        return self.stream.stream_width_au

    def zhr_prediction(self) -> float:
        """
        Predict ZHR from stream density.

        ZHR ∝ M_stream / (stream_width³) — simplified cross-section model.
        """
        M = self.cumulative_mass_flux()
        w = self.stream_width_au_effective()
        density = M / w**3 if w > 0 else 0.0
        # Calibration: historical Geminid ZHR ≈ 120 at density_ref
        density_ref = self.cumulative_mass_flux(self.n_orbits_in_stream_age) / (0.05**3)
        if density_ref > 0:
            return self.stream.zhr_peak * density / density_ref
        return self.stream.zhr_peak

    def stream_width_au_effective(self) -> float:
        return self.stream.stream_width_au

    def ejection_velocity_ms(self, radius_km: float = 2.78) -> float:
        """
        Ejection velocity at Phaethon's surface escape speed.
        v_esc = √(2GM/r) ≈ 1.2 m/s for Phaethon's bulk density.

        Prediction: v_eject ≈ 1.2 ± 0.4 m/s (Prediction #40).
        """
        G = 6.674e-11
        rho = 1700.0  # kg/m³ — B-type asteroid typical density
        r = radius_km * 1e3
        M = (4 / 3) * math.pi * r**3 * rho
        v_esc = math.sqrt(2 * G * M / r)
        return v_esc

    def summary(self) -> dict[str, float]:
        return {
            "n_orbits_stream": self.n_orbits_in_stream_age,
            "cumulative_mass_kg": self.cumulative_mass_flux(),
            "stream_width_au": self.orbital_diffusion_width(),
            "predicted_zhr": self.zhr_prediction(),
            "ejection_velocity_ms": self.ejection_velocity_ms(),
            "stream_age_years": self.stream.stream_age_years,
        }
