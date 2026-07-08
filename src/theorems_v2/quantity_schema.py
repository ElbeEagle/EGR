"""Canonical scalar-quantity references for theorem state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class QuantityRef:
    kind: str
    subjects: Tuple[Any, ...]

    @classmethod
    def of(cls, kind: str, *subjects: Any) -> "QuantityRef":
        return cls(kind, tuple(subjects))
