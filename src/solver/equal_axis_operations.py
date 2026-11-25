"""Finite numeric equal-axis qualification; no state mutation."""
import sympy as sp
from .transition_primitives import TransitionError

def equal_axis_eccentricity(a_sq,b_sq):
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (a_sq,b_sq)):
        raise TransitionError('undetermined','Finite numeric semiaxes required')
    if any(v.is_positive is not True for v in (a_sq,b_sq)):
        raise TransitionError('conflict','Positive squared semiaxes required')
    if sp.simplify(a_sq-b_sq)!=0:
        raise TransitionError('inapplicable','Hyperbola is not equal-axis')
    return sp.sqrt(2)
