"""Definition models 0-2 for theorem v2."""

from __future__ import annotations

from typing import Any, Dict, List

from ..base import TheoremModelV2
from ..expressions import ConservativeSolver, add, equation, mul, sub
from ..schema import Derivation, StateDelta, Term
from ..state import InformationState
from .common import entities_of_type, parameter_fact, theorem_fact


class _TwoFocusDefinition(TheoremModelV2):
    curve_type: str
    use_absolute_difference: bool

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for curve in entities_of_type(state, self.curve_type):
            foci = state.find("FocusOf", curve)
            axis = parameter_fact(state, curve, "semi_axis_a")
            if len(foci) != 2 or axis is None:
                continue
            points = [
                fact
                for fact in state.find("PointOnCurve")
                if len(fact.arguments) == 2 and fact.arguments[1] == curve
            ]
            for point_fact in points:
                matches.append(
                    {
                        "G": curve,
                        "P": point_fact.arguments[0],
                        "F1": foci[0].arguments[1],
                        "F2": foci[1].arguments[1],
                        "a": axis.value,
                        "_evidence": (point_fact, foci[0], foci[1], axis),
                    }
                )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        distance_1 = Term("distance", (binding["P"], binding["F1"]))
        distance_2 = Term("distance", (binding["P"], binding["F2"]))
        if self.use_absolute_difference:
            left = Term("abs", (sub(distance_1, distance_2),))
        else:
            left = add(distance_1, distance_2)
        relation = equation(left, mul(2, binding["a"]))
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "DefinitionRelation",
            binding["G"],
            binding["P"],
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class EllipseDefinitionV2(_TwoFocusDefinition):
    model_id = 0
    name = "Ellipse_Definition_V2"
    curve_type = "Ellipse"
    use_absolute_difference = False


class HyperbolaDefinitionV2(_TwoFocusDefinition):
    model_id = 1
    name = "Hyperbola_Definition_V2"
    curve_type = "Hyperbola"
    use_absolute_difference = True


class ParabolaDefinitionV2(TheoremModelV2):
    model_id = 2
    name = "Parabola_Definition_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for curve in entities_of_type(state, "Parabola"):
            foci = state.find("FocusOf", curve)
            directrices = state.find("DirectrixOf", curve)
            if len(foci) != 1 or len(directrices) != 1:
                continue
            points = [
                fact
                for fact in state.find("PointOnCurve")
                if len(fact.arguments) == 2 and fact.arguments[1] == curve
            ]
            for point_fact in points:
                matches.append(
                    {
                        "G": curve,
                        "P": point_fact.arguments[0],
                        "F": foci[0].arguments[1],
                        "L": directrices[0].arguments[1],
                        "_evidence": (
                            point_fact,
                            foci[0],
                            directrices[0],
                        ),
                    }
                )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        relation = equation(
            Term("distance", (binding["P"], binding["F"])),
            Term("distance_to_line", (binding["P"], binding["L"])),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "DefinitionRelation",
            binding["G"],
            binding["P"],
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))
