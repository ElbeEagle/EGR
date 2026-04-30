"""
Model 64: Basic_Inequality_Equal_Condition

Equality condition for AM-GM: equality holds when the compared terms are equal.
"""

from ..base_model import TheoremModel


class BasicInequalityEqualCondition(TheoremModel):
    """
    Adds the equality condition associated with the basic inequality.
    """

    def __init__(self):
        super().__init__(
            model_id=64,
            name="Basic_Inequality_Equal_Condition",
            chinese_name="基本不等式取等条件"
        )

    def can_apply(self, state) -> bool:
        return self._has_basic_inequality_context(state) and self._terms(state) is not None

    def apply(self, state) -> bool:
        try:
            terms = self._terms(state)
            if terms is None:
                return False

            left, right = terms
            condition = f"{left} = {right}"
            state.parameters["basic_inequality_equality_condition"] = condition
            self._append_once(state.constraints, condition)
            self._append_once(
                state.geometric_relations,
                f"BasicInequalityEqualityCondition: {condition}"
            )
            self._append_once(state.applied_models, self.model_id)
            return True
        except Exception:
            return False

    def _has_basic_inequality_context(self, state) -> bool:
        keywords = (
            "BasicInequality",
            "basic inequality",
            "AM-GM",
            "am-gm",
            "a + b >= 2",
            "a+b>=2",
            "基本不等式",
        )
        return any(
            keyword in relation
            for relation in state.geometric_relations
            for keyword in keywords
        )

    def _terms(self, state):
        terms = state.parameters.get("amgm_terms")
        if isinstance(terms, (list, tuple)) and len(terms) == 2:
            return str(terms[0]), str(terms[1])

        if "amgm_left" in state.parameters and "amgm_right" in state.parameters:
            return str(state.parameters["amgm_left"]), str(state.parameters["amgm_right"])

        if "a" in state.parameters and "b" in state.parameters:
            return "a", "b"

        return None

    def _append_once(self, values, value) -> None:
        if value not in values:
            values.append(value)
