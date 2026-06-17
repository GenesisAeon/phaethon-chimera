# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
