"""Typed information state for theorem v2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .expressions import ConservativeSolver
from .schema import Fact, Provenance, StateDelta, SymbolRef


@dataclass(frozen=True)
class DeltaCommit:
    state: "InformationState"
    added_count: int
    conflicts: Tuple[str, ...] = ()


@dataclass
class InformationState:
    symbols: Dict[str, SymbolRef] = field(default_factory=dict)
    facts: Dict[Tuple[Any, ...], Fact] = field(default_factory=dict)
    history: List[Any] = field(default_factory=list)
    _next_fact_id: int = 0

    def clone(self) -> "InformationState":
        return InformationState(
            symbols=self.symbols.copy(),
            facts=self.facts.copy(),
            history=self.history.copy(),
            _next_fact_id=self._next_fact_id,
        )

    def declare(
        self,
        name: str,
        type_name: str,
        provenance: Optional[Provenance] = None,
    ) -> "InformationState":
        symbol = SymbolRef(name, type_name)
        existing = self.symbols.get(name)
        if existing is not None and existing != symbol:
            raise ValueError(f"conflicting symbol declaration for {name}")
        self.symbols[name] = symbol
        self.add_given(
            "TypeOf", name, value=type_name, provenance=provenance
        )
        return self

    def add_given(
        self,
        predicate: str,
        *arguments: Any,
        value: Any = None,
        provenance: Optional[Provenance] = None,
        raw_expression: Optional[str] = None,
    ) -> Fact:
        fact = Fact(
            predicate=predicate,
            arguments=tuple(arguments),
            value=value,
            provenance=provenance or Provenance.given(),
            raw_expression=raw_expression,
            fact_id=self._allocate_fact_id("g"),
        )
        existing = self.facts.get(fact.slot_key)
        if existing is not None and existing.value != fact.value:
            raise ValueError(f"conflicting given fact for {fact.slot_key}")
        if existing is None:
            self.facts[fact.slot_key] = fact
            return fact
        return existing

    def find(self, predicate: str, *argument_prefix: Any) -> List[Fact]:
        prefix = tuple(argument_prefix)
        return [
            fact
            for fact in self.facts.values()
            if fact.predicate == predicate
            and fact.arguments[: len(prefix)] == prefix
        ]

    def get(self, predicate: str, *arguments: Any) -> Optional[Fact]:
        return self.facts.get((predicate, tuple(arguments)))

    def value(self, predicate: str, *arguments: Any, default: Any = None) -> Any:
        fact = self.get(predicate, *arguments)
        return default if fact is None else fact.value

    def has_type(self, name: str, type_name: str) -> bool:
        return self.value("TypeOf", name) == type_name

    def commit_delta(
        self,
        delta: StateDelta,
        solver: Optional[ConservativeSolver] = None,
    ) -> DeltaCommit:
        solver = solver or ConservativeSolver()
        candidate = self.clone()
        conflicts: List[str] = []
        added = 0

        for symbol in delta.add_symbols:
            existing = candidate.symbols.get(symbol.name)
            if existing is not None and existing != symbol:
                conflicts.append(f"symbol:{symbol.name}")
                continue
            if existing is None:
                candidate.symbols[symbol.name] = symbol
                added += 1

        for source_fact in delta.add_facts:
            fact = source_fact
            if fact.fact_id is None:
                fact = Fact(
                    predicate=fact.predicate,
                    arguments=fact.arguments,
                    value=fact.value,
                    provenance=fact.provenance,
                    raw_expression=fact.raw_expression,
                    fact_id=candidate._allocate_fact_id("d"),
                )
            existing = candidate.facts.get(fact.slot_key)
            if existing is None:
                candidate.facts[fact.slot_key] = fact
                added += 1
            elif not solver.equivalent(existing.value, fact.value):
                from .resolution import StateExpressionResolver

                resolver = StateExpressionResolver(candidate, solver)
                if resolver.equivalent(existing.value, fact.value):
                    continue
                conflicts.append(
                    f"fact:{fact.predicate}{fact.arguments}:"
                    f"{existing.value!r}!={fact.value!r}"
                )

        if conflicts:
            return DeltaCommit(self, 0, tuple(conflicts))
        return DeltaCommit(candidate, added)

    def _allocate_fact_id(self, prefix: str) -> str:
        fact_id = f"{prefix}{self._next_fact_id}"
        self._next_fact_id += 1
        return fact_id
