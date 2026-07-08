"""Compile structured coordinate and vector conditions into exact equations."""

from __future__ import annotations

import re
from typing import Iterable, Optional, Tuple

from .expressions import ConservativeSolver, equation, is_number, mul, neg, square, sub
from .resolution import StateExpressionResolver
from .schema import Fact, Provenance, StandardConicForm, Term
from .structured_schema import Point2D


class CoordinateEquationCompiler:
    """Lower high-confidence analytic-geometry conditions to EquationConstraint."""

    def __init__(self, solver=None):
        self.solver = solver or ConservativeSolver()

    def enrich(self, source):
        state = source.clone()
        self._materialize_coordinate_variables(state)
        self._right_angles(state)
        self._line_relations(state)
        self._midpoints(state)
        self._distances(state)
        self._distance_ratios(state)
        self._dot_products(state)
        self._vector_scales(state)
        self._vector_linear_relations(state)
        self._points_on_lines(state)
        self._points_on_conics(state)
        return state

    def _materialize_coordinate_variables(self, state):
        for point in sorted(self._participating_points(state)):
            if state.get("PointPositionOf", point) is not None:
                continue
            if not state.has_type(point, "Point") or self._is_semantic_point(state, point):
                continue
            x = state.value("XCoordinateOf", point)
            y = state.value("YCoordinateOf", point)
            if x is None:
                x = self._coordinate_symbol(state, point, "x")
            if y is None:
                y = self._coordinate_symbol(state, point, "y")
            state.add_given(
                "PointPositionOf",
                point,
                value=Point2D(x, y),
                provenance=Provenance("compiler", "coordinate_variables"),
            )

    def _participating_points(self, state):
        points = set()
        for predicate in (
            "RightAngleOf",
            "RequestedDistanceOf",
            "DistanceRatioOf",
            "RequestedDotProductOf",
            "VectorScaleRelation",
        ):
            for fact in state.find(predicate):
                points.update(
                    value
                    for value in fact.arguments
                    if isinstance(value, str) and state.has_type(value, "Point")
                )
        for fact in state.find("MidPointOf"):
            points.update(
                value
                for value in fact.arguments
                if isinstance(value, str) and state.has_type(value, "Point")
            )
        for fact in state.find("VectorLinearRelation"):
            for start, end, _ in fact.value or ():
                if state.has_type(start, "Point"):
                    points.add(start)
                if state.has_type(end, "Point"):
                    points.add(end)
        for fact in state.find("PointOnCurve"):
            if fact.arguments and state.has_type(fact.arguments[0], "Point"):
                points.add(fact.arguments[0])
            if len(fact.arguments) == 2:
                endpoints = self._line_endpoints(state, fact.arguments[1])
                if endpoints is not None:
                    points.update(endpoints[:2])
        for predicate in ("PerpendicularOf", "ParallelOf"):
            for fact in state.find(predicate):
                for line in fact.arguments:
                    endpoints = self._line_endpoints(state, line)
                    if endpoints is not None:
                        points.update(endpoints[:2])
        return points

    @staticmethod
    def _is_semantic_point(state, point):
        for fact in state.find("FocusOf"):
            if len(fact.arguments) == 2 and fact.arguments[1] == point:
                return True
        for fact in state.find("VertexSideOf"):
            if len(fact.arguments) == 2 and fact.arguments[1] == point:
                return True
        for fact in state.find("CenterPointOf"):
            if len(fact.arguments) == 2 and fact.arguments[1] == point:
                return True
        for predicate in (
            "MidPointOf",
            "FootPointOf",
            "TangentPointOf",
            "ChordMidpointOf",
        ):
            for fact in state.find(predicate):
                if fact.value == point:
                    return True
        for fact in state.find("IntersectionOf"):
            targets = fact.value if isinstance(fact.value, tuple) else (fact.value,)
            if point in targets:
                return True
        return False

    @staticmethod
    def _coordinate_symbol(state, point, axis):
        safe_point = re.sub(r"[^A-Za-z0-9_]+", "_", point)
        name = f"__coord_{safe_point}_{axis}"
        if name not in state.symbols:
            state.declare(
                name,
                "Number",
                provenance=Provenance("compiler", "coordinate_variables"),
            )
        target = Term("symbol", (name,))
        sign = state.value("CoordinateSignOf", point, axis)
        if sign == 1 and state.get("Positive", target) is None:
            state.add_given(
                "Positive",
                target,
                value=True,
                provenance=Provenance("compiler", "coordinate_sign"),
            )
        elif sign == -1 and state.get("Negative", target) is None:
            state.add_given(
                "Negative",
                target,
                value=True,
                provenance=Provenance("compiler", "coordinate_sign"),
            )
        return target

    def _right_angles(self, state):
        for relation in state.find("RightAngleOf"):
            if len(relation.arguments) != 3:
                continue
            first, vertex, third = relation.arguments
            positions = self._positions(state, first, vertex, third)
            if positions is None:
                continue
            p1, pv, p3 = positions
            dot = self._dot(
                (sub(p1.x, pv.x), sub(p1.y, pv.y)),
                (sub(p3.x, pv.x), sub(p3.y, pv.y)),
            )
            self._add_equation(state, "right_angle", relation, "dot", dot, 0)

    def _line_relations(self, state):
        for predicate, rule, mode in (
            ("PerpendicularOf", "perpendicular", "dot"),
            ("ParallelOf", "parallel", "cross"),
        ):
            for relation in state.find(predicate):
                if len(relation.arguments) != 2:
                    continue
                first = self._line_direction(state, relation.arguments[0])
                second = self._line_direction(state, relation.arguments[1])
                if first is None or second is None:
                    continue
                first_vector, first_evidence = first
                second_vector, second_evidence = second
                expression = (
                    self._dot(first_vector, second_vector)
                    if mode == "dot"
                    else self._cross(first_vector, second_vector)
                )
                self._add_equation(
                    state,
                    rule,
                    relation,
                    mode,
                    expression,
                    0,
                    extra_evidence=first_evidence + second_evidence,
                )

    def _midpoints(self, state):
        for relation in state.find("MidPointOf"):
            if len(relation.arguments) != 2:
                continue
            first, second = relation.arguments
            midpoint = relation.value
            positions = self._positions(state, first, second, midpoint)
            if positions is None:
                continue
            p1, p2, pm = positions
            self._add_equation(
                state,
                "midpoint",
                relation,
                "x",
                mul(2, pm.x),
                self.solver.add(p1.x, p2.x),
            )
            self._add_equation(
                state,
                "midpoint",
                relation,
                "y",
                mul(2, pm.y),
                self.solver.add(p1.y, p2.y),
            )

    def _distances(self, state):
        for relation in state.find("RequestedDistanceOf"):
            if len(relation.arguments) != 2:
                continue
            first, second = relation.arguments
            positions = self._positions(state, first, second)
            if positions is None:
                continue
            p1, p2 = positions
            squared_distance = self.solver.add(
                square(sub(p2.x, p1.x)),
                square(sub(p2.y, p1.y)),
            )
            self._add_equation(
                state,
                "point_distance",
                relation,
                "squared",
                square(relation.value),
                squared_distance,
            )

    def _distance_ratios(self, state):
        for relation in state.find("DistanceRatioOf"):
            if len(relation.arguments) != 4:
                continue
            a, b, c, d = relation.arguments
            positions = self._positions(state, a, b, c, d)
            if positions is None:
                continue
            pa, pb, pc, pd = positions
            left_squared = self.solver.add(
                square(sub(pb.x, pa.x)),
                square(sub(pb.y, pa.y)),
            )
            right_squared = self.solver.add(
                square(sub(pd.x, pc.x)),
                square(sub(pd.y, pc.y)),
            )
            self._add_equation(
                state,
                "distance_ratio",
                relation,
                "squared",
                left_squared,
                mul(square(relation.value), right_squared),
            )

    def _dot_products(self, state):
        for relation in state.find("RequestedDotProductOf"):
            if len(relation.arguments) != 4:
                continue
            a, b, c, d = relation.arguments
            positions = self._positions(state, a, b, c, d)
            if positions is None:
                continue
            pa, pb, pc, pd = positions
            dot = self._dot(
                (sub(pb.x, pa.x), sub(pb.y, pa.y)),
                (sub(pd.x, pc.x), sub(pd.y, pc.y)),
            )
            self._add_equation(
                state,
                "dot_product",
                relation,
                "value",
                dot,
                relation.value,
            )

    def _vector_scales(self, state):
        for relation in state.find("VectorScaleRelation"):
            if len(relation.arguments) != 4:
                continue
            a, b, c, d = relation.arguments
            positions = self._positions(state, a, b, c, d)
            if positions is None:
                continue
            pa, pb, pc, pd = positions
            left = (sub(pb.x, pa.x), sub(pb.y, pa.y))
            right = (sub(pd.x, pc.x), sub(pd.y, pc.y))
            for axis, left_value, right_value in zip(("x", "y"), left, right):
                self._add_equation(
                    state,
                    "vector_scale",
                    relation,
                    axis,
                    left_value,
                    mul(relation.value, right_value),
                )

    def _vector_linear_relations(self, state):
        for relation in state.find("VectorLinearRelation"):
            terms = relation.value
            if not isinstance(terms, tuple) or not terms:
                continue
            points = []
            for start, end, _ in terms:
                points.extend((start, end))
            positions = self._positions(state, *points)
            if positions is None:
                continue
            position_by_name = dict(zip(points, positions))
            for axis in ("x", "y"):
                expression = 0
                for start, end, coefficient in terms:
                    first = getattr(position_by_name[start], axis)
                    second = getattr(position_by_name[end], axis)
                    expression = self.solver.add(
                        expression,
                        mul(coefficient, sub(second, first)),
                    )
                self._add_equation(
                    state,
                    "vector_linear_relation",
                    relation,
                    axis,
                    expression,
                    0,
                )

    def _points_on_lines(self, state):
        for relation in state.find("PointOnCurve"):
            if len(relation.arguments) != 2:
                continue
            point, line = relation.arguments
            endpoints = self._line_endpoints(state, line)
            if endpoints is None:
                continue
            first, second, endpoint_fact = endpoints
            positions = self._positions(state, point, first, second)
            if positions is None:
                continue
            pp, p1, p2 = positions
            determinant = self._cross(
                (sub(pp.x, p1.x), sub(pp.y, p1.y)),
                (sub(p2.x, p1.x), sub(p2.y, p1.y)),
            )
            self._add_equation(
                state,
                "point_on_line",
                relation,
                "determinant",
                determinant,
                0,
                extra_evidence=(endpoint_fact,),
            )

    def _points_on_conics(self, state):
        resolver = StateExpressionResolver(state, self.solver)
        for relation in state.find("PointOnCurve"):
            if len(relation.arguments) != 2:
                continue
            point, curve = relation.arguments
            form = state.value("ConicStandardForm", curve)
            position = state.value("PointPositionOf", point)
            if not isinstance(form, StandardConicForm) or not isinstance(
                position, Point2D
            ):
                continue
            form = resolver.resolve(form)
            position = resolver.resolve(position)
            x, y = position.x, position.y
            if form.curve_type == "parabola":
                if form.orientation in {"right", "left"}:
                    left = square(y)
                    right = mul(form.two_p, x)
                    self._add_axis_sign(
                        state,
                        x,
                        nonnegative=form.orientation == "right",
                    )
                else:
                    left = square(x)
                    right = mul(form.two_p, y)
                    self._add_axis_sign(
                        state,
                        y,
                        nonnegative=form.orientation == "up",
                    )
            elif (
                form.curve_type in {"ellipse", "hyperbola"}
                and is_number(form.a2)
                and is_number(form.b2)
            ):
                a2, b2 = form.a2, form.b2
                if form.curve_type == "ellipse":
                    if form.orientation == "horizontal":
                        left = self.solver.add(
                            mul(b2, square(x)),
                            mul(a2, square(y)),
                        )
                    else:
                        left = self.solver.add(
                            mul(a2, square(x)),
                            mul(b2, square(y)),
                        )
                elif form.orientation == "horizontal":
                    left = self.solver.add(
                        mul(b2, square(x)),
                        neg(mul(a2, square(y))),
                    )
                else:
                    left = self.solver.add(
                        mul(b2, square(y)),
                        neg(mul(a2, square(x))),
                    )
                right = mul(a2, b2)
            else:
                continue
            self._add_equation(
                state,
                "point_on_conic",
                relation,
                "membership",
                left,
                right,
            )

    @staticmethod
    def _add_axis_sign(state, value, nonnegative):
        if not isinstance(value, Term) or value.operator != "symbol":
            return
        predicate = "NonNegative" if nonnegative else "NonPositive"
        if state.get(predicate, value) is None:
            state.add_given(
                predicate,
                value,
                value=True,
                provenance=Provenance("compiler", "conic_axis_sign"),
            )

    def _positions(self, state, *points) -> Optional[Tuple[Point2D, ...]]:
        resolver = StateExpressionResolver(state, self.solver)
        positions = []
        for point in points:
            value = state.value("PointPositionOf", point)
            if not isinstance(value, Point2D):
                return None
            positions.append(resolver.resolve(value))
        return tuple(positions)

    def _line_direction(self, state, raw_line):
        endpoints = self._line_endpoints(state, raw_line)
        if endpoints is None:
            return None
        first, second, endpoint_fact = endpoints
        positions = self._positions(state, first, second)
        if positions is None:
            return None
        p1, p2 = positions
        return (
            (sub(p2.x, p1.x), sub(p2.y, p1.y)),
            (endpoint_fact,),
        )

    @staticmethod
    def _canonical_line(raw_line):
        return re.sub(r",s*", ",", str(raw_line).strip())

    def _line_endpoints(self, state, raw_line):
        line = self._canonical_line(raw_line)
        fact = state.get("EndpointsOf", line)
        if fact is None or not isinstance(fact.value, tuple) or len(fact.value) != 2:
            return None
        return fact.value[0], fact.value[1], fact

    def _add_equation(
        self,
        state,
        rule,
        source,
        component,
        left,
        right,
        extra_evidence: Iterable[Fact] = (),
    ):
        if self.solver.equivalent(left, right):
            return
        relation = equation(left, right)
        evidence = (source, *tuple(extra_evidence))
        evidence_ids = tuple(
            fact.fact_id for fact in evidence if fact.fact_id is not None
        )
        provenance = Provenance("compiler", rule, evidence_ids)
        if state.get("EquationConstraint", relation) is None:
            state.add_given(
                "EquationConstraint",
                relation,
                value=None,
                provenance=provenance,
            )
        source_id = source.fact_id or repr(source.slot_key)
        if state.get("CompiledCoordinateEquation", source_id, rule, component) is None:
            state.add_given(
                "CompiledCoordinateEquation",
                source_id,
                rule,
                component,
                value=relation,
                provenance=provenance,
            )

    def _dot(self, first, second):
        return self.solver.add(
            self._product(first[0], second[0]),
            self._product(first[1], second[1]),
        )

    @staticmethod
    def _product(first, second):
        return square(first) if first == second else mul(first, second)

    def _cross(self, first, second):
        return sub(
            mul(first[0], second[1]),
            mul(first[1], second[0]),
        )
