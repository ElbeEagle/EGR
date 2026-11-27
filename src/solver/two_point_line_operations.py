"""Numeric determinant line through two distinct points; no state mutation."""
import sympy as sp
from .transition_primitives import TransitionError
from .midpoint_operations import canonical_numeric_line


def two_point_line(x, y, first, second):
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (*first, *second)):
        raise TransitionError('undetermined', 'Finite real point coordinates required')
    dx, dy = (sp.simplify(b-a) for a, b in zip(first, second))
    if dx == 0 and dy == 0:
        raise TransitionError('inapplicable', 'Coincident points do not determine a line')
    return canonical_numeric_line(dy*(x-first[0])-dx*(y-first[1]), x, y)
