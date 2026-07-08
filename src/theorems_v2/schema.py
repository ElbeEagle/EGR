"""Core data structures for the v2 theorem system.

This package is intentionally separate from ``src.theorems``.  The old
runtime remains available while v2 develops a typed, auditable transition
contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import InformationState


@dataclass(frozen=True, order=True)
class SymbolRef:
    name: str
    type_name: str


@dataclass(frozen=True)
class Term:
    operator: str
    arguments: Tuple[Any, ...]

    def __str__(self) -> str:
        args = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.operator}({args})"


@dataclass(frozen=True)
class Provenance:
    source_kind: str
    source_id: str
    evidence_fact_ids: Tuple[str, ...] = ()

    @classmethod
    def given(cls, source_id: str = "input") -> "Provenance":
        return cls("given", source_id)

    @classmethod
    def theorem(
        cls, model_id: int, evidence_fact_ids: Tuple[str, ...] = ()
    ) -> "Provenance":
        return cls("theorem", str(model_id), evidence_fact_ids)


@dataclass(frozen=True)
class Fact:
    predicate: str
    arguments: Tuple[Any, ...]
    value: Any = None
    provenance: Provenance = field(default_factory=Provenance.given)
    raw_expression: Optional[str] = None
    fact_id: Optional[str] = None

    @property
    def slot_key(self) -> Tuple[Any, ...]:
        """Return the identity of a fact, excluding its value and provenance."""
        return (self.predicate, self.arguments)


@dataclass(frozen=True)
class PolynomialEquation:
    """Normalized ``sum(coeff * monomial) = 0`` in x and y.

    Producing coefficients is algebraic normalization, not a conic theorem.
    Conic models are responsible for interpreting these coefficients.
    """

    x2: Any = 0
    xy: Any = 0
    y2: Any = 0
    x: Any = 0
    y: Any = 0
    constant: Any = 0


@dataclass(frozen=True)
class StandardConicForm:
    curve_type: str
    orientation: str
    a2: Any = None
    b2: Any = None
    two_p: Any = None
    focus_offset: Any = None


@dataclass(frozen=True)
class LineThroughOrigin:
    dependent_axis: str
    slope: Any


@dataclass(frozen=True)
class AxisLine:
    axis: str
    value: Any


@dataclass(frozen=True)
class StateDelta:
    add_symbols: Tuple[SymbolRef, ...] = ()
    add_facts: Tuple[Fact, ...] = ()


class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    ALREADY_KNOWN = "ALREADY_KNOWN"
    NO_MATCH = "NO_MATCH"
    AMBIGUOUS_BINDING = "AMBIGUOUS_BINDING"
    PRECONDITION_UNRESOLVED = "PRECONDITION_UNRESOLVED"
    SOLVER_UNRESOLVED = "SOLVER_UNRESOLVED"
    CONFLICT = "CONFLICT"
    POSTCONDITION_FAILED = "POSTCONDITION_FAILED"
    EXCEPTION = "EXCEPTION"


@dataclass(frozen=True)
class Derivation:
    delta: StateDelta
    evidence_fact_ids: Tuple[str, ...] = ()


@dataclass(frozen=True)
class SupportApplication:
    """A concrete helper action committed inside one macro application.

    The requested theorem remains the externally visible selector action.
    Support applications make omitted deterministic/theorem steps auditable
    without rewriting the observed natural-language theorem sequence.
    """

    model_id: int
    status: ApplicationStatus
    binding: Mapping[str, Any]
    delta: StateDelta = field(default_factory=StateDelta)
    evidence_fact_ids: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ApplicationResult:
    model_id: int
    status: ApplicationStatus
    binding: Mapping[str, Any]
    delta: StateDelta = field(default_factory=StateDelta)
    evidence_fact_ids: Tuple[str, ...] = ()
    postcondition_errors: Tuple[str, ...] = ()
    conflicts: Tuple[str, ...] = ()
    state_after: Optional["InformationState"] = None
    support_applications: Tuple[SupportApplication, ...] = ()
