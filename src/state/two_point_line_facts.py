"""RM73 coordinate binding and read-only freshness checks."""
import hashlib
from src.solver.transition_primitives import TransitionError
from src.solver.midpoint_operations import canonical_numeric_line


def point_pair_inputs(state, line):
    identity = state.named_lines.get(line)
    if identity is None or state.entities.get(line) != 'Line' or len(set(identity.endpoints)) != 2:
        raise TransitionError('inapplicable', 'Named two-point line required')
    reads = [f'identity:{line}']
    if not state.provenance.get(reads[0]):
        raise TransitionError('inapplicable', 'Line identity source required')
    coordinates = []
    for name in identity.endpoints:
        point = state.coordinates.get(name)
        if state.entities.get(name) != 'Point' or point is None or point.point != name:
            raise TransitionError('inapplicable', 'Current point coordinates required')
        if not state.provenance.get(point.fact_id):
            raise TransitionError('inapplicable', 'Coordinate source required')
        coordinates.append(point)
        reads.extend((f'entity:{name}', point.fact_id))
    return tuple(coordinates), tuple(reads)


def coordinate_snapshot(state, line):
    coordinates, reads = point_pair_inputs(state, line)
    payload = (line, state.named_lines[line].endpoints, tuple(map(repr, coordinates)),
               tuple((k, state.provenance.get(k)) for k in reads),
               tuple(sorted((str(k), str(v)) for k, v in state.values.items())))
    return hashlib.sha256(repr(payload).encode()).hexdigest()


def line_snapshot(state, line, expression):
    normal = canonical_numeric_line(expression, state.symbols['x'], state.symbols['y'])
    return 'RM73:' + hashlib.sha256((coordinate_snapshot(state, line)+str(normal)).encode()).hexdigest()


def fresh_two_point_line(state, fact):
    try:
        _, reads = point_pair_inputs(state, fact.owner)
        return (fact.role == 'line' and fact.fact_id == f'derived:{fact.owner}:two_points'
                and all(k in state.provenance.get(fact.fact_id, ()) for k in reads)
                and fact.source == line_snapshot(state, fact.owner, fact.expression))
    except TransitionError:
        return False
