"""RM33 focal chord from committed standard geometry and a root sum."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.parabola_operations import substitute_point
from src.solver.intersection_operations import quadratic_coefficients
from .parabola_proposals import bound_parabola, parabola_reads
from .bound_application import Proposal, check_binding


def derive_focal_chord(state, action):
    reduction = check_binding(state, action)
    if action.mode != 'derive_focal_chord':
        raise TransitionError('inapplicable', 'Unsupported RM33 mode')
    _, axis, sign, p, focus = bound_parabola(state, action, state.equations[action.equation_id])
    x, y = state.symbols['x'], state.symbols['y']
    line = state.equations[action.line_equation_id]
    residual = substitute_point(line.expression.subs(state.values), x, y, focus)
    if residual != 0:
        raise TransitionError('inapplicable', 'Bound line does not pass through focus')
    names = ('root_sum', 'discriminant', 'distinct_real_roots')
    if any((reduction.fact_id,n) not in state.properties for n in names):
        raise TransitionError('inapplicable', 'Committed root sum and real-pair qualification required')
    total, disc, count = (state.properties[(reduction.fact_id,n)].subs(state.values) for n in names)
    a,b,c = quadratic_coefficients(reduction.polynomial, reduction.variable)
    if sp.simplify(a*total+b)!=0 or sp.simplify(disc-(b*b-4*a*c))!=0:
        raise TransitionError('conflict', 'Root properties disagree with source polynomial')
    if count != 2 or disc.is_positive is not True:
        raise TransitionError('inapplicable', 'Two distinct finite real intersections required')
    # Lift the sum to the longitudinal coordinate; no product or root solving.
    axial = sp.Poly(reduction.xy[0 if axis=='x' else 1], reduction.variable)
    if axial.degree()>1 or any(v.free_symbols or v.is_real is not True or v.is_finite is not True
                              for v in axial.all_coeffs()):
        raise TransitionError('undetermined', 'Numeric affine longitudinal lift required')
    axial_sum = sp.simplify(axial.nth(1)*total+2*axial.nth(0))
    length = sp.simplify(sign*axial_sum+p)
    if length.free_symbols or length.is_positive is not True:
        raise TransitionError('undetermined', 'Positive numeric focal chord not established')
    return Proposal(properties={(reduction.fact_id,'chord_length'):length,
                                (reduction.fact_id,'focus_on_line'):sp.S.One},
                    read_facts=(*parabola_reads(state,action),line.fact_id,reduction.fact_id,
                                *(f'property:{reduction.fact_id}:{n}' for n in names)),
                    operations=[{'operation':'verify_line_through_focus','focus':focus,'residual':residual},
                                {'operation':'focal_chord_from_root_sum','axis':axis,'sign':sign,
                                 'axial_sum':axial_sum,'p':p,'length':length}])
