# phaethon-chimera

[![GenesisAeon Package](https://img.shields.io/badge/GenesisAeon-Package%2035-blueviolet)](https://doi.org/10.5281/zenodo.17472834)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17472834.svg)](https://doi.org/10.5281/zenodo.17472834)
[![Whitepaper](https://img.shields.io/badge/Whitepaper-Zenodo-blue)](https://doi.org/10.5281/zenodo.19645351)
[![DESTINY+](https://img.shields.io/badge/DESTINY%2B-Flyby%202029-orange)](https://www.isas.jaxa.jp/missions/spacecraft/destiny_plus/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**GenesisAeon Package 35** — Phaethon-Asteroid: Frustrierte Systeme & Chimera-Zustände

UTAC-Modellierung von **3200 Phaethon** als frustriertes Chimera-System.
**47 quantitative Vorhersagen** für die DESTINY+ JAXA-Mission (Flyby 2029).

---

## Wissenschaftlicher Hintergrund

3200 Phaethon ist ein anomales Objekt — gleichzeitig Asteroid (deterministisch, Keplerbahn) und
kometenähnlich (stochastischer Staubausstoß bei Perihel, Quelle der Geminiden).

Diese **Frustration** im UTAC-Kontext entsteht durch:

```
dH/dt = r·H·(1-H/K)·tanh(σΓ) + A·cos(ω_Phaethon·t)
```

Der periodische Term (Bahnfrequenz) konkurriert mit dem UTAC-Logistik-Term → **Chimera-Zustand**:
Teil des Systems ist geordnet (Keplerbahn), Teil ist SOC (stochastische Aktivität bei Perihel).

### CREP-Einordnung

| System        | Γ         | Domäne            |
|---------------|-----------|-------------------|
| Amazon        | 0.116     | Ökologie          |
| **Phaethon**  | **0.165** | **Asteroidendynamik** |
| AMOC          | 0.251     | Ozeanographie     |
| Neural        | 0.251     | Neurowissenschaft |

Phaethon liegt **zwischen Amazon und AMOC** — im mittleren kritischen Bereich.

---

## Quickstart

```bash
uv sync
uv run pytest

# CLI
uv run phaethon run --n-orbits 10
uv run phaethon run --n-orbits 10 --destiny-predictions
uv run phaethon chimera-state
uv run phaethon destiny-report --format table
```

## Kernklassen

| Klasse | Funktion |
|--------|----------|
| `PhaethonChimera` | Diamond-Interface (run_cycle, CREP, UTAC, phase events) |
| `FrustratedUTAC` | Frustrierte UTAC-ODE mit periodischem Forcing |
| `ChimeraDetector` | Kuramoto-Ordnungsparameter R ∈ [0,1] |
| `PhaethonOrbit` | Keplersche Bahn (JPL Horizons) |
| `DustEmissionModel` | Stochastische Staubemission (Bernoulli + SOC) |
| `SOCPhaethon` | Power-Law-Fit, Hurst-Exponent |
| `GeminidModel` | Geminiden-Meteoritenstrom aus UTAC |
| `DESTINY_PREDICTIONS` | Alle 47 falsifizierbaren Vorhersagen |

## 47 DESTINY+ Vorhersagen (Auswahl)

| # | Größe | Wert ± σ | Einheit |
|---|-------|----------|---------|
| 1 | Γ_phaethon | 0.165 ± 0.02 | — |
| 6 | Chimera R (Perihel) | 0.50 ± 0.10 | — |
| 7 | Chimera-Übergangsaltitude | 2.3 ± 0.4 | km |
| 11 | Emissionswahrscheinlichkeit/Orbit | 0.23 ± 0.08 | — |
| 16 | SOC τ-Exponent | 1.3 ± 0.1 | — |
| 36 | Geminid ZHR | 120 ± 20 | /hr |
| 46 | DESTINY+ Flyby | 2029 ± 1 | Jahr |

Alle Vorhersagen sind **vor** dem DESTINY+ Flyby (2029) publiziert → falsifizierbar.

## Repository-Struktur

```
src/phaethon_chimera/
├── system.py              # PhaethonChimera — Diamond interface
├── orbital.py             # Keplersche Bahn (JPL Horizons)
├── frustrated_utac.py     # Frustrierte UTAC-ODE + RK4
├── chimera_detector.py    # Kuramoto-Ordnungsparameter
├── dust_emission.py       # Stochastische Staubemission + SOC
├── soc_phaethon.py        # Power-Law-Fit, Hurst-Exponent
├── destiny_predictions.py # 47 DESTINY+-Vorhersagen
├── geminid_model.py       # Geminiden-Meteoritenstrom
├── benchmark.py           # Benchmark-Targets
├── cli.py                 # phaethon CLI
└── constants.py           # Physikalische Konstanten

data/
├── phaethon_orbital_elements.yaml
├── destiny_plus_targets.yaml
└── ztf_photometry_summary.yaml
```

## Benchmark-Targets

```python
BENCHMARK_TARGETS = {
    "gamma_phaethon":        (0.165, 0.020),
    "chimera_R_perihelion":  (0.500, 0.100),
    "soc_tau_exponent":      (1.300, 0.100),
    "emission_probability":  (0.230, 0.080),
    "geminid_zhr":           (120.0, 30.0),
    "n_destiny_predictions": (47.0,  0.0),
    "phi_cuberoot":          (1.17480502, 0.00001),
}
```

## GENESIS-OS Registrierung

```python
PACKAGE_REGISTRY[35] = {
    "name": "phaethon-chimera",
    "class": PhaethonChimera,
    "domain": "asteroid-dynamics",
    "scale": "solar-system",
    "zenodo": "10.5281/zenodo.17472834",
    "reference": "DESTINY+ 2024+"
}
```

## Zitation

```bibtex
@software{roemer_phaethon_chimera_2026,
  author    = {Römer, Johann},
  title     = {phaethon-chimera: Frustrated UTAC Systems \& Chimera States},
  version   = {1.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.17472834},
  year      = {2026},
  note      = {GenesisAeon Package 35, DESTINY+ predictions}
}
```

## Verbindung zum GenesisAeon-Ökosystem

- **P31** (vrig-cosmological): v_RIG ≈ 1352 km/s normiert auf Phaethon-Orbitalgeschwindigkeit
- **P32** (beta-clustering): β-Cluster — Phaethon im astrophysikalischen Cluster (β ≈ 0.65–1.20)
- **P36** (sa-sv-duality): S_A/S_V-Entropiedualität der Phaethon-Trajektorie
- **P38** (phi-scaling): Φ^(1/3) ≈ 1.174 Skalierung zwischen Orbitaldynamik-Domänen

**Zeitkritisch: DESTINY+ Flyby 2029 — alle Vorhersagen sind vor dem Flyby publiziert.**

---

*Johann Römer · MOR Research Collective · Mai 2026*
