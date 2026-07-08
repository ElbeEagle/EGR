"""Point-difference, chord, triangle, and area executors."""

from __future__ import annotations

from fractions import Fraction

from ..base import TheoremModelV2
from ..expressions import equation, is_zero, mul, neg, sub
from ..schema import Derivation, PolynomialEquation, StateDelta, Term
from ..structured_schema import LineEquation, Point2D, QuadraticPolynomial
from .common import theorem_fact


def _coordinate(point, axis):
    return Term("coordinate", (point, axis))


def _distance(first, second):
    return Term("distance", (first, second))


def _point_difference_matches(state, curve_type=None):
    matches = []
    for intersection in state.find("IntersectionOf"):
        if len(intersection.arguments) != 2:
            continue
        first, second = intersection.arguments
        if state.has_type(first, "Line"):
            line, curve = first, second
        elif state.has_type(second, "Line"):
            line, curve = second, first
        else:
            continue
        if curve_type is not None and not state.has_type(curve, curve_type):
            continue
        points = intersection.value
        expression = state.get("ExpressionPolynomial", curve)
        if (
            not isinstance(points, tuple)
            or len(points) != 2
            or expression is None
            or not isinstance(expression.value, PolynomialEquation)
        ):
            continue
        matches.append(
            {
                "line": line,
                "curve": curve,
                "points": points,
                "polynomial": expression.value,
                "_evidence": (intersection, expression),
            }
        )
    return matches


def _point_difference_relation(polynomial, first, second, solver):
    x1, x2 = _coordinate(first, "x"), _coordinate(second, "x")
    y1, y2 = _coordinate(first, "y"), _coordinate(second, "y")
    return equation(
        solver.add(
            solver.mul(polynomial.x2, solver.add(x1, x2), sub(x1, x2)),
            solver.mul(
                polynomial.xy,
                sub(solver.mul(x1, y1), solver.mul(x2, y2)),
            ),
            solver.mul(polynomial.y2, solver.add(y1, y2), sub(y1, y2)),
            solver.mul(polynomial.x, sub(x1, x2)),
            solver.mul(polynomial.y, sub(y1, y2)),
        ),
        0,
    )


class PointDifferenceV2(TheoremModelV2):
    model_id = 44
    name = "Point_Difference_Method_V2"
    curve_type = None
    output_predicate = "PointDifferenceRelationOf"

    def match(self, state):
        return _point_difference_matches(state, self.curve_type)

    def derive(self, state, binding, solver):
        first, second = binding["points"]
        relation = _point_difference_relation(
            binding["polynomial"], first, second, solver
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            self.output_predicate,
            binding["line"],
            binding["curve"],
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class EllipsePointDifferenceV2(PointDifferenceV2):
    model_id = 45
    name = "Point_Difference_Method_Ellipse_V2"
    curve_type = "Ellipse"
    output_predicate = "EllipsePointDifferenceRelationOf"


class HyperbolaPointDifferenceV2(PointDifferenceV2):
    model_id = 46
    name = "Point_Difference_Method_Hyperbola_V2"
    curve_type = "Hyperbola"
    output_predicate = "HyperbolaPointDifferenceRelationOf"


class CosineLawV2(TheoremModelV2):
    model_id = 47
    name = "Cosine_Law_V2"

    def match(self, state):
        return [
            {
                "first": angle.arguments[0],
                "vertex": angle.arguments[1],
                "third": angle.arguments[2],
                "angle": angle.value,
                "_evidence": (angle,),
            }
            for angle in state.find("AngleValueOf")
        ]

    def derive(self, state, binding, solver):
        first = binding["first"]
        vertex = binding["vertex"]
        third = binding["third"]
        opposite = _distance(first, third)
        side1 = _distance(first, vertex)
        side2 = _distance(vertex, third)
        relation = equation(
            solver.square(opposite),
            solver.sub(
                solver.add(solver.square(side1), solver.square(side2)),
                solver.mul(
                    2,
                    side1,
                    side2,
                    Term("cos", (binding["angle"],)),
                ),
            ),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "CosineLawRelationOf",
            first,
            vertex,
            third,
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class SineLawV2(TheoremModelV2):
    model_id = 48
    name = "Sine_Law_V2"

    def match(self, state):
        grouped = {}
        for angle in state.find("AngleValueOf"):
            points = frozenset(angle.arguments)
            grouped.setdefault(points, []).append(angle)
        matches = []
        for angles in grouped.values():
            if len(angles) < 2:
                continue
            first, second = angles[:2]
            matches.append(
                {
                    "first_angle": first,
                    "second_angle": second,
                    "_evidence": (first, second),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = binding["first_angle"]
        second = binding["second_angle"]
        a, vertex_a, c = first.arguments
        b, vertex_b, _ = second.arguments
        opposite_a = _distance(a, c)
        opposite_b = _distance(b, c)
        relation = equation(
            solver.div(opposite_a, Term("sin", (first.value,))),
            solver.div(opposite_b, Term("sin", (second.value,))),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "SineLawRelationOf",
            tuple(sorted(set(first.arguments + second.arguments))),
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class PythagoreanTheoremV2(TheoremModelV2):
    model_id = 49
    name = "Pythagorean_Theorem_V2"

    def match(self, state):
        matches = []
        for right_angle in state.find("RightAngleOf"):
            matches.append(
                {
                    "first": right_angle.arguments[0],
                    "vertex": right_angle.arguments[1],
                    "third": right_angle.arguments[2],
                    "_evidence": (right_angle,),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = binding["first"]
        vertex = binding["vertex"]
        third = binding["third"]
        relation = equation(
            solver.square(_distance(first, third)),
            solver.add(
                solver.square(_distance(first, vertex)),
                solver.square(_distance(vertex, third)),
            ),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "PythagoreanRelationOf",
            first,
            vertex,
            third,
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ChordLengthV2(TheoremModelV2):
    model_id = 50
    name = "Chord_Length_Formula_V2"
    output_predicate = "ChordLengthFormulaOf"

    def match(self, state):
        matches = []
        for quadratic_fact in state.find("QuadraticPolynomialOf"):
            line, curve = quadratic_fact.arguments
            quadratic = quadratic_fact.value
            if not isinstance(quadratic, QuadraticPolynomial):
                continue
            line_form = state.get("LineNormalFormOf", line)
            if line_form is None or not isinstance(line_form.value, LineEquation):
                continue
            matches.append(
                {
                    "line": line,
                    "curve": curve,
                    "quadratic": quadratic,
                    "line_form": line_form.value,
                    "_evidence": (quadratic_fact, line_form),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        quadratic = binding["quadratic"]
        root_sum = solver.div(neg(quadratic.b), quadratic.a)
        root_product = solver.div(quadratic.c, quadratic.a)
        difference = solver.sqrt_positive(
            sub(solver.square(root_sum), solver.mul(4, root_product))
        )
        line = binding["line_form"]
        if quadratic.variable == "x":
            slope = solver.div(neg(line.a), line.b)
            factor = solver.sqrt_positive(
                solver.add(1, solver.square(slope))
            )
        else:
            factor = Fraction(1)
        length = solver.mul(difference, factor)
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            self.output_predicate,
            binding["line"],
            binding["curve"],
            value=length,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ChordLengthWithKV2(ChordLengthV2):
    model_id = 51
    name = "Chord_Length_Formula_With_K_V2"
    output_predicate = "ChordLengthWithKFormulaOf"


class TriangleAreaBaseHeightV2(TheoremModelV2):
    model_id = 56
    name = "Triangle_Area_Formula_V2"

    def match(self, state):
        return [
            {
                "points": request.arguments,
                "target": request.value,
                "_evidence": (request,),
            }
            for request in state.find("RequestedAreaOf")
        ]

    def derive(self, state, binding, solver):
        first, second, third = binding["points"]
        area = solver.div(
            solver.mul(
                _distance(first, second),
                Term(
                    "point_line_distance",
                    (third, f"LineOf({first},{second})"),
                ),
            ),
            2,
        )
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "AreaBaseHeightFormulaOf",
                first,
                second,
                third,
                value=area,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                "area",
                self.model_id,
                *binding["points"],
                value=equation(binding["target"], area),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class TriangleAreaWithSinV2(TheoremModelV2):
    model_id = 57
    name = "Triangle_Area_With_Sin_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedAreaOf"):
            points = set(request.arguments)
            for angle in state.find("AngleValueOf"):
                if set(angle.arguments) != points:
                    continue
                matches.append(
                    {
                        "points": request.arguments,
                        "target": request.value,
                        "angle_fact": angle,
                        "_evidence": (request, angle),
                    }
                )
        return matches

    def derive(self, state, binding, solver):
        angle = binding["angle_fact"]
        first, vertex, third = angle.arguments
        area = solver.div(
            solver.mul(
                _distance(first, vertex),
                _distance(vertex, third),
                Term("sin", (angle.value,)),
            ),
            2,
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "AreaWithSinFormulaOf",
            binding["points"],
            value=area,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class TriangleAreaCoordinateV2(TheoremModelV2):
    model_id = 58
    name = "Triangle_Area_Coordinate_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedAreaOf"):
            positions = [
                state.value("PointPositionOf", point)
                for point in request.arguments
            ]
            if not all(isinstance(position, Point2D) for position in positions):
                continue
            matches.append(
                {
                    "points": request.arguments,
                    "positions": positions,
                    "target": request.value,
                    "_evidence": (
                        request,
                        *(
                            state.get("PointPositionOf", point)
                            for point in request.arguments
                        ),
                    ),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first, second, third = binding["positions"]
        determinant = solver.add(
            solver.mul(
                first.x,
                sub(second.y, third.y),
            ),
            solver.mul(
                second.x,
                sub(third.y, first.y),
            ),
            solver.mul(
                third.x,
                sub(first.y, second.y),
            ),
        )
        if isinstance(determinant, Fraction):
            absolute = abs(determinant)
        else:
            absolute = Term("abs", (determinant,))
        area = solver.div(absolute, 2)
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "CoordinateAreaFormulaOf",
                binding["points"],
                value=area,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                "area",
                self.model_id,
                *binding["points"],
                value=equation(binding["target"], area),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


def constructed_geometry_models():
    return [
        PointDifferenceV2(),
        EllipsePointDifferenceV2(),
        HyperbolaPointDifferenceV2(),
        CosineLawV2(),
        SineLawV2(),
        PythagoreanTheoremV2(),
        ChordLengthV2(),
        ChordLengthWithKV2(),
        TriangleAreaBaseHeightV2(),
        TriangleAreaWithSinV2(),
        TriangleAreaCoordinateV2(),
    ]
