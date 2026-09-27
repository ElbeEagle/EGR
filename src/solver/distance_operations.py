"""Exact point-to-line distance; independent of curve and theorem selection."""
import sympy as sp
from .transition_primitives import TransitionError


def point_to_line_distance(expression, x, y, xy):
    try:
        poly = sp.Poly(expression, x, y)
    except sp.PolynomialError as exc:
        raise TransitionError('inapplicable', 'Expected a linear equation') from exc
    if poly.total_degree() > 1:
        raise TransitionError('inapplicable', 'Expected a linear equation')
    a, b, c = (poly.coeff_monomial(term) for term in (x, y, 1))
    numbers = tuple(map(sp.sympify, (*xy, a, b, c)))
    if len(xy) != 2:
        raise TransitionError('inapplicable', 'Expected two coordinates')
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in numbers):
        raise TransitionError('undetermined', 'Distance requires finite real coordinates and coefficients')
    norm_sq = sp.simplify(a*a+b*b)
    if norm_sq == 0:
        raise TransitionError('inapplicable', 'Degenerate line equation')
    return sp.simplify(sp.Abs(a*numbers[0]+b*numbers[1]+c)/sp.sqrt(norm_sq))
