"""Stochastic dust emission model for Phaethon at perihelion."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from phaethon_chimera.constants import (
    EMISSION_PROBABILITY,
    GAMMA_PHAETHON,
    PHAETHON_PERIHELION_AU,
    SOC_TAU_EXPONENT,
)


@dataclass
class DustEmissionEvent:
    orbit_number: int
    time_days: float
    flux_normalised: float
    radius_au: float
    triggered: bool


class DustEmissionModel:
    """
    Stochastic dust emission model for 3200 Phaethon.

    Phaethon emits dust stochastically near perihelion — the emission
    probability per orbit is P_emit ≈ 0.23 ± 0.08.

    Dust flux peaks at perihelion and scales with solar flux:
        F_dust(r) = F_peak · (r_peri/r)^α · Bernoulli(P_emit)

    where α ≈ 2 (thermal emission from heated surface).
    The CREP coupling Γ_phaethon modulates the peak flux.
    """

    def __init__(
        self,
        emit_probability: float = EMISSION_PROBABILITY,
        gamma: float = GAMMA_PHAETHON,
        tau_exponent: float = SOC_TAU_EXPONENT,
        seed: int | None = 42,
    ) -> None:
        self.emit_probability = emit_probability
        self.gamma = gamma
        self.tau_exponent = tau_exponent
        self._rng = random.Random(seed)
        self._np_rng = np.random.default_rng(seed)

    # ── Flux model ──────────────────────────────────────────────────────────

    def peak_flux(self, radius_au: float) -> float:
        """Normalised dust flux at given heliocentric distance."""
        r_peri = PHAETHON_PERIHELION_AU
        # tanh(σΓ) modulation from UTAC — emission saturates at high Γ
        crep_factor = math.tanh(2.2 * self.gamma)
        return crep_factor * (r_peri / radius_au) ** 2

    def emission_per_orbit(
        self, orbit: int, radius_au: float = PHAETHON_PERIHELION_AU
    ) -> DustEmissionEvent:
        """Stochastic emission decision for one perihelion passage."""
        triggered = self._rng.random() < self.emit_probability
        flux = self.peak_flux(radius_au) if triggered else 0.0
        return DustEmissionEvent(
            orbit_number=orbit,
            time_days=orbit * 523.5,
            flux_normalised=flux,
            radius_au=radius_au,
            triggered=triggered,
        )

    def simulate(self, n_orbits: int = 50) -> list[DustEmissionEvent]:
        return [self.emission_per_orbit(i) for i in range(n_orbits)]

    def emission_statistics(self, n_orbits: int = 1000) -> dict[str, float]:
        events = self.simulate(n_orbits)
        triggered = [e for e in events if e.triggered]
        fluxes = [e.flux_normalised for e in triggered]
        return {
            "n_orbits": n_orbits,
            "n_triggered": len(triggered),
            "empirical_probability": len(triggered) / n_orbits,
            "mean_flux": float(np.mean(fluxes)) if fluxes else 0.0,
            "max_flux": float(max(fluxes)) if fluxes else 0.0,
        }

    # ── SOC avalanche size distribution ────────────────────────────────────

    def avalanche_sizes(self, n_events: int = 500) -> NDArray[np.float64]:
        """
        Power-law distributed avalanche sizes: P(s) ∝ s^{-τ}

        τ = SOC_TAU_EXPONENT ≈ 1.3 (DESTINY+ prediction).
        """
        # Inverse CDF sampling: s = u^{-1/(τ-1)} for s ≥ 1
        u = self._np_rng.uniform(0, 1, n_events)
        tau = self.tau_exponent
        return u ** (-1 / (tau - 1))

    def fit_tau(self, sizes: NDArray[np.float64]) -> float:
        """MLE estimate of power-law exponent τ from avalanche sizes."""
        s_min = float(np.min(sizes))
        n = len(sizes)
        # Hill estimator
        tau_hat = 1 + n / np.sum(np.log(sizes / s_min))
        return float(tau_hat)
