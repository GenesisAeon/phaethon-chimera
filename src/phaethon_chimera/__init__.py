"""
phaethon-chimera — GenesisAeon Package 35.

Phaethon-Asteroid: Frustrierte Systeme & Chimera-Zustände.

47 quantitative predictions for DESTINY+ mission (JAXA, flyby 2029).
CREP coupling: Γ_phaethon ≈ 0.165 (between Amazon 0.116 and AMOC 0.251).

DOI: 10.5281/zenodo.17472834
"""

from phaethon_chimera.chimera_detector import ChimeraDetector
from phaethon_chimera.constants import GAMMA_PHAETHON, PHI_CUBEROOT
from phaethon_chimera.destiny_predictions import DESTINY_PREDICTIONS
from phaethon_chimera.dust_emission import DustEmissionModel
from phaethon_chimera.frustrated_utac import FrustratedUTAC
from phaethon_chimera.geminid_model import GeminidModel
from phaethon_chimera.orbital import PhaethonOrbit
from phaethon_chimera.soc_phaethon import SOCPhaethon
from phaethon_chimera.system import PhaethonChimera

__version__ = "1.0.0"
__package_number__ = 35
__all__ = [
    "PhaethonChimera",
    "FrustratedUTAC",
    "ChimeraDetector",
    "PhaethonOrbit",
    "DustEmissionModel",
    "SOCPhaethon",
    "GeminidModel",
    "DESTINY_PREDICTIONS",
    "GAMMA_PHAETHON",
    "PHI_CUBEROOT",
]
