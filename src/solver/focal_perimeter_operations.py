"""Finite perimeter calculation and supplied-coordinate checks, without state writes."""
import sympy as sp
from .transition_primitives import TransitionError

def focal_perimeter(a_sq,c_sq):
    if any(v.free_symbols or v.is_finite is not True or v.is_positive is not True for v in (a_sq,c_sq)):
        raise TransitionError('undetermined','Positive finite numeric parameters required')
    return sp.simplify(2*sp.sqrt(a_sq)+2*sp.sqrt(c_sq))


def verify_coordinates(curve,x,y,axis,c_sq,point_xy,focus_xy):
    supplied=([point_xy] if point_xy is not None else [])+list(focus_xy)
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for xy in supplied for v in xy):
        raise TransitionError('undetermined','Finite numeric supplied coordinates required')
    if point_xy is not None and sp.simplify(curve.subs(dict(zip((x,y),point_xy))))!=0:
        raise TransitionError('conflict','Point coordinates contradict ellipse incidence')
    c=sp.sqrt(c_sq);expected=((c,sp.S.Zero),(-c,sp.S.Zero)) if axis=='x' else ((sp.S.Zero,c),(sp.S.Zero,-c))
    for xy in focus_xy:
        if not any(all(sp.simplify(a-b)==0 for a,b in zip(xy,target)) for target in expected):
            raise TransitionError('conflict','Focus coordinates contradict ellipse')
    if len(focus_xy)==2 and all(sp.simplify(a-b)==0 for a,b in zip(*focus_xy)):
        raise TransitionError('conflict','Distinct focus labels cannot share coordinates')
