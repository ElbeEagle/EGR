"""Freshness evidence for numeric distances consuming RM73 lines."""
from dataclasses import dataclass
import hashlib
import sympy as sp
from src.solver.transition_primitives import TransitionError
from .two_point_line_facts import fresh_two_point_line
from src.solver.midpoint_operations import canonical_numeric_line


@dataclass(frozen=True)
class DistanceSnapshot:
    point: str
    line: str
    coordinate_id: str
    line_equation_id: str
    digest: str
    value: sp.Expr


def protected_distance(state, line, fact):
    return (line in state.named_lines or fact.fact_id == f'derived:{line}:two_points'
            or fact.source.startswith('RM73:'))


def distance_inputs(state, point, line, fact):
    matches = [f for f in state.equations.values() if f.owner == line and f.role == 'line']
    coordinate = state.coordinates.get(point)
    if (len(matches) != 1 or matches[0] != fact or fact.owner != line
            or not fresh_two_point_line(state, fact)):
        raise TransitionError('inapplicable', 'A unique fresh RM73 line is required')
    if state.entities.get(point) != 'Point' or coordinate is None or coordinate.point != point:
        raise TransitionError('inapplicable', 'Target point coordinates required')
    if not state.provenance.get(coordinate.fact_id):
        raise TransitionError('inapplicable', 'Target coordinate source required')
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in coordinate.xy):
        raise TransitionError('undetermined', 'Finite numeric target required')
    reads = (fact.fact_id, coordinate.fact_id, f'entity:{line}', f'entity:{point}')
    normal = canonical_numeric_line(fact.expression, state.symbols['x'], state.symbols['y'])
    payload = (point, line, repr(coordinate), fact.fact_id, str(normal), fact.source,
               state.provenance.get(fact.fact_id), state.provenance.get(coordinate.fact_id),
               tuple(sorted((str(k),str(v)) for k,v in state.values.items())))
    digest = hashlib.sha256(repr(payload).encode()).hexdigest()
    return coordinate, digest, reads


def make_distance_snapshot(state, point, line, fact, value):
    coordinate, digest, _ = distance_inputs(state, point, line, fact)
    return DistanceSnapshot(point, line, coordinate.fact_id, fact.fact_id, digest, value)


def read_named_distance(state, point, line, fact):
    key = (line, f'point_line_distance:{point}:{fact.fact_id}')
    evidence = state.distance_snapshots.get(key)
    value = state.properties.get(key)
    if evidence is None or value is None:
        return None
    try:
        expected = make_distance_snapshot(state, point, line, fact, value)
        _, _, reads = distance_inputs(state, point, line, fact)
        source = state.provenance.get(f'property:{key[0]}:{key[1]}', ())
        if evidence != expected or any(k not in source for k in reads):
            return None
    except TransitionError:
        return None
    return value
