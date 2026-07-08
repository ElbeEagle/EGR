"""Additional Conic10K fact patterns for the expanded executor batch."""

from __future__ import annotations

import ast
import re
from typing import Any, List, Tuple

from .expressions import div, neg, sign, square
from .raw_adapter import AdaptationResult, RawFactAdapter
from .schema import Term


class ExpandedRawFactAdapter(RawFactAdapter):
    FOCUS_SET = re.compile(r"^Focus\((\w+)\)\s*=\s*\{(\w+)\s*,\s*(\w+)\}$")
    ONE_FOCUS = re.compile(
        r"^OneOf\(Focus\((\w+)\)\)\s*=\s*(\w+)$"
    )
    ONE_ASYMPTOTE = re.compile(
        r"^OneOf\(Asymptote\((\w+)\)\)\s*=\s*(\w+)$"
    )
    ECCENTRICITY = re.compile(r"^Eccentricity\((\w+)\)\s*=\s*(.+)$")
    FOCAL_LENGTH = re.compile(r"^FocalLength\((\w+)\)\s*=\s*(.+)$")
    FOCUS_DIRECTRIX_DISTANCE = re.compile(
        r"^Distance\(Focus\((\w+)\),\s*Directrix\(\1\)\)\s*=\s*(.+)$"
    )
    AXIS_LENGTH = re.compile(
        r"^Length\((MajorAxis|MinorAxis|RealAxis|ImageinaryAxis)"
        r"\((\w+)\)\)\s*=\s*(.+)$"
    )
    AXIS_LENGTH_RELATION = re.compile(
        r"^(?:(.+?)\s*\*\s*)?"
        r"Length\((MajorAxis|MinorAxis|RealAxis|ImageinaryAxis)\((\w+)\)\)"
        r"\s*=\s*"
        r"(?:(.+?)\s*\*\s*)?"
        r"Length\((MajorAxis|MinorAxis|RealAxis|ImageinaryAxis)\((\w+)\)\)$"
    )
    POINT_ON_ASYMPTOTE = re.compile(
        r"^PointOnCurve\((\w+),\s*(?:OneOf\()?Asymptote\((\w+)\)\)?\)"
        r"(?:\s*=\s*True)?$"
    )
    AXIS_FOCUS = re.compile(r"^PointOnCurve\(Focus\((\w+)\),\s*([xy])Axis\)$")
    SIMPLE_ASSIGNMENT = re.compile(r"^([abcep])\s*=\s*(.+)$")
    SYMBOL_ORDER = re.compile(r"^(\w+)\s*>\s*(\w+)$")
    QUADRANT = re.compile(r"^Quadrant\((\w+)\)\s*=\s*([1-4])$")
    SLOPE = re.compile(r"^Slope\((\w+)\)\s*=\s*(.+)$")
    X_COORDINATE = re.compile(r"^XCoordinate\((\w+)\)\s*=\s*(.+)$")
    Y_COORDINATE = re.compile(r"^YCoordinate\((\w+)\)\s*=\s*(.+)$")
    MIDPOINT = re.compile(r"^MidPoint\(LineSegmentOf\((\w+),\s*(\w+)\)\)\s*=\s*(\w+)$")
    ASYMPTOTE_EXPRESSION = re.compile(
        r"^Expression\(OneOf\(Asymptote\((\w+)\)\)\)\s*=\s*\((.*)\)$"
    )
    ASYMPTOTE_EXPRESSION_GENERIC = re.compile(
        r"^Expression\(Asymptote\((\w+)\)\)\s*=\s*\((.*)\)$"
    )
    ASYMPTOTE_SLOPE = re.compile(
        r"^Slope\(OneOf\(Asymptote\((\w+)\)\)\)\s*=\s*(.+)$"
    )

    PARAMETER_NAMES = {
        "a": "semi_axis_a",
        "b": "semi_axis_b",
        "c": "focal_half_distance",
        "e": "eccentricity",
        "p": "p",
    }

    def adapt(self, fact_expressions: str, query_expressions: str | None = None) -> AdaptationResult:
        base = super().adapt(fact_expressions, query_expressions)
        state = base.state
        remaining: List[str] = []
        extra_errors = list(base.errors)

        for fact in base.unparsed_facts:
            try:
                if self._adapt_extra_fact(state, fact):
                    continue
            except (SyntaxError, ValueError, ZeroDivisionError) as exc:
                extra_errors.append(f"{fact}: {exc}")
            remaining.append(fact)
        return AdaptationResult(state, tuple(remaining), tuple(extra_errors))

    def _adapt_extra_fact(self, state, fact: str) -> bool:
        match = self.QUADRANT.match(fact)
        if match:
            point, quadrant_text = match.groups()
            quadrant = int(quadrant_text)
            state.add_given(
                "CoordinateSignOf",
                point,
                "x",
                value=1 if quadrant in {1, 4} else -1,
                raw_expression=fact,
            )
            state.add_given(
                "CoordinateSignOf",
                point,
                "y",
                value=1 if quadrant in {1, 2} else -1,
                raw_expression=fact,
            )
            return True

        match = self.SYMBOL_ORDER.match(fact)
        if match:
            left = Term("symbol", (match.group(1),))
            right = Term("symbol", (match.group(2),))
            state.add_given("GreaterThan", left, right, value=True)
            state.add_given("OrderConstraint", fact, value=True)
            if state.get("Positive", right) is not None:
                state.add_given("Positive", left, value=True)
            return True

        match = self.FOCUS_SET.match(fact)
        if match:
            curve, first, second = match.groups()
            state.add_given("FocusOf", curve, first, value=True)
            state.add_given("FocusOf", curve, second, value=True)
            return True

        match = self.ONE_FOCUS.match(fact)
        if match:
            curve, point = match.groups()
            if point not in state.symbols:
                state.declare(point, "Point")
            state.add_given(
                "FocusOf", curve, point, value=True, raw_expression=fact
            )
            return True

        match = self.ONE_ASYMPTOTE.match(fact)
        if match:
            curve, line = match.groups()
            if line not in state.symbols:
                state.declare(line, "Line")
            state.add_given(
                "AsymptoteOf", curve, line, value=True, raw_expression=fact
            )
            return True

        match = self.ECCENTRICITY.match(fact)
        if match:
            curve, value = match.groups()
            parsed = self._scalar(value)
            if isinstance(parsed, Term) and parsed.operator == "symbol":
                state.add_given("ParameterAlias", parsed.arguments[0], value=(curve, "eccentricity"))
            else:
                state.add_given("ParameterOf", curve, "eccentricity", value=parsed)
            return True

        match = self.FOCUS_DIRECTRIX_DISTANCE.match(fact)
        if match:
            curve, value_text = match.groups()
            state.add_given(
                "FocusDirectrixDistanceOf",
                curve,
                value=self._scalar(value_text),
            )
            return True

        match = self.AXIS_LENGTH_RELATION.match(fact)
        if match:
            (
                left_scale_text,
                left_kind,
                left_curve,
                right_scale_text,
                right_kind,
                right_curve,
            ) = match.groups()
            if left_curve != right_curve:
                return False
            left_scale = self._scalar(left_scale_text or "1")
            right_scale = self._scalar(right_scale_text or "1")
            state.add_given(
                "AxisLengthRatioOf",
                left_curve,
                left_kind,
                right_kind,
                value=div(right_scale, left_scale),
                raw_expression=fact,
            )
            return True

        match = self.AXIS_LENGTH.match(fact)
        if match:
            kind, curve, value_text = match.groups()
            value = div(self._scalar(value_text), 2)
            short_name = "a" if kind in {"MajorAxis", "RealAxis"} else "b"
            parameter_name = self.PARAMETER_NAMES[short_name]
            state.add_given("ParameterOf", curve, parameter_name, value=value)
            state.add_given(
                "ParameterOf",
                curve,
                f"{parameter_name}_squared",
                value=square(value),
            )
            if short_name in state.symbols:
                state.add_given("SymbolValueOf", short_name, value=value)
                state.add_given(
                    "ParameterAlias",
                    short_name,
                    value=(curve, parameter_name),
                )
            return True

        match = self.FOCAL_LENGTH.match(fact)
        if match:
            curve, value = match.groups()
            focal_length = self._scalar(value)
            half = div(focal_length, 2)
            state.add_given("ParameterOf", curve, "focal_half_distance", value=half)
            state.add_given("ParameterOf", curve, "focal_half_distance_squared", value=square(half))
            return True

        match = self.POINT_ON_ASYMPTOTE.match(fact)
        if match:
            point, curve = match.groups()
            state.add_given(
                "PointOnAsymptoteOf",
                curve,
                point,
                value=True,
                raw_expression=fact,
            )
            return True
        match = self.AXIS_FOCUS.match(fact)
        if match:
            curve, axis = match.groups()
            state.add_given("AxisOrientationOf", curve, value="horizontal" if axis == "x" else "vertical")
            return True

        match = self.SLOPE.match(fact)
        if match:
            line, value = match.groups()
            state.add_given("SlopeOf", line, value=self._scalar(value))
            return True

        match = self.X_COORDINATE.match(fact)
        if match:
            point, value = match.groups()
            state.add_given("XCoordinateOf", point, value=self._scalar(value))
            return True

        match = self.Y_COORDINATE.match(fact)
        if match:
            point, value = match.groups()
            state.add_given("YCoordinateOf", point, value=self._scalar(value))
            return True

        match = self.MIDPOINT.match(fact)
        if match:
            first, second, midpoint = match.groups()
            state.add_given("MidPointOf", first, second, value=midpoint)
            return True

        match = (
            self.ASYMPTOTE_EXPRESSION.match(fact)
            or self.ASYMPTOTE_EXPRESSION_GENERIC.match(fact)
        )
        if match:
            curve, expression = match.groups()
            expression = expression.replace("±", "pm").replace("pm", "1")
            polynomial = self.expression_parser.parse_equation(expression)
            if polynomial.x2 != 0 or polynomial.y2 != 0 or polynomial.xy != 0:
                return False
            if polynomial.y == 0:
                return False
            line = f"{curve}__given_asymptote"
            if line not in state.symbols:
                state.declare(line, "Line")
            slope = div(neg(polynomial.x), polynomial.y)
            state.add_given("AsymptoteOf", curve, line, value=True)
            state.add_given("SlopeOf", line, value=slope)
            return True

        match = self.ASYMPTOTE_SLOPE.match(fact)
        if match:
            curve, slope_text = match.groups()
            line = f"{curve}__given_asymptote"
            if line not in state.symbols:
                state.declare(line, "Line")
            state.add_given("AsymptoteOf", curve, line, value=True)
            state.add_given("SlopeOf", line, value=self._scalar(slope_text))
            return True

        match = self.SIMPLE_ASSIGNMENT.match(fact)
        if match:
            short_name, value_text = match.groups()
            conics = [
                symbol.name
                for symbol in state.symbols.values()
                if symbol.type_name in {"Ellipse", "Hyperbola", "Parabola"}
            ]
            if len(conics) != 1:
                return False
            value = self._scalar(value_text)
            parameter_name = self.PARAMETER_NAMES[short_name]
            state.add_given("SymbolValueOf", short_name, value=value)
            if sign(value) == 1:
                state.add_given(
                    "Positive", Term("symbol", (short_name,)), value=True
                )
            state.add_given(
                "ParameterAlias",
                short_name,
                value=(conics[0], parameter_name),
            )
            return True

        return False

    def _scalar(self, text: str) -> Any:
        node = ast.parse(text.strip().replace("^", "**"), mode="eval").body
        polynomial = self.expression_parser._visit(node)
        value = polynomial.scalar_value()
        if value is None:
            raise ValueError("expected scalar expression")
        return value
