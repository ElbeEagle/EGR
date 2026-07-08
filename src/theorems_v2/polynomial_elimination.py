"""Conservative elimination for small exact polynomial systems."""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, Optional, Tuple

from .expressions import mul, number, sqrt_positive
from .schema import Term


Variable = Term
Monomial = Tuple[Variable, ...]
Polynomial = Dict[Monomial, Fraction]


class ConservativePolynomialEliminator:
    """Eliminate quadratic monomials without selecting ambiguous branches."""

    def solve(self, state, known):
        rows = []
        for fact in state.find("EquationConstraint"):
            if not fact.arguments:
                continue
            relation = fact.arguments[0]
            if not isinstance(relation, Term) or relation.operator != "eq":
                continue
            left = self._polynomial(relation.arguments[0], known)
            right = self._polynomial(relation.arguments[1], known)
            if left is None or right is None:
                continue
            polynomial = self._subtract(left, right)
            if polynomial:
                rows.append((polynomial, fact))

        variables = sorted(
            {
                variable
                for polynomial, _ in rows
                for monomial in polynomial
                for variable in monomial
            },
            key=repr,
        )
        solutions = {}
        for target in variables:
            candidate_rows = self._target_rows(rows, target)
            candidates = None
            evidence = []
            for constant, linear, quadratic, facts in candidate_rows:
                row_roots = {
                    root
                    for root in self._quadratic_roots(
                        constant,
                        linear,
                        quadratic,
                    )
                    if self._admissible(state, target, root)
                }
                if not row_roots:
                    continue
                candidates = (
                    row_roots
                    if candidates is None
                    else candidates.intersection(row_roots)
                )
                evidence.extend(facts)
            if candidates is not None and len(candidates) == 1:
                solutions[target] = (
                    next(iter(candidates)),
                    tuple(dict.fromkeys(evidence)),
                )
        return solutions

    def _target_rows(self, rows, target):
        monomials = sorted(
            {
                monomial
                for polynomial, _ in rows
                for monomial in polynomial
                if monomial
            },
            key=repr,
        )
        target_linear = (target,)
        target_quadratic = (target, target)
        nuisance = [
            monomial
            for monomial in monomials
            if monomial not in {target_linear, target_quadratic}
        ]
        columns = nuisance + [(), target_linear, target_quadratic]
        matrix = [
            [polynomial.get(column, Fraction(0)) for column in columns]
            for polynomial, _ in rows
        ]
        evidence = [[fact] for _, fact in rows]

        pivot_row = 0
        for column in range(len(nuisance)):
            pivot = next(
                (
                    index
                    for index in range(pivot_row, len(matrix))
                    if matrix[index][column] != 0
                ),
                None,
            )
            if pivot is None:
                continue
            matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
            evidence[pivot_row], evidence[pivot] = (
                evidence[pivot],
                evidence[pivot_row],
            )
            scale = matrix[pivot_row][column]
            matrix[pivot_row] = [
                value / scale for value in matrix[pivot_row]
            ]
            for index in range(len(matrix)):
                if index == pivot_row or matrix[index][column] == 0:
                    continue
                factor = matrix[index][column]
                matrix[index] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(
                        matrix[index],
                        matrix[pivot_row],
                    )
                ]
                evidence[index].extend(evidence[pivot_row])
            pivot_row += 1

        results = []
        seen = set()
        for row, facts in zip(matrix, evidence):
            if any(row[index] != 0 for index in range(len(nuisance))):
                continue
            coefficients = tuple(row[len(nuisance) :])
            if coefficients == (0, 0, 0) or coefficients in seen:
                continue
            seen.add(coefficients)
            results.append((*coefficients, tuple(facts)))
        return results

    def _polynomial(self, expression, known) -> Optional[Polynomial]:
        expression = number(expression)
        if isinstance(expression, Fraction):
            return {} if expression == 0 else {(): expression}
        if not isinstance(expression, Term):
            return None
        if expression.operator in {"symbol", "parameter"}:
            if expression in known:
                value = known[expression]
                return {} if value == 0 else {(): value}
            return {(expression,): Fraction(1)}
        if expression.operator == "add":
            result = {}
            for argument in expression.arguments:
                part = self._polynomial(argument, known)
                if part is None:
                    return None
                result = self._add(result, part)
            return result
        if expression.operator == "mul":
            result = {(): Fraction(1)}
            for argument in expression.arguments:
                part = self._polynomial(argument, known)
                if part is None:
                    return None
                result = self._multiply(result, part)
                if result is None:
                    return None
            return result
        if expression.operator == "div":
            numerator = self._polynomial(expression.arguments[0], known)
            denominator = self._polynomial(expression.arguments[1], known)
            if (
                numerator is None
                or denominator is None
                or set(denominator) - {()}
                or denominator.get((), 0) == 0
            ):
                return None
            scale = Fraction(1) / denominator[()]
            return {
                monomial: coefficient * scale
                for monomial, coefficient in numerator.items()
            }
        if expression.operator == "pow" and number(expression.arguments[1]) == 2:
            base = self._polynomial(expression.arguments[0], known)
            return None if base is None else self._multiply(base, base)
        if expression.operator in {"sqrt", "sqrt_positive"}:
            argument = self._polynomial(expression.arguments[0], known)
            if argument is None or set(argument) - {()}:
                return None
            value = number(sqrt_positive(argument.get((), 0)))
            if not isinstance(value, Fraction):
                return None
            return {} if value == 0 else {(): value}
        return None

    @staticmethod
    def _add(left, right):
        result = dict(left)
        for monomial, coefficient in right.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
        return result

    def _subtract(self, left, right):
        return self._add(
            left,
            {
                monomial: -coefficient
                for monomial, coefficient in right.items()
            },
        )

    @staticmethod
    def _multiply(left, right):
        result = {}
        for left_monomial, left_coefficient in left.items():
            for right_monomial, right_coefficient in right.items():
                monomial = tuple(
                    sorted(left_monomial + right_monomial, key=repr)
                )
                if len(monomial) > 2:
                    return None
                result[monomial] = (
                    result.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return {
            monomial: coefficient
            for monomial, coefficient in result.items()
            if coefficient != 0
        }

    @staticmethod
    def _quadratic_roots(constant, linear, quadratic):
        if quadratic == 0:
            return () if linear == 0 else (-constant / linear,)
        discriminant = linear * linear - 4 * quadratic * constant
        if discriminant < 0:
            return ()
        root = sqrt_positive(discriminant)
        if not isinstance(root, Fraction):
            if linear == 0:
                positive = sqrt_positive(-constant / quadratic)
                return positive, mul(-1, positive)
            return ()
        denominator = 2 * quadratic
        return (
            (-linear + root) / denominator,
            (-linear - root) / denominator,
        )

    @classmethod
    def _admissible(cls, state, target, value):
        sign = cls._root_sign(value)
        if state.get("Positive", target) is not None:
            return sign == 1
        if state.get("Negative", target) is not None:
            return sign == -1
        if state.get("NonNegative", target) is not None:
            return sign in {0, 1}
        if state.get("NonPositive", target) is not None:
            return sign in {-1, 0}
        return True

    @staticmethod
    def _root_sign(value):
        value = number(value)
        if isinstance(value, Fraction):
            return 1 if value > 0 else -1 if value < 0 else 0
        if isinstance(value, Term) and value.operator == "sqrt_positive":
            return 1
        if isinstance(value, Term) and value.operator == "mul":
            sign = 1
            for factor in value.arguments:
                factor_sign = ConservativePolynomialEliminator._root_sign(factor)
                if factor_sign is None:
                    return None
                sign *= factor_sign
            return sign
        return None