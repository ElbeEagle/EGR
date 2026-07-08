"""Quantity propagation plus directrix and tangent-point closure."""

from __future__ import annotations

from .condition_closure import ConicConditionEquationClosure
from .coordinate_equation_compiler import CoordinateEquationCompiler
from .elimination import ExactEliminationClosure
from .expressions import mul, neg, sub
from .geometry_closure import GeometryApplicatorV2, GeometryClosure
from .quantity_schema import QuantityRef
from .schema import AxisLine
from .structured_schema import LineEquation, Point2D


class QuantityGeometryClosure(GeometryClosure):
    def __init__(
        self,
        solver=None,
        elimination=None,
        conditions=None,
        coordinate_compiler=None,
    ):
        super().__init__(solver)
        self.elimination = elimination or ExactEliminationClosure(self.solver)
        self.conditions = conditions or ConicConditionEquationClosure()
        self.coordinate_compiler = (
            coordinate_compiler or CoordinateEquationCompiler(self.solver)
        )

    def enrich(self, source):
        state = super().enrich(source)
        for _ in range(3):
            before = len(state.facts)
            self._directrices(state)
            self._tangent_points(state)
            self._chord_distances(state)
            self._quantities(state)
            if len(state.facts) == before:
                break
        state = self.coordinate_compiler.enrich(state)
        state = self.conditions.enrich(state)
        elimination = self.elimination.close(state)
        return elimination.state

    def _directrices(self, state):
        for relation in state.find("DirectrixOf"):
            curve, line = relation.arguments
            expression = state.value("DirectrixExpressionOf", curve)
            if not isinstance(expression, AxisLine):
                family = state.value("DirectrixFamilyOf", curve)
                side = state.value("DirectrixSideOf", curve, line)
                if isinstance(family, tuple) and side in {"left", "right"}:
                    expression = self._select_directrix(family, side)
            if isinstance(expression, AxisLine):
                self._add(
                    state,
                    "LineNormalFormOf",
                    line,
                    value=self._axis_line(expression),
                )

        for fact in state.find("GivenDirectrixExpressionOf"):
            curve = fact.arguments[0]
            virtual_line = f"Directrix({curve})"
            if virtual_line not in state.symbols:
                state.declare(virtual_line, "Line")
            self._add(
                state,
                "LineNormalFormOf",
                virtual_line,
                value=self._axis_line(fact.value),
            )

        for fact in state.find("DirectrixExpressionOf"):
            curve = fact.arguments[0]
            if not isinstance(fact.value, AxisLine):
                continue
            virtual_line = f"Directrix({curve})"
            if virtual_line not in state.symbols:
                state.declare(virtual_line, "Line")
            if not state.find("DirectrixOf", curve):
                self._add(
                    state,
                    "DirectrixOf",
                    curve,
                    virtual_line,
                    value=True,
                )
            self._add(
                state,
                "LineNormalFormOf",
                virtual_line,
                value=self._axis_line(fact.value),
            )

    @staticmethod
    def _select_directrix(family, side):
        candidates = [
            line
            for line in family
            if isinstance(line, AxisLine)
        ]
        if len(candidates) != 2:
            return None
        if side == "left":
            return candidates[1]
        return candidates[0]

    @staticmethod
    def _axis_line(line):
        if line.axis == "x":
            return LineEquation(1, 0, neg(line.value))
        return LineEquation(0, 1, neg(line.value))

    def _tangent_points(self, state):
        for relation in state.find("TangentPointOf"):
            first, second = relation.arguments
            if state.has_type(first, "Line"):
                line, circle = first, second
            elif state.has_type(second, "Line"):
                line, circle = second, first
            else:
                continue
            line_form = state.value("LineNormalFormOf", line)
            circle_form = state.value("CircleStandardForm", circle)
            if (
                not isinstance(line_form, LineEquation)
                or not isinstance(circle_form, tuple)
                or len(circle_form) != 3
            ):
                continue
            center = Point2D(circle_form[0], circle_form[1])
            point = self._project(center, line_form)
            self._add(
                state,
                "PointPositionOf",
                relation.value,
                value=point,
            )

    def _project(self, point, line):
        denominator = self.solver.add(
            self.solver.square(line.a),
            self.solver.square(line.b),
        )
        numerator = self.solver.add(
            self.solver.mul(line.a, point.x),
            self.solver.mul(line.b, point.y),
            line.c,
        )
        scale = self.solver.div(numerator, denominator)
        return Point2D(
            sub(point.x, mul(line.a, scale)),
            sub(point.y, mul(line.b, scale)),
        )

    def _chord_distances(self, state):
        """Expose a derived chord length as the distance of its endpoints."""
        length_predicates = (
            "ChordLengthFormulaOf",
            "ChordLengthWithKFormulaOf",
            "ParabolaFocalChordLengthOf",
        )
        for intersection in state.find("IntersectionOf"):
            points = intersection.value
            if not isinstance(points, tuple) or len(points) != 2:
                continue
            first_object, second_object = intersection.arguments
            for predicate in length_predicates:
                length = state.value(
                    predicate, first_object, second_object
                )
                if length is None:
                    length = state.value(
                        predicate, second_object, first_object
                    )
                if length is None:
                    continue
                self._add(
                    state,
                    "DistanceFormulaOf",
                    points[0],
                    points[1],
                    value=length,
                )
                break

    def _quantities(self, state):
        for fact in state.find("ParameterOf"):
            if len(fact.arguments) != 2:
                continue
            entity, parameter = fact.arguments
            if parameter != "radius":
                continue
            reference = QuantityRef.of("radius", entity)
            self._add(
                state,
                "QuantityValueOf",
                reference,
                value=fact.value,
            )

        mappings = (
            ("DistanceFormulaOf", "distance"),
            ("SlopeFormulaOf", "slope"),
            ("CoordinateAreaFormulaOf", "area"),
            ("DotProductFormulaOf", "dot_product"),
        )
        for predicate, kind in mappings:
            for fact in state.find(predicate):
                reference = QuantityRef.of(kind, *fact.arguments)
                self._add(
                    state,
                    "QuantityValueOf",
                    reference,
                    value=fact.value,
                )


class QuantityApplicatorV2(GeometryApplicatorV2):
    def __init__(self, solver=None, closure=None):
        super().__init__(
            solver,
            closure or QuantityGeometryClosure(solver),
        )
