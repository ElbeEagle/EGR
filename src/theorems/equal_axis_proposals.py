"""RM24 numeric equal-axis proposal, without implicit RM12/13."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.equal_axis_operations import equal_axis_eccentricity

def check_equal_axis_binding(state,a):
    f=state.equations.get(a.equation_id)
    equations=[e for e in state.equations.values() if e.owner==a.curve and e.role=='curve']
    if (a.mode!='derive_equal_axis_eccentricity' or state.entities.get(a.curve)!='Hyperbola' or f is None or f.owner!=a.curve or f.role!='curve' or len(equations)!=1 or
        any(v is not None for v in (a.line,a.line_equation_id,a.relation_id,a.peer_curve,a.peer_equation_id,a.point,a.coordinate_id,a.point_role,a.incidence_id,a.slope_sum_id))):
        raise TransitionError('inapplicable','Unique hyperbola equation binding required')
    return f

def derive_equal_axis_eccentricity(state,a):
    from .bound_application import Proposal,bound_parameters,bound_axis
    f=check_equal_axis_binding(state,a)
    aa,bb=bound_parameters(state,a.curve,a.equation_id);axis=bound_axis(state,a.curve,a.equation_id)
    reads=[a.equation_id,f'frame:{a.curve}',*(f'property:{a.curve}:{k}' for k in ('a_sq','b_sq'))]
    if any(not state.provenance.get(k) for k in reads[1:]):raise TransitionError('inapplicable','Standard parameter sources required')
    aa,bb=(v.subs(state.values) for v in (aa,bb));value=equal_axis_eccentricity(aa,bb)
    if (a.curve,'c_sq') in state.properties:
        if sp.simplify(state.properties[a.curve,'c_sq'].subs(state.values)-aa-bb)!=0:
            raise TransitionError('conflict','Existing focal parameter contradicts hyperbola')
        reads.append(f'property:{a.curve}:c_sq')
    return Proposal(properties={(a.curve,'eccentricity'):value},read_facts=tuple(reads),
        operations=[{'operation':'equal_axis_eccentricity','axis':axis,'a_sq':aa,'b_sq':bb,'equal_axis':True,'eccentricity':value}])
