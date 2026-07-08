"""Semantically stable advanced conic and line executors."""

from __future__ import annotations

from fractions import Fraction

from ..base import TheoremModelV2
from ..expressions import equation, is_zero, mul, neg, sub
from ..quantity_schema import QuantityRef
from ..schema import (
    Derivation,
    LineThroughOrigin,
    PolynomialEquation,
    StandardConicForm,
    StateDelta,
    Term,
)
from ..structured_schema import LineEquation, Point2D, Vector2D
from .common import theorem_fact


def _focus_triangle_matches(state, curve_type):
    matches = []
    for angle in state.find("AngleValueOf"):
        first, point, second = angle.arguments
        curves = [
            curve
            for curve in state.symbols
            if state.has_type(curve, curve_type)
            and state.get("FocusOf", curve, first) is not None
            and state.get("FocusOf", curve, second) is not None
            and state.get("PointOnCurve", point, curve) is not None
        ]
        for curve in curves:
            b2 = state.get("ParameterOf", curve, "semi_axis_b_squared")
            if b2 is None:
                continue
            area = state.get("RequestedAreaOf", first, point, second)
            if area is None:
                area = state.get("RequestedAreaOf", point, first, second)
            evidence = [angle, b2]
            if area is not None:
                evidence.append(area)
            matches.append(
                {
                    "curve": curve,
                    "points": (first, point, second),
                    "angle": angle.value,
                    "b2": b2.value,
                    "target": area.value if area is not None else None,
                    "_evidence": tuple(evidence),
                }
            )
    return matches


class _FocalTriangleAreaV2(TheoremModelV2):
    curve_type: str
    function_name: str

    def match(self, state):
        return _focus_triangle_matches(state, self.curve_type)

    def derive(self, state, binding, solver):
        half_angle = solver.div(binding["angle"], 2)
        tangent = Term("tan", (half_angle,))
        if self.function_name == "tan":
            area = solver.mul(binding["b2"], tangent)
        else:
            area = solver.div(binding["b2"], tangent)
        evidence = binding["_evidence"]
        facts = [
            theorem_fact(
                self.model_id,
                "FocalTriangleAreaFormulaOf",
                binding["curve"],
                value=area,
                evidence=evidence,
            )
        ]
        if binding["target"] is not None:
            facts.append(
                theorem_fact(
                    self.model_id,
                    "EquationConstraint",
                    "focal_triangle_area",
                    binding["curve"],
                    value=equation(binding["target"], area),
                    evidence=evidence,
                )
            )
        return Derivation(
            StateDelta(add_facts=tuple(facts)),
            self.evidence(*evidence),
        )


class EllipseFocalTriangleAreaV2(_FocalTriangleAreaV2):
    model_id = 30
    name = "Ellipse_Focal_Triangle_Area_V2"
    curve_type = "Ellipse"
    function_name = "tan"


class HyperbolaFocalTriangleAreaV2(_FocalTriangleAreaV2):
    model_id = 31
    name = "Hyperbola_Focal_Triangle_Area_V2"
    curve_type = "Hyperbola"
    function_name = "cot"


def _parabola_focal_chords(state):
    matches = []
    for intersection in state.find("IntersectionOf"):
        first, second = intersection.arguments
        if state.has_type(first, "Line") and state.has_type(second, "Parabola"):
            line, curve = first, second
        elif state.has_type(second, "Line") and state.has_type(first, "Parabola"):
            line, curve = second, first
        else:
            continue
        points = intersection.value
        form = state.get("ConicStandardForm", curve)
        if (
            not isinstance(points, tuple)
            or len(points) != 2
            or form is None
            or not isinstance(form.value, StandardConicForm)
        ):
            continue
        focus_relations = state.find("FocusOf", curve)
        through_focus = [
            relation
            for relation in focus_relations
            if state.get("PointOnCurve", relation.arguments[1], line) is not None
        ]
        if not through_focus:
            continue
        matches.append(
            {
                "line": line,
                "curve": curve,
                "points": points,
                "form": form.value,
                "_evidence": (intersection, form, through_focus[0]),
            }
        )
    return matches


class ParabolaFocalChordLengthV2(TheoremModelV2):
    model_id = 33
    name = "Parabola_Focal_Chord_Length_V2"

    def match(self, state):
        return _parabola_focal_chords(state)

    def derive(self, state, binding, solver):
        first, second = binding["points"]
        form = binding["form"]
        axis = "x" if form.orientation in {"right", "left"} else "y"
        coordinate_sum = solver.add(
            Term("coordinate", (first, axis)),
            Term("coordinate", (second, axis)),
        )
        p = solver.div(form.two_p, 2)
        directed_sum = (
            coordinate_sum
            if form.orientation in {"right", "up"}
            else neg(coordinate_sum)
        )
        length = solver.add(directed_sum, p)
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "ParabolaFocalChordLengthOf",
            binding["line"],
            binding["curve"],
            value=length,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ParabolaFocalChordProductXV2(TheoremModelV2):
    model_id = 34
    name = "Parabola_Focal_Chord_Product_X_V2"

    def match(self, state):
        return [
            match
            for match in _parabola_focal_chords(state)
            if match["form"].orientation in {"right", "left"}
        ]

    def derive(self, state, binding, solver):
        form = binding["form"]
        value = solver.square(form.focus_offset)
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "FocalChordCoordinateProductOf",
            binding["line"],
            binding["curve"],
            "x",
            value=value,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ParabolaFocalChordProductYV2(ParabolaFocalChordProductXV2):
    model_id = 35
    name = "Parabola_Focal_Chord_Product_Y_V2"

    def derive(self, state, binding, solver):
        form = binding["form"]
        p = solver.div(form.two_p, 2)
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "FocalChordCoordinateProductOf",
            binding["line"],
            binding["curve"],
            "y",
            value=neg(solver.square(p)),
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class ParabolaFocalChordAngleV2(TheoremModelV2):
    model_id = 36
    name = "Parabola_Focal_Chord_Formula_Angle_V2"

    def match(self, state):
        matches = []
        for match in _parabola_focal_chords(state):
            angle = state.get(
                "QuantityValueOf",
                QuantityRef.of("inclination", match["line"]),
            )
            if angle is None:
                continue
            matches.append(
                {
                    **match,
                    "angle": angle.value,
                    "_evidence": (*match["_evidence"], angle),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        sine = Term("sin", (binding["angle"],))
        length = solver.div(
            binding["form"].two_p,
            solver.square(sine),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "FocalChordAngleLengthOf",
            binding["line"],
            binding["curve"],
            value=length,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class EllipseMidpointChordSlopeV2(TheoremModelV2):
    model_id = 40
    name = "Ellipse_Midpoint_Chord_Slope_V2"

    def match(self, state):
        matches = []
        for intersection in state.find("IntersectionOf"):
            first, second = intersection.arguments
            if state.has_type(first, "Line") and state.has_type(second, "Ellipse"):
                line, curve = first, second
            elif state.has_type(second, "Line") and state.has_type(first, "Ellipse"):
                line, curve = second, first
            else:
                continue
            points = intersection.value
            if not isinstance(points, tuple) or len(points) != 2:
                continue
            midpoint = state.get("MidPointOf", *points)
            if midpoint is None:
                midpoint = state.get("MidPointOf", points[1], points[0])
            line_form = state.get("LineNormalFormOf", line)
            expression = state.get("ExpressionPolynomial", curve)
            if (
                midpoint is None
                or line_form is None
                or not isinstance(line_form.value, LineEquation)
                or expression is None
                or not isinstance(expression.value, PolynomialEquation)
            ):
                continue
            position = state.get("PointPositionOf", midpoint.value)
            if position is None or not isinstance(position.value, Point2D):
                continue
            matches.append(
                {
                    "line": line,
                    "curve": curve,
                    "midpoint": midpoint.value,
                    "position": position.value,
                    "line_form": line_form.value,
                    "polynomial": expression.value,
                    "_evidence": (
                        intersection,
                        midpoint,
                        position,
                        line_form,
                        expression,
                    ),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        line = binding["line_form"]
        position = binding["position"]
        polynomial = binding["polynomial"]
        chord_slope = solver.div(neg(line.a), line.b)
        midpoint_slope = solver.div(position.y, position.x)
        expected = solver.div(neg(polynomial.x2), polynomial.y2)
        relation = equation(
            solver.mul(chord_slope, midpoint_slope),
            expected,
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "MidpointChordSlopeRelationOf",
            binding["line"],
            binding["curve"],
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class VectorDotProductGeometricV2(TheoremModelV2):
    model_id = 60
    name = "Vector_Dot_Product_Geometric_V2"

    def match(self, state):
        matches = []
        for request in state.find("RequestedDotProductOf"):
            a, b, c, d = request.arguments
            if a != c:
                continue
            angle = state.get("AngleValueOf", b, a, d)
            if angle is None:
                angle = state.get("AngleValueOf", d, a, b)
            if angle is None:
                continue
            first = state.get("VectorOf", a, b)
            second = state.get("VectorOf", c, d)
            matches.append(
                {
                    "first": (a, b),
                    "second": (c, d),
                    "angle": angle.value,
                    "target": request.value,
                    "_evidence": tuple(
                        fact
                        for fact in (request, angle, first, second)
                        if fact is not None
                    ),
                }
            )
        return matches

    def derive(self, state, binding, solver):
        first = Term("vector_norm", (binding["first"],))
        second = Term("vector_norm", (binding["second"],))
        value = solver.mul(
            first,
            second,
            Term("cos", (binding["angle"],)),
        )
        evidence = binding["_evidence"]
        facts = (
            theorem_fact(
                self.model_id,
                "GeometricDotProductOf",
                binding["first"],
                binding["second"],
                value=value,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                "dot_product_geometric",
                binding["first"],
                binding["second"],
                value=equation(binding["target"], value),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class LineInterceptFormV2(TheoremModelV2):
    model_id = 74
    name = "Line_Intercept_Form_V2"

    def match(self, state):
        return [
            {
                "line": fact.arguments[0],
                "form": fact.value,
                "_evidence": (fact,),
            }
            for fact in state.find("LineNormalFormOf")
            if isinstance(fact.value, LineEquation)
            and not is_zero(fact.value.a)
            and not is_zero(fact.value.b)
            and not is_zero(fact.value.c)
        ]

    def derive(self, state, binding, solver):
        form = binding["form"]
        intercepts = (
            solver.div(neg(form.c), form.a),
            solver.div(neg(form.c), form.b),
        )
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "LineInterceptsOf",
            binding["line"],
            value=intercepts,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


class CircleTangentConditionV2(TheoremModelV2):
    model_id = 76
    name = "Circle_Tangent_Condition_V2"

    def match(self, state):
        matches = []
        for tangent in state.find("TangentRelation"):
            first, second = tangent.arguments
            circle, other = self._circle_and_other(state, first, second)
            if circle is None:
                continue
            center = self._center(state, circle)
            radius = self._radius(state, circle)
            line = self._line_form(state, other)
            if center is None or radius is None or line is None:
                continue
            matches.append(
                {
                    "circle": circle,
                    "other": other,
                    "center": center,
                    "radius": radius,
                    "line": line,
                    "_evidence": (tangent,),
                }
            )
        return matches

    @staticmethod
    def _circle_and_other(state, first, second):
        if state.has_type(first, "Circle"):
            return first, second
        if state.has_type(second, "Circle"):
            return second, first
        return None, None

    @staticmethod
    def _center(state, circle):
        form = state.value("CircleStandardForm", circle)
        if isinstance(form, tuple) and len(form) == 3:
            return Point2D(form[0], form[1])
        relations = state.find("CenterPointOf", circle)
        if len(relations) == 1:
            return state.value("PointPositionOf", relations[0].arguments[1])
        return None

    @staticmethod
    def _radius(state, circle):
        value = state.value("ParameterOf", circle, "radius")
        if value is not None:
            return value
        return state.value(
            "QuantityValueOf", QuantityRef.of("radius", circle)
        )

    @staticmethod
    def _line_form(state, other):
        line = state.value("LineNormalFormOf", other)
        if isinstance(line, LineEquation):
            return line
        directrix = state.value("LineNormalFormOf", other.replace(" ", ""))
        if isinstance(directrix, LineEquation):
            return directrix
        if other.startswith("Asymptote(") and other.endswith(")"):
            curve = other[len("Asymptote(") : -1]
            family = state.value("AsymptoteFamilyOf", curve)
            if isinstance(family, tuple) and family:
                candidate = family[0]
                if isinstance(candidate, LineThroughOrigin):
                    return LineEquation(neg(candidate.slope), 1, 0)
        return None

    def derive(self, state, binding, solver):
        center = binding["center"]
        line = binding["line"]
        numerator = solver.add(
            solver.mul(line.a, center.x),
            solver.mul(line.b, center.y),
            line.c,
        )
        denominator = solver.sqrt_positive(
            solver.add(solver.square(line.a), solver.square(line.b))
        )
        distance = solver.div(Term("abs", (numerator,)), denominator)
        relation = equation(distance, binding["radius"])
        evidence = binding["_evidence"]
        fact = theorem_fact(
            self.model_id,
            "CircleTangentConditionOf",
            binding["circle"],
            binding["other"],
            value=relation,
            evidence=evidence,
        )
        return Derivation(StateDelta(add_facts=(fact,)), self.evidence(*evidence))


def quantity_conic_models():
    return [
        EllipseFocalTriangleAreaV2(),
        HyperbolaFocalTriangleAreaV2(),
        ParabolaFocalChordLengthV2(),
        ParabolaFocalChordProductXV2(),
        ParabolaFocalChordProductYV2(),
        ParabolaFocalChordAngleV2(),
        EllipseMidpointChordSlopeV2(),
        VectorDotProductGeometricV2(),
        LineInterceptFormV2(),
        CircleTangentConditionV2(),
    ]
