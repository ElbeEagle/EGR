"""
Unified evaluation protocol for EGR reasoning runs.

This module is intentionally a reporting layer. It consumes existing
ReasoningResult objects and dataset samples, then emits auditable sample-level
records plus paper-table friendly summaries.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


SCHEMA_VERSION = "egr_eval_protocol_v1"


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def detect_curve_type(facts: str) -> str:
    fl = (facts or "").lower()
    if "ellipse" in fl:
        return "Ellipse"
    if "hyperbola" in fl:
        return "Hyperbola"
    if "parabola" in fl:
        return "Parabola"
    if "circle" in fl:
        return "Circle"
    return "Other"


def detect_query_type(query: str) -> str:
    ql = (query or "").lower()
    if "eccentricity" in ql:
        return "Eccentricity"
    if "equation" in ql or "expression" in ql:
        return "Equation"
    if "length" in ql:
        return "Length"
    if "coordinate" in ql:
        return "Coordinate"
    if "distance" in ql:
        return "Distance"
    if "area" in ql:
        return "Area"
    if "range" in ql:
        return "Range"
    return "Value"


def normalize_reasoning_failure(reason: Optional[str]) -> str:
    text = str(reason or "").strip()
    lower = text.lower()
    if not text:
        return "unknown"
    if "fatal error" in lower or "exception" in lower:
        return "exception"
    if "no applicable model" in lower:
        return "no_model"
    if "max steps" in lower:
        return "max_steps"
    if "apply failed" in lower:
        return "apply_failed"
    return "other"


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    try:
        return float(value)
    except Exception:
        return str(value)


def _string_or_none(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _extract_top_ids(trace_step: Mapping[str, Any]) -> List[int]:
    candidates = trace_step.get("candidates") or trace_step.get("top_k_candidates") or []
    top_ids: List[int] = []
    if isinstance(candidates, list):
        for candidate in candidates:
            if not isinstance(candidate, Mapping):
                continue
            model_id = candidate.get("model_id")
            if model_id is None:
                continue
            try:
                top_ids.append(int(model_id))
            except (TypeError, ValueError):
                continue
    if not top_ids:
        for key in ("selected_model_id", "predicted_model_id", "model_id"):
            model_id = trace_step.get(key)
            if model_id is None:
                continue
            try:
                top_ids.append(int(model_id))
                break
            except (TypeError, ValueError):
                pass
    return top_ids


def compute_trace_selection_metrics(
    trace: Iterable[Mapping[str, Any]],
    label_sequence: Iterable[Any],
) -> Dict[str, Any]:
    labels: List[int] = []
    for label in label_sequence or []:
        try:
            labels.append(int(label))
        except (TypeError, ValueError):
            continue

    steps: List[Dict[str, Any]] = []
    total = 0
    top1_hits = 0
    top3_hits = 0
    top5_hits = 0

    for index, (trace_step, label) in enumerate(zip(trace or [], labels), start=1):
        top_ids = _extract_top_ids(trace_step)
        if not top_ids:
            continue
        total += 1
        top1 = label in top_ids[:1]
        top3 = label in top_ids[:3]
        top5 = label in top_ids[:5]
        top1_hits += int(top1)
        top3_hits += int(top3)
        top5_hits += int(top5)
        steps.append(
            {
                "step": index,
                "label_model_id": label,
                "top_model_ids": top_ids[:5],
                "top1_hit": top1,
                "top3_hit": top3,
                "top5_hit": top5,
            }
        )

    return {
        "label_sequence": labels,
        "evaluated_steps": total,
        "top1_hits": top1_hits,
        "top3_hits": top3_hits,
        "top5_hits": top5_hits,
        "top1_accuracy": safe_div(top1_hits, total),
        "top3_accuracy": safe_div(top3_hits, total),
        "top5_accuracy": safe_div(top5_hits, total),
        "step_details": steps,
    }


def build_sample_report(
    sample: Mapping[str, Any],
    result: Any,
    final_answer_correct: bool,
    exception: Optional[BaseException] = None,
) -> Dict[str, Any]:
    facts = sample.get("fact_expressions", "")
    query = sample.get("query_expressions", "")
    expected_answer = sample.get("answer_expressions")
    reasoning_success = bool(result is not None and getattr(result, "success", False))
    predicted_answer = getattr(result, "answer", None) if result is not None else None
    raw_reason = getattr(result, "failure_reason", None) if result is not None else None

    if exception is not None:
        raw_reason = f"exception: {exception}"

    if final_answer_correct:
        failure_reason = None
    elif reasoning_success:
        failure_reason = "answer_mismatch"
    else:
        failure_reason = normalize_reasoning_failure(raw_reason)

    trace = getattr(result, "reasoning_trace", []) if result is not None else []
    label_sequence = sample.get("models") or []
    theorem_selection = compute_trace_selection_metrics(trace, label_sequence)

    return {
        "schema_version": SCHEMA_VERSION,
        "sample_id": sample.get("id", sample.get("sample_id")),
        "facts": facts,
        "query": query,
        "expected_answer": _string_or_none(expected_answer),
        "predicted_answer": _string_or_none(predicted_answer),
        "final_answer_correct": bool(final_answer_correct),
        "reasoning_success": reasoning_success,
        "failure_reason": failure_reason,
        "reasoning_failure_reason": (
            None if reasoning_success else normalize_reasoning_failure(raw_reason)
        ),
        "raw_failure_reason": _string_or_none(raw_reason),
        "applied_model_sequence": list(getattr(result, "model_sequence", []) or []),
        "applied_model_names": list(getattr(result, "model_names", []) or []),
        "model_level_trace": _json_safe(trace),
        "theorem_selection": theorem_selection,
        "curve_type": detect_curve_type(str(facts)),
        "query_type": detect_query_type(str(query)),
        "num_steps": int(getattr(result, "num_steps", 0) or 0) if result is not None else 0,
        "elapsed_time": float(getattr(result, "elapsed_time", 0.0) or 0.0)
        if result is not None
        else 0.0,
    }


def _empty_bucket() -> Dict[str, Any]:
    return {
        "total_samples": 0,
        "reasoning_success_count": 0,
        "final_answer_correct_count": 0,
        "elapsed_time_sum": 0.0,
        "theorem_selection_labeled_steps": 0,
        "theorem_selection_top1_hits": 0,
        "theorem_selection_top3_hits": 0,
        "theorem_selection_top5_hits": 0,
    }


def _add_to_bucket(bucket: MutableMapping[str, Any], sample: Mapping[str, Any]) -> None:
    selection = sample.get("theorem_selection", {}) or {}
    bucket["total_samples"] += 1
    bucket["reasoning_success_count"] += int(bool(sample.get("reasoning_success")))
    bucket["final_answer_correct_count"] += int(bool(sample.get("final_answer_correct")))
    bucket["elapsed_time_sum"] += float(sample.get("elapsed_time") or 0.0)
    bucket["theorem_selection_labeled_steps"] += int(selection.get("evaluated_steps") or 0)
    bucket["theorem_selection_top1_hits"] += int(selection.get("top1_hits") or 0)
    bucket["theorem_selection_top3_hits"] += int(selection.get("top3_hits") or 0)
    bucket["theorem_selection_top5_hits"] += int(selection.get("top5_hits") or 0)


def _finalize_bucket(bucket: Mapping[str, Any]) -> Dict[str, Any]:
    total = int(bucket.get("total_samples", 0) or 0)
    success = int(bucket.get("reasoning_success_count", 0) or 0)
    correct = int(bucket.get("final_answer_correct_count", 0) or 0)
    labeled = int(bucket.get("theorem_selection_labeled_steps", 0) or 0)
    top1 = int(bucket.get("theorem_selection_top1_hits", 0) or 0)
    top3 = int(bucket.get("theorem_selection_top3_hits", 0) or 0)
    top5 = int(bucket.get("theorem_selection_top5_hits", 0) or 0)
    return {
        "total_samples": total,
        "reasoning_success_count": success,
        "reasoning_success_rate": safe_div(success, total),
        "final_answer_correct_count": correct,
        "final_answer_accuracy": safe_div(correct, total),
        "answer_accuracy_among_successful_reasoning": safe_div(correct, success),
        "avg_elapsed_time": safe_div(float(bucket.get("elapsed_time_sum", 0.0) or 0.0), total),
        "theorem_selection_labeled_steps": labeled,
        "theorem_selection_top1_hits": top1,
        "theorem_selection_top3_hits": top3,
        "theorem_selection_top5_hits": top5,
        "theorem_selection_top1_accuracy": safe_div(top1, labeled),
        "theorem_selection_top3_accuracy": safe_div(top3, labeled),
        "theorem_selection_top5_accuracy": safe_div(top5, labeled),
    }


def _finalize_grouped(grouped: Mapping[str, Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(key): _finalize_bucket(value) for key, value in sorted(grouped.items())}


def summarize_samples(samples: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    sample_list = list(samples)
    overall = _empty_bucket()
    by_curve_type: Dict[str, Dict[str, Any]] = defaultdict(_empty_bucket)
    by_query_type: Dict[str, Dict[str, Any]] = defaultdict(_empty_bucket)
    by_failure_reason: Dict[str, Dict[str, Any]] = defaultdict(_empty_bucket)
    by_model_id: Dict[str, Dict[str, Any]] = defaultdict(_empty_bucket)
    failure_reasons = Counter()
    reasoning_failure_reasons = Counter()
    model_id_usage = Counter()
    model_id_failure_distribution: Dict[str, Counter] = defaultdict(Counter)

    for sample in sample_list:
        _add_to_bucket(overall, sample)
        _add_to_bucket(by_curve_type[str(sample.get("curve_type") or "Unknown")], sample)
        _add_to_bucket(by_query_type[str(sample.get("query_type") or "Unknown")], sample)

        failure_reason = sample.get("failure_reason")
        if failure_reason:
            failure_reasons[str(failure_reason)] += 1
            _add_to_bucket(by_failure_reason[str(failure_reason)], sample)

        reasoning_failure_reason = sample.get("reasoning_failure_reason")
        if reasoning_failure_reason:
            reasoning_failure_reasons[str(reasoning_failure_reason)] += 1

        applied_models = [str(mid) for mid in sample.get("applied_model_sequence", []) or []]
        seen_models = set(applied_models)
        for model_id in applied_models:
            model_id_usage[model_id] += 1
        for model_id in seen_models:
            _add_to_bucket(by_model_id[model_id], sample)
            if failure_reason:
                model_id_failure_distribution[model_id][str(failure_reason)] += 1

    finalized_overall = _finalize_bucket(overall)
    finalized_overall["elapsed_time_sum"] = round(float(overall["elapsed_time_sum"]), 6)

    return {
        "overall": finalized_overall,
        "theorem_selection": {
            "labeled_steps": finalized_overall["theorem_selection_labeled_steps"],
            "top1_hits": finalized_overall["theorem_selection_top1_hits"],
            "top3_hits": finalized_overall["theorem_selection_top3_hits"],
            "top5_hits": finalized_overall["theorem_selection_top5_hits"],
            "top1_accuracy": finalized_overall["theorem_selection_top1_accuracy"],
            "top3_accuracy": finalized_overall["theorem_selection_top3_accuracy"],
            "top5_accuracy": finalized_overall["theorem_selection_top5_accuracy"],
        },
        "by_curve_type": _finalize_grouped(by_curve_type),
        "by_query_type": _finalize_grouped(by_query_type),
        "by_failure_reason": _finalize_grouped(by_failure_reason),
        "failure_reason_distribution": dict(sorted(failure_reasons.items())),
        "reasoning_failure_reason_distribution": dict(sorted(reasoning_failure_reasons.items())),
        "model_id_usage": {
            str(k): v for k, v in sorted(model_id_usage.items(), key=lambda item: int(item[0]))
        },
        "by_model_id": _finalize_grouped(by_model_id),
        "model_id_failure_distribution": {
            str(model_id): dict(sorted(counter.items()))
            for model_id, counter in sorted(
                model_id_failure_distribution.items(), key=lambda item: int(item[0])
            )
        },
    }


def selector_summary_from_report(report: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
    if not report:
        return None
    total = int(report.get("total_predictions") or 0)
    top1 = int(report.get("top1_hits") or 0)
    top3 = int(report.get("top3_hits") or 0)
    top5 = int(report.get("top5_hits") or 0)
    return {
        "source": "selector_evaluation_results",
        "total_predictions": total,
        "top1_hits": top1,
        "top3_hits": top3,
        "top5_hits": top5,
        "top1_accuracy": safe_div(top1, total),
        "top3_accuracy": safe_div(top3, total),
        "top5_accuracy": safe_div(top5, total),
    }


def build_eval_report(
    samples: List[Mapping[str, Any]],
    run_metadata: Optional[Mapping[str, Any]] = None,
    selector_report: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    summary = summarize_samples(samples)
    selector_summary = selector_summary_from_report(selector_report)
    if selector_summary is not None:
        summary["external_selector_report"] = selector_summary

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run": dict(run_metadata or {}),
        "summary": summary,
        "samples": samples,
    }


def summary_rows(summary: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    def add_row(group: str, value: str, metrics: Mapping[str, Any]) -> None:
        rows.append(
            {
                "group": group,
                "value": value,
                "total_samples": metrics.get("total_samples", 0),
                "reasoning_success_count": metrics.get("reasoning_success_count", 0),
                "reasoning_success_rate": metrics.get("reasoning_success_rate", 0.0),
                "final_answer_correct_count": metrics.get("final_answer_correct_count", 0),
                "final_answer_accuracy": metrics.get("final_answer_accuracy", 0.0),
                "answer_accuracy_among_successful_reasoning": metrics.get(
                    "answer_accuracy_among_successful_reasoning", 0.0
                ),
                "theorem_selection_labeled_steps": metrics.get(
                    "theorem_selection_labeled_steps", 0
                ),
                "theorem_selection_top1_accuracy": metrics.get(
                    "theorem_selection_top1_accuracy", 0.0
                ),
                "theorem_selection_top3_accuracy": metrics.get(
                    "theorem_selection_top3_accuracy", 0.0
                ),
                "theorem_selection_top5_accuracy": metrics.get(
                    "theorem_selection_top5_accuracy", 0.0
                ),
            }
        )

    add_row("overall", "all", summary.get("overall", {}))
    for group_name in ("by_curve_type", "by_query_type", "by_failure_reason", "by_model_id"):
        for value, metrics in (summary.get(group_name, {}) or {}).items():
            add_row(group_name, str(value), metrics)
    return rows


def write_eval_artifacts(report: Mapping[str, Any], output_dir: str | Path) -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    report_path = out / "report.json"
    summary_path = out / "summary.json"
    samples_path = out / "samples.jsonl"
    csv_path = out / "summary.csv"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(report.get("summary", {}), f, indent=2, ensure_ascii=False)
    with samples_path.open("w", encoding="utf-8") as f:
        for sample in report.get("samples", []) or []:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    rows = summary_rows(report.get("summary", {}))
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
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {
        "report": str(report_path),
        "summary_json": str(summary_path),
        "samples_jsonl": str(samples_path),
        "summary_csv": str(csv_path),
    }
