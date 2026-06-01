"""Chimera state detection: partial synchronisation between ordered and SOC dynamics."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from phaethon_chimera.constants import CHIMERA_R_PERIHELION, PHAETHON_PERIOD_DAYS


class ChimeraDetector:
    """
    Detects chimera states via the Kuramoto-style order parameter R.

    For a trajectory H(t), the instantaneous phase θ(t) is estimated
    from the Hilbert transform. The order parameter:

        R = |<e^{iθ_j}>|   over a window of N cycles

    R ≈ 1: fully synchronised (pure Keplerian)
    R ≈ 0: fully disordered (pure SOC)
    0 < R < 1: chimera state

    Phaethon prediction: R ≈ 0.50 near perihelion.
    """

    def __init__(self, period_days: float = PHAETHON_PERIOD_DAYS, window_orbits: int = 3) -> None:
        self.period_days = period_days
        self.window_orbits = window_orbits

    # ── Phase estimation ────────────────────────────────────────────────────

    @staticmethod
    def _instantaneous_phase(H: NDArray[np.float64]) -> NDArray[np.float64]:
        """Estimate phase via analytic signal (Hilbert transform approximation)."""
        # Simple zero-crossing phase for single-frequency signal
        H_centered = H - H.mean()
        phase = np.unwrap(np.arctan2(
            np.imag(np.fft.ifft(
                -1j * np.sign(np.fft.fftfreq(len(H))) * np.fft.fft(H_centered)
            )).real,
            H_centered,
        ))
        return phase

    # ── Order parameter ─────────────────────────────────────────────────────

    def order_parameter(
        self,
        times: NDArray[np.float64],
        H: NDArray[np.float64],
        t_window_start: float | None = None,
        t_window_end: float | None = None,
    ) -> float:
        """
        Compute R ∈ [0, 1] over a time window.

        Higher R near perihelion → less chimera (more Keplerian).
        Lower R → more disordered (SOC-dominated).
        """
        if t_window_start is not None:
            mask = (times >= t_window_start) & (times <= (t_window_end or times[-1]))
            H_win = H[mask]
        else:
            H_win = H

        if len(H_win) < 10:
            return 0.5  # Insufficient data → neutral estimate

        phase = self._instantaneous_phase(H_win)
        R = float(np.abs(np.mean(np.exp(1j * phase))))
        return min(1.0, max(0.0, R))

    # ── Per-orbit order parameters ──────────────────────────────────────────

    def order_parameter_per_orbit(
        self,
        times: NDArray[np.float64],
        H: NDArray[np.float64],
    ) -> list[dict[str, float]]:
        """Compute R for each orbital period. Perihelion windows expected low R."""
        results = []
        t_max = times[-1]
        t = 0.0
        while t + self.period_days <= t_max:
            R = self.order_parameter(times, H, t, t + self.period_days)
            results.append({"t_start": t, "t_end": t + self.period_days, "R": R})
            t += self.period_days
        return results

    # ── Chimera classification ──────────────────────────────────────────────

    @staticmethod
    def classify(R: float) -> str:
        if R > 0.85:
            return "ordered"
        elif R < 0.15:
            return "disordered"
        else:
            return "chimera"

    def chimera_fraction(
        self,
        times: NDArray[np.float64],
        H: NDArray[np.float64],
    ) -> float:
        """Fraction of orbital periods in chimera state."""
        per_orbit = self.order_parameter_per_orbit(times, H)
        if not per_orbit:
            return 0.0
        chimera_count = sum(1 for o in per_orbit if self.classify(o["R"]) == "chimera")
        return chimera_count / len(per_orbit)

    def perihelion_R(
        self,
        times: NDArray[np.float64],
        H: NDArray[np.float64],
        window_days: float = 5.0,
    ) -> float:
        """Order parameter near perihelion passages — key DESTINY+ prediction."""
        R_values = []
        t_max = times[-1]
        t = 0.0
        while t <= t_max:
            R = self.order_parameter(times, H, max(0, t - window_days), t + window_days)
            R_values.append(R)
            t += self.period_days
        return float(np.mean(R_values)) if R_values else CHIMERA_R_PERIHELION

    def summary(
        self,
        times: NDArray[np.float64],
        H: NDArray[np.float64],
    ) -> dict[str, float | str]:
        R_mean = self.order_parameter(times, H)
        R_peri = self.perihelion_R(times, H)
        return {
            "R_mean": R_mean,
            "R_perihelion": R_peri,
            "chimera_fraction": self.chimera_fraction(times, H),
            "classification": self.classify(R_mean),
        }
