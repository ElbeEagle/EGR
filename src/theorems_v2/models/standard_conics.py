"""Standard conic equation models 3-10 and 75."""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Optional

from ..base import TheoremModelV2
from ..expressions import ConservativeSolver, add, div, equation, mul, neg, square, sub
from ..schema import Derivation, PolynomialEquation, StandardConicForm, StateDelta, Term
from ..state import InformationState
from .common import entities_of_type, orientation_fact, parameter_term, theorem_fact


def _zero_other_terms(
    poly: PolynomialEquation,
    solver: ConservativeSolver,
    allowed: set[str],
) -> bool:
    for name in ("x2", "xy", "y2", "x", "y", "constant"):
        if name not in allowed and not solver.equivalent(getattr(poly, name), 0):
            return False
    return True


def _known_positive(
    state: InformationState, value: Any, solver: ConservativeSolver
) -> bool:
    value_sign = solver.sign(value)
    if value_sign is not None:
        return value_sign > 0
    if state.get("Positive", value) is not None:
        return True
    if isinstance(value, Term) and value.operator == "mul":
        if len(value.arguments) == 2 and value.arguments[0] == value.arguments[1]:
            return True
        return all(_known_positive(state, factor, solver) for factor in value.arguments)
    if (
        isinstance(value, Term)
        and value.operator == "pow"
        and value.arguments[1] == 2
    ):
        return _known_positive(state, value.arguments[0], solver)
    return False


def _explicitly_positive(
    state: InformationState, value: Any, solver: ConservativeSolver
) -> bool:
    value_sign = solver.sign(value)
    if value_sign is not None:
        return value_sign > 0
    if state.get("Positive", value) is not None:
        return True
    if isinstance(value, Term) and value.operator == "mul":
        return all(
            _explicitly_positive(state, factor, solver)
            for factor in value.arguments
        )
    if (
        isinstance(value, Term)
        and value.operator == "pow"
        and value.arguments[1] == 2
    ):
        return _explicitly_positive(state, value.arguments[0], solver)
    return False


def _ratio(numerator: Any, denominator: Any) -> Any:
    """Simplify rational coefficient shapes produced by polynomial parsing."""
    if isinstance(denominator, Term) and denominator.operator == "div":
        inner_numerator, inner_denominator = denominator.arguments
        return div(mul(numerator, inner_denominator), inner_numerator)
    if isinstance(denominator, Term) and denominator.operator == "mul":
        numeric = Fraction(1)
        symbolic = []
        for factor in denominator.arguments:
            if isinstance(factor, Fraction):
                numeric *= factor
            else:
                symbolic.append(factor)
        if len(symbolic) == 1 and isinstance(symbolic[0], Term):
            factor = symbolic[0]
            if factor.operator == "div":
                inner_numerator, inner_denominator = factor.arguments
                scaled = mul(numerator, inner_denominator, Fraction(1, 1) / numeric)
                return div(scaled, inner_numerator)
    return div(numerator, denominator)

def _known_comparison(
    state: InformationState,
    left: Any,
    right: Any,
    solver: ConservativeSolver,
) -> Optional[int]:
    direct = solver.sign(sub(left, right))
    if direct is not None:
        return direct
    if state.get("GreaterThan", left, right) is not None:
        return 1
    if state.get("GreaterThan", right, left) is not None:
        return -1
    if (
        isinstance(left, Term)
        and left.operator == "mul"
        and len(left.arguments) == 2
        and left.arguments[0] == left.arguments[1]
        and isinstance(right, Term)
        and right.operator == "mul"
        and len(right.arguments) == 2
        and right.arguments[0] == right.arguments[1]
        and _known_positive(state, left.arguments[0], solver)
        and _known_positive(state, right.arguments[0], solver)
    ):
        if state.get("GreaterThan", left.arguments[0], right.arguments[0]) is not None:
            return 1
        if state.get("GreaterThan", right.arguments[0], left.arguments[0]) is not None:
            return -1
    return None

class CenteredConicEquationV2(TheoremModelV2):
    def __init__(
        self,
        model_id: int,
        curve_type: str,
        orientation: str,
    ):
        self.model_id = model_id
        self.curve_type = curve_type
        self.orientation = orientation
        self.name = f"{curve_type}_Standard_{orientation}_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        solver = ConservativeSolver()
        matches: List[Dict[str, Any]] = []
        curves = entities_of_type(state, self.curve_type)
        for curve in curves:
            for expression_fact in state.find("ExpressionPolynomial", curve):
                poly = expression_fact.value
                if not isinstance(poly, PolynomialEquation):
                    continue
                if not _zero_other_terms(
                    poly, solver, {"x2", "y2", "constant"}
                ):
                    continue
                parameters = self._extract(state, curve, poly, solver)
                if parameters is None:
                    continue
                if len(curves) > 1 and not all(
                    _explicitly_positive(state, value, solver)
                    for value in parameters
                ):
                    continue
                matches.append(
                    {
                        "G": curve,
                        "a2": parameters[0],
                        "b2": parameters[1],
                        "_evidence": (expression_fact,),
                    }
                )
        return matches

    def _extract(
        self,
        state: InformationState,
        curve: str,
        poly: PolynomialEquation,
        solver: ConservativeSolver,
    ) -> Optional[tuple[Any, Any]]:
        if solver.equivalent(poly.x2, 0) or solver.equivalent(poly.y2, 0):
            return None
        if solver.equivalent(poly.constant, 0):
            return None

        if self.curve_type == "Ellipse":
            x_denominator = _ratio(neg(poly.constant), poly.x2)
            y_denominator = _ratio(neg(poly.constant), poly.y2)
            if not (
                _known_positive(state, x_denominator, solver)
                and _known_positive(state, y_denominator, solver)
            ):
                return None
            x_sign = _known_comparison(state, x_denominator, y_denominator, solver)
            explicit = orientation_fact(state, curve)
            inferred = "horizontal" if x_sign == 1 else "vertical" if x_sign == -1 else None
            orientation = inferred or (explicit.value if explicit else None)
            if orientation != self.orientation:
                return None
            if self.orientation == "horizontal":
                return x_denominator, y_denominator
            return y_denominator, x_denominator

        if self.orientation == "horizontal":
            a2 = _ratio(neg(poly.constant), poly.x2)
            b2 = _ratio(poly.constant, poly.y2)
        else:
            a2 = _ratio(neg(poly.constant), poly.y2)
            b2 = _ratio(poly.constant, poly.x2)
        if not (
            _known_positive(state, a2, solver)
            and _known_positive(state, b2, solver)
        ):
            return None
        return a2, b2

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        evidence = binding["_evidence"]
        curve = binding["G"]
        a2, b2 = binding["a2"], binding["b2"]
        existing_a2 = state.value("ParameterOf", curve, "semi_axis_a_squared")
        existing_b2 = state.value("ParameterOf", curve, "semi_axis_b_squared")
        existing_a = state.value("ParameterOf", curve, "semi_axis_a")
        existing_b = state.value("ParameterOf", curve, "semi_axis_b")
        effective_a2 = (
            existing_a2
            if existing_a2 is not None
            else solver.square(existing_a) if existing_a is not None else a2
        )
        effective_b2 = (
            existing_b2
            if existing_b2 is not None
            else solver.square(existing_b) if existing_b is not None else b2
        )
        facts = [
            theorem_fact(
                self.model_id,
                "ConicStandardForm",
                curve,
                value=StandardConicForm(
                    self.curve_type.lower(),
                    self.orientation,
                    a2=effective_a2,
                    b2=effective_b2,
                ),
                evidence=evidence,
            )
        ]
        parameter_values = (
            ("semi_axis_a_squared", effective_a2),
            ("semi_axis_b_squared", effective_b2),
            ("semi_axis_a", solver.sqrt_positive(effective_a2)),
            ("semi_axis_b", solver.sqrt_positive(effective_b2)),
        )
        for parameter_name, value in parameter_values:
            if state.get("ParameterOf", curve, parameter_name) is None:
                facts.append(
                    theorem_fact(
                        self.model_id,
                        "ParameterOf",
                        curve,
                        parameter_name,
                        value=value,
                        evidence=evidence,
                    )
                )
        return Derivation(
            StateDelta(add_facts=tuple(facts)), self.evidence(*evidence)
        )


class ParabolaEquationV2(TheoremModelV2):
    def __init__(self, model_id: int, direction: str):
        self.model_id = model_id
        self.direction = direction
        self.name = f"Parabola_Standard_{direction}_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        solver = ConservativeSolver()
        matches: List[Dict[str, Any]] = []
        horizontal = self.direction in {"right", "left"}
        for curve in entities_of_type(state, "Parabola"):
            explicit = orientation_fact(state, curve)
            for expression_fact in state.find("ExpressionPolynomial", curve):
                poly = expression_fact.value
                if not isinstance(poly, PolynomialEquation):
                    continue
                allowed = {"y2", "x"} if horizontal else {"x2", "y"}
                if not _zero_other_terms(poly, solver, allowed):
                    continue
                squared = poly.y2 if horizontal else poly.x2
                linear = poly.x if horizontal else poly.y
                if solver.equivalent(squared, 0):
                    continue
                coefficient = div(neg(linear), squared)
                coefficient_sign = solver.sign(coefficient)
                if coefficient_sign is None and _known_positive(
                    state, coefficient, solver
                ):
                    coefficient_sign = 1
                elif coefficient_sign is None and _known_positive(
                    state, neg(coefficient), solver
                ):
                    coefficient_sign = -1
                inferred = None
                if coefficient_sign == 1:
                    inferred = "right" if horizontal else "up"
                elif coefficient_sign == -1:
                    inferred = "left" if horizontal else "down"
                direction = inferred or (explicit.value if explicit else None)
                if direction != self.direction:
                    continue
                two_p = coefficient if direction in {"right", "up"} else neg(coefficient)
                if not _known_positive(state, two_p, solver):
                    continue
                matches.append(
                    {
                        "G": curve,
                        "two_p": two_p,
                        "_evidence": (expression_fact,),
                    }
                )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        evidence = binding["_evidence"]
        curve, two_p = binding["G"], binding["two_p"]
        p = solver.div(two_p, 2)
        focus_offset = solver.div(p, 2)
        facts = (
            theorem_fact(
                self.model_id,
                "ConicStandardForm",
                curve,
                value=StandardConicForm(
                    "parabola",
                    self.direction,
                    two_p=two_p,
                    focus_offset=focus_offset,
                ),
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "ParameterOf",
                curve,
                "two_p",
                value=two_p,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "ParameterOf",
                curve,
                "p",
                value=p,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "FocusOffsetOf",
                curve,
                value=focus_offset,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "EquationConstraint",
                equation(
                    parameter_term(curve, "two_p"),
                    mul(2, parameter_term(curve, "p")),
                ),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


class CircleStandardEquationV2(TheoremModelV2):
    model_id = 75
    name = "Circle_Standard_Equation_V2"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        solver = ConservativeSolver()
        matches: List[Dict[str, Any]] = []
        for circle in entities_of_type(state, "Circle"):
            for expression_fact in state.find("ExpressionPolynomial", circle):
                poly = expression_fact.value
                if not isinstance(poly, PolynomialEquation):
                    continue
                if not solver.equivalent(poly.x2, poly.y2):
                    continue
                if solver.equivalent(poly.x2, 0) or not solver.equivalent(poly.xy, 0):
                    continue
                coefficient = poly.x2
                h = div(neg(poly.x), mul(2, coefficient))
                k = div(neg(poly.y), mul(2, coefficient))
                radius2 = sub(add(square(h), square(k)), div(poly.constant, coefficient))
                if not _known_positive(state, radius2, solver):
                    continue
                matches.append(
                    {
                        "C": circle,
                        "h": h,
                        "k": k,
                        "r2": radius2,
                        "_evidence": (expression_fact,),
                    }
                )
        return matches

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        evidence = binding["_evidence"]
        circle = binding["C"]
        h, k, radius2 = binding["h"], binding["k"], binding["r2"]
        facts = (
            theorem_fact(
                self.model_id,
                "CircleStandardForm",
                circle,
                value=(h, k, radius2),
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "CenterCoordinateOf",
                circle,
                value=(h, k),
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "ParameterOf",
                circle,
                "radius_squared",
                value=radius2,
                evidence=evidence,
            ),
            theorem_fact(
                self.model_id,
                "ParameterOf",
                circle,
                "radius",
                value=solver.sqrt_positive(radius2),
                evidence=evidence,
            ),
        )
        return Derivation(StateDelta(add_facts=facts), self.evidence(*evidence))


def standard_equation_models() -> List[TheoremModelV2]:
    return [
        CenteredConicEquationV2(3, "Ellipse", "horizontal"),
        CenteredConicEquationV2(4, "Ellipse", "vertical"),
        CenteredConicEquationV2(5, "Hyperbola", "horizontal"),
        CenteredConicEquationV2(6, "Hyperbola", "vertical"),
        ParabolaEquationV2(7, "right"),
        ParabolaEquationV2(8, "left"),
        ParabolaEquationV2(9, "up"),
        ParabolaEquationV2(10, "down"),
    ]
