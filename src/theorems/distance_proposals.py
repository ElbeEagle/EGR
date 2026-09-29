"""Bound distances for independent lines and existing parabola directrices."""
from src.solver.transition_primitives import TransitionError
from src.solver.distance_operations import point_to_line_distance
from .bound_application import Proposal, check_binding


def point_line_distance_proposal(state, action):
    check_binding(state, action)
    if action.mode != 'point_line_distance':
        raise TransitionError('inapplicable', 'Unsupported RM52 mode')
    line = state.equations[action.line_equation_id]
    xy = tuple(v.subs(state.values) for v in state.coordinates[action.point].xy)
    distance = point_to_line_distance(line.expression.subs(state.values),
                                      state.symbols['x'], state.symbols['y'], xy)
    owner = action.line if action.line is not None else action.curve
    key = f'point_line_distance:{action.point}:{line.fact_id}'
    return Proposal(properties={(owner, key): distance},
                    read_facts=(line.fact_id, action.coordinate_id, f'entity:{owner}', f'entity:{action.point}',
                                *state.constraints.keys(), *(f'value:{s}' for s in state.values)),
                    operations=[{'operation': 'point_to_line_distance', 'point': action.point,
                                 'line': line.fact_id, 'result': distance}])


