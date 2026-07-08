"""Conservative query reachability and answer checking for v3 replay."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, replace
from enum import Enum
from fractions import Fraction
from typing import Any, Optional, Tuple

from .expressions import div, mul, neg
from .quantity_raw_adapter import QuantityRawFactAdapter
from .quantity_schema import QuantityRef
from .schema import (
    AxisLine,
    LineThroughOrigin,
    PolynomialEquation,
    StandardConicForm,
    Term,
)
from .structured_schema import Point2D


class GoalStatus(str, Enum):
    GOAL_UNSUPPORTED = "GOAL_UNSUPPORTED"
    GOAL_NOT_REACHED = "GOAL_NOT_REACHED"
    VALUE_UNRESOLVED = "VALUE_UNRESOLVED"
    ANSWER_UNSUPPORTED = "ANSWER_UNSUPPORTED"
    ANSWER_CORRECT = "ANSWER_CORRECT"
    ANSWER_INCORRECT = "ANSWER_INCORRECT"


@dataclass(frozen=True)
class GoalCheckResult:
    status: GoalStatus
    query_kind: str
    actual_value: Any = None
    expected_value: Any = None
    source_predicate: Optional[str] = None
    detail: str = ""


@dataclass(frozen=True)
class LineEquationTarget:
    kind: str
    axis: str
    value: Any


class GoalCheckerV3:
    ECCENTRICITY = re.compile(r"^Eccentricity\((\w+)\)$")
    EXPRESSION = re.compile(r"^Expression\((\w+)\)$")
    ASYMPTOTE_EXPRESSION = re.compile(
        r"^Expression\(Asymptote\((\w+)\)\)$"
    )
    DIRECTRIX_EXPRESSION = re.compile(
        r"^Expression\((Directrix|LeftDirectrix|RightDirectrix)"
        r"\((\w+)\)\)$"
    )
    FOCAL_LENGTH = re.compile(r"^FocalLength\((\w+)\)$")
    AXIS_LENGTH = re.compile(
        r"^Length\((MajorAxis|MinorAxis|RealAxis|ImageinaryAxis)"
        r"\((\w+)\)\)$"
    )
    RADIUS = re.compile(r"^Radius\((\w+)\)$")
    COORDINATE = re.compile(r"^Coordinate\((\w+)\)$")
    FOCUS_COORDINATE = re.compile(
        r"^Coordinate\((Focus|LeftFocus|RightFocus)\((\w+)\)\)$"
    )
    X_COORDINATE = re.compile(r"^XCoordinate\((\w+)\)$")
    Y_COORDINATE = re.compile(r"^YCoordinate\((\w+)\)$")
    DISTANCE = re.compile(r"^Distance\((\w+),\s*(\w+)\)$")
    FOCUS_DIRECTRIX_DISTANCE = re.compile(
        r"^Distance\(Focus\((\w+)\),\s*Directrix\(\1\)\)$"
    )
    FOCUS_ASYMPTOTE_DISTANCE = re.compile(
        r"^Distance\(Focus\((\w+)\),\s*Asymptote\(\1\)\)$"
    )
    NAMED_FOCUS_ASYMPTOTE_DISTANCE = re.compile(
        r"^Distance\((\w+),\s*OneOf\(Asymptote\((\w+)\)\)\)$"
    )
    PERIMETER = re.compile(
        r"^Perimeter\(TriangleOf\((\w+),\s*(\w+),\s*(\w+)\)\)$"
    )
    SEGMENT = re.compile(
        r"^Abs\(LineSegmentOf\((\w+),\s*(\w+)\)\)$"
    )
    SLOPE = re.compile(r"^Slope\((\w+)\)$")
    AREA = re.compile(
        r"^Area\(TriangleOf\((\w+),\s*(\w+),\s*(\w+)\)\)$"
    )
    SIMPLE_PARAMETER = re.compile(r"^([abcep])$")

    PARAMETER_NAMES = {
        "a": "semi_axis_a",
        "b": "semi_axis_b",
        "c": "focal_half_distance",
        "e": "eccentricity",
        "p": "p",
    }

    def __init__(self):
        self.parser = QuantityRawFactAdapter()

    def check(self, state, query: str, answer: str) -> GoalCheckResult:
        query = str(query or "").strip()
        answer = str(answer or "").strip()
        if not query or ";" in query or "\n" in query:
            return GoalCheckResult(
                GoalStatus.GOAL_UNSUPPORTED,
                self.query_kind(query),
                detail="empty or multi-goal query",
            )

        extracted = self._extract(state, query)
        if extracted is None:
            return GoalCheckResult(
                GoalStatus.GOAL_UNSUPPORTED,
                self.query_kind(query),
                detail="query grammar is not supported",
            )
        actual, predicate = extracted
        if actual is None:
            return GoalCheckResult(
                GoalStatus.GOAL_NOT_REACHED,
                self.query_kind(query),
                source_predicate=predicate,
            )

        from .resolution import StateExpressionResolver

        actual = StateExpressionResolver(state).resolve(actual)
        expected = self._parse_answer(answer, actual)
        if expected is _UNSUPPORTED:
            return GoalCheckResult(
                GoalStatus.ANSWER_UNSUPPORTED,
                self.query_kind(query),
                actual_value=actual,
                source_predicate=predicate,
                detail="answer expression is not supported",
            )

        comparison = self._equivalent(actual, expected)
        if comparison is None:
            return GoalCheckResult(
                GoalStatus.VALUE_UNRESOLVED,
                self.query_kind(query),
                actual_value=actual,
                expected_value=expected,
                source_predicate=predicate,
            )
        return GoalCheckResult(
            GoalStatus.ANSWER_CORRECT
            if comparison
            else GoalStatus.ANSWER_INCORRECT,
            self.query_kind(query),
            actual_value=actual,
            expected_value=expected,
            source_predicate=predicate,
        )

    @staticmethod
    def _parameter_value(state, entity, parameter_name):
        from .resolution import StateExpressionResolver

        return StateExpressionResolver(state).parameter_value(
            entity, parameter_name
        )

    def _extract(self, state, query):
        match = self.ASYMPTOTE_EXPRESSION.match(query)
        if match:
            family = state.value("AsymptoteFamilyOf", match.group(1))
            if isinstance(family, tuple) and family and all(
                isinstance(line, LineThroughOrigin) for line in family
            ):
                line = family[0]
                return (
                    LineEquationTarget(
                        "asymptote",
                        line.dependent_axis,
                        Term("abs", (line.slope,)),
                    ),
                    "AsymptoteFamilyOf",
                )
            return None, "AsymptoteFamilyOf"

        match = self.DIRECTRIX_EXPRESSION.match(query)
        if match:
            relation, curve = match.groups()
            line = state.value("DirectrixExpressionOf", curve)
            if isinstance(line, AxisLine):
                return (
                    LineEquationTarget("axis_line", line.axis, line.value),
                    "DirectrixExpressionOf",
                )
            family = state.value("DirectrixFamilyOf", curve)
            if isinstance(family, tuple) and len(family) == 2:
                if relation == "LeftDirectrix":
                    line = family[1]
                elif relation == "RightDirectrix":
                    line = family[0]
                else:
                    line = None
                if isinstance(line, AxisLine):
                    return (
                        LineEquationTarget("axis_line", line.axis, line.value),
                        "DirectrixFamilyOf",
                    )
            return None, "DirectrixExpressionOf"
        match = self.EXPRESSION.match(query)
        if match:
            curve = match.group(1)
            form = state.value("ConicStandardForm", curve)
            if isinstance(form, StandardConicForm):
                updates = {}
                for field_name, parameter_name in (
                    ("a2", "semi_axis_a_squared"),
                    ("b2", "semi_axis_b_squared"),
                    ("two_p", "two_p"),
                ):
                    value = self._parameter_value(
                        state, curve, parameter_name
                    )
                    if value is not None:
                        updates[field_name] = value
                if updates:
                    form = replace(form, **updates)
            return form, "ConicStandardForm"
        match = self.ECCENTRICITY.match(query)
        if match:
            return (
                self._parameter_value(state, match.group(1), "eccentricity"),
                "ParameterOf",
            )

        match = self.FOCAL_LENGTH.match(query)
        if match:
            value = self._parameter_value(
                state, match.group(1), "focal_half_distance"
            )
            return (None if value is None else mul(2, value), "ParameterOf")

        match = self.AXIS_LENGTH.match(query)
        if match:
            kind, entity = match.groups()
            parameter = (
                "semi_axis_a"
                if kind in {"MajorAxis", "RealAxis"}
                else "semi_axis_b"
            )
            value = self._parameter_value(state, entity, parameter)
            return (None if value is None else mul(2, value), "ParameterOf")

        match = self.RADIUS.match(query)
        if match:
            entity = match.group(1)
            value = self._parameter_value(state, entity, "radius")
            if value is None:
                value = state.value(
                    "QuantityValueOf",
                    QuantityRef.of("radius", entity),
                )
            return value, "QuantityValueOf"

        match = self.COORDINATE.match(query)
        if match:
            return (
                state.value("PointPositionOf", match.group(1)),
                "PointPositionOf",
            )

        match = self.FOCUS_COORDINATE.match(query)
        if match:
            relation, curve = match.groups()
            positions = []
            for focus in state.find("FocusOf", curve):
                point = focus.arguments[1]
                side = state.value("FocusSideOf", curve, point)
                if relation == "LeftFocus" and side != "left":
                    continue
                if relation == "RightFocus" and side != "right":
                    continue
                position = state.value("PointPositionOf", point)
                if position is not None:
                    positions.append(position)
            if len(positions) == 1:
                return positions[0], "PointPositionOf"
            if len(positions) > 1:
                return tuple(positions), "PointPositionOf"
            return None, "PointPositionOf"

        match = self.X_COORDINATE.match(query)
        if match:
            point = state.value("PointPositionOf", match.group(1))
            return (
                point.x if isinstance(point, Point2D) else None,
                "PointPositionOf",
            )

        match = self.Y_COORDINATE.match(query)
        if match:
            point = state.value("PointPositionOf", match.group(1))
            return (
                point.y if isinstance(point, Point2D) else None,
                "PointPositionOf",
            )

        match = self.FOCUS_DIRECTRIX_DISTANCE.match(query)
        if match:
            return self._parameter_value(state, match.group(1), "p"), "ParameterOf"

        match = self.FOCUS_ASYMPTOTE_DISTANCE.match(query)
        if match:
            return (
                state.value("FocusAsymptoteDistanceOf", match.group(1)),
                "FocusAsymptoteDistanceOf",
            )

        match = self.NAMED_FOCUS_ASYMPTOTE_DISTANCE.match(query)
        if match:
            point, curve = match.groups()
            if state.get("FocusOf", curve, point) is None:
                return None, "FocusAsymptoteDistanceOf"
            return (
                state.value("FocusAsymptoteDistanceOf", curve),
                "FocusAsymptoteDistanceOf",
            )

        match = self.PERIMETER.match(query)
        if match:
            requested = set(match.groups())
            candidates = []
            for fact in state.find("FocalTrianglePerimeterOf"):
                curve = fact.arguments[0]
                foci = {
                    focus.arguments[1]
                    for focus in state.find("FocusOf", curve)
                }
                curve_points = {
                    point.arguments[0]
                    for point in state.find("PointOnCurve")
                    if len(point.arguments) == 2 and point.arguments[1] == curve
                }
                if foci.issubset(requested) and requested - foci <= curve_points:
                    candidates.append(fact.value)
            if len(candidates) == 1:
                return candidates[0], "FocalTrianglePerimeterOf"
            return None, "FocalTrianglePerimeterOf"

        distance_sum = self._distance_sum_parts(query)
        if distance_sum is not None:
            point, first_focus, second_focus = distance_sum
            candidates = []
            for relation in state.find("DefinitionRelation"):
                if len(relation.arguments) != 2 or relation.arguments[1] != point:
                    continue
                curve = relation.arguments[0]
                if not state.has_type(curve, "Ellipse"):
                    continue
                foci = {
                    focus.arguments[1]
                    for focus in state.find("FocusOf", curve)
                }
                if foci != {first_focus, second_focus}:
                    continue
                value = relation.value
                if isinstance(value, Term) and value.operator == "eq":
                    candidates.append(value.arguments[1])
            if len(candidates) == 1:
                return candidates[0], "DefinitionRelation"
            return None, "DefinitionRelation"

        match = self.DISTANCE.match(query)
        if match:
            first, second = match.groups()
            value = state.value("DistanceFormulaOf", first, second)
            if value is None:
                value = state.value(
                    "QuantityValueOf",
                    QuantityRef.of("distance", first, second),
                )
            return value, "DistanceFormulaOf"

        match = self.SEGMENT.match(query)
        if match:
            first, second = match.groups()
            value = state.value("DistanceFormulaOf", first, second)
            if value is None:
                value = state.value(
                    "QuantityValueOf",
                    QuantityRef.of("distance", first, second),
                )
            return value, "DistanceFormulaOf"

        match = self.SLOPE.match(query)
        if match:
            return state.value("SlopeOf", match.group(1)), "SlopeOf"

        match = self.AREA.match(query)
        if match:
            points = match.groups()
            value = state.value("CoordinateAreaFormulaOf", points)
            if value is None:
                value = state.value(
                    "QuantityValueOf",
                    QuantityRef.of("area", *points),
                )
            return value, "CoordinateAreaFormulaOf"

        match = self.SIMPLE_PARAMETER.match(query)
        if match:
            symbol_name = match.group(1)
            direct = state.value("SymbolValueOf", symbol_name)
            if direct is not None:
                return direct, "SymbolValueOf"

            alias = state.value("ParameterAlias", symbol_name)
            if isinstance(alias, tuple) and len(alias) == 2:
                return self._parameter_value(state, *alias), "ParameterOf"

            declared = state.symbols.get(symbol_name)
            if declared is not None and declared.type_name in {"Number", "Real"}:
                return None, "SymbolValueOf"

            entities = [
                symbol.name
                for symbol in state.symbols.values()
                if symbol.type_name
                in {"Ellipse", "Hyperbola", "Parabola", "Circle"}
            ]
            if len(entities) != 1:
                return None, "ParameterOf"
            parameter = self.PARAMETER_NAMES[symbol_name]
            return (
                self._parameter_value(state, entities[0], parameter),
                "ParameterOf",
            )

        return None

    def _parse_answer(self, answer, actual):
        if not answer:
            return _UNSUPPORTED
        if isinstance(actual, LineEquationTarget):
            try:
                text = answer.replace("±", "pm").replace("pm", "1")
                polynomial = self.parser.expression_parser.parse_equation(text)
            except (SyntaxError, ValueError, ZeroDivisionError):
                return _UNSUPPORTED
            if actual.kind == "asymptote":
                if polynomial.y == 0:
                    return _UNSUPPORTED
                slope = div(neg(polynomial.x), polynomial.y)
                return LineEquationTarget(
                    "asymptote", "y", Term("abs", (slope,))
                )
            coefficient = polynomial.x if actual.axis == "x" else polynomial.y
            other = polynomial.y if actual.axis == "x" else polynomial.x
            if coefficient == 0 or other != 0:
                return _UNSUPPORTED
            value = div(neg(polynomial.constant), coefficient)
            return LineEquationTarget("axis_line", actual.axis, value)
        if isinstance(actual, StandardConicForm):
            try:
                return self.parser.expression_parser.parse_equation(answer)
            except (SyntaxError, ValueError, ZeroDivisionError):
                return _UNSUPPORTED
        if isinstance(actual, Point2D):
            match = re.match(r"^\((.*),(.*)\)$", answer)
            if not match or "pm" in answer:
                return _UNSUPPORTED
            try:
                return Point2D(
                    self.parser._scalar(match.group(1)),
                    self.parser._scalar(match.group(2)),
                )
            except (SyntaxError, ValueError, ZeroDivisionError):
                return _UNSUPPORTED
        try:
            return self.parser._scalar(answer)
        except (SyntaxError, ValueError, ZeroDivisionError):
            return _UNSUPPORTED

    def _equivalent(self, actual, expected):
        if actual == expected:
            return True
        if isinstance(actual, LineEquationTarget) and isinstance(
            expected, LineEquationTarget
        ):
            if actual.kind != expected.kind or actual.axis != expected.axis:
                return False
            return self._equivalent(actual.value, expected.value)
        if isinstance(actual, StandardConicForm) and isinstance(
            expected, PolynomialEquation
        ):
            return self._polynomial_equivalent(
                self._standard_form_polynomial(actual), expected
            )
        if isinstance(actual, Point2D) and isinstance(expected, Point2D):
            x_equal = self._equivalent(actual.x, expected.x)
            y_equal = self._equivalent(actual.y, expected.y)
            if x_equal is None or y_equal is None:
                return None
            return x_equal and y_equal
        actual_number = numeric_value(actual)
        expected_number = numeric_value(expected)
        if actual_number is None or expected_number is None:
            return None
        return math.isclose(
            actual_number,
            expected_number,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

    @staticmethod
    def _standard_form_polynomial(form):
        if form.curve_type == "ellipse":
            if form.orientation == "horizontal":
                return PolynomialEquation(
                    x2=div(1, form.a2), y2=div(1, form.b2), constant=-1
                )
            return PolynomialEquation(
                x2=div(1, form.b2), y2=div(1, form.a2), constant=-1
            )
        if form.curve_type == "hyperbola":
            if form.orientation == "horizontal":
                return PolynomialEquation(
                    x2=div(1, form.a2),
                    y2=neg(div(1, form.b2)),
                    constant=-1,
                )
            return PolynomialEquation(
                x2=neg(div(1, form.b2)),
                y2=div(1, form.a2),
                constant=-1,
            )
        if form.curve_type == "parabola":
            if form.orientation in {"right", "left"}:
                coefficient = (
                    form.two_p
                    if form.orientation == "right"
                    else neg(form.two_p)
                )
                return PolynomialEquation(y2=1, x=neg(coefficient))
            coefficient = (
                form.two_p if form.orientation == "up" else neg(form.two_p)
            )
            return PolynomialEquation(x2=1, y=neg(coefficient))
        return PolynomialEquation()

    @staticmethod
    def _polynomial_equivalent(actual, expected):
        names = ("x2", "xy", "y2", "x", "y", "constant")
        actual_values = [numeric_value(getattr(actual, name)) for name in names]
        expected_values = [numeric_value(getattr(expected, name)) for name in names]
        if any(value is None for value in actual_values + expected_values):
            return None
        ratio = None
        for left, right in zip(actual_values, expected_values):
            if math.isclose(left, 0.0, abs_tol=1e-12) and math.isclose(
                right, 0.0, abs_tol=1e-12
            ):
                continue
            if math.isclose(left, 0.0, abs_tol=1e-12) or math.isclose(
                right, 0.0, abs_tol=1e-12
            ):
                return False
            current = left / right
            if ratio is None:
                ratio = current
            elif not math.isclose(
                current, ratio, rel_tol=1e-9, abs_tol=1e-9
            ):
                return False
        return ratio is not None
    @staticmethod
    def _distance_sum_parts(query):
        normalized = re.sub(r"\s+", "", query)
        normalized = re.sub(
            r"Abs\(LineSegmentOf\((\w+),(\w+)\)\)",
            r"Distance(\1,\2)",
            normalized,
        )
        match = re.match(
            r"^Distance\((\w+),(\w+)\)\+Distance\((\w+),(\w+)\)$",
            normalized,
        )
        if not match:
            return None
        first_point, first_focus, second_point, second_focus = match.groups()
        if first_point != second_point:
            return None
        return first_point, first_focus, second_focus
    @staticmethod
    def query_kind(query):
        match = re.match(r"^([A-Za-z_]+)", str(query or "").strip())
        return match.group(1) if match else "OTHER"


_UNSUPPORTED = object()


def numeric_value(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return None
    if isinstance(value, Fraction):
        return float(value)
    if isinstance(value, int):
        return float(value)
    if isinstance(value, float):
        return value
    if not isinstance(value, Term):
        return None

    arguments = [numeric_value(argument) for argument in value.arguments]
    operator = value.operator
    if operator in {"sqrt", "sqrt_positive"}:
        if len(arguments) != 1 or arguments[0] is None or arguments[0] < 0:
            return None
        return math.sqrt(arguments[0])
    if operator == "add":
        return None if any(item is None for item in arguments) else sum(arguments)
    if operator == "mul":
        if any(item is None for item in arguments):
            return None
        result = 1.0
        for item in arguments:
            result *= item
        return result
    if operator == "div":
        if (
            len(arguments) != 2
            or arguments[0] is None
            or arguments[1] in {None, 0}
        ):
            return None
        return arguments[0] / arguments[1]
    if operator == "pow":
        if len(arguments) != 2 or any(item is None for item in arguments):
            return None
        return arguments[0] ** arguments[1]
    if operator == "abs":
        if len(arguments) != 1 or arguments[0] is None:
            return None
        return abs(arguments[0])
    return None
