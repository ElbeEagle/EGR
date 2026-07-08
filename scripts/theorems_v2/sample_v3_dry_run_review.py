"""Create a stratified human-review sample from the v3 dry-run manifest."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


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
        "--output",
        type=Path,
        default=Path("outputs/theorems_v2/v3_review_sample.jsonl"),
    )
    parser.add_argument("--per-bucket", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260703)
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    source = {str(row.get("id")): row for row in rows}
    manifests = [
        json.loads(line)
        for line in args.manifest.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    buckets = defaultdict(list)
    for item in manifests:
        for operation in (
            item["observed_operations"] + item["executable_operations"]
        ):
            if operation["operation"] == "replace_misaligned_model":
                detail = f"{operation['before']}->{operation['after']}"
            else:
                detail = str(
                    operation.get("consumer")
                    or operation.get("before")
                    or ""
                )
            key = f"operation:{operation['operation']}:{detail}"
            buckets[key].append((item, operation, None))
        for flag in item["semantic_flags"]:
            key = f"semantic:{flag['model_id']}:{flag['status']}"
            buckets[key].append((item, None, flag))

    rng = random.Random(args.seed)
    selected = []
    for bucket in sorted(buckets):
        candidates = buckets[bucket]
        sample = (
            candidates
            if len(candidates) <= args.per_bucket
            else rng.sample(candidates, args.per_bucket)
        )
        for item, operation, flag in sample:
            row = source.get(str(item["id"]), {})
            selected.append(
                {
                    "bucket": bucket,
                    "id": item["id"],
                    "text": row.get("text", ""),
                    "fact_expressions": row.get("fact_expressions", ""),
                    "process": row.get("process", ""),
                    "original_models": item["original_models"],
                    "models_v3_observed": item["models_v3_observed"],
                    "models_v3_executable": item["models_v3_executable"],
                    "operation": operation,
                    "semantic_flag": flag,
                    "quality_candidate": item["quality_candidate"],
                    "review_decision": None,
                    "review_note": "",
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for item in selected:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(
        json.dumps(
            {
                "bucket_count": len(buckets),
                "sample_rows": len(selected),
                "per_bucket": args.per_bucket,
                "seed": args.seed,
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
