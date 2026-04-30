#!/usr/bin/env python3
"""
Run standalone search-strategy ablations for EGR.

The script reuses the unified evaluation protocol for per-strategy artifacts and
writes an additional paper-table friendly ablation_summary.{json,csv}.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import torch


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.reasoning.batch_test import load_test_data
from src.evaluation import build_eval_report, build_sample_report, write_eval_artifacts
from src.reasoning import ReasoningEngine
from src.reasoning.answer_comparator import compare_answers
from src.reasoning.search import (
    DEFAULT_LAMBDA_WEIGHTS,
    SEARCH_ABLATION_SCHEMA_VERSION,
    SearchSelectorAdapter,
    SearchStrategyConfig,
    default_ablation_strategies,
    normalize_strategy_name,
)
from src.selector import MaxEntropyClassifier
from src.state import StateConstructor
from src.theorems import TheoremLibrary


ABLATION_TABLE_SCHEMA_VERSION = "egr_search_ablation_table_v1"


def parse_lambda_weights(value: str) -> tuple[float, float, float]:
    parts = [part.strip() for part in value.split(",") if part.strip()]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("lambda weights must have exactly 3 comma-separated values")
    try:
        weights = tuple(float(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("lambda weights must be numeric") from exc
    return weights  # type: ignore[return-value]


def parse_strategies(value: str) -> List[str]:
    if value.strip().lower() == "all":
        return default_ablation_strategies()
    strategies: List[str] = []
    for item in value.split(","):
        if not item.strip():
            continue
        normalized = normalize_strategy_name(item)
        if normalized not in strategies:
            strategies.append(normalized)
    if not strategies:
        raise argparse.ArgumentTypeError("at least one strategy is required")
    return strategies


def load_neural_network(checkpoint_path: Path, device: str) -> MaxEntropyClassifier:
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"checkpoint not found: {checkpoint_path}")

    model = MaxEntropyClassifier()
    checkpoint = torch.load(checkpoint_path, map_location=device)
    state_dict = checkpoint.get("model_state_dict") if isinstance(checkpoint, Mapping) else checkpoint
    if state_dict is None:
        raise ValueError(f"checkpoint has no model_state_dict: {checkpoint_path}")
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


def strategy_needs_neural(strategy: str) -> bool:
    return strategy != "rule_only"


def build_engine(
    strategy: str,
    args: argparse.Namespace,
    neural_network: Optional[MaxEntropyClassifier],
) -> tuple[ReasoningEngine, SearchSelectorAdapter]:
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    selector = SearchSelectorAdapter(
        strategy=strategy,
        theorem_library=library,
        neural_network=neural_network if strategy_needs_neural(strategy) else None,
        state_constructor=constructor,
        device=args.device,
        top_k=args.top_k,
        lambda_weights=args.lambda_weights,
        avoid_repeated_models=not args.allow_repeated_models,
    )
    engine = ReasoningEngine(
        theorem_library=library,
        model_selector=selector,
        state_constructor=constructor,
        max_steps=args.max_steps,
        completeness_threshold=args.completeness_threshold,
        min_steps=args.min_steps,
        max_retries_per_step=args.max_retries_per_step,
        verbose=False,
    )
    return engine, selector


def run_strategy(
    strategy: str,
    samples: Sequence[Mapping[str, Any]],
    args: argparse.Namespace,
    neural_network: Optional[MaxEntropyClassifier],
) -> Dict[str, Any]:
    engine, selector = build_engine(strategy, args, neural_network)
    sample_reports: List[Dict[str, Any]] = []
    started_at = time.time()
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

        sample_report = build_sample_report(
            sample=sample,
            result=result,
            final_answer_correct=final_answer_correct,
            exception=exception,
        )
        sample_report["strategy"] = strategy
        sample_report["strategy_metadata"] = selector.metadata()
        sample_reports.append(sample_report)

        if not args.quiet and (index % args.progress_every == 0 or index == total):
            success = sum(1 for item in sample_reports if item["reasoning_success"])
            correct = sum(1 for item in sample_reports if item["final_answer_correct"])
            print(
                f"{strategy}: progress {index}/{total} "
                f"reasoning_success={success} final_correct={correct}"
            )

    elapsed_seconds = time.time() - started_at
    run_metadata = SearchStrategyConfig(
        name=strategy,
        top_k=args.top_k,
        lambda_weights=args.lambda_weights,
        avoid_repeated_models=not args.allow_repeated_models,
        checkpoint_path=args.checkpoint,
        max_steps=args.max_steps,
        seed=args.seed,
        sample_size=args.num,
    ).to_metadata()
    run_metadata.update(
        {
            "entrypoint": "scripts/experiments/run_search_ablation.py",
            "data_path": args.data,
            "device": args.device,
            "min_steps": args.min_steps,
            "completeness_threshold": args.completeness_threshold,
            "max_retries_per_step": args.max_retries_per_step,
            "elapsed_seconds": round(elapsed_seconds, 6),
            "selector_metadata": selector.metadata(),
        }
    )

    report = build_eval_report(sample_reports, run_metadata=run_metadata)
    augment_strategy_summary(report, sample_reports)

    strategy_dir = Path(args.output_dir) / strategy
    paths = write_eval_artifacts(report, PROJECT_ROOT / strategy_dir)
    row = build_ablation_row(strategy, report, args)
    return {
        "strategy": strategy,
        "report": report,
        "paths": paths,
        "row": row,
    }


def augment_strategy_summary(
    report: Dict[str, Any],
    sample_reports: Sequence[Mapping[str, Any]],
) -> None:
    summary = report.setdefault("summary", {})
    overall = summary.setdefault("overall", {})
    total = len(sample_reports)
    steps = [int(sample.get("num_steps") or 0) for sample in sample_reports]
    overall["avg_steps"] = sum(steps) / total if total else 0.0
    overall["avg_steps_successful_reasoning"] = _average(
        int(sample.get("num_steps") or 0)
        for sample in sample_reports
        if sample.get("reasoning_success")
    )
    summary["strategy_diagnostics"] = collect_strategy_diagnostics(sample_reports)


def collect_strategy_diagnostics(
    sample_reports: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    trace_fields = {
        "prediction_entropy": [],
        "info_gain": [],
        "score": [],
        "h_current": [],
        "h_next": [],
    }
    candidate_count = 0

    for sample in sample_reports:
        for trace_step in sample.get("model_level_trace", []) or []:
            for field, values in trace_fields.items():
                value = trace_step.get(field)
                if isinstance(value, (int, float)):
                    values.append(float(value))
            candidate_count += len(trace_step.get("candidates", []) or [])

    diagnostics: Dict[str, Any] = {
        "total_trace_steps": sum(len(sample.get("model_level_trace", []) or []) for sample in sample_reports),
        "total_recorded_candidates": candidate_count,
    }
    for field, values in trace_fields.items():
        diagnostics[f"avg_{field}"] = sum(values) / len(values) if values else None
    return diagnostics


def build_ablation_row(
    strategy: str,
    report: Mapping[str, Any],
    args: argparse.Namespace,
) -> Dict[str, Any]:
    summary = report.get("summary", {}) or {}
    overall = summary.get("overall", {}) or {}
    diagnostics = summary.get("strategy_diagnostics", {}) or {}
    theorem = summary.get("theorem_selection", {}) or {}

    return {
        "schema_version": ABLATION_TABLE_SCHEMA_VERSION,
        "strategy": strategy,
        "seed": args.seed,
        "sample_size": args.num,
        "checkpoint_path": args.checkpoint,
        "max_steps": args.max_steps,
        "top_k": args.top_k,
        "lambda_1_p_y_x": args.lambda_weights[0],
        "lambda_2_info_gain": args.lambda_weights[1],
        "lambda_3_h_y_x": args.lambda_weights[2],
        "reasoning_success_count": overall.get("reasoning_success_count", 0),
        "reasoning_success_rate": overall.get("reasoning_success_rate", 0.0),
        "final_answer_correct_count": overall.get("final_answer_correct_count", 0),
        "final_answer_accuracy": overall.get("final_answer_accuracy", 0.0),
        "answer_accuracy_among_successful_reasoning": overall.get(
            "answer_accuracy_among_successful_reasoning", 0.0
        ),
        "avg_steps": overall.get("avg_steps", 0.0),
        "avg_steps_successful_reasoning": overall.get("avg_steps_successful_reasoning", 0.0),
        "theorem_selection_labeled_steps": theorem.get("labeled_steps", 0),
        "theorem_selection_top1_accuracy": theorem.get("top1_accuracy", 0.0),
        "theorem_selection_top3_accuracy": theorem.get("top3_accuracy", 0.0),
        "theorem_selection_top5_accuracy": theorem.get("top5_accuracy", 0.0),
        "avg_prediction_entropy": diagnostics.get("avg_prediction_entropy"),
        "avg_info_gain": diagnostics.get("avg_info_gain"),
        "avg_score": diagnostics.get("avg_score"),
        "failure_reason_distribution": json.dumps(
            summary.get("failure_reason_distribution", {}) or {},
            sort_keys=True,
        ),
        "reasoning_failure_reason_distribution": json.dumps(
            summary.get("reasoning_failure_reason_distribution", {}) or {},
            sort_keys=True,
        ),
    }


def write_ablation_table(
    output_dir: Path,
    strategy_runs: Sequence[Mapping[str, Any]],
    args: argparse.Namespace,
) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [dict(run["row"]) for run in strategy_runs]
    payload = {
        "schema_version": ABLATION_TABLE_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run": {
            "entrypoint": "scripts/experiments/run_search_ablation.py",
            "strategies": [run["strategy"] for run in strategy_runs],
            "num_samples": args.num,
            "seed": args.seed,
            "data_path": args.data,
            "checkpoint_path": args.checkpoint,
            "max_steps": args.max_steps,
            "top_k": args.top_k,
            "lambda_weights": list(args.lambda_weights),
        },
        "rows": rows,
        "reports": {run["strategy"]: run["paths"] for run in strategy_runs},
    }

    json_path = output_dir / "ablation_summary.json"
    csv_path = output_dir / "ablation_summary.csv"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    fieldnames = list(rows[0].keys()) if rows else []
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {
        "ablation_summary_json": str(json_path),
        "ablation_summary_csv": str(csv_path),
    }


def _average(values: Sequence[int] | Any) -> float:
    value_list = list(values)
    return sum(value_list) / len(value_list) if value_list else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run EGR search-strategy ablations")
    parser.add_argument("--num", type=int, default=50, help="Number of samples")
    parser.add_argument("--seed", type=int, default=42, help="Sampling seed")
    parser.add_argument(
        "--data",
        default="data/train_with_models_v2.json",
        help="Reasoning dataset path",
    )
    parser.add_argument(
        "--strategies",
        type=parse_strategies,
        default=default_ablation_strategies(),
        help="Comma-separated strategies or 'all'",
    )
    parser.add_argument(
        "--checkpoint",
        default="checkpoints/model_selector_v2.pth",
        help="Model selector checkpoint for neural strategies",
    )
    parser.add_argument("--device", default="cpu", help="Torch device")
    parser.add_argument("--max-steps", type=int, default=15, help="Reasoning max steps")
    parser.add_argument("--min-steps", type=int, default=1, help="Minimum applied steps")
    parser.add_argument(
        "--max-retries-per-step",
        type=int,
        default=3,
        help="ReasoningEngine retry budget per step",
    )
    parser.add_argument(
        "--completeness-threshold",
        type=float,
        default=0.99,
        help="Reasoning completeness threshold",
    )
    parser.add_argument("--top-k", type=int, default=10, help="Strategy candidate budget")
    parser.add_argument(
        "--lambda-weights",
        type=parse_lambda_weights,
        default=DEFAULT_LAMBDA_WEIGHTS,
        help="Full EGR weights as lambda1,lambda2,lambda3",
    )
    parser.add_argument(
        "--allow-repeated-models",
        action="store_true",
        help="Do not exclude models already recorded in symbolic_state.applied_models",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/experiments/search_ablation_smoke",
        help="Directory for per-strategy reports and ablation summary",
    )
    parser.add_argument("--progress-every", type=int, default=25, help="Progress interval")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress logs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    strategies = args.strategies
    checkpoint_path = PROJECT_ROOT / args.checkpoint

    neural_network = None
    if any(strategy_needs_neural(strategy) for strategy in strategies):
        print(f"loading neural checkpoint: {args.checkpoint}")
        neural_network = load_neural_network(checkpoint_path, args.device)

    print("loading samples...")
    samples = load_test_data(path=args.data, num_samples=args.num, seed=args.seed)

    strategy_runs = []
    for strategy in strategies:
        print(f"\nrunning strategy: {strategy}")
        strategy_runs.append(run_strategy(strategy, samples, args, neural_network))

    table_paths = write_ablation_table(PROJECT_ROOT / args.output_dir, strategy_runs, args)

    print("\nsearch ablation summary")
    for run in strategy_runs:
        row = run["row"]
        print(
            f"{row['strategy']}: "
            f"reasoning={row['reasoning_success_count']}/{row['sample_size']} "
            f"({row['reasoning_success_rate']:.4f}), "
            f"final_correct={row['final_answer_correct_count']}/{row['sample_size']} "
            f"({row['final_answer_accuracy']:.4f}), "
            f"avg_steps={row['avg_steps']:.2f}"
        )
    print("artifacts:")
    for name, path in table_paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
