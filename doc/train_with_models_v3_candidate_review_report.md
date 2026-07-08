# train_with_models_v3 Candidate 审查与验证报告

## 1. 审查方式

本轮使用三类证据审查 dry-run：

- typed state 与唯一可执行 sibling；
- 题面声明的曲线类型、方程方向和依赖对象；
- 文字解答中实际使用的公式、几何关系或代数策略。

共审查 73 个初始 bucket。审查过程中发现并修复三类规则问题：

1. 多曲线题中，不能把另一个曲线上的可执行模型当作原标签替代；
2. 通用点差法 44 与具体点差法 45/46 不是互斥 sibling；
3. 依赖自身 APPLIED 不足以证明补链有效，必须让 consumer 最终成功。

依赖补全现已改为事务式试跑，失败时整条临时依赖链回滚。该修正过滤了 107 个无效补链，同时保持完整可回放行数不变。

## 2. 审查后的操作决策

| 操作 | 数量 | 决策 |
| --- | ---: | --- |
| replace_misaligned_model | 319 | approve_observed |
| remove_adjacent_duplicate | 12 | approve_observed |
| insert_verified_dependency | 241 | approve_executable_only |
| move_dependency_before_consumer | 1 | approve_executable_only |

replacement 和 duplicate 可以进入 observed。依赖操作只进入 executable，不修改观察到的文字步骤。

## 3. 语义标签审查

剩余 1,142 个 legacy 漂移标签不再直接作为 theorem 强监督目标，selector weight 全部设为 0。

根据文字过程可映射为 namespaced action 的共有 625 次：

| Action | Count |
| --- | ---: |
| tactic.basic_inequality_bound | 160 |
| geometry.midpoint_midline_relation | 188 |
| geometry.incircle_incenter_relation | 29 |
| tactic.dimensionless_homogenization | 130 |
| tactic.area_equivalence | 21 |
| tactic.inequality_equality_condition | 19 |
| tactic.quadratic_extremum | 51 |
| tactic.feasibility_by_discriminant | 20 |
| geometry.trapezoid_midline_relation | 7 |

仍有 517 次无法由文字可靠确定，保留为 unresolved.legacy_model_ID。

这 625 个 action 目前是弱标注建议，不替换整数 models，也不进入 selector 强监督；它们可用于下一轮 action taxonomy 设计。

## 4. Candidate 数据结构

每条样本保留：

- models_legacy；
- models / models_v3_observed；
- models_v3_executable；
- model_actions_v3；
- selector_weights_v3；
- v3_quality；
- v3_repair。

原始字段全部保留。新文件共 7,757 行，与源数据逐行对应。

结构校验：

- models_legacy 与原始 models 完全一致；
- 319 行 observed 发生变化；
- 5,359 个有标签样本的 observed/action/weight 长度全部一致；
- 非法 model ID 为 0；
- selector weight 为 0 的漂移动作共 1,142 个；
- A/B 高精度子集 432 行。

## 5. Candidate 裸测

同一 QuantityTheoremLibraryV2 与 QuantityApplicatorV2 下：

| 指标 | v2 | v3 candidate observed |
| --- | ---: | ---: |
| 原始步骤 | 20,212 | 20,200 |
| APPLIED + ALREADY_KNOWN | 4,172 | 4,632 |
| 全步骤 apply 率 | 20.64% | 22.93% |
| concrete 步骤 apply 率 | 21.88% | 24.30% |
| 完整跑通题目 | 298 (5.56%) | 360 (6.72%) |
| 辅助纠错后完整跑通 | 490 (9.15%) | 493 (9.21%) |
| 后续 repair artifact 行 | 1,312 | 1,128 |

observed 的提升来自错位标签修正和重复删除，不包含 executable 中额外插入的依赖。

## 6. 使用建议

- theorem selector：使用 observed，按 selector_weights_v3 屏蔽 1,142 个漂移动作；
- applicator/序列训练：可使用 executable，但应保留 operation metadata；
- action taxonomy 实验：使用 model_actions_v3 中的 namespaced 弱标注；
- 高精度冒烟训练：使用 432 行 A/B 子集；
- 正式训练不应只使用 A/B 子集，否则曲线类型和定理分布会严重偏斜。

## 7. 当前 concern

v3 candidate 修复了确定性错位，但仍有大量 NO_MATCH。它们混合了：

- 信息解析尚未覆盖；
- 文字过程省略中间步骤；
- legacy 标签粒度过粗；
- 真正的错误标签。

因此 v3 candidate 可以作为新版工程基线，但不能宣称为人工金标准。后续应从 517 个 unresolved action 和高频 NO_MATCH 模型继续抽样，而不是继续自动删除标签。

原始 data/train_with_models_v2.json 未修改。
