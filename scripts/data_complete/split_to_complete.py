"""
将 train_with_models_v2.json 中 process 为空的题目分批，
保存为多个待补齐文件 (data/data_complete/to_complete_part_X.json)。

输出格式（便于后续由 LLM 补齐 process + models）：
{
  "_meta": {...},
  "samples": [
    {
      "id": 1,
      "text": "...",
      "fact_expressions": "...",
      "query_expressions": "...",
      "answer_expressions": "..."
    },
    ...
  ]
}
"""

import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "train_with_models_v2.json"
OUT_DIR = ROOT / "data" / "data_complete"
NUM_PARTS = 10


def main() -> None:
    with open(SRC, "r", encoding="utf-8") as f:
        data = json.load(f)

    empty_proc = [x for x in data if not x.get("process", "").strip()]
    proc_yes_models_no = [
        x for x in data if x.get("process", "").strip() and not x.get("models")
    ]

    print(f"总题目数: {len(data)}")
    print(f"process 为空: {len(empty_proc)}")
    print(f"process 非空但 models 为空: {len(proc_yes_models_no)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    chunk_size = math.ceil(len(empty_proc) / NUM_PARTS)
    for i in range(NUM_PARTS):
        start = i * chunk_size
        end = min(start + chunk_size, len(empty_proc))
        chunk = empty_proc[start:end]
        if not chunk:
            break

        samples = [
            {
                "id": x["id"],
                "text": x["text"],
                "fact_expressions": x["fact_expressions"],
                "query_expressions": x["query_expressions"],
                "answer_expressions": x["answer_expressions"],
            }
            for x in chunk
        ]

        out_path = OUT_DIR / f"to_complete_part_{i+1}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "_meta": {
                        "part": i + 1,
                        "total_parts": NUM_PARTS,
                        "num_samples": len(samples),
                        "id_range": [samples[0]["id"], samples[-1]["id"]],
                        "task": "补齐 process（解题过程）与 models（80模型库中的模型id序列）",
                    },
                    "samples": samples,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(
            f"  -> {out_path.name}: {len(samples)} 题, id [{samples[0]['id']}, {samples[-1]['id']}]"
        )

    if proc_yes_models_no:
        out_path = OUT_DIR / "to_complete_models_only.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "_meta": {
                        "task": "已有 process，仅需补齐 models",
                        "num_samples": len(proc_yes_models_no),
                    },
                    "samples": [
                        {
                            "id": x["id"],
                            "text": x["text"],
                            "fact_expressions": x["fact_expressions"],
                            "query_expressions": x["query_expressions"],
                            "answer_expressions": x["answer_expressions"],
                            "process": x["process"],
                        }
                        for x in proc_yes_models_no
                    ],
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"  -> {out_path.name}: {len(proc_yes_models_no)} 题 (仅 models)")


if __name__ == "__main__":
    main()
