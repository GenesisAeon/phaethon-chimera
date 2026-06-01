"""CLI for phaethon-chimera Package 35."""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Phaethon-Chimera P35 — Frustrated UTAC & DESTINY+ predictions")
console = Console()


@app.command()
def run(
    n_orbits: int = typer.Option(10, "--n-orbits", "-n", help="Number of orbits to simulate"),
    destiny_predictions: bool = typer.Option(
        False, "--destiny-predictions", help="Print all 47 predictions"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Run full Phaethon-Chimera simulation cycle."""
    from phaethon_chimera.system import PhaethonChimera

    pc = PhaethonChimera(n_orbits=n_orbits)
    results = pc.run_cycle()

    if json_output:
        # Flatten for JSON serialisation
        out = {
            "gamma_phaethon": results["gamma_phaethon"],
            "utac_fixed_point": results["utac_fixed_point"],
            "frustration_ratio": results["frustration_ratio"],
            "chimera_R_mean": results["chimera"]["R_mean"],
            "chimera_R_perihelion": results["chimera"]["R_perihelion"],
            "soc_tau": results["soc"].get("tau_hat", None),
            "hurst": results["soc"]["hurst_exponent"],
            "emission_probability": results["dust"]["empirical_probability"],
            "geminid_zhr": results["geminid"]["predicted_zhr"],
            "n_destiny_predictions": results["n_destiny_predictions"],
        }
        console.print(json.dumps(out, indent=2))
        return

    console.print(f"[bold cyan]Phaethon-Chimera P35[/] — {n_orbits} orbits simulated")
    table = Table(title="Phaethon-Chimera Simulation Results", show_header=True)
    table.add_column("Quantity", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Target", style="yellow")

    table.add_row("Γ_phaethon", f"{results['gamma_phaethon']:.3f}", "0.165 ± 0.020")
    table.add_row("UTAC fixed point H*", f"{results['utac_fixed_point']:.4f}", "0.286 ± 0.030")
    table.add_row("Frustration ratio ω_p/ω_0", f"{results['frustration_ratio']:.3f}", "≈ 1.0")
    table.add_row("Chimera R (mean)", f"{results['chimera']['R_mean']:.3f}", "-")
    table.add_row(
        "Chimera R (perihelion)",
        f"{results['chimera']['R_perihelion']:.3f}",
        "0.50 ± 0.10",
    )
    table.add_row("Chimera state", str(results["chimera"]["classification"]), "chimera")
    table.add_row("SOC τ exponent", f"{results['soc'].get('tau_hat', 'N/A')}", "1.3 ± 0.1")
    table.add_row("Hurst exponent", f"{results['soc']['hurst_exponent']:.3f}", "> 0.5 (SOC)")
    table.add_row(
        "Emission probability",
        f"{results['dust']['empirical_probability']:.3f}",
        "0.23 ± 0.08",
    )
    table.add_row(
        "Geminid ZHR prediction", f"{results['geminid']['predicted_zhr']:.1f}", "120 ± 20"
    )
    table.add_row("Φ^(1/3) scaling", f"{results['phi_cuberoot']:.5f}", "1.17480")
    table.add_row("DESTINY+ predictions", str(results["n_destiny_predictions"]), "47")
    console.print(table)

    if destiny_predictions:
        _print_destiny_table()


@app.command("chimera-state")
def chimera_state(
    n_orbits: int = typer.Option(10, "--n-orbits"),
    threshold: float = typer.Option(
        0.5, "--threshold", help="R threshold for chimera classification"
    ),
) -> None:
    """Detect and report chimera state from simulation."""
    from phaethon_chimera.system import PhaethonChimera

    pc = PhaethonChimera(n_orbits=n_orbits)
    pc.run_cycle()
    R = pc.chimera_order_parameter()
    classification = "chimera" if 0.15 < R < 0.85 else ("ordered" if R >= 0.85 else "disordered")
    console.print(f"Order parameter R = [bold]{R:.4f}[/]  → [cyan]{classification}[/]")
    console.print(f"(threshold for chimera: 0.15 < R < 0.85, current threshold ref = {threshold})")


@app.command("destiny-report")
def destiny_report(
    fmt: str = typer.Option("table", "--format", help="Output format: table | json | zenodo"),
) -> None:
    """Print all 47 DESTINY+ mission predictions."""
    _print_destiny_table(fmt=fmt)


def _print_destiny_table(fmt: str = "table") -> None:
    from phaethon_chimera.destiny_predictions import DESTINY_PREDICTIONS, prediction_summary

    if fmt == "json":
        out = [
            {
                "id": p.id,
                "category": p.category,
                "quantity": p.quantity,
                "value": p.value,
                "uncertainty": p.uncertainty,
                "unit": p.unit,
            }
            for p in DESTINY_PREDICTIONS
        ]
        console.print(json.dumps(out, indent=2))
        return

    table = Table(title=f"DESTINY+ Predictions (n={len(DESTINY_PREDICTIONS)})")
    table.add_column("#", style="dim")
    table.add_column("Category", style="magenta")
    table.add_column("Quantity", style="cyan")
    table.add_column("Value ± σ", style="green")
    table.add_column("Unit", style="yellow")

    for p in DESTINY_PREDICTIONS:
        table.add_row(str(p.id), p.category, p.quantity, f"{p.value} ± {p.uncertainty}", p.unit)

    console.print(table)

    summary = prediction_summary()
    console.print("\n[bold]By category:[/]", summary)


if __name__ == "__main__":
    app()
