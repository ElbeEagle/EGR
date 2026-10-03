"""Forward eccentricity consumes existing squared parameters; no hidden RM11/12."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from .bound_application import Proposal, check_binding, bound_parameters


def derive_eccentricity(state, action):
    fact = check_binding(state, action)
    if action.mode != 'derive_eccentricity':
        raise TransitionError('inapplicable', 'Unsupported RM13 mode')
    keys = ('a_sq', 'b_sq', 'c_sq')
    if any((action.curve, k) not in state.properties for k in keys):
        raise TransitionError('inapplicable', 'Existing a_sq, b_sq and c_sq required')
    bound_parameters(state, action.curve, fact.fact_id)
    a, b, c = [sp.simplify(state.properties[action.curve, k].subs(state.values)) for k in keys]
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (a,b,c)):
        raise TransitionError('undetermined', 'RM13 currently requires finite real parameters')
    if any(v.is_positive is not True for v in (a,b,c)):
        raise TransitionError('conflict', 'Squared parameters must be positive')
    residual = a-b-c if state.entities[action.curve] == 'Ellipse' else c-a-b
    if sp.simplify(residual) != 0:
        raise TransitionError('conflict', 'Existing c_sq violates conic parameter identity')
    value = sp.sqrt(sp.cancel(c/a))
    return Proposal(properties={(action.curve, 'eccentricity'): value},
                    read_facts=(fact.fact_id, f'entity:{action.curve}', f'frame:{action.curve}',
                                *(f'property:{action.curve}:{k}' for k in keys),
                                *state.constraints.keys(), *(f'value:{v}' for v in state.values)),
                    operations=[{'operation': 'verify_parameter_identity', 'residual': residual},
                                {'operation': 'eccentricity_from_squared_parameters',
                                 'a_sq': a, 'c_sq': c, 'result': value}])
