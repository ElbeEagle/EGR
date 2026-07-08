"""Evaluate expanded v2 apply coverage and export conservative repairs."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.theorems_v2.applicator import ApplicatorV2
from src.theorems_v2.complete_library import SupportLevel
from src.theorems_v2.expanded_correction import ExpandedSequenceCorrector
from src.theorems_v2.expanded_library import ExpandedTheoremLibraryV2
from src.theorems_v2.expanded_raw_adapter import ExpandedRawFactAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "train_with_models_v2.json",
    )
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--repairs-output", type=Path)
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    rows = [
        row
        for row in rows
        if row.get("models") and str(row.get("process") or "").strip()
    ]
    adapter = ExpandedRawFactAdapter()
    library = ExpandedTheoremLibraryV2()
    applicator = ApplicatorV2()
    corrector = ExpandedSequenceCorrector(library, applicator)

    bare = Counter()
    corrected = Counter()
    operations = Counter()
    full_bare = 0
    full_corrected = 0
    repairs = []
    unparsed = 0
    adapter_errors = 0

    for row in rows:
        adaptation = adapter.adapt(
            row.get("fact_expressions", ""),
            row.get("query_expressions", ""),
        )
        unparsed += len(adaptation.unparsed_facts)
        adapter_errors += len(adaptation.errors)
        state = adaptation.state
        bare_statuses = []
        for model_id in row["models"]:
            capability = library.get_capability(model_id)
            if capability.support_level == SupportLevel.SPECIFICATION_ONLY:
                status = "SPECIFICATION_ONLY"
            else:
                result = applicator.apply(library.get_model(model_id), state)
                status = result.status.value
                if result.state_after is not None:
                    state = result.state_after
            bare[status] += 1
            bare_statuses.append(status)
        if all(
            status in {"APPLIED", "ALREADY_KNOWN"}
            for status in bare_statuses
        ):
            full_bare += 1

        repair = corrector.repair(row["models"], adaptation.state)
        corrected.update(step.status for step in repair.trace)
        operations.update(operation.operation for operation in repair.operations)
        if repair.trace and all(
            step.status in {"APPLIED", "ALREADY_KNOWN"}
            for step in repair.trace
        ):
            full_corrected += 1
        if repair.operations or repair.branches:
            repairs.append(
                {
                    "id": row.get("id"),
                    "original_models": row["models"],
                    "repaired_models": list(repair.repaired_sequence),
                    "branches": [list(branch) for branch in repair.branches],
                    "operations": [
                        {
                            "operation": operation.operation,
                            "index": operation.index,
                        }
                        for operation in repair.operations
                    ],
                    "issues": [issue.kind.value for issue in repair.issues],
                    "confidence": repair.confidence,
                }
            )

    total_steps = sum(bare.values())
    concrete_steps = total_steps - bare["SPECIFICATION_ONLY"]
    summary = {
        "total_rows": len(rows),
        "original_steps": total_steps,
        "concrete_model_count": len(library.get_executable_models()),
        "bare_statuses": dict(bare),
        "bare_all_step_apply_rate": (
            bare["APPLIED"] + bare["ALREADY_KNOWN"]
        ) / total_steps,
        "bare_concrete_step_apply_rate": (
            bare["APPLIED"] + bare["ALREADY_KNOWN"]
        ) / concrete_steps,
        "bare_fully_executable_rows": full_bare,
        "bare_fully_executable_rate": full_bare / len(rows),
        "corrected_statuses": dict(corrected),
        "corrected_operations": dict(operations),
        "corrected_fully_executable_rows": full_corrected,
        "corrected_fully_executable_rate": full_corrected / len(rows),
        "repair_artifact_rows": len(repairs),
        "unparsed_fact_atoms": unparsed,
        "adapter_errors": adapter_errors,
    }
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    print(rendered)

    if args.summary_output:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        args.summary_output.write_text(rendered + "\n", encoding="utf-8")
    if args.repairs_output:
        args.repairs_output.parent.mkdir(parents=True, exist_ok=True)
        with args.repairs_output.open("w", encoding="utf-8") as handle:
            for repair in repairs:
                handle.write(json.dumps(repair, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
