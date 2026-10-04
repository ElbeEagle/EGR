"""Structural named-line facts; parsing does not parameterize or solve a line."""
from dataclasses import dataclass
import re
import sympy as sp
from src.solver.transition_primitives import parse_expression

NAME = r'([A-Za-z]\w*)'
LINE = rf'LineOf\(\s*{NAME}\s*,\s*{NAME}\s*\)'
SEGMENT_SLOPE = rf'Slope\(\s*LineSegmentOf\(\s*{NAME}\s*,\s*{NAME}\s*\)\s*\)'


@dataclass(frozen=True)
class NamedLine:
    line: str
    endpoints: tuple[str, str]


@dataclass(frozen=True)
class NamedIntersection:
    fact_id: str
    line: str
    curve: str
    points: tuple[str, str]  # Unordered labels, not an ordering of numeric roots.
    source: str


@dataclass(frozen=True)
class SlopeSum:
    fact_id: str
    base_point: str  # Common starting point; not necessarily coordinate origin.
    endpoints: tuple[str, str]
    value: sp.Expr
    nonzero_x_differences: tuple[tuple[str, str], ...]
    source: str


@dataclass(frozen=True)
class NamedLineQuery:
    line: str


def register_named_line(state, first: str, second: str, source_id: str) -> str:
    if first == second or any(state.entities.get(p) != 'Point' for p in (first, second)):
        raise ValueError('LineOf requires two distinct declared point labels')
    endpoints = tuple(sorted((first, second)))
    line = '@line:' + ':'.join(endpoints)
    state.entities[line] = 'Line'
    state.named_lines[line] = NamedLine(line, endpoints)
    key = f'identity:{line}'
    state.provenance[key] = tuple(dict.fromkeys((*state.provenance.get(key, ()), source_id)))
    return line


def parse_named_line_fact(state, part: str, fact_id: str) -> bool:
    """Record supported given relationships; return False for other syntax."""
    from .transition_state import PointOnCurve
    incidence = re.fullmatch(rf'PointOnCurve\(\s*{NAME}\s*,\s*{LINE}\s*\)', part)
    if incidence:
        point, first, second = incidence.groups()
        if state.entities.get(point) != 'Point':
            raise ValueError('Named line incidence requires a declared point')
        line = register_named_line(state, first, second, fact_id)
        state.incidences[fact_id] = PointOnCurve(fact_id, point, line, part)
        return True
    intersection = re.fullmatch(rf'Intersection\(\s*{LINE}\s*,\s*{NAME}\s*\)\s*=\s*\{{\s*{NAME}\s*,\s*{NAME}\s*\}}', part)
    if intersection:
        first, second, curve, a, b = intersection.groups()
        if state.entities.get(curve) != 'Parabola' or a == b or set((a,b)) != set((first,second)):
            raise ValueError('Named intersection requires its two line endpoints and a Parabola')
        line = register_named_line(state, first, second, fact_id)
        points = tuple(sorted((a,b)))
        state.named_intersections[fact_id] = NamedIntersection(fact_id, line, curve, points, part)
        for point in points:
            for owner in (line, curve):
                key = f'{fact_id}:on:{point}:{owner}'
                state.incidences[key] = PointOnCurve(key, point, owner, part)
                state.provenance[key] = (fact_id,)
        return True
    slope_sum = re.fullmatch(rf'{SEGMENT_SLOPE}\s*\+\s*{SEGMENT_SLOPE}\s*=\s*(.+)', part)
    if slope_sum:
        base, a, other_base, b, text = slope_sum.groups()
        if base != other_base or len({base,a,b}) != 3 or any(state.entities.get(p) != 'Point' for p in (base,a,b)):
            raise ValueError('Slope sum requires a common base and two distinct endpoints')
        value, guards = parse_expression(text, state.symbols)
        if guards or value.free_symbols or value.is_real is not True or value.is_finite is not True:
            raise ValueError('Slope sum currently requires a finite numeric target')
        points = tuple(sorted((a,b)))
        state.slope_sums[fact_id] = SlopeSum(fact_id, base, points, value,
                                           tuple((p,base) for p in points), part)
        return True
    return False
