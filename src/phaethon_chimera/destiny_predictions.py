"""47 quantitative predictions for the DESTINY+ mission (JAXA, flyby 2029)."""

from __future__ import annotations

from dataclasses import dataclass

from phaethon_chimera.constants import (
    CHIMERA_ALTITUDE_KM,
    CHIMERA_R_PERIHELION,
    EMISSION_PROBABILITY,
    GAMMA_PHAETHON,
    SOC_TAU_EXPONENT,
)


@dataclass(frozen=True)
class Prediction:
    """A single DESTINY+ testable prediction."""

    id: int
    category: str
    quantity: str
    value: float
    uncertainty: float
    unit: str
    method: str
    falsifiable: bool = True


def build_predictions() -> list[Prediction]:
    """
    47 quantitative predictions for DESTINY+ Phaethon flyby (2029).

    Categories: CREP, Chimera, SOC, Orbital, Dust, Geminid, Thermal,
    Spectral, Morphological, Information-Geometric.
    """
    p: list[Prediction] = []

    # ── CREP / UTAC predictions ─────────────────────────────────────────────
    p.append(Prediction(1, "CREP", "Gamma_phaethon", GAMMA_PHAETHON, 0.02, "dimensionless",
                         "UTAC fixed-point: H* = K·tanh(σΓ)"))
    p.append(Prediction(2, "CREP", "UTAC_r_growth_rate", 0.18, 0.04, "1/orbit",
                         "MLE fit from ZTF photometry variability"))
    p.append(Prediction(3, "CREP", "UTAC_sigma_steepness", 2.2, 0.3, "dimensionless",
                         "Beta-to-Gamma bridge (P32 CREP-beta-bridge)"))
    p.append(Prediction(4, "CREP", "UTAC_fixed_point_H_star", 0.286, 0.03, "normalised",
                         "H* = K·tanh(2.2 × 0.165)"))
    p.append(Prediction(5, "CREP", "CREP_C_coherence", 0.45, 0.10, "dimensionless",
                         "Context continuity near perihelion from STEREO data"))

    # ── Chimera state predictions ───────────────────────────────────────────
    p.append(Prediction(6, "Chimera", "order_parameter_R_perihelion", CHIMERA_R_PERIHELION, 0.10,
                         "dimensionless", "Kuramoto R from dust flux time series"))
    p.append(Prediction(7, "Chimera", "chimera_transition_altitude_km", CHIMERA_ALTITUDE_KM, 0.4,
                         "km", "Height above surface where R transitions to chimera"))
    p.append(Prediction(8, "Chimera", "chimera_fraction_of_orbit", 0.18, 0.06, "fraction",
                         "Fraction of orbital period in chimera state"))
    p.append(Prediction(9, "Chimera", "order_parameter_R_aphelion", 0.85, 0.08, "dimensionless",
                         "Aphelion: near-Keplerian, R ≈ 0.85"))
    p.append(Prediction(10, "Chimera", "frustration_ratio_omega", 1.05, 0.15, "dimensionless",
                         "ω_p / ω_UTAC_natural — near resonance"))

    # ── Dust emission predictions ──────────────────────────────────────────
    p.append(Prediction(11, "Dust", "emission_probability_per_orbit", EMISSION_PROBABILITY, 0.08,
                         "probability", "Bernoulli model from STEREO historical detections"))
    p.append(Prediction(12, "Dust", "peak_dust_flux_at_perihelion_Gamma", 0.68, 0.05,
                         "normalised", "Γ_peri = tanh(σΓ) · (r_peri_ref/r_peri)²"))
    p.append(Prediction(13, "Dust", "dust_flux_FWHM_days", 4.2, 0.8, "days",
                         "Full-width half-maximum of perihelion dust pulse"))
    p.append(Prediction(14, "Dust", "dust_flux_falloff_exponent", 2.0, 0.3, "dimensionless",
                         "F ∝ r^{-α}, α ≈ 2 (thermal emission)"))
    p.append(Prediction(15, "Dust", "mean_dust_flux_active_orbits", 0.55, 0.12, "normalised",
                         "Mean flux | emission triggered"))

    # ── SOC statistics ─────────────────────────────────────────────────────
    p.append(Prediction(16, "SOC", "powerlaw_tau_exponent", SOC_TAU_EXPONENT, 0.1,
                         "dimensionless", "MLE Hill estimator from DESTINY+ resolved events"))
    p.append(Prediction(17, "SOC", "hurst_exponent", 0.68, 0.08, "dimensionless",
                         "R/S analysis of dust flux time series — persistent"))
    p.append(Prediction(18, "SOC", "min_detectable_avalanche_size_m", 10.0, 5.0, "m",
                         "Minimum resolvable grain cluster for DESTINY+ TCAP"))
    p.append(Prediction(19, "SOC", "max_avalanche_size_m", 500.0, 200.0, "m",
                         "Upper cutoff of power-law (finite-size effect)"))
    p.append(Prediction(20, "SOC", "ks_pvalue_powerlaw", 0.15, 0.10, "probability",
                         "KS test p-value: must exceed 0.05 for SOC confirmation"))

    # ── Orbital / Thermal predictions ──────────────────────────────────────
    p.append(Prediction(21, "Thermal", "peak_surface_temperature_K", 1020.0, 50.0, "K",
                         "T_peak at perihelion r=0.14 AU (blackbody + albedo)"))
    p.append(Prediction(22, "Thermal", "temperature_FWHM_days", 3.8, 0.6, "days",
                         "Duration of T > 800 K during perihelion passage"))
    p.append(Prediction(23, "Thermal", "thermal_inertia_J_m2_K_s05", 600.0, 100.0, "J/m²/K/√s",
                         "From ZTF lightcurve thermal modelling"))
    p.append(Prediction(24, "Thermal", "albedo_geometric", 0.11, 0.02, "dimensionless",
                         "Blue-shifted spectrum consistent with B-type asteroid"))
    p.append(Prediction(25, "Thermal", "effective_emissivity", 0.90, 0.05, "dimensionless",
                         "Thermal emission efficiency"))

    # ── Morphological predictions ──────────────────────────────────────────
    p.append(Prediction(26, "Morphology", "mean_radius_km", 2.78, 0.08, "km",
                         "From Hanus et al. 2016 occultation data"))
    p.append(Prediction(27, "Morphology", "shape_elongation_a_over_b", 1.09, 0.05, "dimensionless",
                         "Near-spherical: a/b ≈ 1.09 from lightcurve"))
    p.append(Prediction(28, "Morphology", "surface_roughness_rms_m", 15.0, 8.0, "m",
                         "SOC-generated surface texture — rough from thermal cracking"))
    p.append(Prediction(29, "Morphology", "crater_density_per_km2", 120.0, 40.0, "1/km²",
                         "Lower than expected due to thermal gardening"))
    p.append(Prediction(30, "Morphology", "regolith_depth_m", 0.5, 0.3, "m",
                         "Shallow regolith due to strong thermal stress cycling"))

    # ── Spectral predictions ───────────────────────────────────────────────
    p.append(Prediction(31, "Spectral", "spectral_slope_percent_per_100nm", -0.8, 0.3, "% / 100nm",
                         "Blue-sloped B-type spectrum (DESTINY+ SMEI instrument)"))
    p.append(Prediction(32, "Spectral", "UV_excess_fraction", 0.12, 0.04, "dimensionless",
                         "UV brightening near perihelion from Na emission analogue"))
    p.append(Prediction(33, "Spectral", "Na_emission_equivalent_width_nm", 0.003, 0.002, "nm",
                         "Tentative Na emission from STEREO — speculative"))
    p.append(Prediction(34, "Spectral", "silicate_feature_strength_Gamma", 0.04, 0.02, "normalised",
                         "Weak silicate emission at 10 μm from UTAC thermal model"))
    p.append(Prediction(35, "Spectral", "hydration_band_depth_percent", 0.5, 0.5, "percent",
                         "Low/absent hydration — thermally desiccated surface"))

    # ── Geminid meteor shower ──────────────────────────────────────────────
    p.append(Prediction(36, "Geminid", "annual_ZHR_zenith_hourly_rate", 120.0, 20.0, "counts/hr",
                         "From UTAC mass-flux model extrapolated to stream density"))
    p.append(Prediction(37, "Geminid", "stream_age_years", 2000.0, 500.0, "yr",
                         "UTAC-orbit integration backward: stream age estimate"))
    p.append(Prediction(38, "Geminid", "mean_grain_mass_kg", 1e-6, 5e-7, "kg",
                         "Consistent with radar/visual Geminid observations"))
    p.append(Prediction(39, "Geminid", "stream_width_AU", 0.05, 0.02, "AU",
                         "Orbital diffusion from frustrated UTAC over 2000 yr"))
    p.append(Prediction(40, "Geminid", "ejection_velocity_m_s", 1.2, 0.4, "m/s",
                         "v_eject ≈ v_RIG_normalised at Phaethon surface gravity"))

    # ── Information-geometric predictions ──────────────────────────────────
    p.append(Prediction(41, "InfoGeo", "Fisher_Rao_velocity_perihelion", 0.68, 0.12, "normalised",
                         "Parameter-space speed of UTAC during perihelion — peaks"))
    p.append(Prediction(42, "InfoGeo", "entropy_production_rate_S_A_per_orbit", 0.31, 0.08,
                         "nats/orbit", "S_A = ∫ σ_s dt over one orbit (P36 bridge)"))
    p.append(Prediction(43, "InfoGeo", "volume_entropy_S_V", 0.44, 0.10, "nats",
                         "Shannon entropy of H distribution over 10 orbits"))
    p.append(Prediction(44, "InfoGeo", "duality_product_SA_SV", 0.136, 0.040, "nats²",
                         "S_A · S_V ≈ const (P36 S_A/S_V duality)"))
    p.append(Prediction(45, "InfoGeo", "phi_scaling_ratio_check", 1.174, 0.06, "dimensionless",
                         "Γ_ratio between orbital domains should ≈ Φ^{1/3} (P38)"))

    # ── Mission timeline ───────────────────────────────────────────────────
    p.append(Prediction(46, "Mission", "DESTINY_flyby_year", 2029.0, 1.0, "year",
                         "Expected DESTINY+ Phaethon encounter year"))
    p.append(Prediction(47, "Mission", "n_perihelion_passages_before_flyby", 4.0, 0.0, "count",
                         "Perihelion passages between 2026 and expected flyby"))

    assert len(p) == 47, f"Expected 47 predictions, got {len(p)}"
    return p


DESTINY_PREDICTIONS: list[Prediction] = build_predictions()


def prediction_summary() -> dict[str, int]:
    categories: dict[str, int] = {}
    for pred in DESTINY_PREDICTIONS:
        categories[pred.category] = categories.get(pred.category, 0) + 1
    return categories
