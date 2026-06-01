"""Benchmark targets and validation for Package 35."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from phaethon_chimera.constants import (
    CHIMERA_R_PERIHELION,
    EMISSION_PROBABILITY,
    GAMMA_PHAETHON,
    SOC_TAU_EXPONENT,
)

BENCHMARK_TARGETS: dict[str, tuple[float, float | None]] = {
    "gamma_phaethon":          (GAMMA_PHAETHON, 0.02),
    "chimera_R_perihelion":    (CHIMERA_R_PERIHELION, 0.10),
    "soc_tau_exponent":        (SOC_TAU_EXPONENT, 0.10),
    "emission_probability":    (EMISSION_PROBABILITY, 0.08),
    "geminid_zhr":             (120.0, 30.0),
    "n_destiny_predictions":   (47.0, 0.0),
    "phi_cuberoot":            (1.17480502, 0.00001),
    "hurst_exponent_min":      (0.5, None),  # H > 0.5 for SOC
    "chimera_altitude_km":     (2.3, 0.4),
}


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
    if tol is None:
        passed = actual > target  # e.g. Hurst > 0.5
    else:
        passed = abs(actual - target) <= tol
    return BenchmarkResult(
        key=key,
        target=target,
        tolerance=tol,
        actual=actual,
        passed=passed,
        delta=actual - target,
    )


def run_benchmark(results: dict[str, Any]) -> dict[str, BenchmarkResult]:
    """Run benchmark checks against BENCHMARK_TARGETS."""
    checks: dict[str, BenchmarkResult] = {}
    for key in BENCHMARK_TARGETS:
        if key in results:
            checks[key] = check_target(key, float(results[key]))
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
