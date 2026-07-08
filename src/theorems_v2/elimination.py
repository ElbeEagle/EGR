"""Exact, auditable elimination over structured equation constraints."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from .expressions import ConservativeSolver, number, sqrt_positive
from .polynomial_elimination import ConservativePolynomialEliminator
from .resolution import StateExpressionResolver
from .schema import Fact, Provenance, StateDelta, Term


Variable = Term
LinearForm = Tuple[Dict[Variable, Fraction], Fraction]


@dataclass(frozen=True)
class EliminationStep:
    target: Variable
    value: Any
    evidence_fact_ids: Tuple[str, ...]


@dataclass(frozen=True)
class EliminationResult:
    state: Any
    steps: Tuple[EliminationStep, ...]
    rounds: int
    inconsistent_constraints: Tuple[str, ...] = ()


class ExactEliminationClosure:
    """Solve uniquely determined exact linear components to a fixed point."""

    def __init__(
        self,
        solver: Optional[ConservativeSolver] = None,
        polynomial=None,
    ):
        self.solver = solver or ConservativeSolver()
        self.polynomial = (
            polynomial or ConservativePolynomialEliminator()
        )

    def close(self, state, max_rounds: int = 8) -> EliminationResult:
        current = state
        steps: List[EliminationStep] = []
        inconsistent: List[str] = []
        for round_index in range(max_rounds):
            known = self._known_values(current)
            rows = []
            for fact in current.find("EquationConstraint"):
                row = self._constraint_row(fact, known)
                if row is None:
                    continue
                coefficients, constant = row
                if not coefficients:
                    if constant != 0:
                        inconsistent.append(fact.fact_id or "unknown")
                    continue
                rows.append((coefficients, constant, fact))

            solutions = self._solve_rows(rows)
            if not solutions:
                solutions = self._solve_quadratic_constraints(current, known)
            if (
                not solutions
                and (
                    current.find("CompiledCoordinateEquation")
                    or self._has_symbol_constraint(current)
                )
            ):
                solutions = self.polynomial.solve(current, known)
            if not solutions:
                return EliminationResult(
                    current,
                    tuple(steps),
                    round_index + 1,
                    tuple(dict.fromkeys(inconsistent)),
                )

            changed = False
            for target, (value, evidence) in solutions.items():
                if target in known or not self._admissible(current, target, value):
                    continue
                predicate, arguments = self._target_slot(current, target)
                evidence_ids = tuple(
                    fact.fact_id for fact in evidence if fact.fact_id is not None
                )
                derived = Fact(
                    predicate,
                    arguments,
                    value=value,
                    provenance=Provenance(
                        "solver", "exact_linear_elimination", evidence_ids
                    ),
                )
                commit = current.commit_delta(
                    StateDelta(add_facts=(derived,)), self.solver
                )
                if commit.conflicts or commit.added_count == 0:
                    continue
                current = commit.state
                steps.append(EliminationStep(target, value, evidence_ids))
                changed = True
            if not changed:
                return EliminationResult(
                    current,
                    tuple(steps),
                    round_index + 1,
                    tuple(dict.fromkeys(inconsistent)),
                )
        return EliminationResult(
            current,
            tuple(steps),
            max_rounds,
            tuple(dict.fromkeys(inconsistent)),
        )

    def _known_values(self, state) -> Dict[Variable, Fraction]:
        resolver = StateExpressionResolver(state, self.solver)
        known: Dict[Variable, Fraction] = {}
        for fact in state.find("SymbolValueOf"):
            if len(fact.arguments) != 1:
                continue
            value = number(resolver.resolve(fact.value))
            if isinstance(value, Fraction):
                known[Term("symbol", (fact.arguments[0],))] = value
        slots = {}
        for predicate in ("ParameterOf", "ResolvedParameterOf"):
            for fact in state.find(predicate):
                if len(fact.arguments) == 2:
                    slots[fact.arguments] = fact
        for arguments, fact in slots.items():
            value = number(resolver.parameter_value(*arguments))
            if isinstance(value, Fraction):
                known[Term("parameter", arguments)] = value
        return known

    def _constraint_row(self, fact: Fact, known) -> Optional[LinearForm]:
        if not fact.arguments:
            return None
        relation = fact.arguments[0]
        if not isinstance(relation, Term) or relation.operator != "eq":
            return None
        left = self._linearize(relation.arguments[0], known)
        right = self._linearize(relation.arguments[1], known)
        if left is None or right is None:
            return None
        coefficients = dict(left[0])
        for variable, coefficient in right[0].items():
            coefficients[variable] = coefficients.get(variable, Fraction(0)) - coefficient
            if coefficients[variable] == 0:
                del coefficients[variable]
        return coefficients, left[1] - right[1]

    def _linearize(self, expression: Any, known) -> Optional[LinearForm]:
        expression = number(expression)
        if isinstance(expression, Fraction):
            return {}, expression
        if not isinstance(expression, Term):
            return None
        if expression.operator in {"symbol", "parameter"}:
            if expression in known:
                return {}, known[expression]
            return {expression: Fraction(1)}, Fraction(0)
        if expression.operator == "add":
            result: LinearForm = ({}, Fraction(0))
            for argument in expression.arguments:
                part = self._linearize(argument, known)
                if part is None:
                    return None
                result = self._add_forms(result, part)
            return result
        if expression.operator == "mul":
            result: LinearForm = ({}, Fraction(1))
            for argument in expression.arguments:
                part = self._linearize(argument, known)
                if part is None:
                    return None
                result = self._multiply_forms(result, part)
                if result is None:
                    return None
            return result
        if expression.operator == "div":
            numerator = self._linearize(expression.arguments[0], known)
            denominator = self._linearize(expression.arguments[1], known)
            if (
                numerator is None
                or denominator is None
                or denominator[0]
                or denominator[1] == 0
            ):
                return None
            scale = Fraction(1) / denominator[1]
            return (
                {key: value * scale for key, value in numerator[0].items()},
                numerator[1] * scale,
            )
        if expression.operator in {"sqrt", "sqrt_positive"}:
            argument = self._linearize(expression.arguments[0], known)
            if argument is None or argument[0]:
                return None
            value = number(sqrt_positive(argument[1]))
            return ({}, value) if isinstance(value, Fraction) else None
        if expression.operator == "pow":
            base = self._linearize(expression.arguments[0], known)
            exponent = number(expression.arguments[1])
            if base is None or exponent != 2 or base[0]:
                return None
            return {}, base[1] * base[1]
        return None

    @staticmethod
    def _add_forms(left: LinearForm, right: LinearForm) -> LinearForm:
        coefficients = dict(left[0])
        for variable, coefficient in right[0].items():
            coefficients[variable] = coefficients.get(variable, Fraction(0)) + coefficient
            if coefficients[variable] == 0:
                del coefficients[variable]
        return coefficients, left[1] + right[1]

    @staticmethod
    def _multiply_forms(left: LinearForm, right: LinearForm) -> Optional[LinearForm]:
        if left[0] and right[0]:
            return None
        if not left[0] and not right[0]:
            return {}, left[1] * right[1]
        variable, constant = (left, right[1]) if left[0] else (right, left[1])
        return (
            {key: value * constant for key, value in variable[0].items()},
            variable[1] * constant,
        )

    def _solve_rows(self, rows):
        solutions = {}
        remaining = list(rows)
        while remaining:
            seed = remaining.pop()
            component = [seed]
            variables = set(seed[0])
            changed = True
            while changed:
                changed = False
                keep = []
                for row in remaining:
                    if variables.intersection(row[0]):
                        component.append(row)
                        variables.update(row[0])
                        changed = True
                    else:
                        keep.append(row)
                remaining = keep
            solved = self._gaussian_component(component, sorted(variables, key=repr))
            if solved is None:
                continue
            evidence = tuple(row[2] for row in component)
            for variable, value in solved.items():
                solutions[variable] = (value, evidence)
        return solutions

    @staticmethod
    def _gaussian_component(rows, variables):
        if len(rows) < len(variables):
            return None
        matrix = []
        for coefficients, constant, _ in rows:
            matrix.append(
                [coefficients.get(variable, Fraction(0)) for variable in variables]
                + [-constant]
            )
        pivot_row = 0
        pivots = {}
        for column in range(len(variables)):
            pivot = next(
                (index for index in range(pivot_row, len(matrix)) if matrix[index][column] != 0),
                None,
            )
            if pivot is None:
                continue
            matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
            scale = matrix[pivot_row][column]
            matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
            for index in range(len(matrix)):
                if index == pivot_row or matrix[index][column] == 0:
                    continue
                factor = matrix[index][column]
                matrix[index] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(matrix[index], matrix[pivot_row])
                ]
            pivots[column] = pivot_row
            pivot_row += 1
        for row in matrix:
            if all(value == 0 for value in row[:-1]) and row[-1] != 0:
                return None
        if len(pivots) != len(variables):
            return None
        return {
            variables[column]: matrix[row_index][-1]
            for column, row_index in pivots.items()
        }

    def _solve_quadratic_constraints(self, state, known):
        solutions = {}
        for fact in state.find("EquationConstraint"):
            if not fact.arguments:
                continue
            relation = fact.arguments[0]
            if not isinstance(relation, Term) or relation.operator != "eq":
                continue
            variables = self._variables(relation, known)
            if len(variables) != 1:
                continue
            target = next(iter(variables))
            left = self._quadratic(relation.arguments[0], target, known)
            right = self._quadratic(relation.arguments[1], target, known)
            if left is None or right is None:
                continue
            coefficients = tuple(left[i] - right[i] for i in range(3))
            roots = self._quadratic_roots(coefficients)
            admissible = [
                root
                for root in roots
                if self._admissible(state, target, root)
            ]
            unique = []
            for root in admissible:
                if root not in unique:
                    unique.append(root)
            if len(unique) == 1:
                solutions[target] = (unique[0], (fact,))
        return solutions

    def _variables(self, expression, known) -> Set[Variable]:
        if not isinstance(expression, Term):
            return set()
        if expression.operator in {"symbol", "parameter"}:
            return set() if expression in known else {expression}
        result = set()
        for argument in expression.arguments:
            result.update(self._variables(argument, known))
        return result

    def _quadratic(self, expression, target, known):
        expression = number(expression)
        if isinstance(expression, Fraction):
            return expression, Fraction(0), Fraction(0)
        if not isinstance(expression, Term):
            return None
        if expression.operator in {"symbol", "parameter"}:
            if expression in known:
                return known[expression], Fraction(0), Fraction(0)
            if expression == target:
                return Fraction(0), Fraction(1), Fraction(0)
            return None
        if expression.operator == "add":
            result = (Fraction(0), Fraction(0), Fraction(0))
            for argument in expression.arguments:
                part = self._quadratic(argument, target, known)
                if part is None:
                    return None
                result = tuple(result[i] + part[i] for i in range(3))
            return result
        if expression.operator == "mul":
            result = (Fraction(1), Fraction(0), Fraction(0))
            for argument in expression.arguments:
                part = self._quadratic(argument, target, known)
                if part is None:
                    return None
                product = [Fraction(0), Fraction(0), Fraction(0)]
                for left_degree, left_value in enumerate(result):
                    for right_degree, right_value in enumerate(part):
                        degree = left_degree + right_degree
                        if degree > 2 and left_value and right_value:
                            return None
                        if degree <= 2:
                            product[degree] += left_value * right_value
                result = tuple(product)
            return result
        if expression.operator == "div":
            numerator = self._quadratic(expression.arguments[0], target, known)
            denominator = self._quadratic(expression.arguments[1], target, known)
            if numerator is None or denominator is None or denominator[1:] != (0, 0):
                return None
            if denominator[0] == 0:
                return None
            return tuple(value / denominator[0] for value in numerator)
        if expression.operator == "pow" and number(expression.arguments[1]) == 2:
            base = self._quadratic(expression.arguments[0], target, known)
            if base is None or base[2] != 0:
                return None
            return (
                base[0] * base[0],
                2 * base[0] * base[1],
                base[1] * base[1],
            )
        return None

    @staticmethod
    def _quadratic_roots(coefficients):
        constant, linear, quadratic = coefficients
        if quadratic == 0:
            return () if linear == 0 else (-constant / linear,)
        discriminant = linear * linear - 4 * quadratic * constant
        if discriminant < 0:
            return ()
        root = sqrt_positive(discriminant)
        if not isinstance(root, Fraction):
            if linear == 0:
                positive_root = sqrt_positive(-constant / quadratic)
                return (positive_root, Term("mul", (Fraction(-1), positive_root)))
            return ()
        denominator = 2 * quadratic
        return (
            (-linear + root) / denominator,
            (-linear - root) / denominator,
        )

    @staticmethod
    def _target_slot(state, target: Variable):
        if target.operator == "symbol":
            return "SymbolValueOf", target.arguments
        predicate = (
            "ResolvedParameterOf"
            if state.get("ParameterOf", *target.arguments) is not None
            else "ParameterOf"
        )
        return predicate, target.arguments

    @classmethod
    def _has_symbol_constraint(cls, state):
        return any(
            fact.arguments
            and cls._contains_symbol(fact.arguments[0])
            for fact in state.find("EquationConstraint")
        )

    @classmethod
    def _contains_symbol(cls, value):
        if isinstance(value, Term):
            if value.operator == "symbol":
                return True
            return any(cls._contains_symbol(item) for item in value.arguments)
        if isinstance(value, (tuple, list)):
            return any(cls._contains_symbol(item) for item in value)
        return False

    def _admissible(self, state, target: Variable, value: Any) -> bool:
        return self.polynomial._admissible(state, target, value)