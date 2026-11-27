"""Finite numeric two-point distance, including coincident points."""
import sympy as sp
from .transition_primitives import TransitionError


def point_pair_distance(first, second):
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (*first,*second)):
        raise TransitionError('undetermined', 'Finite real coordinates required')
    delta = tuple(sp.simplify(b-a) for a,b in zip(first,second))
    squared = sp.simplify(sum(v*v for v in delta))
    return sp.sqrt(squared), delta, squared
