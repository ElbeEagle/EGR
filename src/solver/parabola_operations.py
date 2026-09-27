"""Exact standard-parabola and point-incidence operations; no theorem selection."""
import sympy as sp
from .transition_primitives import TransitionError, require

DIRECTIONS = {7: ('x', 1, 'right'), 8: ('x', -1, 'left'),
              9: ('y', 1, 'up'), 10: ('y', -1, 'down')}


def parabola_coefficient(expression, x, y, axis, constraints=()):
    longitudinal, transverse = (x, y) if axis == 'x' else (y, x)
    try:
        poly = sp.Poly(expression, transverse, longitudinal)
    except sp.PolynomialError as exc:
        raise TransitionError('inapplicable', 'Not a polynomial parabola') from exc
    if set(poly.monoms()) != {(2, 0), (0, 1)}:
        raise TransitionError('inapplicable', 'Only origin-vertex axis-aligned standard parabolas supported')
    require(sp.Ne(poly.coeff_monomial(transverse**2), 0), constraints,
            'Nonzero quadratic coefficient not established')
    return sp.cancel(-poly.coeff_monomial(longitudinal)/poly.coeff_monomial(transverse**2))


def substitute_point(expression, x, y, xy):
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in xy):
        raise TransitionError('undetermined', 'Point requires finite real numeric coordinates')
    return sp.simplify(expression.subs({x: xy[0], y: xy[1]}, simultaneous=True))


def parabola_geometry(coefficient, axis, sign, constraints):
    p = sp.simplify(sign*coefficient/2)
    require(p > 0, constraints, 'Opening direction or nondegeneracy not established')
    focus = (sign*p/2, sp.S.Zero) if axis == 'x' else (sp.S.Zero, sign*p/2)
    return p, focus
