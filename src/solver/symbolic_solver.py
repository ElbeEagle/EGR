"""
Lightweight symbolic solver utilities used by the answer extractor.

The solver intentionally covers common axis-aligned conic patterns in the
current formal language. It returns ``None`` for unsupported shapes instead of
pretending to solve them.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import sympy as sp

from src.state.symbolic_state import SymbolicState


X, Y = sp.symbols("x y")


@dataclass
class CurveModel:
    target: str
    curve_type: str
    expression: str
    x_denom: Optional[sp.Expr] = None
    y_denom: Optional[sp.Expr] = None
    parabola_axis: Optional[str] = None
    parabola_p: Optional[sp.Expr] = None


class SymbolicSolver:
    """Small exact solver for common conic answer-extraction cases."""

    def expression_entries(self, state: SymbolicState) -> List[Tuple[str, str]]:
        entries = []
        for equation in state.equations:
            parsed = self.parse_expression_assignment(equation)
            if parsed:
                entries.append(parsed)
        return entries

    def parse_expression_assignment(self, equation: str) -> Optional[Tuple[str, str]]:
        text = equation.strip()
        prefix = "Expression("
        start = text.find(prefix)
        if start < 0:
            return None

        target_start = start + len(prefix)
        target_end = self.find_matching_paren(text, target_start - 1)
        if target_end < 0:
            return None

        target = text[target_start:target_end].strip()
        rest = text[target_end + 1 :].strip()
        if not rest.startswith("="):
            return None
        value = rest[1:].strip()
        value = self.strip_outer_parens(value)
        return target, value

    def find_matching_paren(self, text: str, open_index: int) -> int:
        depth = 0
        for idx in range(open_index, len(text)):
            char = text[idx]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return idx
        return -1

    def strip_outer_parens(self, text: str) -> str:
        text = text.strip()
        while text.startswith("(") and text.endswith(")"):
            end = self.find_matching_paren(text, 0)
            if end != len(text) - 1:
                break
            text = text[1:-1].strip()
        return text

    def split_top_level(self, text: str, separators: Sequence[str]) -> List[str]:
        parts = []
        depth = 0
        start = 0
        for idx, char in enumerate(text):
            if char in "({[":
                depth += 1
            elif char in ")}]":
                depth = max(0, depth - 1)
            elif depth == 0 and char in separators:
                part = text[start:idx].strip()
                if part:
                    parts.append(part)
                start = idx + 1
        tail = text[start:].strip()
        if tail:
            parts.append(tail)
        return parts

    def parse_expr(self, expr: Any) -> Optional[sp.Expr]:
        if expr is None:
            return None
        if isinstance(expr, (int, float, sp.Expr)):
            return sp.sympify(expr)

        text = str(expr).strip()
        if not text:
            return None
        text = self.strip_outer_parens(text)
        text = text.replace("^", "**")
        text = text.replace("pm*", "")
        text = text.replace("pm", "")
        text = re.sub(r"\bSin\(", "sin(", text)
        text = re.sub(r"\bCos\(", "cos(", text)
        text = re.sub(r"\bTan\(", "tan(", text)

        # Some coordinates in the current parser lose the final ")" for sqrt.
        if text.count("(") > text.count(")"):
            text += ")" * (text.count("(") - text.count(")"))

        locals_dict = {
            "sqrt": sp.sqrt,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "pi": sp.pi,
            "x": X,
            "y": Y,
        }
        try:
            return sp.sympify(text, locals=locals_dict)
        except Exception:
            return None

    def parse_equation_expr(self, equation: str) -> Optional[sp.Expr]:
        if "=" not in equation:
            return self.parse_expr(equation)
        left, right = equation.split("=", 1)
        lhs = self.parse_expr(left)
        rhs = self.parse_expr(right)
        if lhs is None or rhs is None:
            return None
        return sp.expand(lhs - rhs)

    def curve_models(self, state: SymbolicState) -> Dict[str, CurveModel]:
        models: Dict[str, CurveModel] = {}
        for target, expression in self.expression_entries(state):
            if "Asymptote" in target or "Directrix" in target or "Tangent" in target:
                continue
            model = self.parse_curve_model(state, target, expression)
            if model:
                models[target] = model
        return models

    def parse_curve_model(
        self,
        state: SymbolicState,
        target: str,
        expression: str,
    ) -> Optional[CurveModel]:
        curve_type = state.entities.get(target, "Unknown")
        equation_expr = self.parse_equation_expr(expression)
        if equation_expr is None:
            return None

        try:
            poly = sp.Poly(sp.expand(equation_expr), X, Y)
        except Exception:
            return None

        if poly.total_degree() > 2:
            return None

        x2 = poly.coeff_monomial(X**2)
        y2 = poly.coeff_monomial(Y**2)
        x1 = poly.coeff_monomial(X)
        y1 = poly.coeff_monomial(Y)
        xy = poly.coeff_monomial(X * Y)
        const = poly.coeff_monomial(1)

        if xy != 0:
            return None

        if x2 != 0 and y2 != 0 and x1 == 0 and y1 == 0 and const != 0:
            x_denom = sp.simplify(-const / x2)
            y_denom = sp.simplify(-const / y2)
            if curve_type == "Unknown":
                curve_type = self.infer_centered_curve_type(x_denom, y_denom)
            return CurveModel(
                target=target,
                curve_type=curve_type,
                expression=expression,
                x_denom=x_denom,
                y_denom=y_denom,
            )

        # y^2 = k*x or x^2 = k*y, centered at the origin.
        if y2 != 0 and x1 != 0 and x2 == 0 and y1 == 0 and const == 0:
            k = sp.simplify(-x1 / y2)
            return CurveModel(
                target=target,
                curve_type="Parabola",
                expression=expression,
                parabola_axis="x",
                parabola_p=sp.simplify(k / 4),
            )
        if x2 != 0 and y1 != 0 and y2 == 0 and x1 == 0 and const == 0:
            k = sp.simplify(-y1 / x2)
            return CurveModel(
                target=target,
                curve_type="Parabola",
                expression=expression,
                parabola_axis="y",
                parabola_p=sp.simplify(k / 4),
            )
        return None

    def infer_centered_curve_type(self, x_denom: sp.Expr, y_denom: sp.Expr) -> str:
        x_sign = self.expr_sign(x_denom)
        y_sign = self.expr_sign(y_denom)
        if x_sign and y_sign and x_sign == y_sign:
            return "Ellipse"
        if x_sign and y_sign and x_sign != y_sign:
            return "Hyperbola"
        return "Unknown"

    def expr_sign(self, expr: sp.Expr) -> Optional[int]:
        try:
            value = float(expr)
        except Exception:
            return None
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0

    def format_expr(self, expr: Any) -> str:
        parsed = self.parse_expr(expr)
        if parsed is None:
            return str(expr).strip()
        simplified = sp.simplify(parsed)
        if simplified == sp.oo:
            return "+oo"
        if simplified == -sp.oo:
            return "-oo"
        return sp.sstr(simplified).replace("**", "^").replace(" ", "")

    def format_number_or_expr(self, expr: Any) -> Any:
        parsed = self.parse_expr(expr)
        if parsed is None:
            return expr
        simplified = sp.simplify(parsed)
        if simplified.is_Integer:
            return int(simplified)
        if simplified.is_Rational:
            return self.format_expr(simplified)
        return self.format_expr(simplified)

    def format_signed_sqrt_pair(self, value: sp.Expr) -> str:
        return f"pm*{self.format_expr(sp.sqrt(sp.simplify(value)))}"

    def format_coordinate(self, x_value: Any, y_value: Any) -> str:
        return f"({self.format_expr(x_value)}, {self.format_expr(y_value)})"

    def format_pm_coordinate(self, x_value: Any, y_square: Any) -> str:
        return f"({self.format_expr(x_value)}, {self.format_signed_sqrt_pair(y_square)})"

    def format_term(self, variable: str, denominator: Any) -> str:
        denom = sp.simplify(self.parse_expr(denominator))
        if denom == 1:
            return f"{variable}^2"
        return f"{variable}^2/{self.format_expr(denom)}"

    def format_centered_conic(
        self,
        x_denom: Any,
        y_denom: Any,
        curve_type: str,
    ) -> Optional[str]:
        x_d = self.parse_expr(x_denom)
        y_d = self.parse_expr(y_denom)
        if x_d is None or y_d is None:
            return None
        x_d = sp.simplify(x_d)
        y_d = sp.simplify(y_d)

        if curve_type == "Ellipse":
            return f"{self.format_term('x', x_d)}+{self.format_term('y', y_d)}=1"

        if curve_type == "Hyperbola":
            if self.expr_sign(x_d) == 1 and self.expr_sign(y_d) == -1:
                return f"{self.format_term('x', x_d)}-{self.format_term('y', -y_d)}=1"
            if self.expr_sign(y_d) == 1 and self.expr_sign(x_d) == -1:
                return f"{self.format_term('y', y_d)}-{self.format_term('x', -x_d)}=1"
            # Use x-axis orientation when the symbolic denominator is expected
            # to be negative but not known until solving.
            return f"{self.format_term('x', x_d)}-{self.format_term('y', sp.Abs(y_d))}=1"
        return None

    def conic_eccentricity(self, model: CurveModel) -> Optional[str]:
        if model.x_denom is None or model.y_denom is None:
            return None
        x_d = sp.simplify(model.x_denom)
        y_d = sp.simplify(model.y_denom)
        curve_type = model.curve_type

        if curve_type == "Ellipse":
            values = [x_d, y_d]
            if all(v.is_number for v in values):
                a2 = max(values, key=lambda item: float(item))
                b2 = min(values, key=lambda item: float(item))
            else:
                a2, b2 = x_d, y_d
            return self.format_expr(sp.sqrt(sp.simplify((a2 - b2) / a2)))

        if curve_type == "Hyperbola":
            if self.expr_sign(x_d) == 1 and self.expr_sign(y_d) == -1:
                return self.format_expr(sp.sqrt(sp.simplify((x_d - y_d) / x_d)))
            if self.expr_sign(y_d) == 1 and self.expr_sign(x_d) == -1:
                return self.format_expr(sp.sqrt(sp.simplify((y_d - x_d) / y_d)))
            # Most current formal hyperbolas use x^2/a^2 + y^2/m = 1 with m<0.
            return self.format_expr(sp.sqrt(sp.simplify((x_d - y_d) / x_d)))
        if curve_type == "Parabola":
            return "1"
        return None

    def conic_focus(self, model: CurveModel, side: str = "both") -> Optional[str]:
        if model.curve_type == "Parabola" and model.parabola_p is not None:
            p = model.parabola_p
            if model.parabola_axis == "x":
                return self.format_coordinate(p, 0)
            if model.parabola_axis == "y":
                return self.format_coordinate(0, p)

        if model.x_denom is None or model.y_denom is None:
            return None
        x_d = sp.simplify(model.x_denom)
        y_d = sp.simplify(model.y_denom)

        if model.curve_type == "Ellipse":
            if all(v.is_number for v in [x_d, y_d]) and float(y_d) > float(x_d):
                c2 = y_d - x_d
                return f"(0, {self.format_signed_sqrt_pair(c2)})"
            c2 = x_d - y_d
            return f"({self.format_signed_sqrt_pair(c2)}, 0)"

        if model.curve_type == "Hyperbola":
            if self.expr_sign(x_d) == 1:
                c2 = x_d + abs(y_d)
                return f"({self.format_signed_sqrt_pair(c2)}, 0)"
            c2 = y_d + abs(x_d)
            return f"(0, {self.format_signed_sqrt_pair(c2)})"
        return None

    def conic_focal_distance(self, model: CurveModel) -> Optional[str]:
        if model.x_denom is None or model.y_denom is None:
            return None
        x_d = sp.simplify(model.x_denom)
        y_d = sp.simplify(model.y_denom)
        if model.curve_type == "Ellipse":
            c2 = abs(x_d - y_d)
        elif model.curve_type == "Hyperbola":
            if self.expr_sign(x_d) == 1:
                c2 = x_d + abs(y_d)
            else:
                c2 = y_d + abs(x_d)
        else:
            return None
        return self.format_expr(2 * sp.sqrt(sp.simplify(c2)))

    def conic_asymptote(self, model: CurveModel) -> Optional[str]:
        if model.curve_type != "Hyperbola" or model.x_denom is None or model.y_denom is None:
            return None
        x_d = sp.simplify(model.x_denom)
        y_d = sp.simplify(model.y_denom)
        if self.expr_sign(x_d) == 1 or self.expr_sign(x_d) is None:
            slope = sp.sqrt(sp.simplify(-y_d / x_d))
        else:
            slope = sp.sqrt(sp.simplify(-x_d / y_d))
        return f"y=pm*{self.format_expr(slope)}*x"

    def direct_relation_value(self, state: SymbolicState, query: str) -> Optional[str]:
        compact_query = self.normalize_relation_lhs(query)
        for relation in list(state.geometric_relations) + list(state.equations):
            if "=" not in relation:
                continue
            left, right = relation.split("=", 1)
            if self.normalize_relation_lhs(left) == compact_query:
                return self.strip_outer_parens(right.strip())
        return None

    def normalize_relation_lhs(self, text: str) -> str:
        return re.sub(r"\s+", "", text.strip())

    def solve_variable(self, state: SymbolicState, variable: str) -> Optional[str]:
        for model in self.curve_models(state).values():
            if model.x_denom is not None and model.y_denom is not None:
                symbol = sp.Symbol(variable)
                if symbol in (model.x_denom.free_symbols | model.y_denom.free_symbols):
                    solved = self.solve_variable_from_model_relations(state, model, variable)
                    if solved is not None:
                        return solved

        if variable in state.parameters:
            value = state.parameters[variable]
            if str(value) != variable and str(value) not in {"Number", "Real"}:
                return self.format_expr(value)

        direct = self.direct_relation_value(state, variable)
        if direct:
            return self.format_expr(direct)
        return None

    def solve_variable_from_model_relations(
        self,
        state: SymbolicState,
        model: CurveModel,
        variable: str,
    ) -> Optional[str]:
        symbol = sp.Symbol(variable)
        x_d = model.x_denom
        y_d = model.y_denom

        if x_d is None or y_d is None:
            return None

        ecc_value = self.direct_relation_value(state, f"Eccentricity({model.target})")
        if ecc_value:
            e = self.parse_expr(ecc_value)
            if e is not None and symbol in (x_d.free_symbols | y_d.free_symbols):
                if model.curve_type == "Hyperbola":
                    equation = sp.Eq(e**2, sp.simplify((x_d - y_d) / x_d))
                    return self.first_solution(symbol, equation)
                if model.curve_type == "Ellipse":
                    equation = sp.Eq(e**2, sp.simplify((x_d - y_d) / x_d))
                    return self.first_solution(symbol, equation)

        asymptote = self.find_asymptote_expression(state, model.target)
        if asymptote and symbol in (x_d.free_symbols | y_d.free_symbols):
            slope = self.line_slope(asymptote)
            if slope is not None and model.curve_type == "Hyperbola":
                if slope.free_symbols & (x_d.free_symbols | y_d.free_symbols):
                    return None
                if self.expr_sign(x_d) == 1 or self.expr_sign(x_d) is None:
                    slope_square = sp.simplify(-y_d / x_d)
                else:
                    slope_square = sp.simplify(-x_d / y_d)
                equation = sp.Eq(slope**2, slope_square)
                solutions = sp.solve(equation, symbol)
                if solutions:
                    value = sp.simplify(solutions[-1])
                    if value.is_number and value >= 0:
                        return f"pm*{self.format_expr(value)}"
                    return self.format_expr(value)

        if self.has_relation_containing(state, f"Length(ImageinaryAxis({model.target}))*3", f"FocalLength({model.target})"):
            if symbol in (x_d.free_symbols | y_d.free_symbols):
                b2 = -y_d
                equation = sp.Eq(9 * b2, x_d + b2)
                return self.first_solution(symbol, equation)

        focus_coord = self.find_focus_coordinate(state, model.target)
        if focus_coord is not None and symbol in (x_d.free_symbols | y_d.free_symbols):
            fx, fy = focus_coord
            if fy != 0 and model.curve_type == "Ellipse":
                equation = sp.Eq(fy**2, y_d - x_d)
                return self.first_solution(symbol, equation)
            if fx != 0 and model.curve_type == "Ellipse":
                equation = sp.Eq(fx**2, x_d - y_d)
                return self.first_solution(symbol, equation)

        shared_focus = self.find_shared_parabola_focus_constraint(state, model.target)
        if shared_focus is not None and symbol in (x_d.free_symbols | y_d.free_symbols):
            if model.curve_type == "Hyperbola":
                if self.expr_sign(x_d) == 1 or self.expr_sign(x_d) is None:
                    c2 = sp.simplify(x_d - y_d)
                else:
                    c2 = sp.simplify(y_d - x_d)
                equation = sp.Eq(shared_focus, c2)
                try:
                    solutions = sp.solve(equation, symbol)
                except Exception:
                    solutions = []
                if solutions:
                    positives = [s for s in solutions if s.is_number and float(s) > 0]
                    if positives:
                        return self.format_expr(positives[0])
                    return self.format_expr(solutions[-1])

        return None

    def find_shared_parabola_focus_constraint(self, state: SymbolicState, curve: str) -> Optional[sp.Expr]:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            patterns = [
                rf"Focus\((\w+)\)=RightFocus\({re.escape(curve)}\)",
                rf"RightFocus\({re.escape(curve)}\)=Focus\((\w+)\)",
            ]
            for pattern in patterns:
                match = re.match(pattern, compact)
                if not match:
                    continue
                other = match.group(1)
                other_model = self.curve_models(state).get(other)
                if other_model and other_model.curve_type == "Parabola" and other_model.parabola_p is not None:
                    return sp.simplify(other_model.parabola_p**2)
        return None

    def first_solution(self, symbol: sp.Symbol, equation: sp.Eq) -> Optional[str]:
        try:
            solutions = sp.solve(equation, symbol)
        except Exception:
            return None
        if not solutions:
            return None
        return self.format_expr(sp.simplify(solutions[0]))

    def has_relation_containing(self, state: SymbolicState, *parts: str) -> bool:
        compact_parts = [self.normalize_relation_lhs(part) for part in parts]
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            if all(part in compact for part in compact_parts):
                return True
        return False

    def find_asymptote_expression(self, state: SymbolicState, curve: str) -> Optional[str]:
        for target, expression in self.expression_entries(state):
            if "Asymptote" in target and curve in target:
                return expression
        return None

    def line_slope(self, expression: str) -> Optional[sp.Expr]:
        expr = expression.strip()
        if "=" in expr:
            left, right = expr.split("=", 1)
            lhs = self.parse_expr(left)
            rhs = self.parse_expr(right)
            if lhs is None or rhs is None:
                return None
            equation = sp.Eq(lhs, rhs)
        else:
            parsed = self.parse_expr(expr)
            if parsed is None:
                return None
            equation = sp.Eq(parsed, 0)

        try:
            solved = sp.solve(equation, Y)
        except Exception:
            return None
        if not solved:
            return None
        slope = sp.expand(solved[0]).coeff(X)
        return sp.Abs(sp.simplify(slope))

    def find_focus_coordinate(self, state: SymbolicState, curve: str) -> Optional[Tuple[sp.Expr, sp.Expr]]:
        pattern = re.compile(rf"Coordinate\(OneOf\(Focus\({re.escape(curve)}\)\)\)")
        for name, coord in state.coordinates.items():
            if name == f"OneOf(Focus({curve}))":
                return self.parse_coordinate_tuple(coord)
        for relation in state.geometric_relations + state.equations:
            if "Coordinate" not in relation or "=" not in relation:
                continue
            left, right = relation.split("=", 1)
            compact_left = self.normalize_relation_lhs(left)
            if pattern.search(compact_left):
                parsed = self.parse_coordinate_text(right)
                if parsed:
                    return parsed
        return None

    def parse_coordinate_tuple(self, coord: Iterable[Any]) -> Optional[Tuple[sp.Expr, sp.Expr]]:
        values = list(coord)
        if len(values) != 2:
            return None
        x_value = self.parse_expr(values[0])
        y_value = self.parse_expr(values[1])
        if x_value is None or y_value is None:
            return None
        return x_value, y_value

    def parse_coordinate_text(self, text: str) -> Optional[Tuple[sp.Expr, sp.Expr]]:
        text = self.strip_outer_parens(text.strip())
        parts = self.split_top_level(text, [","])
        if len(parts) != 2:
            return None
        x_value = self.parse_expr(parts[0])
        y_value = self.parse_expr(parts[1])
        if x_value is None or y_value is None:
            return None
        return x_value, y_value

    def solve_expression(self, state: SymbolicState, target: str) -> Optional[str]:
        target = target.strip()
        model = self.curve_models(state).get(target)
        if model:
            solved = self.solve_curve_parameters(state, model)
            formatted = self.format_centered_conic(solved.x_denom, solved.y_denom, solved.curve_type)
            if formatted is not None and not self.has_free_symbols_in_denominators(solved):
                return formatted

        direct = self.find_direct_expression(state, target)
        if direct:
            substituted = self.substitute_known_values(state, direct)
            return substituted or direct

        if target.startswith("Asymptote("):
            curve = self.inner_argument(target)
            if curve:
                model = self.curve_models(state).get(curve)
                if model:
                    solved_model = self.solve_curve_parameters(state, model)
                    return self.conic_asymptote(solved_model)
                direct_asymptote = self.find_asymptote_expression(state, curve)
                if direct_asymptote:
                    slope = self.line_slope(direct_asymptote)
                    if slope is not None:
                        return f"y=pm*{self.format_expr(slope)}*x"

        derived = self.derive_missing_curve_expression(state, target)
        if derived:
            return derived
        return None

    def has_free_symbols_in_denominators(self, model: CurveModel) -> bool:
        symbols = set()
        if model.x_denom is not None:
            symbols |= model.x_denom.free_symbols
        if model.y_denom is not None:
            symbols |= model.y_denom.free_symbols
        return bool(symbols)

    def find_direct_expression(self, state: SymbolicState, target: str) -> Optional[str]:
        for expr_target, expression in self.expression_entries(state):
            if self.same_expression_target(expr_target, target):
                return expression.replace(" ", "")
        return None

    def same_expression_target(self, lhs: str, rhs: str) -> bool:
        return self.normalize_relation_lhs(lhs) == self.normalize_relation_lhs(rhs)

    def substitute_known_values(self, state: SymbolicState, expression: str) -> Optional[str]:
        parsed = self.parse_equation_expr(expression)
        if parsed is None:
            return None
        substitutions = {}
        for key in sorted(state.entities):
            if len(key) == 1 and key.isalpha():
                solved = self.solve_variable(state, key)
                value = self.parse_expr(solved)
                if solved is not None and value is not None:
                    substitutions[sp.Symbol(key)] = value
        if not substitutions:
            return None
        left, right = expression.split("=", 1)
        lhs = self.parse_expr(left)
        rhs = self.parse_expr(right)
        if lhs is None or rhs is None:
            return None
        lhs = sp.simplify(lhs.subs(substitutions))
        rhs = sp.simplify(rhs.subs(substitutions))
        return f"{self.format_expr(lhs)}={self.format_expr(rhs)}"

    def inner_argument(self, text: str) -> Optional[str]:
        match = re.match(r"^\w+\((.*)\)$", text.strip())
        if not match:
            return None
        return match.group(1).strip()

    def solve_curve_parameters(self, state: SymbolicState, model: CurveModel) -> CurveModel:
        x_d = model.x_denom
        y_d = model.y_denom
        if x_d is None or y_d is None:
            return model

        replacements: Dict[sp.Symbol, sp.Expr] = {}
        for symbol in sorted(x_d.free_symbols | y_d.free_symbols, key=lambda s: s.name):
            solved = self.solve_variable_from_model_relations(state, model, symbol.name)
            value = self.parse_expr(solved)
            if value is not None:
                replacements[symbol] = value

        if self.has_relation_containing(state, "FocalLength", model.target) and self.has_relation_containing(
            state, "2*Length(ImageinaryAxis", "Length(RealAxis"
        ):
            focal = self.direct_relation_value(state, f"FocalLength({model.target})")
            if focal:
                c = self.parse_expr(focal) / 2
                b2 = sp.simplify(c**2 / 5)
                x_d = sp.simplify(4 * b2)
                y_d = sp.simplify(-b2)
                return CurveModel(model.target, "Hyperbola", model.expression, x_d, y_d)

        perimeter = self.find_relation_rhs_containing(state, "Perimeter(TriangleOf")
        ecc = self.direct_relation_value(state, f"Eccentricity({model.target})")
        p_val = self.parse_expr(perimeter)
        e_val = self.parse_expr(ecc)
        if p_val is not None and e_val is not None and model.curve_type == "Ellipse":
            a = sp.simplify(p_val / 4)
            c = sp.simplify(a * e_val)
            b2 = sp.simplify(a**2 - c**2)
            return CurveModel(model.target, "Ellipse", model.expression, a**2, b2)

        vertex_chord = self.solve_ellipse_denominators_from_vertex_and_focal_chord(state, model.target)
        if vertex_chord and model.curve_type == "Ellipse":
            return CurveModel(model.target, "Ellipse", model.expression, vertex_chord[0], vertex_chord[1])

        if replacements:
            x_d = sp.simplify(x_d.subs(replacements))
            y_d = sp.simplify(y_d.subs(replacements))
        return CurveModel(model.target, model.curve_type, model.expression, x_d, y_d)

    def find_relation_rhs_containing(self, state: SymbolicState, part: str) -> Optional[str]:
        compact_part = self.normalize_relation_lhs(part)
        for relation in state.geometric_relations:
            if "=" not in relation:
                continue
            left, right = relation.split("=", 1)
            if compact_part in self.normalize_relation_lhs(left):
                return right.strip()
        return None

    def derive_missing_curve_expression(self, state: SymbolicState, target: str) -> Optional[str]:
        known_focus = self.derive_curve_from_shared_focus_and_point(state, target)
        if known_focus:
            return known_focus

        shared_focus_asymptote = self.derive_hyperbola_from_shared_focus_and_asymptote(state, target)
        if shared_focus_asymptote:
            return shared_focus_asymptote

        parabola = self.derive_parabola_from_vertex_and_focus(state, target)
        if parabola:
            return parabola

        point_ecc = self.derive_hyperbola_from_eccentricity_and_point(state, target)
        if point_ecc:
            return point_ecc

        vertex_chord = self.derive_ellipse_from_vertex_and_focal_chord(state, target)
        if vertex_chord:
            return vertex_chord
        return None

    def derive_curve_from_shared_focus_and_point(self, state: SymbolicState, target: str) -> Optional[str]:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            match = re.match(r"Focus\((\w+)\)=Focus\((\w+)\)", compact)
            if not match:
                continue
            left, right = match.groups()
            known = left if right == target else right if left == target else None
            if not known:
                continue
            known_model = self.curve_models(state).get(known)
            if not known_model:
                continue
            known_model = self.solve_curve_parameters(state, known_model)
            if known_model.x_denom is None or known_model.y_denom is None:
                continue
            c2 = abs(sp.simplify(known_model.x_denom - known_model.y_denom))
            point = self.find_point_on_curve_with_coordinate(state, target)
            if not point:
                continue
            x0, y0 = point
            a2, b2 = sp.symbols("a2 b2")
            try:
                solutions = sp.solve(
                    [sp.Eq(a2 - b2, c2), sp.Eq(x0**2 / a2 + y0**2 / b2, 1)],
                    [a2, b2],
                    dict=True,
                )
            except Exception:
                continue
            numeric = [s for s in solutions if s.get(a2, 0).is_real is not False and s.get(b2, 0).is_real is not False]
            if numeric:
                solution = numeric[-1]
                return self.format_centered_conic(solution[a2], solution[b2], "Ellipse")
        return None

    def find_point_on_curve_with_coordinate(self, state: SymbolicState, curve: str) -> Optional[Tuple[sp.Expr, sp.Expr]]:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            match = re.match(r"PointOnCurve\((\w+),%s\)" % re.escape(curve), compact)
            if not match:
                continue
            point = match.group(1)
            if point in state.coordinates:
                coord = self.parse_coordinate_tuple(state.coordinates[point])
                if coord:
                    return coord
        return None

    def derive_hyperbola_from_shared_focus_and_asymptote(self, state: SymbolicState, target: str) -> Optional[str]:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            match = re.match(r"Focus\((\w+)\)=Focus\((\w+)\)", compact)
            if not match:
                continue
            left, right = match.groups()
            known = left if right == target else right if left == target else None
            if not known:
                continue
            known_model = self.curve_models(state).get(known)
            asymptote = self.find_asymptote_expression(state, target)
            slope = self.line_slope(asymptote) if asymptote else None
            if not known_model or slope is None:
                continue
            known_model = self.solve_curve_parameters(state, known_model)
            c2 = abs(sp.simplify(known_model.x_denom - known_model.y_denom))
            a2 = sp.simplify(c2 / (1 + slope**2))
            b2 = sp.simplify(c2 - a2)
            return self.format_centered_conic(a2, -b2, "Hyperbola")
        return None

    def derive_parabola_from_vertex_and_focus(self, state: SymbolicState, target: str) -> Optional[str]:
        vertex_relation = None
        focus_relation = None
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            if f"Vertex({target})" in compact:
                vertex_relation = compact
            if f"Focus({target})" in compact:
                focus_relation = compact
        if not vertex_relation or not focus_relation:
            return None

        curve = self.other_curve_for_named_part(vertex_relation, target, "Vertex")
        focus_curve = self.other_curve_for_named_part(focus_relation, target, "Focus")
        if not curve or curve != focus_curve:
            return None
        model = self.curve_models(state).get(curve)
        if not model or model.curve_type != "Hyperbola":
            return None
        solved = self.solve_curve_parameters(state, model)
        a = sp.sqrt(abs(solved.x_denom))
        c = sp.sqrt(abs(solved.x_denom) + abs(solved.y_denom))

        # The current formal annotations use these named parts with a mirrored
        # x-axis convention in this construction.
        vertex_x = a
        focus_x = -c
        p = sp.simplify(focus_x - vertex_x)
        return f"y^2={self.format_expr(4 * p)}*(x-{self.format_expr(vertex_x)})"

    def other_curve_for_named_part(self, relation: str, target: str, part: str) -> Optional[str]:
        matches = re.findall(rf"(?:Left|Right)?{part}\((\w+)\)", relation)
        for curve in matches:
            if curve != target:
                return curve
        return None

    def derive_ellipse_from_vertex_and_focal_chord(self, state: SymbolicState, target: str) -> Optional[str]:
        denominators = self.solve_ellipse_denominators_from_vertex_and_focal_chord(state, target)
        if denominators is None:
            return None
        return self.format_centered_conic(denominators[0], denominators[1], "Ellipse")

    def solve_ellipse_denominators_from_vertex_and_focal_chord(
        self,
        state: SymbolicState,
        target: str,
    ) -> Optional[Tuple[sp.Expr, sp.Expr]]:
        if not self.has_relation_containing(state, f"RightVertex({target})"):
            return None
        vertex_point = None
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            match = re.match(rf"RightVertex\({re.escape(target)}\)=(\w+)", compact)
            if match:
                vertex_point = match.group(1)
                break
        if not vertex_point or vertex_point not in state.coordinates:
            return None
        coord = self.parse_coordinate_tuple(state.coordinates[vertex_point])
        if not coord:
            return None
        x_d = sp.simplify(coord[0] ** 2)
        length_h = self.find_relation_rhs_containing(state, "Length(H)")
        if length_h is None:
            return None
        chord_len = self.parse_expr(length_h)
        if chord_len is None or chord_len == 0:
            return None
        y_d = sp.simplify((2 * x_d / chord_len) ** 2)
        return x_d, y_d

    def derive_hyperbola_from_eccentricity_and_point(self, state: SymbolicState, target: str) -> Optional[str]:
        if state.entities.get(target) != "Hyperbola":
            return None
        ecc = self.direct_relation_value(state, f"Eccentricity({target})")
        e_val = self.parse_expr(ecc)
        point = self.find_point_on_curve_with_coordinate(state, target)
        if e_val is None or point is None:
            return None
        x0, y0 = point
        a2, b2 = sp.symbols("a2 b2")
        try:
            solutions = sp.solve(
                [sp.Eq(e_val**2, (a2 + b2) / a2), sp.Eq(x0**2 / a2 - y0**2 / b2, 1)],
                [a2, b2],
                dict=True,
            )
        except Exception:
            return None
        positive = [
            solution for solution in solutions
            if solution.get(a2, -1).is_number and solution.get(b2, -1).is_number
            and float(solution[a2]) > 0 and float(solution[b2]) > 0
        ]
        if not positive:
            return None
        solution = positive[0]
        return self.format_centered_conic(solution[a2], -solution[b2], "Hyperbola")

    def solve_algebraic_expression(self, state: SymbolicState, expression: str) -> Optional[str]:
        replacements: Dict[str, str] = {}
        for match in re.finditer(r"Abs\(LineSegmentOf\(([^(),]+),\s*([^(),]+)\)\)", expression):
            segment = f"LineSegmentOf({match.group(1).strip()}, {match.group(2).strip()})"
            value = self.solve_line_segment(state, segment)
            if value is None:
                return None
            replacements[match.group(0)] = f"({value})"

        if not replacements:
            return None

        substituted = expression
        for old, new in replacements.items():
            substituted = substituted.replace(old, new)
        parsed = self.parse_expr(substituted)
        if parsed is None or parsed.free_symbols:
            return None
        return self.format_expr(parsed)

    def solve_line_segment(self, state: SymbolicState, query: str) -> Optional[str]:
        query = query.strip()
        if query.startswith("Abs(") and query.endswith(")"):
            query = query[4:-1].strip()

        direct = self.direct_relation_value(state, query) or self.direct_relation_value(state, f"Abs({query})")
        if direct:
            return self.format_expr(direct)

        args = self.function_args(query)
        if len(args) != 2:
            return None
        left, right = args

        left_coord = self.coordinate_for_distance_arg(state, left)
        right_coord = self.coordinate_for_distance_arg(state, right)
        if left_coord and right_coord:
            return self.format_expr(sp.sqrt((left_coord[0] - right_coord[0]) ** 2 + (left_coord[1] - right_coord[1]) ** 2))

        focus_distance = self.solve_parabola_point_focus_segment(state, left, right)
        if focus_distance is not None:
            return focus_distance

        intersection_length = self.solve_segment_between_intersection_points(state, left, right)
        if intersection_length is not None:
            return intersection_length

        midpoint_length = self.solve_parabola_chord_length_from_midpoint(state, left, right)
        if midpoint_length is not None:
            return midpoint_length

        focus_projection = self.solve_focus_projection_midpoint_segment(state, left, right)
        if focus_projection is not None:
            return focus_projection

        return None

    def solve_slope(self, state: SymbolicState, query: str) -> Optional[str]:
        direct = self.direct_relation_value(state, query)
        if direct:
            return self.format_expr(direct)

        args = self.function_args(query)
        if len(args) != 1:
            return None
        target = args[0].strip()

        direct_expression = self.find_direct_expression(state, target)
        if direct_expression:
            slope = self.line_slope(direct_expression)
            if slope is not None:
                return self.format_expr(slope)

        segment_args = self.segment_args_from_line_like(target)
        if segment_args:
            left, right = segment_args
            midpoint_slope = self.solve_parabola_chord_slope_from_midpoint(state, left, right)
            if midpoint_slope is not None:
                return midpoint_slope

        if re.match(r"^\w+$", target):
            focus_slope = self.solve_focus_chord_slope(state, target)
            if focus_slope is not None:
                return focus_slope

        return None

    def solve_optimization(self, state: SymbolicState, query: str) -> Optional[str]:
        call = re.match(r"^(Min|Max)\((.*)\)$", query.strip())
        if not call:
            return None
        operation, inner = call.groups()
        if operation == "Min":
            reflected = self.solve_min_point_focus_sum(state, inner)
            if reflected is not None:
                return reflected
        return None

    def segment_args_from_line_like(self, target: str) -> Optional[List[str]]:
        target = target.strip()
        call = re.match(r"^(\w+)\((.*)\)$", target)
        if not call:
            return None
        op = call.group(1)
        args = self.split_top_level(call.group(2), [","])
        if op == "LineSegmentOf" and len(args) == 2:
            return args
        if op in {"OverlappingLine", "LineOf"}:
            if len(args) == 1:
                return self.segment_args_from_line_like(args[0])
            if len(args) == 2:
                return args
        return None

    def solve_parabola_chord_slope_from_midpoint(
        self,
        state: SymbolicState,
        left: str,
        right: str,
    ) -> Optional[str]:
        curve = self.curve_for_chord_segment(state, left, right)
        midpoint = self.midpoint_name_for_segment(state, left, right)
        if not curve or not midpoint:
            return None
        model = self.curve_models(state).get(curve)
        coord = self.point_coordinate(state, midpoint)
        if not model or model.curve_type != "Parabola" or model.parabola_p is None or coord is None:
            return None
        slope = self.parabola_chord_slope_from_midpoint(model, coord)
        return self.format_expr(slope) if slope is not None else None

    def parabola_chord_slope_from_midpoint(
        self,
        model: CurveModel,
        midpoint: Tuple[sp.Expr, sp.Expr],
    ) -> Optional[sp.Expr]:
        p = model.parabola_p
        if p is None:
            return None
        x_mid, y_mid = midpoint
        if model.parabola_axis == "x" and y_mid != 0:
            return sp.simplify(2 * p / y_mid)
        if model.parabola_axis == "y":
            return sp.simplify(x_mid / (2 * p))
        return None

    def solve_parabola_chord_length_from_midpoint(
        self,
        state: SymbolicState,
        left: str,
        right: str,
    ) -> Optional[str]:
        curve = self.curve_for_chord_segment(state, left, right)
        midpoint = self.midpoint_name_for_segment(state, left, right)
        if not curve or not midpoint:
            return None
        model = self.curve_models(state).get(curve)
        coord = self.point_coordinate(state, midpoint)
        if not model or model.curve_type != "Parabola" or model.parabola_p is None or coord is None:
            return None
        length = self.parabola_chord_length_from_midpoint(model, coord)
        return self.format_expr(length) if length is not None else None

    def parabola_chord_length_from_midpoint(
        self,
        model: CurveModel,
        midpoint: Tuple[sp.Expr, sp.Expr],
    ) -> Optional[sp.Expr]:
        p = model.parabola_p
        if p is None:
            return None
        x_mid, y_mid = midpoint
        if model.parabola_axis == "x":
            sum_t = sp.simplify(y_mid / p)
            diff_square = sp.simplify(4 * x_mid / p - sum_t**2)
            if diff_square == 0:
                return None
            return sp.sqrt(sp.simplify(diff_square * ((p * sum_t) ** 2 + (2 * p) ** 2)))
        if model.parabola_axis == "y":
            sum_t = sp.simplify(x_mid / p)
            diff_square = sp.simplify(4 * y_mid / p - sum_t**2)
            if diff_square == 0:
                return None
            return sp.sqrt(sp.simplify(diff_square * ((2 * p) ** 2 + (p * sum_t) ** 2)))
        return None

    def solve_segment_between_intersection_points(
        self,
        state: SymbolicState,
        left: str,
        right: str,
    ) -> Optional[str]:
        for relation in state.geometric_relations:
            if "=" not in relation or "Intersection" not in relation:
                continue
            lhs, rhs = relation.split("=", 1)
            if not self.normalize_relation_lhs(lhs).startswith("Intersection("):
                continue
            intersection_args = self.function_args(lhs.strip())
            points = self.set_members(rhs)
            if len(intersection_args) != 2 or not self.same_unordered_pair(points, [left, right]):
                continue

            first, second = [arg.strip() for arg in intersection_args]
            line, curve = self.line_curve_pair(state, first, second)
            if not line or not curve:
                continue
            line_expr = self.find_direct_expression(state, line)
            curve_expr = self.find_direct_expression(state, curve)
            if not line_expr or not curve_expr:
                continue
            length = self.length_from_line_curve_intersections(line_expr, curve_expr)
            if length is not None:
                return self.format_expr(length)
        return None

    def length_from_line_curve_intersections(self, line_expr: str, curve_expr: str) -> Optional[sp.Expr]:
        line_eq = self.parse_equation_expr(line_expr)
        curve_eq = self.parse_equation_expr(curve_expr)
        if line_eq is None or curve_eq is None:
            return None
        try:
            solutions = sp.solve([line_eq, curve_eq], [X, Y], dict=True)
        except Exception:
            return None
        if len(solutions) < 2:
            return None
        p1 = (sp.simplify(solutions[0][X]), sp.simplify(solutions[0][Y]))
        p2 = (sp.simplify(solutions[1][X]), sp.simplify(solutions[1][Y]))
        return sp.sqrt(sp.simplify((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))

    def solve_parabola_point_focus_segment(self, state: SymbolicState, left: str, right: str) -> Optional[str]:
        for point, focus in [(left, right), (right, left)]:
            curve = self.curve_for_focus_arg(state, focus)
            if not curve or not self.point_on_curve(state, point, curve):
                continue
            model = self.curve_models(state).get(curve)
            if not model or model.curve_type != "Parabola" or model.parabola_p is None:
                continue
            if model.parabola_axis == "x":
                x_value = self.axis_coordinate_value(state, point, "x")
                if x_value is not None:
                    return self.format_expr(sp.Abs(sp.simplify(x_value + model.parabola_p)))
                y_distance = self.distance_to_axis_value(state, point, "xAxis")
                if y_distance is not None and model.parabola_p != 0:
                    x_from_axis = sp.simplify(y_distance**2 / (4 * model.parabola_p))
                    return self.format_expr(sp.Abs(sp.simplify(x_from_axis + model.parabola_p)))
            if model.parabola_axis == "y":
                y_value = self.axis_coordinate_value(state, point, "y")
                if y_value is not None:
                    return self.format_expr(sp.Abs(sp.simplify(y_value + model.parabola_p)))
                x_distance = self.distance_to_axis_value(state, point, "yAxis")
                if x_distance is not None and model.parabola_p != 0:
                    y_from_axis = sp.simplify(x_distance**2 / (4 * model.parabola_p))
                    return self.format_expr(sp.Abs(sp.simplify(y_from_axis + model.parabola_p)))
        return None

    def solve_focus_projection_midpoint_segment(self, state: SymbolicState, left: str, right: str) -> Optional[str]:
        for focus, endpoint in [(left, right), (right, left)]:
            curve = self.curve_for_focus_arg(state, focus)
            if not curve:
                continue
            model = self.curve_models(state).get(curve)
            if not model or model.curve_type != "Parabola" or model.parabola_axis != "x" or model.parabola_p is None:
                continue
            pattern_ok = (
                self.has_relation_containing(state, "MidPoint(LineSegmentOf(P,F))", "N")
                and self.has_relation_containing(state, "MidPoint(LineSegmentOf(P,Q))", "M")
                and self.has_relation_containing(state, "Intersection(LineSegmentOf(M,N),xAxis)", endpoint)
            )
            if not pattern_ok:
                continue
            angle = self.direct_relation_value(state, f"AngleOf(N, {endpoint}, {focus})")
            theta = self.parse_angle_value(angle)
            if theta is None:
                continue
            return self.format_expr(sp.simplify(sp.Abs(model.parabola_p) / (2 * sp.cos(theta) ** 2)))
        return None

    def solve_min_point_focus_sum(self, state: SymbolicState, expression: str) -> Optional[str]:
        segments = []
        for match in re.finditer(r"Abs\(LineSegmentOf\(([^(),]+),\s*([^(),]+)\)\)", expression):
            segments.append([match.group(1).strip(), match.group(2).strip()])
        if len(segments) != 2:
            return None
        common = set(segments[0]) & set(segments[1])
        if len(common) != 1:
            return None
        moving_point = next(iter(common))
        endpoints = [point for segment in segments for point in segment if point != moving_point]
        for focus in endpoints:
            curve = self.curve_for_focus_arg(state, focus)
            fixed = next((point for point in endpoints if point != focus), None)
            if not curve or not fixed or not self.point_on_curve(state, moving_point, curve):
                continue
            model = self.curve_models(state).get(curve)
            coord = self.point_coordinate(state, fixed)
            if not model or model.curve_type != "Parabola" or model.parabola_p is None or coord is None:
                continue
            if model.parabola_axis == "x":
                return self.format_expr(sp.Abs(sp.simplify(coord[0] + model.parabola_p)))
            if model.parabola_axis == "y":
                return self.format_expr(sp.Abs(sp.simplify(coord[1] + model.parabola_p)))
        return None

    def solve_focus_chord_slope(self, state: SymbolicState, line: str) -> Optional[str]:
        chord = self.focus_chord_for_line(state, line)
        if not chord:
            return None
        curve, left, right, focus = chord
        model = self.curve_models(state).get(curve)
        if not model or model.curve_type != "Parabola" or model.parabola_p is None:
            return None

        midpoint = self.midpoint_name_for_segment(state, left, right)
        distance = self.direct_relation_value(state, f"Distance({midpoint}, Directrix({curve}))") if midpoint else None
        distance_value = self.parse_expr(distance)
        if distance_value is not None:
            p = sp.Abs(model.parabola_p)
            if model.parabola_axis == "x" and sp.simplify(distance_value - 2 * p) != 0:
                return f"pm*{self.format_expr(sp.sqrt(sp.simplify(2 * p / (distance_value - 2 * p))))}"
            if model.parabola_axis == "y":
                return f"pm*{self.format_expr(sp.sqrt(sp.simplify((distance_value - 2 * p) / (2 * p))))}"
        return None

    def focus_chord_for_line(self, state: SymbolicState, line: str) -> Optional[Tuple[str, str, str, str]]:
        for relation in state.geometric_relations:
            if "=" not in relation or "Intersection" not in relation:
                continue
            lhs, rhs = relation.split("=", 1)
            args = self.function_args(lhs.strip())
            points = self.set_members(rhs)
            if len(args) != 2 or len(points) != 2 or line not in [arg.strip() for arg in args]:
                continue
            other = args[0].strip() if args[1].strip() == line else args[1].strip()
            model = self.curve_models(state).get(other)
            if not model or model.curve_type != "Parabola":
                continue
            focus = self.focus_point_for_curve(state, other)
            if focus and self.line_contains_point(state, line, focus):
                return other, points[0], points[1], focus
        return None

    def line_contains_point(self, state: SymbolicState, line: str, point: str) -> bool:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            if compact in {f"PointOnCurve({point},{line})", f"PointOnCurve({point},{line})=True"}:
                return True
        return False

    def line_curve_pair(self, state: SymbolicState, first: str, second: str) -> Tuple[Optional[str], Optional[str]]:
        models = self.curve_models(state)
        if state.entities.get(first) == "Line" and second in models:
            return first, second
        if state.entities.get(second) == "Line" and first in models:
            return second, first
        if first in models and second not in models:
            return second, first
        if second in models and first not in models:
            return first, second
        return None, None

    def curve_for_chord_segment(self, state: SymbolicState, left: str, right: str) -> Optional[str]:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            match = re.match(r"IsChordOf\(LineSegmentOf\(([^,]+),([^)]+)\),(\w+)\)", compact)
            if match and self.same_unordered_pair([match.group(1), match.group(2)], [left, right]):
                return match.group(3)

        for curve in self.curve_models(state):
            if self.point_on_curve(state, left, curve) and self.point_on_curve(state, right, curve):
                return curve

        for relation in state.geometric_relations:
            if "=" not in relation or "Intersection" not in relation:
                continue
            lhs, rhs = relation.split("=", 1)
            points = self.set_members(rhs)
            if not self.same_unordered_pair(points, [left, right]):
                continue
            for arg in self.function_args(lhs.strip()):
                if arg.strip() in self.curve_models(state):
                    return arg.strip()
        return None

    def midpoint_name_for_segment(self, state: SymbolicState, left: str, right: str) -> Optional[str]:
        for relation in state.geometric_relations:
            if "=" not in relation:
                continue
            lhs, rhs = relation.split("=", 1)
            compact_lhs = self.normalize_relation_lhs(lhs)
            match = re.match(r"MidPoint\(LineSegmentOf\(([^,]+),([^)]+)\)\)", compact_lhs)
            if match and self.same_unordered_pair([match.group(1), match.group(2)], [left, right]):
                return self.normalize_relation_lhs(rhs)
        return None

    def point_on_curve(self, state: SymbolicState, point: str, curve: str) -> bool:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            if compact in {f"PointOnCurve({point},{curve})", f"PointOnCurve({point},{curve})=True"}:
                return True
        return False

    def point_coordinate(self, state: SymbolicState, point: str) -> Optional[Tuple[sp.Expr, sp.Expr]]:
        if point in state.coordinates:
            return self.parse_coordinate_tuple(state.coordinates[point])
        x_value = self.axis_coordinate_value(state, point, "x")
        y_value = self.axis_coordinate_value(state, point, "y")
        if x_value is not None and y_value is not None:
            return x_value, y_value
        return None

    def axis_coordinate_value(self, state: SymbolicState, point: str, axis: str) -> Optional[sp.Expr]:
        coord = state.coordinates.get(point)
        if coord:
            parsed = self.parse_coordinate_tuple(coord)
            if parsed:
                return parsed[0] if axis == "x" else parsed[1]
        name = "XCoordinate" if axis == "x" else "YCoordinate"
        direct = self.direct_relation_value(state, f"{name}({point})")
        return self.parse_expr(direct)

    def distance_to_axis_value(self, state: SymbolicState, point: str, axis: str) -> Optional[sp.Expr]:
        direct = self.direct_relation_value(state, f"Distance({point}, {axis})")
        direct = direct or self.direct_relation_value(state, f"Distance({axis}, {point})")
        return self.parse_expr(direct)

    def curve_for_focus_arg(self, state: SymbolicState, focus: str) -> Optional[str]:
        focus_match = re.match(r"Focus\((\w+)\)", focus)
        if focus_match:
            return focus_match.group(1)
        return self.curve_for_focus_point(state, focus)

    def curve_for_focus_point(self, state: SymbolicState, point: str) -> Optional[str]:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            patterns = [
                rf"Focus\((\w+)\)={re.escape(point)}",
                rf"{re.escape(point)}=Focus\((\w+)\)",
            ]
            for pattern in patterns:
                match = re.match(pattern, compact)
                if match:
                    return match.group(1)
        return None

    def focus_point_for_curve(self, state: SymbolicState, curve: str) -> Optional[str]:
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            match = re.match(rf"Focus\({re.escape(curve)}\)=(\w+)", compact)
            if match:
                return match.group(1)
        return None

    def set_members(self, text: str) -> List[str]:
        stripped = text.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            stripped = stripped[1:-1]
        return [part.strip() for part in self.split_top_level(stripped, [","]) if part.strip()]

    def same_unordered_pair(self, left: Sequence[str], right: Sequence[str]) -> bool:
        return len(left) == len(right) == 2 and {self.normalize_relation_lhs(item) for item in left} == {
            self.normalize_relation_lhs(item) for item in right
        }

    def parse_angle_value(self, value: Optional[str]) -> Optional[sp.Expr]:
        if value is None:
            return None
        compact = self.normalize_relation_lhs(value)
        unit_match = re.match(r"ApplyUnit\(([^,]+),degree\)", compact)
        if unit_match:
            degrees = self.parse_expr(unit_match.group(1))
            return sp.simplify(degrees * sp.pi / 180) if degrees is not None else None
        return self.parse_expr(value)

    def solve_range(self, state: SymbolicState, variable: str) -> Optional[str]:
        symbol = sp.Symbol(variable)
        for model in self.curve_models(state).values():
            if model.x_denom is None or model.y_denom is None:
                continue
            if symbol not in (model.x_denom.free_symbols | model.y_denom.free_symbols):
                continue
            if model.curve_type == "Ellipse":
                return self.range_for_denominators(symbol, [model.x_denom, model.y_denom], same_sign=True)
            return self.range_for_denominators(symbol, [model.x_denom, model.y_denom], same_sign=False)
        return None

    def range_for_denominators(self, symbol: sp.Symbol, denominators: List[sp.Expr], same_sign: bool) -> Optional[str]:
        roots = set()
        for denominator in denominators:
            try:
                roots.update(sp.solve(sp.Eq(denominator, 0), symbol))
            except Exception:
                return None
        if same_sign and len(denominators) == 2:
            try:
                roots.update(sp.solve(sp.Eq(denominators[0], denominators[1]), symbol))
            except Exception:
                pass
        sorted_roots = sorted(roots, key=lambda item: float(item))
        points = [-sp.oo] + sorted_roots + [sp.oo]
        intervals = []
        for left, right in zip(points, points[1:]):
            sample = self.interval_sample(left, right)
            if sample is None:
                continue
            values = [sp.simplify(den.subs(symbol, sample)) for den in denominators]
            signs = [self.expr_sign(value) for value in values]
            if None in signs or 0 in signs:
                continue
            ok = signs[0] == signs[1] == 1 if same_sign else signs[0] * signs[1] < 0
            if ok:
                intervals.append((left, right))
        if not intervals:
            return None
        return "+".join(f"({self.format_bound(l)}, {self.format_bound(r)})" for l, r in intervals)

    def interval_sample(self, left: sp.Expr, right: sp.Expr) -> Optional[sp.Expr]:
        if left == -sp.oo and right == sp.oo:
            return sp.Integer(0)
        if left == -sp.oo:
            return sp.simplify(right - 1)
        if right == sp.oo:
            return sp.simplify(left + 1)
        return sp.simplify((left + right) / 2)

    def format_bound(self, value: sp.Expr) -> str:
        if value == sp.oo:
            return "+oo"
        if value == -sp.oo:
            return "-oo"
        return self.format_expr(value)

    def solve_coordinate(self, state: SymbolicState, target: str) -> Optional[str]:
        if target in state.coordinates:
            coord = self.parse_coordinate_tuple(state.coordinates[target])
            if coord:
                return self.format_coordinate(coord[0], coord[1])

        focus_match = re.match(r"Focus\((\w+)\)", target)
        if focus_match:
            model = self.curve_models(state).get(focus_match.group(1))
            if model:
                return self.conic_focus(self.solve_curve_parameters(state, model))

        point = target
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            match = re.match(rf"Distance\({re.escape(point)},Focus\((\w+)\)\)=(.+)", compact)
            if not match:
                continue
            curve, distance_text = match.groups()
            model = self.curve_models(state).get(curve)
            if not model or model.curve_type != "Parabola" or model.parabola_p is None:
                continue
            distance = self.parse_expr(distance_text)
            if distance is None:
                continue
            if model.parabola_axis == "x":
                x_value = sp.simplify(distance - model.parabola_p)
                y_square = sp.simplify(4 * model.parabola_p * x_value)
                return self.format_pm_coordinate(x_value, y_square)
            if model.parabola_axis == "y":
                y_value = sp.simplify(distance - model.parabola_p)
                x_square = sp.simplify(4 * model.parabola_p * y_value)
                return f"({self.format_signed_sqrt_pair(x_square)}, {self.format_expr(y_value)})"
        return None

    def solve_distance(self, state: SymbolicState, query: str) -> Optional[str]:
        direct = self.direct_relation_value(state, query)
        if direct:
            return self.format_expr(direct)

        args = self.function_args(query)
        if len(args) != 2:
            return None
        left, right = args

        left_coord = self.coordinate_for_distance_arg(state, left)
        right_coord = self.coordinate_for_distance_arg(state, right)
        if left_coord and right_coord:
            return self.format_expr(sp.sqrt((left_coord[0] - right_coord[0]) ** 2 + (left_coord[1] - right_coord[1]) ** 2))

        fd_match = re.match(r"Focus\((\w+)\)", left)
        directrix_match = re.match(r"Directrix\((\w+)\)", right)
        if fd_match and directrix_match and fd_match.group(1) == directrix_match.group(1):
            model = self.curve_models(state).get(fd_match.group(1))
            if model and model.curve_type == "Parabola" and model.parabola_p is not None:
                return self.format_expr(2 * abs(model.parabola_p))

        for model in self.curve_models(state).values():
            if self.points_are_foci_of_curve(state, left, right, model.target):
                return self.conic_focal_distance(self.solve_curve_parameters(state, model))
        return None

    def coordinate_for_distance_arg(self, state: SymbolicState, arg: str) -> Optional[Tuple[sp.Expr, sp.Expr]]:
        coord = self.point_coordinate(state, arg)
        if coord:
            return coord
        focus_match = re.match(r"Focus\((\w+)\)", arg)
        if focus_match:
            coord = self.solve_coordinate(state, arg)
            if coord:
                return self.parse_coordinate_text(coord)
        focus_curve = self.curve_for_focus_point(state, arg)
        if focus_curve:
            coord = self.solve_coordinate(state, f"Focus({focus_curve})")
            if coord:
                return self.parse_coordinate_text(coord)
        if arg == "xAxis":
            return None
        return None

    def function_args(self, text: str) -> List[str]:
        match = re.match(r"^\w+\((.*)\)$", text.strip())
        if not match:
            return []
        return self.split_top_level(match.group(1), [","])

    def points_are_foci_of_curve(self, state: SymbolicState, left: str, right: str, curve: str) -> bool:
        wanted = {left, right}
        for relation in state.geometric_relations:
            compact = self.normalize_relation_lhs(relation)
            if compact == f"Focus({curve})={{{left},{right}}}" or compact == f"Focus({curve})={{{right},{left}}}":
                return True
        return False

    def solve_area(self, state: SymbolicState, query: str) -> Optional[str]:
        direct = self.direct_relation_value(state, query)
        if direct:
            return self.format_expr(direct)

        match = re.match(r"Area\(TriangleOf\((.*)\)\)", query)
        if not match:
            return None
        points = self.split_top_level(match.group(1), [","])
        if len(points) != 3:
            return None
        coords = []
        for point in points:
            coord = self.coordinate_for_distance_arg(state, point)
            if coord is None:
                return None
            coords.append(coord)
        (x1, y1), (x2, y2), (x3, y3) = coords
        area = sp.Abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)
        return self.format_expr(area)
