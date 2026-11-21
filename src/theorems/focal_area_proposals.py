"""RM30 eligibility and perimeter proposal; no implicit parameter recovery."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.focal_perimeter_operations import focal_perimeter,verify_coordinates
from src.state.focal_area_facts import area_owner

def check_area_binding(state,a):
    pair=state.focus_pairs.get(a.curve);eq=state.equations.get(a.equation_id);inc=state.incidences.get(a.incidence_id)
    if (a.mode!='derive_focal_area' or pair is None or pair.curve!=a.curve or not pair.sources or
        state.entities.get(a.curve)!='Ellipse' or any(state.entities.get(p)!='Point' for p in pair.points) or
        state.entities.get(a.point)!='Point' or a.point in pair.points or
        eq is None or eq.owner!=a.curve or eq.role!='curve' or inc is None or (inc.point,inc.curve)!=(a.point,a.curve) or
        a.relation_id!=area_owner(pair,a.point) or
        any(v is not None for v in (a.line,a.line_equation_id,a.peer_curve,a.peer_equation_id,a.coordinate_id,a.point_role,a.slope_sum_id))):
        raise TransitionError('inapplicable','Focal triangle binding mismatch')
    return pair,eq

def derive_focal_area(state,a):
    from .bound_application import Proposal,bound_parameters,bound_axis
    pair,eq=check_area_binding(state,a)
    aa,bb=bound_parameters(state,a.curve,a.equation_id);axis=bound_axis(state,a.curve,a.equation_id)
    keys=[f'property:{a.curve}:{k}' for k in ('a_sq','b_sq','c_sq')]
    if (a.curve,'c_sq') not in state.properties or any(not state.provenance.get(k) for k in keys):
        raise TransitionError('inapplicable','Committed parameters and sources required')
    cc=state.properties[a.curve,'c_sq'];aa,bb,cc=(v.subs(state.values) for v in (aa,bb,cc))
    if sp.simplify(cc-aa+bb)!=0:raise TransitionError('conflict','Focal parameter disagrees with ellipse')
    focal_perimeter(aa,cc)  # Reuse finite positive parameter qualification.
    angle=state.angle_facts.get((a.point,pair.points))
    if angle is None or not angle.sources or (angle.vertex,angle.endpoints)!=(a.point,pair.points):
        raise TransitionError('inapplicable','Matching focal angle and sources required')
    from src.solver.focal_area_operations import focal_area,verify_point_angle
    value,margin=focal_area(aa,bb,cc,angle.value)
    coords=state.coordinates;names=(a.point,*pair.points)
    verify_coordinates(eq.expression.subs(state.values),state.symbols['x'],state.symbols['y'],axis,cc,
                       coords[a.point].xy if a.point in coords else None,[coords[p].xy for p in pair.points if p in coords])
    if a.point in coords:verify_point_angle(coords[a.point].xy,axis,cc,angle.value)
    return Proposal(properties={(a.relation_id,'area'):value},
        read_facts=(a.equation_id,a.incidence_id,*pair.sources,*angle.sources,f'frame:{a.curve}',*keys,*(coords[p].fact_id for p in names if p in coords)),
        operations=[{'operation':'focal_triangle_area','a_sq':aa,'c_sq':cc,'theta':angle.value,'attainability_margin':margin,'area':value}])
