# Theorem V2 全目录、纠错与辅助求解实现

**日期**: 2026-07-01  
**代码入口**: `src/theorems_v2/full.py`

## 1. 完整性的定义

当前实现区分两种完成度：

1. `SPECIFICATION coverage = 80/80`：每个模型都有名称、公式、类别、输入需求、输出类型、依赖和应用模式。
2. `CONCRETE executor coverage = 17/80`：当前高频模型 `0-13,21,29,75` 具有可产生 `StateDelta` 的数学执行器。

其余 63 个模型标记为 `SPECIFICATION_ONLY`。纠错器会明确报告该状态，不会把它混成 `NO_MATCH`，也不会假装应用成功。

## 2. 模块

| 模块 | 责任 |
|---|---|
| `catalog.py` | 80 个模型的 v2 需求目录和依赖图 |
| `complete_library.py` | 统一暴露 80 个模型及 support level |
| `raw_adapter.py` | `fact_expressions/query` 到 typed information state |
| `correction.py` | ID 纠错、依赖插入/重排、分支和能力缺口识别 |
| `assistant.py` | theorem 固定点闭包、一元线性约束闭包、QueryGoal 检查 |
| `pipeline.py` | 串联解析、纠错、执行、辅助闭包和目标检查 |
| `audit.py` | 数据集级工程指标 |

## 3. 纠错边界

允许自动修复：

- 状态证据唯一支持另一个方向模型时替换 ID。
- 已知依赖模型可唯一应用时插入依赖。
- Model 2 在 Model 29 前且缺准线时移动依赖。
- 单椭圆的 `3 -> 4` 标记为 axis branch。
- specification-only、no-match、ambiguous 分开报告。

禁止自动修复：

- 放宽数学 precondition 以适配错误标签。
- 在多个绑定中随意选择一个。
- 为未知方向、点名或曲线名设置默认值。
- 把 specification-only 当成已执行定理。

## 4. 使用方式

```python
from src.theorems_v2.full import TheoremPipelineV2

result = TheoremPipelineV2().run(
    fact_expressions=facts,
    query_expressions=query,
    model_sequence=models,
)

print(result.repair.repaired_sequence)
print(result.repair.issues)
print(result.goals_satisfied)
```

数据集审计：

```bash
python scripts/theorems_v2/audit_dataset.py \
  --input data/train_with_models_v2.json
```

## 5. 2026-07-01 基线

输入：7,757 题，其中 5,355 题同时含 model sequence 和文字过程。

原始步骤：20,212；纠错后额外插入 150 个依赖步骤。

```text
APPLIED                3,858
SPECIFICATION_ONLY     8,017
NO_MATCH               8,441
AMBIGUOUS_BINDING         46

方向模型替换              184
依赖插入                  150
依赖重排                  519
分支样本                  111
```

Raw adapter 显式保留了 11,653 个尚未结构化的 fact atom，并记录 46 个表达式解析错误。

这些数字是工程基线，不是定理序列错误率。多个问题会重叠；`SPECIFICATION_ONLY` 主要表示后续 concrete executor 的开发工作量。

## 6. 下一阶段

1. 按数据频率和 `SPECIFICATION_ONLY` 数量实现下一批 concrete executors。
2. 优先补坐标/距离、Vieta、向量和判别式等通用模型族。
3. 扩展 raw adapter 对 `Abs/LineSegmentOf/VectorOf/Intersection/Negation` 的支持。
4. 接入 SymPy 后端，处理符号分母、根式、参数不等式和非线性约束。
5. 对 branch trajectories 输出多个可信后续状态，而不是强制单路径。
