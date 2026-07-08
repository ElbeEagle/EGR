"""Shared helpers for v2 theorem models."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable, List, Optional, Tuple

from ..schema import Fact, Provenance, Term
from ..state import InformationState


def theorem_fact(
    model_id: int,
    predicate: str,
    *arguments: Any,
    value: Any = None,
    evidence: Iterable[Fact] = (),
) -> Fact:
    evidence_ids = tuple(
        fact.fact_id for fact in evidence if fact.fact_id is not None
    )
    return Fact(
        predicate=predicate,
        arguments=tuple(arguments),
        value=value,
        provenance=Provenance.theorem(model_id, evidence_ids),
    )


def entities_of_type(state: InformationState, type_name: str) -> List[str]:
    return [
        name
        for name, symbol in state.symbols.items()
        if symbol.type_name == type_name
    ]


def parameter_fact(
    state: InformationState, entity: str, parameter_name: str
) -> Optional[Fact]:
    fact = state.get("ResolvedParameterOf", entity, parameter_name)
    if fact is None:
        fact = state.get("ParameterOf", entity, parameter_name)
    if fact is None:
        return None
    from ..resolution import StateExpressionResolver

    resolved = StateExpressionResolver(state).resolve(fact.value)
    return fact if resolved == fact.value else replace(fact, value=resolved)


def parameter_term(entity: str, parameter_name: str) -> Term:
    return Term("parameter", (entity, parameter_name))


def orientation_fact(state: InformationState, entity: str) -> Optional[Fact]:
    return state.get("AxisOrientationOf", entity)
