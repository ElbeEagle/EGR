"""Base contract for auditable theorem actions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from .expressions import ConservativeSolver
from .schema import Derivation, Fact
from .state import InformationState


class TheoremModelV2(ABC):
    model_id: int
    name: str

    @abstractmethod
    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        """Return all valid variable bindings for the current state."""

    @abstractmethod
    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        """Derive a delta without mutating ``state``."""

    def validate(
        self,
        state_before: InformationState,
        state_after: InformationState,
        derivation: Derivation,
        solver: ConservativeSolver,
    ) -> Tuple[str, ...]:
        errors = []
        for expected in derivation.delta.add_facts:
            actual = state_after.get(expected.predicate, *expected.arguments)
            if actual is None:
                errors.append(f"missing postcondition: {expected.slot_key}")
            elif not solver.equivalent(actual.value, expected.value):
                errors.append(f"invalid postcondition: {expected.slot_key}")
        return tuple(errors)

    @staticmethod
    def evidence(*facts: Fact) -> Tuple[str, ...]:
        return tuple(fact.fact_id for fact in facts if fact.fact_id is not None)
