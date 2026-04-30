import json
from pathlib import Path

import pytest

from src.reasoning.entropy_estimator import EntropyEstimator
from src.state.abstract_state import AbstractState


def test_heuristic_entropy_decreases_with_more_complete_state():
    estimator = EntropyEstimator(mode='heuristic')

    early = AbstractState(completeness_score=0.2, reasoning_depth=0)
    early.has_equation = True

    later = AbstractState(completeness_score=0.9, reasoning_depth=4)
    later.has_equation = True
    later.has_parameters = {'a', 'b', 'c'}
    later.has_focus_info = True

    assert 0.0 <= estimator.estimate(early) <= 1.0
    assert 0.0 <= estimator.estimate(later) <= 1.0
    assert estimator.estimate(later) < estimator.estimate(early)
    assert estimator.compute_info_gain(early, later) > 0


def test_learned_linear_entropy_from_weights():
    state = AbstractState(completeness_score=0.4, reasoning_depth=2)
    weights = [0.0] * 28
    weights[26] = 0.5
    weights[27] = 0.25

    estimator = EntropyEstimator(mode='learned', weights=weights, bias=0.1)
    expected = 0.1 + 0.5 * state.to_vector()[26] + 0.25 * state.to_vector()[27]

    assert estimator.estimate(state) == pytest.approx(expected)
    assert estimator.compare(state)['learned_entropy'] == pytest.approx(expected)


def test_learned_linear_model_file(tmp_path: Path):
    model_path = tmp_path / 'entropy_model.json'
    payload = {
        'model_type': 'linear_entropy_regressor',
        'weights': [0.01] * 28,
        'bias': 0.2,
    }
    model_path.write_text(json.dumps(payload), encoding='utf-8')

    estimator = EntropyEstimator.from_model_file(str(model_path))
    state = AbstractState(completeness_score=0.5)

    assert estimator.mode == 'learned'
    assert 0.0 <= estimator.estimate(state) <= 1.0


def test_learned_linear_rejects_wrong_vector_dim():
    estimator = EntropyEstimator(mode='learned', weights=[0.1] * 28)

    with pytest.raises(ValueError, match='dimension mismatch'):
        estimator.estimate_from_vector([0.0] * 27)
