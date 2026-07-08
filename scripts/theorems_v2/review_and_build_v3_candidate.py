"""Apply reviewed dry-run decisions and build a v3 candidate dataset."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


SEMANTIC_IDS = {63, 64, 68, 69, 70, 71, 77, 79}


def classify_semantic_action(model_id: int, process: str):
    compact = re.sub(r"\s+", "", process or "")
    if model_id == 63:
        if any(cue in compact for cue in ("基本不等式", "均值不等式", "≥", ">=", "geqslant", "geq")):
            return "tactic.basic_inequality_bound", "reviewed_text_cue"
    elif model_id == 64:
        if any(cue in compact for cue in ("当且仅当", "等号成立", "取等", "时等号")):
            return "tactic.inequality_equality_condition", "reviewed_text_cue"
    elif model_id == 68:
        if any(cue in compact for cue in ("中位线", "中点", "一半", "frac{1}{2}")):
            return "geometry.midpoint_midline_relation", "reviewed_text_cue"
    elif model_id == 69:
        if any(cue in compact for cue in ("梯形", "中位线", "上下底")):
            return "geometry.trapezoid_midline_relation", "reviewed_text_cue"
    elif model_id == 70:
        if any(cue in compact for cue in ("内切圆", "内心", "内切", "角平分线")):
            return "geometry.incircle_incenter_relation", "reviewed_text_cue"
    elif model_id == 71:
        if any(cue in compact for cue in ("面积", "等底", "等高", "S_", "S_{")):
            return "tactic.area_equivalence", "reviewed_text_cue"
    elif model_id == 77:
        if any(cue in compact for cue in ("齐次", "同除", "两边除", "除以a", "除以c", "无量纲")):
            return "tactic.dimensionless_homogenization", "reviewed_text_cue"
        if "e=" in compact and any(cue in compact for cue in ("a^{2}", "b^{2}", "c^{2}")):
            return "tactic.dimensionless_homogenization", "inferred_ratio_rewrite"
    elif model_id == 79:
        if any(cue in compact for cue in ("二次函数", "配方", "顶点")) or (
            any(cue in compact for cue in ("最大值", "最小值", "最值"))
            and any(cue in compact for cue in ("x^{2}", "y^{2}", "函数"))
        ):
            return "tactic.quadratic_extremum", "reviewed_text_cue"
        if any(
            cue in compact
            for cue in (
                "判别式",
                "triangle",
                "Delta",
                "有公共点",
                "恒有公共点",
                "有交点",
                "参数范围",
            )
        ):
            return "tactic.feasibility_by_discriminant", "reviewed_text_cue"
    return "unresolved.legacy_model_" + str(model_id), "needs_relabel"


def reviewed_manifest_item(item, source_row):
    reviewed = dict(item)
    reviewed["reviewed_operations"] = []
    for operation in item["observed_operations"]:
        decision = dict(operation)
        decision["review_decision"] = "approve_observed"
        decision["review_basis"] = (
            "stratified text audit plus unique typed sibling execution"
        )
        reviewed["reviewed_operations"].append(decision)
    for operation in item["executable_operations"]:
        decision = dict(operation)
        decision["review_decision"] = "approve_executable_only"
        decision["review_basis"] = (
            "transactional dependency chain unlocked consumer"
        )
        reviewed["reviewed_operations"].append(decision)

    process = str(source_row.get("process") or "")
    reviewed_semantics = []
    for flag in item["semantic_flags"]:
        action, basis = classify_semantic_action(flag["model_id"], process)
        reviewed_semantics.append(
            {
                **flag,
                "action_v3": action,
                "review_basis": basis,
                "review_decision": (
                    "map_to_namespaced_action"
                    if basis != "needs_relabel"
                    else "keep_legacy_unresolved"
                ),
                "selector_weight": 0,
            }
        )
    reviewed["reviewed_semantics"] = reviewed_semantics
    return reviewed


def build_candidate_row(row, manifest):
    output = dict(row)
    legacy = list(row.get("models") or [])
    output["models_legacy"] = legacy
    if manifest is None:
        output["models_v3_observed"] = legacy
        output["models_v3_executable"] = legacy
        output["model_actions_v3"] = []
        output["selector_weights_v3"] = []
        output["v3_quality"] = "unlabeled"
        return output

    observed = manifest["models_v3_observed"]
    executable = manifest["models_v3_executable"]
    semantics = {
        item["model_id"]: item
        for item in manifest["reviewed_semantics"]
    }
    actions = []
    weights = []
    for model_id in observed:
        semantic = semantics.get(model_id)
        if semantic is None:
            actions.append(f"theorem.{model_id}")
            weights.append(1)
        else:
            actions.append(semantic["action_v3"])
            weights.append(0)

    output["models"] = observed
    output["models_v3_observed"] = observed
    output["models_v3_executable"] = executable
    output["model_actions_v3"] = actions
    output["selector_weights_v3"] = weights
    output["v3_quality"] = manifest["quality_candidate"]
    output["v3_repair"] = {
        "observed_operations": manifest["observed_operations"],
        "executable_operations": manifest["executable_operations"],
        "semantic_review": manifest["reviewed_semantics"],
        "unparsed_fact_count": manifest["unparsed_fact_count"],
        "adapter_errors": manifest["adapter_errors"],
    }
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/train_with_models_v2.json"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("outputs/theorems_v2/v3_dry_run_manifest.jsonl"),
    )
    parser.add_argument(
        "--reviewed-manifest-output",
        type=Path,
        default=Path("outputs/theorems_v2/v3_reviewed_manifest.jsonl"),
    )
    parser.add_argument(
        "--candidate-output",
        type=Path,
        default=Path("data/train_with_models_v3_candidate.json"),
    )
    parser.add_argument(
        "--high-confidence-output",
        type=Path,
        default=Path("data/train_with_models_v3_high_confidence.json"),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("outputs/theorems_v2/v3_review_summary.json"),
    )
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    source = {str(row.get("id")): row for row in rows}
    manifests = [
        json.loads(line)
        for line in args.manifest.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    reviewed = [
        reviewed_manifest_item(
            item,
            source.get(str(item["id"]), {}),
        )
        for item in manifests
    ]
    by_id = {str(item["id"]): item for item in reviewed}
    candidate = [
        build_candidate_row(row, by_id.get(str(row.get("id"))))
        for row in rows
    ]
    high_confidence = [
        row
        for row in candidate
        if row.get("v3_quality") in {"A", "B"}
        and row.get("models_v3_observed")
    ]

    operation_decisions = Counter()
    semantic_actions = Counter()
    semantic_review_basis = Counter()
    for item in reviewed:
        for operation in item["reviewed_operations"]:
            operation_decisions[
                f"{operation['operation']}:{operation['review_decision']}"
            ] += 1
        for semantic in item["reviewed_semantics"]:
            semantic_actions[semantic["action_v3"]] += 1
            semantic_review_basis[semantic["review_basis"]] += 1

    summary = {
        "source_rows": len(rows),
        "rows_with_reviewed_models": len(reviewed),
        "candidate_rows": len(candidate),
        "high_confidence_rows": len(high_confidence),
        "operation_decisions": dict(operation_decisions),
        "semantic_actions": dict(semantic_actions),
        "semantic_review_basis": dict(semantic_review_basis),
        "changed_observed_rows": sum(
            item["original_models"] != item["models_v3_observed"]
            for item in reviewed
        ),
        "changed_executable_rows": sum(
            item["models_v3_observed"] != item["models_v3_executable"]
            for item in reviewed
        ),
    }

    args.reviewed_manifest_output.parent.mkdir(parents=True, exist_ok=True)
    with args.reviewed_manifest_output.open("w", encoding="utf-8") as handle:
        for item in reviewed:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    args.candidate_output.parent.mkdir(parents=True, exist_ok=True)
    args.candidate_output.write_text(
        json.dumps(candidate, ensure_ascii=False),
        encoding="utf-8",
    )
    args.high_confidence_output.write_text(
        json.dumps(high_confidence, ensure_ascii=False),
        encoding="utf-8",
    )
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
