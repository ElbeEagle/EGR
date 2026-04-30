"""
Trajectory and correlation reports for H(S) estimators.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional, Sequence

from .dataset import group_entries_by_trajectory
from .linear_model import predict_linear_entropy
from .metrics import (
    mae,
    nonincreasing_adjacent_rate,
    pearson_correlation,
    rmse,
    spearman_correlation,
)


def attach_learned_predictions(
    entries: Sequence[Dict[str, Any]],
    learned_model: Dict[str, Any],
) -> List[Dict[str, Any]]:
    vectors = [entry['state_vector'] for entry in entries]
    predictions = predict_linear_entropy(learned_model, vectors)
    enriched = []
    for entry, prediction in zip(entries, predictions):
        updated = dict(entry)
        updated['learned_entropy'] = round(float(prediction), 8)
        enriched.append(updated)
    return enriched


def build_correlation_summary(entries: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    targets = [float(entry['normalized_remaining_steps']) for entry in entries]
    remaining_steps = [float(entry['remaining_steps']) for entry in entries]
    progress = [float(entry['progress']) for entry in entries]
    heuristic = [float(entry['heuristic_entropy']) for entry in entries]
    learned = [
        float(entry['learned_entropy'])
        for entry in entries
        if 'learned_entropy' in entry
    ]

    summary: Dict[str, Any] = {
        'entry_count': len(entries),
        'heuristic_entropy': _estimator_correlations(heuristic, targets, remaining_steps, progress),
        'answer_correctness': {
            'available': False,
            'note': 'answer_correct is not available in train_with_models_v2-derived entropy labels',
        },
    }

    if len(learned) == len(entries):
        summary['learned_entropy'] = _estimator_correlations(
            learned,
            targets,
            remaining_steps,
            progress,
        )
        summary['learned_vs_target_error'] = {
            'mae': round(float(mae(targets, learned)), 8),
            'rmse': round(float(rmse(targets, learned)), 8),
        }

    path_level = _path_level_correlations(entries)
    summary['path_success'] = path_level
    return summary


def build_trajectory_report(entries: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    grouped = group_entries_by_trajectory(entries)
    trajectory_rows = []
    path_type_buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for trajectory_id, trajectory_entries in grouped.items():
        path_type = trajectory_entries[0]['path_type']
        row = _trajectory_row(trajectory_id, trajectory_entries)
        trajectory_rows.append(row)
        path_type_buckets[path_type].append(row)

    by_path_type = {
        path_type: _aggregate_trajectory_rows(rows)
        for path_type, rows in sorted(path_type_buckets.items())
    }

    return {
        'trajectory_count': len(trajectory_rows),
        'by_path_type': by_path_type,
        'sample_trajectories': sorted(
            trajectory_rows,
            key=lambda item: (item['path_type'], item['trajectory_id']),
        )[:20],
    }


def _estimator_correlations(
    values: Sequence[float],
    targets: Sequence[float],
    remaining_steps: Sequence[float],
    progress: Sequence[float],
) -> Dict[str, float]:
    return {
        'vs_normalized_remaining_steps_pearson': round(
            float(pearson_correlation(values, targets)), 8
        ),
        'vs_normalized_remaining_steps_spearman': round(
            float(spearman_correlation(values, targets)), 8
        ),
        'vs_remaining_steps_pearson': round(float(pearson_correlation(values, remaining_steps)), 8),
        'vs_progress_pearson': round(float(pearson_correlation(values, progress)), 8),
    }


def _path_level_correlations(entries: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    grouped = group_entries_by_trajectory(entries)
    initial_heuristic = []
    final_heuristic = []
    executable = []
    initial_learned = []
    final_learned = []
    learned_available = True

    for trajectory_entries in grouped.values():
        first = trajectory_entries[0]
        last = trajectory_entries[-1]
        initial_heuristic.append(float(first['heuristic_entropy']))
        final_heuristic.append(float(last['heuristic_entropy']))
        executable.append(1.0 if first['path_executable'] else 0.0)
        if 'learned_entropy' in first and 'learned_entropy' in last:
            initial_learned.append(float(first['learned_entropy']))
            final_learned.append(float(last['learned_entropy']))
        else:
            learned_available = False

    result: Dict[str, Any] = {
        'trajectory_count': len(grouped),
        'executable_rate': round(sum(executable) / len(executable), 8) if executable else 0.0,
        'initial_heuristic_vs_executable_pearson': round(
            float(pearson_correlation(initial_heuristic, executable)), 8
        ) if len(executable) > 1 else 0.0,
        'final_heuristic_vs_executable_pearson': round(
            float(pearson_correlation(final_heuristic, executable)), 8
        ) if len(executable) > 1 else 0.0,
    }

    if learned_available and initial_learned:
        result['initial_learned_vs_executable_pearson'] = round(
            float(pearson_correlation(initial_learned, executable)), 8
        ) if len(executable) > 1 else 0.0
        result['final_learned_vs_executable_pearson'] = round(
            float(pearson_correlation(final_learned, executable)), 8
        ) if len(executable) > 1 else 0.0

    return result


def _trajectory_row(
    trajectory_id: str,
    trajectory_entries: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    heuristic_values = [float(entry['heuristic_entropy']) for entry in trajectory_entries]
    target_values = [float(entry['normalized_remaining_steps']) for entry in trajectory_entries]
    learned_values: Optional[List[float]] = None
    if all('learned_entropy' in entry for entry in trajectory_entries):
        learned_values = [float(entry['learned_entropy']) for entry in trajectory_entries]

    row: Dict[str, Any] = {
        'trajectory_id': trajectory_id,
        'path_type': trajectory_entries[0]['path_type'],
        'problem_id': trajectory_entries[0]['problem_id'],
        'sequence_length': trajectory_entries[0]['sequence_length'],
        'path_executable': trajectory_entries[0]['path_executable'],
        'solvable_on_path': trajectory_entries[0]['solvable_on_path'],
        'initial_heuristic_entropy': round(heuristic_values[0], 8),
        'final_heuristic_entropy': round(heuristic_values[-1], 8),
        'heuristic_entropy_delta': round(heuristic_values[0] - heuristic_values[-1], 8),
        'heuristic_monotonicity_rate': round(nonincreasing_adjacent_rate(heuristic_values), 8),
        'target_monotonicity_rate': round(nonincreasing_adjacent_rate(target_values), 8),
        'transition_statuses': [
            entry['transition_status']
            for entry in trajectory_entries
        ],
        'next_model_ids': [
            entry['next_model_id']
            for entry in trajectory_entries
            if entry['next_model_id'] is not None
        ],
    }

    if learned_values is not None:
        row.update({
            'initial_learned_entropy': round(learned_values[0], 8),
            'final_learned_entropy': round(learned_values[-1], 8),
            'learned_entropy_delta': round(learned_values[0] - learned_values[-1], 8),
            'learned_monotonicity_rate': round(nonincreasing_adjacent_rate(learned_values), 8),
        })

    return row


def _aggregate_trajectory_rows(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {}

    aggregate = {
        'trajectory_count': len(rows),
        'executable_rate': round(
            sum(1 for row in rows if row['path_executable']) / len(rows), 8
        ),
        'avg_initial_heuristic_entropy': _avg(row['initial_heuristic_entropy'] for row in rows),
        'avg_final_heuristic_entropy': _avg(row['final_heuristic_entropy'] for row in rows),
        'avg_heuristic_entropy_delta': _avg(row['heuristic_entropy_delta'] for row in rows),
        'avg_heuristic_monotonicity_rate': _avg(row['heuristic_monotonicity_rate'] for row in rows),
        'avg_target_monotonicity_rate': _avg(row['target_monotonicity_rate'] for row in rows),
    }

    if all('learned_entropy_delta' in row for row in rows):
        aggregate.update({
            'avg_initial_learned_entropy': _avg(row['initial_learned_entropy'] for row in rows),
            'avg_final_learned_entropy': _avg(row['final_learned_entropy'] for row in rows),
            'avg_learned_entropy_delta': _avg(row['learned_entropy_delta'] for row in rows),
            'avg_learned_monotonicity_rate': _avg(row['learned_monotonicity_rate'] for row in rows),
        })

    return aggregate


def _avg(values: Sequence[float]) -> float:
    value_list = [float(value) for value in values]
    return round(sum(value_list) / len(value_list), 8) if value_list else 0.0
