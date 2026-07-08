"""Run V3 replay correctness benchmark and export state trajectories."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.theorems_v2.replay_benchmark import ReplayBenchmarkV3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT
        / "data"
        / "train_with_models_v3_candidate.json",
    )
    parser.add_argument(
        "--sequence-field",
        choices=("models_v3_observed", "models_v3_executable"),
        default="models_v3_observed",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "v3_replay_summary.json",
    )
    parser.add_argument(
        "--diagnostics-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "v3_replay_diagnostics.jsonl",
    )
    parser.add_argument(
        "--trajectories-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "v3_state_trajectories.jsonl",
    )
    parser.add_argument(
        "--selector-trajectories-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "v3_selector_usable_trajectories.jsonl",
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--assisted-apply",
        action="store_true",
        help=(
            "treat each selected theorem as a macro and transactionally "
            "insert helper theorem applications when they unlock it"
        ),
    )
    parser.add_argument("--max-support-steps", type=int, default=12)
    parser.add_argument(
        "--no-export-trajectories",
        action="store_true",
        help="compute replay metrics without the second trajectory pass",
    )
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    rows = [
        row
        for row in rows
        if row.get(args.sequence_field)
        and str(row.get("process") or "").strip()
    ]
    if args.limit is not None:
        rows = rows[: args.limit]

    benchmark = ReplayBenchmarkV3(
        assisted_apply=args.assisted_apply,
        max_support_steps=args.max_support_steps,
    )
    diagnostics = []
    trajectories = []
    selector_trajectories = []
    step_statuses = Counter()
    goal_statuses = Counter()
    initial_goal_statuses = Counter()
    success_goal_statuses = Counter()
    first_failure_models = Counter()
    first_failure_statuses = Counter()
    missing_predicates = Counter()
    query_goal_statuses = defaultdict(Counter)
    sequence_success = 0
    selector_usable = 0
    goal_progress = 0
    unparsed = 0
    adapter_errors = 0
    support_applications = 0
    support_models = Counter()

    for index, row in enumerate(rows, start=1):
        result = benchmark.evaluate_row(
            row,
            sequence_field=args.sequence_field,
            export_trajectory=not args.no_export_trajectories,
        )
        trajectory = result.pop("trajectory", None)
        diagnostics.append(result)
        if trajectory is not None:
            trajectories.append(
                {
                    "id": result["id"],
                    "sequence_field": args.sequence_field,
                    "sequence": result["sequence"],
                    "query_expressions": row.get(
                        "query_expressions", ""
                    ),
                    "answer_expressions": row.get(
                        "answer_expressions", ""
                    ),
                    "initial_goal": result["initial_goal"],
                    "goal": result["goal"],
                    "selector_usable": result["selector_usable"],
                    "steps": trajectory,
                }
            )
            if result["selector_usable"]:
                selector_trajectories.append(trajectories[-1])
        step_statuses.update(result["step_statuses"])
        for model_ids in result["support_model_ids"]:
            support_applications += len(model_ids)
            support_models.update(model_ids)
        initial_goal_statuses[result["initial_goal"]["status"]] += 1
        goal_statuses[result["goal"]["status"]] += 1
        query_goal_statuses[result["goal"]["query_kind"]][
            result["goal"]["status"]
        ] += 1
        unparsed += result["unparsed_fact_count"]
        adapter_errors += len(result["adapter_errors"])
        if result["sequence_success"]:
            sequence_success += 1
            success_goal_statuses[result["goal"]["status"]] += 1
        if result["selector_usable"]:
            selector_usable += 1
        if result["goal_progress"]:
            goal_progress += 1
        failure = result["first_failure"]
        if failure is not None:
            first_failure_models[
                f"{failure['model_id']}:{failure['status']}"
            ] += 1
            first_failure_statuses[failure["status"]] += 1
            missing_predicates.update(
                failure["missing_predicates"]
            )
        if index % 250 == 0:
            print(
                f"processed {index}/{len(rows)}",
                file=sys.stderr,
            )

    supported = sum(
        count
        for status, count in goal_statuses.items()
        if status != "GOAL_UNSUPPORTED"
    )
    answer_evaluable = (
        goal_statuses["ANSWER_CORRECT"]
        + goal_statuses["ANSWER_INCORRECT"]
    )
    summary = {
        "input": str(args.input),
        "sequence_field": args.sequence_field,
        "assisted_apply": args.assisted_apply,
        "max_support_steps": args.max_support_steps,
        "total_rows": len(rows),
        "step_statuses": dict(step_statuses),
        "sequence_success_rows": sequence_success,
        "sequence_success_rate": (
            sequence_success / len(rows) if rows else 0
        ),
        "initial_goal_statuses": dict(initial_goal_statuses),
        "initial_answer_correct_rows": initial_goal_statuses["ANSWER_CORRECT"],
        "goal_statuses": dict(goal_statuses),
        "goal_progress_rows": goal_progress,
        "goal_supported_rows": supported,
        "goal_supported_rate": supported / len(rows) if rows else 0,
        "answer_evaluable_rows": answer_evaluable,
        "answer_correct_rows": goal_statuses["ANSWER_CORRECT"],
        "answer_accuracy_when_evaluable": (
            goal_statuses["ANSWER_CORRECT"] / answer_evaluable
            if answer_evaluable
            else 0
        ),
        "sequence_success_goal_statuses": dict(
            success_goal_statuses
        ),
        "selector_usable_rows": selector_usable,
        "support_applications": support_applications,
        "support_models": dict(support_models.most_common()),
        "first_failure_statuses": dict(first_failure_statuses),
        "first_failure_models": dict(
            first_failure_models.most_common()
        ),
        "first_failure_missing_predicates": dict(
            missing_predicates.most_common()
        ),
        "query_goal_statuses": {
            query_kind: dict(statuses)
            for query_kind, statuses in sorted(
                query_goal_statuses.items()
            )
        },
        "unparsed_fact_atoms": unparsed,
        "adapter_errors": adapter_errors,
        "trajectory_rows": len(trajectories),
        "selector_trajectory_rows": len(selector_trajectories),
    }

    args.diagnostics_output.parent.mkdir(
        parents=True, exist_ok=True
    )
    with args.diagnostics_output.open(
        "w", encoding="utf-8"
    ) as handle:
        for item in diagnostics:
            handle.write(
                json.dumps(item, ensure_ascii=False) + "\n"
            )

    args.trajectories_output.parent.mkdir(
        parents=True, exist_ok=True
    )
    with args.trajectories_output.open(
        "w", encoding="utf-8"
    ) as handle:
        for item in trajectories:
            handle.write(
                json.dumps(item, ensure_ascii=False) + "\n"
            )

    args.selector_trajectories_output.parent.mkdir(
        parents=True, exist_ok=True
    )
    with args.selector_trajectories_output.open(
        "w", encoding="utf-8"
    ) as handle:
        for item in selector_trajectories:
            handle.write(
                json.dumps(item, ensure_ascii=False) + "\n"
            )

    args.summary_output.parent.mkdir(
        parents=True, exist_ok=True
    )
    rendered = json.dumps(
        summary, ensure_ascii=False, indent=2
    )
    args.summary_output.write_text(
        rendered + "\n", encoding="utf-8"
    )
    print(rendered)


if __name__ == "__main__":
    main()
