"""Exact line substitution; no root solving, point naming or state mutation."""
from dataclasses import dataclass
import sympy as sp
from .transition_primitives import TransitionError, truth
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


@dataclass(frozen=True)
class QuadraticRootStatus:
    discriminant: sp.Expr
    distinct_real_roots: int


def quadratic_coefficients(polynomial: sp.Expr, variable: sp.Symbol, parameters=()):
    """Validate a numeric quadratic without solving for its roots."""
    poly = sp.Poly(polynomial, variable)
    if poly.degree() != 2:
        raise TransitionError('inapplicable', 'A quadratic root pair is required')
    coefficients = tuple(poly.all_coeffs())
    if any(v.free_symbols - set(parameters) or v.is_real is not True or v.is_finite is not True for v in coefficients):
        raise TransitionError('undetermined', 'Finite real quadratic coefficients required')
    if coefficients[0].free_symbols or coefficients[0].is_zero is not False:
        raise TransitionError('undetermined', 'Nonzero numeric leading coefficient required')
    return coefficients


def quadratic_root_relation(polynomial: sp.Expr, variable: sp.Symbol, kind: str, parameters=()) -> sp.Expr:
    a, b, c = quadratic_coefficients(polynomial, variable, parameters)
    if kind not in ('sum', 'product'):
        raise TransitionError('inapplicable', 'Unknown root relation')
    return sp.cancel(-b/a if kind == 'sum' else c/a)


def classify_quadratic_roots(polynomial: sp.Expr, variable: sp.Symbol, parameters=(), constraints=()) -> QuadraticRootStatus:
    a, b, c = quadratic_coefficients(polynomial, variable, parameters)
    discriminant = sp.simplify(b*b-4*a*c)
    if truth(discriminant > 0, constraints) is True:
        count = 2
    elif discriminant.is_zero:
        count = 1
    elif discriminant.is_negative:
        count = 0
    else:
        raise TransitionError('undetermined', 'Real root count cannot be established')
    return QuadraticRootStatus(discriminant, count)


def chord_length_from_relations(root_sum: sp.Expr, root_product: sp.Expr,
                                xy: tuple[sp.Expr, sp.Expr], variable: sp.Symbol) -> sp.Expr:
    """Distance from an affine lift and supplied relations; does not apply Vieta."""
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True
           for v in (root_sum, root_product)):
        raise TransitionError('undetermined', 'Numeric root relations required')
    polys = [sp.Poly(v, variable) for v in xy]
    if len(polys) != 2 or any(p.degree() > 1 for p in polys):
        raise TransitionError('inapplicable', 'An affine coordinate lift is required')
    if any(c.free_symbols or c.is_real is not True or c.is_finite is not True
           for p in polys for c in p.all_coeffs()):
        raise TransitionError('undetermined', 'Numeric affine coefficients required')
    metric = sp.simplify(sum(p.nth(1)**2 for p in polys))
    gap = sp.simplify(root_sum**2-4*root_product)
    if metric.is_positive is not True or gap.is_positive is not True:
        raise TransitionError('inapplicable', 'Two distinct real points are required')
    return sp.sqrt(sp.simplify(metric*gap))


def parameterize_through_point(curve, x, y, xy, parameter):
    """Exclude the horizontal branch of an x-axis standard parabola pencil."""
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in xy):
        raise TransitionError('undetermined', 'Numeric through-point required')
    coefficient = parabola_coefficient(curve, x, y, 'x')
    if coefficient.free_symbols or coefficient.is_real is not True or coefficient.is_finite is not True:
        raise TransitionError('undetermined', 'Numeric standard parabola required')
    horizontal = sp.Poly(curve.subs(y, xy[1]), x)
    if horizontal.degree() != 1 or horizontal.LC().is_zero is not False:
        raise TransitionError('undetermined', 'Horizontal branch not excluded')
    lift = (sp.expand(parameter*(y-xy[1])+xy[0]), y)
    polynomial = sp.Poly(curve.subs(x, lift[0]), y).monic().as_expr()
    return LineSubstitution(y, lift, polynomial), horizontal.as_expr()
