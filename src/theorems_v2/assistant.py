"""Auxiliary theorem saturation, constraint closure, and goal checks."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .applicator import ApplicatorV2
from .complete_library import CompleteTheoremLibraryV2
from .expressions import ConservativeSolver, add, div, mul, neg, number
from .schema import ApplicationStatus, Fact, Provenance, StateDelta, Term
from .state import InformationState


@dataclass(frozen=True)
class ClosureStep:
    source: str
    identifier: str
    status: str


@dataclass(frozen=True)
class ClosureResult:
    state: InformationState
    steps: Tuple[ClosureStep, ...]
    rounds: int
    reached_fixed_point: bool


class ConstraintClosure:
    """Solve exact one-unknown linear constraints over scoped parameters."""

    def __init__(self, solver: Optional[ConservativeSolver] = None):
        self.solver = solver or ConservativeSolver()

    def close(
        self, state: InformationState, max_rounds: int = 8
    ) -> ClosureResult:
        current = state
        steps: List[ClosureStep] = []
        for round_index in range(max_rounds):
            changed = False
            known = self._known_parameters(current)
            for constraint in current.find("EquationConstraint"):
                if not constraint.arguments:
                    continue
                relation = constraint.arguments[0]
                if not isinstance(relation, Term) or relation.operator != "eq":
                    continue
                unknowns = self._unknown_parameters(relation, known)
                if len(unknowns) != 1:
                    continue
                target = next(iter(unknowns))
                solved = self._solve_linear(relation, target, known)
                if solved is None:
                    continue
                entity, parameter_name = target.arguments
                fact = Fact(
                    "ParameterOf",
                    (entity, parameter_name),
                    value=solved,
                    provenance=Provenance(
                        "solver",
                        "linear_constraint_closure",
                        (constraint.fact_id,) if constraint.fact_id else (),
                    ),
                )
                commit = current.commit_delta(
                    StateDelta(add_facts=(fact,)), self.solver
                )
                if commit.conflicts or commit.added_count == 0:
                    continue
                current = commit.state
                steps.append(
                    ClosureStep(
                        "constraint",
                        constraint.fact_id or "unknown",
                        f"solved {entity}.{parameter_name}={solved}",
                    )
                )
                changed = True
                break
            if not changed:
                return ClosureResult(current, tuple(steps), round_index + 1, True)
        return ClosureResult(current, tuple(steps), max_rounds, False)

    @staticmethod
    def _known_parameters(state: InformationState) -> Dict[Term, Any]:
        return {
            Term("parameter", fact.arguments): fact.value
            for fact in state.find("ParameterOf")
            if len(fact.arguments) == 2
        }

    def _unknown_parameters(
        self, expression: Any, known: Dict[Term, Any]
    ) -> Set[Term]:
        if isinstance(expression, Term):
            if expression.operator == "parameter":
                return set() if expression in known else {expression}
            result: Set[Term] = set()
            for argument in expression.arguments:
                result.update(self._unknown_parameters(argument, known))
            return result
        return set()

    def _solve_linear(
        self,
        relation: Term,
        target: Term,
        known: Dict[Term, Any],
    ) -> Optional[Any]:
        left, right = relation.arguments
        left_linear = self._linearize(left, target, known)
        right_linear = self._linearize(right, target, known)
        if left_linear is None or right_linear is None:
            return None
        coefficient = self.solver.sub(left_linear[0], right_linear[0])
        constant = self.solver.sub(left_linear[1], right_linear[1])
        coefficient = number(coefficient)
        constant = number(constant)
        if not isinstance(coefficient, Fraction) or coefficient == 0:
            return None
        if not isinstance(constant, Fraction):
            return None
        return -constant / coefficient

    def _linearize(
        self,
        expression: Any,
        target: Term,
        known: Dict[Term, Any],
    ) -> Optional[Tuple[Any, Any]]:
        expression = number(expression)
        if isinstance(expression, Fraction):
            return Fraction(0), expression
        if isinstance(expression, str):
            return None
        if not isinstance(expression, Term):
            return None
        if expression.operator == "parameter":
            if expression == target:
                return Fraction(1), Fraction(0)
            value = number(known.get(expression))
            if isinstance(value, Fraction):
                return Fraction(0), value
            return None
        if expression.operator == "add":
            coefficient = Fraction(0)
            constant = Fraction(0)
            for argument in expression.arguments:
                part = self._linearize(argument, target, known)
                if part is None:
                    return None
                coefficient += part[0]
                constant += part[1]
            return coefficient, constant
        if expression.operator == "mul":
            variable_part = None
            constant_factor = Fraction(1)
            for argument in expression.arguments:
                part = self._linearize(argument, target, known)
                if part is None:
                    return None
                if part[0] != 0:
                    if variable_part is not None:
                        return None
                    variable_part = part
                else:
                    constant_factor *= part[1]
            if variable_part is None:
                return Fraction(0), constant_factor
            return (
                variable_part[0] * constant_factor,
                variable_part[1] * constant_factor,
            )
        if expression.operator == "div":
            numerator = self._linearize(expression.arguments[0], target, known)
            denominator = self._linearize(expression.arguments[1], target, known)
            if numerator is None or denominator is None or denominator[0] != 0:
                return None
            if denominator[1] == 0:
                return None
            return (
                numerator[0] / denominator[1],
                numerator[1] / denominator[1],
            )
        return None


class AuxiliaryReasoner:
    """Apply uniquely matching concrete theorem actions to a fixed point."""

    def __init__(
        self,
        library: Optional[CompleteTheoremLibraryV2] = None,
        applicator: Optional[ApplicatorV2] = None,
        constraint_closure: Optional[ConstraintClosure] = None,
    ):
        self.library = library or CompleteTheoremLibraryV2()
        self.applicator = applicator or ApplicatorV2()
        self.constraint_closure = constraint_closure or ConstraintClosure()

    def saturate(
        self,
        state: InformationState,
        allowed_model_ids: Optional[Iterable[int]] = None,
        max_rounds: int = 8,
    ) -> ClosureResult:
        allowed = list(
            allowed_model_ids
            if allowed_model_ids is not None
            else self.library.get_executable_models()
        )
        current = state
        steps: List[ClosureStep] = []
        for round_index in range(max_rounds):
            changed = False
            for model_id in allowed:
                model = self.library.get_model(model_id)
                matches = model.match(current)
                if len(matches) != 1:
                    continue
                result = self.applicator.apply(model, current, matches[0])
                if result.status != ApplicationStatus.APPLIED:
                    continue
                current = result.state_after
                steps.append(ClosureStep("theorem", str(model_id), "APPLIED"))
                changed = True
            constraint_result = self.constraint_closure.close(current)
            if constraint_result.state is not current:
                current = constraint_result.state
                steps.extend(constraint_result.steps)
                changed = True
            if not changed:
                return ClosureResult(current, tuple(steps), round_index + 1, True)
        return ClosureResult(current, tuple(steps), max_rounds, False)


class GoalEvaluator:
    """Check typed QueryGoal facts without performing hidden reasoning."""

    @staticmethod
    def add_goal(
        state: InformationState, predicate: str, *arguments: Any
    ) -> Fact:
        return state.add_given("QueryGoal", predicate, *arguments)

    @staticmethod
    def unresolved_goals(state: InformationState) -> Tuple[Fact, ...]:
        unresolved = []
        for goal in state.find("QueryGoal"):
            if not goal.arguments:
                unresolved.append(goal)
                continue
            predicate, *arguments = goal.arguments
            if state.get(predicate, *arguments) is None:
                unresolved.append(goal)
        return tuple(unresolved)

    @classmethod
    def all_satisfied(cls, state: InformationState) -> bool:
        goals = state.find("QueryGoal")
        return bool(goals) and not cls.unresolved_goals(state)
