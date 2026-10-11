"""Given coordinate aliases and product targets; no symbolic theorem execution."""
from dataclasses import dataclass
import re

NAME = r'([A-Za-z]\w*)'


@dataclass(frozen=True)
class CoordinateComponentAlias:
    fact_id: str
    symbol: str
    point: str
    axis: str
    source: str


@dataclass(frozen=True)
class IntersectionCount:
    fact_id: str
    line: str
    curve: str
    count: int
    source: str


@dataclass(frozen=True)
class CoordinateProductQuery:
    symbols: tuple[str, str]


def parse_coordinate_product_fact(state, text: str, fact_id: str) -> bool:
    """Record a component identity or given count, without producing coordinates."""
    alias = re.fullmatch(rf'([XY])Coordinate\(\s*{NAME}\s*\)\s*=\s*{NAME}', text)
    if alias:
        axis, point, symbol = alias.groups()
        if state.entities.get(point) != 'Point' or state.entities.get(symbol) not in ('Number', 'Real'):
            raise ValueError('Coordinate alias requires a Point and declared scalar')
        if symbol in state.coordinate_aliases:
            raise ValueError('Duplicate or ambiguous coordinate alias')
        state.coordinate_aliases[symbol] = CoordinateComponentAlias(fact_id, symbol, point, axis.lower(), text)
        return True
    count = re.fullmatch(rf'NumIntersection\(\s*{NAME}\s*,\s*{NAME}\s*\)\s*=\s*(\d+)', text)
    if count:
        first, second, number = count.groups()
        if sorted(state.entities.get(v, '') for v in (first, second)) != ['Line', 'Parabola']:
            raise ValueError('Intersection count requires a Line and Parabola')
        line, curve = (first, second) if state.entities[first] == 'Line' else (second, first)
        state.intersection_counts[fact_id] = IntersectionCount(fact_id, line, curve, int(number), text)
        return True
    return False


def validate_coordinate_product_input(state) -> None:
    """Reject inconsistent declarations; do not infer point or parameter values."""
    counts = {}
    for fact in state.intersection_counts.values():
        key = (fact.line, fact.curve)
        if key in counts and counts[key] != fact.count:
            raise ValueError('Conflicting intersection counts')
        counts[key] = fact.count
    for fact in state.named_intersections.values():
        if (fact.line, fact.curve) in counts and counts[fact.line, fact.curve] != len(fact.points):
            raise ValueError('Intersection count conflicts with named pair')
    if isinstance(state.query, CoordinateProductQuery):
        aliases = [state.coordinate_aliases.get(s) for s in state.query.symbols]
        if any(a is None for a in aliases):
            raise ValueError('Product query requires two coordinate aliases')
        first, second = aliases
        if first.axis != second.axis or first.point == second.point:
            raise ValueError('Product query requires one axis and two distinct points')


def read_coordinate_product(state, query: CoordinateProductQuery):
    """Locate a unique named pair's committed product; never multiply coordinates."""
    aliases = [state.coordinate_aliases.get(s) for s in query.symbols]
    if any(a is None for a in aliases):
        return None
    first, second = aliases
    if first.axis != second.axis or first.point == second.point:
        return None
    points = tuple(sorted((first.point, second.point)))
    candidates = [f for f in state.named_intersections.values() if f.points == points]
    if len(candidates) != 1:
        return None
    return state.properties.get((candidates[0].fact_id, first.axis + '_product'))
