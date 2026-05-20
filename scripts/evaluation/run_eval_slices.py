#!/usr/bin/env python3
"""
Generate compact slice tables for EGR unified evaluation runs.

This script either post-processes an existing run_eval_protocol output
directory, or runs the same unified protocol in compact mode and writes only
summary/table artifacts by default.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.evaluation.run_eval_protocol import load_selector_report, run_samples
from scripts.reasoning.batch_test import load_test_data
from src.evaluation import build_eval_report
from src.evaluation.protocol import summary_rows


METRIC_COLUMNS = [
    "slice",
    "total_samples",
    "final_answer_correct_count",
    "final_answer_accuracy",
    "reasoning_success_count",
    "reasoning_success_rate",
    "answer_accuracy_among_successful_reasoning",
    "theorem_selection_labeled_steps",
    "theorem_selection_top1_accuracy",
    "theorem_selection_top3_accuracy",
    "theorem_selection_top5_accuracy",
]


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def metric_row(name: str, metrics: Mapping[str, Any]) -> Dict[str, Any]:
    row = {"slice": name}
    for column in METRIC_COLUMNS[1:]:
        row[column] = metrics.get(column, 0)
    return row


def grouped_metric_rows(group: Mapping[str, Mapping[str, Any]]) -> list[Dict[str, Any]]:
    rows = [metric_row(str(name), metrics) for name, metrics in group.items()]
    return sorted(rows, key=lambda item: (-int(item["total_samples"]), str(item["slice"])))


def distribution_rows(distribution: Mapping[str, Any], key_name: str) -> list[Dict[str, Any]]:
    rows = []
    for name, count in distribution.items():
        rows.append({key_name: str(name), "count": int(count)})
    return sorted(rows, key=lambda item: (-item["count"], item[key_name]))


def write_summary_csv(summary: Mapping[str, Any], output_dir: Path) -> Path:
    rows = summary_rows(summary)
    fieldnames = [
        "group",
        "value",
        "total_samples",
        "reasoning_success_count",
        "reasoning_success_rate",
        "final_answer_correct_count",
        "final_answer_accuracy",
        "answer_accuracy_among_successful_reasoning",
        "theorem_selection_labeled_steps",
        "theorem_selection_top1_accuracy",
        "theorem_selection_top3_accuracy",
        "theorem_selection_top5_accuracy",
    ]
    path = output_dir / "summary.csv"
    write_csv(path, rows, fieldnames)
    return path


def format_rate(value: Any) -> str:
    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return "0.0000"


def write_markdown_report(
    path: Path,
    summary: Mapping[str, Any],
    table_paths: Mapping[str, Path],
) -> None:
    overall = summary.get("overall", {}) or {}
    lines = [
        "# Round 2 Evaluation Slice Tables",
        "",
        "Primary metric is final answer accuracy. Reasoning success is reported separately.",
        "",
        "## Overall",
        "",
        "| metric | value |",
        "| --- | ---: |",
        f"| total_samples | {overall.get('total_samples', 0)} |",
        (
            "| final_answer_accuracy | "
            f"{overall.get('final_answer_correct_count', 0)}/"
            f"{overall.get('total_samples', 0)} = "
            f"{format_rate(overall.get('final_answer_accuracy'))} |"
        ),
        (
            "| reasoning_success_rate | "
            f"{overall.get('reasoning_success_count', 0)}/"
            f"{overall.get('total_samples', 0)} = "
            f"{format_rate(overall.get('reasoning_success_rate'))} |"
        ),
        (
            "| answer_accuracy_among_successful_reasoning | "
            f"{format_rate(overall.get('answer_accuracy_among_successful_reasoning'))} |"
        ),
        "",
        "## Tables",
        "",
    ]
    for name, table_path in table_paths.items():
        lines.append(f"- {name}: `{table_path.relative_to(PROJECT_ROOT)}`")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def generate_slice_tables(summary: Mapping[str, Any], output_dir: Path) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    table_dir = output_dir / "slice_tables"
    table_dir.mkdir(parents=True, exist_ok=True)

    table_paths: Dict[str, Path] = {}

    overall_path = table_dir / "overall_table.csv"
    write_csv(
        overall_path,
        [metric_row("all", summary.get("overall", {}) or {})],
        METRIC_COLUMNS,
    )
    table_paths["overall"] = overall_path

    for key, filename, label in [
        ("by_query_type", "query_type_table.csv", "query_type"),
        ("by_curve_type", "curve_type_table.csv", "curve_type"),
        ("by_failure_reason", "failure_reason_table.csv", "failure_reason"),
    ]:
        path = table_dir / filename
        rows = grouped_metric_rows(summary.get(key, {}) or {})
        fieldnames = [label] + METRIC_COLUMNS[1:]
        normalized = [{label: row.pop("slice"), **row} for row in rows]
        write_csv(path, normalized, fieldnames)
        table_paths[label] = path

    failure_dist_path = table_dir / "failure_reason_distribution.csv"
    write_csv(
        failure_dist_path,
        distribution_rows(summary.get("failure_reason_distribution", {}) or {}, "failure_reason"),
        ["failure_reason", "count"],
    )
    table_paths["failure_reason_distribution"] = failure_dist_path

    reasoning_failure_path = table_dir / "reasoning_failure_reason_distribution.csv"
    write_csv(
        reasoning_failure_path,
        distribution_rows(
            summary.get("reasoning_failure_reason_distribution", {}) or {},
            "reasoning_failure_reason",
        ),
        ["reasoning_failure_reason", "count"],
    )
    table_paths["reasoning_failure_reason_distribution"] = reasoning_failure_path

    markdown_path = output_dir / "slice_tables.md"
    write_markdown_report(markdown_path, summary, table_paths)
    table_paths["markdown"] = markdown_path

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": {
            name: {
                "path": str(path),
                "size_bytes": path.stat().st_size if path.exists() else 0,
            }
            for name, path in sorted(table_paths.items())
        },
    }
    manifest_path = output_dir / "slice_artifact_manifest.json"
    write_json(manifest_path, manifest)
    table_paths["manifest"] = manifest_path

    return {name: str(path) for name, path in table_paths.items()}


def write_samples_jsonl(path: Path, samples: Iterable[Mapping[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")


def run_compact_eval(args: argparse.Namespace) -> Mapping[str, Any]:
    samples = load_test_data(path=args.data, num_samples=args.num, seed=args.seed)
    sample_reports = run_samples(samples, verbose_progress=not args.quiet)
    selector_report = load_selector_report(PROJECT_ROOT / args.selector_report)
    report = build_eval_report(
        sample_reports,
        run_metadata={
            "num_samples": args.num,
            "seed": args.seed,
            "data_path": args.data,
            "selector_report_path": args.selector_report if selector_report else None,
            "protocol_entrypoint": "scripts/evaluation/run_eval_slices.py",
            "reasoning_entrypoint": "scripts/reasoning/batch_test.py:init_engine",
            "compact_artifacts": not args.write_samples,
        },
        selector_report=selector_report,
    )

    output_dir = PROJECT_ROOT / args.output_dir
    write_json(output_dir / "summary.json", report["summary"])
    write_json(
        output_dir / "run_metadata.json",
        {
            "schema_version": report["schema_version"],
            "generated_at": report["generated_at"],
            "run": report["run"],
            "sample_level_artifacts_written": bool(args.write_samples),
        },
    )
    write_summary_csv(report["summary"], output_dir)

    if args.write_samples:
        write_samples_jsonl(output_dir / "samples.jsonl", report["samples"])

    return report["summary"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run or post-process EGR unified evaluation slice tables"
    )
    parser.add_argument(
        "--eval-dir",
        help="Existing evaluation directory containing summary.json",
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory. Defaults to --eval-dir for post-processing.",
    )
    parser.add_argument(
        "--run-eval",
        action="store_true",
        help="Run unified evaluation before generating compact slice tables.",
    )
    parser.add_argument("--num", type=int, default=500, help="Number of samples for --run-eval")
    parser.add_argument("--seed", type=int, default=42, help="Sampling seed for --run-eval")
    parser.add_argument(
        "--data",
        default="data/train_with_models_v2.json",
        help="Reasoning dataset path for --run-eval",
    )
    parser.add_argument(
        "--selector-report",
        default="outputs/selector/evaluation_results.json",
        help="Optional selector report to include in summary for --run-eval",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress logs")
    parser.add_argument(
        "--write-samples",
        action="store_true",
        help="Also write samples.jsonl in compact eval mode.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.run_eval:
        if not args.output_dir:
            raise SystemExit("--output-dir is required with --run-eval")
        summary = run_compact_eval(args)
        output_dir = PROJECT_ROOT / args.output_dir
    else:
        if not args.eval_dir:
            raise SystemExit("--eval-dir is required unless --run-eval is set")
        eval_dir = PROJECT_ROOT / args.eval_dir
        output_dir = PROJECT_ROOT / (args.output_dir or args.eval_dir)
        summary = read_json(eval_dir / "summary.json")

    table_paths = generate_slice_tables(summary, output_dir)
    overall = summary.get("overall", {}) or {}
    print(
        "slice summary: "
        f"final_answer_accuracy="
        f"{overall.get('final_answer_correct_count', 0)}/"
        f"{overall.get('total_samples', 0)}="
        f"{format_rate(overall.get('final_answer_accuracy'))}, "
        f"reasoning_success="
        f"{overall.get('reasoning_success_count', 0)}/"
        f"{overall.get('total_samples', 0)}="
        f"{format_rate(overall.get('reasoning_success_rate'))}"
    )
    print("artifacts:")
    for name, path in sorted(table_paths.items()):
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
