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
