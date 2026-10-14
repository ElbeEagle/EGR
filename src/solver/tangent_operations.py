"""Numeric standard-ellipse tangent calculation; no state or model selection."""
import sympy as sp
from .transition_primitives import TransitionError


def ellipse_tangent(x, y, x_sq, y_sq, xy):
    """Verify a finite point on x²/x_sq+y²/y_sq=1 and return residual and line."""
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True
           for v in (x_sq, y_sq, *xy)):
        raise TransitionError('undetermined', 'Finite numeric ellipse and point required')
    if x_sq.is_positive is not True or y_sq.is_positive is not True:
        raise TransitionError('inapplicable', 'Positive ellipse denominators required')
    x0, y0 = xy
    residual = sp.simplify(x0**2/x_sq+y0**2/y_sq-1)
    if residual != 0:
        raise TransitionError('conflict', 'Tangent point not on bound ellipse')
    return residual, sp.expand(x0*x/x_sq+y0*y/y_sq-1)
