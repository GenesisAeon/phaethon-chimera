# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.4] - 2026-09-15

### Revised (Prediction #47, real orbital data)
- The 1.0.3 audit flagged Prediction #47 (perihelion passages before
  flyby, value 4.0) as inconsistent with a naive period-division
  estimate (~2.8 passages). Pulled real orbital elements from JPL SBDB
  (tp=JD 2461285.616438 TDB, period=523.6665665 d, solution 2026-06-25):
  actual perihelion passages fall on 2026-09-02, 2028-02-07, 2029-07-15,
  and 2030-12-21 -- not evenly spaced across calendar years the way a
  period-division estimate assumes. `4.0` IS consistent with real data
  if the JFY2030 flyby (Apr 2030-Mar 2031) occurs on or after
  2030-12-21; `3.0` would be correct if it occurs earlier in that
  fiscal year. JAXA's public schedule states only "JFY2030" with no
  month yet published, so this stays open -- narrowed from "unclear by
  ~2" to "exactly 3 or 4, pending JAXA's flyby-month announcement," not
  force-resolved either way.

## [1.0.3] - 2026-09-15

### Fixed (real, independently verified errors found during the DESTINY+
predictions audit — spot-checking predictions citing external sources)
- **#26 (mean radius)**: was `2.78 km` attributed to "Hanus et al. 2016
  occultation data". The real Hanus et al. 2016 (A&A 592, A34) result is
  an effective *diameter* of 5.1±0.2 km from *thermophysical* modelling
  of infrared data, not an occultation measurement — neither the value
  nor the method matched. Corrected to `PHAETHON_RADIUS_KM = 2.55 km`
  (= 5.1/2), citation corrected.
- **#40 (ejection velocity)**: was hardcoded to `1.2 m/s`, but
  `GeminidModel.ejection_velocity_ms()` — the package's own escape-
  velocity function, `v_esc = sqrt(2GM/r)` — was never actually called
  to produce this value. Running it with its own stated inputs
  (ρ=1700 kg/m³) gives ≈2.49 m/s at the corrected radius. Corrected the
  prediction and the function's own docstring, which made the same
  wrong claim.
- **#46 (DESTINY+ flyby year)**: was `2029`, an earlier mission plan.
  JAXA's current public schedule (launch-vehicle change to H3) targets
  JFY2028 launch / JFY2030 Phaethon flyby. Corrected `DESTINY_FLYBY_YEAR`
  and propagated to README.md, `.zenodo.json`, `__init__.py`,
  `system.py`.
- **`data/ztf_photometry_summary.yaml`**: flagged (not deleted) — this
  file is never actually loaded by any code, and its `genesisaeon_utac_fit`
  section's values exactly equal pre-existing ecosystem defaults
  (σ=2.2, Γ=0.165) rather than being a credible independent fit from
  2 STEREO detections + 1 ZTF amplitude number.

### Documented (open issue, not force-fixed)
- **#47 (perihelion passages before flyby)**: `4.0` does not follow
  arithmetically from `PHAETHON_PERIOD_YEARS` and either flyby year
  under a simple period-division estimate. Needs real perihelion epoch
  data (e.g. JPL Horizons) to resolve properly — left as-is with an
  honest note rather than substituting an unverified number.

Predictions #5-25, #27-35, #38-45 are pure UTAC/Chimera/SOC model
outputs with no external literature to check against before the 2030
flyby; left as-is. #36 (Geminid ZHR) and #37 (stream age) were checked
against real published estimates and are consistent, though their
"UTAC model" attribution is unverifiable either way. See
`D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md` for the full
audit and `destiny_predictions.py` for per-prediction detail.

## [1.0.2] - 2026-09-15

### Fixed (documentation/data honesty, no numeric value change)
- **Ecosystem-wide Γ-circularity review — most severe finding of the
  review**: `GAMMA_PHAETHON=0.165` has NO cited physical derivation
  (unlike other GenesisAeon Γ constants, which at least rescale a real
  domain ratio) — its original code comment described it only as a
  "target: between Amazon (0.116) and AMOC (0.251)", i.e. chosen to
  occupy a plausible slot in the shared cross-package Γ ordering, not
  derived from any measured or modelled property of asteroid 3200
  Phaethon. This value was presented in `README.md`/
  `destiny_predictions.py` as DESTINY+ Prediction #1 (with an
  uncertainty band, framed as falsifiable against the 2029 flyby).
  Prediction #4 (`H*`) is directly computed from #1 and #3, so it is
  not independent of #1 either. Both are now marked
  `falsifiable=False` in `destiny_predictions.py` (the dataclass
  already had this field; it was never previously set). Prediction #3
  (`sigma=2.2`, cited as "Beta-to-Gamma bridge, P32") traces to
  `beta-clustering-utac`'s own claim that this constant "emerges from
  the beta distribution" — not independently re-verified in this pass;
  flagged in `FOLLOWUP_TICKETS.md` for a separate audit. Predictions
  #5-47 were not individually re-audited. Updated `constants.py`,
  `destiny_predictions.py`, `cli.py` (destiny-report now shows a
  Falsifiable column and includes `method`/`falsifiable` in JSON
  export), `README.md`, `.zenodo.json`. Added
  `test_non_independent_predictions_marked_unfalsifiable`. See
  `D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md` for the
  full finding.

### Fixed (CI/typing only, no behavior change)
- 3 pre-existing `mypy --strict` errors (missing `np.ndarray` generic
  type parameters in `system.py`; a `numpy` stub return-type mismatch
  in `frustrated_utac.py`'s RK4 integrator, fixed by pinning
  `np.linspace`'s dtype to `float64`) — not yet caught by CI (this
  morning's Ticket-5 push predates a numpy release that changed stub
  strictness) but reproduced locally with the current unpinned `numpy`
  release.

## [1.0.1] - 2026-09-15

### Fixed (test suite only, no behavior change)
- Removed `tests/test_preset.py`, `tests/test_validator.py`: unmodified
  copies of `diamond-setup`'s own test suite, exercising only
  `diamond_setup` internals, never `phaethon-chimera` code.
- `tests/test_cli.py` replaced with real tests against this package's
  own `cli.py` (`run`/`chimera-state`/`destiny-report`), previously a
  copy of diamond-setup's CLI tests with zero actual coverage of this
  package's own CLI. One of the new tests initially asserted `"5
  orbits" in result.output` without accounting for rich's ANSI
  highlighting splitting the digit into its own escape sequence —
  fixed by stripping ANSI codes before the substring check.

## [1.0.0] - 2026
### Added
- Initial v1.0.0 release as part of the GenesisAeon ecosystem-wide 1.0.0
  milestone.
- `PhaethonChimera` Diamond Interface (`run_cycle`, `get_crep_state`,
  `get_utac_state`, `get_phase_events`, `to_zenodo_record`).
- Frustrated UTAC ODE, Kuramoto chimera detector, SOC avalanche statistics,
  stochastic dust emission model, and 47 quantitative DESTINY+ predictions.
- Standardized release tooling: `.zenodo.json`, GitHub Actions release
  workflow (`.github/workflows/release.yml`), `RELEASE_GUIDE.md`,
  `CONTRIBUTING.md`, issue/PR templates.

### Changed
- Project metadata (`pyproject.toml`) normalized: version, license,
  authors, `requires-python`.
