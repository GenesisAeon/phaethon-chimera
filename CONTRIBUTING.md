# Contributing

Thanks for your interest in contributing to this GenesisAeon ecosystem
package!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
   (or `.venv\Scripts\activate` on Windows).
3. Install in editable mode with dev dependencies: `pip install -e ".[dev]"`
   (or `uv sync`).
4. Run the test suite: `pytest` (or `uv run pytest`).

## Code style

- Format and lint with `ruff format` / `ruff check`.
- Type-check with `mypy` (this package uses `strict = true`).
- Keep functions documented with concise docstrings.

## Diamond Interface

This package implements the GenesisAeon Diamond Interface
(`run_cycle`, `get_crep_state`, `get_utac_state`, `get_phase_events`,
`to_zenodo_record`) on `PhaethonChimera`. Any change to these methods'
signatures or return shapes is a **breaking change** and requires a MAJOR
version bump (see `RELEASE_GUIDE.md`).

## Pull requests

- One logical change per PR.
- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` under an `## [Unreleased]` section.
- Fill out the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).

## Reporting issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` — they help us
triage bug reports vs. feature requests quickly.

## Scientific claims

This package makes falsifiable, quantitative predictions for the
DESTINY+ mission (flyby 2029). If your contribution touches the physical
model, CREP `Γ` value, or any of the 47 predictions, please cite the
source and clearly mark speculative vs. validated claims.
