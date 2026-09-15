"""Tests for phaethon-chimera's own CLI (src/phaethon_chimera/cli.py)."""

import re

from typer.testing import CliRunner

from phaethon_chimera.cli import app

runner = CliRunner()

_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _plain(output: str) -> str:
    """Strip rich's ANSI escape codes (which can split numeric substrings
    like "5 orbits" into separate highlighted tokens) before matching."""
    return _ANSI_ESCAPE.sub("", output)


def test_run_with_n_orbits():
    result = runner.invoke(app, ["run", "--n-orbits", "5"])
    assert result.exit_code == 0, result.output
    plain = _plain(result.output)
    assert "Phaethon-Chimera" in plain
    assert "5 orbits" in plain


def test_run_json():
    result = runner.invoke(app, ["run", "--json", "--n-orbits", "5"])
    assert result.exit_code == 0, result.output
    assert "gamma_phaethon" in result.output
    assert "utac_fixed_point" in result.output


def test_chimera_state():
    result = runner.invoke(app, ["chimera-state", "--n-orbits", "5"])
    assert result.exit_code == 0, result.output
    assert "Order parameter" in result.output


def test_destiny_report():
    result = runner.invoke(app, ["destiny-report"])
    assert result.exit_code == 0, result.output
    assert "DESTINY+" in result.output
