"""Finite positive standard-parameter latus lengths, without state mutation."""
import sympy as sp
from .transition_primitives import TransitionError

def latus_length(model_id,first,second=None):
    values=(first,) if model_id==20 else (first,second)
    if any(v is None or v.free_symbols or v.is_finite is not True or v.is_positive is not True for v in values):
        raise TransitionError('undetermined','Positive finite numeric parameters required')
    return sp.simplify(2*first if model_id==20 else 2*second/sp.sqrt(first))
