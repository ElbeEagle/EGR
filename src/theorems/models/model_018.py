"""
Model 18: Ellipse_Latus_Rectum

Latus rectum length for an ellipse: 2*b^2/a.
"""

from ..base_model import TheoremModel


class EllipseLatusRectum(TheoremModel):
    """
    Computes the ellipse latus rectum from a and b.
    """

    def __init__(self):
        super().__init__(
            model_id=18,
            name="Ellipse_Latus_Rectum",
            chinese_name="椭圆通径"
        )

    def can_apply(self, state) -> bool:
        has_ellipse = any(
            entity_type.lower() == "ellipse"
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False

        return self._get_a(state) is not None and self._get_b_squared(state) is not None

    def apply(self, state) -> bool:
        try:
            a_val = self._get_a(state)
            b_squared = self._get_b_squared(state)
            if a_val is None or b_squared is None:
                return False

            latus_rectum = self._divide_by_a(f"2*{b_squared}", a_val)
            state.parameters["ellipse_latus_rectum"] = latus_rectum
            state.parameters["latus_rectum"] = latus_rectum

            self._append_once(
                state.geometric_relations,
                f"EllipseLatusRectum: l = 2*{b_squared}/{a_val} = {latus_rectum}"
            )
            self._append_once(state.applied_models, self.model_id)
            return True
        except Exception:
            return False

    def _get_a(self, state):
        if "a" in state.parameters:
            return str(state.parameters["a"])

        a_squared = state.parameters.get("a^2")
        if a_squared is None:
            return None

        try:
            a_num = float(a_squared) ** 0.5
            return str(int(a_num)) if a_num == int(a_num) else str(a_num)
        except (ValueError, TypeError):
            return f"sqrt({a_squared})"

    def _get_b_squared(self, state):
        if "b^2" in state.parameters:
            return str(state.parameters["b^2"])

        b_val = state.parameters.get("b")
        if b_val is None:
            return None

        try:
            b_num = float(b_val)
            b_squared = b_num ** 2
            return str(int(b_squared)) if b_squared == int(b_squared) else str(b_squared)
        except (ValueError, TypeError):
            return f"({b_val})^2"

    def _divide_by_a(self, numerator_expr: str, a_val: str) -> str:
        try:
            numerator = self._eval_product(numerator_expr)
            denominator = float(a_val)
            value = numerator / denominator
            return str(int(value)) if value == int(value) else str(value)
        except (ValueError, TypeError, ZeroDivisionError):
            return f"{numerator_expr}/{a_val}"

    def _eval_product(self, expr: str) -> float:
        left, right = expr.split("*", 1)
        return float(left) * float(right)

    def _append_once(self, values, value) -> None:
        if value not in values:
            values.append(value)
