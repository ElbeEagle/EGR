#!/usr/bin/env python3
"""
Run the EGR unified evaluation protocol.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.reasoning.batch_test import init_engine, load_test_data
from src.evaluation import build_eval_report, build_sample_report, write_eval_artifacts
from src.reasoning.answer_comparator import compare_answers


def load_selector_report(path: Path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_samples(samples, verbose_progress: bool = True):
    engine = init_engine(verbose=False)
    sample_reports = []
    total = len(samples)

    for index, sample in enumerate(samples, start=1):
        result = None
        exception = None
        try:
            result = engine.solve(sample["fact_expressions"], sample["query_expressions"])
        except Exception as exc:
            exception = exc

        final_answer_correct = False
        if result is not None:
            final_answer_correct = compare_answers(
                getattr(result, "answer", None),
                sample.get("answer_expressions"),
            )

        sample_reports.append(
            build_sample_report(
                sample=sample,
                result=result,
                final_answer_correct=final_answer_correct,
                exception=exception,
            )
        )

        if verbose_progress and (index % 50 == 0 or index == total):
            success = sum(1 for item in sample_reports if item["reasoning_success"])
            correct = sum(1 for item in sample_reports if item["final_answer_correct"])
            print(f"progress {index}/{total}: reasoning_success={success}, correct={correct}")

    return sample_reports


def parse_args():
    parser = argparse.ArgumentParser(description="Run EGR unified evaluation protocol")
    parser.add_argument("--num", type=int, default=200, help="Number of samples")
    parser.add_argument("--seed", type=int, default=42, help="Sampling seed")
    parser.add_argument(
        "--data",
        default="data/train_with_models_v2.json",
        help="Reasoning dataset path",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/evaluation/protocol_200",
        help="Output directory for report.json, summary.json, samples.jsonl, summary.csv",
    )
    parser.add_argument(
        "--selector-report",
        default="outputs/selector/evaluation_results.json",
        help="Optional existing selector evaluation JSON to include in the summary",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress logs",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print("loading samples...")
    samples = load_test_data(path=args.data, num_samples=args.num, seed=args.seed)

    print("running protocol evaluation...")
    sample_reports = run_samples(samples, verbose_progress=not args.quiet)

    selector_report = load_selector_report(PROJECT_ROOT / args.selector_report)
    report = build_eval_report(
        sample_reports,
        run_metadata={
            "num_samples": args.num,
            "seed": args.seed,
            "data_path": args.data,
            "selector_report_path": args.selector_report if selector_report else None,
            "protocol_entrypoint": "scripts/evaluation/run_eval_protocol.py",
            "reasoning_entrypoint": "scripts/reasoning/batch_test.py:init_engine",
        },
        selector_report=selector_report,
    )

    paths = write_eval_artifacts(report, PROJECT_ROOT / args.output_dir)
    overall = report["summary"]["overall"]
    theorem = report["summary"]["theorem_selection"]

    print("\nprotocol summary")
    print(f"total_samples: {overall['total_samples']}")
    print(
        "reasoning_success: "
        f"{overall['reasoning_success_count']}/{overall['total_samples']} "
        f"= {overall['reasoning_success_rate']:.4f}"
    )
    print(
        "final_answer_correct: "
        f"{overall['final_answer_correct_count']}/{overall['total_samples']} "
        f"= {overall['final_answer_accuracy']:.4f}"
    )
    print(
        "answer_accuracy_among_successful_reasoning: "
        f"{overall['answer_accuracy_among_successful_reasoning']:.4f}"
    )
    print(
        "theorem_selection: "
        f"steps={theorem['labeled_steps']} "
        f"top1={theorem['top1_accuracy']:.4f} "
        f"top3={theorem['top3_accuracy']:.4f} "
        f"top5={theorem['top5_accuracy']:.4f}"
    )
    print("artifacts:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
