"""Concrete coordinate, line, and vector executors."""

from __future__ import annotations

from fractions import Fraction

from ..base import TheoremModelV2
from ..expressions import ConservativeSolver, equation, mul, number, sub
from ..schema import Derivation, StateDelta, Term
from ..state import InformationState
from ..structured_schema import LineEquation, Point2D, Vector2D
from .common import entities_of_type, theorem_fact


def _position(state, point):
    fact = state.get("PointPositionOf", point)
    if fact is None or not isinstance(fact.value, Point2D):
        return None
    return fact


class PointToLineDistanceV2(TheoremModelV2):
    model_id = 52
    name = "Point_To_Line_Distance_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedPointLineDistanceOf"):
            point, line = request.arguments
            position = _position(state, point)
            normal = state.get("LineNormalFormOf", line)
            if position is None or normal is None:
                continue
            if not isinstance(normal.value, LineEquation):
                continue
            matches.append(
                {
                    "point": point,
                    "line": line,
                    "position": position.value,
                    "normal": normal.value,
                    "target": request.value,
                    "_evidence": (request, position, normal),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        point = binding["position"]
        line = binding["normal"]
        numerator = solver.add(
            solver.mul(line.a, point.x),
            solver.mul(line.b, point.y),
            line.c,
        )
        denominator = solver.sqrt_positive(
            solver.add(solver.square(line.a), solver.square(line.b))
        )
        normalized = number(numerator)
        absolute = (
            abs(normalized)
            if isinstance(normalized, Fraction)
            else Term("abs", (numerator,))
        )
        distance = solver.div(absolute, denominator)
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "DistanceFormulaOf",
                binding["point"],
                binding["line"],
                value=distance,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                binding["target"],
                value=equation(binding["target"], distance),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class TwoPointsDistanceV2(TheoremModelV2):
    model_id = 53
    name = "Two_Points_Distance_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedDistanceOf"):
            first, second = request.arguments
            first_position = _position(state, first)
            second_position = _position(state, second)
            if first_position is None or second_position is None:
                continue
            matches.append(
                {
                    "first": first,
                    "second": second,
                    "first_position": first_position.value,
                    "second_position": second_position.value,
                    "target": request.value,
                    "_evidence": (request, first_position, second_position),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = binding["first_position"]
        second = binding["second_position"]
        squared = solver.add(
            solver.square(sub(second.x, first.x)),
            solver.square(sub(second.y, first.y)),
        )
        distance = solver.sqrt_positive(squared)
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "DistanceFormulaOf",
                binding["first"],
                binding["second"],
                value=distance,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                binding["target"],
                value=equation(binding["target"], distance),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class MidpointFormulaV2(TheoremModelV2):
    model_id = 54
    name = "Midpoint_Formula_V2"

    def match(self, state):
        matches = []
        for relation in state.find("MidPointOf"):
            first, second = relation.arguments
            first_position = _position(state, first)
            second_position = _position(state, second)
            if first_position is None or second_position is None:
                continue
            matches.append(
                {
                    "first": first,
                    "second": second,
                    "midpoint": relation.value,
                    "first_position": first_position.value,
                    "second_position": second_position.value,
                    "_evidence": (relation, first_position, second_position),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = binding["first_position"]
        second = binding["second_position"]
        midpoint = Point2D(
            solver.div(solver.add(first.x, second.x), 2),
            solver.div(solver.add(first.y, second.y), 2),
        )
        evidence = binding["_evidence"]
        facts = [
            theorem_fact(
                self.model_id,
                "MidpointFormulaOf",
                binding["first"],
                binding["second"],
                value=midpoint,
                evidence=evidence,
            )
        ]
        if state.get("PointPositionOf", binding["midpoint"]) is None:
            facts.append(
                theorem_fact(
                    self.model_id,
                    "PointPositionOf",
                    binding["midpoint"],
                    value=midpoint,
                    evidence=evidence,
                )
            )
        return Derivation(
            StateDelta(add_facts=tuple(facts)),
            self.evidence(*evidence),
        )


class SlopeFormulaV2(TheoremModelV2):
    model_id = 55
    name = "Slope_Formula_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedSlopeOf"):
            first, second = request.arguments
            first_position = _position(state, first)
            second_position = _position(state, second)
            if first_position is None or second_position is None:
                continue
            matches.append(
                {
                    "first": first,
                    "second": second,
                    "first_position": first_position.value,
                    "second_position": second_position.value,
                    "target": request.value,
                    "_evidence": (request, first_position, second_position),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = binding["first_position"]
        second = binding["second_position"]
        slope = solver.div(
            sub(second.y, first.y),
            sub(second.x, first.x),
        )
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "SlopeFormulaOf",
                binding["first"],
                binding["second"],
                value=slope,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                binding["target"],
                value=equation(binding["target"], slope),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class VectorDotProductV2(TheoremModelV2):
    model_id = 59
    name = "Vector_Dot_Product_Algebraic_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedDotProductOf"):
            a, b, c, d = request.arguments
            first = state.get("VectorOf", a, b)
            second = state.get("VectorOf", c, d)
            if (
                first is None
                or second is None
                or not isinstance(first.value, Vector2D)
                or not isinstance(second.value, Vector2D)
            ):
                continue
            matches.append(
                {
                    "first": (a, b),
                    "second": (c, d),
                    "first_vector": first.value,
                    "second_vector": second.value,
                    "target": request.value,
                    "_evidence": (request, first, second),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = binding["first_vector"]
        second = binding["second_vector"]
        dot_product = solver.add(
            solver.mul(first.x, second.x),
            solver.mul(first.y, second.y),
        )
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "DotProductFormulaOf",
                binding["first"],
                binding["second"],
                value=dot_product,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                binding["target"],
                value=equation(binding["target"], dot_product),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class VectorPerpendicularV2(TheoremModelV2):
    model_id = 61
    name = "Vector_Perpendicular_Condition_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedDotProductOf"):
            if request.value != 0:
                continue
            matches.append(
                {
                    "first": request.arguments[:2],
                    "second": request.arguments[2:],
                    "_evidence": (request,),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "PerpendicularVectorPair",
            binding["first"],
            binding["second"],
            value=True,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class VectorCollinearV2(TheoremModelV2):
    model_id = 62
    name = "Vector_Collinear_Condition_V2"

    def match(self, state):
        return [
            {
                "first": relation.arguments[:2],
                "second": relation.arguments[2:],
                "scale": relation.value,
                "_evidence": (relation,),
            }
            for relation in state.find("VectorScaleRelation")
        ]

    def derive(self, state, binding, solver):
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "CollinearVectorPair",
                binding["first"],
                binding["second"],
                value=True,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "VectorScaleOf",
                binding["first"],
                binding["second"],
                value=binding["scale"],
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class LinePointSlopeV2(TheoremModelV2):
    model_id = 72
    name = "Line_Point_Slope_Form_V2"

    def match(self, state):
        matches = []
        for line in entities_of_type(state, "Line"):
            slope = state.get("SlopeOf", line)
            if slope is None:
                continue
            for relation in state.find("PointOnCurve"):
                if len(relation.arguments) != 2 or relation.arguments[1] != line:
                    continue
                point = relation.arguments[0]
                position = _position(state, point)
                if position is None:
                    continue
                matches.append(
                    {
                        "line": line,
                        "point": point,
                        "slope": slope.value,
                        "position": position.value,
                        "_evidence": (slope, relation, position),
                    }
                )
        return matches

    def derive(self, state, binding, solver):
        point = binding["position"]
        slope = binding["slope"]
        normal = LineEquation(
            mul(-1, slope),
            1,
            sub(mul(slope, point.x), point.y),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "LinePointSlopeFormOf",
            binding["line"],
            value=normal,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class LineTwoPointV2(TheoremModelV2):
    model_id = 73
    name = "Line_Two_Point_Form_V2"

    def match(self, state):
        matches = []
        for line in entities_of_type(state, "Line"):
            linked = [
                relation
                for relation in state.find("PointOnCurve")
                if len(relation.arguments) == 2
                and relation.arguments[1] == line
                and _position(state, relation.arguments[0]) is not None
            ]
            if len(linked) != 2:
                continue
            first, second = (item.arguments[0] for item in linked)
            first_position = _position(state, first)
            second_position = _position(state, second)
            matches.append(
                {
                    "line": line,
                    "first": first,
                    "second": second,
                    "first_position": first_position.value,
                    "second_position": second_position.value,
                    "_evidence": (
                        linked[0],
                        linked[1],
                        first_position,
                        second_position,
                    ),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = binding["first_position"]
        second = binding["second_position"]
        normal = LineEquation(
            sub(first.y, second.y),
            sub(second.x, first.x),
            sub(mul(first.x, second.y), mul(second.x, first.y)),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "LineTwoPointFormOf",
            binding["line"],
            value=normal,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


def analytic_geometry_models():
    return [
        PointToLineDistanceV2(),
        TwoPointsDistanceV2(),
        MidpointFormulaV2(),
        SlopeFormulaV2(),
        VectorDotProductV2(),
        VectorPerpendicularV2(),
        VectorCollinearV2(),
        LinePointSlopeV2(),
        LineTwoPointV2(),
    ]
