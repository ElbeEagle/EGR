"""Numeric common distance and existing asymptote consistency checks."""
import sympy as sp
from .transition_primitives import TransitionError
from .midpoint_operations import canonical_numeric_line

def focus_asymptote_distance(aa,bb):
    if any(v.free_symbols or v.is_finite is not True or v.is_positive is not True for v in (aa,bb)):
        raise TransitionError('undetermined','Positive finite numeric semiaxes required')
    return sp.sqrt(bb)

def verify_asymptote(expression,x,y,aa,bb,axis):
    slope=sp.sqrt(bb/aa if axis=='x' else aa/bb)
    line=canonical_numeric_line(expression,x,y)
    expected=[canonical_numeric_line(y-sign*slope*x,x,y) for sign in (-1,1)]
    if not any(sp.simplify(line-e)==0 for e in expected):
        raise TransitionError('conflict','Existing asymptote contradicts standard hyperbola')
