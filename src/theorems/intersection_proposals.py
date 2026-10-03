"""RM78 equation-scoped substitution, distinct from root/point inference."""
from src.solver.transition_primitives import TransitionError
from src.solver.intersection_operations import substitute_line_in_parabola
from src.state.transition_state import IntersectionReduction
from .bound_application import Proposal, check_binding


def substitute_bound_line(state, action):
    curve = check_binding(state, action)
    if action.mode != 'substitute_line':
        raise TransitionError('inapplicable', 'Unsupported RM78 mode')
    line = state.equations[action.line_equation_id]
    reduction = substitute_line_in_parabola(curve.expression.subs(state.values),
        line.expression.subs(state.values), state.symbols['x'], state.symbols['y'])
    key = f'derived:intersection:{curve.fact_id}:{line.fact_id}'
    fact = IntersectionReduction(key, action.curve, action.line, curve.fact_id, line.fact_id,
                                 reduction.variable, reduction.xy, reduction.polynomial, 'RM78')
    reads = (f'entity:{action.curve}', f'entity:{action.line}', curve.fact_id, line.fact_id,
             *(f'value:{s}' for s in sorted((curve.expression.free_symbols | line.expression.free_symbols)
                                           & state.values.keys(), key=str)))
    return Proposal(intersection_reductions={key: fact}, read_facts=reads,
                    operations=[{'operation': 'parameterize_line', 'variable': reduction.variable,
                                 'xy': reduction.xy},
                                {'operation': 'substitute_and_normalize', 'polynomial': reduction.polynomial}])


def derive_root_relation(state, action):
    import sympy as sp
    from src.solver.intersection_operations import quadratic_root_relation, classify_quadratic_roots
    check_binding(state, action)
    kind = {42: 'sum', 43: 'product'}[action.model_id]
    if action.mode != f'derive_root_{kind}':
        raise TransitionError('inapplicable', 'Unsupported root relation mode')
    fact = state.intersection_reductions[action.relation_id]
    value = quadratic_root_relation(fact.polynomial, fact.variable, kind)
    status = classify_quadratic_roots(fact.polynomial, fact.variable)
    return Proposal(properties={(fact.fact_id, f'root_{kind}'): value,
                                (fact.fact_id, 'discriminant'): status.discriminant,
                                (fact.fact_id, 'distinct_real_roots'): sp.Integer(status.distinct_real_roots)},
                    read_facts=(fact.fact_id,),
                    operations=[{'operation': 'vieta_'+kind, 'variable': fact.variable, 'value': value},
                                {'operation': 'classify_real_roots', 'discriminant': status.discriminant,
                                 'distinct_real_roots': status.distinct_real_roots}])


def derive_chord_length(state, action):
    import sympy as sp
    from src.solver.intersection_operations import quadratic_coefficients, chord_length_from_relations
    check_binding(state, action)
    if action.mode != 'derive_chord_length':
        raise TransitionError('inapplicable', 'Unsupported chord mode')
    fact = state.intersection_reductions[action.relation_id]
    names = ('root_sum', 'root_product', 'discriminant', 'distinct_real_roots')
    if any((fact.fact_id, name) not in state.properties for name in names):
        raise TransitionError('inapplicable', 'Committed root relations and qualification required')
    total, product, discriminant, count = (state.properties[(fact.fact_id, n)] for n in names)
    a, b, c = quadratic_coefficients(fact.polynomial, fact.variable)
    # Check supplied results against their source; never fill a missing relation.
    if any(sp.simplify(v) != 0 for v in (a*total+b, a*product-c, discriminant-(b*b-4*a*c))):
        raise TransitionError('conflict', 'Root properties disagree with source polynomial')
    if count != 2 or discriminant.is_positive is not True:
        raise TransitionError('inapplicable', 'Not a pair of distinct real intersections')
    length = chord_length_from_relations(total, product, fact.xy, fact.variable)
    return Proposal(properties={(fact.fact_id, 'chord_length'): length},
                    read_facts=(fact.fact_id, *(f'property:{fact.fact_id}:{n}' for n in names)),
                    operations=[{'operation': 'chord_length_from_root_relations', 'xy': fact.xy,
                                 'root_sum': total, 'root_product': product, 'length': length}])
