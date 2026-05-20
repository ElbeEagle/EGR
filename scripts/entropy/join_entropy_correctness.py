"""
Join entropy trajectories with end-to-end evaluation correctness.

This analysis is intentionally conservative: it only joins existing entropy
labels to evaluation samples when `problem_id == sample_id` matches, and it
keeps trajectory-level entropy evidence separate from final-answer correctness.
"""

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]


ENTROPY_METRICS = [
    'initial_heuristic_entropy',
    'final_heuristic_entropy',
    'mean_heuristic_entropy',
    'heuristic_entropy_delta',
    'heuristic_monotonicity_rate',
    'initial_learned_entropy',
    'final_learned_entropy',
    'mean_learned_entropy',
    'learned_entropy_delta',
    'learned_monotonicity_rate',
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entropy-jsonl', default='outputs/entropy/entropy_dataset.jsonl')
    parser.add_argument('--eval-jsonl', default='outputs/evaluation/main_integration_200/samples.jsonl')
    parser.add_argument('--learned-model', default='outputs/entropy/learned_entropy_estimator.json')
    parser.add_argument('--train-data', default='data/train_with_models_v2.json')
    parser.add_argument('--output-dir', default='outputs/entropy/round2_correctness_join')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entropy_path = PROJECT_ROOT / args.entropy_jsonl
    eval_path = PROJECT_ROOT / args.eval_jsonl
    model_path = PROJECT_ROOT / args.learned_model
    train_path = PROJECT_ROOT / args.train_data
    output_dir = PROJECT_ROOT / args.output_dir

    entropy_entries = read_jsonl(str(entropy_path))
    learned_available = False
    if model_path.exists():
        with model_path.open('r', encoding='utf-8') as f:
            learned_model = json.load(f)
        entropy_entries = attach_learned_predictions(entropy_entries, learned_model)
        learned_available = True

    eval_samples = read_jsonl(str(eval_path))
    train_samples = _load_train_samples(train_path)

    eval_by_id, duplicate_eval_ids = _index_eval_samples(eval_samples)
    entropy_problem_ids = {_stable_key(entry.get('problem_id')) for entry in entropy_entries}
    eval_ids = set(eval_by_id)
    overlap_ids = sorted(eval_ids & entropy_problem_ids, key=_sort_key)

    trajectory_rows = _joined_trajectory_rows(entropy_entries, eval_by_id)
    sample_model_rows = [row for row in trajectory_rows if row['path_type'] == 'model']

    key_reliability = _key_reliability_summary(
        entropy_entries=entropy_entries,
        eval_samples=eval_samples,
        train_samples=train_samples,
        entropy_problem_ids=entropy_problem_ids,
        eval_ids=eval_ids,
        overlap_ids=overlap_ids,
        duplicate_eval_ids=duplicate_eval_ids,
        joined_trajectory_rows=trajectory_rows,
    )

    summary = {
        'inputs': {
            'entropy_jsonl': args.entropy_jsonl,
            'eval_jsonl': args.eval_jsonl,
            'learned_model': args.learned_model if learned_available else None,
            'train_data': args.train_data if train_samples else None,
        },
        'join_key': {
            'used': 'entropy.problem_id == eval.sample_id',
            'rejected': 'entropy.sample_index is local to the filtered entropy slice and is not used',
            'reliability': key_reliability,
        },
        'eval_overall': _eval_outcome_summary(eval_samples),
        'joined_eval_subset': _eval_outcome_summary(
            [eval_by_id[sample_id] for sample_id in overlap_ids]
        ),
        'path_type_summary': _path_type_summary(trajectory_rows),
        'outcome_metric_correlations': _outcome_metric_correlations(trajectory_rows),
        'failure_reason_summary': _failure_reason_summary(trajectory_rows),
        'claim_boundary': _claim_boundary(key_reliability),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / 'correctness_join_summary.json', summary)
    _write_csv(output_dir / 'trajectory_join_rows.csv', trajectory_rows)
    _write_csv(output_dir / 'sample_model_rows.csv', sample_model_rows)
    _write_csv(output_dir / 'path_type_summary.csv', summary['path_type_summary'])
    _write_csv(
        output_dir / 'outcome_metric_correlations.csv',
        summary['outcome_metric_correlations'],
    )
    _write_csv(output_dir / 'failure_reason_summary.csv', summary['failure_reason_summary'])
    _write_markdown_report(output_dir / 'report.md', summary)

    print(f"Wrote correctness join summary: {output_dir / 'correctness_join_summary.json'}")
    print(f"Wrote trajectory rows: {output_dir / 'trajectory_join_rows.csv'}")
    print(f"Wrote report: {output_dir / 'report.md'}")
    print(
        "Joined eval samples: "
        f"{key_reliability['joined_eval_sample_count']}/"
        f"{key_reliability['eval_sample_count']}"
    )


def _stable_key(value: Any) -> Any:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return str(value)


def _sort_key(value: Any) -> Tuple[int, Any]:
    if isinstance(value, int):
        return (0, value)
    return (1, str(value))


def _load_train_samples(path: Path) -> Dict[Any, Dict[str, Any]]:
    if not path.exists():
        return {}
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return {_stable_key(item.get('id')): item for item in data}


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def group_entries_by_trajectory(
    entries: Sequence[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[str(entry['trajectory_id'])].append(entry)
    for trajectory_entries in grouped.values():
        trajectory_entries.sort(key=lambda item: int(item.get('step', 0)))
    return dict(grouped)


def attach_learned_predictions(
    entries: Sequence[Dict[str, Any]],
    learned_model: Dict[str, Any],
) -> List[Dict[str, Any]]:
    weights = [float(value) for value in learned_model['weights']]
    bias = float(learned_model.get('bias', 0.0))
    enriched = []
    for entry in entries:
        vector = [float(value) for value in entry['state_vector']]
        if len(vector) != len(weights):
            raise ValueError(f"Feature dimension mismatch: {len(vector)} vs {len(weights)}")
        prediction = sum(value * weight for value, weight in zip(vector, weights)) + bias
        updated = dict(entry)
        updated['learned_entropy'] = _round(max(0.0, min(1.0, prediction)))
        enriched.append(updated)
    return enriched


def _index_eval_samples(samples: Sequence[Dict[str, Any]]) -> Tuple[Dict[Any, Dict[str, Any]], List[Any]]:
    indexed: Dict[Any, Dict[str, Any]] = {}
    duplicates: List[Any] = []
    for sample in samples:
        key = _stable_key(sample.get('sample_id'))
        if key in indexed:
            duplicates.append(key)
        indexed[key] = sample
    return indexed, duplicates


def _joined_trajectory_rows(
    entries: Sequence[Dict[str, Any]],
    eval_by_id: Dict[Any, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for trajectory_id, trajectory_entries in group_entries_by_trajectory(entries).items():
        first = trajectory_entries[0]
        join_key = _stable_key(first.get('problem_id'))
        eval_sample = eval_by_id.get(join_key)
        if eval_sample is None:
            continue
        rows.append(_trajectory_row(trajectory_id, trajectory_entries, eval_sample))
    return sorted(rows, key=lambda row: (_sort_key(row['sample_id']), row['path_type'], row['trajectory_id']))


def _trajectory_row(
    trajectory_id: str,
    entries: Sequence[Dict[str, Any]],
    eval_sample: Dict[str, Any],
) -> Dict[str, Any]:
    first = entries[0]
    heuristic_values = [float(entry['heuristic_entropy']) for entry in entries]
    learned_values = (
        [float(entry['learned_entropy']) for entry in entries]
        if all('learned_entropy' in entry for entry in entries)
        else []
    )
    final_answer_correct = bool(eval_sample.get('final_answer_correct'))
    reasoning_success = bool(eval_sample.get('reasoning_success'))
    failure_bucket = _failure_bucket(eval_sample)

    row: Dict[str, Any] = {
        'sample_id': _stable_key(eval_sample.get('sample_id')),
        'trajectory_id': trajectory_id,
        'path_type': first.get('path_type'),
        'sequence_length': int(first.get('sequence_length', 0)),
        'entry_count': len(entries),
        'path_executable': bool(first.get('path_executable')),
        'solvable_on_path': bool(first.get('solvable_on_path')),
        'transition_statuses': '|'.join(str(entry.get('transition_status')) for entry in entries),
        'next_model_ids': '|'.join(
            str(entry.get('next_model_id'))
            for entry in entries
            if entry.get('next_model_id') is not None
        ),
        'eval_applied_model_sequence': '|'.join(
            str(model_id) for model_id in eval_sample.get('applied_model_sequence', [])
        ),
        'reasoning_success': reasoning_success,
        'final_answer_correct': final_answer_correct,
        'failure_reason': eval_sample.get('failure_reason'),
        'reasoning_failure_reason': eval_sample.get('reasoning_failure_reason'),
        'raw_failure_reason': eval_sample.get('raw_failure_reason'),
        'failure_bucket': failure_bucket,
        'curve_type': eval_sample.get('curve_type'),
        'query_type': eval_sample.get('query_type'),
        'num_eval_steps': int(eval_sample.get('num_steps') or 0),
        'initial_heuristic_entropy': _round(heuristic_values[0]),
        'final_heuristic_entropy': _round(heuristic_values[-1]),
        'mean_heuristic_entropy': _round(_mean(heuristic_values)),
        'heuristic_entropy_delta': _round(heuristic_values[0] - heuristic_values[-1]),
        'heuristic_monotonicity_rate': _round(nonincreasing_adjacent_rate(heuristic_values)),
    }
    if learned_values:
        row.update({
            'initial_learned_entropy': _round(learned_values[0]),
            'final_learned_entropy': _round(learned_values[-1]),
            'mean_learned_entropy': _round(_mean(learned_values)),
            'learned_entropy_delta': _round(learned_values[0] - learned_values[-1]),
            'learned_monotonicity_rate': _round(nonincreasing_adjacent_rate(learned_values)),
        })
    return row


def _failure_bucket(sample: Dict[str, Any]) -> str:
    if bool(sample.get('final_answer_correct')):
        return 'correct'
    return (
        sample.get('failure_reason')
        or sample.get('reasoning_failure_reason')
        or sample.get('raw_failure_reason')
        or 'unknown_incorrect'
    )


def _key_reliability_summary(
    *,
    entropy_entries: Sequence[Dict[str, Any]],
    eval_samples: Sequence[Dict[str, Any]],
    train_samples: Dict[Any, Dict[str, Any]],
    entropy_problem_ids: set,
    eval_ids: set,
    overlap_ids: Sequence[Any],
    duplicate_eval_ids: Sequence[Any],
    joined_trajectory_rows: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    entropy_trajectory_ids = {entry.get('trajectory_id') for entry in entropy_entries}
    joined_entry_count = sum(
        1 for entry in entropy_entries if _stable_key(entry.get('problem_id')) in set(overlap_ids)
    )
    train_checks = _train_key_checks(eval_samples, train_samples, set(overlap_ids))
    eval_sample_count = len(eval_samples)
    joined_eval_sample_count = len(overlap_ids)
    return {
        'status': (
            'stable_key_low_coverage'
            if joined_eval_sample_count < eval_sample_count
            else 'stable_key_full_coverage'
        ),
        'eval_sample_count': eval_sample_count,
        'eval_unique_sample_id_count': len(eval_ids),
        'duplicate_eval_sample_ids': [str(value) for value in duplicate_eval_ids],
        'entropy_entry_count': len(entropy_entries),
        'entropy_unique_problem_id_count': len(entropy_problem_ids),
        'entropy_trajectory_count': len(entropy_trajectory_ids),
        'joined_eval_sample_count': joined_eval_sample_count,
        'joined_eval_coverage_rate': _round(_safe_div(joined_eval_sample_count, eval_sample_count)),
        'joined_entropy_entry_count': joined_entry_count,
        'joined_trajectory_count': len(joined_trajectory_rows),
        'joined_eval_sample_ids': [str(value) for value in overlap_ids],
        'missing_eval_sample_count': len(eval_ids - set(overlap_ids)),
        'first_20_missing_eval_sample_ids': [
            str(value) for value in sorted(eval_ids - set(overlap_ids), key=_sort_key)[:20]
        ],
        'train_key_checks': train_checks,
        'interpretation': (
            'problem_id/sample_id is reliable for the matched samples, but the current '
            'entropy slice only covers a small subset of the 200 eval samples. Treat all '
            'correctness correlations as exploratory and underpowered.'
        ),
    }


def _train_key_checks(
    eval_samples: Sequence[Dict[str, Any]],
    train_samples: Dict[Any, Dict[str, Any]],
    joined_ids: set,
) -> Dict[str, Any]:
    if not train_samples:
        return {'available': False}

    eval_present = 0
    eval_exact_match = 0
    joined_present = 0
    joined_exact_match = 0
    mismatches: List[Dict[str, Any]] = []

    for sample in eval_samples:
        key = _stable_key(sample.get('sample_id'))
        train_sample = train_samples.get(key)
        if train_sample is None:
            continue
        eval_present += 1
        exact_match = (
            _normalize_text(sample.get('facts')) == _normalize_text(train_sample.get('fact_expressions'))
            and _normalize_text(sample.get('query')) == _normalize_text(train_sample.get('query_expressions'))
        )
        if exact_match:
            eval_exact_match += 1
        elif len(mismatches) < 10:
            mismatches.append({'sample_id': str(key), 'reason': 'facts_or_query_mismatch'})

        if key in joined_ids:
            joined_present += 1
            if exact_match:
                joined_exact_match += 1

    return {
        'available': True,
        'eval_ids_present_in_train': eval_present,
        'eval_facts_query_exact_matches': eval_exact_match,
        'joined_ids_present_in_train': joined_present,
        'joined_facts_query_exact_matches': joined_exact_match,
        'first_10_mismatches': mismatches,
    }


def _normalize_text(value: Any) -> str:
    return ' '.join(str(value or '').split())


def _eval_outcome_summary(samples: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(samples)
    final_correct = sum(1 for sample in samples if bool(sample.get('final_answer_correct')))
    reasoning_success = sum(1 for sample in samples if bool(sample.get('reasoning_success')))
    failures = Counter(_failure_bucket(sample) for sample in samples)
    return {
        'sample_count': total,
        'final_answer_correct_count': final_correct,
        'final_answer_accuracy': _round(_safe_div(final_correct, total)),
        'reasoning_success_count': reasoning_success,
        'reasoning_success_rate': _round(_safe_div(reasoning_success, total)),
        'failure_bucket_counts': dict(sorted(failures.items())),
    }


def _path_type_summary(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for path_type in sorted({row['path_type'] for row in rows}):
        bucket = [row for row in rows if row['path_type'] == path_type]
        result.append(_summary_for_rows(path_type, bucket))
    result.append(_summary_for_rows('all_joined_trajectories', list(rows)))
    return result


def _summary_for_rows(path_type: str, rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    sample_ids = {row['sample_id'] for row in rows}
    final_correct = sum(1 for row in rows if row['final_answer_correct'])
    reasoning_success = sum(1 for row in rows if row['reasoning_success'])
    executable = sum(1 for row in rows if row['path_executable'])
    summary: Dict[str, Any] = {
        'path_type': path_type,
        'trajectory_count': len(rows),
        'unique_eval_sample_count': len(sample_ids),
        'final_answer_correct_count': final_correct,
        'final_answer_accuracy': _round(_safe_div(final_correct, len(rows))),
        'reasoning_success_count': reasoning_success,
        'reasoning_success_rate': _round(_safe_div(reasoning_success, len(rows))),
        'path_executable_count': executable,
        'path_executable_rate': _round(_safe_div(executable, len(rows))),
    }
    for metric in ENTROPY_METRICS:
        values = _numeric_values(rows, metric)
        if values:
            summary[f'{metric}_mean'] = _round(_mean(values))
            summary[f'{metric}_median'] = _round(median(values))
    return summary


def _outcome_metric_correlations(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    path_types = sorted({row['path_type'] for row in rows}) + ['all_joined_trajectories']
    for path_type in path_types:
        path_rows = list(rows) if path_type == 'all_joined_trajectories' else [
            row for row in rows if row['path_type'] == path_type
        ]
        for outcome in ['final_answer_correct', 'reasoning_success']:
            labels = [1.0 if row[outcome] else 0.0 for row in path_rows]
            positive_count = int(sum(labels))
            negative_count = len(labels) - positive_count
            for metric in ENTROPY_METRICS:
                paired = [
                    (float(row[metric]), label)
                    for row, label in zip(path_rows, labels)
                    if metric in row and row[metric] != ''
                ]
                if len(paired) < 2:
                    continue
                values = [value for value, _label in paired]
                paired_labels = [label for _value, label in paired]
                positive_values = [
                    value for value, label in paired if label == 1.0
                ]
                negative_values = [
                    value for value, label in paired if label == 0.0
                ]
                output.append({
                    'path_type': path_type,
                    'outcome': outcome,
                    'metric': metric,
                    'n': len(paired),
                    'positive_count': positive_count,
                    'negative_count': negative_count,
                    'pearson': _round(pearson_correlation(values, paired_labels)),
                    'spearman': _round(spearman_correlation(values, paired_labels)),
                    'positive_mean': _round(_mean(positive_values)) if positive_values else '',
                    'negative_mean': _round(_mean(negative_values)) if negative_values else '',
                    'mean_diff_positive_minus_negative': (
                        _round(_mean(positive_values) - _mean(negative_values))
                        if positive_values and negative_values else ''
                    ),
                })
    return output


def _failure_reason_summary(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    path_types = sorted({row['path_type'] for row in rows}) + ['all_joined_trajectories']
    for path_type in path_types:
        path_rows = list(rows) if path_type == 'all_joined_trajectories' else [
            row for row in rows if row['path_type'] == path_type
        ]
        for failure_bucket in sorted({row['failure_bucket'] for row in path_rows}):
            bucket = [row for row in path_rows if row['failure_bucket'] == failure_bucket]
            row_out: Dict[str, Any] = {
                'path_type': path_type,
                'failure_bucket': failure_bucket,
                'trajectory_count': len(bucket),
                'unique_eval_sample_count': len({row['sample_id'] for row in bucket}),
                'final_answer_correct_count': sum(1 for row in bucket if row['final_answer_correct']),
                'reasoning_success_count': sum(1 for row in bucket if row['reasoning_success']),
                'path_executable_rate': _round(
                    _safe_div(sum(1 for row in bucket if row['path_executable']), len(bucket))
                ),
            }
            for metric in ENTROPY_METRICS:
                values = _numeric_values(bucket, metric)
                if values:
                    row_out[f'{metric}_mean'] = _round(_mean(values))
            output.append(row_out)
    return output


def _claim_boundary(key_reliability: Dict[str, Any]) -> Dict[str, List[str]]:
    coverage = key_reliability['joined_eval_coverage_rate']
    return {
        'can_claim_now': [
            (
                'A stable ID join is available for matched samples using '
                '`problem_id == sample_id`; train-data checks show these IDs map '
                'to the same facts/query for the joined subset.'
            ),
            (
                f'The current entropy slice covers {coverage:.3f} of the 200-sample '
                'end-to-end eval, so the join is useful as a diagnostic slice.'
            ),
            (
                'Heuristic and learned entropy can be reported side by side against '
                'reasoning_success, final_answer_correct, and failure buckets on this '
                'joined slice.'
            ),
        ],
        'cannot_claim_now': [
            (
                'Do not claim that remaining-step entropy predicts final answer '
                'correctness; the joined subset is small and final-correct positives '
                'are sparse.'
            ),
            (
                'Do not claim end-to-end solver improvement from entropy; the estimator '
                'was not integrated into the reasoning engine.'
            ),
            (
                'Do not interpret random/correct/model entropy trajectories as the '
                'actual solver trajectory unless the eval-applied sequence is separately '
                'reconstructed and validated.'
            ),
        ],
    }


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    with path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)


def _write_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_report(path: Path, summary: Dict[str, Any]) -> None:
    reliability = summary['join_key']['reliability']
    joined = summary['joined_eval_subset']
    overall = summary['eval_overall']
    path_rows = summary['path_type_summary']
    model_summary = next(row for row in path_rows if row['path_type'] == 'model')
    model_correlations = [
        row for row in summary['outcome_metric_correlations']
        if row['path_type'] == 'model'
        and row['metric'] in {
            'initial_heuristic_entropy',
            'heuristic_entropy_delta',
            'initial_learned_entropy',
            'learned_entropy_delta',
        }
    ]

    lines = [
        '# Round2 Entropy Correctness Join',
        '',
        '## Join Key Reliability',
        '',
        f"- Join key used: `{summary['join_key']['used']}`.",
        f"- Eval coverage: {reliability['joined_eval_sample_count']}/{reliability['eval_sample_count']} "
        f"({reliability['joined_eval_coverage_rate']:.4f}).",
        f"- Joined trajectory rows: {reliability['joined_trajectory_count']}.",
        f"- Entropy unique problem IDs: {reliability['entropy_unique_problem_id_count']}.",
        f"- Duplicate eval sample IDs: {len(reliability['duplicate_eval_sample_ids'])}.",
        f"- Train facts/query exact matches for joined IDs: "
        f"{reliability['train_key_checks'].get('joined_facts_query_exact_matches')}/"
        f"{reliability['train_key_checks'].get('joined_ids_present_in_train')}.",
        '',
        'Interpretation: the ID join is stable for matched samples, but coverage is low. '
        'Use this as a diagnostic slice, not as paper-level evidence that entropy predicts final correctness.',
        '',
        '## Eval Outcome Coverage',
        '',
        f"- Full eval: final-answer accuracy {overall['final_answer_correct_count']}/"
        f"{overall['sample_count']} ({overall['final_answer_accuracy']:.4f}); "
        f"reasoning success {overall['reasoning_success_count']}/"
        f"{overall['sample_count']} ({overall['reasoning_success_rate']:.4f}).",
        f"- Joined subset: final-answer accuracy {joined['final_answer_correct_count']}/"
        f"{joined['sample_count']} ({joined['final_answer_accuracy']:.4f}); "
        f"reasoning success {joined['reasoning_success_count']}/"
        f"{joined['sample_count']} ({joined['reasoning_success_rate']:.4f}).",
        f"- Joined failure buckets: `{json.dumps(joined['failure_bucket_counts'], sort_keys=True)}`.",
        '',
        '## Model-Path Entropy Slice',
        '',
        f"- Model-path trajectories: {model_summary['trajectory_count']} "
        f"over {model_summary['unique_eval_sample_count']} eval samples.",
        f"- Model-path executable rate: {model_summary['path_executable_count']}/"
        f"{model_summary['trajectory_count']} ({model_summary['path_executable_rate']:.4f}).",
        f"- Mean heuristic entropy delta: "
        f"{model_summary.get('heuristic_entropy_delta_mean', '')}.",
        f"- Mean learned entropy delta: "
        f"{model_summary.get('learned_entropy_delta_mean', '')}.",
        '',
        'Selected model-path correlations are below. Positive labels are `true` for the named outcome.',
        '',
        '| Outcome | Metric | n | Positive | Pearson | Spearman | Positive mean | Negative mean |',
        '|---|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for row in model_correlations:
        lines.append(
            f"| {row['outcome']} | {row['metric']} | {row['n']} | "
            f"{row['positive_count']} | {row['pearson']} | {row['spearman']} | "
            f"{row['positive_mean']} | {row['negative_mean']} |"
        )

    lines.extend([
        '',
        '## Claim Boundary',
        '',
        'Can claim now:',
    ])
    lines.extend(f"- {item}" for item in summary['claim_boundary']['can_claim_now'])
    lines.extend(['', 'Cannot claim now:'])
    lines.extend(f"- {item}" for item in summary['claim_boundary']['cannot_claim_now'])
    lines.append('')
    path.write_text('\n'.join(lines), encoding='utf-8')


def _numeric_values(rows: Sequence[Dict[str, Any]], key: str) -> List[float]:
    values: List[float] = []
    for row in rows:
        value = row.get(key)
        if value == '' or value is None:
            continue
        values.append(float(value))
    return values


def pearson_correlation(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys):
        raise ValueError("Length mismatch")
    if len(xs) < 2:
        return 0.0
    x_values = [float(value) for value in xs]
    y_values = [float(value) for value in ys]
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    x_var = sum((x - x_mean) ** 2 for x in x_values)
    y_var = sum((y - y_mean) ** 2 for y in y_values)
    denominator = math.sqrt(x_var * y_var)
    if denominator == 0:
        return 0.0
    return numerator / denominator


def spearman_correlation(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys):
        raise ValueError("Length mismatch")
    if len(xs) < 2:
        return 0.0
    return pearson_correlation(_rank(xs), _rank(ys))


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


def _mean(values: Iterable[float]) -> float:
    value_list = [float(value) for value in values]
    if not value_list:
        return 0.0
    return sum(value_list) / len(value_list)


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return float(numerator) / float(denominator)


def _round(value: float) -> float:
    return round(float(value), 8)


if __name__ == '__main__':
    main()
