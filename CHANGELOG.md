# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
