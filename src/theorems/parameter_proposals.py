"""Shared proposal construction for intrinsic ellipse/hyperbola parameter relations."""
import sympy as sp

from src.solver.transition_primitives import (
    TransitionError, centered_denominators, finite_real_solutions, truth,
)
from src.state.transition_state import CurveFrame
from .bound_application import Proposal, check_binding


PARAMETER_MODES = ('derive_a_sq', 'derive_b_sq', 'derive_c_sq', 'constrain_parameters')


def parameter_proposal(state, action):
    fact = check_binding(state, action)
    curve = action.curve
    kind = state.entities[curve]
    keys = ('a_sq', 'b_sq', 'c_sq')
    known = {key: state.properties[curve, key].subs(state.values)
             for key in keys if (curve, key) in state.properties}
    reads = [f'entity:{curve}', *(f'property:{curve}:{key}' for key in known),
             *state.constraints.keys()]
    # An equation-bound action must consume the frame established by a standard
    # model; intrinsic object-only actions can also use other upstream facts.
    if fact is not None:
        if state.frames.get(curve) != CurveFrame(fact.fact_id):
            raise TransitionError('inapplicable', 'Missing matching standard-curve frame')
        x_sq, y_sq = centered_denominators(fact.expression, state.symbols['x'], state.symbols['y'])
        expected = {'a_sq': x_sq, 'b_sq': y_sq if kind == 'Ellipse' else -y_sq}
        for key in ('a_sq', 'b_sq'):
            if key in known and sp.simplify(known[key] - expected[key].subs(state.values)) != 0:
                raise TransitionError('conflict', 'Parameter does not match bound equation')
        reads.extend((fact.fact_id, f'frame:{curve}'))
    operations = []
    if action.mode == 'constrain_parameters':
        if len(known) != 3:
            raise TransitionError('inapplicable', 'Parameter constraint mode requires all three expressions')
        if not isinstance(state.query, sp.Symbol):
            raise TransitionError('inapplicable', 'Parameter solving requires a scalar query')
        a, b, c = (known[key] for key in keys)
        equation = sp.cancel(a-b-c if kind == 'Ellipse' else c-a-b)
        operations.append({'operation': 'parameter_constraint', 'curve': curve, 'expression': equation})
        conditions = [v > 0 for v in known.values()]
        constraints = [condition.subs(state.values) for condition in state.constraints.values()]
        if state.query in state.values or equation == 0:
            for condition in [*conditions, sp.Eq(equation, 0)]:
                valid = truth(condition, constraints)
                if valid is not True:
                    raise TransitionError('conflict' if valid is False else 'undetermined',
                                          'Parameter identity or positivity is not satisfied')
            return Proposal(read_facts=tuple(reads), operations=operations)
        candidates = finite_real_solutions(equation, state.query, [*constraints, *conditions], operations)
        if not candidates:
            raise TransitionError('conflict', 'No admissible parameter solution')
        return Proposal(values={state.query: candidates[0]} if len(candidates) == 1 else {},
                        candidates=candidates, read_facts=tuple(reads), operations=operations)
    target = action.mode.removeprefix('derive_')
    if target not in keys:
        raise TransitionError('inapplicable', 'Unsupported parameter relation mode')
    inputs = [key for key in keys if key != target]
    if any(key not in known for key in inputs):
        raise TransitionError('inapplicable', 'Two other squared parameters are required')
    if kind == 'Ellipse':
        value = {'a_sq': lambda: known['b_sq'] + known['c_sq'],
                 'b_sq': lambda: known['a_sq'] - known['c_sq'],
                 'c_sq': lambda: known['a_sq'] - known['b_sq']}[target]()
    else:
        value = {'a_sq': lambda: known['c_sq'] - known['b_sq'],
                 'b_sq': lambda: known['c_sq'] - known['a_sq'],
                 'c_sq': lambda: known['a_sq'] + known['b_sq']}[target]()
    value = sp.simplify(value)
    constraints = [c.subs(state.values) for c in state.constraints.values()]
    for item in [*(known[key] for key in inputs), value]:
        valid = truth(item > 0, constraints)
        if valid is not True:
            raise TransitionError('conflict' if valid is False else 'undetermined',
                                  'Nondegenerate conic parameters must be positive')
    if fact is not None and target in expected:
        equal = truth(sp.Eq(value, expected[target].subs(state.values)), constraints)
        if equal is not True:
            raise TransitionError('conflict' if equal is False else 'undetermined',
                                  'Derived parameter not established for bound equation')
    operations.append({'operation': 'parameter_relation', 'curve': curve, 'kind': kind,
                       'inputs': {k: known[k] for k in inputs}, 'target': target, 'result': value})
    return Proposal(properties={(curve, target): value}, read_facts=tuple(reads), operations=operations)
