"""RM22 bounded common-distance proposal, without implicit RM12/21/52."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.focus_asymptote_operations import focus_asymptote_distance,verify_asymptote

def check_focus_asymptote_binding(state,a):
    f=state.equations.get(a.equation_id)
    equations=[e for e in state.equations.values() if e.owner==a.curve and e.role=='curve']
    if (a.mode!='derive_focus_asymptote_distance' or state.entities.get(a.curve)!='Hyperbola' or f is None or f.owner!=a.curve or f.role!='curve' or len(equations)!=1 or
        any(v is not None for v in (a.line,a.line_equation_id,a.relation_id,a.peer_curve,a.peer_equation_id,a.point,a.coordinate_id,a.point_role,a.incidence_id,a.slope_sum_id))):
        raise TransitionError('inapplicable','Unique hyperbola equation binding required')
    return f

def derive_focus_asymptote_distance(state,a):
    from .bound_application import Proposal,bound_parameters,bound_axis
    f=check_focus_asymptote_binding(state,a)
    aa,bb=bound_parameters(state,a.curve,a.equation_id);axis=bound_axis(state,a.curve,a.equation_id)
    reads=[a.equation_id,f'frame:{a.curve}',*(f'property:{a.curve}:{k}' for k in ('a_sq','b_sq'))]
    if any(not state.provenance.get(k) for k in reads[1:]):raise TransitionError('inapplicable','Standard parameter sources required')
    aa,bb=(v.subs(state.values) for v in (aa,bb));distance=focus_asymptote_distance(aa,bb)
    if (a.curve,'c_sq') in state.properties:
        if sp.simplify(state.properties[a.curve,'c_sq'].subs(state.values)-aa-bb)!=0:
            raise TransitionError('conflict','Existing focal parameter contradicts hyperbola')
        reads.append(f'property:{a.curve}:c_sq')
    for line in state.equations.values():
        if line.owner==a.curve and line.role=='asymptote':
            verify_asymptote(line.expression.subs(state.values),state.symbols['x'],state.symbols['y'],aa,bb,axis)
            reads.append(line.fact_id)
    return Proposal(properties={(a.curve,'focus_asymptote_distance'):distance},read_facts=tuple(reads),
        operations=[{'operation':'hyperbola_focus_asymptote_distance','axis':axis,'b_sq':bb,'distance':distance}])
