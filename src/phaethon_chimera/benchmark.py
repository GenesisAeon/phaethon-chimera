"""Benchmark targets and validation for Package 35."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from phaethon_chimera.constants import (
    CHIMERA_ALTITUDE_KM,
    CHIMERA_R_PERIHELION,
    EMISSION_PROBABILITY,
    GAMMA_PHAETHON,
    PHI_CUBEROOT,
    SOC_TAU_EXPONENT,
)

BENCHMARK_TARGETS: dict[str, tuple[float, float | None]] = {
    "gamma_phaethon":          (GAMMA_PHAETHON, 0.02),
    "chimera_R_perihelion":    (CHIMERA_R_PERIHELION, 0.10),
    "soc_tau_exponent":        (SOC_TAU_EXPONENT, 0.10),
    "emission_probability":    (EMISSION_PROBABILITY, 0.08),
    "geminid_zhr":             (120.0, 30.0),
    "n_destiny_predictions":   (47.0, 0.0),
    "phi_cuberoot":            (PHI_CUBEROOT, 1e-8),
    "hurst_exponent_min":      (0.5, None),  # H > 0.5 for SOC
    "chimera_altitude_km":     (CHIMERA_ALTITUDE_KM, 0.4),
}

# Mapping: BENCHMARK_TARGETS key -> path in run_cycle() output
# Nested values are addressed with dot notation: "parent.child"
_KEY_PATH: dict[str, str] = {
    "gamma_phaethon":         "gamma_phaethon",
    "chimera_R_perihelion":   "chimera.R_perihelion",
    "soc_tau_exponent":       "soc.tau_hat",
    "emission_probability":   "dust.empirical_probability",
    "geminid_zhr":            "geminid.predicted_zhr",
    "n_destiny_predictions":  "n_destiny_predictions",
    "phi_cuberoot":           "phi_cuberoot",
    "hurst_exponent_min":     "soc.hurst_exponent",
    "chimera_altitude_km":    "chimera_altitude_km",
}


def _extract(results: dict[str, Any], path: str) -> float | None:
    """Traverse dot-separated path into nested dict. Returns None if missing."""
    parts = path.split(".")
    obj: Any = results
    for part in parts:
        if not isinstance(obj, dict) or part not in obj:
            return None
        obj = obj[part]
    try:
        return float(obj)
    except (TypeError, ValueError):
        return None


@dataclass
class BenchmarkResult:
    key: str
    target: float
    tolerance: float | None
    actual: float
    passed: bool
    delta: float


def check_target(key: str, actual: float) -> BenchmarkResult:
    target, tol = BENCHMARK_TARGETS[key]
    passed = actual > target if tol is None else abs(actual - target) <= tol
    return BenchmarkResult(
        key=key,
        target=target,
        tolerance=tol,
        actual=actual,
        passed=passed,
        delta=actual - target,
    )


def run_benchmark(results: dict[str, Any]) -> dict[str, BenchmarkResult]:
    """
    Run benchmark checks against BENCHMARK_TARGETS.

    Accepts the direct output of PhaethonChimera.run_cycle() — nested keys
    (chimera.R_perihelion, soc.tau_hat, etc.) are resolved automatically.
    """
    checks: dict[str, BenchmarkResult] = {}
    for key, path in _KEY_PATH.items():
        value = _extract(results, path)
        if value is not None:
            checks[key] = check_target(key, value)
    return checks


def print_benchmark_report(checks: dict[str, BenchmarkResult]) -> None:
    print("\n── Phaethon-Chimera P35 Benchmark ──────────────────────")
    for r in checks.values():
        status = "✓" if r.passed else "✗"
        tol_str = f"±{r.tolerance}" if r.tolerance is not None else ">target"
        print(f"  {status} {r.key:<35} {r.actual:.4f}  (target {r.target} {tol_str})")
    n_pass = sum(1 for r in checks.values() if r.passed)
    print(f"\n  {n_pass}/{len(checks)} benchmarks passed")
    print("────────────────────────────────────────────────────────\n")
