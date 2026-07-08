"""Randomly sample problems whose theorem sequence is non-empty.

The sample is written both as readable Markdown and as structured JSON.  A
local ``random.Random`` instance makes the result reproducible without
changing global random state.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.theorems_v2.catalog import THEOREM_CATALOG
from src.theorems_v2.replay_benchmark import ReplayBenchmarkV3


def sample_rows(
    rows: Iterable[dict[str, Any]],
    sequence_field: str,
    sample_size: int,
    seed: int,
) -> tuple[list[dict[str, Any]], int]:
    """Return a stable random sample and the eligible population size."""
    eligible = [
        (index, row)
        for index, row in enumerate(rows)
        if row.get(sequence_field)
    ]
    if sample_size < 1:
        raise ValueError("sample_size must be positive")
    if sample_size > len(eligible):
        raise ValueError(
            f"requested {sample_size} rows, but only {len(eligible)} "
            f"have a non-empty {sequence_field}"
        )

    sampled = random.Random(seed).sample(eligible, sample_size)
    sampled.sort(key=lambda item: item[0])
    result = []
    for index, row in sampled:
        item = dict(row)
        item["dataset_index"] = index
        result.append(item)
    return result, len(eligible)


def load_model_names(path: Path) -> dict[int, str]:
    mapping = json.loads(path.read_text(encoding="utf-8"))
    return {int(model_id): name for name, model_id in mapping.items()}


def review_record(
    row: dict[str, Any],
    sequence_field: str,
    model_names: dict[int, str],
    sample_number: int,
    replay_result: dict[str, Any] | None = None,
    benchmark: ReplayBenchmarkV3 | None = None,
) -> dict[str, Any]:
    sequence = list(row[sequence_field])
    statuses = (
        replay_result.get("step_statuses", []) if replay_result else []
    )
    support_model_ids = (
        replay_result.get("support_model_ids", []) if replay_result else []
    )
    theorem_steps = []
    for index, model_id in enumerate(sequence):
        requirement = THEOREM_CATALOG.get(model_id)
        capability = (
            benchmark.library.get_capability(model_id)
            if benchmark is not None
            else None
        )
        theorem_steps.append(
            {
                "step": index + 1,
                "model_id": model_id,
                "name": (
                    requirement.name
                    if requirement
                    else model_names.get(model_id, f"Unknown({model_id})")
                ),
                "category": requirement.category if requirement else None,
                "formula": requirement.formula if requirement else None,
                "required_types": (
                    list(requirement.required_types) if requirement else []
                ),
                "required_predicates": (
                    list(requirement.required_predicates)
                    if requirement
                    else []
                ),
                "produced_predicates": (
                    list(requirement.produced_predicates)
                    if requirement
                    else []
                ),
                "dependencies": (
                    [
                        THEOREM_CATALOG[dependency].name
                        for dependency in requirement.dependencies
                    ]
                    if requirement
                    else []
                ),
                "applicator_support": (
                    capability.support_level.value if capability else None
                ),
                "application_status": (
                    statuses[index] if index < len(statuses) else None
                ),
                "inserted_support_models": (
                    [
                        THEOREM_CATALOG[support_id].name
                        for support_id in support_model_ids[index]
                    ]
                    if index < len(support_model_ids)
                    else []
                ),
            }
        )

    applicator_result = None
    if replay_result is not None:
        applicator_result = {
            "can_complete_sequence": replay_result["sequence_success"],
            "step_statuses": list(replay_result["step_statuses"]),
            "first_failure": replay_result["first_failure"],
            "initial_goal": replay_result["initial_goal"],
            "final_goal": replay_result["goal"],
            "answer_correct": (
                replay_result["goal"]["status"] == "ANSWER_CORRECT"
            ),
            "goal_progress": replay_result["goal_progress"],
            "selector_usable": replay_result["selector_usable"],
        }
    return {
        "sample_number": sample_number,
        "dataset_index": row["dataset_index"],
        "id": row.get("id"),
        "text": row.get("text", ""),
        "fact_expressions": row.get("fact_expressions", ""),
        "query_expressions": row.get("query_expressions", ""),
        "answer_expressions": row.get("answer_expressions", ""),
        "process": row.get("process", ""),
        "sequence_field": sequence_field,
        "theorem_sequence": sequence,
        "theorem_names": [
            model_names.get(model_id, f"Unknown({model_id})")
            for model_id in sequence
        ],
        "theorem_content_sequence": theorem_steps,
        "applicator_result": applicator_result,
        "models_v3_observed": row.get("models_v3_observed", []),
        "models_v3_executable": row.get("models_v3_executable", []),
        "model_actions_v3": row.get("model_actions_v3", []),
        "v3_quality": row.get("v3_quality"),
    }


def render_markdown(
    records: list[dict[str, Any]],
    input_path: Path,
    eligible_rows: int,
    sequence_field: str,
    seed: int,
) -> str:
    complete_rows = sum(
        bool(item["applicator_result"]["can_complete_sequence"])
        for item in records
    )
    correct_rows = sum(
        bool(item["applicator_result"]["answer_correct"])
        for item in records
    )
    lines = [
        "# 随机抽取的非空定理序列题目",
        "",
        f"- 数据文件：`{input_path}`",
        f"- 序列字段：`{sequence_field}`",
        f"- 非空候选数：{eligible_rows}",
        f"- 抽样数：{len(records)}",
        f"- 随机种子：{seed}",
        f"- Applicator 完整执行：{complete_rows}/{len(records)}",
        f"- 最终答案正确：{correct_rows}/{len(records)}",
        "",
    ]
    for item in records:
        applicator = item["applicator_result"]
        complete_display = (
            "是（完整执行）"
            if applicator["can_complete_sequence"]
            else "否（存在失败步骤）"
        )
        answer_display = (
            "正确" if applicator["answer_correct"] else "未得到正确答案"
        )
        lines.extend(
            [
                f"## {item['sample_number']}. 题目 ID {item['id']}",
                "",
                f"- 数据索引：{item['dataset_index']}",
                f"- V3 质量：{item['v3_quality']}",
                "",
                "### 题目",
                "",
                item["text"] or "（空）",
                "",
                "### 形式化信息",
                "",
                f"- 已知：`{item['fact_expressions']}`",
                f"- 查询：`{item['query_expressions']}`",
                f"- 答案：`{item['answer_expressions']}`",
                "",
                "### 解题过程",
                "",
                f"${item['process']}$" if item["process"] else "（空）",
                "",
                "### 定理内容序列",
                "",
            ]
        )
        for theorem in item["theorem_content_sequence"]:
            required_types = ", ".join(theorem["required_types"]) or "无"
            required = ", ".join(theorem["required_predicates"]) or "无"
            produced = ", ".join(theorem["produced_predicates"]) or "无"
            dependencies = " → ".join(theorem["dependencies"]) or "无"
            support = theorem["applicator_support"] or "UNKNOWN"
            status = theorem["application_status"] or "NOT_EVALUATED"
            lines.extend(
                [
                    f"#### 步骤 {theorem['step']}：{theorem['name']}",
                    "",
                    f"- 具体公式/规则：${theorem['formula']}$",
                    f"- 类别：`{theorem['category']}`",
                    f"- 所需对象类型：`{required_types}`",
                    f"- 所需信息：`{required}`",
                    f"- 产出信息：`{produced}`",
                    f"- 目录依赖：`{dependencies}`",
                    f"- Applicator 支持：`{support}`",
                    f"- 本题执行状态：`{status}`",
                    "",
                ]
            )
        final_goal = applicator["final_goal"]
        lines.extend(
            [
                "### 当前 Applicator 回放结果",
                "",
                f"- 能否完整执行：**{complete_display}**",
                f"- 最终答案：**{answer_display}**",
                f"- 初始目标状态：`{applicator['initial_goal']['status']}`",
                f"- 最终目标状态：`{final_goal['status']}`",
                f"- Applicator 实际值：`{final_goal['actual_value']}`",
                f"- 标注期望值：`{final_goal['expected_value']}`",
                f"- 结果说明：{final_goal['detail'] or '无'}",
            ]
        )
        if applicator["first_failure"] is not None:
            failure = applicator["first_failure"]
            lines.extend(
                [
                    f"- 首个失败步骤：第 {failure['index'] + 1} 步",
                    f"- 失败状态：`{failure['status']}`",
                    "- 缺失谓词：`"
                    + (", ".join(failure["missing_predicates"]) or "无")
                    + "`",
                    "- 缺失对象类型：`"
                    + (", ".join(failure["missing_types"]) or "无")
                    + "`",
                ]
            )
        lines.extend(
            [
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Randomly sample problems with non-empty theorem sequences."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "train_with_models_v3_candidate.json",
    )
    parser.add_argument(
        "--sequence-field",
        choices=("models", "models_v3_observed", "models_v3_executable"),
        default="models_v3_executable",
    )
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20260708)
    parser.add_argument(
        "--model-ids",
        type=Path,
        default=PROJECT_ROOT / "model" / "conic_model_ids.json",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "random_50_nonempty_sequences.md",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "random_50_nonempty_sequences.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = json.loads(args.input.read_text(encoding="utf-8"))
    sampled, eligible_rows = sample_rows(
        rows, args.sequence_field, args.count, args.seed
    )
    names = load_model_names(args.model_ids)
    benchmark = ReplayBenchmarkV3(assisted_apply=False)
    records = []
    for number, row in enumerate(sampled, start=1):
        replay_result = benchmark.evaluate_row(
            row,
            sequence_field=args.sequence_field,
            export_trajectory=False,
        )
        records.append(
            review_record(
                row,
                args.sequence_field,
                names,
                number,
                replay_result=replay_result,
                benchmark=benchmark,
            )
        )

    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(
        render_markdown(
            records,
            args.input,
            eligible_rows,
            args.sequence_field,
            args.seed,
        ),
        encoding="utf-8",
    )
    args.json_output.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "dataset_rows": len(rows),
                "eligible_rows": eligible_rows,
                "sample_rows": len(records),
                "sequence_field": args.sequence_field,
                "seed": args.seed,
                "markdown_output": str(args.markdown_output),
                "json_output": str(args.json_output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
