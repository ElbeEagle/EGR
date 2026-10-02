"""RM72: consistency of y=kx+b with a known point; no vertical-line mode."""
import sympy as sp
from src.solver.transition_primitives import TransitionError, require, truth, finite_real_solutions
from src.solver.parabola_operations import substitute_point
from .bound_application import Proposal, check_binding


def recover_line_from_point(state, action):
    fact = check_binding(state, action)
    if action.mode != 'recover_from_point':
        raise TransitionError('inapplicable', 'Unsupported RM72 mode')
    x, y = state.symbols['x'], state.symbols['y']
    expression = fact.expression.subs(state.values)
    try:
        poly = sp.Poly(expression, x, y)
    except sp.PolynomialError as exc:
        raise TransitionError('inapplicable', 'Expected polynomial line') from exc
    if poly.total_degree() != 1:
        raise TransitionError('inapplicable', 'Expected nondegenerate linear equation')
    a, b, c = (poly.coeff_monomial(v) for v in (x, y, 1))
    conditions = [v.subs(state.values) for v in state.constraints.values()]
    require(sp.Ne(b, 0), conditions, 'Nonzero y coefficient required; vertical lines unsupported')
    slope, intercept = sp.cancel(-a/b), sp.cancel(-c/b)
    xy = tuple(v.subs(state.values) for v in state.coordinates[action.point].xy)
    residual = substitute_point(expression, x, y, xy)
    operations = [{'operation': 'line_point_slope_consistency', 'slope': slope,
                   'intercept': intercept, 'point': action.point, 'residual': residual}]
    reads = (fact.fact_id, action.coordinate_id, action.relation_id,
             f'entity:{action.line}', *state.constraints.keys(), *(f'value:{v}' for v in state.values))
    unknowns = expression.free_symbols - {x, y}
    assignments, candidates = {}, ()
    if unknowns:
        if len(unknowns) != 1:
            raise TransitionError('undetermined', 'Line recovery supports one unknown parameter')
        target = next(iter(unknowns))
        # Keep unrelated pending constraints in state; coupled conditions must still resolve.
        relevant = [v for v in conditions if not v.free_symbols or target in v.free_symbols]
        candidates = finite_real_solutions(residual, target, relevant, operations)
        if not candidates:
            raise TransitionError('conflict', 'Point has no admissible line parameter')
        if len(candidates) > 1:
            return Proposal(read_facts=reads, operations=operations, candidates=candidates)
        assignments[target] = candidates[0]
    valid = truth(sp.Eq(residual.subs(assignments), 0))
    if valid is not True:
        raise TransitionError('conflict' if valid is False else 'undetermined', 'Line incidence not verified')
    require(sp.Ne(b.subs(assignments), 0), [v.subs(assignments) for v in conditions],
            'Recovered line has zero y coefficient')
    return Proposal(values=assignments, candidates=candidates, read_facts=reads, operations=operations,
                    properties={(action.line, 'slope'): slope.subs(assignments),
                                (action.line, 'intercept'): intercept.subs(assignments)})
