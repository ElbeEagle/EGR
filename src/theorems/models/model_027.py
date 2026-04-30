"""
Model 27: Ellipse_Directrix

Directrix for an ellipse: x = +/- a^2/c or y = +/- a^2/c.
"""

import re

from ..base_model import TheoremModel


class EllipseDirectrix(TheoremModel):
    """
    Adds structured directrix information for an ellipse.
    """

    def __init__(self):
        super().__init__(
            model_id=27,
            name="Ellipse_Directrix",
            chinese_name="椭圆准线"
        )

    def can_apply(self, state) -> bool:
        has_ellipse = any(
            entity_type.lower() == "ellipse"
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False

        return self._get_a_squared(state) is not None and self._get_c(state) is not None

    def apply(self, state) -> bool:
        try:
            a_squared = self._get_a_squared(state)
            c_val = self._get_c(state)
            if a_squared is None or c_val is None:
                return False

            axis = self._infer_axis(state)
            curve_name = self._ellipse_name(state)
            distance = self._divide(a_squared, c_val)
            equation = f"{axis} = pm*({distance})"

            state.parameters["directrix_axis"] = axis
            state.parameters["directrix_distance"] = distance
            state.parameters["ellipse_directrix"] = equation

            self._append_once(
                state.equations,
                f"Expression(Directrix({curve_name})) = ({equation})"
            )
            self._append_once(
                state.geometric_relations,
                f"EllipseDirectrix: {axis} = +/- {a_squared}/{c_val}"
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

        a_val = state.parameters.get("a")
        if a_val is None:
            return None

        try:
            a_num = float(a_val)
            a_squared = a_num ** 2
            return str(int(a_squared)) if a_squared == int(a_squared) else str(a_squared)
        except (ValueError, TypeError):
            return f"({a_val})^2"

    def _get_c(self, state):
        if "c" in state.parameters:
            return str(state.parameters["c"])

        c_squared = state.parameters.get("c^2")
        if c_squared is None:
            a_squared = state.parameters.get("a^2")
            b_squared = state.parameters.get("b^2")
            if a_squared is not None and b_squared is not None:
                try:
                    c_squared_num = float(a_squared) - float(b_squared)
                    if c_squared_num < 0:
                        return None
                    c_squared = (
                        str(int(c_squared_num))
                        if c_squared_num == int(c_squared_num)
                        else str(c_squared_num)
                    )
                    state.parameters.setdefault("c^2", c_squared)
                except (ValueError, TypeError):
                    c_squared = f"({a_squared})-({b_squared})"
                    state.parameters.setdefault("c^2", c_squared)

        if c_squared is None:
            return None

        try:
            c_num = float(c_squared) ** 0.5
            c_val = str(int(c_num)) if c_num == int(c_num) else str(c_num)
        except (ValueError, TypeError):
            c_val = f"sqrt({c_squared})"

        state.parameters.setdefault("c", c_val)
        return c_val

    def _infer_axis(self, state) -> str:
        for rel in state.geometric_relations:
            lowered = rel.lower()
            if "焦点在y轴" in rel or "focus on y" in lowered:
                return "y"
            if "焦点在x轴" in rel or "focus on x" in lowered:
                return "x"

        for eq in state.equations:
            axis = self._infer_axis_from_equation(eq)
            if axis:
                return axis

        return "x"

    def _infer_axis_from_equation(self, equation: str):
        eq = equation.replace(" ", "")
        x_match = re.search(r"x\^2/([^+\-=)]+)", eq)
        y_match = re.search(r"y\^2/([^+\-=)]+)", eq)
        if not x_match or not y_match:
            return None

        x_den = x_match.group(1)
        y_den = y_match.group(1)
        try:
            return "x" if float(x_den) >= float(y_den) else "y"
        except (ValueError, TypeError):
            return "x"

    def _divide(self, numerator: str, denominator: str) -> str:
        try:
            value = float(numerator) / float(denominator)
            return str(int(value)) if value == int(value) else str(value)
        except (ValueError, TypeError, ZeroDivisionError):
            return f"{numerator}/{denominator}"

    def _append_once(self, values, value) -> None:
        if value not in values:
            values.append(value)
