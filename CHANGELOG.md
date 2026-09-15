# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
