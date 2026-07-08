"""Fifth-stage adapter with canonical quantities and tangent relations."""

from __future__ import annotations

import re
from typing import List

from .expressions import div, neg
from .geometry_raw_adapter import GeometryRawFactAdapter
from .quantity_schema import QuantityRef
from .raw_adapter import AdaptationResult
from .schema import AxisLine


class QuantityRawFactAdapter(GeometryRawFactAdapter):
    LENGTH = re.compile(r"^Length\((.*)\)\s*=\s*(.+)$")
    RADIUS = re.compile(r"^Radius\((\w+)\)\s*=\s*(.+)$")
    INCLINATION = re.compile(r"^Inclination\((\w+)\)\s*=\s*(.+)$")
    TANGENT = re.compile(r"^IsTangent\((.*)\)(?:\s*=\s*True)?$")
    TANGENT_POINT = re.compile(
        r"^TangentPoint\((.*)\)\s*=\s*(\w+)$"
    )
    DIRECTRIX_SIDE = re.compile(
        r"^(LeftDirectrix|RightDirectrix)\((\w+)\)\s*=\s*(\w+)$"
    )
    DIRECTRIX_EXPRESSION = re.compile(
        r"^Expression\(Directrix\((\w+)\)\)\s*=\s*\((.*)\)$"
    )
    INCENTER = re.compile(
        r"^Incenter\(TriangleOf\((\w+),\s*(\w+),\s*(\w+)\)\)"
        r"\s*=\s*(\w+)$"
    )

    def adapt(
        self,
        fact_expressions: str,
        query_expressions: str | None = None,
    ) -> AdaptationResult:
        base = super().adapt(fact_expressions, query_expressions)
        state = base.state
        self._canonicalize_existing_quantities(state)

        remaining: List[str] = []
        errors = list(base.errors)
        for fact in base.unparsed_facts:
            try:
                if self._adapt_quantity_fact(state, fact):
                    continue
            except (SyntaxError, ValueError, ZeroDivisionError) as exc:
                errors.append(f"{fact}: {exc}")
            remaining.append(fact)
        return AdaptationResult(state, tuple(remaining), tuple(errors))

    def _canonicalize_existing_quantities(self, state) -> None:
        mappings = (
            ("RequestedDistanceOf", "distance"),
            ("RequestedPointLineDistanceOf", "point_line_distance"),
            ("RequestedSlopeOf", "slope"),
            ("RequestedDotProductOf", "dot_product"),
            ("RequestedAreaOf", "area"),
        )
        for predicate, kind in mappings:
            for fact in state.find(predicate):
                reference = QuantityRef.of(kind, *fact.arguments)
                if state.get("QuantityValueOf", reference) is None:
                    state.add_given(
                        "QuantityValueOf",
                        reference,
                        value=fact.value,
                        raw_expression=fact.raw_expression,
                    )

    def _adapt_quantity_fact(self, state, fact: str) -> bool:
        match = self.LENGTH.match(fact)
        if match:
            subject, value = match.groups()
            reference = QuantityRef.of("length", subject.strip())
            state.add_given(
                "QuantityValueOf",
                reference,
                value=self._scalar(value),
                raw_expression=fact,
            )
            return True

        match = self.RADIUS.match(fact)
        if match:
            circle, value = match.groups()
            state.add_given(
                "QuantityValueOf",
                QuantityRef.of("radius", circle),
                value=self._scalar(value),
                raw_expression=fact,
            )
            return True

        match = self.INCLINATION.match(fact)
        if match:
            line, value = match.groups()
            state.add_given(
                "QuantityValueOf",
                QuantityRef.of("inclination", line),
                value=self._scalar(value),
                raw_expression=fact,
            )
            return True

        match = self.TANGENT.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            state.add_given(
                "TangentRelation",
                operands[0],
                operands[1],
                value=True,
                raw_expression=fact,
            )
            return True

        match = self.TANGENT_POINT.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            state.add_given(
                "TangentPointOf",
                operands[0],
                operands[1],
                value=match.group(2),
                raw_expression=fact,
            )
            return True

        match = self.DIRECTRIX_SIDE.match(fact)
        if match:
            relation, curve, line = match.groups()
            state.add_given(
                "DirectrixOf", curve, line, value=True, raw_expression=fact
            )
            state.add_given(
                "DirectrixSideOf",
                curve,
                line,
                value="left" if relation == "LeftDirectrix" else "right",
                raw_expression=fact,
            )
            return True

        match = self.DIRECTRIX_EXPRESSION.match(fact)
        if match:
            curve, expression = match.groups()
            polynomial = self.expression_parser.parse_equation(expression)
            if polynomial.x != 0 and polynomial.y == 0:
                axis_line = AxisLine(
                    "x", div(neg(polynomial.constant), polynomial.x)
                )
            elif polynomial.y != 0 and polynomial.x == 0:
                axis_line = AxisLine(
                    "y", div(neg(polynomial.constant), polynomial.y)
                )
            else:
                return False
            state.add_given(
                "GivenDirectrixExpressionOf",
                curve,
                value=axis_line,
                raw_expression=fact,
            )
            return True

        match = self.INCENTER.match(fact)
        if match:
            first, second, third, point = match.groups()
            state.add_given(
                "IncenterOf",
                first,
                second,
                third,
                value=point,
                raw_expression=fact,
            )
            return True

        return False
