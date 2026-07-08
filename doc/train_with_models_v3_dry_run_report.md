# train_with_models_v3 多证据 Dry-run 报告

## 1. 目标与边界

本轮未生成或覆盖训练数据，只产出修复 manifest、汇总和人工审查样本。

修复器区分两套候选序列：

- models_v3_observed：只修复高置信错标和已验证的相邻重复；
- models_v3_executable：在 observed 基础上允许插入或前移真实返回 APPLIED 的声明依赖。

NO_MATCH 不作为删除标签的依据。语义漂移模型不自动重写，只标记并建议 selector_weight=0。

## 2. 多证据规则

自动替换必须满足：

1. 原模型当前不可执行；
2. 同族候选中只有一个返回 APPLIED；
3. 候选对应的实体类型唯一存在；
4. 跨曲线类型替换时，原模型对应的实体类型必须完全不存在。

小样本首次运行发现同时含 Ellipse 与 Parabola 的题会产生 3→7 假替换，因此增加第 4 条约束。通用点差法 44 与具体点差法 45/46 也从 sibling replacement 中移除。

依赖补全必须同时满足：

- dependency 出现在 predicate-level requirement 中；
- dependency executor 在当前 state 返回 APPLIED；
- 插入只进入 executable；
- 若依赖原本位于后方，则记录为 move，而不是重复插入。

## 3. 数据规模

- 原始数据：7,757 行；
- 含 models：5,359 行；
- 原始完整可回放：299 行。

## 4. Dry-run 结果

| 指标 | Original | Observed | Executable |
| --- | ---: | ---: | ---: |
| 完整可回放行 | 299 | 361 | 432 |
| APPLIED 步骤 | 4,157 | 4,618 | 5,235 |
| NO_MATCH 步骤 | 14,833 | 14,358 | 14,077 |
| SPECIFICATION_ONLY | 1,142 | 1,142 | 1,142 |

Executable 含新增依赖步骤，因此其 APPLIED 数量不能与原序列作严格同分母比较；完整可回放行数更适合比较。

候选变更：

- observed 修改 319 行；
- executable 相对 observed 修改 314 行；
- replace_misaligned_model：319 次，high confidence；
- remove_adjacent_duplicate：12 次，high confidence；
- insert_verified_dependency：341 次，medium confidence；
- move_dependency_before_consumer：8 次，medium confidence。

主要替换包括：

- 7→9：125；
- 3→4：55；
- 14→15：30；
- 7→8：25；
- 7→10：14；
- 5→6：13；
- 9→7：12；
- 6→5：10。

## 5. 语义漂移审计

剩余 1,142 个 specification-only 标签全部进入文本 cue 审计：

- likely_semantic_drift：945；
- legacy_semantics_unverified：197。

高风险集中在：

- model 63：291 条 likely drift；
- model 68：288 条 likely drift；
- model 77：211 条 likely drift；
- model 79：73 条 likely drift；
- model 71：43 条 likely drift。

cue 命中只说明文字可能提到该概念，不代表标签已经正确，因此两类状态目前都建议 selector_weight=0。

## 6. 质量候选

| Tier | Rows | 含义 |
| --- | ---: | --- |
| A | 361 | observed 完整可回放，无语义漂移和 adapter error |
| B | 71 | executable 补依赖后完整可回放 |
| C | 3,998 | 无明显漂移，但仍有 NO_MATCH 或信息缺口 |
| D | 929 | likely drift、adapter error 或严重不确定 |

A+B 共 432 行，可以作为 v3 高精度种子集，但暂不应代表完整训练分布。

## 7. 人工抽检方案

已按以下 bucket 分层抽样：

- 每一种 replacement pair；
- 每一种依赖 consumer；
- 每个 semantic model 和 drift 状态；
- 每桶最多 5 条，固定随机种子。

共 73 个 bucket、251 条样本。每条预留 review_decision 与 review_note 字段。

建议验收门槛：

- high-confidence replacement 抽检精度至少 98%；
- duplicate removal 精度 100%；
- dependency insertion / move 至少 95%，且确认是否应进入训练序列；
- semantic drift 不自动接受，只用于建立新 action taxonomy。

## 8. 下一步决策

建议先完成 251 条审查样本中的 replacement 和 dependency bucket。通过门槛后：

1. 自动接受通过审查的 high-confidence 规则；
2. executable 依赖补全保持独立字段；
3. 生成 train_with_models_v3_candidate.json，而不是直接替换 models；
4. 同时生成 A/B 高精度子集；
5. 对未通过的 replacement pair 整组禁用，而不是逐题打补丁。

本轮未修改 data/train_with_models_v2.json。
