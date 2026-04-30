"""
Run the entropy dataset, training, and report pipeline.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.entropy.dataset import EntropyDatasetBuilder, read_jsonl, summarize_entries, write_jsonl
from src.entropy.linear_model import train_linear_entropy_model
from src.entropy.metrics import mae, pearson_correlation, rmse, spearman_correlation
from src.entropy.reporting import (
    attach_learned_predictions,
    build_correlation_summary,
    build_trajectory_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/train_with_models_v2.json')
    parser.add_argument('--output-dir', default='outputs/entropy')
    parser.add_argument('--max-samples', type=int, default=None)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--random-paths-per-sample', type=int, default=1)
    parser.add_argument('--sample-timeout-seconds', type=float, default=1.0)
    parser.add_argument('--l2', type=float, default=1e-3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = PROJECT_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    builder = EntropyDatasetBuilder(
        seed=args.seed,
        sample_timeout_seconds=args.sample_timeout_seconds,
    )
    entries = builder.build_from_file(
        str(PROJECT_ROOT / args.input),
        limit=args.max_samples,
        include_random=True,
        random_paths_per_sample=args.random_paths_per_sample,
    )
    dataset_path = output_dir / 'entropy_dataset.jsonl'
    summary_path = output_dir / 'entropy_dataset_summary.json'
    write_jsonl(str(dataset_path), entries)

    summary = summarize_entries(entries)
    summary.update({
        'input': args.input,
        'max_samples': args.max_samples,
        'seed': args.seed,
        'random_paths_per_sample': args.random_paths_per_sample,
        'sample_timeout_seconds': args.sample_timeout_seconds,
        'skipped_path_count': len(builder.skipped_paths),
        'skipped_paths': builder.skipped_paths[:100],
    })
    with summary_path.open('w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

    training_entries = [entry for entry in entries if entry['path_type'] == 'model']
    vectors = [entry['state_vector'] for entry in training_entries]
    targets = [float(entry['normalized_remaining_steps']) for entry in training_entries]
    heuristic = [float(entry['heuristic_entropy']) for entry in training_entries]
    model = train_linear_entropy_model(vectors, targets, l2=args.l2, seed=args.seed)
    model.update({
        'source_dataset': str(dataset_path.relative_to(PROJECT_ROOT)),
        'training_path_types': ['model'],
        'only_executable': False,
    })

    model_path = output_dir / 'learned_entropy_estimator.json'
    metrics_path = output_dir / 'training_metrics.json'
    with model_path.open('w', encoding='utf-8') as f:
        json.dump(model, f, ensure_ascii=False, indent=2, sort_keys=True)

    metrics = {
        'target': 'normalized_remaining_steps',
        'selected_entry_count': len(training_entries),
        'heuristic_baseline': {
            'mae': round(float(mae(targets, heuristic)), 8),
            'rmse': round(float(rmse(targets, heuristic)), 8),
            'pearson': round(float(pearson_correlation(targets, heuristic)), 8),
            'spearman': round(float(spearman_correlation(targets, heuristic)), 8),
        },
        'learned_linear': model['metrics'],
        'sample_counts': model['sample_counts'],
    }
    with metrics_path.open('w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2, sort_keys=True)

    enriched_entries = attach_learned_predictions(read_jsonl(str(dataset_path)), model)
    trajectory_report = build_trajectory_report(enriched_entries)
    correlation_summary = build_correlation_summary(enriched_entries)

    trajectory_path = output_dir / 'trajectory_report.json'
    correlation_path = output_dir / 'correlation_summary.json'
    with trajectory_path.open('w', encoding='utf-8') as f:
        json.dump(trajectory_report, f, ensure_ascii=False, indent=2, sort_keys=True)
    with correlation_path.open('w', encoding='utf-8') as f:
        json.dump(correlation_summary, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"Wrote {dataset_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {model_path}")
    print(f"Wrote {metrics_path}")
    print(f"Wrote {trajectory_path}")
    print(f"Wrote {correlation_path}")
    print(f"Entries: {summary['entry_count']}, trajectories: {summary['trajectory_count']}")
    print(f"Skipped paths: {summary['skipped_path_count']}")
    print(f"Validation MAE: {model['metrics']['validation']['mae']:.6f}")


if __name__ == '__main__':
    main()
