"""Auditable theorem system v2.

Legacy theorem code remains under ``src.theorems``.  Importing this package is
an explicit opt-in to the typed v2 information space and applicator.
"""

from .applicator import ApplicatorV2
from .expressions import ConservativeSolver
from .library import TheoremLibraryV2
from .schema import (
    ApplicationResult,
    ApplicationStatus,
    AxisLine,
    Fact,
    LineThroughOrigin,
    PolynomialEquation,
    Provenance,
    StandardConicForm,
    StateDelta,
    SymbolRef,
    Term,
)
from .state import InformationState

__all__ = [
    "ApplicationResult",
    "ApplicationStatus",
    "ApplicatorV2",
    "AxisLine",
    "ConservativeSolver",
    "Fact",
    "InformationState",
    "LineThroughOrigin",
    "PolynomialEquation",
    "Provenance",
    "StandardConicForm",
    "StateDelta",
    "SymbolRef",
    "Term",
    "TheoremLibraryV2",
]
