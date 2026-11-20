"""Numeric named-root midpoint proposals; no endpoint construction."""
from dataclasses import dataclass, replace
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.intersection_operations import substitute_line_in_parabola, quadratic_root_relation, classify_quadratic_roots

@dataclass(frozen=True)
class MidpointCoordinateQuery:
    points: tuple[str, str]


def verify_numeric_association(state, fact):
    matches=[n for n in state.named_intersections.values() if (n.curve,n.line)==(fact.curve,fact.line)]
    if not matches or len({n.points for n in matches})!=1 or fact.named_points!=matches[0].points or fact.intersection_id not in {n.fact_id for n in matches}:
        raise TransitionError('conflict','Missing or ambiguous named-root identity')
    curve=state.equations[fact.curve_equation_id];line=state.equations[fact.line_equation_id]
    fresh=substitute_line_in_parabola(curve.expression.subs(state.values),line.expression.subs(state.values),state.symbols['x'],state.symbols['y'])
    if (fresh.variable,fresh.xy,fresh.polynomial)!=(fact.variable,fact.xy,fact.polynomial):
        raise TransitionError('conflict','Stale numeric reduction or non-affine lift')
    return tuple(n.fact_id for n in matches)


def derive_midpoint_from_roots(state, action):
    from .bound_application import check_binding, Proposal
    f=check_binding(state,replace(action,model_id=41))
    reads=verify_numeric_association(state,f)
    names=('root_sum','discriminant','distinct_real_roots')
    keys=[f'property:{f.fact_id}:{n}' for n in names]
    if any((f.fact_id,n) not in state.properties or f.fact_id not in state.provenance.get(k, ()) for n,k in zip(names,keys)):
        raise TransitionError('inapplicable','Committed root sum and qualification with sources required')
    total,delta,count=(state.properties[f.fact_id,n] for n in names)
    status=classify_quadratic_roots(f.polynomial,f.variable)
    if (total,delta,count)!=(quadratic_root_relation(f.polynomial,f.variable,'sum'),status.discriminant,status.distinct_real_roots):
        raise TransitionError('conflict','Root properties disagree with polynomial')
    if count!=2:
        raise TransitionError('inapplicable','Two distinct real endpoints required')
    xy=tuple(sp.simplify(v.subs(f.variable,total/2)) for v in f.xy)
    from src.solver.midpoint_operations import verify_chord_endpoints
    coords=[state.coordinates[p].xy for p in f.named_points if p in state.coordinates]
    verify_chord_endpoints(state.equations[f.curve_equation_id].expression,state.equations[f.line_equation_id].expression,state.symbols['x'],state.symbols['y'],xy,coords)
    return Proposal(properties={(f.fact_id,'midpoint_x'):xy[0],(f.fact_id,'midpoint_y'):xy[1]},
        read_facts=(f.fact_id,*reads,*keys,*(state.coordinates[p].fact_id for p in f.named_points if p in state.coordinates)),
        operations=[{'operation':'affine_root_midpoint','root_sum':total,'xy':xy}])


def read_midpoint(state,query):
    matches=[f for f in state.intersection_reductions.values() if f.named_points==query.points]
    if len(matches)!=1:return None
    f=matches[0]
    try:verify_numeric_association(state,f)
    except (TransitionError,KeyError):return None
    values=tuple(state.properties.get((f.fact_id,k)) for k in ('midpoint_x','midpoint_y'))
    return values if all(v is not None for v in values) else None
