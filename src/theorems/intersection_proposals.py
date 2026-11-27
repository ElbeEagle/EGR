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
    matches=[n for n in state.named_intersections.values() if (n.curve,n.line)==(action.curve,action.line)]
    if len({n.points for n in matches})>1:
        raise TransitionError('conflict','Ambiguous named endpoint pairs')
    if matches:
        from dataclasses import replace
        fact=replace(fact,named_points=matches[0].points,intersection_id=matches[0].fact_id)
    reads = (*(n.fact_id for n in matches), f'entity:{action.curve}', f'entity:{action.line}', curve.fact_id, line.fact_id,
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
    parameters, extra_reads = (), ()
    if fact.named_points and fact.line not in state.parameterizations:
        from .root_midpoint_proposals import verify_numeric_association
        extra_reads=verify_numeric_association(state,fact)
    elif fact.named_points:
        local = state.parameterizations.get(fact.line)
        named = state.named_intersections.get(fact.intersection_id)
        if (local is None or named is None or named.points != fact.named_points
                or named.line != fact.line or named.curve != fact.curve
                or local.line_equation_id != fact.line_equation_id):
            raise TransitionError('inapplicable', 'Missing scoped named-root association')
        parameters = (local.parameter,)
        extra_reads = (f'parameterization:{fact.line}', named.fact_id, *state.constraints.keys())
    value = quadratic_root_relation(fact.polynomial, fact.variable, kind, parameters)
    status = classify_quadratic_roots(fact.polynomial, fact.variable, parameters,
                                      [c.subs(state.values) for c in state.constraints.values()])
    return Proposal(properties={(fact.fact_id, f'root_{kind}'): value,
                                (fact.fact_id, 'discriminant'): status.discriminant,
                                (fact.fact_id, 'distinct_real_roots'): sp.Integer(status.distinct_real_roots)},
                    read_facts=(fact.fact_id, *extra_reads),
                    operations=[{'operation': 'vieta_'+kind, 'variable': fact.variable, 'value': value},
                                {'operation': 'classify_real_roots', 'discriminant': status.discriminant,
                                 'distinct_real_roots': status.distinct_real_roots}])


def derive_root_relations(state, action):
    """Propose both numeric quadratic relations and real-root qualification atomically."""
    import sympy as sp
    from src.solver.intersection_operations import quadratic_root_relation, classify_quadratic_roots
    fact = check_binding(state, action)
    if action.mode != 'derive_root_relations':
        raise TransitionError('inapplicable', 'Unsupported joint root relation mode')
    if fact.named_points and fact.line not in state.parameterizations:
        from .root_midpoint_proposals import verify_numeric_association
        verify_numeric_association(state,fact)
    # No allowed symbolic parameters: RM41's first mode is strictly numeric.
    total = quadratic_root_relation(fact.polynomial, fact.variable, 'sum')
    product = quadratic_root_relation(fact.polynomial, fact.variable, 'product')
    status = classify_quadratic_roots(fact.polynomial, fact.variable)
    return Proposal(properties={(fact.fact_id, 'root_sum'): total,
                                (fact.fact_id, 'root_product'): product,
                                (fact.fact_id, 'discriminant'): status.discriminant,
                                (fact.fact_id, 'distinct_real_roots'): sp.Integer(status.distinct_real_roots)},
                    read_facts=(fact.fact_id,),
                    operations=[{'operation': 'vieta_sum', 'variable': fact.variable, 'value': total},
                                {'operation': 'vieta_product', 'variable': fact.variable, 'value': product},
                                {'operation': 'classify_real_roots', 'discriminant': status.discriminant,
                                 'distinct_real_roots': status.distinct_real_roots}])


def verified_root_pair(state, fact):
    """Check committed relations and two-real-root qualification; never fill gaps."""
    import sympy as sp
    from src.solver.intersection_operations import quadratic_coefficients
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
    return total, product, names


def derive_chord_length(state, action):
    import sympy as sp
    from src.solver.intersection_operations import quadratic_coefficients, chord_length_from_relations
    check_binding(state, action)
    if action.mode != 'derive_chord_length':
        raise TransitionError('inapplicable', 'Unsupported chord mode')
    fact = state.intersection_reductions[action.relation_id]
    total, product, names = verified_root_pair(state, fact)
    length = chord_length_from_relations(total, product, fact.xy, fact.variable)
    return Proposal(properties={(fact.fact_id, 'chord_length'): length},
                    read_facts=(fact.fact_id, *(f'property:{fact.fact_id}:{n}' for n in names)),
                    operations=[{'operation': 'chord_length_from_root_relations', 'xy': fact.xy,
                                 'root_sum': total, 'root_product': product, 'length': length}])


def parameterize_named_line(state, action):
    import sympy as sp
    from src.solver.intersection_operations import parameterize_through_point
    from src.state.transition_state import EquationFact, LineParameterization
    curve = check_binding(state, action)
    line_id = f'derived:{action.line}:parameterized'
    if any(f.owner == action.line and f.role == 'line' and f.fact_id != line_id
           for f in state.equations.values()):
        raise TransitionError('inapplicable', 'Line already has an independent equation')
    parameter = sp.Symbol(f'@parameter:{action.line}:u', real=True)
    xy = tuple(v.subs(state.values) for v in state.coordinates[action.point].xy)
    reduction, horizontal = parameterize_through_point(curve.expression.subs(state.values),
        state.symbols['x'], state.symbols['y'], xy, parameter)
    n = state.named_intersections[action.relation_id]
    key = f'derived:intersection:{curve.fact_id}:{line_id}'
    fact = IntersectionReduction(key, action.curve, action.line, curve.fact_id, line_id,
        reduction.variable, reduction.xy, reduction.polynomial, 'RM78', n.points, n.fact_id)
    local = LineParameterization(action.line, parameter, action.point, action.coordinate_id,
                                action.incidence_id, n.fact_id, line_id)
    reads = (curve.fact_id, action.coordinate_id, action.incidence_id, n.fact_id,
             f'identity:{action.line}', *(f'value:{v}' for v in sorted(state.values, key=str)))
    distinct_guard = sp.Gt(sp.discriminant(fact.polynomial, fact.variable), 0)
    return Proposal(constraints={f'{key}:distinct_roots': distinct_guard},
                    equations={line_id: EquationFact(line_id, action.line, 'line',
                            state.symbols['x']-reduction.xy[0], 'RM78')},
                    intersection_reductions={key: fact}, parameterizations={action.line: local},
                    read_facts=reads,
                    operations=[{'operation':'exclude_horizontal_branch', 'polynomial':horizontal,
                                 'distinct_intersections':1, 'required':2},
                                {'operation':'parameterize_through_point', 'parameter':parameter,
                                 'xy':reduction.xy},
                                {'operation':'substitute_and_associate_roots', 'polynomial':fact.polynomial,
                                 'unordered_points':n.points, 'coordinate':'y',
                                 'required_distinct_guard':distinct_guard}])


def derive_slope_chord_length(state, action):
    """Finite RM51 consumes scoped root facts and proposes the existing chord property."""
    import sympy as sp
    from src.solver.intersection_operations import slope_chord_length
    fact = check_binding(state, action)
    if action.mode != 'derive_chord_length':
        raise TransitionError('inapplicable', 'Unsupported RM51 mode')
    total, product, names = verified_root_pair(state, fact)
    reads = (fact.fact_id, *(f'property:{fact.fact_id}:{n}' for n in names))
    if any(fact.fact_id not in state.provenance.get(k, ()) for k in reads[1:]):
        raise TransitionError('inapplicable', 'Root relation sources required')
    if any(k not in state.provenance.get(fact.fact_id, ()) for k in (action.equation_id, action.line_equation_id)):
        raise TransitionError('inapplicable', 'Reduction equation sources required')
    curve = state.equations[action.equation_id].expression.subs(state.values)
    line = state.equations[action.line_equation_id].expression.subs(state.values)
    x, y = state.symbols['x'], state.symbols['y']
    substitute_line_in_parabola(curve, line, x, y)  # Restrict to the existing numeric family.
    length, details = slope_chord_length(total, product, fact.xy, fact.variable)
    mapping = dict(zip((x, y), fact.xy))
    if sp.simplify(line.subs(mapping, simultaneous=True)) != 0:
        raise TransitionError('conflict', 'Lift no longer matches line')
    current = sp.Poly(curve.subs(mapping, simultaneous=True), fact.variable)
    recorded = sp.Poly(fact.polynomial, fact.variable)
    if current.degree() != 2 or sp.simplify(current.monic().as_expr()-recorded.monic().as_expr()) != 0:
        raise TransitionError('conflict', 'Reduction no longer matches curve')
    return Proposal(properties={(fact.fact_id, 'chord_length'): length},
                    read_facts=(*reads, action.equation_id, action.line_equation_id),
                    operations=[{'operation': 'finite_slope_chord', 'variable': fact.variable,
                                 **details, 'length': length}])
