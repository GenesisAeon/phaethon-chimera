"""PhaethonChimera — Diamond interface (GenesisAeon Package 35)."""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any

import numpy as np

from phaethon_chimera.chimera_detector import ChimeraDetector
from phaethon_chimera.constants import (
    DESTINY_FLYBY_YEAR,
    GAMMA_PHAETHON,
    PACKAGE_NUMBER,
    PHI_CUBEROOT,
    PHAETHON_PERIOD_DAYS,
    ZENODO_DOI,
)
from phaethon_chimera.destiny_predictions import DESTINY_PREDICTIONS, Prediction
from phaethon_chimera.dust_emission import DustEmissionModel
from phaethon_chimera.frustrated_utac import FrustratedUTAC
from phaethon_chimera.geminid_model import GeminidModel
from phaethon_chimera.orbital import PhaethonOrbit
from phaethon_chimera.soc_phaethon import SOCPhaethon


class PhaethonChimera:
    """
    Package 35 — Phaethon-Asteroid: Frustrierte Systeme & Chimera-Zustände.

    Diamond interface: implements run_cycle / get_crep_state / get_utac_state /
    get_phase_events / to_zenodo_record as required by GenesisAeon ecosystem.

    Physical model:
      - Keplerian orbit (PhaethonOrbit)
      - Frustrated UTAC ODE: dH/dt = r·H·(1-H/K)·tanh(σΓ) + A·cos(ω_p·t)
      - Chimera state detection (order parameter R)
      - Stochastic dust emission (Bernoulli with SOC avalanche statistics)
      - 47 DESTINY+ quantitative predictions

    Reference: DESTINY+ mission (JAXA), flyby 2029.
    DOI: 10.5281/zenodo.17472834
    """

    def __init__(self, n_orbits: int = 10, seed: int = 42) -> None:
        self.n_orbits = n_orbits
        self._orbit = PhaethonOrbit()
        self._utac = FrustratedUTAC()
        self._chimera = ChimeraDetector()
        self._dust = DustEmissionModel(seed=seed)
        self._soc = SOCPhaethon()
        self._geminid = GeminidModel()

        self._times: np.ndarray | None = None
        self._H: np.ndarray | None = None
        self._run_results: dict[str, Any] = {}

    # ── Diamond interface ────────────────────────────────────────────────────

    def run_cycle(self, n_orbits: int | None = None) -> dict[str, Any]:
        """
        Full simulation cycle: integrate frustrated UTAC over n_orbits,
        compute chimera state, dust statistics, SOC analysis.
        """
        n = n_orbits or self.n_orbits
        t_end = n * PHAETHON_PERIOD_DAYS

        # Integrate ODE
        times, H = self._utac.integrate(H0=0.3, t_end=t_end, dt=1.0)
        self._times = times
        self._H = H

        # Chimera analysis
        chimera_summary = self._chimera.summary(times, H)

        # Dust emission
        dust_stats = self._dust.emission_statistics(n_orbits=n * 10)

        # SOC analysis
        avalanche_sizes = self._dust.avalanche_sizes(n_events=500)
        soc_report = self._soc.analyse(H, avalanche_sizes)

        # Geminid
        geminid = self._geminid.summary()

        # CREP Γ computation
        gamma = GAMMA_PHAETHON

        self._run_results = {
            "gamma_phaethon": gamma,
            "utac_fixed_point": self._utac.fixed_point(),
            "frustration_ratio": self._utac.frustration_ratio,
            "is_frustrated": self._utac.is_frustrated(),
            "chimera": chimera_summary,
            "dust": dust_stats,
            "soc": soc_report,
            "geminid": geminid,
            "n_orbits_simulated": n,
            "n_destiny_predictions": len(DESTINY_PREDICTIONS),
            "phi_cuberoot": PHI_CUBEROOT,
        }
        return self._run_results

    def get_crep_state(self) -> dict[str, float]:
        """CREP tensor components for Phaethon system."""
        gamma = GAMMA_PHAETHON
        # C: context coherence (orbital predictability vs. stochastic emission)
        C = 0.72  # High: Keplerian orbit is very predictable
        # R: reproducibility (chimera state repeats per orbit)
        R = self._run_results.get("chimera", {}).get("R_mean", 0.50)
        # E: entropy (normalised SOC Hurst exponent)
        E = 0.68  # Hurst > 0.5 → persistent SOC
        # P: productivity (dust events per orbit)
        P = self._run_results.get("dust", {}).get("empirical_probability", 0.23)
        gamma_computed = (C * R * E * P) ** 0.25
        return {
            "C": C,
            "R": float(R),
            "E": E,
            "P": float(P),
            "Gamma": gamma_computed,
            "Gamma_target": gamma,
        }

    def get_utac_state(self) -> dict[str, float]:
        """UTAC ODE parameters for Phaethon."""
        return {
            "r": self._utac.r,
            "K": self._utac.K,
            "sigma": self._utac.sigma,
            "Gamma": self._utac.gamma,
            "H_star": self._utac.fixed_point(),
            "amplitude": self._utac.amplitude,
            "omega_p": self._utac._omega,
            "omega_natural": self._utac.omega_natural,
            "frustration_ratio": self._utac.frustration_ratio,
        }

    def get_phase_events(self) -> list[dict[str, Any]]:
        """Perihelion passages = phase events (UTAC threshold crossings)."""
        events = []
        for i, t in enumerate(self._orbit.perihelion_times(self.n_orbits)):
            orb_state = self._orbit.state_at(t)
            events.append({
                "type": "perihelion",
                "orbit": i,
                "time_days": t,
                "radius_au": orb_state.radius_au,
                "solar_flux": orb_state.solar_flux_relative,
                "is_emission_orbit": self._dust._rng.random() < 0.23,
            })
        return events

    def to_zenodo_record(self) -> dict[str, Any]:
        """Metadata record for Zenodo deposition."""
        return {
            "title": "Phaethon-Chimera: Frustrated UTAC Systems & Chimera States (Package 35)",
            "description": (
                "GenesisAeon Package 35 — UTAC modelling of 3200 Phaethon as a frustrated "
                "chimera system. Implements: FrustratedUTAC ODE, ChimeraDetector (Kuramoto R), "
                "SOC avalanche statistics, stochastic dust emission, and 47 quantitative "
                "predictions for the DESTINY+ JAXA mission (flyby 2029). "
                f"CREP coupling: Γ_phaethon ≈ {GAMMA_PHAETHON} "
                "(between Amazon 0.116 and AMOC 0.251)."
            ),
            "keywords": [
                "phaethon", "asteroid", "chimera-state", "frustrated-systems",
                "UTAC", "CREP", "SOC", "DESTINY+", "meteor-shower", "Geminids",
                "GenesisAeon", "complex-systems", "orbital-mechanics",
            ],
            "creators": [{"name": "Römer, Johann", "affiliation": "MOR Research Collective"}],
            "version": "1.0.0",
            "license": "MIT",
            "zenodo_doi": ZENODO_DOI,
            "related_identifiers": [
                {"relation": "isPartOf", "identifier": ZENODO_DOI},
                {"relation": "isDocumentedBy", "identifier": "10.5281/zenodo.19645351"},
            ],
            "package_number": PACKAGE_NUMBER,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    # ── Convenience accessors ────────────────────────────────────────────────

    def destiny_predictions(self) -> list[Prediction]:
        """All 47 DESTINY+ testable predictions."""
        return DESTINY_PREDICTIONS

    def chimera_order_parameter(self) -> float:
        """Current R ∈ [0,1] chimera state measure (from last run_cycle)."""
        if self._times is None or self._H is None:
            return 0.5
        return self._chimera.order_parameter(self._times, self._H)

    def v_rig_normalised(self) -> float:
        """v_RIG at Phaethon surface (normalised to orbital velocity)."""
        v_orbital_km_s = 2 * math.pi * self._orbit._semi_major_au * 1.496e8 / (
            self._orbit.period_days * 86400
        )
        v_rig_km_s = 1352.12
        return v_rig_km_s / v_orbital_km_s

    def __repr__(self) -> str:
        return (
            f"PhaethonChimera(Γ={GAMMA_PHAETHON}, n_orbits={self.n_orbits}, "
            f"n_predictions={len(DESTINY_PREDICTIONS)}, flyby={DESTINY_FLYBY_YEAR})"
        )
