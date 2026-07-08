"""Third-stage adapter for algebra, lines, intersections, and vectors."""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from .expressions import div, mul, neg, sign, sub
from .expanded_raw_adapter import ExpandedRawFactAdapter
from .raw_adapter import AdaptationResult
from .schema import PolynomialEquation, Term
from .structured_schema import LineEquation, Point2D, Vector2D


class StructuredRawFactAdapter(ExpandedRawFactAdapter):
    INTERSECTION = re.compile(r"^Intersection\((.*)\)\s*=\s*(\{.*\}|\w+)$")
    NUM_INTERSECTION = re.compile(r"^NumIntersection\((.*)\)\s*=\s*(\d+)$")
    SEGMENT_DISTANCE = re.compile(
        r"^Abs\(LineSegmentOf\((\w+),\s*(\w+)\)\)\s*=\s*(.+)$"
    )
    SEGMENT_DISTANCE_RATIO = re.compile(
        r"^(?:(.+?)\s*\*\s*)?Abs\(LineSegmentOf\((\w+),\s*(\w+)\)\)"
        r"\s*=\s*(?:(.+?)\s*\*\s*)?"
        r"Abs\(LineSegmentOf\((\w+),\s*(\w+)\)\)$"
    )
    DISTANCE = re.compile(r"^Distance\((\w+),\s*(\w+)\)\s*=\s*(.+)$")
    SEGMENT_SLOPE = re.compile(
        r"^Slope\((?:LineSegmentOf|LineOf)\((\w+),\s*(\w+)\)\)\s*=\s*(.+)$"
    )
    VECTOR_RELATION = re.compile(
        r"^VectorOf\((\w+),\s*(\w+)\)\s*=\s*(.+?)\s*\*\s*"
        r"VectorOf\((\w+),\s*(\w+)\)$"
    )
    DOT_PRODUCT = re.compile(
        r"^DotProduct\(VectorOf\((\w+),\s*(\w+)\),\s*"
        r"VectorOf\((\w+),\s*(\w+)\)\)\s*=\s*(.+)$"
    )
    VECTOR_REF = re.compile(r"VectorOf\((\w+),\s*(\w+)\)")

    def adapt(
        self,
        fact_expressions: str,
        query_expressions: str | None = None,
    ) -> AdaptationResult:
        base = super().adapt(fact_expressions, query_expressions)
        state = base.state
        self._derive_structured_values(state)

        remaining: List[str] = []
        errors = list(base.errors)
        for fact in base.unparsed_facts:
            try:
                if self._adapt_structured_fact(state, fact):
                    continue
            except (SyntaxError, ValueError, ZeroDivisionError) as exc:
                errors.append(f"{fact}: {exc}")
            remaining.append(fact)

        for start, end in self.VECTOR_REF.findall(fact_expressions):
            self._ensure_vector(state, start, end)

        return AdaptationResult(state, tuple(remaining), tuple(errors))

    def _derive_structured_values(self, state) -> None:
        for coordinate in list(state.find("CoordinateOf")):
            if len(coordinate.arguments) != 1:
                continue
            raw = coordinate.value
            if not isinstance(raw, tuple) or len(raw) != 2:
                continue
            try:
                point = Point2D(
                    self._scalar(str(raw[0])),
                    self._scalar(str(raw[1])),
                )
            except (SyntaxError, ValueError, ZeroDivisionError):
                continue
            state.add_given(
                "PointPositionOf",
                coordinate.arguments[0],
                value=point,
                raw_expression=coordinate.raw_expression,
            )

        for expression in list(state.find("ExpressionPolynomial")):
            entity = expression.arguments[0]
            polynomial = expression.value
            if not state.has_type(entity, "Line"):
                continue
            if not isinstance(polynomial, PolynomialEquation):
                continue
            if any((polynomial.x2, polynomial.xy, polynomial.y2)):
                continue
            if polynomial.x == 0 and polynomial.y == 0:
                continue
            state.add_given(
                "LineNormalFormOf",
                entity,
                value=LineEquation(
                    polynomial.x, polynomial.y, polynomial.constant
                ),
                raw_expression=expression.raw_expression,
            )

    def _adapt_structured_fact(self, state, fact: str) -> bool:
        match = self.INTERSECTION.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            targets = self._parse_targets(match.group(2))
            state.add_given(
                "IntersectionOf",
                operands[0],
                operands[1],
                value=targets,
                raw_expression=fact,
            )
            return True

        match = self.NUM_INTERSECTION.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            state.add_given(
                "IntersectionCountOf",
                operands[0],
                operands[1],
                value=int(match.group(2)),
                raw_expression=fact,
            )
            return True

        match = self.SEGMENT_DISTANCE_RATIO.match(fact)
        if match:
            left_scale, a, b, right_scale, c, d = match.groups()
            left_scale = self._scalar(left_scale or "1")
            right_scale = self._scalar(right_scale or "1")
            if sign(left_scale) == 1 and sign(right_scale) == 1:
                ratio = div(right_scale, left_scale)
                state.add_given(
                    "DistanceRatioOf",
                    a,
                    b,
                    c,
                    d,
                    value=ratio,
                    raw_expression=fact,
                )
                if state.get("RequestedDistanceOf", a, b) is None:
                    state.add_given(
                        "RequestedDistanceOf",
                        a,
                        b,
                        value=mul(ratio, Term("distance", (c, d))),
                        raw_expression=fact,
                    )
                return True

        match = self.SEGMENT_DISTANCE.match(fact)
        if match:
            first, second, target = match.groups()
            state.add_given(
                "RequestedDistanceOf",
                first,
                second,
                value=self._scalar(target),
                raw_expression=fact,
            )
            return True

        match = self.DISTANCE.match(fact)
        if match:
            first, second, target = match.groups()
            predicate = (
                "RequestedPointLineDistanceOf"
                if state.has_type(second, "Line")
                else "RequestedDistanceOf"
            )
            state.add_given(
                predicate,
                first,
                second,
                value=self._scalar(target),
                raw_expression=fact,
            )
            return True

        match = self.SEGMENT_SLOPE.match(fact)
        if match:
            first, second, target = match.groups()
            state.add_given(
                "RequestedSlopeOf",
                first,
                second,
                value=self._scalar(target),
                raw_expression=fact,
            )
            return True

        match = self.VECTOR_RELATION.match(fact)
        if match:
            a, b, scale, c, d = match.groups()
            state.add_given(
                "VectorScaleRelation",
                a,
                b,
                c,
                d,
                value=self._scalar(scale),
                raw_expression=fact,
            )
            return True

        if "VectorOf(" in fact and "=" in fact:
            left, right = fact.split("=", 1)
            left_terms = self._numeric_vector_terms(left)
            right_terms = self._numeric_vector_terms(right)
            if left_terms is not None and right_terms is not None:
                terms = left_terms + tuple(
                    (start, end, neg(coefficient))
                    for start, end, coefficient in right_terms
                )
                state.add_given(
                    "VectorLinearRelation",
                    fact,
                    value=terms,
                    raw_expression=fact,
                )
                return True

        match = self.DOT_PRODUCT.match(fact)
        if match:
            a, b, c, d, target = match.groups()
            state.add_given(
                "RequestedDotProductOf",
                a,
                b,
                c,
                d,
                value=self._scalar(target),
                raw_expression=fact,
            )
            return True

        return False

    def _numeric_vector_terms(self, expression):
        compact = re.sub(r"\s+", "", expression)
        pieces = compact.replace("-", "+-").split("+")
        terms = []
        pattern = re.compile(
            r"^([+-]?)(?:(.+?)\*)?VectorOf\((\w+),(\w+)\)"
            r"(?:/(.+))?$"
        )
        for piece in pieces:
            if not piece:
                continue
            match = pattern.match(piece)
            if match is None:
                return None
            sign_text, numerator_text, start, end, denominator_text = (
                match.groups()
            )
            try:
                coefficient = self._scalar(numerator_text or "1")
                if denominator_text:
                    coefficient = div(
                        coefficient, self._scalar(denominator_text)
                    )
            except (SyntaxError, ValueError, ZeroDivisionError):
                return None
            if sign_text == "-":
                coefficient = neg(coefficient)
            if sign(coefficient) not in {-1, 1}:
                return None
            terms.append((start, end, coefficient))
        return tuple(terms) if terms else None

    def _ensure_vector(self, state, start: str, end: str) -> None:
        if state.get("VectorOf", start, end) is not None:
            return
        first = state.value("PointPositionOf", start)
        second = state.value("PointPositionOf", end)
        if isinstance(first, Point2D) and isinstance(second, Point2D):
            value = Vector2D(
                sub(second.x, first.x),
                sub(second.y, first.y),
            )
        else:
            value = Term("vector_between", (start, end))
        state.add_given("VectorOf", start, end, value=value)

    @staticmethod
    def _parse_targets(text: str) -> Tuple[str, ...]:
        text = text.strip()
        if text.startswith("{") and text.endswith("}"):
            return tuple(
                item.strip()
                for item in text[1:-1].split(",")
                if item.strip()
            )
        return (text,)

    @staticmethod
    def _split_top_level(text: str) -> Tuple[str, ...]:
        parts = []
        start = 0
        depth = 0
        for index, character in enumerate(text):
            if character in "({[":
                depth += 1
            elif character in ")}]":
                depth -= 1
            elif character == "," and depth == 0:
                parts.append(text[start:index].strip())
                start = index + 1
        parts.append(text[start:].strip())
        return tuple(parts)
