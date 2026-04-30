"""
Train a lightweight learned H(S) estimator from entropy labels.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.entropy.dataset import read_jsonl
from src.entropy.linear_model import train_linear_entropy_model
from src.entropy.metrics import mae, pearson_correlation, rmse, spearman_correlation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset-jsonl', default='outputs/entropy/entropy_dataset.jsonl')
    parser.add_argument('--model-output', default='outputs/entropy/learned_entropy_estimator.json')
    parser.add_argument('--metrics-output', default='outputs/entropy/training_metrics.json')
    parser.add_argument('--path-type', action='append', default=['model'])
    parser.add_argument('--target', default='normalized_remaining_steps')
    parser.add_argument('--l2', type=float, default=1e-3)
    parser.add_argument('--train-ratio', type=float, default=0.8)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--only-executable', action='store_true')
    return parser.parse_args()


def select_training_entries(
    entries: List[Dict[str, Any]],
    path_types: List[str],
    *,
    only_executable: bool,
) -> List[Dict[str, Any]]:
    selected = [
        entry for entry in entries
        if entry['path_type'] in set(path_types)
    ]
    if only_executable:
        selected = [entry for entry in selected if entry['path_executable']]
    return selected


def main() -> None:
    args = parse_args()
    entries = read_jsonl(str(PROJECT_ROOT / args.dataset_jsonl))
    selected = select_training_entries(
        entries,
        args.path_type,
        only_executable=args.only_executable,
    )
    if not selected:
        raise SystemExit("No entropy entries selected for training")

    vectors = [entry['state_vector'] for entry in selected]
    targets = [float(entry[args.target]) for entry in selected]
    heuristic = [float(entry['heuristic_entropy']) for entry in selected]

    model = train_linear_entropy_model(
        vectors,
        targets,
        l2=args.l2,
        train_ratio=args.train_ratio,
        seed=args.seed,
    )
    model.update({
        'source_dataset': args.dataset_jsonl,
        'training_path_types': args.path_type,
        'only_executable': bool(args.only_executable),
    })

    heuristic_metrics = {
        'mae': round(float(mae(targets, heuristic)), 8),
        'rmse': round(float(rmse(targets, heuristic)), 8),
        'pearson': round(float(pearson_correlation(targets, heuristic)), 8),
        'spearman': round(float(spearman_correlation(targets, heuristic)), 8),
    }
    metrics = {
        'target': args.target,
        'selected_entry_count': len(selected),
        'heuristic_baseline': heuristic_metrics,
        'learned_linear': model['metrics'],
        'sample_counts': model['sample_counts'],
    }

    model_output = PROJECT_ROOT / args.model_output
    metrics_output = PROJECT_ROOT / args.metrics_output
    model_output.parent.mkdir(parents=True, exist_ok=True)
    with model_output.open('w', encoding='utf-8') as f:
        json.dump(model, f, ensure_ascii=False, indent=2, sort_keys=True)
    with metrics_output.open('w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"Wrote learned entropy model: {model_output}")
    print(f"Wrote training metrics: {metrics_output}")
    print(f"Selected entries: {len(selected)}")
    print(f"Validation MAE: {model['metrics']['validation']['mae']:.6f}")


if __name__ == '__main__':
    main()
