"""Numeric centered-ellipse chord direction and affine line normalization."""
import sympy as sp
from .transition_primitives import TransitionError


def canonical_numeric_line(expression, x, y):
    try:
        poly = sp.Poly(expression, x, y)
    except sp.PolynomialError as exc:
        raise TransitionError('undetermined','Affine numeric line required') from exc
    if poly.total_degree()!=1:
        raise TransitionError('conflict','Nondegenerate affine line required')
    a,b,c = (poly.coeff_monomial(v) for v in (x,y,1))
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (a,b,c)):
        raise TransitionError('undetermined','Numeric line coefficients required')
    return sp.expand((a*x+b*y+c)/(a if a!=0 else b))


def ellipse_midpoint_chord(x, y, dx, dy, xy):
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (dx,dy,*xy)):
        raise TransitionError('undetermined','Finite numeric ellipse and midpoint required')
    if dx.is_positive is not True or dy.is_positive is not True:
        raise TransitionError('inapplicable','Positive ellipse denominators required')
    mx,my = xy
    rho = sp.simplify(mx**2/dx+my**2/dy)
    if rho == 0:
        raise TransitionError('undetermined','Center midpoint does not determine a unique diameter')
    if (1-rho).is_positive is not True:
        raise TransitionError('conflict','Midpoint must be strictly inside a nondegenerate chord')
    nx,ny = mx/dx,my/dy
    line = canonical_numeric_line(nx*(x-mx)+ny*(y-my),x,y)
    return rho,(nx,ny),line
