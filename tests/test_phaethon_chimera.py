"""Tests for Package 35 — phaethon-chimera."""

from __future__ import annotations

import math

import numpy as np
import pytest

from phaethon_chimera.constants import (
    CHIMERA_R_PERIHELION,
    EMISSION_PROBABILITY,
    GAMMA_PHAETHON,
    PHI,
    PHI_CUBEROOT,
    SOC_TAU_EXPONENT,
    UTAC_SIGMA,
)
from phaethon_chimera.destiny_predictions import DESTINY_PREDICTIONS, prediction_summary
from phaethon_chimera.dust_emission import DustEmissionModel
from phaethon_chimera.frustrated_utac import FrustratedUTAC
from phaethon_chimera.geminid_model import GeminidModel
from phaethon_chimera.orbital import PhaethonOrbit
from phaethon_chimera.soc_phaethon import SOCPhaethon
from phaethon_chimera.system import PhaethonChimera


# ── Constants ────────────────────────────────────────────────────────────────

def test_phi_cuberoot():
    assert abs(PHI_CUBEROOT - PHI ** (1 / 3)) < 1e-10


def test_phi_cuberoot_value():
    import math
    assert abs(PHI_CUBEROOT - ((1 + math.sqrt(5)) / 2) ** (1 / 3)) < 1e-10


def test_gamma_phaethon_between_amazon_and_amoc():
    assert 0.116 < GAMMA_PHAETHON < 0.251


def test_sigma_phi():
    from phaethon_chimera.constants import SIGMA_PHI
    assert abs(SIGMA_PHI - 1 / 16) < 1e-12


# ── Orbital ──────────────────────────────────────────────────────────────────

def test_orbit_radius_perihelion():
    orbit = PhaethonOrbit()
    r = orbit.radius(0.0)  # t=0 ~ perihelion
    assert abs(r - orbit.perihelion_au) < 0.01


def test_orbit_radius_positive():
    orbit = PhaethonOrbit()
    for t in [0, 100, 250, 500]:
        assert orbit.radius(float(t)) > 0


def test_orbital_state():
    orbit = PhaethonOrbit()
    state = orbit.state_at(0.0)
    assert state.solar_flux_relative > 1.0  # at perihelion: flux > 1 AU


def test_perihelion_times_count():
    orbit = PhaethonOrbit()
    times = orbit.perihelion_times(5)
    assert len(times) == 6  # 0..5 inclusive


# ── FrustratedUTAC ───────────────────────────────────────────────────────────

def test_utac_fixed_point():
    utac = FrustratedUTAC()
    H_star = utac.fixed_point()
    assert 0.1 < H_star < 0.9


def test_utac_integration_shape():
    utac = FrustratedUTAC()
    times, H = utac.integrate(n_orbits=3)
    assert len(times) == len(H)
    assert len(times) > 100


def test_utac_H_stays_non_negative():
    utac = FrustratedUTAC()
    _, H = utac.integrate(n_orbits=5)
    assert np.all(H >= 0)


def test_utac_frustration_ratio():
    utac = FrustratedUTAC()
    assert utac.frustration_ratio > 0


def test_utac_omega_natural_positive():
    utac = FrustratedUTAC()
    assert utac.omega_natural >= 0


# ── DustEmissionModel ────────────────────────────────────────────────────────

def test_dust_emission_probability():
    model = DustEmissionModel(seed=42)
    stats = model.emission_statistics(n_orbits=2000)
    p_emp = stats["empirical_probability"]
    # Should be within 3σ of EMISSION_PROBABILITY
    assert abs(p_emp - EMISSION_PROBABILITY) < 0.06


def test_dust_avalanche_power_law():
    model = DustEmissionModel(seed=42)
    sizes = model.avalanche_sizes(n_events=1000)
    assert np.all(sizes > 0)
    assert np.max(sizes) > np.min(sizes)


def test_dust_fit_tau():
    model = DustEmissionModel(seed=42)
    sizes = model.avalanche_sizes(n_events=1000)
    tau_hat = model.fit_tau(sizes)
    assert abs(tau_hat - SOC_TAU_EXPONENT) < 0.5


def test_dust_peak_flux_at_perihelion():
    model = DustEmissionModel()
    from phaethon_chimera.constants import PHAETHON_PERIHELION_AU
    flux = model.peak_flux(PHAETHON_PERIHELION_AU)
    assert 0 < flux <= 1.0


# ── SOCPhaethon ──────────────────────────────────────────────────────────────

def test_soc_powerlaw_fit():
    soc = SOCPhaethon(seed=42)
    rng = np.random.default_rng(42)
    # Synthetic Pareto data with τ ≈ 1.3
    sizes = rng.pareto(SOC_TAU_EXPONENT - 1, size=300) + 1.0
    fit = soc.fit_powerlaw(sizes)
    assert abs(fit["tau_hat"] - SOC_TAU_EXPONENT) < 0.5


def test_hurst_persistent():
    soc = SOCPhaethon(seed=42)
    # Long-range correlated series (AR1 with high correlation)
    rng = np.random.default_rng(0)
    x = np.zeros(512)
    x[0] = rng.standard_normal()
    for i in range(1, 512):
        x[i] = 0.85 * x[i - 1] + 0.1 * rng.standard_normal()
    H = soc.hurst_exponent(x)
    assert H > 0.5  # persistent


# ── DESTINY+ Predictions ─────────────────────────────────────────────────────

def test_n_destiny_predictions():
    assert len(DESTINY_PREDICTIONS) == 47


def test_prediction_ids_unique():
    ids = [p.id for p in DESTINY_PREDICTIONS]
    assert len(ids) == len(set(ids))


def test_prediction_categories_summary():
    summary = prediction_summary()
    assert "CREP" in summary
    assert "Chimera" in summary
    assert "SOC" in summary
    assert "Dust" in summary
    assert "Mission" in summary
    assert sum(summary.values()) == 47


def test_gamma_phaethon_prediction():
    gamma_pred = next(p for p in DESTINY_PREDICTIONS if p.quantity == "Gamma_phaethon")
    assert abs(gamma_pred.value - GAMMA_PHAETHON) < 1e-6


def test_chimera_altitude_prediction():
    pred = next(p for p in DESTINY_PREDICTIONS if "altitude" in p.quantity)
    assert abs(pred.value - 2.3) < 0.01


# ── GeminidModel ─────────────────────────────────────────────────────────────

def test_geminid_zhr_reasonable():
    gm = GeminidModel()
    s = gm.summary()
    assert 50 < s["predicted_zhr"] < 300


def test_geminid_ejection_velocity():
    gm = GeminidModel()
    v = gm.ejection_velocity_ms()
    assert 0.5 < v < 3.0  # m/s


def test_geminid_n_orbits():
    gm = GeminidModel()
    n = gm.n_orbits_in_stream_age
    assert 1000 < n < 2000


# ── PhaethonChimera Diamond Interface ────────────────────────────────────────

def test_phaethon_chimera_run_cycle():
    pc = PhaethonChimera(n_orbits=3)
    results = pc.run_cycle()
    assert "gamma_phaethon" in results
    assert "chimera" in results
    assert "soc" in results
    assert results["n_destiny_predictions"] == 47


def test_get_crep_state():
    pc = PhaethonChimera(n_orbits=3)
    pc.run_cycle()
    crep = pc.get_crep_state()
    assert "Gamma" in crep
    assert 0 < crep["Gamma"] < 1
    assert 0 < crep["C"] <= 1


def test_get_utac_state():
    pc = PhaethonChimera(n_orbits=3)
    utac_state = pc.get_utac_state()
    assert utac_state["sigma"] == UTAC_SIGMA
    assert utac_state["Gamma"] == GAMMA_PHAETHON


def test_get_phase_events():
    pc = PhaethonChimera(n_orbits=5)
    events = pc.get_phase_events()
    assert len(events) == 6  # 0..5
    assert events[0]["type"] == "perihelion"


def test_to_zenodo_record():
    pc = PhaethonChimera(n_orbits=2)
    record = pc.to_zenodo_record()
    assert record["package_number"] == 35
    assert "phaethon" in record["keywords"]
    assert "DESTINY+" in record["keywords"]


def test_chimera_order_parameter_before_run():
    pc = PhaethonChimera(n_orbits=2)
    R = pc.chimera_order_parameter()
    assert 0 <= R <= 1


def test_chimera_order_parameter_after_run():
    pc = PhaethonChimera(n_orbits=5)
    pc.run_cycle()
    R = pc.chimera_order_parameter()
    assert 0 <= R <= 1


def test_repr():
    pc = PhaethonChimera()
    assert "PhaethonChimera" in repr(pc)
    assert "0.165" in repr(pc)
