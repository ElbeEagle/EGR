"""State-aware, provenance-preserving expression resolution."""

from __future__ import annotations

from dataclasses import fields, is_dataclass, replace
from typing import Any, Optional, Set, Tuple

from .expressions import ConservativeSolver, add, div, mul, sqrt_positive, square
from .schema import Term


class StateExpressionResolver:
    """Resolve only values explicitly supported by facts in one state."""

    def __init__(self, state, solver: Optional[ConservativeSolver] = None):
        self.state = state
        self.solver = solver or ConservativeSolver()

    def resolve(self, value: Any, seen: Optional[Set[Tuple[Any, ...]]] = None) -> Any:
        seen = set() if seen is None else set(seen)
        if isinstance(value, Term):
            if value.operator == "symbol":
                key = ("symbol", value.arguments[0])
                if key in seen:
                    return value
                known = self.state.value("SymbolValueOf", value.arguments[0])
                if known is None:
                    return value
                seen.add(key)
                return self.resolve(known, seen)

            if value.operator == "parameter":
                key = ("parameter", *value.arguments)
                if key in seen:
                    return value
                known = self.state.value(
                    "ResolvedParameterOf", *value.arguments
                )
                if known is None:
                    known = self.state.value("ParameterOf", *value.arguments)
                if known is None:
                    return value
                seen.add(key)
                return self.resolve(known, seen)

            arguments = tuple(self.resolve(argument, seen) for argument in value.arguments)
            if value.operator == "add":
                return add(*arguments)
            if value.operator == "mul":
                return mul(*arguments)
            if value.operator == "div":
                return div(*arguments)
            if value.operator == "pow" and len(arguments) == 2 and arguments[1] == 2:
                return square(arguments[0])
            if value.operator in {"sqrt", "sqrt_positive"} and len(arguments) == 1:
                return sqrt_positive(arguments[0])
            if value.operator == "eq" and len(arguments) == 2:
                return Term("eq", arguments)
            return Term(value.operator, arguments)

        if isinstance(value, tuple):
            return tuple(self.resolve(item, seen) for item in value)
        if isinstance(value, list):
            return [self.resolve(item, seen) for item in value]
        if is_dataclass(value) and not isinstance(value, type):
            changes = {
                field.name: self.resolve(getattr(value, field.name), seen)
                for field in fields(value)
            }
            return replace(value, **changes)
        return value

    def parameter_value(self, entity: str, parameter_name: str) -> Any:
        value = self.state.value(
            "ResolvedParameterOf", entity, parameter_name
        )
        if value is None:
            value = self.state.value("ParameterOf", entity, parameter_name)
        return None if value is None else self.resolve(value)

    def equivalent(self, left: Any, right: Any) -> bool:
        return self.solver.equivalent(self.resolve(left), self.resolve(right))