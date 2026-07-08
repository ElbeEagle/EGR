"""Generate a multi-evidence dry-run manifest for train_with_models v3."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.theorems_v2.v3_repair import V3DryRunRepairer, summarize_manifests


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "train_with_models_v2.json",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "v3_dry_run_manifest.jsonl",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=PROJECT_ROOT
        / "outputs"
        / "theorems_v2"
        / "v3_dry_run_summary.json",
    )
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    rows = [row for row in rows if row.get("models")]
    if args.limit is not None:
        rows = rows[: args.limit]

    repairer = V3DryRunRepairer()
    manifests = []
    for index, row in enumerate(rows, start=1):
        manifests.append(repairer.repair_row(row))
        if index % 500 == 0:
            print(f"processed {index}/{len(rows)}", file=sys.stderr)

    summary = summarize_manifests(manifests)
    summary["source_rows"] = len(
        json.loads(args.input.read_text(encoding="utf-8"))
    )
    summary["input"] = str(args.input)
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)

    args.manifest_output.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest_output.open("w", encoding="utf-8") as handle:
        for item in manifests:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
