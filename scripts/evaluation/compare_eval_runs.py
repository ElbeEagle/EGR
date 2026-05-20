#!/usr/bin/env python3
"""
Compare two EGR unified evaluation sample JSONL files.

The script is intentionally offline: it only reads sample-level evaluation
artifacts and writes audit tables. It does not import or execute the reasoning
engine, solver, selector, or theorem library.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
NONE_LABEL = "none"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two EGR eval runs")
    parser.add_argument(
        "--before",
        default="outputs/evaluation/protocol_200_smoke/samples.jsonl",
        help="Baseline sample JSONL path",
    )
    parser.add_argument(
        "--after",
        default="outputs/evaluation/main_integration_200/samples.jsonl",
        help="Post-change sample JSONL path",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/evaluation/round2_error_audit",
        help="Directory for delta.json, CSV tables, and summary.md",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of samples to list in top-case tables",
    )
    return parser.parse_args()


def resolve_path(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            if "sample_id" not in item:
                raise ValueError(f"{path}:{line_no} has no sample_id")
            rows.append(item)
    return rows


def index_by_sample_id(rows: list[dict[str, Any]], path: Path) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        sample_id = str(row["sample_id"])
        if sample_id in indexed:
            raise ValueError(f"{path} contains duplicate sample_id={sample_id}")
        indexed[sample_id] = row
    return indexed


def norm(value: Any) -> str:
    if value is None:
        return NONE_LABEL
    if isinstance(value, str) and value == "":
        return NONE_LABEL
    return str(value)


def bool_state(value: Any, true_label: str, false_label: str) -> str:
    return true_label if bool(value) else false_label


def seq(row: dict[str, Any]) -> tuple[int, ...]:
    return tuple(row.get("applied_model_sequence") or [])


def seq_str(values: tuple[int, ...]) -> str:
    return " ".join(str(value) for value in values)


def first_or_none(values: tuple[int, ...]) -> str:
    return str(values[0]) if values else NONE_LABEL


def last_or_none(values: tuple[int, ...]) -> str:
    return str(values[-1]) if values else NONE_LABEL


def longest_common_prefix(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    length = 0
    for left_value, right_value in zip(left, right):
        if left_value != right_value:
            break
        length += 1
    return length


def has_repeated_loop(values: tuple[int, ...]) -> bool:
    if len(values) < 5:
        return False
    counts = Counter(values)
    _, count = counts.most_common(1)[0]
    return count >= 5 and count / len(values) >= 0.7


def compact(text: Any, limit: int = 220) -> str:
    value = "" if text is None else str(text)
    value = value.replace("\n", " ").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def md_escape(value: Any) -> str:
    return compact(value, 260).replace("|", "\\|")


def transition_matrix(
    rows: list[dict[str, Any]],
    before_key: str,
    after_key: str,
) -> list[dict[str, Any]]:
    counts = Counter((row[before_key], row[after_key]) for row in rows)
    return [
        {"before": before, "after": after, "count": count}
        for (before, after), count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def build_sample_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_seq = seq(before)
    after_seq = seq(after)
    before_correct = bool(before.get("final_answer_correct"))
    after_correct = bool(after.get("final_answer_correct"))
    before_success = bool(before.get("reasoning_success"))
    after_success = bool(after.get("reasoning_success"))
    before_steps = int(before.get("num_steps") or 0)
    after_steps = int(after.get("num_steps") or 0)
    before_failure = norm(before.get("failure_reason"))
    after_failure = norm(after.get("failure_reason"))
    before_reasoning_failure = norm(before.get("reasoning_failure_reason"))
    after_reasoning_failure = norm(after.get("reasoning_failure_reason"))
    before_query_type = norm(before.get("query_type"))
    after_query_type = norm(after.get("query_type"))
    before_curve_type = norm(before.get("curve_type"))
    after_curve_type = norm(after.get("curve_type"))

    correctness_transition = (
        f"{bool_state(before_correct, 'correct', 'wrong')}->"
        f"{bool_state(after_correct, 'correct', 'wrong')}"
    )
    reasoning_transition = (
        f"{bool_state(before_success, 'success', 'failure')}->"
        f"{bool_state(after_success, 'success', 'failure')}"
    )

    return {
        "sample_id": str(before["sample_id"]),
        "facts": before.get("facts"),
        "query": before.get("query"),
        "expected_answer": before.get("expected_answer"),
        "before_predicted_answer": before.get("predicted_answer"),
        "after_predicted_answer": after.get("predicted_answer"),
        "before_reasoning_success": before_success,
        "after_reasoning_success": after_success,
        "before_final_answer_correct": before_correct,
        "after_final_answer_correct": after_correct,
        "before_failure_reason": before_failure,
        "after_failure_reason": after_failure,
        "before_reasoning_failure_reason": before_reasoning_failure,
        "after_reasoning_failure_reason": after_reasoning_failure,
        "before_query_type": before_query_type,
        "after_query_type": after_query_type,
        "before_curve_type": before_curve_type,
        "after_curve_type": after_curve_type,
        "before_num_steps": before_steps,
        "after_num_steps": after_steps,
        "num_steps_delta": after_steps - before_steps,
        "before_model_sequence": seq_str(before_seq),
        "after_model_sequence": seq_str(after_seq),
        "before_model_sequence_len": len(before_seq),
        "after_model_sequence_len": len(after_seq),
        "model_sequence_changed": before_seq != after_seq,
        "model_sequence_lcp": longest_common_prefix(before_seq, after_seq),
        "before_first_model": first_or_none(before_seq),
        "after_first_model": first_or_none(after_seq),
        "before_last_model": last_or_none(before_seq),
        "after_last_model": last_or_none(after_seq),
        "new_model_ids_after": seq_str(tuple(sorted(set(after_seq) - set(before_seq)))),
        "removed_model_ids_after": seq_str(tuple(sorted(set(before_seq) - set(after_seq)))),
        "after_repeated_model_loop": has_repeated_loop(after_seq),
        "correctness_transition": correctness_transition,
        "reasoning_transition": reasoning_transition,
        "accuracy_gain": (not before_correct) and after_correct,
        "accuracy_regression": before_correct and (not after_correct),
        "success_regression": before_success and (not after_success),
        "success_gain": (not before_success) and after_success,
        "query_type_changed": before_query_type != after_query_type,
        "curve_type_changed": before_curve_type != after_curve_type,
    }


def summarize_by_query_type(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = row["after_query_type"]
        grouped[key].append(row)

    summary: list[dict[str, Any]] = []
    for query_type, items in grouped.items():
        before_success = sum(1 for item in items if item["before_reasoning_success"])
        after_success = sum(1 for item in items if item["after_reasoning_success"])
        before_correct = sum(1 for item in items if item["before_final_answer_correct"])
        after_correct = sum(1 for item in items if item["after_final_answer_correct"])
        step_deltas = [item["num_steps_delta"] for item in items]
        summary.append(
            {
                "query_type": query_type,
                "total": len(items),
                "before_reasoning_success": before_success,
                "after_reasoning_success": after_success,
                "reasoning_success_delta": after_success - before_success,
                "before_final_correct": before_correct,
                "after_final_correct": after_correct,
                "final_correct_delta": after_correct - before_correct,
                "success_regressions": sum(1 for item in items if item["success_regression"]),
                "success_gains": sum(1 for item in items if item["success_gain"]),
                "accuracy_gains": sum(1 for item in items if item["accuracy_gain"]),
                "accuracy_regressions": sum(1 for item in items if item["accuracy_regression"]),
                "sequence_changed": sum(1 for item in items if item["model_sequence_changed"]),
                "avg_num_steps_delta": mean(step_deltas) if step_deltas else 0.0,
            }
        )

    return sorted(summary, key=lambda item: (-abs(item["final_correct_delta"]), item["query_type"]))


def summarize_by_curve_type(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["after_curve_type"]].append(row)

    summary: list[dict[str, Any]] = []
    for curve_type, items in grouped.items():
        before_success = sum(1 for item in items if item["before_reasoning_success"])
        after_success = sum(1 for item in items if item["after_reasoning_success"])
        before_correct = sum(1 for item in items if item["before_final_answer_correct"])
        after_correct = sum(1 for item in items if item["after_final_answer_correct"])
        summary.append(
            {
                "curve_type": curve_type,
                "total": len(items),
                "before_reasoning_success": before_success,
                "after_reasoning_success": after_success,
                "reasoning_success_delta": after_success - before_success,
                "before_final_correct": before_correct,
                "after_final_correct": after_correct,
                "final_correct_delta": after_correct - before_correct,
                "success_regressions": sum(1 for item in items if item["success_regression"]),
                "accuracy_gains": sum(1 for item in items if item["accuracy_gain"]),
                "accuracy_regressions": sum(1 for item in items if item["accuracy_regression"]),
            }
        )

    return sorted(summary, key=lambda item: (-abs(item["reasoning_success_delta"]), item["curve_type"]))


def model_usage(rows: list[dict[str, Any]], key: str) -> Counter[int]:
    counter: Counter[int] = Counter()
    for row in rows:
        sequence_text = row[key]
        if not sequence_text:
            continue
        for model_id in sequence_text.split():
            counter[int(model_id)] += 1
    return counter


def model_usage_delta(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    before = model_usage(rows, "before_model_sequence")
    after = model_usage(rows, "after_model_sequence")
    model_ids = sorted(set(before) | set(after))
    entries = [
        {
            "model_id": model_id,
            "before_usage": before.get(model_id, 0),
            "after_usage": after.get(model_id, 0),
            "delta": after.get(model_id, 0) - before.get(model_id, 0),
        }
        for model_id in model_ids
    ]
    return sorted(entries, key=lambda item: (-abs(item["delta"]), item["model_id"]))


def transition_tables(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    tables = {
        "final_answer_correct": transition_matrix(rows, "before_final_state", "after_final_state"),
        "reasoning_success": transition_matrix(rows, "before_reasoning_state", "after_reasoning_state"),
        "failure_reason": transition_matrix(rows, "before_failure_reason", "after_failure_reason"),
        "reasoning_failure_reason": transition_matrix(
            rows,
            "before_reasoning_failure_reason",
            "after_reasoning_failure_reason",
        ),
        "query_type": transition_matrix(rows, "before_query_type", "after_query_type"),
        "curve_type": transition_matrix(rows, "before_curve_type", "after_curve_type"),
        "first_model": transition_matrix(rows, "before_first_model", "after_first_model"),
        "last_model": transition_matrix(rows, "before_last_model", "after_last_model"),
    }

    step_counts = Counter(row["num_steps_delta"] for row in rows)
    tables["num_steps_delta"] = [
        {"before": "delta", "after": str(delta), "count": count}
        for delta, count in sorted(step_counts.items(), key=lambda item: (item[0], item[1]))
    ]
    return tables


def add_state_fields(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        row["before_final_state"] = bool_state(
            row["before_final_answer_correct"],
            "correct",
            "wrong",
        )
        row["after_final_state"] = bool_state(
            row["after_final_answer_correct"],
            "correct",
            "wrong",
        )
        row["before_reasoning_state"] = bool_state(
            row["before_reasoning_success"],
            "success",
            "failure",
        )
        row["after_reasoning_state"] = bool_state(
            row["after_reasoning_success"],
            "success",
            "failure",
        )


def top_accuracy_gains(rows: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    gains = [row for row in rows if row["accuracy_gain"]]
    return sorted(
        gains,
        key=lambda row: (
            row["before_reasoning_success"],
            row["before_failure_reason"],
            row["after_query_type"],
            int(row["sample_id"]),
        ),
        reverse=True,
    )[:top_n]


def top_success_regressions(rows: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    regressions = [row for row in rows if row["success_regression"]]
    return sorted(
        regressions,
        key=lambda row: (
            row["before_final_answer_correct"],
            row["after_reasoning_failure_reason"],
            row["after_query_type"],
            -row["after_num_steps"],
            int(row["sample_id"]),
        ),
        reverse=True,
    )[:top_n]


def top_accuracy_regressions(rows: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    regressions = [row for row in rows if row["accuracy_regression"]]
    return sorted(regressions, key=lambda row: int(row["sample_id"]))[:top_n]


def build_repair_priorities(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priorities: list[dict[str, Any]] = []
    accuracy_regressions = [row for row in rows if row["accuracy_regression"]]
    if accuracy_regressions:
        priorities.append(
            {
                "priority": "P0",
                "area": "Protect previously correct samples",
                "evidence": (
                    f"{len(accuracy_regressions)} samples changed from correct to wrong; "
                    "these are direct regressions on the primary metric."
                ),
                "suggested_next_step": (
                    "Start solver-hardening with these exact cases and add regression tests "
                    "before broader extractor changes."
                ),
                "sample_ids": [row["sample_id"] for row in accuracy_regressions[:10]],
            }
        )

    success_regressions = [row for row in rows if row["success_regression"]]
    success_regression_buckets = Counter(
        (
            row["after_reasoning_failure_reason"],
            row["after_query_type"],
            row["after_curve_type"],
        )
        for row in success_regressions
    )
    if success_regression_buckets:
        (reason, query_type, curve_type), count = success_regression_buckets.most_common(1)[0]
        changed_sequences = sum(1 for row in success_regressions if row["model_sequence_changed"])
        sample_ids = [
            row["sample_id"]
            for row in success_regressions
            if row["after_reasoning_failure_reason"] == reason
            and row["after_query_type"] == query_type
            and row["after_curve_type"] == curve_type
        ][:10]
        priorities.append(
            {
                "priority": "P0",
                "area": "Recover reasoning-success regressions",
                "evidence": (
                    f"{len(success_regressions)} samples changed from reasoning success to "
                    f"reasoning failure; top bucket {reason}/{query_type}/{curve_type}={count}. "
                    f"model_sequence_changed={changed_sequences}/{len(success_regressions)}, "
                    "so this is post-trace extraction/result.success drift."
                ),
                "suggested_next_step": (
                    "Replay this bucket through AnswerExtractor and restore coverage for "
                    "high-frequency Parabola/Value forms without weakening final-answer checks."
                ),
                "sample_ids": sample_ids,
            }
        )

    loop_rows = [
        row
        for row in rows
        if row["after_repeated_model_loop"] and row["after_failure_reason"] != NONE_LABEL
    ]
    if loop_rows:
        loop_models = Counter(row["after_last_model"] for row in loop_rows)
        model_id, count = loop_models.most_common(1)[0]
        priorities.append(
            {
                "priority": "P2",
                "area": "Stop repeated no-progress theorem loops",
                "evidence": (
                    f"{len(loop_rows)} failed after-run samples repeatedly apply one model; "
                    f"model {model_id} appears in {count}. This is a solver-hardening target, "
                    "not a new theorem-route delta."
                ),
                "suggested_next_step": (
                    "Add or tune a no-progress guard after the answer-extraction regressions "
                    "are covered."
                ),
                "sample_ids": [row["sample_id"] for row in loop_rows[:10]],
            }
        )

    accuracy_gains = [row for row in rows if row["accuracy_gain"]]
    if accuracy_gains:
        gain_queries = Counter(row["after_query_type"] for row in accuracy_gains)
        priorities.append(
            {
                "priority": "P1",
                "area": "Preserve symbolic answer-extraction gains",
                "evidence": (
                    f"{len(accuracy_gains)} samples moved from wrong to correct; top query "
                    f"gains are {dict(gain_queries.most_common(4))}."
                ),
                "suggested_next_step": (
                    "Turn the top gain cases into regression tests before hardening adjacent "
                    "solver paths."
                ),
                "sample_ids": [row["sample_id"] for row in accuracy_gains[:10]],
            }
        )

    after_answer_mismatch = [
        row
        for row in rows
        if row["after_failure_reason"] == "answer_mismatch"
        and row["after_reasoning_success"]
    ]
    if after_answer_mismatch:
        mismatch_queries = Counter(row["after_query_type"] for row in after_answer_mismatch)
        query_type, count = mismatch_queries.most_common(1)[0]
        priorities.append(
            {
                "priority": "P2",
                "area": "Reduce remaining successful-reasoning answer mismatches",
                "evidence": (
                    f"{len(after_answer_mismatch)} after-run samples still reason successfully "
                    f"but answer incorrectly; largest query bucket is {query_type} with {count}."
                ),
                "suggested_next_step": (
                    "After recovering success regressions, harden final answer extraction and "
                    "comparison for the largest mismatch query buckets."
                ),
                "sample_ids": [
                    row["sample_id"]
                    for row in after_answer_mismatch
                    if row["after_query_type"] == query_type
                ][:10],
            }
        )

    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    return sorted(priorities, key=lambda item: priority_order.get(item["priority"], 99))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=True)
        handle.write("\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_matrix_csv(path: Path, tables: dict[str, list[dict[str, Any]]]) -> None:
    rows: list[dict[str, Any]] = []
    for name, items in tables.items():
        for item in items:
            rows.append(
                {
                    "matrix": name,
                    "before": item["before"],
                    "after": item["after"],
                    "count": item["count"],
                }
            )
    write_csv(path, rows, ["matrix", "before", "after", "count"])


def md_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "_None._\n"
    headers = [label for _, label in columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(md_escape(row.get(key, "")) for key, _ in columns)
            + " |"
        )
    return "\n".join(lines) + "\n"


def matrix_section(title: str, rows: list[dict[str, Any]], limit: int | None = None) -> str:
    displayed = rows[:limit] if limit else rows
    return (
        f"## {title}\n\n"
        + md_table(
            displayed,
            [("before", "before"), ("after", "after"), ("count", "count")],
        )
        + "\n"
    )


def write_markdown_summary(path: Path, payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    matrices = payload["transition_matrices"]
    case_columns = [
        ("sample_id", "sample_id"),
        ("after_curve_type", "curve"),
        ("after_query_type", "query_type"),
        ("before_failure_reason", "before_failure"),
        ("after_failure_reason", "after_failure"),
        ("before_num_steps", "before_steps"),
        ("after_num_steps", "after_steps"),
        ("expected_answer", "expected"),
        ("before_predicted_answer", "before_predicted"),
        ("after_predicted_answer", "after_predicted"),
        ("query", "query"),
    ]

    lines: list[str] = []
    lines.append("# Round 2 Integration Error Audit")
    lines.append("")
    lines.append(f"Generated at: `{payload['metadata']['generated_at_utc']}`")
    lines.append(f"Before: `{payload['metadata']['before_path']}`")
    lines.append(f"After: `{payload['metadata']['after_path']}`")
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append(
        "- Final answer accuracy: "
        f"{summary['before_final_correct']}/{summary['total_samples']} "
        f"({pct(summary['before_final_accuracy'])}) -> "
        f"{summary['after_final_correct']}/{summary['total_samples']} "
        f"({pct(summary['after_final_accuracy'])}); "
        f"delta {summary['final_correct_delta']:+d} samples."
    )
    lines.append(
        "- Reasoning success: "
        f"{summary['before_reasoning_success']}/{summary['total_samples']} "
        f"({pct(summary['before_reasoning_success_rate'])}) -> "
        f"{summary['after_reasoning_success']}/{summary['total_samples']} "
        f"({pct(summary['after_reasoning_success_rate'])}); "
        f"delta {summary['reasoning_success_delta']:+d} samples."
    )
    lines.append(
        "- Wrong -> correct: "
        f"{summary['accuracy_gain_count']}; correct -> wrong: "
        f"{summary['accuracy_regression_count']}."
    )
    lines.append(
        "- Reasoning success -> reasoning failure: "
        f"{summary['success_regression_count']}; reasoning failure -> success: "
        f"{summary['success_gain_count']}."
    )
    lines.append(
        "- Model sequence changed for "
        f"{summary['model_sequence_changed_count']}/{summary['total_samples']} samples; "
        f"num_steps changed for {summary['num_steps_changed_count']} samples."
    )
    if summary["model_sequence_changed_count"] == 0 and summary["reasoning_success_delta"] != 0:
        lines.append(
            "- Diagnostic: all theorem traces and step counts are identical, so the "
            "reasoning-success delta comes from post-trace answer extraction / "
            "result.success behavior, not changed model selection."
        )
    lines.append("")

    lines.append(matrix_section("Final-Correct Transition Matrix", matrices["final_answer_correct"]))
    lines.append(matrix_section("Reasoning-Success Transition Matrix", matrices["reasoning_success"]))
    lines.append(matrix_section("Failure-Reason Transition Matrix", matrices["failure_reason"]))
    lines.append(matrix_section("Query-Type Transition Matrix", matrices["query_type"]))
    lines.append(matrix_section("Num-Steps Delta Distribution", matrices["num_steps_delta"]))

    lines.append("## By Query Type")
    lines.append("")
    lines.append(
        md_table(
            payload["by_query_type"],
            [
                ("query_type", "query_type"),
                ("total", "n"),
                ("before_reasoning_success", "before_success"),
                ("after_reasoning_success", "after_success"),
                ("reasoning_success_delta", "success_delta"),
                ("before_final_correct", "before_correct"),
                ("after_final_correct", "after_correct"),
                ("final_correct_delta", "correct_delta"),
                ("success_regressions", "success_regressions"),
                ("accuracy_gains", "accuracy_gains"),
                ("accuracy_regressions", "accuracy_regressions"),
            ],
        )
    )
    lines.append("")

    lines.append("## By Curve Type")
    lines.append("")
    lines.append(
        md_table(
            payload["by_curve_type"],
            [
                ("curve_type", "curve_type"),
                ("total", "n"),
                ("before_reasoning_success", "before_success"),
                ("after_reasoning_success", "after_success"),
                ("reasoning_success_delta", "success_delta"),
                ("before_final_correct", "before_correct"),
                ("after_final_correct", "after_correct"),
                ("final_correct_delta", "correct_delta"),
                ("success_regressions", "success_regressions"),
                ("accuracy_gains", "accuracy_gains"),
                ("accuracy_regressions", "accuracy_regressions"),
            ],
        )
    )
    lines.append("")

    lines.append("## Top Accuracy-Gain Samples")
    lines.append("")
    lines.append(md_table(payload["top_accuracy_gain_samples"], case_columns))
    lines.append("")

    lines.append("## Top Success-Regression Samples")
    lines.append("")
    lines.append(md_table(payload["top_success_regression_samples"], case_columns))
    lines.append("")

    lines.append("## Correct-to-Wrong Samples")
    lines.append("")
    lines.append(md_table(payload["top_accuracy_regression_samples"], case_columns))
    lines.append("")

    lines.append("## Largest Model Usage Deltas")
    lines.append("")
    lines.append(
        md_table(
            payload["model_usage_delta"][:20],
            [
                ("model_id", "model_id"),
                ("before_usage", "before_usage"),
                ("after_usage", "after_usage"),
                ("delta", "delta"),
            ],
        )
    )
    lines.append("")

    lines.append("## Solver-Hardening Priorities")
    lines.append("")
    lines.append(
        md_table(
            payload["repair_priorities"],
            [
                ("priority", "priority"),
                ("area", "area"),
                ("evidence", "evidence"),
                ("suggested_next_step", "suggested_next_step"),
                ("sample_ids", "sample_ids"),
            ],
        )
    )
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def build_payload(before_path: Path, after_path: Path, top_n: int) -> dict[str, Any]:
    before_rows = load_jsonl(before_path)
    after_rows = load_jsonl(after_path)
    before_index = index_by_sample_id(before_rows, before_path)
    after_index = index_by_sample_id(after_rows, after_path)

    before_ids = set(before_index)
    after_ids = set(after_index)
    common_ids = sorted(before_ids & after_ids, key=lambda value: int(value))
    if before_ids != after_ids:
        missing_after = sorted(before_ids - after_ids, key=lambda value: int(value))
        missing_before = sorted(after_ids - before_ids, key=lambda value: int(value))
    else:
        missing_after = []
        missing_before = []

    sample_deltas = [
        build_sample_delta(before_index[sample_id], after_index[sample_id])
        for sample_id in common_ids
    ]
    add_state_fields(sample_deltas)

    total = len(sample_deltas)
    before_success = sum(1 for row in sample_deltas if row["before_reasoning_success"])
    after_success = sum(1 for row in sample_deltas if row["after_reasoning_success"])
    before_correct = sum(1 for row in sample_deltas if row["before_final_answer_correct"])
    after_correct = sum(1 for row in sample_deltas if row["after_final_answer_correct"])
    sequence_changed = sum(1 for row in sample_deltas if row["model_sequence_changed"])
    num_steps_changed = sum(1 for row in sample_deltas if row["num_steps_delta"] != 0)

    matrices = transition_tables(sample_deltas)
    gains = top_accuracy_gains(sample_deltas, top_n)
    success_regressions = top_success_regressions(sample_deltas, top_n)
    accuracy_regressions = top_accuracy_regressions(sample_deltas, top_n)

    return {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "before_path": str(before_path.relative_to(PROJECT_ROOT)),
            "after_path": str(after_path.relative_to(PROJECT_ROOT)),
            "common_sample_count": len(common_ids),
            "missing_in_after": missing_after,
            "missing_in_before": missing_before,
            "top_n": top_n,
        },
        "summary": {
            "total_samples": total,
            "before_reasoning_success": before_success,
            "after_reasoning_success": after_success,
            "reasoning_success_delta": after_success - before_success,
            "before_reasoning_success_rate": rate(before_success, total),
            "after_reasoning_success_rate": rate(after_success, total),
            "before_final_correct": before_correct,
            "after_final_correct": after_correct,
            "final_correct_delta": after_correct - before_correct,
            "before_final_accuracy": rate(before_correct, total),
            "after_final_accuracy": rate(after_correct, total),
            "accuracy_gain_count": sum(1 for row in sample_deltas if row["accuracy_gain"]),
            "accuracy_regression_count": sum(1 for row in sample_deltas if row["accuracy_regression"]),
            "success_regression_count": sum(1 for row in sample_deltas if row["success_regression"]),
            "success_gain_count": sum(1 for row in sample_deltas if row["success_gain"]),
            "query_type_changed_count": sum(1 for row in sample_deltas if row["query_type_changed"]),
            "curve_type_changed_count": sum(1 for row in sample_deltas if row["curve_type_changed"]),
            "model_sequence_changed_count": sequence_changed,
            "model_sequence_unchanged_count": total - sequence_changed,
            "num_steps_changed_count": num_steps_changed,
            "avg_num_steps_delta": mean(row["num_steps_delta"] for row in sample_deltas)
            if sample_deltas
            else 0.0,
            "after_repeated_model_loop_failure_count": sum(
                1
                for row in sample_deltas
                if row["after_repeated_model_loop"] and row["after_failure_reason"] != NONE_LABEL
            ),
        },
        "transition_matrices": matrices,
        "by_query_type": summarize_by_query_type(sample_deltas),
        "by_curve_type": summarize_by_curve_type(sample_deltas),
        "model_usage_delta": model_usage_delta(sample_deltas),
        "top_accuracy_gain_samples": gains,
        "top_success_regression_samples": success_regressions,
        "top_accuracy_regression_samples": accuracy_regressions,
        "repair_priorities": build_repair_priorities(sample_deltas),
        "samples": sample_deltas,
    }


def main() -> None:
    args = parse_args()
    before_path = resolve_path(args.before)
    after_path = resolve_path(args.after)
    output_dir = resolve_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = build_payload(before_path, after_path, args.top_n)

    sample_fields = [
        "sample_id",
        "before_curve_type",
        "after_curve_type",
        "before_query_type",
        "after_query_type",
        "query_type_changed",
        "before_reasoning_success",
        "after_reasoning_success",
        "reasoning_transition",
        "before_final_answer_correct",
        "after_final_answer_correct",
        "correctness_transition",
        "before_failure_reason",
        "after_failure_reason",
        "before_reasoning_failure_reason",
        "after_reasoning_failure_reason",
        "before_num_steps",
        "after_num_steps",
        "num_steps_delta",
        "before_first_model",
        "after_first_model",
        "before_last_model",
        "after_last_model",
        "before_model_sequence_len",
        "after_model_sequence_len",
        "model_sequence_changed",
        "model_sequence_lcp",
        "new_model_ids_after",
        "removed_model_ids_after",
        "after_repeated_model_loop",
        "expected_answer",
        "before_predicted_answer",
        "after_predicted_answer",
        "query",
        "facts",
        "before_model_sequence",
        "after_model_sequence",
    ]
    case_fields = [
        "sample_id",
        "after_curve_type",
        "after_query_type",
        "before_failure_reason",
        "after_failure_reason",
        "before_reasoning_failure_reason",
        "after_reasoning_failure_reason",
        "before_num_steps",
        "after_num_steps",
        "expected_answer",
        "before_predicted_answer",
        "after_predicted_answer",
        "query",
        "facts",
        "before_model_sequence",
        "after_model_sequence",
    ]

    write_json(output_dir / "delta.json", payload)
    write_csv(output_dir / "sample_deltas.csv", payload["samples"], sample_fields)
    write_matrix_csv(output_dir / "transition_matrices.csv", payload["transition_matrices"])
    write_csv(
        output_dir / "accuracy_gain_top20.csv",
        payload["top_accuracy_gain_samples"],
        case_fields,
    )
    write_csv(
        output_dir / "success_regression_top20.csv",
        payload["top_success_regression_samples"],
        case_fields,
    )
    write_markdown_summary(output_dir / "summary.md", payload)

    summary = payload["summary"]
    print("comparison complete")
    print(
        "final_answer_accuracy: "
        f"{summary['before_final_correct']}/{summary['total_samples']} -> "
        f"{summary['after_final_correct']}/{summary['total_samples']} "
        f"(delta {summary['final_correct_delta']:+d})"
    )
    print(
        "reasoning_success: "
        f"{summary['before_reasoning_success']}/{summary['total_samples']} -> "
        f"{summary['after_reasoning_success']}/{summary['total_samples']} "
        f"(delta {summary['reasoning_success_delta']:+d})"
    )
    print(f"artifacts: {output_dir}")


if __name__ == "__main__":
    main()
