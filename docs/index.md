# phaethon-chimera

**GenesisAeon Package 35** — Phaethon-Asteroid: Frustrierte Systeme & Chimera-Zustände

UTAC modelling of asteroid **3200 Phaethon** as a frustrated chimera system,
with **47 quantitative predictions** for the DESTINY+ JAXA mission (flyby 2029).

## Physical Model

The frustrated UTAC ODE:

```
dH/dt = r·H·(1-H/K)·tanh(σΓ) + A·cos(ω_Phaethon·t)
```

The periodic orbital forcing competes with the UTAC logistic attractor,
producing a **chimera state** — partial synchronisation between ordered
(Keplerian) and disordered (SOC) dynamics.

## CREP Position

| System    | Γ     | Domain            |
|-----------|-------|-------------------|
| Amazon    | 0.116 | Ecology           |
| **Phaethon** | **0.165** | **Asteroid dynamics** |
| AMOC      | 0.251 | Oceanography      |
| Neural    | 0.251 | Neuroscience      |

## Quickstart

```bash
uv sync
uv run pytest
uv run phaethon run --n-orbits 10
uv run phaethon destiny-report
```

## Key Predictions

| Prediction | Value | Unit |
|-----------|-------|------|
| Γ_phaethon | 0.165 ± 0.02 | — |
| Chimera R (perihelion) | 0.50 ± 0.10 | — |
| SOC τ exponent | 1.3 ± 0.1 | — |
| Emission probability/orbit | 0.23 ± 0.08 | — |
| Chimera transition altitude | 2.3 ± 0.4 | km |
| Geminid ZHR | 120 ± 20 | /hr |
