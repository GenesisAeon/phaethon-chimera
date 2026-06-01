"""SOC (Self-Organised Criticality) statistics for Phaethon's dust activity."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from phaethon_chimera.constants import SOC_TAU_EXPONENT


class SOCPhaethon:
    """
    Self-Organised Criticality analysis of Phaethon dust emission.

    The dust emission process shows SOC signatures:
    - Power-law avalanche size distribution P(s) ∝ s^{-τ}, τ ≈ 1.3
    - Scale-free waiting time distribution
    - Fractal temporal structure (Hurst exponent H > 0.5)

    This characterises Phaethon as an SOC system competing with
    its Keplerian periodicity — the frustrated chimera state.
    """

    def __init__(self, tau: float = SOC_TAU_EXPONENT, seed: int = 42) -> None:
        self.tau = tau
        self._rng = np.random.default_rng(seed)

    # ── Power-law fit ────────────────────────────────────────────────────────

    def fit_powerlaw(self, data: NDArray[np.float64], s_min: float | None = None) -> dict[str, float]:
        """
        Fit power-law exponent via MLE Hill estimator.

        Returns dict with tau_hat, confidence interval, and KS p-value.
        """
        s_min = s_min or float(np.percentile(data, 20))
        data_filtered = data[data >= s_min]
        n = len(data_filtered)
        if n < 5:
            return {"tau_hat": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"), "p_ks": 0.0}

        tau_hat = 1 + n / np.sum(np.log(data_filtered / s_min))

        # Bootstrap CI
        taus = []
        for _ in range(200):
            sample = self._rng.choice(data_filtered, size=n, replace=True)
            taus.append(1 + n / np.sum(np.log(sample / s_min)))
        ci = np.percentile(taus, [2.5, 97.5])

        # KS test: theoretical vs. empirical
        theoretical = stats.pareto(b=tau_hat - 1, scale=s_min)
        _, p_ks = stats.kstest(data_filtered, theoretical.cdf)

        return {
            "tau_hat": float(tau_hat),
            "ci_low": float(ci[0]),
            "ci_high": float(ci[1]),
            "p_ks": float(p_ks),
            "n_events": n,
            "s_min": s_min,
        }

    def is_consistent_with_soc(self, tau_hat: float, p_ks: float) -> bool:
        """True if fitted τ is consistent with SOC prediction (τ ≈ 1.3)."""
        return abs(tau_hat - self.tau) < 0.3 and p_ks > 0.05

    # ── Hurst exponent (fractal time series) ────────────────────────────────

    @staticmethod
    def hurst_exponent(series: NDArray[np.float64]) -> float:
        """
        Estimate Hurst exponent H via R/S analysis.
        H > 0.5 → persistent (long-range correlated) → SOC signature.
        """
        n = len(series)
        lags = [2 ** k for k in range(2, int(np.log2(n)) - 1)]
        rs_values = []
        for lag in lags:
            chunks = [series[i : i + lag] for i in range(0, n - lag, lag)]
            rs_chunk = []
            for chunk in chunks:
                mean_c = np.mean(chunk)
                dev = np.cumsum(chunk - mean_c)
                R = np.ptp(dev)
                S = np.std(chunk, ddof=1)
                if S > 0:
                    rs_chunk.append(R / S)
            if rs_chunk:
                rs_values.append((lag, np.mean(rs_chunk)))

        if len(rs_values) < 2:
            return 0.5

        log_lags = np.log([r[0] for r in rs_values])
        log_rs = np.log([r[1] for r in rs_values])
        slope, *_ = np.polyfit(log_lags, log_rs, 1)
        return float(slope)

    # ── Full SOC report ─────────────────────────────────────────────────────

    def analyse(
        self,
        H_series: NDArray[np.float64],
        avalanche_sizes: NDArray[np.float64],
    ) -> dict[str, float | bool]:
        fit = self.fit_powerlaw(avalanche_sizes)
        hurst = self.hurst_exponent(H_series)
        soc_ok = self.is_consistent_with_soc(
            float(fit.get("tau_hat", 0.0)),
            float(fit.get("p_ks", 0.0)),
        )
        return {
            **fit,
            "hurst_exponent": hurst,
            "persistent": hurst > 0.5,
            "soc_confirmed": soc_ok,
            "target_tau": self.tau,
        }
