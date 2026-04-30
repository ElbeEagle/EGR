"""
Evaluation protocol helpers for EGR.
"""

from .protocol import (
    SCHEMA_VERSION,
    build_eval_report,
    build_sample_report,
    detect_curve_type,
    detect_query_type,
    summarize_samples,
    write_eval_artifacts,
)

__all__ = [
    "SCHEMA_VERSION",
    "build_eval_report",
    "build_sample_report",
    "detect_curve_type",
    "detect_query_type",
    "summarize_samples",
    "write_eval_artifacts",
]
