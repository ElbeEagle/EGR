from src.entropy.metrics import (
    nonincreasing_adjacent_rate,
    pearson_correlation,
    spearman_correlation,
)
from src.entropy.schema import SCHEMA_VERSION, make_entropy_label
from src.state.abstract_state import AbstractState


def test_entropy_label_schema_remaining_step_targets():
    state = AbstractState(completeness_score=0.25, reasoning_depth=1)
    state.has_equation = True

    label = make_entropy_label(
        sample_index=0,
        problem_id=123,
        trajectory_id='model:0:model',
        path_type='model',
        step=1,
        sequence_length=4,
        abstract_state=state,
        transition_status='success',
        path_executable=True,
        solvable_on_path=False,
        next_model_id=21,
    )

    assert label['schema_version'] == SCHEMA_VERSION
    assert label['remaining_steps'] == 3
    assert label['normalized_remaining_steps'] == 0.75
    assert label['progress'] == 0.25
    assert len(label['state_vector']) == 28
    assert label['state_features']['curve_type'] == 'unknown'
    assert label['completeness_score'] == 0.25
    assert 0.0 <= label['heuristic_entropy'] <= 1.0


def test_entropy_metrics_handle_monotonic_and_ranked_values():
    decreasing = [1.0, 0.7, 0.7, 0.2]
    increasing = [0.2, 0.7, 0.7, 1.0]

    assert nonincreasing_adjacent_rate(decreasing) == 1.0
    assert nonincreasing_adjacent_rate(increasing) < 1.0
    assert pearson_correlation(decreasing, decreasing) == 1.0
    assert spearman_correlation(decreasing, decreasing) == 1.0
