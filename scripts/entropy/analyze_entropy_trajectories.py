"""
Analyze entropy trajectories and correlations.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.entropy.dataset import read_jsonl
from src.entropy.reporting import (
    attach_learned_predictions,
    build_correlation_summary,
    build_trajectory_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset-jsonl', default='outputs/entropy/entropy_dataset.jsonl')
    parser.add_argument('--model', default='outputs/entropy/learned_entropy_estimator.json')
    parser.add_argument('--trajectory-output', default='outputs/entropy/trajectory_report.json')
    parser.add_argument('--correlation-output', default='outputs/entropy/correlation_summary.json')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = read_jsonl(str(PROJECT_ROOT / args.dataset_jsonl))

    model_path = PROJECT_ROOT / args.model
    if model_path.exists():
        with model_path.open('r', encoding='utf-8') as f:
            model = json.load(f)
        entries = attach_learned_predictions(entries, model)

    trajectory_report = build_trajectory_report(entries)
    correlation_summary = build_correlation_summary(entries)

    trajectory_path = PROJECT_ROOT / args.trajectory_output
    correlation_path = PROJECT_ROOT / args.correlation_output
    trajectory_path.parent.mkdir(parents=True, exist_ok=True)
    with trajectory_path.open('w', encoding='utf-8') as f:
        json.dump(trajectory_report, f, ensure_ascii=False, indent=2, sort_keys=True)
    with correlation_path.open('w', encoding='utf-8') as f:
        json.dump(correlation_summary, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"Wrote trajectory report: {trajectory_path}")
    print(f"Wrote correlation summary: {correlation_path}")
    print(f"Trajectories: {trajectory_report['trajectory_count']}")


if __name__ == '__main__':
    main()
