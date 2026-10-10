"""RM33 focal chord from committed standard geometry and a root sum."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
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
    from .focal_chord_evidence import verify_focus_line, verify_focal_chord
    verify_focal_chord(state, action)
    residual = verify_focus_line(line.expression.subs(state.values), x, y, focus)
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


def derive_coordinate_product(state, action):
    from .focal_chord_evidence import verify_focal_chord
    mode = {34:'derive_axial_product',35:'derive_transverse_product'}.get(action.model_id)
    if action.mode != mode:
        raise TransitionError('inapplicable','Unsupported coordinate product mode')
    evidence=verify_focal_chord(state,action)
    axial=action.model_id==34
    coordinate=evidence.axis if axial else ('y' if evidence.axis=='x' else 'x')
    value=sp.simplify(evidence.p**2/4 if axial else -evidence.p**2)
    return Proposal(properties={(evidence.owner,coordinate+'_product'):value},
        read_facts=evidence.reads,
        operations=[*evidence.operations, {'operation':'focal_chord_coordinate_product','axis':evidence.axis,
                     'coordinate':coordinate,'p':evidence.p,'value':value}])


def derive_origin_dot(state, action):
    from src.state.named_line_facts import OriginDotProductQuery
    fact=check_binding(state,action)
    q=state.query
    coord=state.coordinates.get(action.point)
    if (action.mode!='derive_origin_dot' or not isinstance(q,OriginDotProductQuery)
            or getattr(fact,'points',())!=q.points or action.point!=q.origin
            or coord is None or coord.fact_id!=action.coordinate_id):
        raise TransitionError('inapplicable','Origin dot binding mismatch')
    if any(sp.simplify(v.subs(state.values))!=0 for v in coord.xy):
        raise TransitionError('inapplicable','Only origin-based vectors supported')
    keys=[(fact.fact_id,c+'_product') for c in ('x','y')]
    if any(k not in state.properties for k in keys):
        raise TransitionError('inapplicable','Committed coordinate products required')
    values=[state.properties[k].subs(state.values) for k in keys]
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in values):
        raise TransitionError('undetermined','Finite numeric products required')
    value=sp.simplify(sum(values))
    return Proposal(properties={(q.owner,'dot_product'):value},
        read_facts=(fact.fact_id,coord.fact_id,*(f'property:{o}:{k}' for o,k in keys)),
        operations=[{'operation':'origin_dot_from_products','products':values,'value':value}])
