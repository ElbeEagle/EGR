"""Conservative Conic10K fact adapter for the v2 information space."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from .expressions import add, div, mul, neg, number, sub
from .schema import PolynomialEquation, Term
from .state import InformationState


@dataclass(frozen=True)
class AdaptationResult:
    state: InformationState
    unparsed_facts: Tuple[str, ...]
    errors: Tuple[str, ...]


class _Polynomial:
    def __init__(self, terms: Optional[Dict[Tuple[int, int], Any]] = None):
        self.terms = {
            monomial: coefficient
            for monomial, coefficient in (terms or {}).items()
            if coefficient != 0
        }

    @classmethod
    def scalar(cls, value: Any) -> "_Polynomial":
        return cls({(0, 0): value})

    @classmethod
    def variable(cls, name: str) -> "_Polynomial":
        return cls({(1, 0): 1}) if name == "x" else cls({(0, 1): 1})

    def scalar_value(self) -> Optional[Any]:
        if not self.terms:
            return Fraction(0)
        if set(self.terms) == {(0, 0)}:
            return self.terms[(0, 0)]
        return None

    def add(self, other: "_Polynomial") -> "_Polynomial":
        keys = set(self.terms) | set(other.terms)
        return _Polynomial(
            {
                key: add(self.terms.get(key, 0), other.terms.get(key, 0))
                for key in keys
            }
        )

    def neg(self) -> "_Polynomial":
        return _Polynomial({key: neg(value) for key, value in self.terms.items()})

    def mul(self, other: "_Polynomial") -> "_Polynomial":
        result: Dict[Tuple[int, int], Any] = {}
        for (x1, y1), left in self.terms.items():
            for (x2, y2), right in other.terms.items():
                monomial = (x1 + x2, y1 + y2)
                if sum(monomial) > 2:
                    raise ValueError("polynomial degree exceeds two")
                result[monomial] = add(
                    result.get(monomial, 0), mul(left, right)
                )
        return _Polynomial(result)

    def divide(self, other: "_Polynomial") -> "_Polynomial":
        denominator = other.scalar_value()
        if denominator is None:
            raise ValueError("division by a non-scalar expression")
        return _Polynomial(
            {key: div(value, denominator) for key, value in self.terms.items()}
        )

    def power(self, exponent: int) -> "_Polynomial":
        if exponent == 0:
            return _Polynomial.scalar(1)
        if exponent == 1:
            return self
        if exponent == 2:
            return self.mul(self)
        scalar = self.scalar_value()
        if scalar is None:
            raise ValueError("unsupported polynomial exponent")
        return _Polynomial.scalar(Term("pow", (scalar, exponent)))

    def to_equation(self) -> PolynomialEquation:
        return PolynomialEquation(
            x2=self.terms.get((2, 0), 0),
            xy=self.terms.get((1, 1), 0),
            y2=self.terms.get((0, 2), 0),
            x=self.terms.get((1, 0), 0),
            y=self.terms.get((0, 1), 0),
            constant=self.terms.get((0, 0), 0),
        )


class _ExpressionParser:
    def parse_equation(self, text: str) -> PolynomialEquation:
        left_text, right_text = self._split_equation(text)
        left = self._visit(ast.parse(self._pythonize(left_text), mode="eval").body)
        right = self._visit(ast.parse(self._pythonize(right_text), mode="eval").body)
        return left.add(right.neg()).to_equation()

    @staticmethod
    def _pythonize(text: str) -> str:
        return text.strip().replace("^", "**")

    @staticmethod
    def _split_equation(text: str) -> Tuple[str, str]:
        depth = 0
        for index, character in enumerate(text):
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
            elif character == "=" and depth == 0:
                return text[:index], text[index + 1 :]
        raise ValueError("equation has no top-level equals sign")

    def _visit(self, node: ast.AST) -> _Polynomial:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return _Polynomial.scalar(number(node.value))
        if isinstance(node, ast.Name):
            if node.id in {"x", "y"}:
                return _Polynomial.variable(node.id)
            return _Polynomial.scalar(Term("symbol", (node.id,)))
        if isinstance(node, ast.UnaryOp):
            operand = self._visit(node.operand)
            if isinstance(node.op, ast.USub):
                return operand.neg()
            if isinstance(node.op, ast.UAdd):
                return operand
        if isinstance(node, ast.BinOp):
            left = self._visit(node.left)
            right = self._visit(node.right)
            if isinstance(node.op, ast.Add):
                return left.add(right)
            if isinstance(node.op, ast.Sub):
                return left.add(right.neg())
            if isinstance(node.op, ast.Mult):
                return left.mul(right)
            if isinstance(node.op, ast.Div):
                return left.divide(right)
            if isinstance(node.op, ast.Pow):
                exponent = right.scalar_value()
                if isinstance(exponent, Fraction) and exponent.denominator == 1:
                    return left.power(int(exponent))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            arguments = [self._visit(argument).scalar_value() for argument in node.args]
            if any(argument is None for argument in arguments):
                raise ValueError("function contains x or y")
            return _Polynomial.scalar(Term(node.func.id, tuple(arguments)))
        raise ValueError(f"unsupported expression node: {ast.dump(node)}")


class RawFactAdapter:
    """Parse a useful subset and preserve every unsupported fact explicitly."""

    DECLARATION = re.compile(r"^(\w+)\s*:\s*(\w+)$")
    EXPRESSION = re.compile(r"^Expression\((\w+)\)\s*=\s*\((.*)\)$")
    COORDINATE = re.compile(r"^Coordinate\((\w+)\)\s*=\s*\((.*),(.*)\)$")
    POINT_ON_CURVE = re.compile(r"^PointOnCurve\((\w+),\s*(\w+)\)(?:\s*=\s*True)?$")
    NAMED_RELATION = re.compile(
        r"^(Focus|LeftFocus|RightFocus|Directrix)\((\w+)\)\s*=\s*(\w+)$"
    )

    def __init__(self):
        self.expression_parser = _ExpressionParser()

    def adapt(
        self,
        fact_expressions: str,
        query_expressions: Optional[str] = None,
    ) -> AdaptationResult:
        state = InformationState()
        unparsed: List[str] = []
        errors: List[str] = []
        raw_facts = [fact.strip() for fact in fact_expressions.split(";") if fact.strip()]

        for fact in raw_facts:
            match = self.DECLARATION.match(fact)
            if match:
                try:
                    state.declare(match.group(1), match.group(2))
                except ValueError as exc:
                    errors.append(str(exc))
                continue

            match = self.EXPRESSION.match(fact)
            if match:
                try:
                    polynomial = self.expression_parser.parse_equation(match.group(2))
                    state.add_given(
                        "ExpressionPolynomial",
                        match.group(1),
                        value=polynomial,
                        raw_expression=fact,
                    )
                except (SyntaxError, ValueError, ZeroDivisionError) as exc:
                    errors.append(f"{fact}: {exc}")
                    unparsed.append(fact)
                continue

            match = self.COORDINATE.match(fact)
            if match:
                state.add_given(
                    "CoordinateOf",
                    match.group(1),
                    value=(match.group(2).strip(), match.group(3).strip()),
                    raw_expression=fact,
                )
                continue

            match = self.POINT_ON_CURVE.match(fact)
            if match:
                state.add_given(
                    "PointOnCurve", match.group(1), match.group(2), value=True
                )
                continue

            match = self.NAMED_RELATION.match(fact)
            if match:
                relation, curve, target = match.groups()
                predicate = "FocusOf" if "Focus" in relation else "DirectrixOf"
                state.add_given(predicate, curve, target, value=True)
                continue

            inequality = re.match(r"^(\w+)\s*>\s*0$", fact)
            if inequality:
                symbol = Term("symbol", (inequality.group(1),))
                state.add_given("Positive", symbol, value=True)
                state.add_given("OrderConstraint", fact, value=True)
                continue

            unparsed.append(fact)

        for index, fact in enumerate(unparsed):
            state.add_given(
                "UnparsedFact", index, value=fact, raw_expression=fact
            )
        if query_expressions:
            self._adapt_query(state, query_expressions.strip())
        return AdaptationResult(state, tuple(unparsed), tuple(errors))

    @staticmethod
    def _adapt_query(state: InformationState, query: str) -> None:
        match = re.match(r"^Eccentricity\((\w+)\)$", query)
        if match:
            state.add_given(
                "QueryGoal",
                "ParameterOf",
                match.group(1),
                "eccentricity",
            )
            return
        match = re.match(r"^Expression\(Asymptote\((\w+)\)\)$", query)
        if match:
            state.add_given("QueryGoal", "AsymptoteFamilyOf", match.group(1))
            return
        match = re.match(r"^Coordinate\(Focus\((\w+)\)\)$", query)
        if match:
            state.add_given("QueryGoal", "FocusCoordinateOf", match.group(1))
            return
        if re.match(r"^\w+$", query):
            state.add_given("QueryGoal", "SymbolValue", query)
        else:
            state.add_given("UnparsedQuery", query, value=True)
