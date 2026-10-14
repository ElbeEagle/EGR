"""RM38/39 tangents at verified numeric points of standard conics."""
import sympy as sp
from src.solver.transition_primitives import TransitionError, truth
from src.solver.parabola_operations import substitute_point
from src.state.transition_state import EquationFact
from .bound_application import Proposal, check_binding
from .parabola_proposals import bound_parabola, parabola_reads


def derive_parabola_tangent(state, action):
    fact = check_binding(state, action)
    if action.mode != 'derive_tangent':
        raise TransitionError('inapplicable', 'Unsupported RM39 mode')
    _, axis, sign, p, _ = bound_parabola(state, action, fact)
    if p.free_symbols or p.is_real is not True or p.is_finite is not True:
        raise TransitionError('undetermined', 'Tangent mode requires finite numeric parameter')
    x, y = state.symbols['x'], state.symbols['y']
    xy = tuple(v.subs(state.values) for v in state.coordinates[action.point].xy)
    residual = substitute_point(fact.expression.subs(state.values), x, y, xy)
    valid = truth(sp.Eq(residual, 0))
    if valid is not True:
        raise TransitionError('conflict' if valid is False else 'undetermined', 'Tangent point not on curve')
    u, v = (x, y) if axis == 'x' else (y, x)
    u0, v0 = xy if axis == 'x' else xy[::-1]
    expression = sp.expand(v0*v-sign*p*(u+u0))
    key = f'derived:{action.curve}:tangent:{action.point}'
    return Proposal(equations={key: EquationFact(key, action.curve, 'tangent', expression, 'RM39')},
                    read_facts=(*parabola_reads(state, action), action.coordinate_id, f'entity:{action.point}'),
                    operations=[{'operation': 'verify_tangent_point', 'residual': residual},
                                {'operation': 'parabola_tangent', 'axis': axis, 'sign': sign,
                                 'p': p, 'point': action.point, 'equation': expression}])


def derive_ellipse_tangent(state, action):
    """Consume committed standard parameters and propose one verified tangent."""
    from src.solver.tangent_operations import ellipse_tangent
    from .bound_application import bound_parameters, bound_axis
    fact = check_binding(state, action)
    if action.mode != 'derive_tangent':
        raise TransitionError('inapplicable', 'Unsupported RM38 mode')
    a_sq, b_sq = bound_parameters(state, action.curve, action.equation_id)
    axis = bound_axis(state, action.curve, action.equation_id)
    x_sq, y_sq = (a_sq, b_sq) if axis == 'x' else (b_sq, a_sq)
    xy = tuple(v.subs(state.values) for v in state.coordinates[action.point].xy)
    residual, expression = ellipse_tangent(state.symbols['x'], state.symbols['y'],
        x_sq.subs(state.values), y_sq.subs(state.values), xy)
    key = f'derived:{action.curve}:tangent:{action.point}'
    return Proposal(
        equations={key: EquationFact(key, action.curve, 'tangent', expression, 'RM38')},
        read_facts=(fact.fact_id, action.coordinate_id, f'entity:{action.curve}',
                    f'entity:{action.point}', f'frame:{action.curve}',
                    *(f'property:{action.curve}:{k}' for k in ('a_sq', 'b_sq')),
                    *state.constraints, *(f'value:{v}' for v in state.values)),
        operations=[{'operation': 'verify_tangent_point', 'residual': residual},
                    {'operation': 'ellipse_tangent', 'axis': axis, 'point': action.point,
                     'x_sq': x_sq, 'y_sq': y_sq, 'equation': expression}])
