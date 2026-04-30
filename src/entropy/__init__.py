"""
Entropy dataset, estimator training, and trajectory analysis utilities.
"""

from .dataset import EntropyDatasetBuilder, summarize_entries, write_jsonl
from .linear_model import train_linear_entropy_model, predict_linear_entropy
from .metrics import mae, pearson_correlation, rmse, spearman_correlation
from .schema import SCHEMA_VERSION, make_entropy_label

__all__ = [
    'EntropyDatasetBuilder',
    'SCHEMA_VERSION',
    'mae',
    'make_entropy_label',
    'pearson_correlation',
    'predict_linear_entropy',
    'rmse',
    'spearman_correlation',
    'summarize_entries',
    'train_linear_entropy_model',
    'write_jsonl',
]
