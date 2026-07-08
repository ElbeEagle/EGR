"""Typed values for the third-stage algebra and analytic-geometry space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class Point2D:
    x: Any
    y: Any


@dataclass(frozen=True)
class LineEquation:
    """Normalized line equation a*x + b*y + c = 0."""

    a: Any
    b: Any
    c: Any


@dataclass(frozen=True)
class QuadraticPolynomial:
    """Univariate quadratic produced by a recorded substitution."""

    variable: str
    a: Any
    b: Any
    c: Any
    roots: Tuple[Any, ...] = ()


@dataclass(frozen=True)
class Vector2D:
    x: Any
    y: Any
