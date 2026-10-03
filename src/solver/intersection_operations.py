"""Exact line substitution; no root solving, point naming or state mutation."""
from dataclasses import dataclass
import sympy as sp
from .transition_primitives import TransitionError
from .parabola_operations import parabola_coefficient


@dataclass(frozen=True)
class LineSubstitution:
    variable: sp.Symbol
    xy: tuple[sp.Expr, sp.Expr]
    polynomial: sp.Expr


def substitute_line_in_parabola(curve, line, x, y) -> LineSubstitution:
    """Numeric standard parabola and affine line -> monic polynomial and lift map.

    Prefer x=m*y+n; for horizontal lines retain x instead. Degree one is
    preserved, never padded into a quadratic or interpreted as two points.
    """
    try:
        cp, lp = sp.Poly(curve, x, y), sp.Poly(line, x, y)
    except sp.PolynomialError as exc:
        raise TransitionError('inapplicable', 'Polynomial equations required') from exc
    if any(c.free_symbols or c.is_real is not True or c.is_finite is not True
           for c in (*cp.coeffs(), *lp.coeffs())):
        raise TransitionError('undetermined', 'Finite numeric coefficients required')
    axis = 'x' if set(cp.monoms()) == {(0, 2), (1, 0)} else 'y'
    parabola_coefficient(curve, x, y, axis)
    if lp.total_degree() != 1:
        raise TransitionError('inapplicable', 'Nondegenerate affine line required')
    a, b, c = lp.coeff_monomial(x), lp.coeff_monomial(y), lp.coeff_monomial(1)
    if a != 0:
        variable, xy = y, (sp.cancel(-(b*y+c)/a), y)
    else:
        variable, xy = x, (x, sp.cancel(-c/b))
    reduced = sp.Poly(sp.expand(curve.subs({x: xy[0], y: xy[1]}, simultaneous=True)), variable)
    if reduced.degree() not in (1, 2):
        raise TransitionError('inapplicable', 'Only linear or quadratic reductions supported')
    return LineSubstitution(variable, xy, reduced.monic().as_expr())
