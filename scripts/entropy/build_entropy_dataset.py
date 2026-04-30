"""
Build entropy-label dataset from train model sequences.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.entropy.dataset import EntropyDatasetBuilder, summarize_entries, write_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/train_with_models_v2.json')
    parser.add_argument('--output-jsonl', default='outputs/entropy/entropy_dataset.jsonl')
    parser.add_argument('--summary', default='outputs/entropy/entropy_dataset_summary.json')
    parser.add_argument('--max-samples', type=int, default=None)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--random-paths-per-sample', type=int, default=1)
    parser.add_argument('--sample-timeout-seconds', type=float, default=1.0)
    parser.add_argument('--no-random', action='store_true')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    builder = EntropyDatasetBuilder(
        seed=args.seed,
        sample_timeout_seconds=args.sample_timeout_seconds,
    )
    entries = builder.build_from_file(
        str(PROJECT_ROOT / args.input),
        limit=args.max_samples,
        include_random=not args.no_random,
        random_paths_per_sample=args.random_paths_per_sample,
    )

    output_jsonl = PROJECT_ROOT / args.output_jsonl
    summary_path = PROJECT_ROOT / args.summary
    write_jsonl(str(output_jsonl), entries)

    summary = summarize_entries(entries)
    summary['input'] = args.input
    summary['max_samples'] = args.max_samples
    summary['seed'] = args.seed
    summary['random_paths_per_sample'] = 0 if args.no_random else args.random_paths_per_sample
    summary['sample_timeout_seconds'] = args.sample_timeout_seconds
    summary['skipped_path_count'] = len(builder.skipped_paths)
    summary['skipped_paths'] = builder.skipped_paths[:100]
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open('w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"Wrote entropy dataset: {output_jsonl}")
    print(f"Wrote entropy summary: {summary_path}")
    print(f"Entries: {summary['entry_count']}, trajectories: {summary['trajectory_count']}")
    print(f"Skipped paths: {summary['skipped_path_count']}")


if __name__ == '__main__':
    main()
