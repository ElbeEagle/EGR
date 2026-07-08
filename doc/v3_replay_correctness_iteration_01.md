# V3 正确性迭代 01：端到端回放基线

## 目标

以“定理序列可执行并得到正确答案”为核心指标，串联 V2 定理库、信息空间、applicator 与最终答案检查；只将可验证正确的轨迹标记为 selector 可用。

## 本轮实现

- 新增保守的 `GoalCheckerV3`，区分目标不支持、目标未到达、值未消元、答案不可解析、答案正确和答案错误。
- 新增 V3 全量回放与首失败诊断，导出每步 `state_before/state_after`、binding、delta、evidence 及当前可用定理集合。
- 修复无依据将命名圆心设为原点的问题。
- 修复普通变量 `a/b` 被误认作圆锥曲线参数的问题；显式变量值与参数别名优先。
- 支持 `a>b` 的结构化顺序信息和正性传播。
- 修复符号乘积取负未合并负号的问题，并支持标准圆锥式中的符号平方、倒数和正性判定。

## 全量结果

数据：`data/train_with_models_v3_candidate.json`，共 5,355 题。

| 指标 | 修复前 observed | 当前 observed | 修复前 executable | 当前 executable |
|---|---:|---:|---:|---:|
| 完整序列成功 | 360 (6.72%) | 458 (8.55%) | 431 (8.05%) | 530 (9.90%) |
| APPLIED 步数 | 4,614 | 5,928 | 5,131 | 6,443 |
| 可计算答案正确率 | 70/73 (95.89%) | 70/70 (100%) | 102/102 (100%) | 102/102 (100%) |
| selector 严格可用题 | 67 | 67 | 98 | 98 |
| 未解析 fact atom | 4,288 | 3,867 | 4,288 | 3,867 |

严格可用定义：序列每一步均成功，最终目标可解析、可计算，并与标注答案等价。序列成功但目标不支持、未到达或仍含未消元符号的轨迹不会自动进入高置信训练集。

## 诊断结论

1. 本轮信息传播使 executable 完整成功增加 99 题、APPLIED 增加 1,312 步，没有新增错误答案。
2. 严格可用题仍为 98，说明新增成功主要停在符号值未消元或目标检查尚未覆盖，而非最终数值答案。
3. 当前前三个首失败为模型 5（1,045）、模型 2（608）、模型 3（553）。抽样显示其中混有大量标签错位，例如没有标准方程却把标准方程定理放在首步，不能通过放宽前提解决。
4. 共有 9 次 `CONFLICT`。审查未发现数值矛盾；主要原因是给定数值参数与定理生成的符号表达式尚不能通过代入证明等价。
5. 当前目标检查仅支持 2,053/5,355 题（38.34%）。`Expression`、`Range`、`Min/Max`、轨迹/方程类目标仍是主要未覆盖区。

## 下一轮优先级

### P0：受控符号代入与约束求解

统一 `SymbolValueOf`、`ParameterAlias`、`ParameterOf`，在 theorem postcondition 和 GoalChecker 比较前做有来源的代入归约。首批验收样本是本轮 9 个冲突以及 66 个 `VALUE_UNRESOLVED`；要求不通过猜测赋值，不把无法证明的一致性记作成功。

### P1：标签错位分类

对模型 5/2/3 的首失败样本分成：缺少必要输入、方向/曲线类型错误、定理位置错误、信息解析缺口。只有最后一类进入 applicator/adapter 开发，其余进入 V3 标签修复。

### P2：目标空间扩展

优先加入 `Expression(conic)`、简单 `Range` 和可直接从状态读取的 `Min/Max`，同时保持 unsupported 与 incorrect 分离。每种目标必须先有答案等价测试，再计入 selector 严格可用率。

## 产物

- `outputs/theorems_v2/v3_replay_observed_summary.json`
- `outputs/theorems_v2/v3_replay_observed_diagnostics.jsonl`
- `outputs/theorems_v2/v3_observed_state_trajectories.jsonl`
- `outputs/theorems_v2/v3_replay_executable_summary.json`
- `outputs/theorems_v2/v3_replay_executable_diagnostics.jsonl`
- `outputs/theorems_v2/v3_executable_state_trajectories.jsonl`

验证：54 条 unittest 全部通过，`src/theorems_v2`、`scripts/theorems_v2` 与 tests 均通过 `compileall`。