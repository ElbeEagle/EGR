"""Object-scoped facts and derived information for bound execution slices."""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

import sympy as sp

from src.solver.transition_primitives import parse_expression
from .named_line_facts import (NamedLine, NamedIntersection, SlopeSum, NamedLineQuery, FocusOnLine, OriginDotProductQuery,
                               LINE, register_named_line, parse_named_line_fact)
from .abstract_state import AbstractState, CurveType, QueryType


@dataclass(frozen=True)
class EquationFact:
    fact_id: str
    owner: str
    role: str
    expression: sp.Expr  # lhs - rhs = 0
    source: str


@dataclass(frozen=True)
class IntersectionReduction:
    fact_id: str
    curve: str
    line: str
    curve_equation_id: str
    line_equation_id: str
    variable: sp.Symbol
    xy: tuple[sp.Expr, sp.Expr]
    polynomial: sp.Expr
    source: str
    named_points: tuple[str, ...] = ()
    intersection_id: str | None = None


@dataclass(frozen=True)
class LineParameterization:
    line: str
    parameter: sp.Symbol
    point: str
    coordinate_id: str
    incidence_id: str
    intersection_id: str
    line_equation_id: str


@dataclass(frozen=True)
class FocusEquality:
    fact_id: str
    curves: tuple[str, str]
    source: str


@dataclass(frozen=True)
class FocusAlias:
    fact_id: str
    curve: str
    point: str
    source: str


@dataclass(frozen=True)
class DirectrixAlias:
    fact_id: str
    curve: str
    line: str
    source: str


@dataclass(frozen=True)
class ChordLengthQuery:
    line: str
    curve: str


@dataclass(frozen=True)
class TangentQuery:
    point: str
    curve: str


@dataclass(frozen=True)
class EccentricityQuery:
    curve: str


@dataclass(frozen=True)
class AsymptoteQuery:
    curve: str


@dataclass(frozen=True)
class PointCoordinates:
    fact_id: str
    point: str
    xy: tuple[sp.Expr, sp.Expr]
    source: str


@dataclass(frozen=True)
class PointOnCurve:
    fact_id: str
    point: str
    curve: str
    source: str


@dataclass(frozen=True)
class FocalDistanceQuery:
    point: str
    curve: str


@dataclass(frozen=True)
class FocusLineDistanceQuery:
    curve: str
    line: str


@dataclass(frozen=True)
class PointLineDistanceQuery:
    point: str
    line: str


@dataclass(frozen=True)
class CurveFrame:
    equation_id: str
    center: tuple[sp.Expr, sp.Expr] = (sp.S.Zero, sp.S.Zero)
    axis: str = 'x'
    direction: str | None = None


@dataclass
class TransitionState:
    entities: dict[str, str]
    symbols: dict[str, sp.Symbol]
    equations: dict[str, EquationFact]
    constraints: dict[str, Any]
    query: None | sp.Symbol | AsymptoteQuery | FocalDistanceQuery | PointLineDistanceQuery | FocusLineDistanceQuery | EccentricityQuery | TangentQuery | ChordLengthQuery | NamedLineQuery
    properties: dict[tuple[str, str], sp.Expr] = field(default_factory=dict)
    values: dict[sp.Symbol, sp.Expr] = field(default_factory=dict)
    provenance: dict[str, tuple[str, ...]] = field(default_factory=dict)
    history: list = field(default_factory=list)
    revision: int = 0
    relations: dict[str, FocusEquality] = field(default_factory=dict)
    frames: dict[str, CurveFrame] = field(default_factory=dict)
    coordinates: dict[str, PointCoordinates] = field(default_factory=dict)
    incidences: dict[str, PointOnCurve] = field(default_factory=dict)

    focus_aliases: dict[str, FocusAlias] = field(default_factory=dict)
    directrix_aliases: dict[str, DirectrixAlias] = field(default_factory=dict)

    intersection_reductions: dict[str, IntersectionReduction] = field(default_factory=dict)

    parameterizations: dict[str, LineParameterization] = field(default_factory=dict)

    focus_incidences: dict[str, FocusOnLine] = field(default_factory=dict)

    named_lines: dict[str, NamedLine] = field(default_factory=dict)
    named_intersections: dict[str, NamedIntersection] = field(default_factory=dict)
    slope_sums: dict[str, SlopeSum] = field(default_factory=dict)

    def line_bindings(self, line: str):
        """Resolve identity only; never derive equations or reconcile alternatives."""
        explicit = [f for f in self.equations.values() if f.owner == line and f.role == 'line']
        aliases = [a for a in self.directrix_aliases.values() if a.line == line]
        if not aliases:
            return [(f, None) for f in explicit]
        if len(aliases) != 1 or explicit:
            return []
        alias = aliases[0]
        fact = self.equations.get(f'derived:{alias.curve}:directrix')
        if fact is None or fact.owner != alias.curve or fact.role != 'directrix':
            return []
        return [(fact, alias.fact_id)]

    @classmethod
    def from_facts(cls, facts: str, query: str | None) -> 'TransitionState':
        parts = [p.strip() for p in facts.split(';') if p.strip()]
        entities = {}
        for part in parts:
            declaration = re.fullmatch(r'([A-Za-z]\w*)\s*:\s*(Hyperbola|Ellipse|Parabola|Line|Point|Origin|Number|Real)', part)
            if declaration:
                name, kind = declaration.groups()
                if name in ('x', 'y') or name in entities:
                    raise ValueError('Duplicate or reserved entity')
                entities[name] = 'Point' if kind == 'Origin' else kind
        symbols = {name: sp.Symbol(name, real=True) for name in ('x', 'y')}
        symbols.update({name: sp.Symbol(name, real=True) for name, kind in entities.items()
                        if kind in ('Number', 'Real')})
        query_text = query if query is not None else ''
        asymptote_query = re.fullmatch(r'Expression\(Asymptote\(([A-Za-z]\w*)\)\)', query_text)
        focal_query = re.fullmatch(r'Distance\(\s*([A-Za-z]\w*)\s*,\s*Focus\(([A-Za-z]\w*)\)\s*\)', query_text)
        line_query = re.fullmatch(r'Distance\(\s*([A-Za-z]\w*)\s*,\s*([A-Za-z]\w*)\s*\)', query_text)
        focus_line_query = re.fullmatch(r'Distance\(\s*Focus\(\s*([A-Za-z]\w*)\s*\)\s*,\s*([A-Za-z]\w*)\s*\)', query_text)
        eccentricity_query = re.fullmatch(r'Eccentricity\(\s*([A-Za-z]\w*)\s*\)', query_text)
        tangent_query = re.fullmatch(r'Expression\(TangentOnPoint\(\s*([A-Za-z]\w*)\s*,\s*([A-Za-z]\w*)\s*\)\)', query_text)
        chord_query = re.fullmatch(r'Length\(InterceptChord\(\s*([A-Za-z]\w*)\s*,\s*([A-Za-z]\w*)\s*\)\)', query_text)
        named_line_query = re.fullmatch(rf'Expression\(\s*{LINE}\s*\)', query_text)
        dot_query = re.fullmatch(r'DotProduct\(\s*VectorOf\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*,\s*VectorOf\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*\)', query_text)
        if dot_query:
            o,a,other,b = dot_query.groups()
            if o != other or a == b or any(entities.get(v) != 'Point' for v in (o,a,b)):
                raise ValueError('Dot query requires a shared base and two points')
            target = OriginDotProductQuery(o,tuple(sorted((a,b))))
        elif query is None or named_line_query:
            target = None  # Explicit facts-only diagnostic; not a solved problem.
        elif chord_query and entities.get(chord_query.group(1)) == 'Line' and entities.get(chord_query.group(2)) == 'Parabola':
            target = ChordLengthQuery(*chord_query.groups())
        elif tangent_query and entities.get(tangent_query.group(1)) == 'Point' and entities.get(tangent_query.group(2)) == 'Parabola':
            target = TangentQuery(*tangent_query.groups())
        elif eccentricity_query and entities.get(eccentricity_query.group(1)) in ('Ellipse', 'Hyperbola'):
            target = EccentricityQuery(eccentricity_query.group(1))
        elif focus_line_query and entities.get(focus_line_query.group(1)) == 'Parabola' and entities.get(focus_line_query.group(2)) == 'Line':
            target = FocusLineDistanceQuery(*focus_line_query.groups())
        elif line_query and entities.get(line_query.group(1)) == 'Point' and entities.get(line_query.group(2)) == 'Line':
            target = PointLineDistanceQuery(*line_query.groups())
        elif focal_query and entities.get(focal_query.group(1)) == 'Point' and entities.get(focal_query.group(2)) == 'Parabola':
            target = FocalDistanceQuery(*focal_query.groups())
        elif asymptote_query and entities.get(asymptote_query.group(1)) == 'Hyperbola':
            target = AsymptoteQuery(asymptote_query.group(1))
        elif query in symbols and query not in ('x', 'y'):
            target = symbols[query]
        else:
            raise ValueError('Unsupported or undeclared query target')
        state = cls(entities, symbols, {}, {}, target)
        if named_line_query:
            state.query = NamedLineQuery(register_named_line(state, *named_line_query.groups(), 'query'))
        for index, part in enumerate(parts):
            fact_id = f'f{index}'
            origin = re.fullmatch(r'([A-Za-z]\w*)\s*:\s*Origin', part)
            if origin:
                point = origin.group(1)
                if point in state.coordinates:
                    raise ValueError('Duplicate origin coordinate')
                state.coordinates[point] = PointCoordinates(fact_id, point, (sp.S.Zero, sp.S.Zero), part)
                state.provenance[fact_id] = (f'entity:{point}',)
                continue
            if parse_named_line_fact(state, part, fact_id):
                continue
            if re.fullmatch(r'([A-Za-z]\w*)\s*:\s*(Hyperbola|Ellipse|Parabola|Line|Point|Origin|Number|Real)', part):
                continue
            intersection = re.fullmatch(
                r'Coordinate\(OneOf\(Intersection\(\s*([A-Za-z]\w*)\s*,\s*([A-Za-z]\w*)\s*\)\)\)\s*=\s*\(([^,]+),([^,]+)\)', part)
            if intersection:
                left, right, xt, yt = intersection.groups()
                if sorted(entities.get(o, '') for o in (left, right)) != ['Line', 'Parabola']:
                    raise ValueError('Known intersection requires a Line and Parabola')
                # A fact-scoped witness is not a solution of an intersection equation.
                point = f'@intersection:{fact_id}'
                entities[point] = 'Point'
                px, gx = parse_expression(xt, symbols)
                py, gy = parse_expression(yt, symbols)
                state.coordinates[point] = PointCoordinates(fact_id, point, (px, py), part)
                for owner in (left, right):
                    key = f'{fact_id}:on:{owner}'
                    state.incidences[key] = PointOnCurve(key, point, owner, part)
                    state.provenance[key] = (fact_id,)
                for i, guard in enumerate(gx + gy):
                    state.constraints[f'{fact_id}:domain:{i}'] = guard
                continue
            coordinate = re.fullmatch(r'Coordinate\(([A-Za-z]\w*)\)\s*=\s*\(([^,]+),([^,]+)\)', part)
            if coordinate:
                point, x_text, y_text = coordinate.groups()
                if entities.get(point) != 'Point' or point in state.coordinates:
                    raise ValueError('Undeclared point or duplicate coordinate fact')
                px, gx = parse_expression(x_text, symbols)
                py, gy = parse_expression(y_text, symbols)
                state.coordinates[point] = PointCoordinates(fact_id, point, (px, py), part)
                for i, guard in enumerate(gx + gy):
                    state.constraints[f'{fact_id}:domain:{i}'] = guard
                continue
            incidence = re.fullmatch(r'PointOnCurve\(\s*([A-Za-z]\w*)\s*,\s*([A-Za-z]\w*)\s*\)', part)
            if incidence:
                point, curve = incidence.groups()
                if entities.get(point) != 'Point' or entities.get(curve) not in ('Ellipse', 'Hyperbola', 'Parabola', 'Line'):
                    raise ValueError('Invalid point/curve incidence')
                state.incidences[fact_id] = PointOnCurve(fact_id, point, curve, part)
                continue
            directrix = re.fullmatch(r'Directrix\(\s*([A-Za-z]\w*)\s*\)\s*=\s*([A-Za-z]\w*)', part)
            if directrix:
                curve, line = directrix.groups()
                if entities.get(curve) != 'Parabola' or entities.get(line) != 'Line':
                    raise ValueError('Directrix alias requires declared Parabola and Line')
                state.directrix_aliases[fact_id] = DirectrixAlias(fact_id, curve, line, part)
                continue
            focus_alias = re.fullmatch(r'Focus\(\s*([A-Za-z]\w*)\s*\)\s*=\s*([A-Za-z]\w*)', part)
            if focus_alias:
                curve, point = focus_alias.groups()
                if entities.get(curve) != 'Parabola' or entities.get(point) != 'Point':
                    raise ValueError('Focus alias requires declared Parabola and Point')
                state.focus_aliases[fact_id] = FocusAlias(fact_id, curve, point, part)
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
                if not asymptote and entities.get(owner) == 'Line':
                    role = 'line'
                if entities.get(owner) not in ('Hyperbola', 'Ellipse', 'Parabola', 'Line') or (asymptote and entities.get(owner) != 'Hyperbola'):
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
            curve_type={'Hyperbola': CurveType.HYPERBOLA, 'Ellipse': CurveType.ELLIPSE, 'Parabola': CurveType.PARABOLA}.get(
                self.entities.get(curve), CurveType.UNKNOWN),
            query_type=(QueryType.EQUATION if isinstance(self.query, (AsymptoteQuery, TangentQuery, NamedLineQuery)) else
                        QueryType.DISTANCE if isinstance(self.query, (FocalDistanceQuery, PointLineDistanceQuery, FocusLineDistanceQuery, ChordLengthQuery)) else QueryType.VALUE),
            has_equation=any(f.owner == curve and f.role in ('curve', 'line') for f in self.equations.values()),
            has_asymptote_info=any(f.owner == curve and f.role == 'asymptote' for f in self.equations.values()),
            has_parameters={key for owner, key in self.properties if owner == curve},
            reasoning_depth=len(self.history),
            completeness_score=float(self.extract_answer() is not None),
        )

    def extract_answer(self):
        """No solving during extraction; missing or ambiguous answers stay unresolved."""
        if isinstance(self.query, OriginDotProductQuery):
            return self.properties.get((self.query.owner, "dot_product"))
        if isinstance(self.query, NamedLineQuery):
            equations = [f for f in self.equations.values() if f.owner == self.query.line and f.role == 'line']
            if len(equations) != 1:
                return None
            expression = equations[0].expression
            if expression.free_symbols - {self.symbols['x'], self.symbols['y']}:
                return None
            return expression
        if isinstance(self.query, ChordLengthQuery):
            curves = [f for f in self.equations.values() if f.owner == self.query.curve and f.role == 'curve']
            lines = [f for f in self.equations.values() if f.owner == self.query.line and f.role == 'line']
            if len(curves) != 1 or len(lines) != 1:
                return None
            key = f'derived:intersection:{curves[0].fact_id}:{lines[0].fact_id}'
            fact = self.intersection_reductions.get(key)
            if fact is None or (fact.curve, fact.line) != (self.query.curve, self.query.line):
                return None
            return self.properties.get((key, 'chord_length'))
        if isinstance(self.query, TangentQuery):
            fact = self.equations.get(f'derived:{self.query.curve}:tangent:{self.query.point}')
            if fact is not None and fact.owner == self.query.curve and fact.role == 'tangent':
                return fact.expression
            return None
        if isinstance(self.query, EccentricityQuery):
            return self.properties.get((self.query.curve, 'eccentricity'))
        if isinstance(self.query, AsymptoteQuery):
            # Only a model-produced pair certifies completeness, not one given line.
            facts = [self.equations.get(f'derived:{self.query.curve}:asymptote:{i}') for i in (0, 1)]
            if all(f is not None and f.owner == self.query.curve and f.role == 'asymptote'
                   for f in facts):
                return tuple(f.expression for f in facts)
            return None
        if isinstance(self.query, FocusLineDistanceQuery):
            lines = [f for f in self.equations.values() if f.owner == self.query.line and f.role == 'line']
            if len(lines) != 1:
                return None
            return self.properties.get((self.query.line,
                                        f'focus_line_distance:{self.query.curve}:{lines[0].fact_id}'))
        if isinstance(self.query, PointLineDistanceQuery):
            lines = [f for f, _ in self.line_bindings(self.query.line)]
            if len(lines) != 1:
                return None  # Do not silently choose among equations for the same line.
            key = f'point_line_distance:{self.query.point}:{lines[0].fact_id}'
            return self.properties.get((self.query.line, key))
        if isinstance(self.query, FocalDistanceQuery):
            return self.properties.get((self.query.curve, f'focal_radius:{self.query.point}'))
        return self.values.get(self.query)
