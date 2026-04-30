"""
Model 38: Ellipse_Tangent_Line

Tangent at (x0, y0) on x^2/a^2 + y^2/b^2 = 1:
x0*x/a^2 + y0*y/b^2 = 1.
"""

import re

from ..base_model import TheoremModel


class EllipseTangentLine(TheoremModel):
    """
    Adds a structured tangent-line equation for an ellipse at a known point.
    """

    def __init__(self):
        super().__init__(
            model_id=38,
            name="Ellipse_Tangent_Line",
            chinese_name="椭圆切线"
        )

    def can_apply(self, state) -> bool:
        has_ellipse = any(
            entity_type.lower() == "ellipse"
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False

        if self._get_a_squared(state) is None or self._get_b_squared(state) is None:
            return False

        return self._find_tangent_point(state) is not None

    def apply(self, state) -> bool:
        try:
            a_squared = self._get_a_squared(state)
            b_squared = self._get_b_squared(state)
            point = self._find_tangent_point(state)
            if a_squared is None or b_squared is None or point is None:
                return False

            point_name, x0, y0 = point
            curve_name = self._ellipse_name(state)
            tangent_equation = f"({x0})*x/{a_squared} + ({y0})*y/{b_squared} = 1"

            state.parameters["tangent_point"] = point_name
            state.parameters["tangent_line"] = tangent_equation
            self._append_once(
                state.equations,
                f"Expression(TangentLine({curve_name}, {point_name})) = ({tangent_equation})"
            )
            self._append_once(
                state.geometric_relations,
                f"EllipseTangentLine({point_name}): {tangent_equation}"
            )
            self._append_once(state.applied_models, self.model_id)
            return True
        except Exception:
            return False

    def _ellipse_name(self, state) -> str:
        for name, entity_type in state.entities.items():
            if entity_type.lower() == "ellipse":
                return name
        return "E"

    def _get_a_squared(self, state):
        if "a^2" in state.parameters:
            return str(state.parameters["a^2"])
        return self._square_param(state.parameters.get("a"))

    def _get_b_squared(self, state):
        if "b^2" in state.parameters:
            return str(state.parameters["b^2"])
        return self._square_param(state.parameters.get("b"))

    def _square_param(self, value):
        if value is None:
            return None
        try:
            squared = float(value) ** 2
            return str(int(squared)) if squared == int(squared) else str(squared)
        except (ValueError, TypeError):
            return f"({value})^2"

    def _find_tangent_point(self, state):
        x0 = state.parameters.get("x0") or state.parameters.get("x_0")
        y0 = state.parameters.get("y0") or state.parameters.get("y_0")
        if x0 is not None and y0 is not None:
            return state.parameters.get("tangent_point", "P"), str(x0), str(y0)

        for rel in state.geometric_relations:
            point_name = self._point_name_from_relation(rel)
            if point_name and point_name in state.coordinates:
                x_coord, y_coord = state.coordinates[point_name]
                return point_name, str(x_coord), str(y_coord)

        tangent_candidates = [
            name for name in state.coordinates
            if name.lower() in {"p", "t", "a", "b"}
        ]
        if len(tangent_candidates) == 1:
            name = tangent_candidates[0]
            x_coord, y_coord = state.coordinates[name]
            return name, str(x_coord), str(y_coord)

        return None

    def _point_name_from_relation(self, relation: str):
        keywords = ("Tangent", "TangentAt", "PointOnCurve", "切点")
        if not any(keyword in relation for keyword in keywords):
            return None

        match = re.search(r"(?:TangentAt|PointOnCurve)\((\w+)", relation)
        if match:
            return match.group(1)

        match = re.search(r"切点[:：]?\s*(\w+)", relation)
        if match:
            return match.group(1)

        return None

    def _append_once(self, values, value) -> None:
        if value not in values:
            values.append(value)
