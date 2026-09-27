"""Shared centered standard-conic extraction for RM3/4/5/6."""
from src.solver.transition_primitives import (
    TransitionError, axis_denominators, ellipse_parameters, require, truth,
)
from src.state.transition_state import CurveFrame
from .bound_application import Proposal, check_binding


def standard_proposal(state, action, axis):
    if action.mode != 'extract_parameters':
        raise TransitionError('inapplicable', 'Unsupported standard-conic mode')
    fact = check_binding(state, action)
    constraints = list(state.constraints.values())
    kind = state.entities[action.curve]
    derived = {}
    if kind == 'Ellipse':
        a_sq, b_sq = ellipse_parameters(fact.expression, state.symbols['x'], state.symbols['y'],
                                        constraints, axis)
    else:
        a_sq, transverse = axis_denominators(fact.expression, state.symbols['x'], state.symbols['y'], axis)
        b_sq = -transverse
        require(a_sq > 0, constraints, 'Positive focal-axis semi-axis square not established')
        sign = truth(b_sq > 0, constraints)
        if sign is False:
            raise TransitionError('inapplicable', 'Equation contradicts the declared hyperbola type')
        if sign is None:
            derived[f'derived:{fact.fact_id}:b_sq_positive'] = b_sq > 0
    operations = [{'operation': f'standard_{kind.lower()}_{axis}', 'equation': fact.fact_id,
                   'axis': axis, 'a_sq': a_sq, 'b_sq': b_sq}]
    for key, condition in derived.items():
        operations.append({'operation': 'derive_type_condition', 'curve': action.curve,
                           'type': kind, 'equation': fact.fact_id,
                           'condition_id': key, 'condition': condition})
    return Proposal(properties={(action.curve, 'a_sq'): a_sq, (action.curve, 'b_sq'): b_sq},
                    frames={action.curve: CurveFrame(fact.fact_id, axis=axis)},
                    read_facts=(fact.fact_id, f'entity:{action.curve}', *state.constraints.keys()),
                    operations=operations, constraints=derived)
