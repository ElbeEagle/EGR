"""JSON-safe serialization for v2 states and trajectories."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction
from typing import Any


def serialize_value(value: Any) -> Any:
    if isinstance(value, Fraction):
        return {
            "__type__": "Fraction",
            "numerator": value.numerator,
            "denominator": value.denominator,
        }
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {
            "__type__": type(value).__name__,
            **{
                field.name: serialize_value(getattr(value, field.name))
                for field in fields(value)
            },
        }
    if isinstance(value, tuple):
        return [serialize_value(item) for item in value]
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {
            str(key): serialize_value(item)
            for key, item in value.items()
        }
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return {"__type__": type(value).__name__, "repr": repr(value)}


def serialize_state(state) -> dict:
    return {
        "symbols": [
            {"name": symbol.name, "type": symbol.type_name}
            for symbol in state.symbols.values()
        ],
        "facts": [
            {
                "fact_id": fact.fact_id,
                "predicate": fact.predicate,
                "arguments": serialize_value(fact.arguments),
                "value": serialize_value(fact.value),
                "provenance": serialize_value(fact.provenance),
            }
            for fact in state.facts.values()
        ],
    }
