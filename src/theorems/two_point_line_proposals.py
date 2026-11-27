"""RM73 scoped binding and single-line proposal."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.midpoint_operations import canonical_numeric_line
from src.solver.two_point_line_operations import two_point_line
from src.state.two_point_line_facts import point_pair_inputs, coordinate_snapshot, line_snapshot, fresh_two_point_line


def check_two_point_binding(state, action):
    if action.mode != 'derive_line_from_points' or any(v is not None for v in (
            action.curve, action.equation_id, action.line_equation_id, action.relation_id,
            action.peer_curve, action.peer_equation_id, action.point, action.coordinate_id,
            action.point_role, action.incidence_id, action.slope_sum_id)):
        raise TransitionError('inapplicable', 'Only a two-coordinate line binding is supported')
    points, reads = point_pair_inputs(state, action.line)
    if (action.coordinate_ids != tuple(p.fact_id for p in points)
            or action.coordinate_snapshot != coordinate_snapshot(state, action.line)):
        raise TransitionError('inapplicable', 'Stale coordinate binding')
    return points, reads


def derive_two_point_line(state, action):
    from .bound_application import Proposal
    from src.state.transition_state import EquationFact
    points, reads = check_two_point_binding(state, action)
    # No symbolic recovery or substitution is performed here.
    expression = two_point_line(state.symbols['x'], state.symbols['y'], *(p.xy for p in points))
    key = f'derived:{action.line}:two_points'
    existing = [f for f in state.equations.values() if f.owner == action.line and f.role == 'line']
    if len(existing) > 1:
        raise TransitionError('inapplicable', 'Ambiguous line equations')
    if existing:
        old = existing[0]
        if sp.simplify(canonical_numeric_line(old.expression, state.symbols['x'], state.symbols['y'])-expression) != 0:
            raise TransitionError('conflict', 'Existing line contradicts endpoints')
        if not state.provenance.get(old.fact_id):
            raise TransitionError('inapplicable', 'Existing line source required')
        if (old.fact_id == key or old.source.startswith('RM73:')) and not fresh_two_point_line(state, old):
            raise TransitionError('inapplicable', 'Stale two-point line result')
        return Proposal(read_facts=(*reads, old.fact_id), operations=[{'operation':'verify_existing_two_point_line'}])
    if key in state.equations:
        raise TransitionError('conflict', 'Two-point line identity occupied')
    fact = EquationFact(key, action.line, 'line', expression, line_snapshot(state, action.line, expression))
    return Proposal(equations={key:fact}, read_facts=reads,
                    operations=[{'operation':'two_point_line', 'endpoints':state.named_lines[action.line].endpoints,
                                 'equation':expression}])
