"""
Label schema for state-entropy supervision.
"""

from typing import Any, Dict, Optional, Sequence

from src.reasoning.entropy_estimator import EntropyEstimator
from src.state.abstract_state import AbstractState


SCHEMA_VERSION = 'entropy-label-v1'
STATE_VECTOR_DIM = 28


def state_feature_summary(state: AbstractState) -> Dict[str, Any]:
    """Return compact, stable metadata for analysis reports."""
    info_flags = [
        state.has_equation,
        state.has_focus_info,
        state.has_vertex_info,
        state.has_point_on_curve,
        state.has_asymptote_info,
        state.has_directrix_info,
        state.has_tangent_info,
        state.has_distance_constraint,
        state.has_angle_constraint,
        state.has_perpendicular,
    ]
    return {
        'curve_type': state.curve_type.value,
        'query_type': state.query_type.value,
        'param_count': len(state.has_parameters),
        'info_feature_count': int(sum(bool(flag) for flag in info_flags)),
        'completeness_score': round(float(state.completeness_score), 6),
        'reasoning_depth': int(state.reasoning_depth),
    }


def make_entropy_label(
    *,
    sample_index: int,
    problem_id: Any,
    trajectory_id: str,
    path_type: str,
    step: int,
    sequence_length: int,
    abstract_state: AbstractState,
    transition_status: str,
    path_executable: bool,
    solvable_on_path: bool,
    next_model_id: Optional[int] = None,
    next_model_name: Optional[str] = None,
    applied_model_id: Optional[int] = None,
    answer_correct: Optional[bool] = None,
    random_seed: Optional[int] = None,
    state_vector: Optional[Sequence[float]] = None,
    estimator: Optional[EntropyEstimator] = None,
) -> Dict[str, Any]:
    """
    Create one entropy-label record for a state in a trajectory.

    Target convention:
    - normalized_remaining_steps is treated as normalized H(S) supervision.
    - progress is the complementary signal.
    - completeness_score is retained as a baseline feature, not as ground truth.
    """
    vector = list(state_vector if state_vector is not None else abstract_state.to_vector())
    if len(vector) != STATE_VECTOR_DIM:
        raise ValueError(f"Expected state vector dim {STATE_VECTOR_DIM}, got {len(vector)}")

    remaining_steps = max(sequence_length - step, 0)
    if sequence_length > 0:
        normalized_remaining_steps = remaining_steps / sequence_length
    else:
        normalized_remaining_steps = 0.0

    entropy_estimator = estimator or EntropyEstimator(mode='heuristic')
    heuristic_entropy = entropy_estimator.estimate(abstract_state)

    return {
        'schema_version': SCHEMA_VERSION,
        'sample_index': int(sample_index),
        'problem_id': problem_id,
        'trajectory_id': trajectory_id,
        'path_type': path_type,
        'random_seed': random_seed,
        'step': int(step),
        'sequence_length': int(sequence_length),
        'remaining_steps': int(remaining_steps),
        'normalized_remaining_steps': round(float(normalized_remaining_steps), 8),
        'progress': round(float(1.0 - normalized_remaining_steps), 8),
        'solvable_on_path': bool(solvable_on_path),
        'path_executable': bool(path_executable),
        'answer_correct': answer_correct,
        'next_model_id': next_model_id,
        'next_model_name': next_model_name,
        'applied_model_id': applied_model_id,
        'transition_status': transition_status,
        'completeness_score': round(float(abstract_state.completeness_score), 8),
        'heuristic_entropy': round(float(heuristic_entropy), 8),
        'state_hash': abstract_state.to_hash(),
        'state_features': state_feature_summary(abstract_state),
        'state_vector': [round(float(value), 8) for value in vector],
        'label_notes': {
            'normalized_remaining_steps': 'remaining_steps / sequence_length; primary learned H(S) target',
            'progress': '1 - normalized_remaining_steps',
            'solvable_on_path': 'true only for fully executable gold/correct paths',
            'completeness_score': 'heuristic baseline feature, not final entropy ground truth',
        },
    }
