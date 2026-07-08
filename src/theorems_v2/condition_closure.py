"""Translate high-confidence conic conditions into exact parameter equations."""

from __future__ import annotations

from fractions import Fraction

from .expressions import div, equation, is_zero, mul, square
from .schema import Provenance, Term
from .structured_schema import Point2D


class ConicConditionEquationClosure:
    """Bridge structured givens and the generic exact elimination engine."""

    _AXIS_PARAMETER = {
        "MajorAxis": "semi_axis_a_squared",
        "RealAxis": "semi_axis_a_squared",
        "MinorAxis": "semi_axis_b_squared",
        "ImageinaryAxis": "semi_axis_b_squared",
    }

    def enrich(self, source):
        state = source.clone()
        self._focus_separations(state)
        self._asymptote_points(state)
        self._axis_length_ratios(state)
        self._vector_parameter_ratios(state)
        self._parameter_square_relations(state)
        return state

    def _focus_separations(self, state):
        for distance in state.find("RequestedDistanceOf"):
            if len(distance.arguments) != 2:
                continue
            first, second = distance.arguments
            matching_curves = []
            for curve in self._conics(state):
                if (
                    state.get("FocusOf", curve, first) is not None
                    and state.get("FocusOf", curve, second) is not None
                    and first != second
                ):
                    matching_curves.append(curve)
            if len(matching_curves) != 1:
                continue
            curve = matching_curves[0]
            half_distance = div(distance.value, 2)
            self._add(
                state,
                "FocusSeparationOf",
                curve,
                value=distance.value,
            )
            self._add(
                state,
                "EquationConstraint",
                equation(
                    self._parameter(curve, "focal_half_distance_squared"),
                    square(half_distance),
                ),
                value=None,
            )

    def _asymptote_points(self, state):
        for relation in state.find("PointOnAsymptoteOf"):
            if len(relation.arguments) != 2:
                continue
            curve, point = relation.arguments
            position = state.value("PointPositionOf", point)
            if not isinstance(position, Point2D) or is_zero(position.x):
                continue
            line = f"{curve}__point_asymptote__{point}"
            if line not in state.symbols:
                state.declare(
                    line,
                    "Line",
                    provenance=Provenance.given("condition_closure"),
                )
            self._add(state, "AsymptoteOf", curve, line, value=True)
            self._add(
                state,
                "SlopeOf",
                line,
                value=div(position.y, position.x),
            )
    def _axis_length_ratios(self, state):
        for relation in state.find("AxisLengthRatioOf"):
            if len(relation.arguments) != 3:
                continue
            curve, left_kind, right_kind = relation.arguments
            left_parameter = self._AXIS_PARAMETER.get(left_kind)
            right_parameter = self._AXIS_PARAMETER.get(right_kind)
            if left_parameter is None or right_parameter is None:
                continue
            self._add(
                state,
                "EquationConstraint",
                equation(
                    self._parameter(curve, left_parameter),
                    mul(
                        square(relation.value),
                        self._parameter(curve, right_parameter),
                    ),
                ),
                value=None,
            )

    def _parameter_square_relations(self, state):
        parameter_pairs = (
            ("semi_axis_a", "semi_axis_a_squared"),
            ("semi_axis_b", "semi_axis_b_squared"),
            ("focal_half_distance", "focal_half_distance_squared"),
        )
        for curve in self._conics(state):
            if state.get("ConicStandardForm", curve) is None:
                continue
            for plain_name, squared_name in parameter_pairs:
                self._add(
                    state,
                    "EquationConstraint",
                    equation(
                        self._parameter(curve, squared_name),
                        square(self._parameter(curve, plain_name)),
                    ),
                    value=None,
                )

    def _vector_parameter_ratios(self, state):
        for relation in state.find("VectorLinearRelation"):
            terms = relation.value
            if not isinstance(terms, tuple) or not terms:
                continue
            weights = {}
            valid = True
            for start, end, coefficient in terms:
                if not isinstance(coefficient, Fraction):
                    valid = False
                    break
                weights[start] = weights.get(start, Fraction(0)) - coefficient
                weights[end] = weights.get(end, Fraction(0)) + coefficient
            if not valid:
                continue
            weights = {
                point: coefficient
                for point, coefficient in weights.items()
                if coefficient != 0
            }
            candidates = []
            for curve in self._conics(state):
                if state.get("ConicStandardForm", curve) is None:
                    continue
                a_coefficient = Fraction(0)
                c_coefficient = Fraction(0)
                supported = True
                for point, coefficient in weights.items():
                    focus = state.get("FocusOf", curve, point)
                    if focus is not None:
                        side = state.value("FocusSideOf", curve, point)
                        direction = self._signed_side(side)
                        if direction is None:
                            supported = False
                            break
                        c_coefficient += coefficient * direction
                        continue
                    vertex = state.get("VertexSideOf", curve, point)
                    if vertex is not None:
                        direction = self._signed_side(vertex.value)
                        if direction is None:
                            supported = False
                            break
                        a_coefficient += coefficient * direction
                        continue
                    supported = False
                    break
                if supported and a_coefficient != 0 and c_coefficient != 0:
                    ratio = -a_coefficient / c_coefficient
                    if ratio > 0:
                        candidates.append((curve, ratio))
            if len(candidates) != 1:
                continue
            curve, ratio = candidates[0]
            self._add(
                state,
                "ParameterRatioOf",
                curve,
                "c_over_a",
                value=ratio,
            )
            self._add(
                state,
                "ResolvedParameterOf",
                curve,
                "eccentricity",
                value=ratio,
            )

    @staticmethod
    def _signed_side(side):
        if side in {"left", "lower"}:
            return Fraction(-1)
        if side in {"right", "upper"}:
            return Fraction(1)
        return None

    @staticmethod
    def _conics(state):
        return (
            name
            for name, symbol in state.symbols.items()
            if symbol.type_name in {"Ellipse", "Hyperbola"}
        )

    @staticmethod
    def _parameter(curve, name):
        return Term("parameter", (curve, name))

    @staticmethod
    def _add(state, predicate, *arguments, value):
        if state.get(predicate, *arguments) is None:
            state.add_given(
                predicate,
                *arguments,
                value=value,
                provenance=Provenance.given("condition_closure"),
            )
