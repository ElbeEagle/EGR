"""
Lightweight learned H(S) estimator.
"""

from typing import Any, Dict, List, Sequence, Tuple

import numpy as np

from .metrics import mae, pearson_correlation, rmse, spearman_correlation


def _to_matrix(vectors: Sequence[Sequence[float]]) -> np.ndarray:
    matrix = np.asarray(vectors, dtype=np.float64)
    if matrix.ndim != 2:
        raise ValueError(f"Expected 2D matrix, got shape {matrix.shape}")
    return matrix


def _to_vector(values: Sequence[float]) -> np.ndarray:
    vector = np.asarray(values, dtype=np.float64)
    if vector.ndim != 1:
        raise ValueError(f"Expected 1D target vector, got shape {vector.shape}")
    return vector


def predict_linear_entropy(
    model: Dict[str, Any],
    vectors: Sequence[Sequence[float]]
) -> List[float]:
    """Predict normalized entropy with a saved linear model payload."""
    weights = np.asarray(model['weights'], dtype=np.float64)
    bias = float(model.get('bias', 0.0))
    matrix = _to_matrix(vectors)
    if matrix.shape[1] != weights.shape[0]:
        raise ValueError(f"Feature dimension mismatch: {matrix.shape[1]} vs {weights.shape[0]}")
    predictions = matrix @ weights + bias
    return np.clip(predictions, 0.0, 1.0).astype(float).tolist()


def _fit_ridge(
    train_x: np.ndarray,
    train_y: np.ndarray,
    l2: float
) -> Tuple[np.ndarray, float]:
    design = np.concatenate([train_x, np.ones((train_x.shape[0], 1), dtype=np.float64)], axis=1)
    regularizer = np.eye(design.shape[1], dtype=np.float64) * float(l2)
    regularizer[-1, -1] = 0.0
    lhs = design.T @ design + regularizer
    rhs = design.T @ train_y
    try:
        params = np.linalg.solve(lhs, rhs)
    except np.linalg.LinAlgError:
        params = np.linalg.lstsq(lhs, rhs, rcond=None)[0]
    return params[:-1], float(params[-1])


def _evaluate(targets: Sequence[float], predictions: Sequence[float]) -> Dict[str, float]:
    return {
        'mae': round(float(mae(targets, predictions)), 8),
        'rmse': round(float(rmse(targets, predictions)), 8),
        'pearson': round(float(pearson_correlation(targets, predictions)), 8),
        'spearman': round(float(spearman_correlation(targets, predictions)), 8),
    }


def train_linear_entropy_model(
    vectors: Sequence[Sequence[float]],
    targets: Sequence[float],
    *,
    l2: float = 1e-3,
    train_ratio: float = 0.8,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Train a deterministic ridge regressor for normalized remaining-step entropy.
    """
    x = _to_matrix(vectors)
    y = _to_vector(targets)
    if x.shape[0] != y.shape[0]:
        raise ValueError(f"Length mismatch: {x.shape[0]} vs {y.shape[0]}")
    if x.shape[0] < 2:
        raise ValueError("Need at least two samples to train learned entropy estimator")

    rng = np.random.default_rng(seed)
    indices = np.arange(x.shape[0])
    rng.shuffle(indices)

    train_size = max(1, min(x.shape[0] - 1, int(round(x.shape[0] * train_ratio))))
    train_idx = indices[:train_size]
    val_idx = indices[train_size:]
    if val_idx.size == 0:
        val_idx = train_idx

    weights, bias = _fit_ridge(x[train_idx], y[train_idx], l2=l2)

    train_predictions = np.clip(x[train_idx] @ weights + bias, 0.0, 1.0).astype(float).tolist()
    val_predictions = np.clip(x[val_idx] @ weights + bias, 0.0, 1.0).astype(float).tolist()
    all_predictions = np.clip(x @ weights + bias, 0.0, 1.0).astype(float).tolist()

    return {
        'model_type': 'linear_entropy_regressor',
        'target': 'normalized_remaining_steps',
        'feature_dim': int(x.shape[1]),
        'l2': float(l2),
        'train_ratio': float(train_ratio),
        'seed': int(seed),
        'weights': [float(value) for value in weights.tolist()],
        'bias': float(bias),
        'metrics': {
            'train': _evaluate(y[train_idx].astype(float).tolist(), train_predictions),
            'validation': _evaluate(y[val_idx].astype(float).tolist(), val_predictions),
            'all': _evaluate(y.astype(float).tolist(), all_predictions),
        },
        'sample_counts': {
            'train': int(train_idx.size),
            'validation': int(val_idx.size),
            'all': int(x.shape[0]),
        },
    }
