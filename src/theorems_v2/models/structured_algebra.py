"""Concrete algebra executors backed by explicit substitution state."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..base import TheoremModelV2
from ..expressions import (
    ConservativeSolver,
    equation,
    is_zero,
    mul,
    neg,
    sub,
)
from ..schema import Derivation, PolynomialEquation, StateDelta, Term
from ..state import InformationState
from ..structured_schema import LineEquation, QuadraticPolynomial
from .common import theorem_fact


def _quadratic_matches(state: InformationState) -> List[Dict[str, Any]]:
    matches = []
    for fact in state.find("QuadraticPolynomialOf"):
        value = fact.value
        if not isinstance(value, QuadraticPolynomial) or is_zero(value.a):
            continue
        matches.append(
            {
                "line": fact.arguments[0],
                "curve": fact.arguments[1],
                "quadratic": value,
                "_evidence": (fact,),
            }
        )
    return matches


class VietaTheoremV2(TheoremModelV2):
    model_id = 41
    name = "Vieta_Theorem_V2"

    def match(self, state):
        return _quadratic_matches(state)

    def derive(self, state, binding, solver):
        quadratic = binding["quadratic"]
        evidence = binding["_evidence"]
        root_sum = solver.div(neg(quadratic.b), quadratic.a)
        root_product = solver.div(quadratic.c, quadratic.a)
        facts = (
            theorem_fact(
                self.model_id,
                "RootSumOf",
                binding["line"],
                binding["curve"],
                value=root_sum,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "RootProductOf",
                binding["line"],
                binding["curve"],
                value=root_product,
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class VietaSumV2(VietaTheoremV2):
    model_id = 42
    name = "Vieta_Theorem_Sum_V2"

    def derive(self, state, binding, solver):
        quadratic = binding["quadratic"]
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "RootSumOf",
            binding["line"],
            binding["curve"],
            value=solver.div(neg(quadratic.b), quadratic.a),
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class VietaProductV2(VietaTheoremV2):
    model_id = 43
    name = "Vieta_Theorem_Product_V2"

    def derive(self, state, binding, solver):
        quadratic = binding["quadratic"]
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "RootProductOf",
            binding["line"],
            binding["curve"],
            value=solver.div(quadratic.c, quadratic.a),
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class DiscriminantV2(TheoremModelV2):
    model_id = 65
    name = "Discriminant_Delta_V2"

    def match(self, state):
        return _quadratic_matches(state)

    def derive(self, state, binding, solver):
        quadratic = binding["quadratic"]
        evidence = binding["_evidence"]
        discriminant = sub(
            solver.square(quadratic.b),
            mul(4, quadratic.a, quadratic.c),
        )
        fact = theorem_fact(
            self.model_id,
            "DiscriminantOf",
            binding["line"],
            binding["curve"],
            value=discriminant,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class _DiscriminantConditionV2(TheoremModelV2):
    intersection_count: int
    relation: str

    def match(self, state):
        matches = []
        for discriminant in state.find("DiscriminantOf"):
            line, curve = discriminant.arguments
            count = state.get("IntersectionCountOf", line, curve)
            if count is None:
                count = state.get("IntersectionCountOf", curve, line)
            if count is None or count.value != self.intersection_count:
                continue
            matches.append(
                {
                    "line": line,
                    "curve": curve,
                    "delta": discriminant.value,
                    "_evidence": (discriminant, count),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        evidence = binding["_evidence"]
        if self.relation == "eq":
            condition = equation(binding["delta"], 0)
        else:
            condition = Term("gt", (binding["delta"], 0))
        facts = (
            theorem_fact(
                self.model_id,
                "DiscriminantConditionOf",
                binding["line"],
                binding["curve"],
                value=condition,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "OrderConstraint",
                binding["line"],
                binding["curve"],
                "discriminant",
                value=condition,
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class DiscriminantTangentV2(_DiscriminantConditionV2):
    model_id = 66
    name = "Discriminant_Tangent_Condition_V2"
    intersection_count = 1
    relation = "eq"


class DiscriminantIntersectV2(_DiscriminantConditionV2):
    model_id = 67
    name = "Discriminant_Intersect_Condition_V2"
    intersection_count = 2
    relation = "gt"


class SubstituteLineIntoConicV2(TheoremModelV2):
    model_id = 78
    name = "Substitution_x_equals_my_plus_n_V2"

    CONIC_TYPES = {"Ellipse", "Hyperbola", "Parabola", "Circle"}

    def match(self, state):
        matches = []
        for intersection in state.find("IntersectionOf"):
            if len(intersection.arguments) != 2:
                continue
            first, second = intersection.arguments
            line, curve = self._line_and_curve(state, first, second)
            if line is None:
                continue
            roots = intersection.value
            if not isinstance(roots, tuple) or not roots:
                continue
            line_fact = state.get("LineNormalFormOf", line)
            curve_fact = state.get("ExpressionPolynomial", curve)
            if (
                line_fact is None
                or not isinstance(line_fact.value, LineEquation)
                or curve_fact is None
                or not isinstance(curve_fact.value, PolynomialEquation)
            ):
                continue
            matches.append(
                {
                    "line": line,
                    "curve": curve,
                    "line_form": line_fact.value,
                    "curve_form": curve_fact.value,
                    "points": roots,
                    "_evidence": (intersection, line_fact, curve_fact),
                }
            )
        return matches

    @classmethod
    def _line_and_curve(cls, state, first, second) -> Tuple[Any, Any]:
        if state.has_type(first, "Line") and any(
            state.has_type(second, curve_type)
            for curve_type in cls.CONIC_TYPES
        ):
            return first, second
        if state.has_type(second, "Line") and any(
            state.has_type(first, curve_type)
            for curve_type in cls.CONIC_TYPES
        ):
            return second, first
        return None, None

    def derive(self, state, binding, solver):
        line = binding["line_form"]
        conic = binding["curve_form"]
        if not is_zero(line.b):
            variable = "x"
            slope = solver.div(neg(line.a), line.b)
            intercept = solver.div(neg(line.c), line.b)
            qa = solver.add(
                conic.x2,
                solver.mul(conic.xy, slope),
                solver.mul(conic.y2, solver.square(slope)),
            )
            qb = solver.add(
                solver.mul(conic.xy, intercept),
                solver.mul(2, conic.y2, slope, intercept),
                conic.x,
                solver.mul(conic.y, slope),
            )
            qc = solver.add(
                solver.mul(conic.y2, solver.square(intercept)),
                solver.mul(conic.y, intercept),
                conic.constant,
            )
            substitution = equation(
                Term("symbol", ("y",)),
                solver.add(
                    solver.mul(slope, Term("symbol", ("x",))),
                    intercept,
                ),
            )
        elif not is_zero(line.a):
            variable = "y"
            intercept = solver.div(neg(line.c), line.a)
            qa = conic.y2
            qb = solver.add(solver.mul(conic.xy, intercept), conic.y)
            qc = solver.add(
                solver.mul(conic.x2, solver.square(intercept)),
                solver.mul(conic.x, intercept),
                conic.constant,
            )
            substitution = equation(Term("symbol", ("x",)), intercept)
        else:
            raise ValueError("line equation has zero normal")

        roots = tuple(
            Term("coordinate", (point, variable))
            for point in binding["points"]
        )
        quadratic = QuadraticPolynomial(variable, qa, qb, qc, roots)
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "QuadraticPolynomialOf",
                binding["line"],
                binding["curve"],
                value=quadratic,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "RootSetOf",
                binding["line"],
                binding["curve"],
                value=roots,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "SubstitutionOf",
                binding["line"],
                binding["curve"],
                value=substitution,
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


def algebra_models():
    return [
        VietaTheoremV2(),
        VietaSumV2(),
        VietaProductV2(),
        DiscriminantV2(),
        DiscriminantTangentV2(),
        DiscriminantIntersectV2(),
        SubstituteLineIntoConicV2(),
    ]
