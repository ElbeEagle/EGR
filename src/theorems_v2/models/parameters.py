"""Parameter relation models 11-13."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from ..base import TheoremModelV2
from ..expressions import ConservativeSolver, add, div, equation, square, sub
from ..schema import Derivation, Fact, StateDelta, Term
from ..state import InformationState
from .common import entities_of_type, parameter_fact, parameter_term, theorem_fact


def _has_unresolved_symbol(value: Any) -> bool:
    if isinstance(value, Term):
        if value.operator in {"symbol", "parameter"}:
            return True
        return any(_has_unresolved_symbol(item) for item in value.arguments)
    if isinstance(value, (tuple, list)):
        return any(_has_unresolved_symbol(item) for item in value)
    return False

_PARAMETER_NAMES = {
    "a": ("semi_axis_a", "semi_axis_a_squared"),
    "b": ("semi_axis_b", "semi_axis_b_squared"),
    "c": ("focal_half_distance", "focal_half_distance_squared"),
}


def _squared_parameter(
    state: InformationState, entity: str, short_name: str
) -> Tuple[Optional[Any], Tuple[Fact, ...]]:
    plain_name, squared_name = _PARAMETER_NAMES[short_name]
    squared_fact = parameter_fact(state, entity, squared_name)
    if squared_fact is not None:
        return squared_fact.value, (squared_fact,)
    plain_fact = parameter_fact(state, entity, plain_name)
    if plain_fact is not None:
        return square(plain_fact.value), (plain_fact,)
    return None, ()


class ParameterRelationV2(TheoremModelV2):
    def __init__(self, model_id: int, curve_type: str):
        self.model_id = model_id
        self.curve_type = curve_type
        self.name = f"{curve_type}_Parameter_Relation_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for curve in entities_of_type(state, self.curve_type):
            values: Dict[str, Any] = {}
            evidence: List[Fact] = []
            symbolic_values: Dict[str, Any] = {}
            symbolic_evidence: Dict[str, Tuple[Fact, ...]] = {}
            for short_name in ("a", "b", "c"):
                value, facts = _squared_parameter(state, curve, short_name)
                if value is None:
                    continue
                key = f"{short_name}2"
                if _has_unresolved_symbol(value):
                    symbolic_values[key] = value
                    symbolic_evidence[key] = facts
                else:
                    values[key] = value
                    evidence.extend(facts)
            if not (len(values) >= 2 and len(symbolic_values) == 1):
                values.update(symbolic_values)
                for facts in symbolic_evidence.values():
                    evidence.extend(facts)
            if len(values) < 2:
                continue
            matches.append(
                {"G": curve, **values, "_evidence": tuple(evidence)}
            )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        curve = binding["G"]
        evidence = binding["_evidence"]
        a_term = parameter_term(curve, "semi_axis_a_squared")
        b_term = parameter_term(curve, "semi_axis_b_squared")
        c_term = parameter_term(curve, "focal_half_distance_squared")
        if self.curve_type == "Ellipse":
            relation = equation(a_term, add(b_term, c_term))
        else:
            relation = equation(c_term, add(a_term, b_term))

        facts: List[Fact] = [
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                relation,
                evidence=evidence,
            )
        ]
        values = {name: binding.get(name) for name in ("a2", "b2", "c2")}
        missing = [name for name, value in values.items() if value is None]
        if len(missing) == 1:
            target = missing[0]
            if self.curve_type == "Ellipse":
                if target == "a2":
                    value = solver.add(values["b2"], values["c2"])
                elif target == "b2":
                    value = solver.sub(values["a2"], values["c2"])
                else:
                    value = solver.sub(values["a2"], values["b2"])
            else:
                if target == "c2":
                    value = solver.add(values["a2"], values["b2"])
                elif target == "a2":
                    value = solver.sub(values["c2"], values["b2"])
                else:
                    value = solver.sub(values["c2"], values["a2"])
            short_name = target[0]
            plain_name, squared_name = _PARAMETER_NAMES[short_name]
            squared_predicate = (
                "ResolvedParameterOf"
                if state.get("ParameterOf", curve, squared_name) is not None
                else "ParameterOf"
            )
            plain_predicate = (
                "ResolvedParameterOf"
                if state.get("ParameterOf", curve, plain_name) is not None
                else "ParameterOf"
            )
            facts.extend(
                [
                    theorem_fact(
                        self.model_id,
                        squared_predicate,
                        curve,
                        squared_name,
                        value=value,
                        evidence=evidence,
                    ),
                    theorem_fact(
                        self.model_id,
                        plain_predicate,
                        curve,
                        plain_name,
                        value=solver.sqrt_positive(value),
                        evidence=evidence,
                    ),
                ]
            )
        return Derivation(
            StateDelta(add_facts=tuple(facts)), self.evidence(*evidence)
        )


class EccentricityFormulaV2(TheoremModelV2):
    model_id = 13
    name = "Eccentricity_Formula_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for curve_type in ("Ellipse", "Hyperbola"):
            for curve in entities_of_type(state, curve_type):
                ratio = state.get(
                    "ParameterRatioOf", curve, "b2_over_a2"
                )
                if ratio is not None:
                    matches.append(
                        {
                            "G": curve,
                            "axis_ratio": ratio.value,
                            "_evidence": (ratio,),
                        }
                    )
                    continue
                a = parameter_fact(state, curve, "semi_axis_a")
                c = parameter_fact(state, curve, "focal_half_distance")
                if a is not None and c is not None:
                    matches.append(
                        {
                            "G": curve,
                            "a": a.value,
                            "c": c.value,
                            "_evidence": (a, c),
                        }
                    )
                    continue
                a2 = parameter_fact(state, curve, "semi_axis_a_squared")
                c2 = parameter_fact(
                    state, curve, "focal_half_distance_squared"
                )
                if a2 is not None and c2 is not None:
                    matches.append(
                        {
                            "G": curve,
                            "a2": a2.value,
                            "c2": c2.value,
                            "_evidence": (a2, c2),
                        }
                    )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        curve = binding["G"]
        evidence = binding["_evidence"]
        facts: List[Fact] = []
        if "axis_ratio" in binding:
            eccentricity2 = solver.add(1, binding["axis_ratio"])
            eccentricity = solver.sqrt_positive(eccentricity2)
        elif "a" in binding:
            eccentricity = solver.div(binding["c"], binding["a"])
            eccentricity2 = solver.square(eccentricity)
        else:
            eccentricity2 = solver.div(binding["c2"], binding["a2"])
            eccentricity = solver.sqrt_positive(eccentricity2)
        if state.get("ParameterOf", curve, "eccentricity_squared") is None:
            facts.append(
                theorem_fact(
                    self.model_id,
                    "ParameterOf",
                    curve,
                    "eccentricity_squared",
                    value=eccentricity2,
                    evidence=evidence,
                )
            )
        if state.get("ParameterOf", curve, "eccentricity") is None:
            facts.append(
                theorem_fact(
                    self.model_id,
                    "ParameterOf",
                    curve,
                    "eccentricity",
                    value=eccentricity,
                    evidence=evidence,
                )
            )
        facts.append(
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                equation(
                    parameter_term(curve, "eccentricity"), eccentricity
                ),
                evidence=evidence,
            )
        )
        return Derivation(
            StateDelta(add_facts=tuple(facts)), self.evidence(*evidence)
        )


def parameter_models() -> List[TheoremModelV2]:
    return [
        ParameterRelationV2(11, "Ellipse"),
        ParameterRelationV2(12, "Hyperbola"),
        EccentricityFormulaV2(),
    ]
