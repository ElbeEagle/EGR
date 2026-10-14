"""Direction-independent products for a given symbolic standard focal chord."""
from src.solver.parabola_operations import signed_parabola_parameter
from src.solver.transition_primitives import TransitionError
from .bound_application import Proposal
from .focal_chord_evidence import check_product_binding, given_focus_sources


def derive_symbolic_product(state, action):
    """Propose a type-derived nonzero condition and one product, without committing."""
    expected = {34: 'derive_symbolic_axial_product', 35: 'derive_symbolic_transverse_product'}
    if expected.get(action.model_id) != action.mode:
        raise TransitionError('inapplicable', 'Symbolic product mode/model mismatch')
    fact = check_product_binding(state, action)
    if fact.fact_id not in state.named_intersections:
        raise TransitionError('inapplicable', 'Given named intersection pair required')
    sources = given_focus_sources(state, fact.curve, fact.line)
    if not sources:
        raise TransitionError('inapplicable', 'Given focus incidence required')
    related_points = set(fact.points) | {a.point for a in state.focus_aliases.values() if a.curve == fact.curve}
    if (any(f.owner == fact.line for f in state.equations.values())
            or related_points.intersection(state.coordinates)):
        raise TransitionError('undetermined', 'Symbolic equation/coordinate cross-check is outside this mode')
    equation = state.equations[action.equation_id]
    if sum(f.owner == action.curve and f.role == 'curve' for f in state.equations.values()) != 1:
        raise TransitionError('undetermined', 'Unique curve equation required')
    expression = equation.expression.subs(state.values)
    axis, q, geometric_p, nonzero = signed_parabola_parameter(
        expression, state.symbols['x'], state.symbols['y'],
        [state.symbols[n] for n, kind in state.entities.items() if kind in ('Number', 'Real')],
        list(state.constraints.values()))
    condition_id = f'derived:{equation.fact_id}:parabola_nonzero'
    coordinate = axis if action.model_id == 34 else ('y' if axis == 'x' else 'x')
    value = q**2/4 if action.model_id == 34 else -q**2
    counts = [c for c in state.intersection_counts.values() if (c.line, c.curve) == (fact.line, fact.curve)]
    if any(c.count != 2 for c in counts):
        raise TransitionError('conflict', 'Named pair and intersection count disagree')
    return Proposal(
        properties={(fact.fact_id, coordinate+'_product'): value},
        constraints={condition_id: nonzero},
        read_facts=(f'entity:{fact.curve}', equation.fact_id, fact.fact_id, *sources,
                    *(c.fact_id for c in counts), *state.constraints,
                    *(f'value:{v}' for v in state.values)),
        operations=[{'operation': 'standard_signed_parameter', 'axis': axis,
                     'signed_q': q, 'positive_geometric_parameter': geometric_p},
                    {'operation': 'nondegenerate_parabola_type_condition',
                     'source': f'entity:{fact.curve}', 'condition': nonzero},
                    {'operation': 'given_focal_chord_product', 'intersection': fact.fact_id,
                     'coordinate': coordinate, 'value': value}])
