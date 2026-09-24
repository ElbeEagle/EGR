"""Object-scoped facts and derived information for bound execution slices."""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

import sympy as sp

from src.solver.transition_primitives import parse_expression
from .abstract_state import AbstractState, CurveType, QueryType


@dataclass(frozen=True)
class EquationFact:
    fact_id: str
    owner: str
    role: str
    expression: sp.Expr  # lhs - rhs = 0
    source: str


@dataclass(frozen=True)
class FocusEquality:
    fact_id: str
    curves: tuple[str, str]
    source: str


@dataclass(frozen=True)
class CurveFrame:
    equation_id: str
    center: tuple[sp.Expr, sp.Expr] = (sp.S.Zero, sp.S.Zero)
    axis: str = 'x'


@dataclass
class TransitionState:
    entities: dict[str, str]
    symbols: dict[str, sp.Symbol]
    equations: dict[str, EquationFact]
    constraints: dict[str, Any]
    query: sp.Symbol
    properties: dict[tuple[str, str], sp.Expr] = field(default_factory=dict)
    values: dict[sp.Symbol, sp.Expr] = field(default_factory=dict)
    provenance: dict[str, tuple[str, ...]] = field(default_factory=dict)
    history: list = field(default_factory=list)
    revision: int = 0
    relations: dict[str, FocusEquality] = field(default_factory=dict)
    frames: dict[str, CurveFrame] = field(default_factory=dict)

    @classmethod
    def from_facts(cls, facts: str, query: str) -> 'TransitionState':
        parts = [p.strip() for p in facts.split(';') if p.strip()]
        entities = {}
        for part in parts:
            declaration = re.fullmatch(r'([A-Za-z]\w*)\s*:\s*(Hyperbola|Ellipse|Number|Real)', part)
            if declaration:
                name, kind = declaration.groups()
                if name in ('x', 'y') or name in entities:
                    raise ValueError('Duplicate or reserved entity')
                entities[name] = kind
        symbols = {name: sp.Symbol(name, real=True) for name in ('x', 'y')}
        symbols.update({name: sp.Symbol(name, real=True) for name, kind in entities.items()
                        if kind in ('Number', 'Real')})
        if query not in symbols or query in ('x', 'y'):
            raise ValueError('Slice requires a declared scalar query')
        state = cls(entities, symbols, {}, {}, symbols[query])
        for index, part in enumerate(parts):
            fact_id = f'f{index}'
            if re.fullmatch(r'([A-Za-z]\w*)\s*:\s*(Hyperbola|Ellipse|Number|Real)', part):
                continue
            focus = re.fullmatch(r'Focus\(([A-Za-z]\w*)\)\s*=\s*Focus\(([A-Za-z]\w*)\)', part)
            if focus:
                curves = focus.groups()
                if any(entities.get(c) not in ('Hyperbola', 'Ellipse') for c in curves):
                    raise ValueError('Focus relation requires declared curves')
                if curves[0] == curves[1]:
                    raise ValueError('Focus relation requires two distinct curves')
                state.relations[fact_id] = FocusEquality(fact_id, curves, part)
                continue
            equation = re.fullmatch(r'Expression\((.+)\)\s*=\s*\((.+)\)', part)
            if equation:
                owner, text = equation.groups()
                asymptote = re.fullmatch(r'OneOf\(Asymptote\(([A-Za-z]\w*)\)\)', owner)
                role = 'asymptote' if asymptote else 'curve'
                owner = asymptote.group(1) if asymptote else owner
                if entities.get(owner) not in ('Hyperbola', 'Ellipse'):
                    raise ValueError('Equation owner is not a declared curve')
                lhs, separator, rhs = text.partition('=')
                if not separator or '=' in rhs:
                    raise ValueError('Expected one equation equality')
                left, guards_l = parse_expression(lhs, symbols)
                right, guards_r = parse_expression(rhs, symbols)
                state.equations[fact_id] = EquationFact(fact_id, owner, role, left-right, part)
                guards = guards_l + guards_r
            else:
                comparison = re.fullmatch(r'(.+?)(>=|<=|!=|>|<|=)(.+)', part)
                if not comparison:
                    raise ValueError(f'Unsupported fact syntax: {part}')
                lhs, operator, rhs = comparison.groups()
                left, guards_l = parse_expression(lhs, symbols)
                right, guards_r = parse_expression(rhs, symbols)
                constructors = {'>': sp.Gt, '<': sp.Lt, '>=': sp.Ge, '<=': sp.Le,
                                '=': sp.Eq, '!=': sp.Ne}
                state.constraints[fact_id] = constructors[operator](left, right)
                guards = guards_l + guards_r
            for i, guard in enumerate(guards):
                state.constraints[f'{fact_id}:domain:{i}'] = guard
        return state

    def abstract(self, curve: str) -> AbstractState:
        """Compatibility view only; object-scoped neural encoding is still pending."""
        return AbstractState(
            curve_type={'Hyperbola': CurveType.HYPERBOLA, 'Ellipse': CurveType.ELLIPSE}.get(
                self.entities.get(curve), CurveType.UNKNOWN),
            query_type=QueryType.VALUE,
            has_equation=any(f.owner == curve and f.role == 'curve' for f in self.equations.values()),
            has_asymptote_info=any(f.owner == curve and f.role == 'asymptote' for f in self.equations.values()),
            has_parameters={key for owner, key in self.properties if owner == curve},
            reasoning_depth=len(self.history),
            completeness_score=float(self.query in self.values),
        )

    def extract_answer(self):
        """No solving during extraction; missing or ambiguous answers stay unresolved."""
        return self.values.get(self.query)
