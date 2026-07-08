"""Fourth-stage adapter for constructed points and nested geometry objects."""

from __future__ import annotations

import re
from typing import List

from .raw_adapter import AdaptationResult
from .structured_raw_adapter import StructuredRawFactAdapter


class GeometryRawFactAdapter(StructuredRawFactAdapter):
    VERTEX = re.compile(
        r"^(LeftVertex|RightVertex|UpperVertex|LowerVertex|Vertex)"
        r"\((\w+)\)\s*=\s*(\{.*\}|\w+)$"
    )
    FOCUS_SIDE = re.compile(
        r"(LeftFocus|RightFocus)\((\w+)\)\s*=\s*(\w+)"
    )
    CENTER = re.compile(r"^Center\((\w+)\)\s*=\s*(\w+)$")
    ASYMPTOTES = re.compile(r"^Asymptote\((\w+)\)\s*=\s*\{(.*)\}$")
    NESTED_POINT_ON = re.compile(
        r"^PointOnCurve\((\w+),\s*((?:LineOf|LineSegmentOf)"
        r"\(\w+,\s*\w+\))\)(?:\s*=\s*True)?$"
    )
    GENERIC_POINT_ON = re.compile(
        r"^PointOnCurve\((.*)\)(?:\s*=\s*True)?$"
    )
    GENERIC_DISTANCE = re.compile(r"^Distance\((.*)\)\s*=\s*(.+)$")
    GENERIC_SEGMENT_DISTANCE = re.compile(
        r"^Abs\(LineSegmentOf\((.*)\)\)\s*=\s*(.+)$"
    )
    SEMANTIC_POINT = re.compile(
        r"^(Center|Focus|LeftFocus|RightFocus|UpperFocus|LowerFocus)"
        r"\((\w+)\)$"
    )
    FOOT_POINT = re.compile(
        r"^FootPoint\((.*)\)\s*=\s*(\w+)$"
    )
    CHORD = re.compile(
        r"^IsChordOf\(LineSegmentOf\((\w+),\s*(\w+)\),\s*(\w+)\)$"
    )
    CHORD_MIDPOINT = re.compile(
        r"^MidPoint\(InterceptChord\((.*)\)\)\s*=\s*(\w+)$"
    )
    AREA = re.compile(
        r"^Area\(TriangleOf\((\w+),\s*(\w+),\s*(\w+)\)\)"
        r"\s*=\s*(.+)$"
    )
    ANGLE = re.compile(
        r"^AngleOf\((\w+),\s*(\w+),\s*(\w+)\)\s*=\s*(.+)$"
    )
    PERPENDICULAR = re.compile(r"^IsPerpendicular\((.*)\)(?:\s*=\s*True)?$")
    PARALLEL = re.compile(r"^IsParallel\((.*)\)(?:\s*=\s*True)?$")
    LINE_REF = re.compile(
        r"(LineOf|LineSegmentOf)\((\w+),\s*(\w+)\)"
    )
    TRIANGLE_REF = re.compile(
        r"TriangleOf\((\w+),\s*(\w+),\s*(\w+)\)"
    )

    def adapt(
        self,
        fact_expressions: str,
        query_expressions: str | None = None,
    ) -> AdaptationResult:
        base = super().adapt(fact_expressions, query_expressions)
        state = base.state
        self._materialize_nested_objects(state, fact_expressions)

        remaining: List[str] = []
        errors = list(base.errors)
        for fact in base.unparsed_facts:
            try:
                if self._adapt_geometry_fact(state, fact):
                    continue
            except (SyntaxError, ValueError, ZeroDivisionError) as exc:
                errors.append(f"{fact}: {exc}")
            remaining.append(fact)
        return AdaptationResult(state, tuple(remaining), tuple(errors))

    def _materialize_nested_objects(self, state, text: str) -> None:
        for relation, curve, point in self.FOCUS_SIDE.findall(text):
            state.add_given(
                "FocusSideOf",
                curve,
                point,
                value="left" if relation == "LeftFocus" else "right",
            )

        for kind, first, second in self.LINE_REF.findall(text):
            name = f"{kind}({first},{second})"
            type_name = "Line" if kind == "LineOf" else "LineSegment"
            if name not in state.symbols:
                state.declare(name, type_name)
            state.add_given("EndpointsOf", name, value=(first, second))

        for first, second, third in self.TRIANGLE_REF.findall(text):
            name = f"TriangleOf({first},{second},{third})"
            if name not in state.symbols:
                state.declare(name, "Triangle")
            state.add_given(
                "TriangleVerticesOf",
                name,
                value=(first, second, third),
            )

        for symbol in list(state.symbols.values()):
            if symbol.type_name == "Origin":
                state.add_given("OriginPoint", symbol.name, value=True)

    def _adapt_geometry_fact(self, state, fact: str) -> bool:
        match = self.VERTEX.match(fact)
        if match:
            relation, curve, target_text = match.groups()
            side = relation.removesuffix("Vertex").lower() or "unspecified"
            for target in self._parse_targets(target_text):
                state.add_given(
                    "VertexSideOf",
                    curve,
                    target,
                    value=side,
                    raw_expression=fact,
                )
            return True

        match = self.CENTER.match(fact)
        if match:
            curve, point = match.groups()
            state.add_given(
                "CenterPointOf", curve, point, value=True, raw_expression=fact
            )
            return True

        match = self.ASYMPTOTES.match(fact)
        if match:
            curve, targets = match.groups()
            for line in self._parse_targets("{" + targets + "}"):
                state.add_given(
                    "AsymptoteOf",
                    curve,
                    line,
                    value=True,
                    raw_expression=fact,
                )
            return True

        match = self.NESTED_POINT_ON.match(fact)
        if match:
            point, raw_line = match.groups()
            line = re.sub(r",\s*", ",", raw_line)
            state.add_given(
                "PointOnCurve", point, line, value=True, raw_expression=fact
            )
            return True

        match = self.GENERIC_POINT_ON.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2 or not re.fullmatch(r"\w+", operands[1]):
                return False
            point = self._semantic_point_reference(state, operands[0], fact)
            if point is None:
                return False
            state.add_given(
                "PointOnCurve",
                point,
                operands[1],
                value=True,
                raw_expression=fact,
            )
            return True

        match = self.GENERIC_DISTANCE.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            if not any(self._is_semantic_point_text(item) for item in operands):
                return False
            first = self._point_reference(state, operands[0], fact)
            second = self._point_reference(state, operands[1], fact)
            if first is None or second is None:
                return False
            predicate = (
                "RequestedPointLineDistanceOf"
                if state.has_type(second, "Line")
                else "RequestedDistanceOf"
            )
            state.add_given(
                predicate,
                first,
                second,
                value=self._scalar(match.group(2)),
                raw_expression=fact,
            )
            return True

        match = self.GENERIC_SEGMENT_DISTANCE.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            if not any(self._is_semantic_point_text(item) for item in operands):
                return False
            first = self._point_reference(state, operands[0], fact)
            second = self._point_reference(state, operands[1], fact)
            if first is None or second is None:
                return False
            state.add_given(
                "RequestedDistanceOf",
                first,
                second,
                value=self._scalar(match.group(2)),
                raw_expression=fact,
            )
            return True

        match = self.FOOT_POINT.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            state.add_given(
                "FootPointOf",
                operands[0],
                operands[1],
                value=match.group(2),
                raw_expression=fact,
            )
            return True

        match = self.CHORD.match(fact)
        if match:
            first, second, curve = match.groups()
            state.add_given(
                "ChordOf", first, second, curve, value=True, raw_expression=fact
            )
            return True

        match = self.CHORD_MIDPOINT.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            state.add_given(
                "ChordMidpointOf",
                operands[0],
                operands[1],
                value=match.group(2),
                raw_expression=fact,
            )
            return True

        match = self.AREA.match(fact)
        if match:
            first, second, third, target = match.groups()
            state.add_given(
                "RequestedAreaOf",
                first,
                second,
                third,
                value=self._scalar(target),
                raw_expression=fact,
            )
            return True

        match = self.ANGLE.match(fact)
        if match:
            first, vertex, third, target = match.groups()
            state.add_given(
                "AngleValueOf",
                first,
                vertex,
                third,
                value=self._scalar(target),
                raw_expression=fact,
            )
            normalized = re.sub(r"\s+", "", target)
            if normalized in {"pi/2", "ApplyUnit(90,degree)"}:
                state.add_given(
                    "RightAngleOf",
                    first,
                    vertex,
                    third,
                    value=True,
                    raw_expression=fact,
                )
            return True

        match = self.PARALLEL.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            state.add_given(
                "ParallelOf",
                operands[0],
                operands[1],
                value=True,
                raw_expression=fact,
            )
            return True

        match = self.PERPENDICULAR.match(fact)
        if match:
            operands = self._split_top_level(match.group(1))
            if len(operands) != 2:
                return False
            state.add_given(
                "PerpendicularOf",
                operands[0],
                operands[1],
                value=True,
                raw_expression=fact,
            )
            return True

        return False

    def _point_reference(self, state, raw: str, source: str):
        raw = re.sub(r"\s+", "", raw)
        if state.has_type(raw, "Point") or state.has_type(raw, "Origin"):
            return raw
        return self._semantic_point_reference(state, raw, source)

    def _is_semantic_point_text(self, raw: str) -> bool:
        return self.SEMANTIC_POINT.match(re.sub(r"\s+", "", raw)) is not None

    def _semantic_point_reference(self, state, raw: str, source: str):
        raw = re.sub(r"\s+", "", raw)
        match = self.SEMANTIC_POINT.match(raw)
        if match is None:
            return None
        kind, curve = match.groups()
        if curve not in state.symbols:
            return None
        if raw not in state.symbols:
            state.declare(raw, "Point")
        if kind == "Center":
            state.add_given(
                "CenterPointOf",
                curve,
                raw,
                value=True,
                raw_expression=source,
            )
            return raw
        state.add_given(
            "FocusOf",
            curve,
            raw,
            value=True,
            raw_expression=source,
        )
        side = {
            "LeftFocus": "left",
            "RightFocus": "right",
            "UpperFocus": "upper",
            "LowerFocus": "lower",
        }.get(kind)
        if side is not None:
            state.add_given(
                "FocusSideOf",
                curve,
                raw,
                value=side,
                raw_expression=source,
            )
        return raw
