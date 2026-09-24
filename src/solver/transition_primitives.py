"""Small exact operations for bound transitions; no unrestricted expression eval."""
from __future__ import annotations

import ast
import math
from typing import Mapping, Sequence

import sympy as sp


class TransitionError(ValueError):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


def parse_expression(text: str, symbols: Mapping[str, sp.Symbol]):
    """Parse arithmetic only, retaining denominator guards before simplification."""
    if len(text) > 1000:
        raise ValueError("Expression exceeds slice limit")
    tree = ast.parse(text.strip().replace('^', '**'), mode='eval')
    if len(list(ast.walk(tree))) > 150:
        raise ValueError("Expression exceeds slice limit")
    guards = []

    def visit(node):
        if isinstance(node, ast.Name) and node.id in symbols:
            return symbols[node.id]
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if isinstance(node.value, float) and not math.isfinite(node.value):
                raise ValueError("Non-finite numeric literal")
            return sp.Rational(str(node.value))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                guards.append(sp.Ne(right, 0))
                return left / right
            if isinstance(node.op, ast.Pow) and right.is_Integer and abs(right) <= 16:
                if right < 0:
                    guards.append(sp.Ne(left, 0))
                return left ** right
        raise ValueError("Unsupported arithmetic syntax or undeclared symbol")

    result = visit(tree.body)
    if result.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        raise ValueError("Undefined arithmetic expression")
    return result, guards


def truth(condition, constraints: Sequence = ()):
    """True/False/None; only attempt a bounded univariate inequality check."""
    condition = sp.simplify(condition)
    if condition in (sp.true, sp.false):
        return bool(condition)
    if condition in constraints:
        return True
    symbols = condition.free_symbols | set().union(*(c.free_symbols for c in constraints))
    if len(symbols) != 1:
        return None
    try:
        if sp.reduce_inequalities([*constraints, sp.Not(condition)], list(symbols)) is sp.false:
            return True
        if sp.reduce_inequalities([*constraints, condition], list(symbols)) is sp.false:
            return False
    except (NotImplementedError, ValueError, TypeError):
        pass
    return None


def require(condition, constraints=(), message="Precondition not satisfied"):
    valid = truth(condition, constraints)
    if valid is not True:
        raise TransitionError('inapplicable' if valid is False else 'undetermined', message)


def hyperbola_parameters(expression, x, y, constraints):
    try:
        poly = sp.Poly(expression, x, y)
    except sp.PolynomialError as exc:
        raise TransitionError('inapplicable', 'Curve is not polynomial in x,y') from exc
    if set(poly.monoms()) != {(2, 0), (0, 2), (0, 0)}:
        raise TransitionError('inapplicable', 'Only centered axis-aligned standard hyperbolas supported')
    constant = poly.coeff_monomial(1)
    a_sq = sp.cancel(-constant / poly.coeff_monomial(x**2))
    b_sq = sp.cancel(constant / poly.coeff_monomial(y**2))
    require(a_sq > 0, constraints, 'Positive x-axis semi-axis square not established')
    require(b_sq > 0, constraints, 'Positive conjugate semi-axis square not established')
    return a_sq, b_sq


def line_slope(expression, x, y, constraints):
    try:
        poly = sp.Poly(expression, x, y)
    except sp.PolynomialError as exc:
        raise TransitionError('inapplicable', 'Not a polynomial line') from exc
    if poly.total_degree() != 1:
        raise TransitionError('inapplicable', 'Expected a line')
    require(sp.Eq(poly.coeff_monomial(1), 0), constraints, 'Asymptote must pass through origin')
    b = poly.coeff_monomial(y)
    require(sp.Ne(b, 0), constraints, 'Vertical line not supported by slope mode')
    return sp.cancel(-poly.coeff_monomial(x) / b)


def finite_real_solutions(expression, target, constraints, trace=None):
    if expression.free_symbols - {target}:
        raise TransitionError('undetermined', 'Other unresolved parameters remain')
    numerator, _ = sp.fraction(sp.cancel(expression))
    try:
        poly = sp.Poly(numerator, target)
    except sp.PolynomialError as exc:
        raise TransitionError('failed', 'Only polynomial parameter equations supported') from exc
    if poly.degree() > 2:
        raise TransitionError('failed', 'Slice supports parameter polynomials of degree <= 2')
    roots = sp.solveset(expression, target, domain=sp.S.Reals)
    if roots is sp.S.EmptySet:
        return ()
    if not isinstance(roots, sp.FiniteSet):
        raise TransitionError('undetermined', 'Parameter solution set is not finite')
    ordered_roots = tuple(sorted(roots, key=sp.default_sort_key))
    if trace is not None:
        trace.append({'operation': 'real_roots', 'roots': ordered_roots})
    accepted = []
    for root in ordered_roots:
        checks = [truth(c.subs(target, root)) for c in constraints]
        residual = expression.subs(target, root)
        checks.append(False if residual.has(sp.zoo, sp.nan) else truth(sp.Eq(residual, 0)))
        if trace is not None:
            trace.append({'operation': 'check_root', 'root': root,
                          'conditions': [c.subs(target, root) for c in constraints],
                          'residual': residual, 'checks': checks})
        if False in checks:
            continue
        if None in checks:
            raise TransitionError('undetermined', 'Candidate has unresolved conditions')
        accepted.append(root)
    return tuple(accepted)
