"""
Small metric helpers for entropy estimator analysis.
"""

import math
from typing import Iterable, List, Sequence


def _as_float_list(values: Iterable[float]) -> List[float]:
    return [float(value) for value in values]


def mae(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch")
    if not y_true:
        return 0.0
    return sum(abs(float(a) - float(b)) for a, b in zip(y_true, y_pred)) / len(y_true)


def rmse(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch")
    if not y_true:
        return 0.0
    mse = sum((float(a) - float(b)) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)
    return math.sqrt(mse)


def pearson_correlation(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys):
        raise ValueError("Length mismatch")
    if len(xs) < 2:
        return 0.0

    x_values = _as_float_list(xs)
    y_values = _as_float_list(ys)
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    x_var = sum((x - x_mean) ** 2 for x in x_values)
    y_var = sum((y - y_mean) ** 2 for y in y_values)
    denominator = math.sqrt(x_var * y_var)
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _rank(values: Sequence[float]) -> List[float]:
    indexed = sorted((float(value), index) for index, value in enumerate(values))
    ranks = [0.0] * len(indexed)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][0] == indexed[i][0]:
            j += 1
        average_rank = (i + j - 1) / 2.0 + 1.0
        for k in range(i, j):
            ranks[indexed[k][1]] = average_rank
        i = j
    return ranks


def spearman_correlation(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys):
        raise ValueError("Length mismatch")
    if len(xs) < 2:
        return 0.0
    return pearson_correlation(_rank(xs), _rank(ys))


def nonincreasing_adjacent_rate(values: Sequence[float], tolerance: float = 1e-8) -> float:
    if len(values) < 2:
        return 1.0
    comparisons = 0
    nonincreasing = 0
    for current_value, next_value in zip(values, values[1:]):
        comparisons += 1
        if float(next_value) <= float(current_value) + tolerance:
            nonincreasing += 1
    return nonincreasing / comparisons if comparisons else 1.0


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
