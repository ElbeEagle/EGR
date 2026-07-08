"""Deterministic coordinate closure for constructed geometry objects."""

from __future__ import annotations

from dataclasses import replace
from typing import Optional

from .applicator import ApplicatorV2
from .expressions import ConservativeSolver, is_zero, mul, neg, sqrt_positive, sub
from .schema import ApplicationResult, Provenance, StandardConicForm, Term
from .structured_schema import LineEquation, Point2D


class GeometryClosure:
    def __init__(self, solver: Optional[ConservativeSolver] = None):
        self.solver = solver or ConservativeSolver()

    def enrich(self, source):
        state = source.clone()
        for _ in range(4):
            before = len(state.facts)
            self._origins(state)
            self._named_conic_points(state)
            self._midpoints(state)
            self._lines_from_point_slope(state)
            self._lines_from_endpoints(state)
            self._line_intersections(state)
            if len(state.facts) == before:
                break
        return state

    @staticmethod
    def _add(state, predicate, *arguments, value):
        if state.get(predicate, *arguments) is None:
            state.add_given(
                predicate,
                *arguments,
                value=value,
                provenance=Provenance.given("geometry_closure"),
            )

    def _origins(self, state):
        for marker in state.find("OriginPoint"):
            point = marker.arguments[0]
            self._add(
                state,
                "PointPositionOf",
                point,
                value=Point2D(0, 0),
            )

    def _named_conic_points(self, state):
        for center in state.find("CenterPointOf"):
            curve, point = center.arguments
            coordinate = state.value("CenterCoordinateOf", curve)
            if coordinate is None:
                circle_form = state.value("CircleStandardForm", curve)
                if isinstance(circle_form, tuple) and len(circle_form) == 3:
                    coordinate = circle_form[:2]
            if coordinate is None:
                conic_form = state.value("ConicStandardForm", curve)
                if isinstance(conic_form, StandardConicForm):
                    coordinate = (0, 0)
            if coordinate is None:
                continue
            self._add(
                state,
                "PointPositionOf",
                point,
                value=Point2D(coordinate[0], coordinate[1]),
            )

        for focus in state.find("FocusOf"):
            curve, point = focus.arguments
            form = state.value("ConicStandardForm", curve)
            if not isinstance(form, StandardConicForm):
                continue
            side = state.value("FocusSideOf", curve, point)
            coordinate = self._focus_coordinate(state, curve, point, form, side)
            if coordinate is not None:
                self._add(
                    state,
                    "PointPositionOf",
                    point,
                    value=coordinate,
                )

        for vertex in state.find("VertexSideOf"):
            curve, point = vertex.arguments
            form = state.value("ConicStandardForm", curve)
            if not isinstance(form, StandardConicForm):
                continue
            coordinate = self._vertex_coordinate(
                state, curve, form, vertex.value
            )
            if coordinate is not None:
                self._add(
                    state,
                    "PointPositionOf",
                    point,
                    value=coordinate,
                )

    def _lines_from_point_slope(self, state):
        for slope_fact in state.find("SlopeOf"):
            if len(slope_fact.arguments) != 1:
                continue
            line = slope_fact.arguments[0]
            if not state.has_type(line, "Line"):
                continue
            known_points = []
            for relation in state.find("PointOnCurve"):
                if len(relation.arguments) != 2 or relation.arguments[1] != line:
                    continue
                position = state.value("PointPositionOf", relation.arguments[0])
                if isinstance(position, Point2D):
                    known_points.append(position)
            if len(known_points) != 1:
                continue
            point = known_points[0]
            slope = slope_fact.value
            constant = sub(point.y, mul(slope, point.x))
            self._add(
                state,
                "LineNormalFormOf",
                line,
                value=LineEquation(slope, -1, constant),
            )

    def _focus_coordinate(self, state, curve, point, form, side):
        if form.curve_type == "parabola":
            offset = form.focus_offset
            mapping = {
                "right": Point2D(offset, 0),
                "left": Point2D(neg(offset), 0),
                "up": Point2D(0, offset),
                "down": Point2D(0, neg(offset)),
            }
            return mapping.get(form.orientation)

        offset = state.value(
            "ResolvedParameterOf", curve, "focal_half_distance"
        )
        if offset is None:
            offset = state.value(
                "ParameterOf", curve, "focal_half_distance"
            )
        if offset is None:
            squared = state.value(
                "ResolvedParameterOf",
                curve,
                "focal_half_distance_squared",
            )
            if squared is None:
                squared = state.value(
                    "ParameterOf",
                    curve,
                    "focal_half_distance_squared",
                )
            if squared is not None:
                offset = sqrt_positive(squared)
        if offset is None and form.focus_offset is not None:
            offset = form.focus_offset
        if offset is None:
            if not self._needs_parameter_coordinate(state, point):
                return None
            offset = Term(
                "parameter", (curve, "focal_half_distance")
            )
        if form.orientation == "horizontal":
            if side == "left":
                return Point2D(neg(offset), 0)
            if side == "right":
                return Point2D(offset, 0)
        if form.orientation == "vertical":
            if side in {"left", "lower"}:
                return Point2D(0, neg(offset))
            if side in {"right", "upper"}:
                return Point2D(0, offset)
        return None

    @staticmethod
    def _needs_parameter_coordinate(state, point):
        predicates = (
            "RightAngleOf",
            "MidPointOf",
            "RequestedDistanceOf",
            "RequestedDotProductOf",
            "VectorScaleRelation",
            "PointOnCurve",
        )
        for predicate in predicates:
            for fact in state.find(predicate):
                if point in fact.arguments or fact.value == point:
                    return True
        return False

    @staticmethod
    def _vertex_coordinate(state, curve, form, side):
        a = state.value("ResolvedParameterOf", curve, "semi_axis_a")
        if a is None:
            a = state.value("ParameterOf", curve, "semi_axis_a")
        if a is None:
            a = Term("parameter", (curve, "semi_axis_a"))
        b = state.value("ResolvedParameterOf", curve, "semi_axis_b")
        if b is None:
            b = state.value("ParameterOf", curve, "semi_axis_b")
        if b is None:
            b = Term("parameter", (curve, "semi_axis_b"))
        if form.orientation == "horizontal":
            mapping = {
                "left": Point2D(neg(a), 0),
                "right": Point2D(a, 0),
            }
            if b is not None:
                mapping.update(
                    {
                        "upper": Point2D(0, b),
                        "lower": Point2D(0, neg(b)),
                    }
                )
        else:
            mapping = {
                "upper": Point2D(0, a),
                "lower": Point2D(0, neg(a)),
            }
            if b is not None:
                mapping.update(
                    {
                        "left": Point2D(neg(b), 0),
                        "right": Point2D(b, 0),
                    }
                )
        return mapping.get(side)

    def _midpoints(self, state):
        for relation in state.find("MidPointOf"):
            first, second = relation.arguments
            midpoint = relation.value
            first_position = state.value("PointPositionOf", first)
            second_position = state.value("PointPositionOf", second)
            if not (
                isinstance(first_position, Point2D)
                and isinstance(second_position, Point2D)
            ):
                continue
            coordinate = Point2D(
                self.solver.div(
                    self.solver.add(first_position.x, second_position.x), 2
                ),
                self.solver.div(
                    self.solver.add(first_position.y, second_position.y), 2
                ),
            )
            self._add(
                state,
                "PointPositionOf",
                midpoint,
                value=coordinate,
            )

    def _lines_from_endpoints(self, state):
        for endpoints in state.find("EndpointsOf"):
            line = endpoints.arguments[0]
            if not state.has_type(line, "Line"):
                continue
            first, second = endpoints.value
            p1 = state.value("PointPositionOf", first)
            p2 = state.value("PointPositionOf", second)
            if not isinstance(p1, Point2D) or not isinstance(p2, Point2D):
                continue
            normal = LineEquation(
                sub(p1.y, p2.y),
                sub(p2.x, p1.x),
                sub(mul(p1.x, p2.y), mul(p2.x, p1.y)),
            )
            self._add(state, "LineNormalFormOf", line, value=normal)
            self._add(state, "PointOnCurve", first, line, value=True)
            self._add(state, "PointOnCurve", second, line, value=True)

    def _line_intersections(self, state):
        for relation in state.find("IntersectionOf"):
            if len(relation.arguments) != 2:
                continue
            first, second = relation.arguments
            first_line = state.value("LineNormalFormOf", first)
            second_line = state.value("LineNormalFormOf", second)
            if not (
                isinstance(first_line, LineEquation)
                and isinstance(second_line, LineEquation)
            ):
                continue
            targets = relation.value
            if not isinstance(targets, tuple) or len(targets) != 1:
                continue
            coordinate = self._intersection(first_line, second_line)
            if coordinate is not None:
                self._add(
                    state,
                    "PointPositionOf",
                    targets[0],
                    value=coordinate,
                )

        for relation in state.find("FootPointOf"):
            first, second = relation.arguments
            first_line = state.value("LineNormalFormOf", first)
            second_line = state.value("LineNormalFormOf", second)
            if not (
                isinstance(first_line, LineEquation)
                and isinstance(second_line, LineEquation)
            ):
                continue
            coordinate = self._intersection(first_line, second_line)
            if coordinate is not None:
                self._add(
                    state,
                    "PointPositionOf",
                    relation.value,
                    value=coordinate,
                )

    def _intersection(self, first, second):
        determinant = sub(
            mul(first.a, second.b),
            mul(second.a, first.b),
        )
        if is_zero(determinant):
            return None
        x = self.solver.div(
            sub(mul(first.b, second.c), mul(second.b, first.c)),
            determinant,
        )
        y = self.solver.div(
            sub(mul(first.c, second.a), mul(second.c, first.a)),
            determinant,
        )
        return Point2D(x, y)


class GeometryApplicatorV2(ApplicatorV2):
    def __init__(self, solver=None, closure=None):
        super().__init__(solver)
        self.closure = closure or GeometryClosure(self.solver)

    def apply(self, model, state, binding=None) -> ApplicationResult:
        enriched = self.closure.enrich(state)
        return self.apply_enriched(model, enriched, binding)

    def apply_enriched(self, model, enriched, binding=None) -> ApplicationResult:
        """Apply to a state already normalized by this applicator's closure.

        Macro application evaluates many candidate helpers against the same
        state.  Exposing this narrow fast path avoids recomputing the expensive
        pre-application geometry/elimination closure for every candidate while
        preserving the normal post-application closure and validation rules.
        """
        result = super().apply(model, enriched, binding)
        if result.state_after is None:
            return result
        return replace(
            result,
            state_after=self.closure.enrich(result.state_after),
        )
