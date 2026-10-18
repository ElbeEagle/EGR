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


def verify_ellipse_midpoint(dx, dy, xy):
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
    return rho


def midpoint_coordinate_sums(xy):
    """Return endpoint sums from a given midpoint, without solving endpoints."""
    return tuple(sp.simplify(2*v) for v in xy)


def ellipse_midpoint_chord(x, y, dx, dy, xy):
    rho = verify_ellipse_midpoint(dx, dy, xy)
    mx,my = xy
    nx,ny = mx/dx,my/dy
    line = canonical_numeric_line(nx*(x-mx)+ny*(y-my),x,y)
    return rho,(nx,ny),line


def ellipse_point_difference(x, y, dx, dy, sums):
    """Subtract endpoint equations: sx/dx * delta_x + sy/dy * delta_y = 0."""
    sx,sy = sums
    midpoint = (sx/2,sy/2)
    rho = verify_ellipse_midpoint(dx,dy,midpoint)
    coefficients = (sx/dx,sy/dy)
    # Half the difference coefficients matches the RM40 normal convention.
    normal = tuple(v/2 for v in coefficients)
    line = canonical_numeric_line(
        coefficients[0]*(x-midpoint[0])+coefficients[1]*(y-midpoint[1]),x,y)
    return rho,normal,line,coefficients


def verify_chord_endpoints(curve, line, x, y, midpoint, coordinates):
    """Check only supplied numeric endpoints; never construct a missing endpoint."""
    for xy in coordinates:
        if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in xy):
            raise TransitionError('undetermined','Numeric endpoint coordinates required')
        if any(sp.simplify(expr.subs({x:xy[0],y:xy[1]}))!=0 for expr in (curve,line)):
            raise TransitionError('conflict','Endpoint is not on both bound curve and line')
    if len(coordinates)==2:
        first,second = coordinates
        if all(sp.simplify(a-b)==0 for a,b in zip(first,second)):
            raise TransitionError('conflict','Chord endpoints must be distinct')
        if any(sp.simplify((a+b)/2-m)!=0 for a,b,m in zip(first,second,midpoint)):
            raise TransitionError('conflict','Endpoint midpoint contradicts given midpoint')
