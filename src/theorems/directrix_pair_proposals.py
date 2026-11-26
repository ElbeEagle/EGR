"""RM28 checks object-scoped sources and proposes two equations atomically."""
import sympy as sp
from dataclasses import replace
from src.solver.transition_primitives import TransitionError
from src.solver.directrix_pair_operations import directrix_pair
from src.solver.midpoint_operations import canonical_numeric_line
from src.state.directrix_pair_query import pair_keys, pair_snapshot


def check_directrix_binding(state, action):
    from .equal_axis_proposals import check_equal_axis_binding
    if action.mode != 'derive_directrix_pair':
        raise TransitionError('inapplicable', 'Unsupported RM28 mode')
    return check_equal_axis_binding(state, replace(action, mode='derive_equal_axis_eccentricity'))


def derive_directrix_pair(state, action):
    from .bound_application import Proposal, bound_parameters, bound_axis
    from src.state.transition_state import EquationFact
    fact = check_directrix_binding(state, action)
    aa, bb = bound_parameters(state, action.curve, action.equation_id)
    axis = bound_axis(state, action.curve, action.equation_id)
    reads = (fact.fact_id, f'frame:{action.curve}', *(f'property:{action.curve}:{p}' for p in ('a_sq', 'b_sq', 'c_sq')))
    if any(fact.fact_id not in state.provenance.get(k, ()) for k in reads[1:]):
        raise TransitionError('inapplicable', 'Matching parameter and frame sources required')
    cc = state.properties.get((action.curve, 'c_sq'))
    if cc is None:
        raise TransitionError('inapplicable', 'Committed c_sq required')
    lines = directrix_pair(state.symbols['x'], state.symbols['y'],
                          *(v.subs(state.values) for v in (aa, bb, cc)), axis)
    keys = pair_keys(action.curve)
    if any(f.owner == action.curve and f.role == 'directrix' and k not in keys for k, f in state.equations.items()):
        raise TransitionError('inapplicable', 'Ambiguous existing directrix identity')
    equations = {}
    for key, line in zip(keys, lines):
        old = state.equations.get(key)
        if old is not None:
            if (old.owner != action.curve or old.role != 'directrix' or old.fact_id != key
                    or sp.simplify(canonical_numeric_line(old.expression, state.symbols['x'], state.symbols['y'])-line) != 0):
                raise TransitionError('conflict', 'Existing directrix contradicts parameters')
            if old.source != pair_snapshot(state, action.curve, old.expression) or fact.fact_id not in state.provenance.get(key, ()):
                raise TransitionError('inapplicable', 'Existing directrix has stale or missing sources')
            equations[key] = old  # Preserve an equivalent scaled line and its sources.
        else:
            equations[key] = EquationFact(key, action.curve, 'directrix', line, pair_snapshot(state, action.curve, line))
    return Proposal(equations=equations, read_facts=reads,
                    operations=[{'operation': 'directrix_pair', 'axis': axis, 'equations': lines}])
