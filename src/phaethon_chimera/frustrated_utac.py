"""Frustrated UTAC ODE: UTAC logistic + periodic orbital forcing."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from phaethon_chimera.constants import (
    FORCING_AMPLITUDE,
    PHAETHON_PERIOD_DAYS,
    UTAC_GAMMA,
    UTAC_K_PHAETHON,
    UTAC_R_PHAETHON,
    UTAC_SIGMA,
)


@dataclass
class FrustratedUTAC:
    """
    UTAC ODE with periodic orbital forcing — the 'frustrated' system.

    dH/dt = r·H·(1-H/K)·tanh(σΓ) + A·cos(ω_p·t + φ)

    The periodic term (orbital forcing at Phaethon's frequency) competes
    with the UTAC logistic attractor. When ω_p ≈ ω_UTAC_natural, the
    system enters a chimera state: part ordered (Keplerian), part SOC.

    H(t): normalised dust/activity level ∈ [0, 1]
    """

    r: float = UTAC_R_PHAETHON
    K: float = UTAC_K_PHAETHON
    sigma: float = UTAC_SIGMA
    gamma: float = UTAC_GAMMA
    amplitude: float = FORCING_AMPLITUDE
    period_days: float = PHAETHON_PERIOD_DAYS
    phi0: float = 0.0  # initial phase offset

    _omega: float = field(init=False)

    def __post_init__(self) -> None:
        self._omega = 2 * math.pi / self.period_days

    # ── UTAC natural frequency ───────────────────────────────────────────────

    @property
    def omega_natural(self) -> float:
        """Natural frequency of the UTAC logistic around its fixed point."""
        H_star = self.K * math.tanh(self.sigma * self.gamma)
        # Linear stability: ω² ≈ r·tanh(σΓ)·(1 - 2H*/K)
        curvature = self.r * math.tanh(self.sigma * self.gamma) * (1 - 2 * H_star / self.K)
        return math.sqrt(max(curvature, 0.0))

    @property
    def frustration_ratio(self) -> float:
        """ω_p / ω_natural — near 1.0 = maximum frustration."""
        on = self.omega_natural
        return self._omega / on if on > 0 else float("inf")

    # ── ODE derivatives ──────────────────────────────────────────────────────

    def dH_dt(self, H: float, t: float) -> float:
        """dH/dt = r·H·(1-H/K)·tanh(σΓ) + A·cos(ω_p·t + φ)"""
        utac_term = self.r * H * (1 - H / self.K) * math.tanh(self.sigma * self.gamma)
        forcing = self.amplitude * math.cos(self._omega * t + self.phi0)
        return utac_term + forcing

    # ── Numerical integration (RK4) ──────────────────────────────────────────

    def integrate(
        self,
        H0: float = 0.3,
        t_start: float = 0.0,
        t_end: float | None = None,
        dt: float = 1.0,
        n_orbits: int = 10,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """
        Integrate the frustrated UTAC ODE via RK4.

        Returns (times, H_values) arrays.
        """
        if t_end is None:
            t_end = n_orbits * self.period_days

        steps = int((t_end - t_start) / dt)
        times = np.linspace(t_start, t_end, steps)
        H = np.zeros(steps)
        H[0] = max(1e-6, H0)

        for i in range(steps - 1):
            t = times[i]
            h = H[i]
            k1 = self.dH_dt(h, t)
            k2 = self.dH_dt(h + dt * k1 / 2, t + dt / 2)
            k3 = self.dH_dt(h + dt * k2 / 2, t + dt / 2)
            k4 = self.dH_dt(h + dt * k3, t + dt)
            H[i + 1] = max(0.0, h + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6)

        return times, H

    # ── Fixed point analysis ─────────────────────────────────────────────────

    def fixed_point(self) -> float:
        """H* = K·tanh(σΓ) — the unforced UTAC fixed point."""
        return self.K * math.tanh(self.sigma * self.gamma)

    def is_frustrated(self, tol: float = 0.3) -> bool:
        """True if forcing frequency is close to natural frequency."""
        return abs(self.frustration_ratio - 1.0) < tol
