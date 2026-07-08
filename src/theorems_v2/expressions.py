"""Small conservative expression helpers used by theorem v2.

The helpers simplify exact rational arithmetic.  Symbolic expressions remain
as immutable ``Term`` objects and can later be delegated to a SymPy-backed
solver without changing theorem contracts.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from numbers import Integral, Rational, Real
from typing import Any, Optional

from .schema import Term


def number(value: Any) -> Any:
    if isinstance(value, bool):
        return value
    if isinstance(value, Fraction):
        return value
    if isinstance(value, Integral):
        return Fraction(int(value), 1)
    if isinstance(value, Rational):
        return Fraction(value.numerator, value.denominator)
    if isinstance(value, float):
        return Fraction(str(value))
    return value


def is_number(value: Any) -> bool:
    return isinstance(number(value), Fraction)


def is_zero(value: Any) -> bool:
    value = number(value)
    return isinstance(value, Fraction) and value == 0


def sign(value: Any) -> Optional[int]:
    value = number(value)
    if not isinstance(value, Fraction):
        return None
    return 1 if value > 0 else -1 if value < 0 else 0


def _sort_key(value: Any) -> str:
    return repr(value)


def add(*values: Any) -> Any:
    flat = []
    numeric = Fraction(0)
    for value in values:
        value = number(value)
        if isinstance(value, Term) and value.operator == "add":
            flat.extend(value.arguments)
        elif isinstance(value, Fraction):
            numeric += value
        else:
            flat.append(value)
    if numeric:
        flat.append(numeric)
    flat = [value for value in flat if not is_zero(value)]
    if not flat:
        return Fraction(0)
    if len(flat) == 1:
        return flat[0]
    return Term("add", tuple(sorted(flat, key=_sort_key)))


def mul(*values: Any) -> Any:
    flat = []
    numeric = Fraction(1)
    pending = list(values)
    while pending:
        value = number(pending.pop())
        if is_zero(value):
            return Fraction(0)
        if isinstance(value, Term) and value.operator == "mul":
            pending.extend(value.arguments)
        elif isinstance(value, Fraction):
            numeric *= value
        else:
            flat.append(value)
    if numeric != 1 or not flat:
        flat.append(numeric)
    flat = [value for value in flat if value != 1 or len(flat) == 1]
    if not flat:
        return Fraction(1)
    if len(flat) == 1:
        return flat[0]
    return Term("mul", tuple(sorted(flat, key=_sort_key)))

def neg(value: Any) -> Any:
    value = number(value)
    if isinstance(value, Term) and value.operator == "mul":
        return mul(-1, *value.arguments)
    return mul(-1, value)


def sub(left: Any, right: Any) -> Any:
    return add(left, neg(right))


def div(numerator: Any, denominator: Any) -> Any:
    numerator = number(numerator)
    denominator = number(denominator)
    if is_zero(denominator):
        raise ZeroDivisionError("symbolic division by zero")
    if isinstance(numerator, Fraction) and isinstance(denominator, Fraction):
        return numerator / denominator
    if isinstance(denominator, Fraction):
        return mul(Fraction(1, 1) / denominator, numerator)
    if denominator == 1:
        return numerator
    return Term("div", (numerator, denominator))


def square(value: Any) -> Any:
    value = number(value)
    if isinstance(value, Fraction):
        return value * value
    if isinstance(value, Term) and value.operator in {"sqrt", "sqrt_positive"}:
        return value.arguments[0]
    if isinstance(value, Term) and value.operator == "mul":
        return mul(*(square(factor) for factor in value.arguments))
    return Term("pow", (value, Fraction(2)))


def sqrt_positive(value: Any) -> Any:
    value = number(value)
    if isinstance(value, Fraction) and value >= 0:
        numerator_root = isqrt(value.numerator)
        denominator_root = isqrt(value.denominator)
        if (
            numerator_root * numerator_root == value.numerator
            and denominator_root * denominator_root == value.denominator
        ):
            return Fraction(numerator_root, denominator_root)
    return Term("sqrt_positive", (value,))


def equation(left: Any, right: Any) -> Term:
    return Term("eq", (number(left), number(right)))


class ConservativeSolver:
    """Exact structural solver with an extension point for richer algebra."""

    def equivalent(self, left: Any, right: Any) -> bool:
        return number(left) == number(right)

    def sign(self, value: Any) -> Optional[int]:
        return sign(value)

    def add(self, *values: Any) -> Any:
        return add(*values)

    def sub(self, left: Any, right: Any) -> Any:
        return sub(left, right)

    def mul(self, *values: Any) -> Any:
        return mul(*values)

    def div(self, numerator: Any, denominator: Any) -> Any:
        return div(numerator, denominator)

    def square(self, value: Any) -> Any:
        return square(value)

    def sqrt_positive(self, value: Any) -> Any:
        return sqrt_positive(value)
