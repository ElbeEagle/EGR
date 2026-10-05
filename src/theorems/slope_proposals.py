"""RM55: origin-based slope sum on a named pair of a standard parabola."""
import sympy as sp
from src.solver.transition_primitives import TransitionError, require, truth, finite_real_solutions
from src.solver.parabola_operations import parabola_coefficient
from src.solver.intersection_operations import quadratic_coefficients
from .bound_application import Proposal, check_binding


def solve_named_slope_sum(state, action):
    fact = check_binding(state, action)
    if action.mode != 'solve_slope_sum':
        raise TransitionError('inapplicable', 'Unsupported RM55 mode')
    slope = state.slope_sums[action.slope_sum_id]
    local = state.parameterizations.get(fact.line)
    named = state.named_intersections.get(fact.intersection_id)
    base = state.coordinates.get(slope.base_point)
    if (local is None or named is None or named.points != fact.named_points
            or named.line != fact.line or named.curve != fact.curve
            or local.line_equation_id != fact.line_equation_id or base is None):
        raise TransitionError('inapplicable', 'Scoped parameter, root association and base coordinates required')
    if any(sp.simplify(v.subs(state.values)) != 0 for v in base.xy):
        raise TransitionError('inapplicable', 'First slope-sum mode requires the coordinate origin')
    names = ('root_sum', 'root_product', 'discriminant', 'distinct_real_roots')
    if any((fact.fact_id, n) not in state.properties for n in names):
        raise TransitionError('inapplicable', 'Committed Vieta relations and root qualification required')
    total, product, discriminant, count = (state.properties[(fact.fact_id,n)].subs(state.values) for n in names)
    parameter = local.parameter
    a,b,c = quadratic_coefficients(fact.polynomial, fact.variable, (parameter,))
    if any(sp.simplify(v) != 0 for v in (a*total+b, a*product-c, discriminant-(b*b-4*a*c))):
        raise TransitionError('conflict', 'Root relations disagree with polynomial')
    conditions = [v.subs(state.values) for v in state.constraints.values()]
    if count != 2:
        raise TransitionError('inapplicable', 'Two distinct real roots required')
    require(discriminant > 0, conditions, 'Real root pair not established')
    require(sp.Ne(product,0), conditions, 'Nonzero root product needed before dividing')
    x,y = state.symbols['x'],state.symbols['y']
    coefficient = parabola_coefficient(state.equations[fact.curve_equation_id].expression.subs(state.values),x,y,'x')
    if coefficient.free_symbols or coefficient.is_real is not True or coefficient.is_zero is not False:
        raise TransitionError('inapplicable', 'Numeric nonzero parabola coefficient required')
    if fact.variable != y or sp.simplify(fact.xy[1]-y)!=0:
        raise TransitionError('inapplicable', 'Slope formula requires y-coordinate roots')
    residual = sp.cancel(coefficient*total/product-slope.value)
    operations = [{'operation':'verify_slope_denominators', 'root_product':product,
                   'x_product':sp.cancel(product**2/coefficient**2), 'points':fact.named_points},
                  {'operation':'slope_sum_from_vieta', 'expression':residual+slope.value,
                   'target':slope.value, 'residual':residual}]
    assignments, candidates = {}, ()
    if parameter not in state.values:
        candidates = finite_real_solutions(residual,parameter,conditions,operations)
        if not candidates:
            raise TransitionError('conflict', 'No admissible slope-sum parameter')
        if len(candidates)>1:
            return Proposal(candidates=candidates,operations=operations)
        assignments[parameter] = candidates[0]
    if truth(sp.Eq(residual.subs(assignments),0)) is not True:
        raise TransitionError('conflict','Slope sum not satisfied by parameter')
    reads = (fact.fact_id, named.fact_id, action.slope_sum_id, base.fact_id,
             fact.curve_equation_id, fact.line_equation_id, f'parameterization:{fact.line}',
             *(f'property:{fact.fact_id}:{n}' for n in names), *state.constraints.keys(),
             *(f'value:{v}' for v in state.values))
    return Proposal(values=assignments,candidates=candidates,read_facts=reads,operations=operations)
