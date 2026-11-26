"""Finite centered-hyperbola directrices; no state mutation."""
import sympy as sp
from .transition_primitives import TransitionError


def directrix_pair(x, y, aa, bb, cc, axis):
    if axis not in ('x', 'y'):
        raise TransitionError('inapplicable', 'Centered axis required')
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (aa, bb, cc)):
        raise TransitionError('undetermined', 'Finite numeric parameters required')
    if any(v.is_positive is not True for v in (aa, bb, cc)) or sp.simplify(cc-aa-bb) != 0:
        raise TransitionError('conflict', 'Invalid hyperbola parameters')
    offset = sp.simplify(aa/sp.sqrt(cc))
    u = x if axis == 'x' else y
    return (u+offset, u-offset)
