# DESTINY+ Predictions

47 quantitative predictions for the DESTINY+ JAXA mission
(flyby of 3200 Phaethon, expected 2029).

All predictions are published **before** the flyby and are therefore
falsifiable against DESTINY+ instrument data.

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| CREP | 5 | UTAC/CREP parameters |
| Chimera | 5 | Chimera state observables |
| Dust | 5 | Dust emission statistics |
| SOC | 5 | Power-law / Hurst exponent |
| Thermal | 5 | Surface temperature |
| Morphology | 5 | Shape and regolith |
| Spectral | 5 | Spectroscopy |
| Geminid | 5 | Meteor shower model |
| InfoGeo | 5 | Information-geometric |
| Mission | 2 | Timeline |

## Top-5 Critical Predictions

| # | Quantity | Value ± σ | Unit | Test |
|---|---------|----------|------|------|
| 11 | Emission probability/orbit | 0.23 ± 0.08 | prob. | DESTINY+ TCAP dust counter |
| 6 | Chimera R (perihelion) | 0.50 ± 0.10 | — | Dust flux time series |
| 16 | SOC τ exponent | 1.3 ± 0.1 | — | Resolved grain avalanches |
| 7 | Chimera transition altitude | 2.3 ± 0.4 | km | Altitude-resolved imaging |
| 12 | Peak dust flux Γ | 0.68 ± 0.05 | norm. | SMEI photometry |

## Falsification Criterion

A prediction is **falsified** if the DESTINY+ measured value deviates
from the predicted value by more than 3σ.

## Python API

```python
from phaethon_chimera import DESTINY_PREDICTIONS

for p in DESTINY_PREDICTIONS:
    print(f"#{p.id} {p.quantity}: {p.value} ± {p.uncertainty} {p.unit}")
```
