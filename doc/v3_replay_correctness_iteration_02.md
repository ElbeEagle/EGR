# V3 正确性迭代 02：状态归约与目标验真

## 本轮目标

继续按最终正确性迭代，不以单纯 `APPLIED` 数量作为完成标准。本轮处理上一轮的符号值冲突，并扩大可严格验真的目标类型。

## 工程调整

### 状态归约

- 新增 `StateExpressionResolver`，只依据当前状态中的 `SymbolValueOf` 和 `ParameterOf` 递归归约表达式。
- 将 `a=4` 一类题目变量赋值记录为 `SymbolValueOf`，不再直接冒充圆锥参数；同时保留 `ParameterAlias` 供审计和查询。
- 参数读取、状态提交和 GoalChecker 使用同一归约规则。
- 模型 13 在离心率已经给定时保留给定值，只增加 `e*a=c` 的公式约束，避免重复写值造成伪冲突。

结果：上一轮 9 个 `CONFLICT` 全部消失；executable 完整成功从 530 增至 536。

### 目标验真

新增以下保守目标：

- `Expression(G)`：从 `ConicStandardForm` 重建多项式，支持方程整体非零倍数等价。
- `Expression(Asymptote(G))`：比较结构化渐近线族的绝对斜率。
- `Expression(Directrix(G))`、左右准线：比较结构化轴线及其位置。

若参数仍含未赋值符号，返回 `VALUE_UNRESOLVED`；不会读取原始题面表达式充当推导结果。

## 全量结果

数据集：`data/train_with_models_v3_candidate.json`，5,355 题。

| 指标 | 迭代 01 observed | 当前 observed | 迭代 01 executable | 当前 executable |
|---|---:|---:|---:|---:|
| 完整序列成功 | 458 | 464 | 530 | 536 |
| APPLIED 步数 | 5,928 | 5,940 | 6,443 | 6,455 |
| 目标支持率 | 38.34% | 55.67% | 38.34% | 55.67% |
| selector 严格可用题 | 67 | 135 | 98 | 168 |
| CONFLICT 首失败 | 7 | 0 | 7 | 0 |

严格可用仍要求：序列完整成功、目标可解释、结果可计算、与标注答案一致。

## 数据错误

新增验真发现两条事实与答案不一致，均已从严格轨迹排除：

- ID 887：事实 `x^2/36-y^2/9=1` 对应渐近线斜率 `1/2`，标签为 `3/4`。
- ID 1834：事实 `x^2-y^2=1` 对应右准线 `x=1/sqrt(2)`，标签和文字过程按另一条方程得到 `3/2`。

机器可读记录：`outputs/theorems_v2/v3_answer_mismatch_review.json`。

## 可直接训练的产物

- observed 严格轨迹：`outputs/theorems_v2/v3_observed_selector_usable_trajectories.jsonl`，135 题。
- executable 严格轨迹：`outputs/theorems_v2/v3_executable_selector_usable_trajectories.jsonl`，168 题。
- 完整成功轨迹仍单独保留，用于诊断，不应与严格轨迹混用。

## 下一轮建议

1. 优先修复模型 5、2、3 的首失败标签错位，区分“缺定理”与“缺信息”，不要继续放宽标准方程定理。
2. 为模型 21、28、29 等关系型 executor 增加可求解的 scoped equation，而非只输出展示对象。
3. 扩展简单距离、周长目标验真；必须继续区分 unsupported、unresolved 和 incorrect。
4. 对严格轨迹按“唯一适用/多定理可用”分层，训练 selector 时先使用唯一适用步骤作为高纯度子集。

验证：61 条 unittest 通过，相关源码、脚本和测试通过 `compileall`。