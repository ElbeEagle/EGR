"""Bound standard-parabola recovery and focal-radius proposals."""
import sympy as sp
from src.solver.transition_primitives import TransitionError, finite_real_solutions, truth
from src.solver.parabola_operations import (
    DIRECTIONS, parabola_coefficient, substitute_point, parabola_geometry,
)
from src.state.transition_state import CurveFrame
from .bound_application import Proposal, check_binding


def standard_parabola_proposal(state, action):
    fact = check_binding(state, action)
    if action.mode not in ('extract_parameters', 'recover_from_point'):
        raise TransitionError('inapplicable', 'Unsupported standard-parabola mode')
    axis, sign, direction = DIRECTIONS[action.model_id]
    x, y = state.symbols['x'], state.symbols['y']
    coefficient = parabola_coefficient(fact.expression, x, y, axis, list(state.constraints.values()))
    values = dict(state.values)
    reads = [fact.fact_id, f'entity:{action.curve}', *state.constraints.keys(),
             *(f'value:{s}' for s in state.values)]
    operations, assignments, candidates = [], {}, ()
    if action.mode == 'recover_from_point':
        coordinate = state.coordinates[action.point]
        xy = tuple(v.subs(values) for v in coordinate.xy)
        residual = substitute_point(fact.expression.subs(values), x, y, xy)
        reads.extend((action.coordinate_id, action.relation_id))
        operations.append({'operation': 'instantiate_point_incidence', 'point': action.point,
                           'curve': action.curve, 'relation': action.relation_id,
                           'coordinate': action.coordinate_id, 'residual': residual})
        unknowns = coefficient.subs(values).free_symbols
        if unknowns:
            if len(unknowns) != 1:
                raise TransitionError('undetermined', 'Point recovery supports one unknown coefficient parameter')
            target = next(iter(unknowns))
            # Do not use the candidate opening direction as a root filter.
            candidates = finite_real_solutions(residual, target,
                                               [c.subs(values) for c in state.constraints.values()], operations)
            if not candidates:
                raise TransitionError('conflict', 'Point incidence has no admissible parameter solution')
            if len(candidates) > 1:
                return Proposal(read_facts=tuple(reads), operations=operations, candidates=candidates)
            assignments[target] = candidates[0]
            values.update(assignments)
        valid = truth(sp.Eq(residual.subs(values), 0))
        if valid is not True:
            raise TransitionError('conflict' if valid is False else 'undetermined', 'Point not on bound curve')
    resolved = sp.simplify(coefficient.subs(values))
    p, focus = parabola_geometry(resolved, axis, sign,
                                 [c.subs(values) for c in state.constraints.values()])
    operations.append({'operation': 'standard_parabola', 'direction': direction,
                       'coefficient': resolved, 'p': p, 'focus': focus})
    return Proposal(properties={(action.curve, 'p'): p, (action.curve, 'focus_x'): focus[0],
                                (action.curve, 'focus_y'): focus[1]},
                    values=assignments, candidates=candidates, read_facts=tuple(reads), operations=operations,
                    frames={action.curve: CurveFrame(fact.fact_id, axis=axis, direction=direction)})


def focal_radius_proposal(state, action):
    fact = check_binding(state, action)
    if action.mode != 'focal_radius':
        raise TransitionError('inapplicable', 'Unsupported RM17 mode')
    frame = state.frames.get(action.curve)
    if (frame is None or frame.equation_id != fact.fact_id or frame.center != (0, 0)
            or frame.direction not in {d[2] for d in DIRECTIONS.values()}):
        raise TransitionError('inapplicable', 'Missing standard-parabola frame')
    axis, sign, _ = next(d for d in DIRECTIONS.values() if d[2] == frame.direction)
    if frame.axis != axis:
        raise TransitionError('conflict', 'Parabola axis and direction disagree')
    x, y = state.symbols['x'], state.symbols['y']
    coefficient = parabola_coefficient(fact.expression, x, y, axis, list(state.constraints.values())).subs(state.values)
    p, focus = parabola_geometry(coefficient, axis, sign, list(state.constraints.values()))
    for key, expected in (('p', p), ('focus_x', focus[0]), ('focus_y', focus[1])):
        if (action.curve, key) not in state.properties:
            raise TransitionError('inapplicable', 'Missing standard-parabola property')
        if sp.simplify(state.properties[action.curve, key].subs(state.values)-expected) != 0:
            raise TransitionError('conflict', 'Parabola property does not match bound equation')
    xy = tuple(v.subs(state.values) for v in state.coordinates[action.point].xy)
    residual = substitute_point(fact.expression.subs(state.values), x, y, xy)
    valid = truth(sp.Eq(residual, 0), list(state.constraints.values()))
    if valid is not True:
        raise TransitionError('conflict' if valid is False else 'undetermined', 'Point incidence not verified')
    u = sign*xy[0 if axis == 'x' else 1]
    radius = sp.simplify(u+p/2)
    if truth(radius > 0, list(state.constraints.values())) is not True:
        raise TransitionError('undetermined', 'Positive focal radius not established')
    return Proposal(properties={(action.curve, f'focal_radius:{action.point}'): radius},
                    read_facts=(fact.fact_id, action.coordinate_id, action.relation_id,
                                f'frame:{action.curve}', *state.constraints.keys(),
                                *(f'value:{s}' for s in state.values),
                                *(f'property:{action.curve}:{k}' for k in ('p', 'focus_x', 'focus_y'))),
                    operations=[{'operation': 'verify_point_incidence', 'residual': residual},
                                {'operation': 'parabola_focal_radius', 'point': action.point,
                                 'direction': frame.direction, 'u': u, 'p': p, 'result': radius}])
