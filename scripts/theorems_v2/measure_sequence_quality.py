"""Measure theorem-sequence execution and final-answer success rates.

This is the compact, one-pass evaluation entry point.  It intentionally does
not export replay trajectories; use ``run_v3_replay_benchmark.py`` when
detailed per-step diagnostics are needed.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.theorems_v2.replay_benchmark import ReplayBenchmarkV3


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def select_rows(
    rows: Iterable[dict[str, Any]],
    sequence_field: str,
    require_process: bool = True,
) -> tuple[list[dict[str, Any]], Counter[str]]:
    """Select rows with a theorem sequence and describe all exclusions."""
    selected: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    for row in rows:
        if not row.get(sequence_field):
            exclusions["empty_sequence"] += 1
        elif require_process and not str(row.get("process") or "").strip():
            exclusions["empty_process"] += 1
        else:
            selected.append(row)
    return selected, exclusions


def evaluate_rows(
    rows: Iterable[dict[str, Any]],
    benchmark: ReplayBenchmarkV3,
    sequence_field: str,
    progress_every: int = 250,
) -> dict[str, Any]:
    """Replay rows and return counts with explicit denominators."""
    rows = list(rows)
    goal_statuses: Counter[str] = Counter()
    failure_statuses: Counter[str] = Counter()
    execution_success = 0
    answer_correct = 0
    newly_answer_correct = 0
    execution_and_answer_correct = 0

    for index, row in enumerate(rows, start=1):
        result = benchmark.evaluate_row(
            row,
            sequence_field=sequence_field,
            export_trajectory=False,
        )
        goal_status = result["goal"]["status"]
        goal_statuses[goal_status] += 1
        sequence_ok = result["sequence_success"]
        answer_ok = goal_status == "ANSWER_CORRECT"

        execution_success += int(sequence_ok)
        answer_correct += int(answer_ok)
        newly_answer_correct += int(result["goal_progress"])
        execution_and_answer_correct += int(sequence_ok and answer_ok)
        if result["first_failure"] is not None:
            failure_statuses[result["first_failure"]["status"]] += 1

        if progress_every and index % progress_every == 0:
            print(f"processed {index}/{len(rows)}", file=sys.stderr)

    total = len(rows)
    answer_evaluable = (
        goal_statuses["ANSWER_CORRECT"]
        + goal_statuses["ANSWER_INCORRECT"]
    )
    return {
        "evaluated_sequence_rows": total,
        "execution_success": {
            "rows": execution_success,
            "denominator": total,
            "rate": _rate(execution_success, total),
        },
        "final_answer_correct": {
            "rows": answer_correct,
            "denominator": total,
            "rate": _rate(answer_correct, total),
        },
        "newly_answer_correct_after_replay": {
            "rows": newly_answer_correct,
            "denominator": total,
            "rate": _rate(newly_answer_correct, total),
        },
        "execution_and_answer_correct": {
            "rows": execution_and_answer_correct,
            "denominator": total,
            "rate": _rate(execution_and_answer_correct, total),
        },
        "answer_correct_given_execution_success": {
            "rows": execution_and_answer_correct,
            "denominator": execution_success,
            "rate": _rate(execution_and_answer_correct, execution_success),
        },
        "answer_accuracy_when_evaluable": {
            "rows": answer_correct,
            "denominator": answer_evaluable,
            "rate": _rate(answer_correct, answer_evaluable),
        },
        "goal_statuses": dict(goal_statuses),
        "first_failure_statuses": dict(failure_statuses),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Replay theorem sequences and measure full-sequence execution "
            "and final-answer correctness."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "train_with_models_v3_candidate.json",
    )
    parser.add_argument(
        "--sequence-field",
        choices=("models_v3_observed", "models_v3_executable"),
        default="models_v3_observed",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "sequence_quality_summary.json",
    )
    parser.add_argument(
        "--assisted-apply",
        action=argparse.BooleanOptionalAction,
        default=False,
        help=(
            "allow transactional helper-theorem insertion; disabled by "
            "default so execution_success measures the original sequence"
        ),
    )
    parser.add_argument("--max-support-steps", type=int, default=12)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--include-empty-process",
        action="store_true",
        help="include the rare labeled rows whose source process is empty",
    )
    parser.add_argument("--progress-every", type=int, default=250)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    all_rows = json.loads(args.input.read_text(encoding="utf-8"))
    selected, exclusions = select_rows(
        all_rows,
        args.sequence_field,
        require_process=not args.include_empty_process,
    )
    if args.limit is not None:
        selected = selected[: args.limit]

    benchmark = ReplayBenchmarkV3(
        assisted_apply=args.assisted_apply,
        max_support_steps=args.max_support_steps,
    )
    metrics = evaluate_rows(
        selected,
        benchmark,
        args.sequence_field,
        progress_every=args.progress_every,
    )
    summary = {
        "input": str(args.input.resolve()),
        "dataset_rows": len(all_rows),
        "sequence_field": args.sequence_field,
        "assisted_apply": args.assisted_apply,
        "max_support_steps": args.max_support_steps,
        "exclusions": dict(exclusions),
        **metrics,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
